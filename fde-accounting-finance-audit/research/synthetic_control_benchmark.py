"""Synthetic engineering sanity test, NOT fraud-screening model validation.

This harness tests exactly one deliberately constructed rule, JE-001.
Balanced and unbalanced journals are generated with known deterministic
ground truth. A perfect score here is expected by construction and cannot be
extrapolated to real accounting records, professional judgments, CAMs or ICFR.
"""
import argparse
import json
import random
from datetime import date
from decimal import Decimal

from app.engine import assess_audit
from app.schemas import AuditRequest


def synthetic_casebook(n=200, seed=20261105):
    if not 2 <= n <= 500:
        raise ValueError("n must be between 2 and 500 (API request bound)")
    rng = random.Random(seed)
    entries, label_by_id = [], {}
    for i in range(n):
        label = i % 4 == 0  # 25% engineered imbalances
        nominal = Decimal(rng.randint(100, 15000))
        variance = Decimal("10") if label else Decimal("0")
        eid = f"SYN-JE-{i:04d}"
        # All entries have evidence pointers; not a demonstration of verified evidence.
        entries.append({
            "entry_id": eid,
            "posted_on": str(date(2026, 10, 15)),
            "posted_by": "maker",
            "approved_by": "controller",
            "is_manual": False,
            "reference": f"REF-{i:04d}",
            "evidence_id": f"SYN-DOC-{i:04d}",
            "lines": [
                {"account": "Receivable", "debit": str(nominal), "credit": "0"},
                {"account": "Revenue", "debit": "0", "credit": str(nominal - variance)},
            ],
        })
        label_by_id[eid] = label
    return AuditRequest.model_validate({"currency": "USD", "entries": entries}), label_by_id


def run(n=200, seed=20261105):
    request, gold = synthetic_casebook(n=n, seed=seed)
    findings = assess_audit(request).findings
    flagged = {finding.entry_id for finding in findings if finding.rule_id == "JE-001"}
    tp = sum(label and eid in flagged for eid, label in gold.items())
    fn = sum(label and eid not in flagged for eid, label in gold.items())
    tn = sum((not label) and eid not in flagged for eid, label in gold.items())
    fp = sum((not label) and eid in flagged for eid, label in gold.items())
    return {
        "experiment_kind": "synthetic_deterministic_rule_sanity_test",
        "seed": seed, "cases": n, "rule": "JE-001",
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "note": "Constructed labels; NOT empirical performance, auditor accuracy or fraud detection.",
        "code_input_provenance": "synthetic_casebook() in research/synthetic_control_benchmark.py",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run synthetic deterministic JE-001 sanity test")
    parser.add_argument("--cases", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261105)
    args = parser.parse_args()
    print(json.dumps(run(args.cases, args.seed), indent=2))
