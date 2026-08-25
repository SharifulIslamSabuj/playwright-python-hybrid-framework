# 13 — Core Framework Development

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-CFD-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 6 — Project Setup |
| Step | Step 13 — Core Framework Development |
| Predecessor Documents | [01](01-Project-Vision.md)–[12](12-Project-Setup.md), all ✅ approved |

## 1. Implementation Summary

Implemented the reusable framework foundation exactly as designed in [11-Framework-Architecture.md](11-Framework-Architecture.md): configuration finalization, the fixture layer, `BasePage`, 5 Page Object skeletons, `BaseApiClient` + 3 concrete API clients (covering all 13 approved automated endpoints except the intentionally-omitted `updateAccount`), 2 utilities, a test-data foundation (typed model + builder), and the reporting/diagnostics defaults. **No business Test Case was implemented.** Two infrastructure-only validation files (`tests/test_setup_validation.py`, revised; `tests/test_framework_foundation.py`, new) prove the foundation actually works, following the same AUT-free validation precedent Step 12 established.

## 2. Files Created / Modified

**Created:**

| File | Implements |
|---|---|
| `src/utils/logger.py` | [11] §23 |
| `src/utils/data_generator.py` | [11] §22 |
| `src/data/models.py` | [11] §41 (typed payload model) |
| `src/data/users.py` | [11] §15 (data-loading/builder foundation) |
| `src/pages/base_page.py` | [11] §12 |
| `src/pages/home_page.py`, `signup_login_page.py`, `products_page.py`, `product_details_page.py`, `cart_page.py` | [11] §11 (skeletons) |
| `src/api/base_api_client.py` | [11] §13 |
| `src/api/products_api_client.py`, `brands_api_client.py`, `auth_api_client.py` | [11] §13 |
| `tests/conftest.py` | [11] §14 |
| `tests/test_framework_foundation.py` | Step 13 validation (infrastructure-only) |
| `docs/13-Core-Framework-Development.md` | This document |

**Modified:**

| File | Change |
|---|---|
| `src/config/settings.py` | Added computed report-path properties and `has_durable_*_account()` helpers (finalization, Section A) |
| `pyproject.toml` | Added diagnostics/reporting `addopts` (Section B/J) |
| `tests/test_setup_validation.py` | Fixed a genuine `asyncio`-loop conflict (Section 13) — the Step 12 file itself, not a Step 1–12 *document* |

**Docs 01–12 were not modified** — only `tests/test_setup_validation.py` (a Step 12 *code* artifact, not a document) required a fix, addressed in Section 13 below with full transparency.

## 3. Architecture Components Implemented

Directly against [11-Framework-Architecture.md](11-Framework-Architecture.md)'s section numbering:

