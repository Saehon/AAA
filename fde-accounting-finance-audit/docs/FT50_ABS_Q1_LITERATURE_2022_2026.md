# Peer-reviewed evidence foundation | FT50 · ABS/AJG 4*/4/3/2 · Q1
**Curated through 5 November 2026.** This page contains original research-to-engineering summaries and official DOI links, not reproduced article text.

### Ranking integrity

**FT50** indicates membership of the Financial Times 2026 journal list. **AJG/ABS 2024** is the Chartered Association of Business Schools journal grade (4*, 4, 3, 2, 1). **Q1** here means the indexed journal's **2025 Scopus/SCImago quartile**, not a ranking of an article or a claim that its individual findings are causal. Journal rankings can change and do not guarantee applicability, data openness or replicability.

Sources: [FT 2026 list](https://www.ft.com/content/db863a0a-6524-45f9-bc52-fee997634bdc), [AJG 2024 accounting grades](https://journalindexes.com/ajg/accounting/), [journal comparison](https://journalranks.com/rankings/ft50/). For articles beyond the accounting list, cross-check venue classifications against the broader AJG guide.

| Study, year and DOI | Venue and scope | FDE design implication |
| --- | --- | --- |
| [Choi, Jung Ho (2026)](https://doi.org/10.1111/1475-679x.70052) | *Journal of Accounting Research*; FT50, AJG 4*, Q1 (2025) | Measure accountant overrides and error propagation, with professionally adjudicated task labels. |
| [Blankespoor, Elizabeth (2026)](https://doi.org/10.1111/1475-679x.70050) | *Journal of Accounting Research*; FT50, AJG 4*, Q1 (2025) | Separate machine-produced disclosure text from verified accounting assertions and cited sources. |
| [Commerford, Benjamin P. (2022)](https://doi.org/10.1111/1475-679X.12407) | *Journal of Accounting Research*; FT50, AJG 4*, Q1 (2025) | Evaluate audit reliance and aversion under contradictory evidence, not only overall task speed. |
| [Millo, Yuval (2024)](https://doi.org/10.1016/j.aos.2024.101567) | *Accounting, Organizations and Society*; FT50, AJG 4*, Q1 (2025) | Use independent outcome measures rather than self-referential model performance scores. |
| [Dee, Carol C. (2026)](https://doi.org/10.1016/j.jacceco.2025.101834) | *Journal of Accounting and Economics*; FT50, AJG 4*, Q1 (2025) | Connect account-level exceptions to evidence, control ownership and remediation workflow. |
| [Libby, Robert (2024)](https://doi.org/10.1111/1911-3846.12941) | *Contemporary Accounting Research*; FT50, AJG 4, Q1 (2025) | Require identifiable reviewer responsibility and independence safeguards. |
| [Ciconte, William A. (2026)](https://doi.org/10.1007/s11142-026-09967-y) | *Review of Accounting Studies*; FT50, AJG 4, Q1 (2025) | Require citations verified against source material and independent falsification. |
| [Shanthikumar, Devin (2026)](https://doi.org/10.1111/1475-679x.70083) | *Journal of Accounting Research*; FT50, AJG 4*, Q1 (2025) | Disaggregate information extraction speed from substantive analyst judgment. |
| [Cao, Sean (2024)](https://doi.org/10.1016/j.jfineco.2024.103910) | *Journal of Financial Economics*; FT50, AJG 4*, Q1 (2025) | Compare human-only, machine-only and combined conditions including tail losses. |
| [Krupa, T. J. (2026)](https://doi.org/10.1007/s11142-026-09940-9) | *Review of Accounting Studies*; FT50, AJG 4, Q1 (2025) | Distinguish informative signals from professional advice; require verified tax-context conditions. |
| [Boerner, X. (2025)](https://doi.org/10.1016/j.mar.2024.100904) | *Management Accounting Research*; AJG 3, Q1 (2025) | Measure controller adoption, interpretability and decisions rather than API latency alone. |
| [Kokina, Julia (2025)](https://doi.org/10.1016/j.accinf.2025.100734) | *International Journal of Accounting Information Systems*; AJG 2, Q1 (2025) | Threat-model hallucination, privacy, robustness and automation overreliance before field use. |
| [Bryzgalova, Svetlana (2025)](https://doi.org/10.1093/rfs/hhae036) | *Review of Financial Studies*; FT50, AJG 4*, Q1 (2025) | Record missingness regimes and train/test leakage; compare imputation to complete-case outcomes. |
| [Chen, Luyang (2024)](https://doi.org/10.1287/mnsc.2023.4695) | *Management Science*; FT50, AJG 4*, Q1 (2025) | Use economically constrained baselines and out-of-sample evaluation rather than unconstrained model scores. |
| [Abbas, Khalid (2026)](https://doi.org/10.1016/j.bar.2025.101551) | *British Accounting Review*; Q1 (2025) | Frame the role of organizational and business-process change in management accounting. |
| [Du, Xingqiang (2026)](https://doi.org/10.1016/j.bar.2026.101950) | *British Accounting Review*; Q1 (2025) | Distinguish causal designs and proxy outcomes from independently observed audit decision accuracy. |
| [Li, Yueqi (2025)](https://doi.org/10.1016/j.accinf.2025.100739) | *International Journal of Accounting Information Systems*; AJG 2, Q1 (2025) | Audit model inputs, data governance, logs, oversight roles and reviewer competence. |
| [Tan, Jianhua (2025)](https://doi.org/10.1016/j.irfa.2025.104271) | *International Review of Financial Analysis*; Q1 unverified | Treat associational audit-quality proxies separately from operational testing; ranking not verified for this entry. |

### Research-to-architecture synthesis

**Accounting:** Human intervention and disclosure validation should be measured independently of processing time (Choi and Xie, 2026; Blankespoor et al., 2026). The demo API can flag journal imbalances, but cannot claim to verify authentic support documents.

**Audit / ICFR:** Auditor skepticism, account-level CAM effects, auditability and documentation are distinct constructs (Commerford et al., 2022; Dee et al., 2026; Li and Goel, 2025). Any commercial pilot needs a provenance-controlled evidence store and actual reviewer approval flow.

**Finance:** Risk modeling must distinguish economic objectives, missingness, out-of-sample error and tail losses (Cao et al., 2024; Bryzgalova et al., 2025; Chen et al., 2024). The current finance module calculates simple ratios; it has not been validated as an investment or treasury decision agent.

**Management accounting:** Implement a controller-usefulness study evaluating information context, decision authority and analytics capability (Boerner et al., 2025; Abbas, 2026), rather than claiming productivity gains from API benchmarks.

**Science:** The most important empirical extension is a preregistered experiment comparing manual work, deterministic support, ungated AI, and evidence-gated/human-approved AI against a separately adjudicated gold set. No such study has yet been executed.

For exact citation records, data/code verification status, journal gradings and machine-readable entries see [the source register](../research/academic_sources_2022_2026.json).
