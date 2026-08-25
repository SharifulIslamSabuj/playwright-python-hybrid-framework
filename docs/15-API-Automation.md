# 15 — API Automation

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-APIA-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 8 — API Automation |
| Step | Step 15 — API Automation |
| Predecessor Documents | [01](01-Project-Vision.md)–[14](14-UI-Automation.md), all ✅ approved |

## 1. Objective

Implement the approved API automation scope — the 13 `AUTOMATE` API Test Cases from [09-Automation-Scope.md](09-Automation-Scope.md) — reusing the `BaseApiClient`/concrete client architecture built in Step 13. Of the 13, **9 were implementable this step**; 4 remain blocked on the same account-provisioning authorization gate that blocked 5 UI cases in Step 14 (Section 16). `AE-API-TC-013` (`MANUAL`) was not implemented and not promoted. The Hybrid case (`AE-E2E-TC-003`) was **not** touched — that is Step 16.

## 2. Approved API Automation Scope

From [09-Automation-Scope.md](09-Automation-Scope.md) §5: 13 `AUTOMATE`, 1 `MANUAL` (`AE-API-TC-013`) among the 14 documented endpoints. This step implements only the `AUTOMATE` subset, and only the portion of it not blocked by the unresolved account-authorization dependency.

## 3. Exact Test Case IDs Implemented

`AE-API-TC-001`, `002`, `003`, `004`, `005`, `006`, `008`, `009`, `010` — 9 of the 13 approved `AUTOMATE` cases. Not implemented: `AE-API-TC-007`, `011`, `012`, `014` (blocked, Section 16) and `AE-API-TC-013` (`MANUAL`, out of scope by definition).

## 4. API Clients / Methods Used

All reused, unmodified, from Step 13 — **no API client code was created or changed this step**:

| Client | Methods Exercised |
|---|---|
| `ProductsApiClient` | `get_products_list()`, `post_products_list()`, `search_product(search_product)` |
| `BrandsApiClient` | `get_brands_list()`, `put_brands_list()` |
| `AuthApiClient` | `verify_login(email, password)`, `delete_verify_login()` |

`AuthApiClient.create_account()`, `delete_account()`, `get_user_detail_by_email()` exist (Step 13) but were **not called** by any test this step (Section 16). `update_account` continues to not exist on the class at all, per Step 13's design and re-verified by the pre-existing `tests/test_framework_foundation.py::test_auth_api_client_does_not_implement_update_account`. No second API client architecture was introduced.

## 5. Test Data Used

| Test Data | Source | Used By |
|---|---|---|
| `SEARCH_KEYWORD_VALID` ("dress") | `src/data/products.py` (Step 14) | AE-API-TC-005 |
| `INVALID_CREDENTIALS` (TD-USER-INVALID-001) | `src/data/users.py` (Step 13) | AE-API-TC-008, 009 |
| None | — | AE-API-TC-001, 002, 003, 004, 006, 010 (no data required) |

No new Test Data was created this step — every dataset needed already existed from Step 13/14. No hard-coded product ID was introduced where live data mattered; `AE-API-TC-001`/`005` assert on the live, API-returned product list structure directly rather than a fixed expected product.

## 6. Test Architecture

Fixtures (`products_api`, `brands_api`, `auth_api`) reused unmodified from `tests/conftest.py` (Step 13) — session-scoped, stateless. One file per API resource area (`tests/api/test_products_api.py`, `test_brands_api.py`, `test_auth_api.py`), matching [11-Framework-Architecture.md](11-Framework-Architecture.md) §26. Every test is independently executable — none shares state with another, and none depends on execution order (confirmed by two consecutive full API-suite runs, Section 9). Request/response handling stays inside the API clients (`BaseApiClient._request`, Step 13); tests only call client methods and assert on the returned `httpx.Response` — no `httpx` call appears directly in any test file.

## 7. Tests Implemented

