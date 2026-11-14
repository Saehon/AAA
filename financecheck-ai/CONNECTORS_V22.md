# Enterprise Connector Gate (not enabled in public plugin)

| Connector candidate | Use | Status |
|---|---|---|
| Snowflake, Databricks, BigQuery | financial data SQL/reporting | NOT CONNECTED |
| Microsoft 365 | approved document/workpaper review | NOT CONNECTED |
| Slack | approved team close status updates | NOT CONNECTED |
| NetSuite, SAP, QuickBooks, Xero | ERP read-only finance workflows | NOT CONNECTED |
| S&P Capital IQ / Kensho | licensed company tear sheets/earnings previews | NO ENTITLEMENT CONNECTED |

**In any future enterprise product:** Require separate authentication and user authorization, narrow read-only permissions, tenant separation, key vault, security/penetration testing, documented lawful basis, GDPR/AI Act assessment, retention, export/deletion, licensed entitlement proof and human review. Never ship blank secrets templates that result in uncontrolled access.

Current public plugin accepts only independently authorized public/synthetic material. No ERP/warehouse tools are bundled.
