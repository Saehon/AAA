# AAA Data Sources and Provenance Policy

AAA uses a mixture of synthetic examples, public/archival information, researcher-provided data, and—where separately licensed—restricted research datasets. This file defines how those sources should be represented.

## Core rule

A file being technically accessible does not mean it is lawful to redistribute, publish, train on, or include in an open repository.

Every material dataset used in an AAA study should have a provenance record containing, where applicable:

- source/provider;
- dataset or collection name;
- acquisition date;
- version/vintage;
- source URL or controlled-access reference;
- licence/terms/permission status;
- unit of observation;
- time period;
- key identifiers;
- transformations and exclusions;
- integrity/hash information where feasible;
- whether the data are public, licensed, confidential, synthetic, or model-generated.

## Evidence/source classes

AAA distinguishes at least:

1. public regulatory and filing data;
2. peer-reviewed research evidence;
3. licensed commercial research data;
4. researcher-provided data;
5. synthetic/digital-twin data;
6. model-generated or weak-label data.

These categories are not interchangeable. Synthetic or model-generated material should never be silently presented as observed professional evidence.

## Typical public research sources

Depending on the specific study, AAA may use or interface with public sources such as SEC EDGAR/XBRL filings, PCAOB public materials, issuer reports, and other regulator or standard-setter publications. The presence of a public webpage does not automatically grant unrestricted redistribution rights.

## Restricted and proprietary sources

Do not commit raw data from licensed databases, confidential engagements, restricted standards, private company systems, or other sources whose terms prohibit redistribution. Use a manifest, schema, synthetic surrogate, acquisition instruction, or secure reference instead.

## Synthetic data

Synthetic datasets should be explicitly labelled and should record:

- generation method;
- planted anomalies or labels;
- seed/configuration where relevant;
- whether any real confidential data were used to generate them;
- intended research/teaching scope.

Synthetic performance is not evidence of real-world audit effectiveness.

## Repository `data/` directory

Files under `data/` must be reviewed individually. Their presence does not imply that all files share the same provenance, licence, evidence quality, or publication permission.

## Publication gate

Before publishing results, verify that:

- the source can be cited accurately;
- the data-use terms permit the analysis and intended disclosure;
- transformations are documented;
- confidential or personally identifiable information is excluded or governed appropriately;
- reported sample counts and periods match the actual frozen dataset;
- any synthetic/model-generated evidence is labelled clearly.