| File | Tests |
|---|---|
| `tests/api/test_products_api.py` | `test_ae_api_tc_001_get_products_list`, `test_ae_api_tc_002_post_products_list_unsupported_method`, `test_ae_api_tc_005_search_product_valid_parameter`, `test_ae_api_tc_006_search_product_missing_parameter` |
| `tests/api/test_brands_api.py` | `test_ae_api_tc_003_get_brands_list`, `test_ae_api_tc_004_put_brands_list_unsupported_method` |
| `tests/api/test_auth_api.py` | `test_ae_api_tc_008_verify_login_invalid_credentials`, `test_ae_api_tc_009_verify_login_missing_email`, `test_ae_api_tc_010_delete_verify_login_unsupported_method` |

9 tests. Every test's docstring states its Test Case/Scenario/Requirement/Test Data IDs and cites the VERIFIED expected result — the same traceability mechanism used in Step 14, no second system introduced.

## 8. Execution Commands

```bash
# Collection check
pytest tests/api --collect-only -q

# API suite in isolation
pytest tests/api -v --html=reports/html/api_suite.html --self-contained-html

# Complete existing suite (setup validation + framework foundation + UI + API)
pytest -v
```

## 9. Execution Results

| Run | Result |
|---|---|
| `pytest tests/api --collect-only` | 9/9 collected, 0 errors |
| `pytest tests/api` (run 1) | 9 passed, 0 failed, 5.44s |
| `pytest tests/api` (run 2, determinism check) | 9 passed, 0 failed, 5.36s |
| `pytest` (full suite) | **48 passed, 1 skipped (pre-existing, unrelated), 0 failed**, 90.81s |

All 12 previously-passing UI tests (Step 14) remain passing, unaffected by this step's changes — confirmed in the same full-suite run.

## 10. AUT Pass/Fail/Block/Restricted/Skipped Status

- **AUT passed (business behavior confirmed correct): 9/9** implemented cases — every documented status code and message ([07-Test-Cases.md](07-Test-Cases.md)) was independently VERIFIED to match live AUT behavior, with one important structural clarification (Section 11).
- **AUT failed:** none.
- **Blocked:** 4 (`AE-API-TC-007`, `011`, `012`, `014`) — authorization/data dependency, not a defect (Section 16).
- **Restricted:** none applicable at the API layer this step (the API-layer `RESTRICTED` cases, if any existed, would be out of scope the same way; in practice all 4 API `RESTRICTED`-adjacent concerns are the same account-mutation cases already covered under "Blocked").
- **Skipped:** 0 among the 9 implemented.
- **Not executed / out of scope:** `AE-API-TC-013` (`MANUAL`, never attempted).

## 11. API Behavior Observations

**The single most significant finding of this step:** every one of the 9 endpoints exercised returns **HTTP 200 at the transport layer, in every case tested — including every "negative"/error scenario** (missing parameter, invalid credentials, unsupported HTTP method). The documented status code (200/400/404/405) is carried **only inside the JSON response body**, as a `responseCode` field — never as the actual HTTP status. VERIFIED directly via raw `httpx` calls before any test was written (not assumed from the site's own `/api_list` documentation, which does not make this transport-vs-body distinction explicit):

```
POST /api/productsList        -> HTTP 200, body: {"responseCode": 405, "message": "This request method is not supported."}
PUT  /api/brandsList          -> HTTP 200, body: {"responseCode": 405, "message": "This request method is not supported."}
POST /api/searchProduct (no param) -> HTTP 200, body: {"responseCode": 400, "message": "Bad request, search_product parameter is missing in POST request."}
POST /api/verifyLogin (invalid)    -> HTTP 200, body: {"responseCode": 404, "message": "User not found!"}
POST /api/verifyLogin (missing email) -> HTTP 200, body: {"responseCode": 400, "message": "..."}
DELETE /api/verifyLogin       -> HTTP 200, body: {"responseCode": 405, "message": "This request method is not supported."}
```

**This is a discrepancy candidate against how earlier project documents implicitly framed these values.** [02-Application-Analysis.md](02-Application-Analysis.md) §10, [03-Requirement-Analysis.md](03-Requirement-Analysis.md) §6.3, [07-Test-Cases.md](07-Test-Cases.md), and [09-Automation-Scope.md](09-Automation-Scope.md) all list "405"/"400"/"404" as "Expected HTTP Status" without distinguishing transport-level status from an in-body status field — a reasonable reading of the site's own `/api_list` page (which likewise doesn't make this distinction explicit). **Per instruction, this document does not silently "fix" that framing in the earlier documents** — it records the evidence here and flags it for QA Lead review (Section 20/Final Report). Every test in this step asserts **both** facts explicitly and separately (`response.status_code == 200` and `body["responseCode"] == <documented value>`), so the automated suite is correct regardless of how the QA Lead ultimately wants the documentation framing reconciled.

