---
name: sec-companyfacts-evidence
description: Select SEC Company Facts annual revenue with as-of provenance and fail-closed ambiguity controls.
---
# SEC Company Facts Evidence
Use engine/sec_companyfacts.py with offline JSON by default. Optional retrieval requires a contact User-Agent and internet connectivity. Reject missing, ambiguous, cross-concept, cross-unit and non-comparable annual observations. This prototype handles selected calendar-year US-GAAP USD revenue only. It does not independently inspect 10-K documents, assure restatements, or validate live SEC connectivity. Always label results SEC_COMPANYFACTS_METADATA_UNRECONCILED.
