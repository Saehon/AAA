"""Source-aware revenue arithmetic over SEC XBRL companyfacts.

Standard library only. Uses no third-party data. The *live* SEC fetch is opt-in
and runs only in an explicitly authorized backend; no network call at import.
The evidence grade is SEC_EXTRACTED_XBRL (not direct filing-page inspection).
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP
import hashlib
import json
import os
import re
import time
import threading
import urllib.error
import urllib.request
from typing import Any

SEC_URL_ROOT = "https://data.sec.gov/api/xbrl/companyfacts/"
USER_AGENT_ENV = "FINANCECHECK_SEC_USER_AGENT"
MAX_JSON_BYTES = 32_000_000
_SEC_ACCESS_LOCK=threading.Lock()
_LAST_SEC_ACCESS=0.0
MIN_REPORT_DAYS = 330
MAX_REPORT_DAYS = 380
_NETWORK_PROVENANCE_CAPABILITY = object()  # Internal marker, not cryptographic attestation
ALLOWED_CONCEPTS = (
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
)
ACC_RE = re.compile(r"^\d{10}-\d{2}-\d{6}$")
CIK_RE = re.compile(r"^\d{1,10}$")

class EvidenceError(ValueError):
    """Validation error with a stable safe public message."""

def safe_cik(raw: Any) -> str:
    if isinstance(raw, bool):
        raise EvidenceError("CIK must be a 1–10 digit SEC identifier")
    s = str(raw).strip()
    if not CIK_RE.fullmatch(s) or int(s) == 0:
        raise EvidenceError("CIK must be a 1–10 digit SEC identifier")
    return s.zfill(10)

def sec_companyfacts_url(cik: Any) -> str:
    return SEC_URL_ROOT + "CIK" + safe_cik(cik) + ".json"

def safe_date(s: Any) -> date:
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        raise EvidenceError("Expected ISO date YYYY-MM-DD")
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise EvidenceError("Invalid reporting or filing date") from None

def number(v: Any) -> Decimal:
    if isinstance(v, bool) or v is None or isinstance(v, (list, dict)):
        raise EvidenceError("Fact value is not a finite numeric quantity")
    try:
        x = Decimal(str(v))
    except (InvalidOperation, ValueError):
        raise EvidenceError("Fact value is not a finite numeric quantity") from None
    if not x.is_finite() or abs(x) > Decimal("1e18"):
        raise EvidenceError("Fact value is outside supported finite range")
    return x

@dataclass(frozen=True)
class Fact:
    concept: str
    amount: Decimal
    unit: str
    start: str
    end: str
    filed: str
    accession: str
    form: str

    def public(self, cik: str, *, include_archive_url: bool) -> dict[str, Any]:
        return {
            "concept": self.concept,
            "amount": str(self.amount),
            "unit": self.unit,
            "start": self.start, "end": self.end,
            "filed": self.filed, "accession": self.accession,
            "form": self.form,
            "filing_archive_directory": ((
                "https://www.sec.gov/Archives/edgar/data/"
                + str(int(cik)) + "/" + self.accession.replace("-", "") + "/"
            ) if include_archive_url else None),
            "direct_filing_document_inspected": False,
        }

def all_annual_facts(doc: dict[str, Any], *, cik: str, year: int, concept: str,
                     as_of: date, unit: str = "USD") -> list[Fact]:
    """Only exact-tag 10-K/10-K-A annual durations; no imputed frame/fy shortcut."""
    if not isinstance(doc, dict) or not isinstance(doc.get("facts"), dict):
        raise EvidenceError("Companyfacts response has no supported SEC facts structure")
    try:
        found_cik = safe_cik(doc.get("cik"))
    except EvidenceError:
        raise EvidenceError("Companyfacts response has invalid issuer CIK") from None
    if found_cik != cik:
        raise EvidenceError("Companyfacts issuer identifier does not match requested CIK")
    if concept not in ALLOWED_CONCEPTS:
        raise EvidenceError("Unsupported or ambiguous revenue concept")
    raw = doc.get("facts", {}).get("us-gaap", {}).get(concept, {}).get("units", {}).get(unit, [])
    if not isinstance(raw, list):
        raise EvidenceError("SEC concept unit container is malformed")
    valid: list[Fact] = []
    for item in raw:
        if not isinstance(item, dict) or item.get("form") not in ("10-K", "10-K/A"):
            continue
        try:
            start, end, filed = (safe_date(item.get(k)) for k in ("start", "end", "filed"))
            acc = item.get("accn")
            if not isinstance(acc, str) or not ACC_RE.fullmatch(acc):
                continue
            if end.year != year or not MIN_REPORT_DAYS <= (end-start).days+1 <= MAX_REPORT_DAYS:
                continue
            if filed < end or filed > as_of:
                continue
            value = number(item.get("val"))
            if value < 0:
                continue
        except EvidenceError:
            continue
        valid.append(Fact(concept, value, unit, start.isoformat(), end.isoformat(),
                          filed.isoformat(), acc, item["form"]))
    return valid

def latest_unique_filing_facts(facts: list[Fact], *, year: int) -> tuple[Fact, list[Fact]]:
    if not facts:
        raise EvidenceError(f"No eligible audited-filing annual revenue facts for {year}")
    # The latest filing date and accession determine a single filing context.
    # Restated comparisons from earlier filings are retained in provenance.
    latest_filing = max((f.filed, f.accession) for f in facts)
    current_filing = [f for f in facts if (f.filed, f.accession) == latest_filing]
    distinct = {(f.start, f.end, f.amount) for f in current_filing}
    if len(distinct) != 1:
        raise EvidenceError(f"Multiple inconsistent annual values in selected filing for {year}")
    selected = current_filing[0]
    # Ensure a single end date within the year for the current reporting period;
    # inconsistent fiscal calendars are not quietly combined.
    for f in facts:
        if f.filed == selected.filed and f.accession == selected.accession and f.end != selected.end:
            raise EvidenceError(f"Ambiguous annual reporting end dates for {year}")
    return selected, facts

def _select_exact_concept(doc: dict[str, Any], cik: str, year: int, as_of: date,
                          concept: str | None) -> tuple[str, list[Fact], list[Fact]]:
    if concept is not None and concept not in ALLOWED_CONCEPTS:
        raise EvidenceError("Unsupported revenue concept; request an exact US-GAAP tag")
    if concept is not None:
        p = all_annual_facts(doc, cik=cik, year=year-1, concept=concept, as_of=as_of)
        q = all_annual_facts(doc, cik=cik, year=year, concept=concept, as_of=as_of)
        if not p or not q:
            raise EvidenceError("The requested exact revenue concept is absent for one of the years")
        return concept, p, q
    matches: list[tuple[str,list[Fact],list[Fact]]] = []
    for tag in ALLOWED_CONCEPTS:
        p=all_annual_facts(doc,cik=cik,year=year-1,concept=tag,as_of=as_of)
        q=all_annual_facts(doc,cik=cik,year=year,concept=tag,as_of=as_of)
        if p and q: matches.append((tag,p,q))
    if not matches:
        raise EvidenceError("No comparable exact-tag annual revenue facts for both years")
    if len(matches)>1:
        raise EvidenceError("Multiple revenue concepts are available: choose one exact US-GAAP concept")
    return matches[0]

def verify_revenue_yoy(doc: dict[str,Any], *, cik: Any, year: int,
                       as_of: str, claimed_percentage: str | int | float | None = None,
                       concept: str | None = None, provenance: str = "SYNTHETIC_FIXTURE",
                       payload_sha256: str | None = None,
                       retrieval_time: str | None = None,
                       _network_capability: object | None = None) -> dict[str,Any]:
    """Evaluates a fact claim against a *known* SEC-shaped document. Never boosts fixtures to SEC status."""
    cik_id=safe_cik(cik)
    if isinstance(year,bool) or not isinstance(year,int) or not 2009 <= year <= 2026:
        raise EvidenceError("Year must be between 2009 and 2026")
    cutoff=safe_date(as_of)
    if cutoff > datetime.now(timezone.utc).date():
        raise EvidenceError("As-of date cannot be in the future")
    if year > cutoff.year:
        raise EvidenceError("Comparison period is after the selected as-of date")
    if provenance not in ("SYNTHETIC_FIXTURE", "SEC_LIVE_RESPONSE"):
        raise EvidenceError("Unrecognized evidence provenance")
    if provenance == "SEC_LIVE_RESPONSE":
        if _network_capability is not _NETWORK_PROVENANCE_CAPABILITY:
            raise EvidenceError("Live source status may only be assigned by the configured SEC fetch path")
        if not payload_sha256 or not retrieval_time:
            raise EvidenceError("Live provenance requires captured payload hash and retrieval time")
    tag, old, new = _select_exact_concept(doc,cik_id,year,cutoff,concept)
    f0, all0 = latest_unique_filing_facts(old,year=year-1)
    f1, all1 = latest_unique_filing_facts(new,year=year)
    # Compare fiscal-year boundaries and retained annual durations (52/53-week friendly).
    start_gap=(safe_date(f1.start)-safe_date(f0.end)).days
    if not -3 <= start_gap <= 10:
        raise EvidenceError("Reporting period calendars are not comparable")
    if abs((safe_date(f1.end)-safe_date(f0.end)).days-365)>38:
        raise EvidenceError("Annual reporting end dates are not reasonably comparable")
    if f0.amount == 0:
        raise EvidenceError("Prior-year revenue is zero; percentage growth is undefined")
    if f0.amount < 0:
        raise EvidenceError("Negative prior-year revenue is unsupported")
    with localcontext() as ctx:
        ctx.prec=50
        pct=(f1.amount-f0.amount)/f0.amount*Decimal(100)
        pct_2=pct.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        difference=f1.amount-f0.amount
    conflict0=len({f.amount for f in all0})>1
    conflict1=len({f.amount for f in all1})>1
    if conflict0 or conflict1:
        # A changed comparison amount in another 10-K cannot be disregarded.
        decision="HUMAN_REVIEW_REQUIRED_RESTATED_OR_CONFLICTING_VALUES"
    else:
        decision="CALCULATED_FROM_EXTRACTED_FACTS"
    claimed=None
    if claimed_percentage is not None:
        claimed=number(claimed_percentage)
        if claimed < Decimal("-100") or claimed>Decimal("1000000"):
            raise EvidenceError("Claimed growth exceeds supported range")
        if decision.startswith("HUMAN_REVIEW"):
            verdict="INSUFFICIENT_EVIDENCE_REVIEW_REQUIRED"
        else:
            verdict=("CONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES" if abs(claimed-pct)<=Decimal("0.05") else
                     "INCONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES")
    else:
        verdict="NO_CLAIM_SUPPLIED"
    is_live=(provenance=="SEC_LIVE_RESPONSE")
    return {
        "issuer_cik":cik_id,
        "issuer_name":str(doc.get("entityName", ""))[:150],
        "metric":"annual_revenue_yoy",
        "period_previous":year-1, "period_current":year,
        "concept":{"taxonomy":"us-gaap","tag":tag,"unit":"USD"},
        "previous_fact":f0.public(cik_id, include_archive_url=is_live),"current_fact":f1.public(cik_id, include_archive_url=is_live),
        "change_value":str(difference),"change_percentage":str(pct_2),
        "claimed_percentage":str(claimed) if claimed is not None else None,
        "claim_verdict":verdict,
        "selection_status":decision,
        "historical_value_conflicts": {str(year-1):conflict0,str(year):conflict1},
        "evidence_source":"OFFICIAL_SEC_XBRL_COMPANYFACTS_API" if is_live else "SYNTHETIC_SEC_SHAPED_FIXTURE",
        "source_authentication":"SEC_API_RESPONSE_RETRIEVED_NOT_FILING_PAGES_INSPECTED" if is_live else "NOT_INDEPENDENTLY_VERIFIED",
        "retrieval_url":sec_companyfacts_url(cik_id) if is_live else None,
        "retrieval_utc":retrieval_time if is_live else None,
        "payload_sha256":payload_sha256 if is_live else None,
        "as_of":cutoff.isoformat(),
        "human_review_required":True,
        "limitations":("SEC machine-extracted public XBRL facts, NOT the underlying filed PDF/HTML text; "
                       "facts may be restated, non-comparable or incompletely tagged; "
                       "no accounting assurance, fraud finding or investment advice."),
    }

class _NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise EvidenceError("SEC endpoint redirected unexpectedly; no source evidence authenticated")

def _fetch_sec_companyfacts(cik: Any, *, user_agent: str, timeout: float = 12) -> tuple[dict[str,Any],str,str]:
    """One SEC API request; caller must enforce global <10 req/s, here 1 req per call."""
    if not isinstance(user_agent,str) or len(user_agent)<12 or not re.search(r"\S+@\S+\.\S+",user_agent):
        raise EvidenceError("SEC requests require a descriptive User-Agent with a real contact email")
    url=sec_companyfacts_url(cik)
    req=urllib.request.Request(url,headers={"User-Agent":user_agent,"Accept":"application/json"},method="GET")
    global _LAST_SEC_ACCESS
    # This process limits itself to one SEC request per second (well below the
    # published 10 requests/second maximum); distributed deployments require a
    # shared limiter in front of the worker pool.
    with _SEC_ACCESS_LOCK:
        delay=1.0-(time.monotonic()-_LAST_SEC_ACCESS)
        if delay > 0:
            time.sleep(delay)
        _LAST_SEC_ACCESS=time.monotonic()
    try:
        opener=urllib.request.build_opener(_NoRedirects())
        with opener.open(req,timeout=timeout) as resp:
            if resp.status != 200:
                raise EvidenceError("SEC returned a non-200 response")
            content_type=resp.headers.get("Content-Type","")
            if "json" not in content_type.lower():
                raise EvidenceError("Unexpected SEC response content type")
            body=resp.read(MAX_JSON_BYTES+1)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError):
        raise EvidenceError("SEC retrieval failed; no company fact was verified") from None
    if len(body)>MAX_JSON_BYTES:
        raise EvidenceError("SEC payload exceeded configured maximum size")
    try: payload=json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError,json.JSONDecodeError):
        raise EvidenceError("SEC returned invalid JSON") from None
    return payload,hashlib.sha256(body).hexdigest(),datetime.now(timezone.utc).isoformat(timespec="seconds")

def verify_live_sec_claim(*,cik:Any,year:int,as_of:str,concept:str|None=None,
                          claimed_percentage:str|int|float|None=None,user_agent:str|None=None)->dict[str,Any]:
    """Explicit opt-in live fetch, never enabled by plugin skill alone."""
    if os.getenv("FINANCECHECK_ENABLE_SEC_LIVE")!="1":
        raise EvidenceError("Live SEC mode is disabled; provide an approved backend and explicitly enable it")
    ua=user_agent or os.getenv(USER_AGENT_ENV,"")
    doc,sha,when=_fetch_sec_companyfacts(cik,user_agent=ua)
    return verify_revenue_yoy(doc,cik=cik,year=year,as_of=as_of,concept=concept,
             claimed_percentage=claimed_percentage,provenance="SEC_LIVE_RESPONSE",
             payload_sha256=sha,retrieval_time=when,
             _network_capability=_NETWORK_PROVENANCE_CAPABILITY)

def evidence_story_card(result: dict[str,Any]) -> dict[str,Any]:
    """Customer-facing 3-step summary with data/source status never hidden."""
    required={'change_percentage','period_previous','period_current','concept','source_authentication',
              'selection_status','issuer_name','previous_fact','current_fact'}
    if not isinstance(result,dict) or not required <= set(result):
        raise EvidenceError('Expected evaluated, source-labeled result')
    pct=number(result['change_percentage'])
    headline=('Revenue increased' if pct>0 else 'Revenue decreased' if pct<0 else 'Revenue was unchanged')
    live=result['source_authentication']=='SEC_API_RESPONSE_RETRIEVED_NOT_FILING_PAGES_INSPECTED'
    conflicted=result['selection_status'].startswith('HUMAN_REVIEW')
    label=('SEC XBRL SOURCE EXTRACTED — FULL FILING NOT INSPECTED' if live else
           'FICTIONAL TEST DATA — NOT REAL COMPANY EVIDENCE')
    if conflicted:label='REVIEW NEEDED: HISTORICAL VALUES CONFLICT'
    return {
       'headline':headline,
       'badge_text':label,
       'figure':str(result['change_percentage'])+'%',
       'share_status': ('DO_NOT_PRESENT_AS_VERIFIED' if not live or conflicted else
                        'SOURCE_LINKED_ONLY_NOT_AUDIT_ASSURANCE'),
       'cards':[
           {'step':1,'title':'What changed?',
            'body':f"Revenue for the selected exact XBRL tag changed {result['change_percentage']}% between fiscal periods {result['period_previous']} and {result['period_current']}."},
           {'step':2,'title':'What is the source?',
            'body':('SEC Company Facts API accession-linked extracted financial tags' if live else
                    'Constructed, fictional SEC-shaped testing records')},
           {'step':3,'title':'What is still uncertain?',
            'body':'Underlying 10-K text, full accounting context, footnotes, comparability and restatements require professional review.'}
       ],
       'links':[result.get('retrieval_url')] if live else [],
       'source_label':label,
       'accessions':[result['previous_fact']['accession'],result['current_fact']['accession']] if live else [],
       'disclaimer':'Educational financial evidence review only; no investment advice, audit assurance or fraud conclusion.'
    }
