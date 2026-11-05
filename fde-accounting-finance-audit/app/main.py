"""Customer-facing demo API; not production-authenticated or certified."""
import hmac
import os

from fastapi import Depends, FastAPI, Header, HTTPException

from .engine import assess_audit, assess_finance, reconcile
from .llm import draft_explanation
from .schemas import (
    AuditRequest, AuditResponse, FinanceRequest, FinanceResponse,
    ReconciliationRequest, ReconciliationResponse, ExplanationRequest,
)

app = FastAPI(
    title="FDE | Accounting • Finance • Audit",
    version="0.1.0",
    description="Synthetic-data-ready rule-based workflows, evidence references, human review. "
                "A demonstration, not an audit opinion, fraud detector or production system.",
)

def demo_auth(x_api_key: str | None = Header(default=None)) -> None:
    configured = os.getenv("DEMO_API_KEY")
    if os.getenv("APP_ENV") == "production" and not configured:
        raise HTTPException(status_code=503, detail="Authentication is not configured")
    if configured and not hmac.compare_digest(x_api_key or "", configured):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": "0.1.0", "model_enabled": os.getenv("ENABLE_LLM") == "true"}

@app.post("/v1/audit/assess", response_model=AuditResponse, dependencies=[Depends(demo_auth)])
def audit_assess(request: AuditRequest):
    return assess_audit(request)

@app.post("/v1/finance/assess", response_model=FinanceResponse, dependencies=[Depends(demo_auth)])
def finance_assess(request: FinanceRequest):
    return assess_finance(request)

@app.post("/v1/accounting/reconcile", response_model=ReconciliationResponse, dependencies=[Depends(demo_auth)])
def accounting_reconcile(request: ReconciliationRequest):
    return reconcile(request)

@app.post("/v1/ai/draft-review", dependencies=[Depends(demo_auth)])
def ai_draft(request: ExplanationRequest):
    return draft_explanation(request)
