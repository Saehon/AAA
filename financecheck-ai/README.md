# FinanceCheck AI — NAAIL v2.1.0 (GitHub review candidate)

**Independent original research and educational finance plugin by Saeid Homayoun / NAAIL OpenLab.**

FinanceCheck AI helps readers understand public company financial statements, check submitted financial arithmetic and explicitly distinguish evidence, assumptions, contradictions and missing sources. It is designed for public/synthetic examples **only** and is **not** an audit, SOX opinion, accountant, investment adviser or company-wide ERP integration.

## Core user questions
- "Did this public company really improve revenue or just adjusted profit?"
- "Explain revenue, cash flow, debt and profitability to someone who never studied accounting."
- "Check the debit/credit arithmetic in this fictional journal entry."
- "Which entries in this *fictional* reconciliation do not match?"
- "Compare an illustrative DCF under different discount and terminal growth assumptions."

## Two modes
**Beginner:** source-linked, plain-language understanding; explicitly label unverified arithmetic and evidence.
**Professional education:** illustrative journal entries, reconciliations, variance bridges, simplified statement ties, ratio arithmetic, DCF, comps and LBO bridge.

## Engineering status
- ChatGPT private plugin V2.1.0 created and updated through Plugin Creator (not publicly listed).
- Cross-platform source candidate and 30 local synthetic unit tests prepared independently.
- Current GitHub branch contains **marketplace/skill distribution scaffold for review**; it is **not** the complete verified calculation engine and not a hosted service.
- The separate complete ZIP, with local deterministic arithmetic, is available from the creator's development package pending IP/license/security sign-off.
- No Claude marketplace installation or public approval is claimed.

## Privacy and limitations
No private GitHub/Drive accounts, personally identifiable finance records, payroll, student data, client audit workpapers, LSEG/Refinitiv/Audit Analytics datasets, protected IFRS text, POMELO/VERA/KIWI patent implementation or unpublished DARWIN data. A user declaring data "public" is not proof of lawful reuse. Never silently infer source authenticity, peer comparability, SOX certification or investment return from a numeric tie.

## Claude Code
Use the repository marketplace `Saehon/AAA` only after the corresponding branch is incorporated and reviewed; the market entry is rooted at `.claude-plugin/marketplace.json`. Current candidate branch may require local marketplace installation. Slash commands: `/financecheck-ai-naail:claim-check`, `/financecheck-ai-naail:close-check`, `/financecheck-ai-naail:valuation-check`.

## Review before merge
See [release-gates.md](release-gates.md). No use of unrelated projects' intellectual property or confidential data is authorized by this README.
