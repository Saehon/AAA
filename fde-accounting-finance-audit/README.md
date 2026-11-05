# Forward Deployed Engineering | Accounting, Finance & Audit

**Public, standalone-in-folder demonstration** · Python/FastAPI · version 0.1.0  
**Research and engineering lead:** Saeid Homayoun  
**Status:** Reproducible software prototype with synthetic examples; **not** an enterprise deployment, fraud-detection model, independent audit or investment service.

> This is a **public showcase inside the already-public [AAA laboratory](../README.md)**. It is *not a separate GitHub repository*. This folder contains deliberately selected, nonconfidential material only; no private research systems, unpublished manuscripts, proprietary client data or API credentials are published.

## What a Forward Deployed Engineer would deliver

A forward deployed engineer translates enterprise workflows into working, testable and governable software. This demo illustrates four small but linked tasks:

| Financial domain | Endpoint | Function | Boundary |
| --- | --- | --- | --- |
| Financial accounting | `POST /v1/accounting/reconcile` | Exact reference+amount, one-to-one matching between synthetic bank and ledger records | Does not connect to bank, ERP or post adjustments |
| Auditing / financial controls | `POST /v1/audit/assess` | Transparent, rule-based journal screening for imbalance, missing evidence IDs, segregation of duties, period-end manual entries and repeated references | Flags are not fraud labels, audit materiality or an audit opinion |
| Financial management | `POST /v1/finance/assess` | Current ratio, runway and cash-flow signals with zero-denominator handling | Not a forecast, investment recommendation or audited financial metric |
| Controlled generative AI | `POST /v1/ai/draft-review` | Optional narrative drafting from previously generated findings | Off by default; professional human approval required; not a substitute for verification |

**Architecture principle:** Calculation and reconciliation remain deterministic. A model can assist in wording a review, but cannot change the numeric results, verify an evidence object or authorize action. Inputs are validated, monetary math uses Decimal, findings carry rule/evidence IDs and responses carry trace IDs. Source evidence IDs are *not* independently verified.

## Quick start

Requires Python 3.11+ (CI uses 3.12).

```bash
git clone https://github.com/Saehon/AAA.git
cd AAA/fde-accounting-finance-audit
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs to explore the documented request schemas.

Sample request (entirely invented journal records):

```bash
curl -s -X POST http://127.0.0.1:8000/v1/audit/assess \
  -H "Content-Type: application/json" \
  --data-binary @examples/audit_request.json
```

Run the **constructed-label rule sanity check**, which is *not* a valid model performance experiment:

```bash
python -m research.synthetic_control_benchmark --cases 200 --seed 20261105
```

Optional local container: `docker build -t fde-controls:demo .`, then `docker run --rm -p 127.0.0.1:8000:8000 fde-controls:demo`. Never bind demo routes to public internet ingress.

## Engineering evidence

- **Executable code:** `app/schemas.py`, `app/engine.py`, `app/main.py`, `app/llm.py`.
- **Reproducible examples:** `examples/*.json`, invented and freely shareable.
- **Automated validation:** `tests/` and [scoped GitHub Actions](../.github/workflows/fde-public-ci.yml).
- **Deployment/risks:** [Technical design](docs/TECHNICAL_DESIGN.md), [safety boundaries](docs/SAFETY.md), [engineering delivery playbook](docs/ENGAGEMENT.md).
- **Academic motivation:** [FT50 / AJG / Q1 evidence map](docs/RESEARCH_EVIDENCE.md) with DOI links, avoiding distribution of copyrighted papers.
- **Release checks and next steps:** [Public release checklist](docs/RELEASE_CHECKLIST.md).

## Current limits

The project **does not** provide SSO, user/tenant authorization, immutable evidence storage, real ERP/bank connectors, validated risk calibration, approval workflow enforcement, cloud deployment, performance or penetration testing. The API's optional demo API key is *not* enterprise identity. The LLM call is disabled by default (`ENABLE_LLM=false`) and must not be turned on with confidential data or without processing approval.

The project's test suite checks implementation behavior on engineered examples. Do not infer journal publication, customer deployment, audit effectiveness, model superiority, fraud detection precision or business savings.

## Licensing, affiliation and scholarly attribution

This directory forms part of the parent [AAA Apache-2.0 repository](../LICENSE), applying to this original public demonstration code subject to third-party dependency licenses. It is an independent academic/engineering showcase and is **not** affiliated with, sponsored by or certified by OpenAI, Anthropic, an audit firm, the PCAOB, or a regulatory body. Copyright © 2026 Saeid Homayoun. Publications are cited by DOI as research context, not copied or relicensed.

**Confidential research and unpublished manuscripts are intentionally excluded from this public release.**
