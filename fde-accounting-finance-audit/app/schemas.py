"""Versioned inputs/outputs: deterministic, inspectable, human-review-oriented."""
from datetime import date
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class LedgerLine(BaseModel):
    account: str = Field(min_length=1, max_length=80)
    debit: Decimal = Field(default=Decimal("0"), ge=0)
    credit: Decimal = Field(default=Decimal("0"), ge=0)

    @model_validator(mode="after")
    def one_side(self):
        if self.debit > 0 and self.credit > 0:
            raise ValueError("A ledger line cannot debit and credit simultaneously")
        return self

class JournalEntry(BaseModel):
    entry_id: str = Field(min_length=1, max_length=80)
    posted_on: date
    posted_by: str = Field(min_length=1, max_length=80)
    approved_by: str | None = None
    is_manual: bool = False
    reference: str | None = None
    evidence_id: str | None = None
    lines: list[LedgerLine] = Field(min_length=2, max_length=100)

class AuditPolicy(BaseModel):
    screening_materiality: Decimal = Field(default=Decimal("10000"), gt=0)
    period_end_window_days: int = Field(default=3, ge=0, le=7)
    reconciliation_tolerance: Decimal = Field(default=Decimal("0.01"), ge=0, le=1)

class AuditRequest(BaseModel):
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    policy: AuditPolicy = Field(default_factory=AuditPolicy)
    entries: list[JournalEntry] = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def unique_entries(self):
        ids = [e.entry_id for e in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("entry_id must be unique")
        return self

class Finding(BaseModel):
    finding_id: str
    entry_id: str
    rule_id: str
    severity: Literal["low", "medium", "high"]
    description: str
    evidence_refs: list[str]
    recommended_action: str

class AuditResponse(BaseModel):
    trace_id: str
    currency: str
    entries_reviewed: int
    screening_index: int
    findings: list[Finding]
    requires_human_review: bool = True
    methodology: str = "Deterministic screening rules; not a fraud probability or audit opinion."

class FinanceRequest(BaseModel):
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    current_assets: Decimal = Field(ge=0)
    current_liabilities: Decimal = Field(ge=0)
    cash_balance: Decimal = Field(ge=0)
    monthly_cash_burn: Decimal = Field(ge=0)
    operating_cash_flow: Decimal

class FinanceResponse(BaseModel):
    trace_id: str
    current_ratio: str | None
    cash_runway_months: str | None
    signals: list[str]
    requires_human_review: bool = True

class BankTransaction(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=80)
    reference: str = Field(min_length=1, max_length=80)
    amount: Decimal

class LedgerTransaction(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=80)
    reference: str = Field(min_length=1, max_length=80)
    amount: Decimal

class ReconciliationRequest(BaseModel):
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    bank: list[BankTransaction] = Field(max_length=5000)
    ledger: list[LedgerTransaction] = Field(max_length=5000)

class ReconciliationResponse(BaseModel):
    trace_id: str
    matched_pairs: list[dict[str, str]]
    unmatched_bank_ids: list[str]
    unmatched_ledger_ids: list[str]
    requires_human_review: bool = True
    matching_policy: str = "Exact reference and exact amount; one-to-one, no fuzzy matching."

class ExplanationRequest(BaseModel):
    findings: list[Finding] = Field(min_length=1, max_length=25)
    data_classification: Literal["synthetic", "approved_nonconfidential"]
    reviewer_context: str = Field(default="", max_length=300)
