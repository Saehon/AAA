from __future__ import annotations

import json
import os
from typing import Any

from anthropic import Anthropic
from pydantic import ValidationError

from .registry import AgentSpec, LEADER_NAME
from .schemas import FrankensteinClaudeReport, SpecialistAssessment


DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")


def _text_from_message(message: Any) -> str:
    parts: list[str] = []
    for block in getattr(message, "content", []):
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", ""))
    return "\n".join(parts).strip()


def _extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("Claude response did not contain a JSON object.")
    return json.loads(text[start : end + 1])


class ClaudeAuditClient:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or DEFAULT_MODEL
        self.client = Anthropic()

    def run_specialist(
        self,
        spec: AgentSpec,
        objective: str,
        deterministic_evidence: dict[str, Any],
    ) -> SpecialistAssessment:
        system = f"""You are the {spec.name}, a specialist inside an evidence-governed accounting and assurance research system.
Your domain is {spec.domain}.
Mandate: {spec.mandate}

Rules:
1. Treat deterministic findings as risk indicators, not proof of fraud, error, noncompliance, or control failure.
2. Tie each material statement to supplied finding IDs/rule IDs or explicitly state that evidence is missing.
3. Never invent accounting standards, regulatory requirements, source documents, or facts.
4. Request corroborating evidence when needed.
5. Do not issue an audit opinion or make autonomous accounting/control changes.
6. Return one JSON object only with keys:
agent_name, domain, risk_summary, key_risks, evidence_references, tests_requested, recommended_actions, limitations.
"""

        prompt = f"""<audit_objective>{objective}</audit_objective>
<deterministic_evidence>
{json.dumps(deterministic_evidence, indent=2)}
</deterministic_evidence>
Analyze only what is supportable from the supplied evidence."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2200,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = _text_from_message(message)
        try:
            parsed = _extract_json(raw)
            parsed["agent_name"] = spec.name
            parsed["domain"] = spec.domain
            return SpecialistAssessment.model_validate(parsed)
        except (ValueError, json.JSONDecodeError, ValidationError):
            return SpecialistAssessment(
                agent_name=spec.name,
                domain=spec.domain,
                risk_summary=raw or "Claude returned no usable specialist narrative.",
                limitations=["Specialist output could not be validated as structured JSON; human review is required."],
            )

    def run_leader(
        self,
        objective: str,
        deterministic_risk_score: int,
        specialists: list[SpecialistAssessment],
        evidence_references: list[str],
        deterministic_limitations: list[str],
    ) -> FrankensteinClaudeReport:
        system = f"""You are the {LEADER_NAME}.
You synthesize specialist work into a concise, evidence-grounded internal-audit decision-support report.

Rules:
1. Do not issue an audit opinion.
2. Do not conclude that fraud occurred.
3. Do not claim legal, regulatory, IFRS, or control compliance.
4. Separate observed deterministic indicators from interpretation.
5. Preserve uncertainty and contradictory specialist views.
6. Every cross-domain risk must be traceable to evidence or explicitly marked as requiring evidence.
7. human_review_required must be true.
8. Return one JSON object only with keys:
executive_summary, audit_objective, deterministic_risk_score, cross_domain_risks,
evidence_references, recommended_actions, limitations, human_review_required.
"""

        payload = {
            "audit_objective": objective,
            "deterministic_risk_score": deterministic_risk_score,
            "specialists": [s.model_dump() for s in specialists],
            "evidence_references": evidence_references,
            "deterministic_limitations": deterministic_limitations,
        }
        message = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=system,
            messages=[{"role": "user", "content": json.dumps(payload, indent=2)}],
        )
        raw = _text_from_message(message)
        try:
            parsed = _extract_json(raw)
            parsed["audit_objective"] = objective
            parsed["deterministic_risk_score"] = deterministic_risk_score
            parsed["specialist_assessments"] = specialists
            parsed["human_review_required"] = True
            return FrankensteinClaudeReport.model_validate(parsed)
        except (ValueError, json.JSONDecodeError, ValidationError):
            return FrankensteinClaudeReport(
                executive_summary=raw or "Claude leader synthesis could not be validated.",
                audit_objective=objective,
                deterministic_risk_score=deterministic_risk_score,
                specialist_assessments=specialists,
                evidence_references=evidence_references,
                limitations=deterministic_limitations
                + ["Leader output could not be validated as structured JSON; human review is required."],
                human_review_required=True,
            )
