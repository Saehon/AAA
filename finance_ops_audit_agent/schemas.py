from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]


class AuditFinding(BaseModel):
    finding_id: str
    rule_id: str
    severity: Severity
    title: str
    transaction_ids: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    rationale: str


class DeterministicAuditResult(BaseModel):
    source_file: str
    row_count: int
    total_absolute_value: float
    risk_score: int
    findings: list[AuditFinding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class AuditAgentReport(BaseModel):
    executive_summary: str
    scope: str
    key_risks: list[str]
    evidence_references: list[str]
    recommended_actions: list[str]
    limitations: list[str]
    human_review_required: bool = True
