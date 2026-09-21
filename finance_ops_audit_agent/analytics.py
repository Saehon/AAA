from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .schemas import AuditFinding, DeterministicAuditResult


REQUIRED_COLUMNS = {
    "transaction_id",
    "timestamp",
    "vendor",
    "amount",
    "currency",
    "requester",
    "approver",
    "account",
    "cost_center",
}

SEVERITY_WEIGHT = {"low": 3, "medium": 7, "high": 15, "critical": 25}


def _safe_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _evidence(row_index: int, row: pd.Series) -> str:
    return (
        f"row={row_index + 2}; transaction_id={_safe_text(row['transaction_id'])}; "
        f"vendor={_safe_text(row['vendor'])}; amount={row['amount']}; "
        f"timestamp={_safe_text(row['timestamp'])}; requester={_safe_text(row['requester'])}; "
        f"approver={_safe_text(row['approver'])}"
    )


def load_transactions(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Transaction file not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if df["amount"].isna().any():
        bad_rows = [int(i) + 2 for i in df.index[df["amount"].isna()].tolist()]
        raise ValueError(f"Non-numeric amount values at CSV rows: {bad_rows}")

    df["parsed_timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    return df


def _add_finding(
    findings: list[AuditFinding],
    rule_id: str,
    severity: str,
    title: str,
    rows: pd.DataFrame,
    rationale: str,
) -> None:
    if rows.empty:
        return
    evidence = [_evidence(int(idx), row) for idx, row in rows.iterrows()]
    tx_ids = sorted({_safe_text(v) for v in rows["transaction_id"].tolist() if _safe_text(v)})
    findings.append(
        AuditFinding(
            finding_id=f"F-{len(findings) + 1:03d}",
            rule_id=rule_id,
            severity=severity,
            title=title,
            transaction_ids=tx_ids,
            evidence=evidence,
            rationale=rationale,
        )
    )


def analyze_transactions(csv_path: str | Path) -> DeterministicAuditResult:
    """Run transparent, deterministic audit tests over a transaction population."""
    path = Path(csv_path)
    df = load_transactions(path)
    findings: list[AuditFinding] = []

    duplicate_mask = df["transaction_id"].astype(str).duplicated(keep=False)
    _add_finding(
        findings,
        "DUPLICATE_ID",
        "high",
        "Duplicate transaction identifiers",
        df[duplicate_mask],
        "Duplicate transaction identifiers can indicate duplicate processing, resubmission, or data-integrity problems and require source-document validation.",
    )

    approver = df["approver"].fillna("").astype(str).str.strip()
    requester = df["requester"].fillna("").astype(str).str.strip()

    _add_finding(
        findings,
        "MISSING_APPROVER",
        "high",
        "Missing approval evidence",
        df[approver.eq("")],
        "Transactions without an identified approver may not satisfy the expected authorization control.",
    )

    sod_mask = requester.ne("") & approver.ne("") & requester.str.casefold().eq(approver.str.casefold())
    _add_finding(
        findings,
        "SOD_CONFLICT",
        "critical",
        "Requester and approver are the same person",
        df[sod_mask],
        "The same requester and approver indicates a segregation-of-duties conflict that can enable control circumvention.",
    )

    valid_ts = df["parsed_timestamp"].notna()
    weekend_mask = valid_ts & df["parsed_timestamp"].dt.dayofweek.ge(5)
    _add_finding(
        findings,
        "WEEKEND_POSTING",
        "medium",
        "Weekend transaction posting",
        df[weekend_mask],
        "Weekend activity is not inherently improper, but it can be a useful contextual anomaly for follow-up.",
    )

    out_of_hours_mask = valid_ts & (
        df["parsed_timestamp"].dt.hour.lt(6) | df["parsed_timestamp"].dt.hour.ge(22)
    )
    _add_finding(
        findings,
        "OUT_OF_HOURS",
        "medium",
        "Out-of-hours transaction posting",
        df[out_of_hours_mask],
        "Posting outside ordinary working hours is a contextual anomaly and should be corroborated with business-process evidence.",
    )

    abs_amount = df["amount"].abs()
    median = float(abs_amount.median()) if len(df) else 0.0
    mad = float((abs_amount - median).abs().median()) if len(df) else 0.0
    if mad > 0:
        threshold = median + 6 * mad
    else:
        threshold = max(median * 5, 10_000.0)
    high_amount_mask = abs_amount.gt(threshold)
    _add_finding(
        findings,
        "ROBUST_AMOUNT_OUTLIER",
        "high",
        "Robust amount outlier",
        df[high_amount_mask],
        f"Absolute transaction amount exceeds the robust threshold of {threshold:,.2f}, based on median plus six median absolute deviations.",
    )

    round_amount_mask = abs_amount.ge(10_000) & (abs_amount.mod(1_000).abs().lt(1e-9))
    _add_finding(
        findings,
        "LARGE_ROUND_AMOUNT",
        "medium",
        "Large round-value transaction",
        df[round_amount_mask],
        "Large round-value transactions can be legitimate but are commonly included in journal-entry and fraud-risk screening.",
    )

    risk_score = min(100, sum(SEVERITY_WEIGHT[f.severity] for f in findings))
    limitations = [
        "Rule-based flags are risk indicators, not findings of fraud or control failure.",
        "The prototype does not inspect invoices, contracts, bank evidence, user-access logs, or ERP workflow history.",
        "Thresholds are illustrative and should be calibrated to entity materiality, process design, and transaction population.",
        "All material conclusions require qualified human review and corroborating evidence.",
    ]

    return DeterministicAuditResult(
        source_file=str(path),
        row_count=int(len(df)),
        total_absolute_value=float(abs_amount.sum()),
        risk_score=risk_score,
        findings=findings,
        limitations=limitations,
    )


def result_as_json(csv_path: str | Path) -> str:
    return json.dumps(analyze_transactions(csv_path).model_dump(), indent=2)
