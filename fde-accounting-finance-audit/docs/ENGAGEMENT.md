# Forward Deployed Engineer — customer engagement exercise

This is a **fictional scenario** intended for portfolio demonstration, not a case study of an actual client.

## Situation

A hypothetical multi-entity company needs to reconcile cash transactions, inspect period-end journals and summarize near-term liquidity for finance leaders. The finance director requires transparency about why a case is flagged. The internal auditor requires traceability and a documented review decision. The security officer prohibits transmitting identifiable or confidential source data to an external model.

## Delivery plan

**Discover:** Identify primary ledger, bank statement, policy thresholds, approvers, legal entity boundaries, accounts and baseline review costs. Establish the control owners and list the actions the system may *never* perform without approval.

**Prototype:** Demonstrate read-only journal screening, exact one-to-one matching and liquidity calculation against invented fixtures. Present findings with rule IDs and support identifiers, not unsupported narratives.

**Validate:** Construct an independently adjudicated gold set, stratify by entity and accounting period, examine false-positive review burden, and test contradictory evidence. Verify eligibility/consent before involving employees or records.

**Secure:** Apply enterprise identity and evidence protection. Do not treat the demonstration API key as adequate or send protected data to an LLM.

**Pilot:** Design a side-by-side controlled trial against the existing manual workflow, measuring accepted decisions per reviewer-hour and severe missed exceptions, not just requests per second.

**Operate:** Define SLOs, incident response, error handling, model drift checks, source-system change management and explicit decommission/rollback rights.

## Demonstration script

1. Run the sample audit request and explain the specific journal imbalance and approval conflict.
2. Show that generated flags require professional review and evidence collection rather than automated posting.
3. Run the reconciliation sample to identify one match and unresolved ledger/bank items.
4. Run the finance sample, discuss where source assumptions and industry context matter.
5. Show that the LLM remains disabled by default.
6. Demonstrate validation behavior for malformed inputs and failed demo access control.
7. Explain which production safeguards remain unimplemented.

## Business-impact evaluation (proposed only)

Collect baseline and post-prototype review minutes, adjudicated acceptable decisions, unresolved-item aging and human override rates. Compute quality-adjusted throughput, false negatives weighted by expert-rated severity, review rework and cloud/service cost. Report uncertainty, adverse results and generalizability limits. **No percentage improvements are asserted without a measured trial.**
