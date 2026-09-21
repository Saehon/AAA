from __future__ import annotations

from pydantic import BaseModel, Field

from .platform_registry import WORKFLOW_STAGES


class EngagementState(BaseModel):
    objective: str
    scope: str = "revenue_and_receivables"
    current_stage: str = "scope"
    evidence_ids: list[str] = Field(default_factory=list)
    challenge_issues: list[str] = Field(default_factory=list)
    verification_complete: bool = False
    leader_synthesis_complete: bool = False
    human_approved: bool = False


def _stage_index(stage: str) -> int:
    if stage not in WORKFLOW_STAGES:
        raise ValueError(f"Unknown workflow stage: {stage}")
    return WORKFLOW_STAGES.index(stage)


def can_advance(state: EngagementState, next_stage: str) -> tuple[bool, str]:
    current_idx = _stage_index(state.current_stage)
    next_idx = _stage_index(next_stage)

    if next_idx != current_idx + 1:
        return False, "Stages must advance sequentially; skipping governance stages is not allowed."

    if next_stage == "deterministic_test" and not state.evidence_ids:
        return False, "At least one source-evidence reference is required before deterministic testing."

    if next_stage == "independent_verification" and not state.challenge_issues:
        return False, "The challenge stage must record at least one challenge issue, even if it is resolved as non-material."

    if next_stage == "leader_synthesis" and not state.verification_complete:
        return False, "Independent verification must be complete before leader synthesis."

    if next_stage == "documentation" and not state.leader_synthesis_complete:
        return False, "Leader synthesis must be complete before documentation."

    if next_stage == "human_gate" and state.human_approved:
        return False, "Human approval is recorded at the human gate, not before it."

    return True, "ok"


def advance(state: EngagementState, next_stage: str) -> EngagementState:
    allowed, reason = can_advance(state, next_stage)
    if not allowed:
        raise ValueError(reason)
    return state.model_copy(update={"current_stage": next_stage})


def record_human_decision(state: EngagementState, approved: bool) -> EngagementState:
    if state.current_stage != "human_gate":
        raise ValueError("Human decisions can only be recorded at the human gate.")
    return state.model_copy(update={"human_approved": approved})
