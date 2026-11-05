# Safety, privacy and professional boundaries

This is an experimental developer portfolio. It must not be deployed to a regulated client's production systems or used to issue audit opinions.

### What is included
- Synthetic examples; deterministic rules; bounded API schemas; evidence reference IDs; a *review required* field.
- A demo-only shared-key guard that can protect routes when `DEMO_API_KEY` is configured.
- Disabled-by-default optional external model drafting; no credential or customer data bundled.

### What is deliberately excluded
- Real customer accounts, health data, clients, employee identities, passwords, provider keys, licensed filings or unpublished manuscripts.
- Production enterprise single sign-on, tenant RBAC, secure evidence store, signed human approvals, real document verification, incident-management infrastructure.
- Authorized integrations with real bank, ERP, audit platforms or tax filing systems.

### Required before any practical pilot
1. Independently approved lawful data sources and processing contracts.
2. Enterprise IAM, tenant boundaries, secrets management, least privilege and secure logs.
3. Evidence integrity, source-level access restrictions, deletion/retention policy.
4. Third-party model transfer assessment and no model access to unapproved data.
5. Review and testing for prompt-injection, unauthorized access and unsafe generated recommendations.
6. Professional approval of findings and any subsequent accounting entries.
7. Independent statistical validation, monitoring and rollback controls.

A successful CI run confirms only the code checks selected by this repository. It is not a security certification, financial statement audit or assurance conclusion. See [technical design](TECHNICAL_DESIGN.md).
