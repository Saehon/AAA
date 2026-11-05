# Technical design and trust boundaries

## Components

1. **FastAPI boundary:** `app/main.py` receives and validates bounded requests with Pydantic.
2. **Deterministic control logic:** `app/engine.py` calculates audit flags, treasury matches and financial ratios with Decimal arithmetic.
3. **Traceable response:** rule IDs, client-supplied support IDs, recommended review actions, a fresh trace UUID and `requires_human_review=true`.
4. **Optional model drafting:** `app/llm.py` offers a bounded summary from explicit findings only, and is disabled unless `ENABLE_LLM=true` with an authorized provider credential. It does not alter rules or release decisions.
5. **Reproducibility:** invented JSON inputs, unit tests, synthetically labeled JE rule sanity check and CI.

```text
Local caller (synthetic only)
       |
  Pydantic/API contracts
       |
    +-- Journal controls ----> Rule and evidence-ID flags ---+
    +-- Bank/ledger ----------> Exact one-to-one matches ----+--> Human review required
    +-- Finance --------------> Ratios and signals ----------+
       |
       +-- [OFF BY DEFAULT] model drafting --> UNVERIFIED prose --> Human review required
```

## Why financial accuracy is separate from natural-language fluency

Financial decisions depend on valid source inputs and professional authority. An evidence ID on a finding does not prove that a document exists, belongs to the entity, is relevant or is admissible. Synthetic imbalanced journals can test that an arithmetic rule works; they cannot establish sensitivity for financial reporting fraud.

The uncalibrated **screening_index** is only a queue/triage heuristic. It must never be described as a fraud probability or an audit risk assessment under ISA or PCAOB standards.

The liquidity signal makes no forecasts. Zero-denominator cases yield an explicitly undefined measure. Transaction matching is exact and may under-match real bank records when references differ: this is a design boundary, not a false claim about production reconciliation accuracy.

## Production readiness gaps

- Verified and authorized ERP/banking source adapters; normalized currency, time, legal entity and period.
- OIDC/SSO, fine-grained roles, multi-tenant isolation and secret-manager integration.
- Hash-anchored document provenance, retention controls and durable protected audit logs.
- Four-eyes approval UI and immutable professional judgment records.
- Automated dependency/security scans, SAST, threat modeling, network isolation and incident drills.
- Independently labeled pilot cases and realistic estimates of exception false-alert costs.
- p95 latency, throughput, failure-mode, model safety, privacy and cost measurement.
- Staged release, rollback and documented control owners.

Those gaps are *not* solved by GitHub Actions passing.
