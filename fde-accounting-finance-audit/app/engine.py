"""No generative model is used to calculate screening results."""
from calendar import monthrange
from collections import Counter, defaultdict, deque
from decimal import Decimal
from uuid import uuid4

from .schemas import (
    AuditRequest, AuditResponse, FinanceRequest, FinanceResponse, Finding,
    ReconciliationRequest, ReconciliationResponse,
)

def _trace() -> str:
    return str(uuid4())

def assess_audit(req: AuditRequest) -> AuditResponse:
    findings: list[Finding] = []
    references = Counter(e.reference for e in req.entries if e.reference)
    sequence = 0

    def flag(entry, rule_id, severity, description, action):
        nonlocal sequence
        sequence += 1
        findings.append(Finding(
            finding_id=f"F-{sequence:04d}",
            entry_id=entry.entry_id,
            rule_id=rule_id,
            severity=severity,
            description=description,
            evidence_refs=[entry.evidence_id] if entry.evidence_id else [],
            recommended_action=action,
        ))

    for entry in req.entries:
        debit = sum((line.debit for line in entry.lines), Decimal("0"))
        credit = sum((line.credit for line in entry.lines), Decimal("0"))
        if abs(debit - credit) > req.policy.reconciliation_tolerance:
            flag(entry, "JE-001", "high", "Journal debits and credits do not balance.",
                 "Inspect source ledger and correct only through approved adjusting entries.")
        if not entry.evidence_id:
            flag(entry, "JE-002", "medium", "No linked support document identifier.",
                 "Request and independently verify contemporaneous support.")
        if entry.approved_by and entry.posted_by.casefold() == entry.approved_by.casefold():
            flag(entry, "JE-003", "high", "Preparer and approver identifiers match.",
                 "Investigate approval workflow and segregation-of-duties exceptions.")
        month_last = monthrange(entry.posted_on.year, entry.posted_on.month)[1]
        if entry.is_manual and month_last - entry.posted_on.day <= req.policy.period_end_window_days:
            flag(entry, "JE-004", "medium", "Manual entry posted near month-end.",
                 "Examine authorization, purpose, reversal, cutoff and source evidence.")
        if entry.is_manual and max(debit, credit) >= req.policy.screening_materiality:
            flag(entry, "JE-005", "medium", "Manual entry exceeds configured screening threshold.",
                 "Review business rationale and evidence; threshold is not audit materiality.")
        if entry.reference and references[entry.reference] > 1:
            flag(entry, "JE-006", "medium", "Reference appears in multiple journal entries.",
                 "Determine whether repeated references reflect legitimate splits or duplication.")

    # An interpretable, intentionally uncalibrated screening index, NOT fraud likelihood.
    weighted = sum({"low": 1, "medium": 3, "high": 7}[f.severity] for f in findings)
    index = min(100, weighted * 2)
    return AuditResponse(trace_id=_trace(), currency=req.currency,
                         entries_reviewed=len(req.entries), screening_index=index,
                         findings=findings)

def assess_finance(req: FinanceRequest) -> FinanceResponse:
    signals = []
    ratio = None
    if req.current_liabilities > 0:
        ratio_value = req.current_assets / req.current_liabilities
        ratio = f"{ratio_value:.2f}"
        if ratio_value < 1:
            signals.append("Current ratio below 1.0; investigate liquidity and classification.")
    else:
        signals.append("Current ratio undefined because current liabilities are zero.")
    runway = None
    if req.monthly_cash_burn > 0:
        runway_value = req.cash_balance / req.monthly_cash_burn
        runway = f"{runway_value:.2f}"
        if runway_value < 3:
            signals.append("Cash runway below three months at stated burn rate.")
    else:
        signals.append("Cash runway not meaningful when monthly cash burn is zero.")
    if req.operating_cash_flow < 0:
        signals.append("Negative operating cash flow; review trend and cash conversion.")
    return FinanceResponse(trace_id=_trace(), current_ratio=ratio,
                           cash_runway_months=runway, signals=signals)

def reconcile(req: ReconciliationRequest) -> ReconciliationResponse:
    # Multimap + removal guarantees one-to-one matches even with repeated values.
    ledger = defaultdict(deque)
    for transaction in req.ledger:
        ledger[(transaction.reference, transaction.amount)].append(transaction.transaction_id)
    pairs = []
    unmatched_bank = []
    used_ledger = set()
    for transaction in req.bank:
        matches = ledger.get((transaction.reference, transaction.amount))
        if matches:
            ledger_id = matches.popleft()
            used_ledger.add(ledger_id)
            pairs.append({"bank_id": transaction.transaction_id, "ledger_id": ledger_id})
        else:
            unmatched_bank.append(transaction.transaction_id)
    unmatched_ledger = [t.transaction_id for t in req.ledger if t.transaction_id not in used_ledger]
    return ReconciliationResponse(
        trace_id=_trace(), matched_pairs=pairs,
        unmatched_bank_ids=unmatched_bank, unmatched_ledger_ids=unmatched_ledger,
    )
