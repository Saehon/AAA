# Mapping to the Finance & Operations Audit Leader Role

This document shows how the prototype operationalizes major capabilities described in the OpenAI Finance & Operations Audit Leader posting.

| Role capability | Prototype implementation | Current maturity |
|---|---|---|
| Lead risk-based finance/operations audits | Lead orchestrator + specialist agents | Prototype |
| Financial reporting/accounting controls | Finance Controls Auditor + deterministic rules | Prototype |
| Treasury/tax/revenue/procurement/payroll/FP&A coverage | Architecture supports specialist expansion | Roadmap |
| Forensic accounting and investigations | Forensic Transaction Analyst | Prototype |
| Transaction-population analytics | Full CSV population scan | Implemented |
| Detect anomalies/control circumvention | Duplicate, SoD, approval, timing and amount rules | Implemented |
| Use AI/automation/data analytics | OpenAI Agents SDK + deterministic analytics | Implemented |
| Continuous monitoring | Same tests can be scheduled against new populations | Roadmap |
| Data quality / lineage / governance | Explicit schema validation and file boundary; deeper lineage controls planned | Early prototype |
| Executive/Board reporting | Structured report schema designed for concise escalation | Prototype |
| Remediation and issue validation | Recommended-action field; lifecycle workflow planned | Roadmap |
| Human judgment and independence | Human-review requirement and evidence-first boundaries | Implemented |

## Demonstration scenario

A reviewer can run the included synthetic transaction population and observe:

- a duplicate transaction identifier;
- a missing approver;
- a requester/approver segregation-of-duties conflict;
- weekend and out-of-hours postings;
- high-value outliers;
- large round-value transactions.

The deterministic layer produces traceable findings. The agentic layer then interprets those findings in finance, forensic, and operational contexts and produces a structured, human-review-required report.

## Design principle

> AI may accelerate risk identification, testing, synthesis, and reporting; it should not silently replace evidence, professional skepticism, independence, or accountable human judgment.

## Portfolio value

This prototype is intended to demonstrate the intersection of:

**Accounting + Internal Audit + Forensic Accounting + Data Analytics + AI Agents + Governance + Human Decision Rights.**
