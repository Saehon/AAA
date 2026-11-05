"""Deterministic contract and control tests; all data are invented."""
from decimal import Decimal
from fastapi.testclient import TestClient

from app.engine import assess_audit, assess_finance, reconcile
from app.main import app
from app.schemas import AuditRequest, FinanceRequest, ReconciliationRequest

client = TestClient(app)

def _entry(entry_id="JE1", reference="INV-1", approved_by="maker", evidence_id=None):
    return {
        "entry_id": entry_id, "posted_on": "2026-10-31",
        "posted_by": "maker", "approved_by": approved_by,
        "is_manual": True, "reference": reference, "evidence_id": evidence_id,
        "lines": [
            {"account": "1100", "debit": "12000", "credit": "0"},
            {"account": "4000", "debit": "0", "credit": "11900"},
        ],
    }

def test_audit_flags_and_evidence_trace():
    request = AuditRequest.model_validate({"entries": [_entry()]})
    result = assess_audit(request)
    assert result.requires_human_review
    assert {"JE-001", "JE-002", "JE-003", "JE-004", "JE-005"} <= {f.rule_id for f in result.findings}
    assert all(f.evidence_refs == [] for f in result.findings)
    assert 0 < result.screening_index <= 100

def test_duplicate_reference_is_flagged_on_both_entries():
    req = AuditRequest.model_validate({"entries": [
        _entry(entry_id="JE1", evidence_id="DOC-A"),
        _entry(entry_id="JE2", evidence_id="DOC-B"),
    ]})
    out = assess_audit(req)
    assert len([f for f in out.findings if f.rule_id == "JE-006"]) == 2

def test_balanced_standard_entry_has_no_findings():
    entry = _entry(approved_by="supervisor", evidence_id="DOC-1")
    entry["posted_on"] = "2026-10-15"
    entry["is_manual"] = False
    entry["lines"][1]["credit"] = "12000"
    out = assess_audit(AuditRequest.model_validate({"entries": [entry]}))
    assert not out.findings and out.screening_index == 0

def test_finance_non_division_and_risk_flags():
    out = assess_finance(FinanceRequest(
        current_assets=Decimal("80"), current_liabilities=Decimal("100"),
        cash_balance=Decimal("10"), monthly_cash_burn=Decimal("5"),
        operating_cash_flow=Decimal("-3"),
    ))
    assert out.current_ratio == "0.80"
    assert out.cash_runway_months == "2.00"
    assert len(out.signals) == 3

def test_reconciliation_is_exact_one_to_one():
    req = ReconciliationRequest.model_validate({
        "bank": [
            {"transaction_id":"B1","reference":"R","amount":"20"},
            {"transaction_id":"B2","reference":"R","amount":"20"},
        ],
        "ledger": [
            {"transaction_id":"L1","reference":"R","amount":"20"},
        ],
    })
    out = reconcile(req)
    assert out.matched_pairs == [{"bank_id":"B1","ledger_id":"L1"}]
    assert out.unmatched_bank_ids == ["B2"]
    assert out.unmatched_ledger_ids == []

def test_api_validation_and_model_gate(monkeypatch):
    monkeypatch.delenv("DEMO_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LLM", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    assert client.get("/healthz").status_code == 200
    assert client.post("/v1/audit/assess", json={"entries":[]}).status_code == 422
    body = {"findings":[{
        "finding_id":"F-0001", "entry_id":"JE1","rule_id":"JE-002",
        "severity":"medium","description":"Evidence missing",
        "evidence_refs":[],"recommended_action":"Request evidence"
    }],"data_classification":"synthetic"}
    assert client.post("/v1/ai/draft-review", json=body).status_code == 503

def test_demo_key_blocks_unauthorized_calls(monkeypatch):
    monkeypatch.setenv("DEMO_API_KEY", "only-for-tests")
    assert client.post("/v1/finance/assess", json={
        "current_assets": 100, "current_liabilities": 50,
        "cash_balance": 10, "monthly_cash_burn": 1, "operating_cash_flow": 0,
    }).status_code == 401
    assert client.post("/v1/finance/assess", headers={"X-API-Key": "only-for-tests"}, json={
        "current_assets": 100, "current_liabilities": 50,
        "cash_balance": 10, "monthly_cash_burn": 1, "operating_cash_flow": 0,
    }).status_code == 200

def test_malformed_line_and_duplicate_entry_rejected():
    payload={"entries":[_entry(),_entry(entry_id="JE1")]}
    assert client.post("/v1/audit/assess",json=payload).status_code == 422
    payload={"entries":[_entry()]}
    payload["entries"][0]["lines"][0]["credit"]="1"
    assert client.post("/v1/audit/assess",json=payload).status_code == 422
