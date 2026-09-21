from __future__ import annotations

from pydantic import BaseModel, Field


class SpecialistAssessment(BaseModel):
    agent_name: str
    domain: str
    risk_summary: str
    key_risks: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    tests_requested: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class FrankensteinClaudeReport(BaseModel):
    executive_summary: str
    audit_objective: str
    deterministic_risk_score: int
    specialist_assessments: list[SpecialistAssessment] = Field(default_factory=list)
    cross_domain_risks: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    human_review_required: bool = True
