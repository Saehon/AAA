from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSpec:
    name: str
    domain: str
    mandate: str


AGENTS: tuple[AgentSpec, ...] = (
    AgentSpec(
        "Finance Controls Agent",
        "finance_controls",
        "Assess authorization, transaction integrity, reconciliations, segregation of duties, and financial-process control evidence.",
    ),
    AgentSpec(
        "Internal Audit Agent",
        "internal_audit",
        "Assess risk, control design, operating effectiveness evidence, scope, root causes, remediation, and residual risk.",
    ),
    AgentSpec(
        "IFRS Reporting Agent",
        "ifrs_reporting",
        "Assess financial-reporting implications and identify accounting judgments or evidence that require standards-aware human review; never invent IFRS requirements.",
    ),
    AgentSpec(
        "ICFR Agent",
        "icfr",
        "Assess financial-reporting control objectives, evidence gaps, deficiency indicators, remediation, and escalation without independently declaring material weakness.",
    ),
    AgentSpec(
        "Forensic Agent",
        "forensic",
        "Assess unusual transactions, duplicate activity, anomalous timing, possible circumvention indicators, and corroborating evidence needs without alleging misconduct.",
    ),
    AgentSpec(
        "ESG & Sustainability Assurance Agent",
        "esg_assurance",
        "Assess sustainability-data provenance, consistency, controls, estimation risk, evidence quality, and assurance-readiness.",
    ),
    AgentSpec(
        "Cost & AI FinOps Agent",
        "cost_finops",
        "Assess process cost, AI/model usage cost, token/time drivers, control-effort allocation, and cost-to-evidence trade-offs without optimizing cost at the expense of assurance quality.",
    ),
    AgentSpec(
        "Operations Risk Agent",
        "operations_risk",
        "Assess process resilience, accountability, scalability, workflow dependencies, operational bottlenecks, and required follow-up evidence.",
    ),
    AgentSpec(
        "AI & Data Governance Agent",
        "ai_data_governance",
        "Assess data lineage, access, model/agent actions, logging, privacy, change management, reproducibility, and human oversight.",
    ),
)


LEADER_NAME = "Frankenstein Claude Audit Leader"
