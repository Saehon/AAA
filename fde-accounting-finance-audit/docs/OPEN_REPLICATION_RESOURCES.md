# Open research datasets, replication code and benchmark boundaries

**Last checked:** 5 November 2026. This is a list of project-relevant resource *pointers*. It does not download, mirror, relicense or assert unrestricted reuse rights over third-party materials.

| Research resource | Original source | Available material / usage | Required check before use |
| --- | --- | --- | --- |
| Missing Financial Data — Bryzgalova et al., *Review of Financial Studies* (2025; FT50, AJG 4*) | [Article DOI](https://doi.org/10.1093/rfs/hhae036); [Pelger data-and-code catalogue](https://mpelger.people.stanford.edu/data-and-code) | Author-linked empirical data and GitHub code are listed. A relevant baseline for missingness-aware financial feature engineering. | Check author repository's exact license, data provenance, updated dependencies and entity/time split. |
| Deep Learning in Asset Pricing — Chen, Pelger & Zhu, *Management Science* (2024; FT50, AJG 4*) | [Article DOI](https://doi.org/10.1287/mnsc.2023.4695); [Pelger data-and-code catalogue](https://mpelger.people.stanford.edu/data-and-code) | Author-listed data, economic-state series and GitHub code pointers; financial ML test baseline. | Do not present as direct validation of accounting audit screening; verify finance data rights and economic evaluation criteria. |
| GenScore — Blankespoor, deHaan & Li, *Journal of Accounting Research* (2026; FT50, AJG 4*) | [Peer-reviewed article](https://doi.org/10.1111/1475-679x.70050); [author-released GenScore register](https://github.com/ed-dehaan/GenScore) | Author-released AI-disclosure measure and associated data for research; candidate text provenance analysis. | Read repository rights; cannot claim to reproduce every original proprietary-model decision. |
| FinanceBench (not an FT50 paper) | [GitHub](https://github.com/patronus-ai/financebench), [paper](https://arxiv.org/abs/2311.11944) | Financial document Q&A benchmark with evidence-based answer evaluation; parts have constrained access. | Verify which subset and licensing terms are actually available; not a substitute for audit assertions. |
| FinQA (not an FT50 paper) | [ACL 2021 article](https://aclanthology.org/2021.emnlp-main.300/), [project site](https://finqasite.github.io/) | Financial table-text reasoning with programs; appropriate for numerical explanation regression tests. | Verify redistributability, dataset splits and task leakage; numerical reasoning does not establish ICFR effectiveness. |
| DAYJOB Finance (2026 preprint/benchmark, not FT50) | [arXiv preprint](https://arxiv.org/abs/2610.01306), [Hugging Face dataset card](https://huggingface.co/datasets/surgeai/DAYJOB-finance) | Long-horizon professional finance assignments and rubric-based evaluation; public subset reported. | Check current task and package licenses, benchmark access and whether an agent can tamper with rubrics. Do not claim current FDE demo passes this benchmark. |

## Priority for this project

**Stage 1:** Run the existing synthetic journal-entry and reconciliation controls only; add fixed reference-output tests and conflicting-evidence fixtures.

**Stage 2:** Prototype read-only financial statement numerical QA with licensed FinQA and/or permitted FinanceBench subsets. Evaluate answer accuracy, evidence provenance, abstention, per-case cost and harmful unsupported claims. These datasets are *not* bank-to-ledger or journal-entry truth sets.

**Stage 3:** Evaluate financial-data missingness and time leakage using openly licensed subsets of the published finance baseline code; compare no-imputation and pre-registered imputation strategies.

**Stage 4:** Formal user research with independently adjudicated accounting, audit and finance cases, human intervention tracking and appropriate approvals.

**No third-party source, data or code has been imported into this repository as part of this bibliography publication.** Dataset and software license compatibility must be independently reviewed before implementation. All present performance claims remain confined to synthetic unit tests.
