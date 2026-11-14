# FinanceCheck AI — NAAIL V3.0

FinanceCheck makes finance accessible through short, accurate plain-language explanations, optional three-card stories, a voluntary one-question lesson, and existing synthetic/public accounting arithmetic exercises.

**Public-first but evidence-conservative:** No original source is claimed verified until truly inspected. The provided MCP demo is local and unconnected. Do not upload confidential client/personal or licensed-restricted datasets. No bank, SEC, ERP or vendor account integrations are embedded.

## V3 changes
- Six new skills: `discover-finance`, `finance-story-cards`, `ethical-customer-growth`, `mcp-runtime-gate`, `finance-lesson-check`, `get-started` (24 skills total).
- Six new Claude commands (19 command markdown files total).
- Tested local stand-alone MCP JSON-RPC demo in `mcp_lab/` (no network or persistence) for revenue change, synthetic story card and finance glossary.
- Master prompt, short-form customer UX, ethical growth experiment, reviewer scorecard and MCP deployment readiness guidance.
- Reuses existing v2.2 educational arithmetic engine and its 54 synthetic regression tests in the **private development package** only. The public GitHub release must not include the private engine without IP clearance.

## Local verification
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## ChatGPT / Claude
ChatGPT personal private plugin is a skills-only installation, **not** a deployed MCP app. Claude skill/command package is provided for installation by the user, not installed remotely. The local MCP reference has never been authenticated with either consumer runtime.

See `references/MASTER_ENGINEERING_PROMPT_V3.md`, `references/MCP_DEPLOYMENT_READINESS.md`, `references/REVIEWER_SCORECARD_V3.md`.
