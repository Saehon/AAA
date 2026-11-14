# FinanceCheck AI — NAAIL V3.2 Release Review

Date: 2026-11-14 | Product: financecheck-ai-naail | Review phase: independent local engineering

## Decision
**Release for private ChatGPT skills testing and publicly inspectable GitHub source only; not approved as a live, independently validated finance-verification service or universal ChatGPT Directory listing.**

## Baseline
V3.1 contained 24 skills and a local arithmetic/MCP demonstration. SEC source authentication and human-labeled benchmarks were absent. A separate local SEC XBRL workflow addresses part of that gap without claiming complete direct filing verification.

## What this release demonstrably implements
- Exact annual SEC XBRL revenue tag selection for USD 10-K facts, source CIK validation, filing accessions, filed/as-of filtering and annual period comparisons.
- Clear distinction among synthetic SEC-shaped fixture, optional live SEC Company Facts API response, and original 10-K document text (NOT inspected).
- Restatement and ambiguous-concept human-review gates. Disabled-by-default live SEC retrieval and a safe local STDIO MCP tool.
- Deterministic benchmark grader that refuses incomplete unlabeled "200-case" accuracy claims.
- 200 **blank** future-collection slots and consent-based financial comprehension pilot design (not executed).
- Preserves existing revenue arithmetic and accounting workflows, educational cards and privacy/rights exclusions.

## Required tests
Inspect `FinanceCheck_V3_2_Test_Report.txt`: all local test cases, with explicit mock/synthetic labels. Tests do not call live SEC endpoints and cannot validate actual real-world filings or a hosted MCP integration.

## Still blocked
- Real SEC network retrieval from this development environment (DNS resolution failure), real 10-K page/footnote inspection, and end-to-end hosted HTTPS MCP integration.
- Human-adjudicated 200 public claim observations and benchmark scoring. All 200 slots are blank.
- Consumer pilot data; protocol exists, but no participant data or results exist.
- EU/institutional IP/licensing/privacy and cybersecurity signoffs, real account publication/approval.

## Scope/rights
Publish only independently authored general SEC XBRL source module, clean skills/instructions, mock fixtures, test harness and benchmark plan. Full V3.1 arithmetic engine, restricted research algorithms, private Drive sources, credentials, personal banking and proprietary market data remain private. SEC API source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces; SEC fair access: https://www.sec.gov/about/developer-resources.
