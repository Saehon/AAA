from pathlib import Path

from finance_ops_audit_agent.analytics import analyze_transactions


SAMPLE = (
    Path(__file__).resolve().parents[1]
    / "sample_data"
    / "transactions.csv"
)


def test_sample_data_detects_expected_control_signals():
    result = analyze_transactions(SAMPLE)
    rules = {finding.rule_id for finding in result.findings}

    assert result.row_count == 12
    assert "DUPLICATE_ID" in rules
    assert "MISSING_APPROVER" in rules
    assert "SOD_CONFLICT" in rules
    assert "WEEKEND_POSTING" in rules
    assert "OUT_OF_HOURS" in rules
    assert "ROBUST_AMOUNT_OUTLIER" in rules
    assert "LARGE_ROUND_AMOUNT" in rules
    assert result.risk_score > 0


def test_every_finding_has_traceable_evidence():
    result = analyze_transactions(SAMPLE)
    for finding in result.findings:
        assert finding.finding_id.startswith("F-")
        assert finding.evidence
        assert finding.rationale
