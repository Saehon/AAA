"""V3.4 regression tests for professional routing and research-code provenance.

No live external network, professional body approval, Google service access,
financial record processing, or competitor method copying.
"""
import unittest, json, pathlib, sys
R=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
from professional.router import professional_route, public_big4_comparison
from research.safe_discovery import audit_research_asset, research_scout, co_scientist_review

GOOD=dict(title='Fictional replication artifact',record_url='https://zenodo.org/records/9999',asset_type='code',license='MIT',source_inspected=True,license_inspected=True)
PROPOSAL=dict(title='Public filing tag ambiguity',question='Do taxonomy extensions predict reporting corrections?', hypotheses=['H1: More extension tags predict more revisions.'],data_source='SEC filings + public XBRL',identification_strategy='Firm and year fixed effects with placebo tests')

class ProfessionalRouting(unittest.TestCase):
 def test_01_source_count(self):self.assertEqual(len(json.loads((R/'professional/professional_bodies.json').read_text())['bodies']),12)
 def test_02_iia_cia(self):self.assertIn('IIA 2024',professional_route(jurisdiction='Sweden',domain='internal_audit',credential='CIA_IIA')['primary_authority_candidate'])
 def test_03_sec_issuer(self):self.assertIn('PCAOB',professional_route(jurisdiction='US',domain='external_audit',listed_issuer=True,credential='CPA_US_AICPA')['primary_authority_candidate'])
 def test_04_nonissuer(self):self.assertNotIn('PCAOB',professional_route(jurisdiction='US',domain='external_audit',listed_issuer=False)['primary_authority_candidate'])
 def test_05_eu_ifrs(self):self.assertIn('IFRS',professional_route(jurisdiction='Sweden',domain='financial_reporting')['primary_authority_candidate'])
 def test_06_sustainability(self):self.assertIn('ESRS',professional_route(jurisdiction='EU',domain='sustainability')['primary_authority_candidate'])
 def test_07_cfe_not_fraud_verdict(self):self.assertFalse(professional_route(jurisdiction='UK',domain='fraud',credential='CFE_ACFE')['assurance_opinion'])
 def test_08_no_local_adoption(self):self.assertFalse(professional_route(jurisdiction='Sweden',domain='sustainability')['local_adoption_verified'])
 def test_09_unknown_body(self):
  with self.assertRaises(ValueError):professional_route(jurisdiction='UK',domain='internal_audit',credential='FAKE')
 def test_10_unknown_domain(self):
  with self.assertRaises(ValueError):professional_route(jurisdiction='UK',domain='aerospace')
 def test_11_bad_issuer(self):
  with self.assertRaises(ValueError):professional_route(jurisdiction='US',domain='external_audit',listed_issuer='true')
 def test_12_big4_four(self):self.assertEqual(len(public_big4_comparison(['PwC','EY','KPMG','Deloitte'])['resources']),4)
 def test_13_big4_not_authority(self):self.assertFalse(public_big4_comparison(['PwC'])['standards_replaced'])
 def test_14_big4_no_inspection(self):self.assertFalse(public_big4_comparison(['KPMG'])['guidance_inspected_for_current_case'])
 def test_15_fake_firm(self):
  with self.assertRaises(ValueError):public_big4_comparison(['Acme'])
 def test_16_duplicate_firm(self):
  with self.assertRaises(ValueError):public_big4_comparison(['PwC','PwC'])
 def test_17_university_ten_unranked(self):
  x=json.loads((R/'research/university_theses_sources.json').read_text());self.assertEqual(len(x['repositories']),10);self.assertIn('NOT AN OFFICIAL',x['ranking'])
 def test_18_no_licensed_standard_content(self):self.assertFalse((R/'professional/AICPA_FULL_STANDARDS.pdf').exists())

