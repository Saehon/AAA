from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoreSpec:
    name: str
    purpose: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class PlatformAgent:
    name: str
    role: str
    decision_right: str


CORES: tuple[CoreSpec, ...] = (
    CoreSpec(
        "Knowledge & Standards Core",
        "Ground professional analysis in accounting, audit, control, sustainability, and entity policy knowledge.",
        (
            "IFRS / reporting policy grounding",
            "PCAOB / audit methodology grounding",
            "COSO / ICFR control grounding",
            "ESG / sustainability assurance grounding",
            "entity policies and process documentation",
        ),
    ),
    CoreSpec(
        "Data & Evidence Core",
        "Convert source data into traceable evidence objects before generative interpretation.",
        (
            "ERP / GL / subledger ingestion",
            "contracts and source-document references",
            "XBRL / financial statement evidence",
            "sustainability evidence",
            "evidence passports and provenance",
            "deterministic population testing",
        ),
    ),
    CoreSpec(
        "Scientific Discovery & Challenge Core",
        "Generate competing explanations and actively try to falsify weak conclusions.",
        (
            "hypothesis generation",
            "quantitative and causal analysis",
            "adversarial challenge",
            "alternative explanation search",
            "replication and independent verification",
        ),
    ),
    CoreSpec(
        "Assurance & Governance Core",
        "Synthesize evidence while preserving professional judgment and explicit human decision rights.",
        (
            "cross-domain synthesis",
            "documentation and reporting",
            "evidence sufficiency checks",
            "model and agent governance",
            "immutable decision trail",
            "mandatory human approval gate",
        ),
    ),
)


AGENT_SOCIETY: tuple[PlatformAgent, ...] = (
    PlatformAgent("Conductor Agent", "Route work, enforce stage order, and prevent unsupported stage skipping.", "coordinate_only"),
    PlatformAgent("Scope & Risk Agent", "Define objective, assertions, material risks, and required evidence.", "recommend_only"),
    PlatformAgent("Evidence Agent", "Create evidence passports and test provenance, completeness, and conflicts.", "evidence_only"),
    PlatformAgent("Accounting Agent", "Analyze accounting treatment and reporting judgments.", "recommend_only"),
    PlatformAgent("Audit & Controls Agent", "Assess controls, audit procedures, exceptions, and follow-up tests.", "recommend_only"),
    PlatformAgent("ERP & Reconciliation Agent", "Reconcile ledgers, subledgers, interfaces, and source records.", "evidence_only"),
    PlatformAgent("Forensic Agent", "Assess anomalous patterns and corroboration needs without alleging misconduct.", "recommend_only"),
    PlatformAgent("ESG Assurance Agent", "Assess sustainability data lineage, controls, estimates, and assurance readiness.", "recommend_only"),
    PlatformAgent("Cost & AI FinOps Agent", "Measure activity, model, token, and review cost without trading off assurance quality.", "recommend_only"),
    PlatformAgent("Quant & Causal Agent", "Run reproducible statistical, forecasting, and causal tests where appropriate.", "evidence_only"),
    PlatformAgent("Scientific Discovery Agent", "Generate competing hypotheses and explicit empirical tests.", "recommend_only"),
    PlatformAgent("Challenger / Falsifier", "Search for contradictory evidence, alternative explanations, and failure modes.", "challenge_only"),
    PlatformAgent("Independent Verification Agent", "Re-run critical tests independently and verify evidence references.", "verify_only"),
    PlatformAgent("Documentation & Reporting Agent", "Produce evidence-grounded workpapers and reports with limitations.", "draft_only"),
    PlatformAgent("Frankenstein Claude Audit Leader", "Synthesize specialist outputs and escalate unresolved conflicts.", "recommend_only"),
    PlatformAgent("Human Gate", "Approve, reject, request more evidence, or authorize professional conclusions.", "human_decision"),
)


WORKFLOW_STAGES: tuple[str, ...] = (
    "scope",
    "ingest",
    "deterministic_test",
    "evidence_passport",
    "specialist_analysis",
    "hypothesis_competition",
    "adversarial_challenge",
    "independent_verification",
    "leader_synthesis",
    "documentation",
    "human_gate",
)
