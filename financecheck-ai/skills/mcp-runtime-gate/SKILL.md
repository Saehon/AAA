---
name: mcp-runtime-gate
description: Determine whether a genuine MCP server performed a finance calculation, distinguish local reference implementation from deployed tools and fail closed if disconnected.
---
# mcp-runtime-gate

Do not call or claim a FinanceCheck MCP tool unless the client actually advertises its connected tool interface. Local reference server under `mcp_lab/` is a test adapter, not deployed, registered or authenticated in ChatGPT or Claude. If unavailable, use independently available tools or clearly state NOT_EXECUTED.
For each execution, record tool name, input classification, accounting period, currency, numerical inputs, output, and runtime status. A result from arithmetic never constitutes an authenticated filing citation. A source URL that was merely supplied cannot become VERIFIED; verify through a separate original-document retrieval before a 'verified company claim' statement.
No credentials, bank/ERP access, vendor APIs, external HTTP, persistence or user telemetry. All real client or personal records are prohibited. Separate proof-of-concept tools from production MCP connection requirements (hosted HTTPS, domain verification, access control, rate limits, privacy policy, secure hosting and external red-team).

**V3.2:** `sec_evidence/mcp_stdio.py` is an optional local, opt-in SEC XBRL reference. It is not hosted, connected, or activated by the skill alone. The live endpoint is disabled unless a permitted backend explicitly enables it with its own User-Agent; the development environment was unable to retrieve SEC live data. Do not upgrade `OFFICIAL_SEC_XBRL_COMPANYFACTS_API` to an independently inspected complete 10-K.
