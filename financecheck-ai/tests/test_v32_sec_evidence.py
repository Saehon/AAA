"""Independent synthetic SEC-shaped source-matching and provenance tests.

All SEC-shaped fact data in fixtures is fictional. NO REAL SEC NETWORK CALLS.
"""
import json,copy,os,unittest, pathlib,sys,subprocess
from unittest.mock import patch
D=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(D))
from sec_evidence.verify import (verify_revenue_yoy,sec_companyfacts_url,verify_live_sec_claim,evidence_story_card,
                                 EvidenceError,ALLOWED_CONCEPTS, _fetch_sec_companyfacts)
from sec_evidence.mcp_stdio import handle,TOOLS
FIX=json.loads((D/'tests/fixtures/fictional_companyfacts.json').read_text())
CK='1234567890'
UA='FinanceCheck NAAIL Research financecheck@example.org'

def check(doc=None,**kw):
    d=copy.deepcopy(doc if doc is not None else FIX)
    args=dict(cik=CK,year=2025,as_of='2026-11-14',claimed_percentage='20')
    args.update(kw)
    return verify_revenue_yoy(d,**args)

def fact_list(d):
    return d['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD']

class TestSECSource(unittest.TestCase):
    def test_01_yoy(self):
        r=check();self.assertEqual(r['change_percentage'],'20.00')
    def test_02_verdict_consistent(self):self.assertEqual(check()['claim_verdict'],'CONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES')
    def test_03_verdict_conflicts(self):self.assertEqual(check(claimed_percentage='22')['claim_verdict'],'INCONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES')
    def test_04_verdict_tolerance(self):self.assertEqual(check(claimed_percentage='20.04')['claim_verdict'],'CONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES')
    def test_05_no_claim(self):self.assertEqual(check(claimed_percentage=None)['claim_verdict'],'NO_CLAIM_SUPPLIED')
    def test_06_synthetic_not_auth(self):self.assertEqual(check()['source_authentication'],'NOT_INDEPENDENTLY_VERIFIED')
    def test_07_fictional_no_real_sec_url(self):self.assertIsNone(check()['previous_fact']['filing_archive_directory'])
    def test_08_concept_exact(self):self.assertEqual(check()['concept']['tag'],'RevenueFromContractWithCustomerExcludingAssessedTax')
    def test_09_no_filings_no_verification(self):
        d=copy.deepcopy(FIX);fact_list(d).clear()
        with self.assertRaises(EvidenceError):check(d)
    def test_10_10q_excluded(self):
        d=copy.deepcopy(FIX);fact_list(d)[1]['form']='10-Q'
        with self.assertRaises(EvidenceError):check(d)
    def test_11_wrong_duration_rejected(self):
        d=copy.deepcopy(FIX);fact_list(d)[1]['start']='2025-07-01'
        with self.assertRaises(EvidenceError):check(d)
    def test_12_asof_filing_excluded(self):
        with self.assertRaises(EvidenceError):check(as_of='2025-12-31')
    def test_13_no_future_as_of(self):
        with self.assertRaises(EvidenceError):check(as_of='2040-01-01')
    def test_14_wrong_cik(self):
        with self.assertRaisesRegex(EvidenceError,'identifier'):check(cik='320193')
    def test_15_bad_cik(self):
        with self.assertRaises(EvidenceError):check(cik='https://evil.com')
    def test_16_bad_concept(self):
        with self.assertRaises(EvidenceError):check(concept='ProfitInvented')
    def test_17_filing_end_not_fy(self):
        d=copy.deepcopy(FIX)
        for f in fact_list(d):f['fy']=1999
        self.assertEqual(check(d)['change_percentage'],'20.00')
    def test_18_regression_restated_conflict(self):
        d=copy.deepcopy(FIX); f=copy.deepcopy(fact_list(d)[0]);f.update(val=95000000,accn='1234567890-26-000010',filed='2026-03-20');fact_list(d).append(f)
        r=check(d)
        self.assertEqual(r['claim_verdict'],'INSUFFICIENT_EVIDENCE_REVIEW_REQUIRED')
        self.assertTrue(r['historical_value_conflicts']['2024'])
    def test_19_same_filing_conflict(self):
        d=copy.deepcopy(FIX);f=copy.deepcopy(fact_list(d)[0]);f['val']=99000000;fact_list(d).append(f)
        with self.assertRaisesRegex(EvidenceError,'inconsistent'):check(d)
    def test_20_two_concepts_ambiguous(self):
        d=copy.deepcopy(FIX)
        d['facts']['us-gaap']['Revenues']=copy.deepcopy(d['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax'])
        with self.assertRaisesRegex(EvidenceError,'Multiple revenue concepts'):check(d)
    def test_21_choose_exact_tag(self):
        d=copy.deepcopy(FIX)
        d['facts']['us-gaap']['Revenues']=copy.deepcopy(d['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax'])
        self.assertEqual(check(d,concept='Revenues')['concept']['tag'],'Revenues')
    def test_22_zero_base_unsupported(self):
        d=copy.deepcopy(FIX);fact_list(d)[0]['val']=0
        with self.assertRaisesRegex(EvidenceError,'zero'):check(d)
    def test_23_wrong_currency_no_match(self):
        d=copy.deepcopy(FIX);d['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']={'EUR':fact_list(d)}
        with self.assertRaises(EvidenceError):check(d)
    def test_24_source_url_whitelisted(self):
        self.assertEqual(sec_companyfacts_url('320193'),'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json')
    def test_25_no_external_host(self):
        with self.assertRaises(EvidenceError):sec_companyfacts_url('data.sec.gov/api?redirect=evil')
    def test_26_opt_in_gate_off(self):
        with patch.dict(os.environ,{'FINANCECHECK_ENABLE_SEC_LIVE':'0'}):
            with self.assertRaisesRegex(EvidenceError,'disabled'):verify_live_sec_claim(cik=CK,year=2025,as_of='2026-11-14')
    def test_27_missing_contact_rejected(self):
        with self.assertRaisesRegex(EvidenceError,'User-Agent'):_fetch_sec_companyfacts(CK,user_agent='bot')
    def test_28_mcp_three_fields_required(self):
        r=handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'inspect_sec_xbrl_revenue_yoy','arguments':{'cik':CK}}})
        self.assertEqual(r['error']['code'],-32602)
    def test_29_mcp_tool_read_only(self):self.assertTrue(TOOLS[0]['annotations']['readOnlyHint'])
    def test_30_mcp_missing_live_error(self):
        with patch.dict(os.environ,{'FINANCECHECK_ENABLE_SEC_LIVE':'0'}):
            r=handle({'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'inspect_sec_xbrl_revenue_yoy','arguments':{'cik':CK,'year':2025,'as_of':'2026-11-14'}}})
        self.assertTrue(r['result']['isError'])
        self.assertNotIn('VERIFIED',str(r['result']))
    def test_31_mcp_tool_listing(self):
        self.assertEqual(handle({'jsonrpc':'2.0','id':5,'method':'tools/list'})['result']['tools'][0]['name'],'inspect_sec_xbrl_revenue_yoy')
    def test_32_notification_no_response(self):self.assertIsNone(handle({'jsonrpc':'2.0','method':'notifications/initialized'}))
    def test_33_mcp_stdio_round_trip(self):
        source=[{'jsonrpc':'2.0','id':1,'method':'initialize'},
                {'jsonrpc':'2.0','id':2,'method':'tools/list'}]
        c=subprocess.run([sys.executable,'-m','sec_evidence.mcp_stdio'],input='\n'.join(map(json.dumps,source))+'\n',capture_output=True,text=True,cwd=D,timeout=5,check=True)
        lines=[json.loads(s) for s in c.stdout.splitlines()]
        self.assertEqual([x['id'] for x in lines],[1,2])
    def test_34_existing_clarification(self):self.assertFalse(check()['current_fact']['direct_filing_document_inspected'])
    def test_35_private_flag_no_filing(self):self.assertTrue(check()['human_review_required'])

class TestSECSourceAdditions(unittest.TestCase):
    def test_36_story_fictional_label(self):
        card=evidence_story_card(check())
        self.assertIn('FICTIONAL',card['badge_text'])
    def test_37_story_not_present_verified(self):
        self.assertEqual(evidence_story_card(check())['share_status'],'DO_NOT_PRESENT_AS_VERIFIED')
    def test_38_story_three_cards(self):self.assertEqual(len(evidence_story_card(check())['cards']),3)
    def test_39_story_no_fixture_links(self):self.assertEqual(evidence_story_card(check())['links'],[])
    def test_40_story_requires_provenance(self):
        with self.assertRaises(EvidenceError):evidence_story_card({'change_percentage':'20'})
    def test_41_story_source_metadata(self):self.assertIn('uncertain',evidence_story_card(check())['cards'][2]['title'].lower())
    def test_42_conflicts_flagged_to_public(self):
        d=copy.deepcopy(FIX); f=copy.deepcopy(fact_list(d)[0]);f.update(val=95000000,accn='1234567890-26-000010',filed='2026-03-20');fact_list(d).append(f)
        self.assertIn('REVIEW',evidence_story_card(check(d))['badge_text'])
    def test_43_fake_liveresponse_requires_provenance(self):
        with self.assertRaisesRegex(EvidenceError,'configured SEC fetch path'):
            check(provenance='SEC_LIVE_RESPONSE')
    def test_44_stale_annual_fiscal_gap(self):
        d=copy.deepcopy(FIX);fact_list(d)[1]['start']='2025-01-20'
        with self.assertRaisesRegex(EvidenceError,'calendars'):check(d)
    def test_45_untrusted_offline_caller_cannot_forge_live(self):
        with self.assertRaisesRegex(EvidenceError,'configured SEC fetch path'):
            check(provenance='SEC_LIVE_RESPONSE',payload_sha256='0'*64,retrieval_time='2026-11-14T12:00:00+00:00')
    def test_46_not_credible_fake_urls_on_fixture(self):
        r=check();self.assertIsNone(r['retrieval_url'])
    def test_47_inflated_source_claim_blocked(self):
        with self.assertRaises(EvidenceError):check(provenance='DIRECT_10K_VERIFIED')

if __name__=='__main__':unittest.main()
