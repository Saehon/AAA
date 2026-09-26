# Frankenstein Claude — Accounting, Audit & Assurance Multi-Agent Prototype

**Evidence-governed Claude orchestration for accounting, auditing, internal controls, forensic analytics, sustainability assurance, cost intelligence, operations risk, and AI/data governance.**

> Independent research prototype by Saeid Homayoun. This project is not affiliated with, endorsed by, sponsored by, or certified by Anthropic. Claude is used as a replaceable model layer; professional conclusions remain subject to qualified human review.

## What this adds to AAA

The existing `finance_ops_audit_agent` performs transparent population-level transaction tests. Frankenstein Claude sits **above that evidence layer** and asks multiple specialist agents to interpret the same traceable findings from different professional perspectives.

It therefore follows:

**Transactions → Deterministic Tests → Evidence Ledger → Claude Specialist Agents → Audit Leader → Human Review Gate**

## Specialist agents

| Agent | Scope |
|---|---|
| Finance Controls Agent | authorization, SoD, reconciliations, transaction integrity |
| Internal Audit Agent | risk, control design/effectiveness evidence, remediation |
| IFRS Reporting Agent | reporting judgments and evidence needs |
| ICFR Agent | financial-reporting controls and deficiency indicators |
| Forensic Agent | anomalous activity and corroboration requirements |
| ESG & Sustainability Assurance Agent | sustainability data, provenance, assurance readiness |
| Cost & AI FinOps Agent | activity/time/token cost and cost-to-evidence trade-offs |
| Operations Risk Agent | resilience, accountability, scalability and bottlenecks |
| AI & Data Governance Agent | lineage, access, logs, model/agent governance |
| Frankenstein Claude Audit Leader | cross-domain synthesis and escalation |

## Current Claude implementation

The prototype uses Anthropic's Python SDK and defaults to:

```text
CLAUDE_MODEL=claude-sonnet-5
```

Set a different active Claude API model through the environment variable without changing the architecture.

The system deliberately does **not** depend on Claude for the underlying transaction tests. Claude receives deterministic evidence after those tests have run.

## Quick start

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r frankenstein_claude/requirements.txt
```

Run entirely offline:

```bash
python -m frankenstein_claude.cli --offline
```

Run with Claude:

```bash
export ANTHROPIC_API_KEY="YOUR_KEY"
export CLAUDE_MODEL="claude-sonnet-5"
python -m frankenstein_claude.cli
```

## Evidence boundaries

Every deterministic finding contains a `finding_id`, `rule_id`, transaction references, row-level evidence, severity, and rationale. Specialist agents are instructed to cite those references or explicitly state that evidence is missing.

The current deterministic layer tests:

- duplicate transaction IDs;
- missing approvals;
- segregation-of-duties conflicts;
- weekend postings;
- out-of-hours activity;
- robust amount outliers;
- large round-value transactions.

These are screening indicators, not proof of fraud, error, or control failure.

## Human Review Gate

The prototype cannot autonomously:

- issue an audit opinion;
- conclude that fraud occurred;
- declare regulatory or IFRS compliance;
- declare a material weakness;
- make accounting entries;
- alter controls;
- sanction an employee/vendor/counterparty.

The final schema always sets `human_review_required = true`.

## Why this is useful as a portfolio project

The repository demonstrates a separation that is important in professional AI systems:

**reproducible analytics ≠ generative interpretation ≠ professional judgment**

It combines accounting/audit domain knowledge with Python, deterministic testing, model orchestration, structured evidence, governance, and reproducible CI.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the system map.


## Platform foundation

The prototype now includes the foundation for the broader **Frankenstein Claude accounting–audit–assurance platform**:

- `platform_registry.py` — four canonical cores, specialist/governance agent society, and controlled workflow stages;
- `evidence_passport.py` — stable evidence IDs, provenance, source references, content hashes, and non-overridable source evidence;
- `engagement_workflow.py` — sequential engagement state machine that prevents governance-stage skipping and reserves approval for the Human Gate;
- `PLATFORM_BLUEPRINT.md` — the full platform architecture and Revenue & Receivables MVP build sequence;
- `tests/test_platform_foundation.py` — offline tests for evidence integrity and human-decision boundaries.

The expanded flow is:

**Source Evidence → Deterministic Tests → Evidence Passports → Specialist Analysis → Hypothesis Competition → Adversarial Challenge → Independent Verification → Frankenstein Claude Audit Leader → Documentation → Human Gate**
