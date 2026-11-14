"""Tests SEC HTTP request construction with fake responses; DOES NOT call SEC."""
import pathlib,sys,json,copy,unittest,hashlib
from unittest.mock import patch
D=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(D))
from sec_evidence import verify
FIX=json.loads((D/'tests/fixtures/fictional_companyfacts.json').read_text())
CK='1234567890'
UA='FinanceCheck Lab RealContact@example.org'
class FakeResp:
  def __init__(self,body,ctype='application/json',status=200):
    self.body=body;self.headers={'Content-Type':ctype};self.status=status
  def __enter__(self):return self
  def __exit__(self,*a):return False
  def read(self,n=None):return self.body[:n]
class FakeOpener:
  def __init__(self,body,status=200,ctype='application/json'):
    self.body=body;self.status=status;self.ctype=ctype;self.url=None;self.ua=None
  def open(self,req,timeout):
    self.url=req.full_url;self.ua=req.get_header('User-agent');return FakeResp(self.body,self.ctype,self.status)
class TestMockSecHTTP(unittest.TestCase):
  def test_01_safe_sec_url_and_declared_ua(self):
    body=json.dumps(FIX).encode();f=FakeOpener(body)
    with patch.object(verify.urllib.request,'build_opener',return_value=f),patch.object(verify.time,'sleep'):
      doc,sha,when=verify._fetch_sec_companyfacts(CK,user_agent=UA)
    self.assertEqual(f.url,'https://data.sec.gov/api/xbrl/companyfacts/CIK1234567890.json')
    self.assertIn('example.org',f.ua)
    self.assertEqual(sha,hashlib.sha256(body).hexdigest())
    self.assertEqual(doc['entityName'],'Fictional Training Corporation')
  def test_02_wrong_content_type(self):
    f=FakeOpener(b'not json',ctype='text/html')
    with patch.object(verify.urllib.request,'build_opener',return_value=f):
      with self.assertRaisesRegex(verify.EvidenceError,'content type'):
        verify._fetch_sec_companyfacts(CK,user_agent=UA)
  def test_03_invalid_json(self):
    f=FakeOpener(b'{bad')
    with patch.object(verify.urllib.request,'build_opener',return_value=f):
      with self.assertRaisesRegex(verify.EvidenceError,'invalid JSON'):
        verify._fetch_sec_companyfacts(CK,user_agent=UA)
  def test_04_http_500(self):
    f=FakeOpener(b'{}',status=500)
    with patch.object(verify.urllib.request,'build_opener',return_value=f):
      with self.assertRaisesRegex(verify.EvidenceError,'non-200'):
        verify._fetch_sec_companyfacts(CK,user_agent=UA)
  def test_05_redirect_disallowed(self):
    from email.message import Message
    req=verify.urllib.request.Request(verify.sec_companyfacts_url(CK))
    with self.assertRaisesRegex(verify.EvidenceError,'redirected'):
      verify._NoRedirects().redirect_request(req,None,301,'Moved',Message(),'https://evil.example/personal')
  def test_06_live_disabled_by_default(self):
    with patch.dict(verify.os.environ,{'FINANCECHECK_ENABLE_SEC_LIVE':'0'}):
      with self.assertRaisesRegex(verify.EvidenceError,'disabled'):
        verify.verify_live_sec_claim(cik=CK,year=2025,as_of='2026-11-14',user_agent=UA)
  def test_07_fake_http_cannot_claim_document_inspected(self):
    fake=FakeOpener(json.dumps(FIX).encode())
    with patch.dict(verify.os.environ,{'FINANCECHECK_ENABLE_SEC_LIVE':'1'}),patch.object(verify.urllib.request,'build_opener',return_value=fake):
      result=verify.verify_live_sec_claim(cik=CK,year=2025,as_of='2026-11-14',user_agent=UA)
    self.assertFalse(result['current_fact']['direct_filing_document_inspected'])
    self.assertIn('NOT_FILING_PAGES_INSPECTED',result['source_authentication'])
    self.assertTrue(result['human_review_required'])
  def test_08_malicious_cik_rejected_before_fetch(self):
    with patch.dict(verify.os.environ,{'FINANCECHECK_ENABLE_SEC_LIVE':'1'}):
      with self.assertRaisesRegex(verify.EvidenceError,'CIK'):
        verify.verify_live_sec_claim(cik='evil.com',year=2025,as_of='2026-11-14',user_agent=UA)

if __name__=='__main__':unittest.main()
