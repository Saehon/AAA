import unittest, json, pathlib
from standards.advisory import assurance_transition,reporting_version,double_materiality_triage,evidence_passport
ROOT=pathlib.Path(__file__).resolve().parents[1]
class SustainabilityQuality(unittest.TestCase):
 def test_01_ghg_pre(self):self.assertEqual(assurance_transition('2026-01-01',subject='GHG')['candidate'],'ISAE_3410_GHG_HISTORICAL_CONTEXT')
 def test_02_ghg_post(self):self.assertEqual(assurance_transition('2027-01-01',subject='GHG')['candidate'],'ISSA_5000_IAASB_BASELINE')
 def test_03_exact_switch(self):self.assertEqual(assurance_transition('2026-12-15',subject='GHG')['candidate'],'ISSA_5000_IAASB_BASELINE')
 def test_04_as_at(self):self.assertEqual(assurance_transition('2026-01-01',subject='GHG',as_at='2026-12-15')['candidate'],'ISSA_5000_IAASB_BASELINE')
 def test_05_jurisdiction_not_automatically_verified(self):self.assertFalse(assurance_transition('2027-01-01',subject='GHG',jurisdiction='Canada')['jurisdiction_adoption_verified'])
 def test_06_financial_audit_separate(self):self.assertEqual(assurance_transition('2027-01-01',subject='financial_audit')['candidate'],'FINANCIAL_AUDIT_STANDARDS_SEPARATE')
 def test_07_bad_subject(self):
  with self.assertRaises(ValueError):assurance_transition('2027-01-01',subject='untrusted')
 def test_08_bad_date(self):
  with self.assertRaises(ValueError):assurance_transition('2027-19-99',subject='GHG')
 def test_09_esrs_2026(self):self.assertEqual(reporting_version('2026-01-01',jurisdiction='EU',framework='ESRS')['candidate_version'],'EU_2026_TRANSITION_OPTION_CHECK_REQUIRED')
 def test_10_esrs_2027(self):self.assertEqual(reporting_version('2027-01-01',jurisdiction='EU',framework='ESRS')['candidate_version'],'REVISED_ESRS_2026_BASELINE')
 def test_11_s2_2026(self):self.assertEqual(reporting_version('2026-01-01',jurisdiction='global',framework='IFRS_S2_GHG_AMENDMENTS')['candidate_version'],'PRE_2027_AMENDMENTS')
 def test_12_s2_2027(self):self.assertEqual(reporting_version('2027-01-01',jurisdiction='global',framework='IFRS_S2_GHG_AMENDMENTS')['candidate_version'],'AMENDED_IFRS_S2')
 def test_13_s2_early(self):self.assertEqual(reporting_version('2026-01-01',jurisdiction='global',framework='IFRS_S2_GHG_AMENDMENTS',early_adoption=True)['candidate_version'],'AMENDED_IFRS_S2')
 def test_14_no_auto_compliance(self):self.assertFalse(reporting_version('2027-01-01',jurisdiction='EU',framework='ESRS')['mandatory_applicability_verified'])
 def test_15_materiality_no_binary_decision(self):self.assertIsNone(double_materiality_triage({'topic':'climate','impact_evidence':True,'financial_evidence':True})['materiality_decision'])
 def test_16_materiality_both_lenses(self):self.assertEqual(set(double_materiality_triage({'topic':'climate','impact_evidence':True,'financial_evidence':True})['potential_dimensions']),{'impact','financial'})
 def test_17_materiality_reject_bad_extra(self):
  with self.assertRaises(ValueError):double_materiality_triage({'topic':'x','personal_id':'123'})
 def test_18_materiality_missing_sources(self):self.assertIn('source_url',double_materiality_triage({'topic':'x'})['missing_evidence'])
 def test_19_passport_not_independent(self):
  p={'claim':'CO2','framework':'S2','report_period':'FY2025','source_url':'https://example.org/x','source_inspected':True,'evidence_type':'public_source'}
  self.assertFalse(evidence_passport(p)['compliance_certified'])
 def test_20_passport_reject_http(self):
  with self.assertRaises(ValueError):evidence_passport({'claim':'x','framework':'S2','report_period':'FY2025','source_url':'http://bad','source_inspected':True,'evidence_type':'public_source'})
 def test_21_ft50_has_50(self):self.assertEqual(len(json.loads((ROOT/'research/ft50_2026_registry.json').read_text())['journals']),50)
 def test_22_ajg_not_claim_complete(self):self.assertIn('NOT the complete',json.loads((ROOT/'research/ajg2024_verified_accounting_finance_subset.json').read_text())['scope'])
 def test_23_fta_jbe_removed(self):self.assertNotIn('Journal of Business Ethics',json.loads((ROOT/'research/ft50_2026_registry.json').read_text())['journals'])
 def test_24_fta_add_ama(self):self.assertIn('Academy of Management Annals',json.loads((ROOT/'research/ft50_2026_registry.json').read_text())['journals'])
 def test_25_standard_registry(self):self.assertEqual(len(json.loads((ROOT/'standards/authority_registry.json').read_text())['standards']),6)
 def test_26_no_certification_claim(self):
  for s in json.loads((ROOT/'standards/authority_registry.json').read_text())['standards']:self.assertIn('verification',s)
 def test_27_s2_jurisdiction(self):self.assertFalse(reporting_version('2027-01-01',jurisdiction='EU',framework='ISSB_S1_S2')['mandatory_applicability_verified'])
 def test_28_more_than_30_skills(self):self.assertEqual(len(list((ROOT/'skills').glob('*/SKILL.md'))),35)
 def test_29_standards_text_not_bundled(self):self.assertFalse((ROOT/'standards/IFRS_S1_FULL_STANDARD.pdf').exists())
 def test_30_year_conditional_human_review(self):self.assertTrue(assurance_transition('2026-01-01',subject='GHG')['review_required'])
if __name__=='__main__':unittest.main()
