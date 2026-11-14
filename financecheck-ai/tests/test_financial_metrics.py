import unittest, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from engine.financial_metrics import calculate

class FinancialMetrics(unittest.TestCase):
    def sample(self):
        return dict(currency="USD", current_period="2025", prior_period="2024", revenue_current="120", revenue_prior="100")
    def test_growth(self):
        self.assertEqual(calculate(self.sample())["value"], "20.0000")
    def test_decline(self):
        a=self.sample(); a["revenue_current"]="80"; self.assertEqual(calculate(a)["value"], "-20.0000")
    def test_zero_base(self):
        a=self.sample(); a["revenue_prior"]=0; self.assertRaises(ValueError,calculate,a)
    def test_missing(self):
        a=self.sample(); del a["revenue_current"]; self.assertRaises(ValueError,calculate,a)
    def test_currency(self):
        a=self.sample(); a["currency"]="XYZ"; self.assertRaises(ValueError,calculate,a)
    def test_nan(self):
        a=self.sample(); a["revenue_current"]="NaN"; self.assertRaises(ValueError,calculate,a)
    def test_period(self):
        a=self.sample(); a["current_period"]="2024"; self.assertRaises(ValueError,calculate,a)
    def test_unverified(self):
        self.assertEqual(calculate(self.sample())["evidence_status"],"USER_SUPPLIED_UNVERIFIED")

if __name__=="__main__": unittest.main()