class ResearchQuality(unittest.TestCase):
 def test_19_manual_review_required(self):self.assertFalse(audit_research_asset(GOOD)['reuse_permitted'])
 def test_20_no_code_execution(self):self.assertFalse(audit_research_asset(GOOD)['code_executed'])
 def test_21_unlicensed_rejected(self):self.assertEqual(audit_research_asset({**GOOD,'license':'unknown'})['status'],'NEEDS_SOURCE_OR_LICENSE_REVIEW')
 def test_22_missing_review(self):self.assertEqual(audit_research_asset({**GOOD,'license_inspected':False})['status'],'NEEDS_SOURCE_OR_LICENSE_REVIEW')
 def test_23_sensitive_flag(self):self.assertEqual(audit_research_asset({**GOOD,'contains_personal_data':True})['status'],'BLOCKED')
 def test_24_untrusted_executable(self):self.assertEqual(audit_research_asset({**GOOD,'untrusted_executable':True})['status'],'BLOCKED')
 def test_25_bad_extra(self):
  with self.assertRaises(ValueError):audit_research_asset({**GOOD,'secret_key':'bad'})
 def test_26_http_link(self):
  with self.assertRaises(ValueError):audit_research_asset({**GOOD,'record_url':'http://example.org'})
 def test_27_doi_syntax(self):self.assertTrue(audit_research_asset({**GOOD,'doi':'10.1234/naail-paper.1'})['doi_syntax_valid_not_resolved'])
 def test_28_doi_invalid(self):
  with self.assertRaises(ValueError):audit_research_asset({**GOOD,'doi':'foo-bar'})
 def test_29_discovery_not_search(self):self.assertFalse(research_scout(topic='audit data study')['search_executed'])
 def test_30_ft50_not_all_papers(self):self.assertIn('names only',research_scout(topic='audit data study')['ft50_register_status'])
 def test_31_ajg_subset(self):self.assertIn('subset',research_scout(topic='audit data study')['ajg4_register_status'])
 def test_32_bad_platform(self):
  with self.assertRaises(ValueError):research_scout(topic='audit data study',platforms=['S&P Capital IQ'])
 def test_33_bad_window(self):
  with self.assertRaises(ValueError):research_scout(topic='audit data study',years=0)
 def test_34_workflow_has_six_tasks(self):self.assertEqual(len(co_scientist_review(PROPOSAL)['tasks']),6)
 def test_35_no_google_service(self):self.assertFalse(co_scientist_review(PROPOSAL)['google_alphaevolve_called'])
 def test_36_no_actual_agent_execution(self):self.assertEqual(co_scientist_review(PROPOSAL)['agent_execution'],'NOT_RUN_WORKFLOW_SPECIFICATION')
 def test_37_no_novelty_proof(self):self.assertFalse(co_scientist_review(PROPOSAL)['novelty_verified'])
 def test_38_no_hypothesis_assertion(self):self.assertIsNone(co_scientist_review(PROPOSAL)['hypothesis_supported'])
 def test_39_no_hypotheses(self):
  with self.assertRaises(ValueError):co_scientist_review({**PROPOSAL,'hypotheses':[]})
 def test_40_no_secret_inputs(self):
  with self.assertRaises(ValueError):co_scientist_review({**PROPOSAL,'private_client_data':'no'})
 def test_41_ft50_50_existing(self):self.assertEqual(len(json.loads((R/'research/ft50_2026_registry.json').read_text())['journals']),50)
 def test_42_quality_source_13(self):self.assertEqual(len(json.loads((R/'research/free_source_catalog.json').read_text())['sources']),13)
 def test_43_skills_46(self):self.assertEqual(len(list((R/'skills').glob('*/SKILL.md'))),46)
 def test_44_all_urls_https(self):
  for p in [R/'professional/professional_bodies.json',R/'professional/big4_public_guidance.json',R/'research/free_source_catalog.json',R/'research/university_theses_sources.json']:
   obj=json.loads(p.read_text());data=obj.get('bodies',obj.get('firms',obj.get('sources',obj.get('repositories',[]))))
   self.assertTrue(all(x['url'].startswith('https://') for x in data))
 def test_45_pcaob_not_equated_with_sustainability(self):
  r=professional_route(jurisdiction='USA',domain='sustainability',credential='CPA_US_AICPA');self.assertNotIn('PCAOB auditing standards for SEC issuer audits',r['primary_authority_candidate'])
 def test_47_replication_leads_three(self):
  x=json.loads((R/'research/verified_replication_leads.json').read_text());self.assertEqual(len(x['leads']),3);self.assertFalse(x['executed'])
 def test_46_no_certification(self):
  for d in ['financial_reporting','external_audit','internal_audit','sustainability','fraud']:
   self.assertFalse(professional_route(jurisdiction='USA',domain=d)['professional_certification'])

if __name__=='__main__':unittest.main()
