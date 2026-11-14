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
