# FRANKENSTEIN Finance & Operations Audit System

A public research prototype for **AI-assisted internal audit, finance controls, forensic analytics, treasury, revenue, procurement/AP, payroll, tax, FP&A, ICFR, AI/data governance, operations risk, evidence challenge, and human-governed reporting**.

This module was designed around the capabilities described in OpenAI's **Finance & Operations Audit Leader** role. It is an independent portfolio project and is **not affiliated with, endorsed by, or built for OpenAI**.

## What FRANKENSTEIN means

FRANKENSTEIN is the project codename for an audit system assembled from **replaceable specialist modules**. Deterministic tests create evidence, domain specialists interpret only relevant evidence, an independent challenger attacks unsupported conclusions, and a qualified human retains final decision rights.

See ARCHITECTURE.md and EVALUATION.md.

## Architecture

~~~mermaid
flowchart LR
    A[Transaction Population] --> B[Deterministic Tests + Provenance]
    B --> C[11 Specialist Audit Agents]
    C --> D[Independent Evidence Challenger]
    D --> E[Audit Leader Synthesis]
    E --> F{Human Approval Gate}
~~~

### Specialist audit team

| Specialist | Focus |
|---|---|
| Finance Controls Auditor | Authorization, accounting controls, classification, transaction integrity |
| Forensic Transaction Analyst | Anomalies, duplicate processing, unusual timing, control circumvention indicators |
| Treasury & Liquidity Auditor | Cash disbursements, high-value activity, liquidity and bank-control dependencies |
| Revenue & Commercial Accounting Auditor | Validity, credits/reversals, cutoff and revenue evidence |
| Procurement & Accounts Payable Auditor | P2P, vendor, approval, duplicate-payment and SoD risk |
| Payroll & People-Cost Auditor | Payroll and people-cost controls; abstains when evidence is absent |
| Tax Control Auditor | Tax-process implications and required corroborating evidence |
| FP&A and Management Reporting Auditor | Budget attribution, unusual spend, variance and reporting quality |
| ICFR Auditor | Financial-reporting control objectives and evidence sufficiency |
| AI & Data Governance Auditor | Data quality, lineage, provenance, model-use boundaries |
| Operations Risk Auditor | Resilience, accountability, scalability and third-party dependencies |

## Why this architecture is stronger

- **Deterministic evidence first:** transaction-level risk indicators originate in reproducible Python rules.
- **SHA-256 provenance:** every run fingerprints the source dataset.
- **Domain routing:** specialists receive findings relevant to their assigned domain.
- **Adversarial challenge:** a separate agent tries to falsify or narrow specialist conclusions.
- **Programmatic evidence validation:** unsupported finding IDs are removed after model output.
- **Structured outputs:** specialist, challenge and executive outputs use Pydantic schemas.
- **Fail-closed governance:** the final state is always pending_human_review.
- **Replaceable modules:** individual audit specialists can be upgraded without redesigning the full system.

## Deterministic analytics

Current tests include:

1. duplicate transaction identifiers;
2. missing approval evidence;
3. requester/approver segregation-of-duties conflicts;
4. invalid timestamps;
5. weekend postings;
6. out-of-hours postings;
7. robust amount outliers using median absolute deviation;
8. large round-value transactions;
9. missing account or cost-center coding;
10. negative-value transactions requiring contextual review;
11. repeated vendor/amount combinations on the same day;
12. high-value transactions without approval evidence.

These are **risk indicators**, not proof of error, fraud, misconduct, or control failure.

## Repository layout

~~~text
finance_ops_audit_agent/
├── README.md
├── ARCHITECTURE.md
├── EVALUATION.md
├── JOB_ROLE_MAPPING.md
├── agent.py
├── specialists.py
├── analytics.py
├── governance.py
├── config.py
├── schemas.py
├── cli.py
├── requirements.txt
├── .env.example
├── sample_data/
│   └── transactions.csv
└── tests/
    ├── test_analytics.py
    └── test_governance.py
~~~

## Quick start

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r finance_ops_audit_agent/requirements.txt
~~~

### Deterministic-only mode

~~~bash
python -m finance_ops_audit_agent.cli --deterministic-only
~~~

### Full FRANKENSTEIN audit

~~~bash
export OPENAI_API_KEY="YOUR_KEY"

python -m finance_ops_audit_agent.cli \
  --csv sample_data/transactions.csv \
  --domains all \
  --objective "Assess transaction-control risk, cross-functional implications, and evidence requiring follow-up."
~~~

### Targeted audit

~~~bash
python -m finance_ops_audit_agent.cli \
  --csv sample_data/transactions.csv \
  --domains finance_controls,forensic,treasury,icfr \
  --objective "Review payment, control, forensic and financial-reporting risks."
~~~

## Configurable thresholds

~~~text
AUDIT_APPROVAL_THRESHOLD=10000
AUDIT_LARGE_ROUND_THRESHOLD=10000
AUDIT_MAD_MULTIPLIER=6
AUDIT_WORKING_HOUR_START=6
AUDIT_WORKING_HOUR_END=22
~~~

They are research defaults and must be calibrated to entity-specific materiality and process design before professional use.

## Governance contract

The system intentionally does **not**:

- issue an audit opinion;
- determine that fraud occurred;
- accuse a person or counterparty of misconduct;
- classify an ICFR observation as a material weakness from transaction data alone;
- claim regulatory compliance;
- make autonomous accounting entries or control changes;
- read transaction files outside this module through its local audit tool.

Every material conclusion must pass:

**Deterministic Evidence → Specialist Review → Independent Challenge → Executive Synthesis → Human Approval Gate**

## Extension roadmap

The architecture is ready for general ledger, trial balance, AP, AR, payroll, treasury/bank, tax, procurement/vendor-master, revenue-contract, budget/forecast, ERP-workflow, identity/access, continuous-monitoring, remediation, graph analytics, and Board-reporting adapters.

## References

- OpenAI Careers: Finance & Operations Audit Leader
  https://openai.com/careers/finance-and-operations-audit-leader-san-francisco/
- OpenAI Agents SDK
  https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK — Agents
  https://openai.github.io/openai-agents-python/agents/
- OpenAI Agents SDK — Guardrails
  https://openai.github.io/openai-agents-python/guardrails/

## Status

**Version 0.2.0 · research prototype · portfolio demonstration · not production assurance software.**
