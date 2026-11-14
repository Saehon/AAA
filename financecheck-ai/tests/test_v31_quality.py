"""V3.1 quality-regression tests: source labels, comparable periods, minimal input schemas."""
import importlib.util, pathlib, unittest
P=pathlib.Path(__file__).resolve().parents[1]/'mcp_lab/server.py'
spec=importlib.util.spec_from_file_location('qa_mcp_v31',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
GOOD={'classification':'synthetic','previous':'100','current':'120','period_previous':'2024','period_current':'2025','currency':'SEK'}
class QualityGate(unittest.TestCase):
 def test_01_annual_good(self):self.assertEqual(m.calculate(GOOD)['percentage_change'],'20.00')
 def test_02_reverse_year_blocked(self):
  with self.assertRaisesRegex(ValueError,'consecutive'):m.calculate({**GOOD,'period_previous':'2025','period_current':'2024'})
 def test_03_cross_frequency_blocked(self):
  with self.assertRaisesRegex(ValueError,'same quarter'):m.calculate({**GOOD,'period_current':'2025-Q1'})
 def test_04_quarter_mismatch_blocked(self):
  with self.assertRaisesRegex(ValueError,'same quarter'):m.calculate({**GOOD,'period_previous':'2024-Q1','period_current':'2025-Q2'})
 def test_05_quarter_yoy_pass(self):self.assertEqual(m.calculate({**GOOD,'period_previous':'2024-Q1','period_current':'2025-Q1'})['percentage_change'],'20.00')
 def test_06_nonadjacent_year_blocked(self):
  with self.assertRaisesRegex(ValueError,'consecutive'):m.calculate({**GOOD,'period_current':'2027'})
 def test_07_four_letter_currency_rejected(self):
  with self.assertRaisesRegex(ValueError,'three-letter'):m.calculate({**GOOD,'currency':'TEST'})
 def test_08_uppercase_currency_normalized(self):self.assertEqual(m.calculate({**GOOD,'currency':'sek'})['currency'],'SEK')
 def test_09_currency_is_only_format_checked(self):self.assertEqual(m.calculate(GOOD)['currency_code_status'],'FORMAT_ONLY_NOT_AUTHENTICATED')
 def test_10_unknown_payload_blocked(self):
  with self.assertRaisesRegex(ValueError,'unsupported fields'):m.calculate({**GOOD,'bank_account':'example fake account'})
 def test_11_invalid_flag_type_blocked(self):
  with self.assertRaisesRegex(ValueError,'booleans'):m.calculate({**GOOD,'private_drive':'false'})
 def test_12_boolean_flag_rejected(self):
  with self.assertRaisesRegex(ValueError,'BLOCKED'):m.calculate({**GOOD,'contains_personal_data':True})
 def test_13_tool_schemas_closed(self):self.assertTrue(all(t['inputSchema']['additionalProperties'] is False for t in m.TOOLS))
 def test_14_tool_annotations(self):self.assertTrue(all(t['annotations']=={'readOnlyHint':True,'destructiveHint':False,'openWorldHint':False} for t in m.TOOLS))
 def test_15_no_false_source(self):self.assertEqual(m.calculate(GOOD)['source_status'],'NOT_INDEPENDENTLY_INSPECTED')
 def test_16_public_story_unverified(self):self.assertEqual(m.story({**GOOD,'classification':'public'})['share_status'],'REQUIRES_ORIGINAL_SOURCE_REVIEW')
 def test_17_invalid_future_history(self):
  with self.assertRaisesRegex(ValueError,'consecutive'):m.calculate({**GOOD,'period_previous':'2026','period_current':'2025'})
 def test_18_valid_fiscal_year_format(self):self.assertEqual(m.calculate({**GOOD,'period_previous':'FY2024','period_current':'FY2025'})['percentage_change'],'20.00')
 def test_19_not_huge_numeric_ratio(self):
  with self.assertRaisesRegex(ValueError,'precision'):m.calculate({**GOOD,'previous':'0.000000000000001'})
 def test_20_not_expose_unknown_data_in_error(self):
  try:m.calculate({**GOOD,'PRIVATE_BANK_ACCOUNT_SECRET':'do-not-repeat'})
  except ValueError as e:self.assertNotIn('do-not-repeat',str(e))
 def test_21_term_reject_extra(self):
  with self.assertRaisesRegex(ValueError,'unsupported fields'):m.explain({'classification':'synthetic','term':'revenue','personal':'unused'})
 def test_22_mcp_three_read_only_tools(self):self.assertEqual(len(m.TOOLS),3)
if __name__=='__main__':unittest.main()
