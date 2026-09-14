# AAA — External Research Integrations

Owner: Saeid Homayoun  
ORCID: https://orcid.org/0000-0002-2536-0446

AAA uses external repositories as attributed research dependencies through adapters.

## Relevant integrations
- AuditData-API → `AuditDataAdapter`: general ledger, trial balance, receivables, payables, inventory and audit-data interchange.
- TimesFM → `TimesFMAdapter`: ICFR/control-risk forecasting, temporal validation and predictive audit analytics.
- yfinance → `MarketDataAdapter`: market validation, event studies and audit-report market-response research.
- Financial Sentiment / BERT / FinBERT → `FinancialNLPAdapter`: CAM/KAM, filing and disclosure text classification.
- fg-data-synthetic → `SyntheticDataAdapter`: synthetic ledgers, control failures, fraud scenarios and privacy-safe education datasets.

## Design rule
External Source → Adapter → Validation → Audit Analytics → Evidence/Provenance → Evaluation → Human Review

Upstream authorship, licenses and data terms remain controlling. AAA does not claim upstream code as original NAAIL IP.