**Secondary, schema-level observations (all newly and directly VERIFIED, not previously captured at this level of detail):**
- `GET /api/productsList` → `{"responseCode": 200, "products": [{"id", "name", "price", "brand", "category": {"usertype": {"usertype": ...}, "category": ...}}, ...]}` — the `category` field is a nested object, not a flat string.
- `GET /api/brandsList` → `{"responseCode": 200, "brands": [{"id", "brand"}, ...]}`.
- `POST /api/searchProduct` (valid) → same `products` array shape as `productsList`.
- The search-relevance rule remains unresolved (unchanged from [03](03-Requirement-Analysis.md)/[14](14-UI-Automation.md)) — `AE-API-TC-005`'s test deliberately asserts only structural correctness (non-empty list), not a relevance claim, for the same reason already established.

## 12. Defects or Defect Candidates Discovered

One defect **candidate**, not a confirmed application defect (this project has no channel to get third-party AUT behavior "fixed," per [04-Test-Plan.md](04-Test-Plan.md) §16's established framing): the HTTP-200-always pattern in Section 11 is unusual API design (a REST client relying on `response.raise_for_status()` or transport-level status codes alone would never detect these "error" responses) and is recorded here as an **observation for QA Lead awareness**, not filed as anything actionable against the AUT.

## 13. Framework Issues Discovered and Fixed

None. Every API client method built in Step 13 worked correctly against the live AUT on the first attempt, once the HTTP-200-always assertion pattern (Section 11) was understood and applied in the tests. No `BaseApiClient` or concrete client change was required.

## 14. Deviations from the Approved Plan

One, minor, self-corrected within this step: an initial draft of `tests/api/test_products_api.py` included a tenth test (`test_search_product_no_match_keyword_returns_empty_list`) not tied to any approved Test Case ID, intended as a diagnostic confirmation of the search "no results" behavior at the API level. Per this step's explicit "do not expand the approved automation scope silently" instruction, it was **removed before finalizing** rather than kept as an unofficial addition — the underlying finding (API search-no-match returns `responseCode: 200` with an empty `products` list, mirroring the UI's already-documented behavior) is recorded here as an observation (Section 11) instead of as a persistent automated test. No other deviation occurred.

## 15. Coverage / Traceability Summary

| Category | Count |
|---|---|
| API Test Cases approved `AUTOMATE` ([09]) | 13 |
| Implemented this step | 9 |
| Blocked (authorization/data gate) | 4 |
| `MANUAL`, out of scope | 1 |
| API requirement coverage (REQ-API-*) directly exercised | 001, 002, 003, 004, 005, 006, 008, 009, 010 (9 of 14) |

Full chain example: `REQ-API-004` → `AE-API-SC-004` → `AE-API-TC-004` → (no Test Data) → `test_ae_api_tc_004_put_brands_list_unsupported_method` — unbroken from [03-Requirement-Analysis.md](03-Requirement-Analysis.md) through to the executed test, for every one of the 9 implemented cases.

## 16. Remaining API Cases and Reasons

| Test Case | Reason Not Implemented |
|---|---|
| AE-API-TC-007 (verifyLogin, valid) | Requires `TD-USER-VALID-001`, the durable account — unprovisioned pending QA Lead authorization ([09](09-Automation-Scope.md) §12/§30 item 4, same gate as [14](14-UI-Automation.md) §8). **BLOCKED**, not reclassified. |
| AE-API-TC-011 (createAccount) | State-mutating; execution-authorization gate explicitly named in [09](09-Automation-Scope.md) §5. **BLOCKED**. |
| AE-API-TC-012 (deleteAccount) | Mandatory cleanup pair for TC-011 — cannot run standalone, and TC-011 is blocked. **BLOCKED**. |
| AE-API-TC-014 (getUserDetailByEmail) | Requires an existing account to query — same unprovisioned-account dependency as TC-007. **BLOCKED**. |
| AE-API-TC-013 (updateAccount) | `MANUAL` per [09-Automation-Scope.md](09-Automation-Scope.md) §5 — out of automated scope by design, not attempted. |

