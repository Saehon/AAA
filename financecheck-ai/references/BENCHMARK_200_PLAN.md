# FinanceCheck v3.2 — preregisterable 200-case benchmark

**Status: DESIGN ONLY — 0 independently adjudicated real-company cases collected or scored.**

## Objective
Independently evaluate public-company claim verification, not just local arithmetic. Freeze evaluation protocol and sample-selection seeds *before* viewing product predictions.

## Proposed balanced sampling strata (40 each; total 200)
1. Annual revenue growth and source accounting tag
2. Net income versus adjusted non-GAAP metrics
3. Operating cash flow and accrual-to-cash reasoning
4. Liquidity, debt and maturity claims
5. Restatements, reporting period traps, concept and currency mismatches

The v3.2 SEC revenue tool **only addresses stratum 1 and some period traps**. The other cases evaluate future product functionality or appropriate abstentions; a baseline may correctly return INSUFFICIENT EVIDENCE rather than a false claim.

## Ground truth and sampling
- Define objective sample years, document languages, revenue concept coverage, SEC CIK population and exclusions before running the benchmark.
- Preserve original filing URL, exact accession/document, relevant page/statement/note, public filing date and source hash. The `data.sec.gov` extracted fact alone does not count as a manually inspected complete original filing.
- Each case requires *two independent reviewers* (qualified accounting/financial reporting experts), blinded to model output, plus adjudication. Record definition disagreements, adjusted metric exclusions and genuine ambiguity.
- Use SEC/issuer original public sources; exclude licensed third-party proprietary data without permission. Do not include student, employee or private financial records.
- Partition a development set from a **held-out** independently collected test set; do not repeatedly prompt-engineer against the held-out labels.
- Preserve input claim, correct verdict, correct source citation, periods/units and allowed alternative explanations.

## Report separately
- Decision accuracy with Wilson 95% CI and denominator including abstentions
- Source-citation correctness measured by a separate human audit, not self-reported source URLs
- False support/false verification rate, including unsupported claims
- Abstention and retrieval coverage
- Error taxonomy: concept mismatch, reporting date, amendment/restatement, currency, calculation, hallucinated provenance
- Language/reading-level and accessibility subgroup results where consent/size permits
- Baselines against generic language-model workflows and relevant finance plugin capabilities on *exactly the same cases* when authorized; public product descriptions are not comparative performance evidence.

## Files
- `benchmark_200_sampling_plan.csv`: 200 **empty** sampling slots with status `TO_COLLECT`; neither companies nor gold labels are fabricated.
- `evaluation/benchmark.py`: strict evaluator that refuses fewer than 200 adjudicated records and requires two unique reviewers per case. Does not retrieve evidence or validate annotator identities.
- `tests/test_v32_benchmark.py`: synthetic tests of score computations and fail-closed input handling.

There are no real-company benchmark results in this release; no superiority over other ChatGPT plugins is claimed.
