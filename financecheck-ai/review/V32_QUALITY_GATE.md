# FinanceCheck AI — V3.2 Reviewer-Engineer Findings

**Outcome: Private engineering upgrade, public-safe GitHub source release; NOT ready to claim verified real-company performance or public ChatGPT Directory listing.**

| Gate | Status | Evidence |
|---|---|---|
| Existing finance engine regression | PASS (local) | Re-run existing V3.1 tests |
| SEC XBRL typed source selection | PASS (fictional test shapes) | Annual flow duration, exact us-gaap tag, CIK, USD, 10-K filing date/accn and as-of cutoff |
| Historical restatement warning | PASS (synthetic) | Conflicting same-period values require human review |
| Local STDIO MCP interface | PASS (synthetic) | initialize, tool list/call, size limits and disabled-by-default live fetch |
| SEC real endpoint executed | NOT_TESTED | Development container has no outbound DNS; no SEC live response retrieved |
| Underlying 10-K full document text inspection | BLOCKED | Not built; official extracted tags must not be called full filing review |
| 200 human-labeled claim evaluation | NOT_TESTED | 200 blank sampling slots; 0 labels; scorer rejects incomplete benchmarks |
| Consumer comprehension outcomes | NOT_TESTED | 12-person pilot plan, no participants/results |
| SEC fair access in multiworker production | BLOCKED | Needs shared rate limiting and monitoring, not only local 1 request/sec |
| Public hosted MCP | NOT_DEPLOYED | Current server is local STDIO, no HTTPS endpoint/security validation |
| Intellectual property and GDPR/privacy | BLOCKED | Institutional rights and hosted dataflow/transfer/privacy assessments outstanding |
| Public ChatGPT Directory | NOT_SUBMITTED | Private owner plugin can be updated; public listing requires developer portal review |

## Scientific claims prohibited
No verified improvements in model accuracy, no better performance than FinancialFilings/Fiscal.ai/etc, no validated audit/SOX/IFRS compliance, no production SEC connectivity, no real 200-case benchmark outcomes.

## Scope
An optional SEC XBRL module adds code paths that could retrieve public extracted facts when deployed with network, declared User-Agent and permission. No real source values were retrieved in the development container. Local test fixture represents **Fictional Training Corporation**, not an SEC filer.
