---
name: sec-xbrl-evidence-review
description: Evaluate a US public company's annual revenue growth claim by comparing exact SEC XBRL tags, filing accessions and dates, distinguishing a retrieved SEC API fact from a directly inspected 10-K and from fictional test data.
---
# SEC XBRL evidence review — V3.2

Use this workflow only for publicly filed US issuer facts; the user need only provide a company/CIK, fiscal year and optional stated revenue-growth claim. Apply `public-data-privacy-gate` before any data processing. Never ask for personal banking information, private Drive or licensed vendor datasets.

1. **Check actual runtime.** Follow `mcp-runtime-gate`. The package contains a **local STDIO reference** in `sec_evidence/mcp_stdio.py`, which does not run inside ChatGPT unless a real connected tool is advertised. Do not claim the SEC API has been contacted without a successful tool result. If connected SEC retrieval is unavailable, clearly state NOT RETRIEVED and offer an ordinary web-assisted inspection of original public filings when web tools actually exist.
2. **Inspect provenance** when a retrieval succeeds: SEC `data.sec.gov` domain, companyfacts endpoint, CIK, exact `us-gaap` concept, USD unit, period start/end, `10-K` form, filed date, accession and retrieval timestamp/hash. Do not equate reporting year (`fy`) with a fact's covered period. Do not mix annual and quarterly durations or adjacent/incomplete fiscal periods.
3. **Reject ambiguous data.** Do not silently choose between multiple available revenue concepts, custom/unavailable concepts, conflicting restated values, different units or missing facts. Flag human review rather than producing a definitive verdict.
4. **Calculate and label.** A claim may be `CONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES`, `INCONSISTENT_WITH_SELECTED_SEC_XBRL_VALUES` or `INSUFFICIENT_EVIDENCE_REVIEW_REQUIRED`. These are not audit opinions. If figures came from `SYNTHETIC_SEC_SHAPED_FIXTURE`, show FICTIONAL in the opening line and never attach invented SEC filing links.
5. **Make evidence visible.** Present the result in plain English, with a concise change calculation, sources, periods, as-of date, official extracted facts, limitations and what a reviewer still needs to inspect in the original filed 10-K/notes. SEC Company Facts API inspection alone does **not** mean you inspected the complete original filing documents.
6. **Share responsibly.** Only create a source-linked public story if actual source data were retrieved; never make a definitive verified badge if an original full filing and context were not inspected. For any material investment or assurance decision, recommend professional independent review.

Source and access standards: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://www.sec.gov/about/developer-resources . The backend must use the SEC fair-access policy, a declared contact User-Agent, global rate limits, safe retry strategy and no user-provided arbitrary HTTP URLs.
