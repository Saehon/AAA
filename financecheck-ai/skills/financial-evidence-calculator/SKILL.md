---
name: financial-evidence-calculator
description: Calculate deterministic revenue growth from supplied financial figures with period, unit and evidence validation.
---
# Financial Evidence Calculator
Use `python engine/financial_metrics.py` with JSON on stdin containing `currency`, `current_period`, `prior_period`, `revenue_current`, `revenue_prior`. Never infer missing fields. Confirm fiscal periods, units, currency, restatements, consolidation and filing acceptance date before asserting comparability. Output remains `USER_SUPPLIED_UNVERIFIED` until original filings are verified. This is not a live SEC connector, assurance opinion or investment recommendation.
