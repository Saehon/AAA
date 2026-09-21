# Mapping to the Finance & Operations Audit Leader Role

This document maps the FRANKENSTEIN Finance & Operations Audit System to capabilities described in the OpenAI Finance & Operations Audit Leader posting.

| Role capability | FRANKENSTEIN implementation | Maturity |
|---|---|---|
| Lead risk-based finance/operations audits | Federated Audit Leader + deterministic evidence pipeline | Prototype |
| Financial reporting/accounting controls | Finance Controls Auditor + ICFR Auditor | Prototype |
| Treasury | Treasury & Liquidity Auditor | Specialist implemented; treasury-specific data adapter roadmap |
| Revenue | Revenue & Commercial Accounting Auditor | Specialist implemented; contract/billing adapter roadmap |
| Procurement / AP | Procurement & AP Auditor + duplicate/approval/SoD analytics | Prototype |
| Payroll | Payroll & People-Cost Auditor with explicit abstention when evidence is absent | Specialist implemented; payroll adapter roadmap |
| Tax | Tax Control Auditor with evidence-bounded conclusions | Specialist implemented; tax adapter roadmap |
| FP&A | FP&A and Management Reporting Auditor | Prototype |
| Forensic accounting / investigations | Forensic Transaction Analyst + anomaly rules | Prototype |
| Transaction-population analytics | Full-population CSV analytics | Implemented |
| Control circumvention / SoD | Same requester/approver + approval tests | Implemented |
| AI, automation and data analytics | OpenAI Agents SDK + deterministic Python analytics | Implemented |
| Data quality / lineage / governance | SHA-256 provenance, schema validation, AI & Data Governance Auditor | Implemented at prototype level |
| Cross-functional risk | Domain-routed specialist architecture | Implemented |
| Independent challenge | Evidence Challenger attempts falsification and narrows unsupported claims | Implemented |
| Evidence traceability | Finding IDs, row-level evidence, source hash, control objectives | Implemented |
| Executive / Board-oriented synthesis | Structured Audit Leader output | Prototype |
| Continuous monitoring | Deterministic engine can be scheduled over new populations | Roadmap |
| Remediation / issue validation | Priority actions + human-gated follow-up | Early prototype |
| Human judgment / independence | Mandatory pending human gate | Implemented |

## Role-to-system logic

~~~text
Transaction Evidence
    ↓
Deterministic Audit Tests
    ↓
Domain Specialists
    ↓
Independent Challenge / Falsification
    ↓
Cross-Domain Audit Leader Synthesis
    ↓
Qualified Human Decision
~~~

## Portfolio demonstration

The included synthetic dataset demonstrates duplicate IDs, missing approvals, segregation-of-duties conflicts, unusual timing, high-value outliers, round-value screening, provenance hashing, cross-domain evidence routing, unsupported-evidence rejection, and human-gated reporting.

## Design principle

> AI may accelerate risk identification, testing, synthesis, challenge and reporting; it should not silently replace evidence, professional skepticism, independence, or accountable human judgment.

## Professional positioning

**Accounting + Internal Audit + Forensic Accounting + ICFR + Treasury + Revenue + Procurement + Payroll + Tax + FP&A + Data Analytics + AI Agents + AI Governance + Evidence Verification + Human Decision Rights.**
