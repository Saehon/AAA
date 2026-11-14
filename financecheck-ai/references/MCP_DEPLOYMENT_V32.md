# SEC XBRL local MCP and production deployment boundary

## Local STDIO reference (NOT automatically connected to ChatGPT)
```bash
cd financecheck_v32
python -m sec_evidence.mcp_stdio
```
Responds to MCP initialize, tools/list and tools/call; live source is **disabled by default**. To authorize a live SEC retrieval **only in a permitted backend with internet access**:
```bash
export FINANCECHECK_ENABLE_SEC_LIVE=1
export FINANCECHECK_SEC_USER_AGENT='YourOrganization ARealContact@yourdomain.example'
python -m sec_evidence.mcp_stdio
```
Replace the contact string with your actual organization/address as required by the SEC; do not copy the placeholder into production. This local reference has not been connected to an authenticated ChatGPT/Claude product.

## Security/reliability requirements before remote MCP hosting
1. Select legal service operator, IP owners, user privacy terms and public test data policy. Never deploy sensitive data support until independently approved.
2. Host stable HTTPS remote MCP; implement official current MCP streamable-HTTP transport and authentication/permissions (as needed); perform end-to-end client scan. STDIO JSON-RPC behavior does **not** prove remote transport compatibility.
3. Implement shared SEC request throttling/caching across *all* nodes (<10 requests/second SEC global fair-use; choose far less), proper User-Agent contact, timeouts, 429 handling without retry storms, circuit breakers, SEC availability status and retention policies.
4. Do not allow users to submit arbitrary HTTP URLs, cookies, authentication tokens or private filings. Prefer typed, bounded CIK, year, exact US-GAAP concept, as-of date and optional public claim.
5. Add observability without storing personal identifiers or raw nonpublic financial records; risk and privacy review before actual telemetry.
6. Run schema validation, replay testing, load/security/red-team tests, provenance checks, policy review and independent 200-case human-labeled benchmark before claiming accurate financial verification.
7. Developer identity verification and applicable OpenAI review must be completed from the user account; neither GitHub source publication nor a private plugin update is a public marketplace listing.

SEC documentation: https://www.sec.gov/about/developer-resources
OpenAI official plugin submission: https://developers.openai.com/plugins/deploy/submission
