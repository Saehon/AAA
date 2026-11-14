"""Offline deterministic financial metrics; no live data access."""
from decimal import Decimal, InvalidOperation
import json, sys

def number(value):
    if isinstance(value, bool) or value is None:
        raise ValueError("Missing or invalid numeric value")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid numeric value") from None
    if not result.is_finite():
        raise ValueError("Nonfinite numeric value")
    return result

def calculate(payload):
    if not isinstance(payload, dict):
        raise ValueError("Input must be an object")
    if payload.get("currency") not in ("USD", "SEK", "EUR", "GBP"):
        raise ValueError("Explicit supported currency required")
    if not isinstance(payload.get("current_period"), str) or not isinstance(payload.get("prior_period"), str) or payload["current_period"] == payload["prior_period"]:
        raise ValueError("Distinct period labels required")
    current = number(payload.get("revenue_current"))
    prior = number(payload.get("revenue_prior"))
    if prior <= 0:
        raise ValueError("Prior revenue must be positive; growth undefined otherwise")
    if current < 0:
        raise ValueError("Negative revenue requires specialist review")
    return {
        "metric": "revenue_growth_percent",
        "value": str(((current-prior)/prior*100).quantize(Decimal("0.0001"))),
        "currency": payload["currency"],
        "current_period": payload["current_period"],
        "prior_period": payload["prior_period"],
        "evidence_status": "USER_SUPPLIED_UNVERIFIED",
        "formula": "(revenue_current - revenue_prior) / revenue_prior * 100",
        "limitations": ["No source filings inspected", "No assurance on accounting comparability or inflation", "No external data retrieval"]
    }

if __name__ == "__main__":
    try:
        print(json.dumps(calculate(json.load(sys.stdin))))
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "evidence_status": "BLOCKED"}), file=sys.stderr)
        sys.exit(2)
