# Frankenstein Claude Platform Blueprint

## Canonical objective

Build an evidence-governed multi-agent platform for accounting, auditing, internal control, forensic work, ESG assurance, management accounting, AI FinOps, and research-grade verification.

The design extends the existing Finance & Operations audit engine rather than replacing it.

## Canonical flow

```text
ERP / GL / contracts / XBRL / ESG evidence
        ↓
Data validation + deterministic tests
        ↓
Evidence Passports + provenance ledger
        ↓
Accounting / Audit / ICFR / Forensic / ESG / Cost specialists
        ↓
Scientific Discovery: competing hypotheses + empirical tests
        ↓
Challenger / Falsifier
        ↓
Independent Verification / replication
        ↓
Frankenstein Claude Audit Leader
        ↓
Evidence-grounded workpapers and report
        ↓
HUMAN GATE
```

## Four cores

1. **Knowledge & Standards Core** — reporting, audit, controls, sustainability, entity policy, and professional-method grounding.
2. **Data & Evidence Core** — ERP, GL, subledgers, contracts, XBRL, ESG evidence, deterministic tests, lineage, and evidence passports.
3. **Scientific Discovery & Challenge Core** — competing hypotheses, quantitative/causal analysis, adversarial challenge, replication, and independent verification.
4. **Assurance & Governance Core** — leader synthesis, documentation, evidence sufficiency, agent governance, audit trail, and human decision rights.

## MVP engagement

The first full engagement should remain narrow and testable:

**Revenue & Receivables Assurance**

Required inputs:
- sales / invoice population;
- customer master;
- cash receipts;
- credit notes;
- approval/workflow logs;
- GL revenue and AR balances;
- selected contracts or order evidence.

Minimum deterministic tests:
- duplicate invoices;
- missing approvals;
- unusual timing / cut-off;
- round or high-value anomalies;
- requester/approver conflicts;
- invoice-to-cash reconciliation exceptions;
- credit-note anomalies.

Claude agents may interpret and request evidence, but the deterministic layer owns reproducible screening logic.

## Evidence Passport rule

Every material claim should be linked to an evidence passport containing:
- stable evidence ID;
- source type and source reference;
- assertion under review;
- support / contradiction status;
- provenance;
- cryptographic content hash;
- human-verification status.

Agents cannot overwrite source evidence or mark themselves as human verifiers.

## Decision rights

AI may:
- scope and recommend;
- run reproducible analytics;
- classify and summarize;
- propose accounting/audit procedures;
- generate competing hypotheses;
- challenge conclusions;
- draft workpapers and reports.

AI may not autonomously:
- issue an audit opinion;
- declare fraud;
- declare a material weakness;
- certify IFRS/regulatory compliance;
- post accounting entries;
- change production controls;
- approve remediation closure.

Those remain human decisions.

## Portfolio adapters

Existing repository boundaries should remain modular:
- `Saehon/AAA` — deterministic audit engine and current Frankenstein Claude implementation;
- `Saehon/IFRS-AI-Inspector` — reporting/standards adapter;
- `Saehon/AuditData-API` — evidence/data access adapter;
- Multi-Agent BERT / financial NLP — textual signal adapter;
- TimesFM — temporal anomaly and forecasting adapter;
- GAN Lab / synthetic data — adversarial and simulation adapter;
- `Saehon/Saeid-Homayoun` — portfolio-level research and governance reference.

Adapters are promoted from “boundary” to “executable dependency” only after reproducible integration tests exist.

## Build sequence

**Phase 1 — Foundation:** platform registry, evidence passports, governed workflow, offline tests.

**Phase 2 — Revenue & Receivables MVP:** data adapters, reconciliations, cut-off tests, contract evidence, specialist prompts, workpaper output.

**Phase 3 — Challenge & Verification:** hypothesis competition, falsifier, independent re-run, evidence-conflict handling.

**Phase 4 — Platform services:** API, persistent evidence ledger, role-based access, job orchestration, UI, engagement dashboard.

**Phase 5 — Expansion:** procurement/AP, payroll, treasury, tax, ESG, estimates, going concern, AI/data governance, management accounting and cost/carbon ledgers.

## Design principle

**Evidence before interpretation; challenge before synthesis; verification before approval; human judgment before professional conclusion.**
