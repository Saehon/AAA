---
name: financial-claim-check
description: Explain public company financial disclosures in plain language and check whether structured revenue, profit, cash-flow or growth claims align with comparable figures and directly inspected original sources.
---

# FinanceCheck AI — public financial claims V3.2

1. Apply the privacy gate. Do not retrieve private Drive/GitHub research or licensed datasets. Never ask for individual banking records or confidential financial reports.
2. Identify company, source, fiscal period, reporting basis, consolidated vs segment, units, currency and exactly what the public user claims.
3. When permitted source retrieval tools exist, inspect original filings (SEC EDGAR or company investor relations) and record exact URL, date, section/page, primary statement or note. Source metadata supplied by a user is not independent authentication. Avoid silently mixing adjusted EPS, GAAP profit, cash flows or restated figures.
4. For a **structured directional statement**, run `claim_change` (current, prior, period and claimed direction). It tests arithmetic only; do not label claims VERIFIED solely from this result.
5. For simple income-statement consistency, run `statement_tie`; for ratios and variance, use the documented deterministic tasks. Without executable tools, mark NOT EXECUTED.
6. Seek contradictory evidence, alternate definitions or a missing denominator. Separate inference from facts. Never allege fraud simply because of an anomaly.
7. Classify overall result: VERIFIED AGAINST INSPECTED SOURCE (only when actual original and formula checked), PARTLY SUPPORTED, ARITHMETIC CONTRADICTED, INSUFFICIENT SOURCE EVIDENCE, or NOT CHECKED. When uncertain, abstain.
8. Present beginner summary first, then a traceability table with source/period/value/check status, uncertainty and what a professional should review. No personalized investment advice.

**Reviewer-engineer validation:** source authenticity, number equality, metric comparability, contradiction search, economic inference, uncertainty and data permissions must be checked independently. A numeric tie alone cannot validate a promotional claim.

## V2.2 invocation
Review any material conclusion with `reviewer-engineer`; use new specialized skills where available. Do not claim that instructions alone execute calculations.

## V3.2 extracted SEC evidence scope
If the user asks about US annual revenue, use `sec-xbrl-evidence-review`. SEC extracted XBRL facts must be distinguished from direct original 10-K document inspection and from synthetic fixtures. A retrieved SEC API response is never an audit opinion. When no genuine live tool/retrieval is available, mark NOT RETRIEVED; never infer a tool call from a bundled script.
