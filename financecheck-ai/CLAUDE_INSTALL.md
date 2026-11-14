# Claude Code / Cowork distribution guide

Claude can use plugin instructions and commands from this self-contained package; **nothing has been installed into your Claude account or the official marketplace**.

The package contains `.claude-plugin/plugin.json`, `commands/` and `skills/`. It does not bundle other companies' plugin code, live ERP connectors or paid market-data access.

For local development in Claude Code, add a local marketplace source pointing at the reviewed GitHub repository or upload/import the ZIP using the supported Claude plugin interface. Example marketplace install patterns in Anthropic's public documentation:

```text
claude plugin marketplace add <github-owner>/<repository>
claude plugin install financecheck-ai-naail@naail-financecheck-marketplace
```

This command works **only after** an accessible GitHub repository contains the marketplace and plugin directory at the documented paths. Check the current Claude CLI documentation and its plugin-marketplace requirements first. A ZIP suitable for inspection and manual installation is included separately as `FinanceCheck_AI_V2_1_Claude_Plugin.zip`.

Proposed slash commands: `/financecheck-ai-naail:claim-check`, `/financecheck-ai-naail:close-check`, `/financecheck-ai-naail:valuation-check`, `/financecheck-ai-naail:reviewer-gate`. Availability/naming must be tested in the actual Claude runtime.

V3.4 adds six standalone commands. No cloud MCP or proprietary Google scientific agents are installed.