- **§12 BasePage** — `goto`/`resolve_url`, `wait_for_load`, `is_visible`, `get_text`, `expect_visible`, `expect_text`. Contains no page-specific locators or business logic.
- **§11 Page Object skeletons** — 5 classes, each a thin `BasePage` subclass with a docstring citing the Test Cases it will serve at Step 14. No locators/actions yet, by design.
- **§13 API Client Architecture** — `BaseApiClient` (base URL, timeout, generic `get`/`post`/`put`/`delete`, response returned unassessed) + `ProductsApiClient`, `BrandsApiClient`, `AuthApiClient` implementing all 13 approved endpoint methods. `update_account` is **not** implemented (`AE-API-TC-013` is `MANUAL`, per [09](09-Automation-Scope.md) §5) — verified by an explicit test (Section 12).
- **§14 Fixture Architecture** — every fixture from the Step 11 table: `settings`, 5 page-object fixtures, 3 API-client fixtures (session-scoped), `unique_user_data`, `durable_valid_account`, `durable_existing_account`, `created_account_cleanup`.
- **§16 Configuration Architecture** — finalized with report-path computation.
- **§22 Utility Architecture** — `logger.py`, `data_generator.py`. No third utility was added (`AE-FA-001`'s broader TS utility set was deliberately not carried forward — [11] §22/§40).
- **§15 Test Data Architecture** — `NewUserPayload`/`Credentials` typed models, `build_new_user_payload()` builder, `ADDRESS_TEMPLATE`, `TEST_ACCOUNT_PASSWORD`, `INVALID_CREDENTIALS`. Deliberately not the full 33-dataset `TD-*` catalog (Section 7).
- **§24/§25 Reporting/Diagnostics** — realized entirely through `pyproject.toml` `addopts` (screenshot-on-failure, trace-retain-on-failure, `pytest-html` output) — no custom capture code, matching [11]'s own conclusion that `pytest-playwright`'s native flags are sufficient.

## 4. Fixture Strategy

Implemented exactly per [11-Framework-Architecture.md](11-Framework-Architecture.md) §14: function-scoped for anything depending on the per-test `page` or requiring isolation (page objects, `unique_user_data`, `created_account_cleanup`), session-scoped only for stateless resources (the 3 API clients, `settings`, the durable-account credential fixtures). Browser/context/page lifecycle was **not** reimplemented — `pytest-playwright`'s own `page` fixture is used directly (ADR-1). `durable_valid_account`/`durable_existing_account` call `pytest.skip()` with an explicit, cited reason when the corresponding environment variables are unset (they are, in this environment) — this is correct, designed behavior, not a defect, and is demonstrated by one deliberately-`@pytest.mark.skip`-marked test kept out of routine collection so the main suite's pass count stays unambiguous (Section 12).

## 5. Configuration Strategy

`src/config/settings.py`'s `Settings` dataclass, already scaffolded at Step 12, gained: `report_dir_path`/`screenshots_dir`/`traces_dir`/`videos_dir`/`html_report_path` (`pathlib.Path` properties, consumed conceptually by the reporting foundation) and `has_durable_valid_account()`/`has_durable_existing_account()` (explicit boolean checks, so no fixture or future page/API code can silently assume a blank credential string is a real one). No new environment variable was introduced beyond what `.env.example` (Step 12) already documented.

## 6. API Foundation

`BaseApiClient` wraps a per-instance `httpx.Client`, exposes `get`/`post`/`put`/`delete` plus a `base_url` property and `close()`/context-manager support, and logs every request/response pair at `DEBUG` level via `src/utils/logger.py` (satisfying [11] §13's "logging/diagnostics where specified" without inventing a new mechanism). **A deliberate, evidence-based design choice:** all POST/PUT/DELETE bodies are sent as form-encoded (`data=`), not JSON, because [02-Application-Analysis.md](02-Application-Analysis.md) §10's VERIFIED evidence describes the AUT's API as accepting *request parameters* (`email`, `password`, `search_product`, etc.), not a JSON body — matching this AUT's actual, documented request shape rather than a generic REST assumption. The three concrete clients implement all 13 approved endpoint methods with zero assertions inside them — every method returns the raw `httpx.Response` for the eventual Test Case (Step 15) to assert on.

## 7. UI Foundation

`BasePage` plus 5 skeleton Page Objects (`HomePage`, `SignupLoginPage`, `ProductsPage`, `ProductDetailsPage`, `CartPage`) — the exact 5 named in [11] §11, none of TS's `CheckoutPage`/`PaymentPage`/`ContactUsPage`, consistent with the scope-driven simplification that document already committed to. No locator, no business action, no page-specific assertion beyond the two generic helpers on `BasePage` itself exists yet — that is explicitly Step 14's work, per this step's instructions.

## 8. Utility / Data Foundation

Two utilities only (`logger`, `data_generator`) — both AUT-agnostic, matching [11] §22's explicit "avoid a generic dumping ground" rule. The test-data foundation is a **builder pattern, not a dataset catalog**: `build_new_user_payload(scenario)` produces a correctly-shaped, uniquely-emailed `NewUserPayload` on demand; only the two datasets safe to define without an account-creation dependency (`INVALID_CREDENTIALS`, `ADDRESS_TEMPLATE`) are defined as static constants now. The remaining 30 of 33 `TD-*` datasets from [08-Test-Data.md](08-Test-Data.md) are intentionally not yet materialized as code — they will be added incrementally as the Test Cases that need them are implemented (Steps 14–16), per this step's explicit instruction not to create the full catalog now.

## 9. Reporting / Diagnostics Foundation

Implemented entirely via `pyproject.toml` `addopts`, using `pytest-playwright`'s native CLI flags rather than custom code: `--screenshot=only-on-failure`, `--tracing=retain-on-failure`, `--html=reports/html/report.html --self-contained-html`. **Video remains off by default** — a deliberate carry-forward of [10-Automation-Strategy.md](10-Automation-Strategy.md) §15's choice to withhold the most expensive diagnostic artifact until a specific investigation justifies it. **One documented translation nuance:** [10] §15 describes trace capture as "on retry only"; `pytest-playwright` has no literal "retry-only" tracing mode, so `retain-on-failure` (trace kept only for tests that end up failing, none for tests that pass — including on retry) is used as the closest functionally-equivalent native option. A byte-for-byte "trace only during a retry attempt, discard if the retry passes" behavior would require a custom pytest hook beyond CLI flags; not built now, since it exceeds what [10] actually required and no case currently needs the distinction.

## 10. Validation Performed

1. **Formatting/static validation** — no linter/formatter dependency exists (deliberately — [10]/[11] never justified adding one, and Step 12 committed to a minimal dependency set); `py_compile` was run across all 17 new/modified Python files as the available syntax-validation substitute.
2. **pytest collection** — `pytest --collect-only -q`.
3. **Full suite execution** — `pytest -v`.
4. **Import-error check** — implied by both of the above completing without collection errors.
5. **Setup-validation regression check** — all 5 original Step 12 tests re-run.
6. **Business-test-case check** — `tests/ui/`, `tests/api/`, `tests/hybrid/` confirmed empty via direct directory listing.
7. **Secret scan** — pattern-based grep across every new/modified file.
8. **Project tree inspection.**
9. **`git status`.**
10. **TypeScript project unchanged** — `git status --short` in the reference project.

## 11. Test Results

| Metric | Result |
|---|---|
| Tests collected | 28 |
| Passed | 27 |
| Skipped | 1 (`test_durable_valid_account_fixture_skips_when_unprovisioned` — explicitly `@pytest.mark.skip`-marked, demonstrating correct skip behavior without cluttering the routine pass count) |
| Failed | 0 (after the fix in Section 13) |
| Import/collection errors | 0 |
| Business test cases found in `tests/ui`/`tests/api`/`tests/hybrid` | 0 |
| Secrets found (excluding the one documented, intentional disposable test-account password) | 0 |

`py_compile` succeeded for all 17 files with zero syntax errors.

## 12. Architectural Decisions Made This Step

| Decision | Reason |
|---|---|
| `BasePage.resolve_url()` factored out as a `@staticmethod`, separate from `goto()` | Enables pure, network-free unit testing of URL-joining logic — consistent with Step 12's precedent of never touching the live AUT during infrastructure validation |
| `BaseApiClient.base_url` exposed as a public property | Avoids tests reaching into the private `_client` attribute — a small correction made mid-step (originally accessed `client._client.base_url` in the first draft of the validation tests, fixed before finalizing) |
| Form-encoded (`data=`) request bodies, not JSON | Matches the AUT's actual VERIFIED request-parameter style ([02] §10), not a generic assumption |
| `created_account_cleanup` logs and swallows deletion failures rather than re-raising | Directly implements the "log, don't re-throw" pattern already logged as REFERENCE KNOWLEDGE in [05-Test-Strategy.md](05-Test-Strategy.md) §29 |
| One `@pytest.mark.skip`-marked test demonstrating the durable-account skip path | Keeps the routine suite's pass/fail count unambiguous while still proving the skip mechanism exists and works when manually run |

## 13. Deviations from Step 11

**One genuine, evidence-based deviation, fully disclosed:**

`tests/test_setup_validation.py::test_playwright_browser_launches` (a Step 12 artifact) originally opened its own `sync_playwright()` context manager. Once Step 13's fixtures made `pytest-playwright`'s plugin actively manage its own `asyncio` event loop within the same test session, that pattern broke with `playwright._impl._errors.Error: It looks like you are using Playwright Sync API inside the asyncio loop` — a real, reproducible failure, not a hypothetical one (full traceback captured during this session). **Fix:** the test now requests `pytest-playwright`'s own session-scoped `playwright` fixture instead of opening a second, independent context. This is a **bug fix to a Step 12 test file**, not a modification of any Step 1–12 *document* — no `docs/*.md` file was touched. It is disclosed here in full rather than silently corrected, per instruction.

No other deviation from [11-Framework-Architecture.md](11-Framework-Architecture.md) occurred — every class, fixture, and file matches the architecture's own naming and responsibility split exactly.

## 14. Deferred Items

Explicitly out of scope for this step, per instruction: Page Object locators/business methods (Step 14), API Test Cases exercising the clients (Step 15), the Hybrid test (Step 16), the remaining ~30 `TD-*` datasets (incremental, Steps 14–16), Dockerfile (Step 20+), CI/CD workflow (Step 19), and any live network call to `automationexercise.com` (deliberately withheld from this step's validation, consistent with Step 12's own precedent — see Section 17).

## 15. Known Risks / Issues

- **Durable accounts remain unprovisioned** — every fixture/test depending on `TD-USER-VALID-001`/`TD-USER-EXISTING-001` will skip (correctly) until QA-Lead-authorized provisioning occurs ([09](09-Automation-Scope.md) §30 item 4). This is expected, not a framework defect.
- **The `asyncio`-loop fix (Section 13) is a reminder, not a one-off** — any future code that opens its own `sync_playwright()` context alongside active `pytest-playwright` fixtures will hit the same error; this is now documented so Step 14+ implementers don't rediscover it the hard way.
- **API client methods have never been exercised against a live response** — construction and configuration are verified; actual request/response behavior (status codes, body shape) is unverified by this step **by design**, since exercising them would mean executing (a subset of) the business Test Cases this step is explicitly not allowed to implement. That verification is Step 15's job.
- **Form-encoding assumption (Section 6) is a design decision based on documented evidence, not yet confirmed against a live response** — carries the same "unverified until Step 15 actually calls it" caveat as the point above.

## 16. Step 13 Exit Criteria

- [x] Steps 1–12 reviewed before any change was made
- [x] No business Test Case implemented (verified: `tests/ui`/`tests/api`/`tests/hybrid` remain empty)
- [x] Configuration finalized, environment-driven, no invented credentials
- [x] pytest configured cleanly, no unnecessary plugins added beyond what Step 12 already justified
- [x] Fixture architecture implemented per [11] §14, correct scopes, no real account creation/deletion performed
- [x] `BasePage` contains only genuinely reusable operations, no business logic
- [x] API foundation implemented per [11] §13, using the architecture-approved client (`httpx`), no assertions inside client code
- [x] Utilities limited to what [11] §22 approved — no dumping ground
- [x] Test data foundation is a builder/model, not the full `TD-*` catalog
- [x] Page Object structure created, foundational only — no full page implementations
- [x] API client structure created, endpoint methods implemented, no endpoint *tests* written
- [x] Reporting/diagnostics foundation implemented via native `pytest-playwright`/`pytest-html` flags only — no Allure, nothing enabled globally beyond what [10] approved
- [x] `pages/` and `api/` verified to never import from each other (Section 3 — neither module imports the other; confirmed by inspection, not just by convention)
- [x] No secret committed (one documented, intentional disposable test-account password is the sole match, explained)
- [x] Dependency versions unchanged from Step 12 — no upgrade/downgrade performed
- [x] Approved HTTP client (`httpx`) and reporting approach (`pytest-html`) not replaced
- [x] pytest collection succeeds, 0 errors
- [x] All 5 original setup-validation tests still pass (after the disclosed Section 13 fix)
- [x] Full suite: 27 passed, 1 deliberately-skipped, 0 failed
- [x] No secrets introduced
- [x] Docs 01–12 unchanged
- [x] TypeScript reference project unchanged
- [ ] QA Lead Review & Approval

## 17. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 14 — UI Automation.
