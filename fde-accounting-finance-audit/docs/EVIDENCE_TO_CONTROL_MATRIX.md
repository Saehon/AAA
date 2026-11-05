# Research-to-Engineering Assurance Gates

This matrix turns the FT50/AJG/Q1 literature, university dissertations, and TLDR news signals into **falsifiable engineering requirements**. They are NOT features proven to exist unless marked "prototype".

| Gate ID | Evidence origins | Requirement | Reproducible acceptance test | Status |
| --- | --- | --- | --- | --- |
| G01 | JAR26_CHOI; MIT26_DOWNING | Support controlled data mapping and meaningful human intervention | Approver and reviewer events can be traced per exception and cannot be auto-approved | Proposed |
| G02 | JAR26_BLANKESPOOR; MIT25_SERT | Constrain generated financial narratives | Every material drafted numerical assertion maps to a verified source; missing evidence triggers abstention | Proposed |
| G03 | JAR22_COMMERFORD; HARVARD26_LONG | Evaluate overreliance and adverse outcomes | Compare performance in conflict cases against blinded expert labels, including tail errors | Proposed |
| G04 | JAE26_DEE; IJAIS25_AUDITABILITY | Account-level control owner and source lineage | All released ICFR findings have valid evidence object, assertion, owner and approved closeout record | Proposed |
| G05 | RFS25_MISSING; HARVARD25_SARKAR | Prevent missingness bias and time leakage | Period- and entity-disjoint train/test; missing-pattern audit and no future text | Proposed |
| G06 | MNSC24_PRICING; MIT24_ZHAO | Finance baselines and economic constraints | Simple baseline, economically grounded negative controls, calibrated error and tail cost | Proposed |
| G07 | BAR26_MA; MAR25_BOERNER; STANFORD24_CAO | Human-centered controllership evaluation | Instrument practitioner decision quality, rework and business-context acceptance | Proposed |
| G08 | MIT25_SOUTH; TLDR26_SECRETS | Tenant-aware authorization and protected credentials | Negative tests for cross-tenant access, vault secret extraction and unapproved tool calls | Proposed |
| G09 | TLDR26_PROMPT; TLDR26_REWARD | Robust tool-input trust boundaries | Inject misleading instructions into source files; no unexpected action or altered test rubric | Proposed |
| G10 | TLDR26_TRACES; STANFORD25_MARKZHAO | Independent operational provenance | Reconstruct every synthetic decision from versioned inputs, code hash, rule ID and reviewer event | Proposed |
| G11 | TLDR26_DAYJOB; HARVARD26_LONG | Long-horizon case evaluation | Multiple supporting files, conflicting information, expert acceptance rubric, cost and error tracking | Proposed |
| G12 | JAR26_CHOI; IJAIS25_KOKINA | Retain existing deterministic engine boundaries | Previously authored pure-function and API tests remain passing after research additions | Prototype |

**Result interpretation:** A passing GitHub Actions suite validates the current code tests only. It does not satisfy the proposed gates, prove operational effectiveness, or validate any publication hypothesis.

Research IDs resolve in [academic](../research/academic_sources_2022_2026.json), [theses](../research/university_theses_2022_2026.json), and [TLDR](../research/tldr_signals_2026.json) registers.
