# Frankenstein Claude Architecture

## Design objective

Frankenstein Claude is a research prototype for combining deterministic audit evidence with multiple Claude-based accounting and assurance specialists while preserving explicit human decision rights.

## Pipeline

```mermaid
flowchart LR
    A[ERP / CSV / GL Evidence] --> B[Deterministic Audit Engine]
    B --> C[Evidence Ledger]
    C --> D1[Finance Controls]
    C --> D2[Internal Audit]
    C --> D3[IFRS Reporting]
    C --> D4[ICFR]
    C --> D5[Forensic]
    C --> D6[ESG Assurance]
    C --> D7[Cost & AI FinOps]
    C --> D8[Operations Risk]
    C --> D9[AI & Data Governance]
    D1 --> E[Frankenstein Claude Audit Leader]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E
    D6 --> E
    D7 --> E
    D8 --> E
    D9 --> E
    E --> F[Evidence-Grounded Report]
    F --> G{Human Review Gate}
```

## Architectural rules

1. Deterministic tests run before generative interpretation.
2. Specialist agents receive the same traceable evidence snapshot.
3. A specialist may request more evidence but may not invent it.
4. Agent consensus is not professional evidence.
5. Fraud, compliance, audit-opinion, and material-weakness conclusions remain human decisions.
6. Model choice is replaceable through `CLAUDE_MODEL`.
7. A missing API key degrades safely to deterministic/offline mode.
8. The public prototype uses synthetic data and does not require confidential client information.

## Planned adapters

- general ledger and journal entries
- revenue and contract data
- procurement / AP / vendor master
- payroll
- treasury and bank evidence
- tax reconciliations
- XBRL / financial statements
- sustainability metrics and source evidence
- access logs and model/agent telemetry
- remediation and issue lifecycle evidence
