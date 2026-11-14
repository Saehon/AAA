import pathlib,sys, tempfile,unittest,csv
D=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(D))
from evaluation.benchmark import evaluate,STRATA,wilson_95,make_sampling_plan

def gold(n=1):
 return [{'case_id':f'case{i}', 'stratum':'revenue_growth','gold_verdict':'SUPPORTED',
          'annotators':['Reviewer_A','Reviewer_B'],'label_status':'ADJUDICATED','source_reviewed':True} for i in range(n)]
def pred(n=1,verdict='SUPPORTED'):
 return [{'case_id':f'case{i}', 'predicted_verdict':verdict} for i in range(n)]

class TestBench(unittest.TestCase):
 def test_01_proposal_200(self):self.assertEqual(sum(STRATA.values()),200)
 def test_02_plan_unlabelled(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'plan.csv';make_sampling_plan(p)
   with p.open(encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
   self.assertEqual(len(rows),200)
   self.assertTrue(all(x['label_status']=='TO_COLLECT' and not x['gold_verdict'] for x in rows))
 def test_03_cannot_fake_200(self):
  with self.assertRaisesRegex(ValueError,'requires 200'):evaluate(gold(),pred())
 def test_04_requires_double_labels(self):
  g=gold();g[0]['annotators']=['A']
  with self.assertRaisesRegex(ValueError,'Two independent'):evaluate(g,pred(),require_200=False)
 def test_05_requires_adjudicated(self):
  g=gold();g[0]['label_status']='PLANNED'
  with self.assertRaisesRegex(ValueError,'Unadjudicated'):evaluate(g,pred(),require_200=False)
 def test_06_cannot_claim_uninspected(self):
  g=gold();g[0]['source_reviewed']=False
  with self.assertRaisesRegex(ValueError,'manually reviewed'):evaluate(g,pred(),require_200=False)
 def test_07_accurate_small_protocol_test(self):self.assertEqual(evaluate(gold(),pred(),require_200=False)['overall_accuracy'],1.0)
 def test_08_inaccurate_small_protocol_test(self):self.assertEqual(evaluate(gold(),pred(verdict='CONTRADICTED'),require_200=False)['overall_accuracy'],0)
 def test_09_missing_prediction_zero(self):self.assertEqual(evaluate(gold(2),pred(1),require_200=False)['overall_accuracy'],0.5)
 def test_10_false_support(self):
  g=gold();g[0]['gold_verdict']='CONTRADICTED'
  self.assertEqual(evaluate(g,pred(),require_200=False)['false_support_rate_among_supported_predictions'],1.0)
 def test_11_abstention(self):self.assertEqual(evaluate(gold(),pred(verdict='INSUFFICIENT_EVIDENCE'),require_200=False)['nonabstention_fraction'],0)
 def test_12_bad_prediction_verdict(self):
  with self.assertRaisesRegex(ValueError,'unsupported verdict'):evaluate(gold(),pred(verdict='FABRICATED'),require_200=False)
 def test_13_duplicate_ids(self):
  with self.assertRaisesRegex(ValueError,'unique'):evaluate(gold(1),pred(1)+pred(1),require_200=False)
 def test_14_unknown_pred(self):
  with self.assertRaisesRegex(ValueError,'not present'):evaluate(gold(),[{'case_id':'wrong','predicted_verdict':'SUPPORTED'}],require_200=False)
 def test_15_wilson(self):
  r=wilson_95(5,10)
  self.assertTrue(r['low']<.5<r['high'])
 def test_16_zero_total(self):self.assertIsNone(wilson_95(0,0))
 def test_17_citation_unmeasured(self):
  self.assertIn('NOT_MEASURED',evaluate(gold(),pred(),require_200=False)['citation_accuracy'])
 def test_18_fake_200_unbalanced(self):
  with self.assertRaisesRegex(ValueError,'40 cases'):evaluate(gold(200),pred(200),require_200=True)

if __name__=='__main__':unittest.main()