No blocked case's Step 9 classification was changed. All 4 blocked cases remain `AUTOMATE` in [09-Automation-Scope.md](09-Automation-Scope.md); this document records only that their *execution* is currently blocked — identical in nature and cause to the 5 UI cases blocked in Step 14.

## 17. Environment / Shared-State Limitations

- **No account was created, updated, or deleted.** No state-mutating request was ever sent to the AUT this step — verified by direct review of all 3 test files (none call `create_account`/`delete_account`).
- **All 9 executed requests were either read-only (`GET`) or explicitly negative-path (`POST`/`PUT`/`DELETE` requests documented by the AUT itself to be rejected/unsupported)** — none of the 9 mutated any shared state, including the "unsupported method" cases, which the AUT itself rejects before any mutation could occur.
- **The durable-account provisioning gap (Section 16) is the single limiting factor** preventing 4 additional cases from running — identical in nature to Step 14's finding, now confirmed to affect both layers equally, as expected given they share the same underlying data dependency ([08-Test-Data.md](08-Test-Data.md) §7).

## 18. Security / Secret-Handling Verification

Pattern-based scan across all 3 new test files for `password=`/`api_key=`/`secret=`/`token=`-style literals: **zero matches**. `INVALID_CREDENTIALS` (fabricated, non-existent) is the only credential-shaped data used, reused unmodified from Step 13. No API key, token, or authentication header was needed or used, consistent with [02-Application-Analysis.md](02-Application-Analysis.md) §10's finding that none of the 14 endpoints requires one.

## 19. Regression-Suite Impact

Full suite grew from 39 to 48 tests (9 new API tests added), pass count grew from 39 to 48, skip count unchanged at 1, fail count unchanged at 0. All 12 UI tests from Step 14 re-ran and passed identically, confirming zero regression from the API layer's addition. Total full-suite runtime: 90.81s (API tests themselves added only ~5s; the rest is unchanged UI/browser overhead).

## 20. Step 15 Exit Criteria

- [x] Steps 1–14 reviewed; actual Step 13 API client implementation inspected before writing tests
- [x] Only `AUTOMATE` API cases implemented; `MANUAL` (`AE-API-TC-013`) not implemented or promoted
- [x] Exact Test Case IDs preserved from [07](07-Test-Cases.md)/[09](09-Automation-Scope.md); no new ID invented
- [x] Blocked cases documented with reasons, not silently reclassified (Section 16)
- [x] Existing `BaseApiClient`/concrete clients reused; no second API client architecture introduced; no client code modified
- [x] Existing configuration, fixtures, logging, and test-data architecture reused unmodified
- [x] `pages/`↔`api/` isolation verified clean; no UI/browser import in any API test
- [x] No arbitrary sleeps; no hard-coded secret; only the pre-existing disposable test data reused
- [x] Assertions validate real response status/body/message — never weakened to force a pass
- [x] A genuine AUT behavior discrepancy (Section 11) was recorded as evidence, not silently reconciled into the existing docs
- [x] One scope-expanding draft test was caught and removed before finalizing (Section 14), not shipped
- [x] Read-only/stateless cases implemented first, then negative/method-validation cases, per the required execution strategy — no mutating case was attempted without the required (currently absent) authorization
- [x] API suite run independently (9/9, twice, deterministic) and as part of the complete suite (48/49, 0 failed)
- [x] All previously-passing UI tests confirmed still passing
- [x] No unintended file changed — verified via directory/`git status` inspection
- [x] docs/01–14 unmodified
- [x] TypeScript project unmodified
- [ ] QA Lead Review & Approval

## 21. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 16 — Hybrid E2E.
