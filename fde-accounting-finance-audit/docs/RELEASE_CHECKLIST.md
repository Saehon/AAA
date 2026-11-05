# Public-release verification

A public source release must not inadvertently expose previously private materials. This release contains a **selected source subtree**, not any private repository commit history.

## Included
- [x] Locally authored FastAPI/typed rules code designed for demonstration.
- [x] Invented journal, treasury and finance examples.
- [x] Unit tests, synthetic rule sanity checker and CI.
- [x] Public bibliography containing links/DOIs only.
- [x] Human-review and production-limitation notices.
- [x] Apache-2.0 inheritance from existing public AAA repository.

## Excluded intentionally
- [x] Unpublished FT50 manuscript drafts and private research proposals.
- [x] Proprietary architecture and unpublished intellectual property.
- [x] Confidential and licensed datasets.
- [x] Google Drive private folder/document links.
- [x] Provider credentials, .env files and private repository references.
- [x] Private GitHub source branch, history and author-only documentation.

## Follow-up validation
- [ ] Run independently verified CI against the public commit and document the outcome.
- [ ] Run dependency / security scanning against fixed production package versions.
- [ ] Have a separate reviewer inspect source and licensing before outside reuse.
- [ ] Implement OIDC/SSO and enforce customer-based permissions before real use.
- [ ] Build independent professionally adjudicated evaluation data before any field accuracy claim.
- [ ] Create a *new* dedicated public repository when GitHub repository-creation permissions become available; maintain this public portfolio link meanwhile.

Status is intentionally **demo / not production**.
