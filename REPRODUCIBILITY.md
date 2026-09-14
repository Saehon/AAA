# AAA Reproducibility Contract

AAA treats reproducibility as a research-governance requirement. A notebook executing successfully once is not, by itself, a reproducible scientific result.

## Current maturity

AAA contains exploratory notebooks and research prototypes. The repository is therefore best treated as a **Research Prototype / Research Laboratory** rather than a fully validated software release.

Some legacy notebooks predate the current NAAIL reproducibility standard and may have unpinned dependencies, environment assumptions, external API dependencies, or incomplete run manifests. Those limitations should be disclosed rather than hidden.

## Minimum experiment record

For each material empirical or AI experiment, preserve where applicable:

- research question and hypothesis;
- Git commit SHA;
- notebook/script name and version;
- Python and package versions;
- model/provider/model-version identifier;
- prompt or policy version where an LLM is used;
- dataset origin, date/version, rights, and transformation steps;
- train/validation/test or temporal holdout design;
- random seeds and sampling rules;
- variable definitions and exclusions;
- evaluation metrics and baselines;
- raw or governed output references;
- robustness/falsification tests;
- failures and null results;
- human-review status.

## Environment

The root dependency manifest currently declares:

```text
streamlit
pandas
```

Individual notebooks may require additional packages. Before a result is described as reproducible, notebook-specific imports should be reconciled with an explicit environment/lock file.

A minimal setup is:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Notebook-specific instructions should be documented next to the notebook or study.

## Data and restricted material

Do not commit confidential client data, credentials, licensed standards text, restricted databases, or other material that cannot lawfully be redistributed. Restricted inputs may be represented by manifests, hashes, schemas, synthetic substitutes, or documented acquisition instructions.

See `DATA_SOURCES.md` for provenance rules.

## Scientific boundary

Reproducibility does not convert an exploratory model result into professional evidence. Stronger claims require appropriate construct validation, robustness, out-of-sample testing, adversarial review, and qualified human judgment.

## Recommended study structure

```text
study/
├── README.md
├── data_manifest/
├── notebooks/
├── src/
├── tests/
├── configs/
├── results/
└── run_manifest.json
```

A future validated release should make it possible for an independent researcher to reconstruct the environment, lawful inputs, transformations, analysis, and reported metrics from a frozen commit and documented manifests.
