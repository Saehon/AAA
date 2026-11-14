# NAAIL Reporting Inspector — Brand, IFRS/XBRL Scope and Rights

**Display name:** NAAIL Reporting Inspector

**Descriptive subtitle:** IFRS® & XBRL™ Financial Reporting Review — Research Preview.

The user-facing name replaces *FinanceCheck AI — NAAIL*. The existing stable internal package identifier `financecheck-ai-naail` remains unchanged. It keeps current installs and source references intact; a distinct canonical ID requires a separate new plugin and installation.

## Trademark and certification boundary
IFRS® is a trademark of the IFRS Foundation; XBRL™ is a trademark of XBRL International. Both identify third-party standards and data formats only. No affiliation, endorsement, certification or conformant-software status is claimed. Do not use either official logo or register the descriptive subtitle as a brand without confirming the necessary rights.

- IFRS Foundation terms: https://www.ifrs.org/legal/terms-and-conditions/
- XBRL International trademark policy: https://www.xbrl.org/the-consortium/about/legal/trademarks-and-logos/

## What currently works versus what is proposed
Current 3.2.1: educational explanations, fictional financial examples, selected deterministic revenue calculations, optional local SEC US-GAAP XBRL source-evidence demonstration, reproducible synthetic/mock tests. No hosted MCP is available in ChatGPT, and no real-company benchmark score is claimed.

**Not implemented:** validating IFRS Accounting Taxonomy tags, processing iXBRL/ESEF filings to official conformance, validating company extensions and anchoring, IFRS 18 professional judgment checks, or auditing underlying financial statements. IFRS accounting materials must be used within applicable licensing terms.

## Development next gate
Add a separately reviewed XBRL taxonomy/instance validation service, use suitably licensed IFRS/ESEF taxonomy packages, run official conformance tests, and compare machine findings against independent qualified-accountant labels before any public claim of certification or professional decision support.
