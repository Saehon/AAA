import pytest

from frankenstein_claude.engagement_workflow import (
    EngagementState,
    advance,
    can_advance,
    record_human_decision,
)
from frankenstein_claude.evidence_passport import build_evidence_passport
from frankenstein_claude.platform_registry import AGENT_SOCIETY, CORES, WORKFLOW_STAGES


def test_four_core_architecture_and_human_gate_exist():
    assert len(CORES) == 4
    assert WORKFLOW_STAGES[-1] == "human_gate"
    assert any(agent.name == "Human Gate" and agent.decision_right == "human_decision" for agent in AGENT_SOCIETY)


def test_evidence_passport_is_stable_and_non_overridable():
    payload = {"invoice_id": "INV-1001", "amount": 125000, "approved": True}
    a = build_evidence_passport(
        source_type="invoice",
        source_ref="sample/INV-1001",
        assertion="Occurrence",
        payload=payload,
        support_status="supports",
    )
    b = build_evidence_passport(
        source_type="invoice",
        source_ref="sample/INV-1001",
        assertion="Occurrence",
        payload=payload,
        support_status="supports",
    )
    assert a.evidence_id == b.evidence_id
    assert a.content_hash == b.content_hash
    assert a.model_can_override is False
    assert a.human_verified is False


def test_workflow_cannot_skip_governance_stages():
    state = EngagementState(objective="Test revenue occurrence and cut-off", evidence_ids=["EV-1"])
    allowed, _ = can_advance(state, "deterministic_test")
    assert allowed is False

    state = advance(state, "ingest")
    state = advance(state, "deterministic_test")
    state = advance(state, "evidence_passport")
    state = advance(state, "specialist_analysis")
    state = advance(state, "hypothesis_competition")
    state = state.model_copy(update={"challenge_issues": ["Alternative explanation assessed."]})
    state = advance(state, "adversarial_challenge")
    state = state.model_copy(update={"verification_complete": True})
    state = advance(state, "independent_verification")
    state = advance(state, "leader_synthesis")
    state = state.model_copy(update={"leader_synthesis_complete": True})
    state = advance(state, "documentation")
    state = advance(state, "human_gate")
    state = record_human_decision(state, approved=True)
    assert state.human_approved is True


def test_human_decision_cannot_be_recorded_early():
    state = EngagementState(objective="Test")
    with pytest.raises(ValueError):
        record_human_decision(state, approved=True)
