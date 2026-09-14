# GitHub Copilot Instructions — AAA Audit & Accounting AI Laboratory

## Identity
AAA is a NAAIL OpenLab research laboratory for auditing, accounting AI, PCAOB-oriented analytics, TDABC, BERT/NLP, anomaly detection and reproducible experiments. Researcher: Saeid Homayoun, ORCID 0000-0002-2536-0446.

## How Copilot should work here
- Treat notebooks and scripts as research artifacts, not production claims.
- Preserve provenance, deterministic preprocessing and reproducible outputs.
- Separate synthetic/proxy examples from real empirical evidence.
- Add tests for leakage, metric correctness, schema assumptions and temporal splits.
- Prefer modular code over monolithic notebooks when refactoring.
- Keep generated outputs out of source logic when practical.

## Scientific protocol
Literature validation → competing hypotheses → ERA empirical design → controlled model/specification comparison → adversarial review → robustness/falsification → OOS/temporal validation → Chain-of-Evidence → Human Gate.

Never optimize for statistical significance, delete failed runs merely because results are unfavorable, or treat LLM judgments as ground truth.

## Audit/professional safeguards
- Do not represent outputs as audit opinions, regulatory conclusions or professional advice.
- Do not invent PCAOB/IFRS/ISA requirements.
- Use authoritative standards only when properly cited and legally available.
- Preserve human professional judgment.

## IP/licensing
Do not expose patent-sensitive POMELO/VERA internals, credentials, confidential data or restricted third-party content. Respect the repository license and all upstream rights. Public GitHub publication is not a patent filing.
