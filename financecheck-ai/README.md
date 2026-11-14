# NAAIL Reporting Inspector V3.4.0

**Professional-body and open research extension.** Educational, public/synthetic research use only; 46 skills. New: ACCA/CPA/CIA/CMA/CFE/CIMA/ICAEW ethics routing; Big Four public guidance; open code/data metadata and licences; curated thesis repositories; offline research-reviewer tasks. **No external publisher standards licensed or Google Co-Scientist/AlphaEvolve service connected; no live market/ERP/SEC/SSRN/Kaggle/HF MCP.** No official endorsement or guaranteed academic replication.

# NAAIL Reporting Inspector — V3.3.0

**IFRS · XBRL · ISSB Sustainability · ESG · ESRS Double Materiality · Assurance · PCAOB · FT50/AJG4 Research**

Adds 10 original research-and-review skills (35 skills total), six Claude command files, a dated standards authority registry, a 50-title FT50 2026 journal roster, a **selected only** AJG 2024 accounting/finance grade-4 subset, a reproducibility template, and a separate deterministic, local non-authoritative standards router. The prior SEC US-GAAP XBRL evidence module and all existing finance/audit capabilities are preserved.

**Not an assurance firm, regulator, IFRS-certified tool, ESEF validator, official standards distributor, licensed publisher research corpus or connected live MCP service.** No claim of verification until actual sources inspected and checks performed.

## Run local tests
`python -m unittest discover -s tests -q`

## New references
- `references/ISSB_ESG_ASSURANCE_RESEARCH_V330.md`
- `references/MASTER_ENGINEERING_PROMPT_V330.md`
- `standards/authority_registry.json`
- `research/ft50_2026_registry.json`
- `research/ajg2024_verified_accounting_finance_subset.json` (partial, not exhaustive)

See original V3.2 documents below for earlier capabilities.

---

# NAAIL Reporting Inspector

**IFRS® and XBRL™ financial reporting evidence review — research preview**

*Formerly FinanceCheck AI — NAAIL. This is a naming and scope clarification release (V3.2.1), not an IFRS or ESEF validator.*

See `references/BRAND_IFRS_XBRL_SCOPE_V321.md` for ownership, trademark and operational limitations.

---

# FinanceCheck AI — NAAIL V3.2.0

**Status:** Private ChatGPT skills plugin; public-safe GitHub source; separate local SEC XBRL reference module **NOT connected to ChatGPT or Claude**.

## What is new in V3.2

- Exact-concept SEC annual revenue comparisons from a fixed public API endpoint (`data.sec.gov/api/xbrl/companyfacts`), with CIK, form, accession, fiscal reporting dates, USD unit, filing cutoff, selection and restatement limitations.
- Distinct labels for completely fictional SEC-shaped fixtures, machine-extracted official SEC XBRL and full original filing review (**the last is not implemented**).
- SEC-network access disabled by default; when a trusted backend explicitly enables it, requests require a real SEC contact User-Agent. No arbitrary URLs and no confidential inputs.
- Added `sec-xbrl-evidence-review` skill; now **25 finance and accounting skills**.
- `evaluation/benchmark_200_sampling_plan.csv`: 200 **unfilled** evaluation slots; no company facts, labels, competitor results or comprehension outcomes invented.
- `evaluation/benchmark.py`: refuses to report a publishable 200-case score without completed independent double annotation.
- `references/CONSUMER_COMPREHENSION_PILOT_V32.md`: consented 12-person usability protocol, not executed.
- `tests`: versioned regression testing for financial arithmetic, privacy, SEC-shaped source selection, mocked HTTP and benchmark controls.

**Do not claim:** a hosted finance MCP, verified real-company reporting from this release, audited SEC source, live ERP access, completed benchmark results, scientific superiority over competitors or a ChatGPT public-directory listing.

## Development commands

```bash
python -m unittest discover -s tests -v
python -m sec_evidence.mcp_stdio
python -m evaluation.benchmark --make-plan evaluation/benchmark_200_sampling_plan.csv
```

See `references/SEC_XBRL_PROVENANCE_V32.md` and `references/MCP_DEPLOYMENT_V32.md` before testing SEC access outside the offline suite.

---

## Earlier release notes — FinanceCheck AI — NAAIL V3.1.0 (quality update)

**Scope:** public/synthetic-only educational finance and accounting workflows, short-form finance learning, arithmetic from supplied inputs, and local STDIO MCP reference. No live filing retrieval, client or bank access, vendor-licensed data, financial advice or audit opinions.

For the v3.1 quality patch, see `review/QUALITY_GATE_V31.md`, `references/QUALITY_CONTRACT_V31.md`, and `references/TOP_10_CHATGPT_COMPETITOR_QA_V31.json`.

# FinanceCheck AI — NAAIL V3.0

FinanceCheck makes finance accessible through short, accurate plain-language explanations, optional three-card stories, a voluntary one-question lesson, and existing synthetic/public accounting arithmetic exercises.

**Public-first but evidence-conservative:** No original source is claimed verified until truly inspected. The provided MCP demo is local and unconnected. Do not upload confidential client/personal or licensed-restricted datasets. No bank, SEC, ERP or vendor account integrations are embedded.

## V3 changes
- Six new skills: `discover-finance`, `finance-story-cards`, `ethical-customer-growth`, `mcp-runtime-gate`, `finance-lesson-check`, `get-started` (24 skills total).
- Six new Claude commands (19 command markdown files total).
- Tested local stand-alone MCP JSON-RPC demo in `mcp_lab/` (no network or persistence) for revenue change, synthetic story card and finance glossary.
- Master prompt, short-form customer UX, ethical growth experiment, reviewer scorecard and MCP deployment readiness guidance.
- Reuses existing v2.2 educational arithmetic engine and its 54 synthetic regression tests in the **private development package** only. The public GitHub release must not include the private engine without IP clearance.

## Local verification
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## ChatGPT / Claude
ChatGPT personal private plugin is a skills-only installation, **not** a deployed MCP app. Claude skill/command package is provided for installation by the user, not installed remotely. The local MCP reference has never been authenticated with either consumer runtime.

See `references/MASTER_ENGINEERING_PROMPT_V3.md`, `references/MCP_DEPLOYMENT_READINESS.md`, `references/REVIEWER_SCORECARD_V3.md`.

Example inspectable public research leads (not executed): `research/verified_replication_leads.json`. The JAE archival research paper has public MIT-labelled GitHub code but includes WRDS data dependencies; free code does not make the research inputs free.
