# TLDR AI technology watch → FDE engineering backlog

**Checked 5 November 2026.** TLDR AI and related TLDR newsletters are news curation resources, *not peer-reviewed scholarly evidence or an automated provider connector in this project*. We reviewed dated public editions and linked them to testable engineering changes rather than copying article text. Sponsored and editorial material must be distinguished.

| TLDR issue | Research / engineering signal | FDE engineering task | Maturity |
| --- | --- | --- | --- |
| [2026-09-25](https://ai.tldr.tech/p/2026-09-25-tldr-ai) | Finance agents need end-to-end, rubric-based evaluation | Create financial work case sets with supporting files and expert pass/fail rubrics; do not equate benchmark success with audit competence. | Planned |
| [2026-09-08](https://ai.tldr.tech/p/2026-09-08-tldr-ai) | Prompt injection through tool output | Test indirect prompt injection in document/tool output, enforce source/action boundaries and human approvals. | Planned |
| [2026-10-29](https://ai.tldr.tech/p/2026-10-29-tldr-ai) | Independent model benchmarking dilemma | Retain hidden gold sets and independent expert review; report version drift and leaderboard overfitting. | Planned |
| [2026-10-23](https://ai.tldr.tech/p/2026-10-23-tldr-ai) | Agent credentials and approval-based secret handling | Use identity vault/short-lived credentials, never send raw secrets to language-model prompts. | Planned |
| [2026-10-15](https://ai.tldr.tech/p/2026-10-15-tldr-ai) | Agent observability and evaluation traces | Implement trace IDs, model version, tool call outcome, cost and reviewer approval lineage. | Planned |
| [2026-06-26](https://signup.tldr.tech/ai/2026-06-26) | Reward hacking and evaluation shortcuts in coding agents | Protect scoring scripts from being changed by the agent and store evaluation assets separately. | Planned |
| [2026-09-14](https://signup.tldr.tech/ai/2026-09-14) | Real-world SWE tasks reveal gaps between agent benchmarks and enterprise work | Test multi-step enterprise work rather than isolated individual API calls. | Planned |

### Highest-priority engineering gates

1. **Independent outcome labels.** The agent must not write its own grading reference or mark itself successful. Use reviewer-approved test tasks and record evaluation code version (benchmark issues, TLDR 29 Oct).
2. **Agent action boundaries.** Treat incoming documents, tool outputs and retrieved webpages as untrusted. A prompt-injected source cannot authorize external transfers or change credentials (TLDR 8 Sep and 23 Oct).
3. **End-to-end financial assignments.** Build reproducible professional task suites: a request, relevant and irrelevant files, ground-truth exceptions, signed review and artifact acceptance. DAYJOB research shows why isolated Q&A is insufficient; original research source [DAYJOB arXiv:2610.01306](https://arxiv.org/abs/2610.01306) is a preprint/benchmark, not a FT50 study.
4. **Operational traceability.** Log bounded trace metadata, model/provider version, deterministic rule/fixture hash, tool errors, elapsed time and explicit approval decision, excluding secrets or private financial payloads (TLDR 15 Oct).
5. **Versioned costs and evaluation drift.** Compare cost per *professionally accepted task*, not tokens alone. Revalidate benchmarks after changing provider or source system.

### How to use this watchlist

The machine-readable watchlist is [research/tldr_signals_2026.json](../research/tldr_signals_2026.json). Run the offline triage tool below to see explicit priorities:

```bash
cd fde-accounting-finance-audit
python -m research.evidence_triage --feed tldr
python -m research.evidence_triage --feed theses
python -m research.evidence_triage --feed journals
python -m research.evidence_triage --check
```

The tool reads a **curated static register**; it **does not scrape TLDR, subscribe to an email account, read a newsletter inbox, or create a recurring monitor**. New items require human review and verification of primary evidence before inclusion. News and preprints inform the engineering hypothesis backlog; they are not allowed to validate finance/audit claims.

Use the original [TLDR AI archive](https://tldr.tech/ai/archives) for future scans and the source links in the watchlist for decisions.
