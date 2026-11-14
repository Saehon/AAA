# Claude / ChatGPT Distribution — FinanceCheck V3.2

## Claude
A separate Claude-compatible source package includes the existing Claude commands and 25 skill instructions plus the optional local SEC reference Python module. The package has NOT been installed in an authenticated Claude Cowork or Claude Code account; test manifest/command discovery in Claude before claiming installation.

Example Claude Code marketplace configuration (after verified GitHub source and permissions):
```
claude plugin marketplace add Saehon/AAA
claude plugin install financecheck-ai-naail@naail-plugins
```

These commands depend on Claude's current marketplace support and user account, and are not claimed tested or guaranteed. Use a new plugin marketplace only if the existing repository's `.claude-plugin/marketplace.json` passes validation.

## ChatGPT
The private ChatGPT skills plugin V3.2 can be updated through the connected Plugin Creator workflow. SEC Python code in the bundle is only a reference, not a connected hosted MCP server. Public directory publication requires a verified developer identity and a separate approval; the connected chat action cannot publish it directly.

## SEC source access
The local SEC reference explicitly requires an approved backend, the `FINANCECHECK_ENABLE_SEC_LIVE=1` environment variable and a real contact `FINANCECHECK_SEC_USER_AGENT`. Running from a private terminal is not an authorized substitute for hosted ChatGPT tools; no test in this release retrieved a real SEC companyfacts response.
