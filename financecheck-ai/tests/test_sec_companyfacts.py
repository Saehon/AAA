import unittest,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from engine.sec_companyfacts import select_annual_revenues,retrieve_companyfacts
def row(year,val,filed=None):
    return dict(start=f"{year-1}-01-01",end=f"{year}-01-01",filed=filed or f"{year}-03-01",fy=year,fp="FY",form="10-K",val=val,accn=f"0000-{year}")
def data(rows):return {"facts":{"us-gaap":{"Revenues":{"units":{"USD":rows}}}}}
class SECOfflineTests(unittest.TestCase):
    def test_growth(self):self.assertEqual(select_annual_revenues(data([row(2024,100),row(2025,125)]),"2025-12-31")[0]["growth_percent"],"25.0000")
    def test_cutoff(self):
        with self.assertRaises(ValueError):select_annual_revenues(data([row(2024,100),row(2025,125)]),"2025-01-01")
    def test_restatement(self):self.assertEqual(select_annual_revenues(data([row(2024,100),row(2025,125),row(2025,140,"2025-05-01")]),"2025-12-31")[0]["growth_percent"],"40.0000")
    def test_ambiguity(self):
        with self.assertRaises(ValueError):select_annual_revenues(data([row(2024,100),row(2025,125),row(2025,140)]),"2025-12-31")
    def test_negative(self):
        with self.assertRaises(ValueError):select_annual_revenues(data([row(2024,-100),row(2025,125)]),"2025-12-31")
    def test_cik(self):
        with self.assertRaises(ValueError):retrieve_companyfacts("../evil","Researcher researcher@example.org")
    def test_user_agent(self):
        with self.assertRaises(ValueError):retrieve_companyfacts("123","bad")
if __name__=="__main__":unittest.main()
