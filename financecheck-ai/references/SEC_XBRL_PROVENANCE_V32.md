# SEC evidence passport — V3.2 architecture

## Source-grade taxonomy
| Source grade | How earned | What it establishes | What it does not |
|---|---|---|---|
| `SYNTHETIC_SEC_SHAPED_FIXTURE` | Test code parses invented JSON | Arithmetic and edge-case behavior | Real issuer revenue or authenticity |
| `OFFICIAL_SEC_XBRL_COMPANYFACTS_API` | Backend performs permitted live GET of `data.sec.gov` | Values as returned by SEC public XBRL extraction at retrieval time, with accession | Complete 10-K/10-Q narrative, audit assurance or absence of restatements |
| `ORIGINAL_FILING_TEXT_INSPECTED` | **Not implemented** in this release | Would require fetching/parsing exact filed document, confirming text/tables/notes | Cannot be inferred from companyfacts or a fabricated URL |

## Evidence passport fields
CIK, issuer name, exact us-gaap concept tag, USD unit, annual duration start/end, form, SEC accession, filing date, revision flag, API URL, retrieval UTC, SHA-256, as-of cutoff, numerical comparison, claim verdict and reviewed-source limitations. Dates and metric taxonomy are not mere cosmetic metadata: they change comparability and the meaning of a claim.

## Protection against common defects
- **No silent tag coalescing:** four US-GAAP revenue concepts are considered; competing tags require explicit choice.
- **No FY field shortcut:** `fy` records reporting context; the actual fact `start` and `end` delimit the amount's time window.
- **No misleading real fixtures:** fabricated test CIK/accession data never get an SEC citation.
- **No quiet restatement:** differing recorded annual amounts across 10-K/10-K-A are flagged for human review.
- **No future look-ahead:** only facts with filed date on/before `as_of` are eligible. This filtering is *not* equivalent to reconstructing a historical API snapshot: the current SEC payload may omit records that were present at an earlier time.
- **No unit conversion:** the initial revenue workflow supports exact-tag USD only; others are blocked.
- **No SSRF:** the URL is constructed internally from a numeric SEC CIK and fixed `https://data.sec.gov/api/xbrl/companyfacts/` endpoint; arbitrary URLs are not accepted.
- **No runtime overclaim:** live fetch explicitly disabled by default; server returns a controlled error if not enabled. The plugin is not remotely connected.
- **Rate limit:** the local process self-limits to 1 SEC API request/second. Hosted multiworker deployments require a *shared* rate limiter, caching, logs and security review to comply with SEC fair access.

## Limitations of the current SEC XBRL prototype
1. Network access to `data.sec.gov` was unavailable from the development container; all execution evidence is from local tests, including synthetic SEC-shaped fixtures.
2. It cannot inspect a full 10-K HTML/PDF or locate individual note and page citations.
3. Company-specific/custom concepts and non-USD reporting are not supported by this bounded initial scope.
4. There is no hosted, authenticated HTTPS MCP endpoint or user-facing source ingestion integration.
5. Human verification must determine whether the extracted XBRL concept matches the user's intended revenue definition; selection is not a financial statement audit.

SEC documentation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://www.sec.gov/about/developer-resources
