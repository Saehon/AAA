from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, Field


SupportStatus = Literal["supports", "contradicts", "context", "unresolved"]


class EvidencePassport(BaseModel):
    evidence_id: str
    source_type: str
    source_ref: str
    assertion: str
    support_status: SupportStatus = "unresolved"
    provenance: dict[str, Any] = Field(default_factory=dict)
    content_hash: str
    human_verified: bool = False
    model_can_override: bool = False


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def build_evidence_passport(
    *,
    source_type: str,
    source_ref: str,
    assertion: str,
    payload: dict[str, Any],
    support_status: SupportStatus = "unresolved",
    provenance: dict[str, Any] | None = None,
) -> EvidencePassport:
    canonical = _canonical_json(payload)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    evidence_id = f"EV-{digest[:12].upper()}"
    return EvidencePassport(
        evidence_id=evidence_id,
        source_type=source_type,
        source_ref=source_ref,
        assertion=assertion,
        support_status=support_status,
        provenance=provenance or {},
        content_hash=digest,
        human_verified=False,
        model_can_override=False,
    )
