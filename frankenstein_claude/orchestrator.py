from __future__ import annotations

import os
from pathlib import Path

from finance_ops_audit_agent.analytics import analyze_transactions

from .claude_client import ClaudeAuditClient
from .registry import AGENTS
from .schemas import FrankensteinClaudeReport, SpecialistAssessment


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE = REPO_ROOT / "finance_ops_audit_agent" / "sample_data" / "transactions.csv"


def _offline_specialists(evidence: dict) -> list[SpecialistAssessment]:
    refs = [f"{f['finding_id']}:{f['rule_id']}" for f in evidence.get("findings", [])]
    titles = [f["title"] for f in evidence.get("findings", [])]
    summary = (
        f"Deterministic testing produced {len(refs)} risk indicators. "
        "Claude synthesis was not called because ANTHROPIC_API_KEY is not set."
    )
    return [
        SpecialistAssessment(
            agent_name=spec.name,
            domain=spec.domain,
            risk_summary=summary,
            key_risks=titles,
            evidence_references=refs,
            tests_requested=["Obtain corroborating source documents, workflow logs, and control-owner evidence."],
            recommended_actions=["Review deterministic indicators and calibrate tests to entity-specific materiality and process design."],
            limitations=["Offline mode provides deterministic evidence only; no Claude interpretation was performed."],
        )
        for spec in AGENTS
    ]


def run_frankenstein_audit(
    objective: str,
    csv_path: str | Path = DEFAULT_SAMPLE,
    use_claude: bool = True,
) -> FrankensteinClaudeReport:
    deterministic = analyze_transactions(csv_path)
    evidence = deterministic.model_dump()
    evidence_refs = [f"{f.finding_id}:{f.rule_id}" for f in deterministic.findings]

    claude_enabled = use_claude and bool(os.getenv("ANTHROPIC_API_KEY"))
    if not claude_enabled:
        specialists = _offline_specialists(evidence)
        return FrankensteinClaudeReport(
            executive_summary=(
                f"Deterministic population testing identified {len(deterministic.findings)} "
                f"risk indicators with an illustrative risk score of {deterministic.risk_score}/100. "
                "Claude synthesis was not executed."
            ),
            audit_objective=objective,
            deterministic_risk_score=deterministic.risk_score,
            specialist_assessments=specialists,
            cross_domain_risks=[f.title for f in deterministic.findings],
            evidence_references=evidence_refs,
            recommended_actions=[
                "Corroborate high-severity indicators with source documents and workflow evidence.",
                "Calibrate rules and thresholds to the entity, process, materiality, and control design.",
                "Require qualified human approval before any professional conclusion or remediation decision.",
            ],
            limitations=deterministic.limitations
            + ["Claude synthesis unavailable or disabled; report reflects deterministic evidence only."],
            human_review_required=True,
        )

    client = ClaudeAuditClient()
    specialists = [
        client.run_specialist(spec, objective, evidence)
        for spec in AGENTS
    ]
    return client.run_leader(
        objective=objective,
        deterministic_risk_score=deterministic.risk_score,
        specialists=specialists,
        evidence_references=evidence_refs,
        deterministic_limitations=deterministic.limitations,
    )
