from __future__ import annotations

from frankenstein_claude.orchestrator import DEFAULT_SAMPLE, run_frankenstein_audit
from frankenstein_claude.registry import AGENTS


def test_registry_contains_required_specialists():
    domains = {agent.domain for agent in AGENTS}
    assert {
        "finance_controls",
        "internal_audit",
        "ifrs_reporting",
        "icfr",
        "forensic",
        "esg_assurance",
        "cost_finops",
        "operations_risk",
        "ai_data_governance",
    }.issubset(domains)


def test_offline_report_is_evidence_grounded_and_human_gated():
    report = run_frankenstein_audit(
        objective="Test controlled audit orchestration.",
        csv_path=DEFAULT_SAMPLE,
        use_claude=False,
    )

    assert report.deterministic_risk_score > 0
    assert report.human_review_required is True
    assert len(report.specialist_assessments) == len(AGENTS)
    assert report.evidence_references
    assert any("DUPLICATE_ID" in ref for ref in report.evidence_references)
    assert any("SOD_CONFLICT" in ref for ref in report.evidence_references)
