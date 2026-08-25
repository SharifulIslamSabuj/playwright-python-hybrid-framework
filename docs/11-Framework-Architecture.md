# 11 — Framework Architecture

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-FA-001 |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Reviewer | QA Lead |
| Date | 2026-08-25 |
| Phase | Phase 5 — Framework Architecture |
| Step | Step 11 — Framework Architecture |
| Predecessor Documents | [01](01-Project-Vision.md)–[10](10-Automation-Strategy.md), all ✅ approved |
| Reference (not template) | TS `AE-FA-001` (read in full for this step), plus previously-inspected TS artifacts (`package.json`, `Dockerfile`, `playwright.config.ts`, `testConfig.ts`, CI workflow) |

## 1. Document Purpose

Defines the complete technical architecture of the Playwright + Python hybrid automation framework that Steps 12+ will implement: layers, folder structure, Page Object Model, API client design, fixtures, configuration, Docker/CI shape, and coding standards — for exactly the **31 approved automated Test Cases** ([09-Automation-Scope.md](09-Automation-Scope.md)) and the strategy already committed to in [10-Automation-Strategy.md](10-Automation-Strategy.md). No source code, dependency, Dockerfile, or CI workflow is created in this step.

## 2. Architecture Objectives

1. Support exactly the approved layer split — 13 API, 17 UI, 1 Hybrid — without over-building for cases that are `MANUAL`/`DEFERRED`/`RESTRICTED`.
2. Separate test logic, page/API interaction, test data, configuration, and utilities — never mixed in one file.
3. Enable the tiered execution model already approved (smoke/PR/main/nightly/release — [10](10-Automation-Strategy.md) §18/22).
4. Produce the failure-diagnostic evidence set already committed to ([10](10-Automation-Strategy.md) §15) using Python-native tooling.
5. Be Docker- and CI-ready in design, without prescribing files that belong to later steps.
6. Stay lean for the current 31-case scope while remaining extensible if `DEFERRED` cases are later promoted ([09](09-Automation-Scope.md) §27).

## 3. Architecture Principles

Directly inherited from [10-Automation-Strategy.md](10-Automation-Strategy.md) §2 and made concrete here: risk-based layering, API-first where the requirement is a backend contract, UI only for user-facing outcomes, exactly one justified Hybrid seam, stable/role-based locators, deterministic assertions, independent tests, minimal shared state, maintainability over cleverness, fast PR feedback, diagnosable failures, no blind retries. One addition specific to *architecture* (not strategy): **build only what the approved 31 cases need.** Every class, fixture, and folder proposed below is traceable to a specific Test Case or a documented cross-cutting need — nothing is added "for completeness."

## 4. Approved Automation Scope (Restated, Not Redecided)

| Layer | Count | Source |
|---|---|---|
| API | 13 | [09](09-Automation-Scope.md) §5 — 10 stateless + `createAccount`/`deleteAccount` paired |
| UI | 17 | [09](09-Automation-Scope.md) §5 — Home, Signup/Login/Logout, Products/Search/Category/Brand, Cart, Checkout gate, Recommended Items |
| Hybrid | 1 | `AE-E2E-TC-003` — UI product listing vs. API oracle |
| **Total automated** | **31** | Unchanged — this document does not revisit scope |

`updateAccount` (`AE-API-TC-013`, `MANUAL`) and all `DEFERRED`/`RESTRICTED` cases (Checkout E2E, Contact Us, Subscription, Product Review, search anomaly, quantity boundary, the 2 blocked Hybrid cases) have **no corresponding architecture component built now** — see Section 39 for how the architecture accommodates their future promotion without rework.

## 5. Framework Technology Stack

| Component | Choice | Status | Rationale |
|---|---|---|---|
| Language | Python | **Decided** (Project Vision) | [01](01-Project-Vision.md) §7 |
| Test runner | pytest | **Decided** (Project Vision) | [01](01-Project-Vision.md) §7 |
| UI browser automation | Playwright (Python), via the official `pytest-playwright` plugin | **Decided this step** | Provides `page`/`browser`/`context` fixtures and built-in screenshot/trace/video hooks natively integrated with pytest — the direct Python-ecosystem equivalent of what `@playwright/test` gives the TS project, without inventing a custom fixture layer for basic browser lifecycle |
| API client library | `httpx` | **Decided this step** | 13 of 31 cases (92.9% of API scope) need no browser at all; using Playwright's `APIRequestContext` would tie every API test to a browser-capable context for no benefit. `httpx` is a modern, well-maintained, sync-capable Python HTTP client — directly realizes the "Python-specific improvement" [10-Automation-Strategy.md](10-Automation-Strategy.md) §29/§30 flagged as a potential, not-yet-proven opportunity; this document is where that evaluation concludes. `requests` was considered as an equally valid alternative (Section 42, ADR-2). |
| HTML reporting | `pytest-html` | **Decided this step** | `@playwright/test`'s built-in HTML reporter (what TS's `reporter: 'html'` used) has no pytest equivalent bundled with `pytest-playwright` — `pytest-html` is the standard, minimal-dependency Python answer that fulfills the same requirement [10-Automation-Strategy.md](10-Automation-Strategy.md) §25 already approved (Playwright HTML report as sufficient baseline, Allure deferred) |
| Config/secrets loading | `python-dotenv` (RECOMMENDED, not final) | To be finalized during implementation | Standard, minimal choice for `.env` loading; no project-specific reason to prefer an alternative, so not elevated to "decided" |
| Dependency manager | Not decided | **To be finalized during implementation (Step 12)** | Steps 1–10 never committed to pip/poetry/uv specifically |
| Package/version pins | Not decided | **To be finalized during implementation (Step 12)** | No Python or Playwright version has been pinned anywhere in Steps 1–10 |
| Cross-browser engines | Chromium (primary), Firefox, WebKit (secondary, curated) | **Decided** ([05](05-Test-Strategy.md) §9, [10](10-Automation-Strategy.md) §17) | Native Playwright trio |

No technology above is introduced without a Steps-1–10 basis; where none exists, it is explicitly marked unresolved rather than invented.

## 6. High-Level Architecture

```
Test Specs (pytest)
        ↓
Fixtures (pytest, conftest.py)
        ↓
Page Objects  ──────────┬────────── API Clients
        ↓                │                ↓
BasePage / shared UI     │        BaseApiClient / shared API
   helpers                │           helpers
        ↓                │                ↓
Utilities + Test Data + Configuration (shared by both sides)
        ↓                                  ↓
Playwright Runtime (pytest-playwright)   httpx
        ↓                                  ↓
   Browser                          Automation Exercise API
        └──────────────┬──────────────────┘
                        ↓
        Reports (pytest-html) + Screenshots + Traces + Videos
```

UI and API are **parallel branches converging only at the shared utilities/config/data layer** — never coupled to each other directly, so an API test never depends on Playwright and a pure-UI test never depends on `httpx`. The one Hybrid test (Section 10) is the sole place both branches are used together, and it does so by composition at the test level, not by a new shared class.

## 7. Architectural Layers

| Layer | Contains | Depends On |
|---|---|---|
| Test Specs | pytest test functions, one file per module, tagged per Section 27 | Fixtures, Page Objects, API Clients |
| Fixtures | pytest fixtures (`conftest.py`) providing page objects, API clients, test data, cleanup | Page Objects, API Clients, Utilities, Config |
| Page Objects | UI interaction classes (Section 11) | BasePage, Utilities, Config |
| API Clients | HTTP request-building classes (Section 13) | BaseApiClient, Utilities, Config |
| Utilities | Data generation, file helpers, logging (Section 22) | Config only |
| Test Data | Static/dynamic dataset definitions (Section 15) | Utilities (for generated data), Config |
| Configuration | Base URL, timeouts, env flags (Section 16) | Nothing (leaf layer) |

## 8. UI Automation Architecture

Implements the 17 approved UI cases across 5 page objects (Section 11) plus BasePage (Section 12). Test files call page-object methods and assert on their return values or on locator-level `expect()` calls — no raw Playwright `page.locator(...)` calls inside test functions.

## 9. API Automation Architecture

Implements the 13 approved API cases across 4 API clients (Section 13) plus BaseApiClient. Test files call client methods and assert on the returned status code and parsed body — no raw `httpx.post(...)` calls inside test functions.

## 10. Hybrid E2E Architecture

Exactly `AE-E2E-TC-003`: the test function requests both a `products_api` fixture and a `products_page` fixture, calls `products_api.get_products_list()` and `products_page.get_rendered_products()`, and asserts the two results are consistent. **No new class is introduced for this** — the value is in the test's composition, not in a "HybridProductsClient" abstraction that would exist to serve exactly one test. This mirrors [10-Automation-Strategy.md](10-Automation-Strategy.md) §6's own conclusion, made concrete: API responsibility (data retrieval) and UI responsibility (rendering) each stay inside their existing layer; only the assertion crosses the boundary. Isolation is trivial here since the case is entirely read-only — no cleanup or state coordination is needed, unlike the two `DEFERRED` Hybrid cases that would require it.

## 11. Page Object Model Design

| Page Object | Responsibility | Serves Test Cases |
|---|---|---|
| `HomePage` | Navigation bar, category/brand panel visibility, featured/recommended items, **add-to-cart from the Recommended Items section** | `AE-UI-TC-001`, `AE-UI-TC-023` |
| `SignupLoginPage` | Signup form, login form (valid/invalid), logout, duplicate-email negative path | `AE-UI-TC-004/005/006/007/008` |
| `ProductsPage` | All-products listing, search, category browsing, brand browsing | `AE-UI-TC-011` (listing part), `012`, `013`, `019`, `020` |
| `ProductDetailsPage` | Product detail fields, quantity input, add-to-cart from detail | `AE-UI-TC-011` (detail part), `015`, `016` |
| `CartPage` | Cart contents/totals, remove item, "Proceed to Checkout" trigger and gate-modal assertion | `AE-UI-TC-015` (view), `016` (view), `018`, `024` |

**Deliberately not built:** `CheckoutPage`, `PaymentPage`, `ContactUsPage` — TS built all three (`AE-FA-001` §6); none serve any case in this project's 31-case scope, since Checkout beyond the gate is `DEFERRED` and Contact Us is `RESTRICTED`. Building them now would be dead code against unautomated cases — a direct, evidence-based simplification over the TS baseline (Section 40).

**Page-object responsibilities:** own locators, own single-step UI actions (`fill_login_form`, `add_to_cart`), and own page-specific, reusable assertions only (e.g., `assert_cart_gate_modal_visible()` — reusable because both `TC-024` and any future Checkout E2E case would need it). **Test responsibilities:** business-flow sequencing, the actual pass/fail assertion for that specific Test Case's expected result, and Test Data selection. **Explicitly must NOT be placed inside Page Objects:** test-specific assertions that only one test cares about, Test Data literals (must come from the test-data layer), `sleep()`/manual waits (Section 14 of [10]), and cross-page orchestration (that belongs in the test function, which may call multiple page objects in sequence).

## 12. Base Page Design

`BasePage` provides: shared navigation (`goto(path)`, base-URL aware), common wait/assertion helpers built on Playwright's own auto-waiting (not custom polling), and generic element-presence checks reused by every page object. Every page object above inherits from it. It contains **no** page-specific locators or business logic — those belong exclusively to the concrete page classes.

## 13. API Client Architecture

| API Client | Endpoints Covered (all VERIFIED, [02](02-Application-Analysis.md) §10) | Serves Test Cases |
|---|---|---|
| `ProductsApiClient` | `GET /api/productsList`, `POST /api/productsList` (405), `POST /api/searchProduct` (valid + missing-param) | `AE-API-TC-001/002/005/006` |
| `BrandsApiClient` | `GET /api/brandsList`, `PUT /api/brandsList` (405) | `AE-API-TC-003/004` |
| `AuthApiClient` | `POST /api/verifyLogin` (valid/invalid/missing-email), `DELETE /api/verifyLogin` (405), `POST /api/createAccount`, `DELETE /api/deleteAccount`, `GET /api/getUserDetailByEmail` | `AE-API-TC-007/008/009/010/011/012/014` |
| `BaseApiClient` | Base URL, shared request/response handling, status-code helper | Used by all three above |

No endpoint is invented beyond [02-Application-Analysis.md](02-Application-Analysis.md) §10's 14-endpoint inventory. `updateAccount` (`PUT /api/updateAccount`) is **not implemented** in `AuthApiClient` yet — it serves only `AE-API-TC-013`, which is `MANUAL`; adding it now would be unused code. **Request construction:** every call builds its payload from a `TD-API-*`/`TD-USER-*` dataset (Section 15), never an inline literal. **Response handling:** every client method returns both the status code and the parsed body to the caller — the client does not itself assert; assertions remain in the test function ([10](10-Automation-Strategy.md) §13). **Authentication handling:** none of the 13 endpoints requires a token/header ([02](02-Application-Analysis.md) §10) — credentials, where needed (`verifyLogin`), are payload fields, not auth headers. **Status-code validation:** performed in the test, using the value the client returns. **API test organization:** one test file per client/resource area (Section 26).

## 14. Fixture Architecture (pytest, `conftest.py`)

| Fixture | Scope | Provides | Notes |
|---|---|---|---|
| `page` | function | A fresh Playwright page/context per test | Supplied by `pytest-playwright` directly — not reimplemented |
| `home_page`, `signup_login_page`, `products_page`, `product_details_page`, `cart_page` | function | The corresponding Page Object, constructed from `page` | One fixture per class in Section 11 |
| `api_client` (or per-resource: `products_api`, `brands_api`, `auth_api`) | function or session | The corresponding API Client, constructed with the base URL from config | Session-scoped is safe since these clients are stateless wrappers around `httpx` |
| `unique_user_data` | function | A freshly generated `TD-USER-NEW-*`-shaped payload (Section 22) | Used by `AE-UI-TC-004`, `AE-API-TC-011` |
| `durable_valid_account` | session (RECOMMENDED) | The pre-provisioned `TD-USER-VALID-001` credentials | Read-only reuse across many tests — provisioning itself happens outside routine test execution ([10](10-Automation-Strategy.md) §9) |
| `created_account_cleanup` | function | Wraps `AE-API-TC-011`-created accounts and **guarantees** `deleteAccount` runs in teardown, even on test failure | The single most important isolation-safety fixture in this framework — directly closes the risk [10-Automation-Strategy.md](10-Automation-Strategy.md) §35 flagged ("if cleanup ever fails silently...") |
| `authenticated_page` (future) | function | A `page` with an already-logged-in session, for tests that need authentication as a precondition rather than as the thing under test | Not needed until `AE-UI-TC-021` is implemented; marked here for completeness, not built prematurely |

Fixture scopes favor `function` scope by default (isolation over speed, per [10](10-Automation-Strategy.md) §8) — `session` scope is used only for genuinely read-only, collision-free resources (API client instances, the durable account's credentials as *data*, never as mutable state).

## 15. Test Data Architecture

Maps directly onto [08-Test-Data.md](08-Test-Data.md)'s 33 `TD-*` datasets — no new data requirement is introduced, and no actual data file is created in this step.

| Data Class | Representation Plan |
|---|---|
| Static (`TD-USER-INVALID-001`, `TD-BRAND-*`) | Plain Python constants/dicts in a data module |
| Dynamic/durable (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) | Config-provided values (e.g., env vars), since these are provisioned once outside routine runs, not generated by the suite |
| Generated/runtime (`TD-USER-NEW-*`) | Produced by a data-generation utility (Section 22) at fixture time, following the builder pattern already recommended in [08](08-Test-Data.md) §22 |
| API-sourced (`TD-PRODUCT-*`) | Fetched live via `ProductsApiClient` at test setup — never hard-coded IDs |
| Auth data (`TD-AUTH-*`) | Derived from the corresponding `TD-USER-*` dataset, not duplicated |
| Cart/checkout data | Only `TD-PRODUCT-*`/quantity values are relevant to the 31-case scope (`TD-CHECKOUT-001`/`TD-PAYMENT-001` are not needed yet, since no Checkout-E2E case is automated) |

## 16. Configuration Architecture

A single config module reads: base URL (UI and API share the same domain — [02](02-Application-Analysis.md)), browser choice, headless/headed mode, default timeout, retry count (Section 30), worker count (Section 29), report output directory, and — separately — any account-provisioning-related values needed by `durable_valid_account`. Every value has a sensible default and is overridable via environment variable; **no secret or credential is ever hard-coded** (Section 37). Exact loading mechanism (`python-dotenv` + `os.environ`, or a typed settings object) is RECOMMENDED, not finalized (Section 5).

## 17. Environment Management

Only one environment exists — the live public Automation Exercise instance ([04](04-Test-Plan.md) §10); there is no staging/QA/prod distinction to manage. Environment management here is limited to: local vs. CI vs. Docker execution context (Section 32), and headless-by-default with headed available for local debugging. A `.env.example` (not `.env` itself) will document expected variables — not created in this step.

## 18. Browser Management

| Tier | Engines | Basis |
|---|---|---|
| Local development | Chromium (default), any engine on demand | [10](10-Automation-Strategy.md) §17 |
| CI — PR/main | Chromium only | Same |
| CI — nightly/release | Chromium + curated Firefox/WebKit subset | Same |

Managed via `pytest-playwright`'s built-in `--browser` CLI flag and its multi-browser fixture parametrization — no custom browser-launch code is designed, since the plugin already provides this.

## 19. Authentication / Session Strategy

No token/session header exists at the API layer ([02](02-Application-Analysis.md) §10). At the UI layer, Playwright's per-context cookie/storage isolation is the mechanism (Section 8 of [10]); a future `authenticated_page` fixture (Section 14) may use Playwright's storage-state save/reuse feature once `AE-UI-TC-005` is implemented and stable — not before, since the login flow itself must first be proven, not shortcut.

## 20. Test Isolation Strategy

Directly implements [10-Automation-Strategy.md](10-Automation-Strategy.md) §8: function-scoped `page`/context fixtures give every UI test a clean browser state; every account-creating test uses `unique_user_data` + `created_account_cleanup`; every cart-touching test builds its own cart from scratch; the two durable accounts are used read-only. No test asserts on or depends on another test's leftover state.

## 21. Shared-State Protection

| Protection | Mechanism |
|---|---|
| Account collision | `unique_user_data` fixture generates a fresh identifier every run (Section 22) |
| Account mutation safety | `created_account_cleanup` fixture guarantees deletion — see Section 14 |
| Cart collision | Each test's cart-touching sequence is self-contained; no shared cart state assumed |
| Destructive-API safety | `deleteAccount` is only ever invoked by `created_account_cleanup` against the account it just created — never a durable account |
| Contact/Subscription/Review side effects | **Structurally absent from this architecture** — no page object or client method exists for them, since none of `AE-UI-TC-002/003/009/022` are in the automated scope |

## 22. Utility / Helper Architecture

| Utility | Purpose | Serves |
|---|---|---|
| `data_generator` | Timestamp/UUID-based unique email + full account-payload builder for `TD-USER-NEW-*` | `unique_user_data` fixture, Section 15 |
| `api_helpers` (or folded into `BaseApiClient`) | Shared response-status/body-parsing helpers | All API clients |
| `logger` | Structured execution logging for local debugging and CI visibility | All layers |

Kept intentionally small — TS's `fileUtils.ts`/`dateUtils.ts`/`assertionUtils.ts` (`AE-FA-001` §8) exist because TS automated invoice-download and multi-page shared assertions; neither is needed for this project's current scope (Section 40).

## 23. Logging Strategy

A single, structured logger (Python's standard `logging` module, configuration TBD at Step 12) used for: fixture setup/teardown visibility (especially account creation/deletion, given its risk profile — Section 21), and test-step context on failure. Not a replacement for pytest's own output — supplementary, for the account-lifecycle and API-request context that a bare assertion failure wouldn't otherwise show.

## 24. Failure Diagnostic Strategy

Directly implements [10-Automation-Strategy.md](10-Automation-Strategy.md) §15 using Python-native mechanisms: `pytest-playwright` natively supports `--screenshot=only-on-failure`, `--tracing=retain-on-failure`, and `--video=retain-on-failure` as CLI flags — no custom capture code is needed, only the CLI/config flags chosen at Step 12/implementation. API/Hybrid failures additionally log the full request/response pair via the `logger` utility (Section 23), since `httpx` has no built-in Playwright-style trace equivalent.

## 25. Reporting Architecture

Per [10-Automation-Strategy.md](10-Automation-Strategy.md) §25 (Playwright HTML report as sufficient baseline; Allure explicitly deferred, not silently added — matching Step 10's own inherited-from-TS conclusion): `pytest-html` generates the primary HTML report (Section 5's ADR explains why this, not a literal port of `@playwright/test`'s reporter). Reports and artifacts (screenshots/traces/videos) are written to a `reports/` directory (Section 33) — not committed to version control (Section 33/37).

## 26. Test Organization

One test file per module/resource, mirroring the Page Object / API Client boundaries above:

```
tests/ui/test_home.py            → AE-UI-TC-001, 023
tests/ui/test_signup_login.py    → AE-UI-TC-004, 005, 006, 007, 008
tests/ui/test_products.py        → AE-UI-TC-011, 012, 013, 019, 020
tests/ui/test_cart.py            → AE-UI-TC-015, 016, 018, 024
tests/api/test_products_api.py   → AE-API-TC-001, 002, 005, 006
tests/api/test_brands_api.py     → AE-API-TC-003, 004
tests/api/test_auth_api.py       → AE-API-TC-007, 008, 009, 010, 011, 012, 014
tests/hybrid/test_product_data_consistency.py → AE-E2E-TC-003
```

No test file exists for Checkout, Contact Us, Subscription, or Product Review — consistent with Section 4.

## 27. Test Tagging / Markers

Using pytest's native `@pytest.mark.<name>` (not a TS-style `@tag` string convention):

| Marker | Purpose | Matches |
|---|---|---|
| `smoke` | The 8-case smoke layer | [10](10-Automation-Strategy.md) §23 |
| `api` / `ui` / `hybrid` | Layer selection | Section 6 |
| `negative` | The 6 API + several UI negative cases | [07](07-Test-Cases.md) test types |
| `ci_restricted` | The 3 CI-RESTRICTED, MAIN/NIGHTLY-only cases | [09](09-Automation-Scope.md) §6 |
| `cross_browser` | The curated Section 18/[10] §17 subset | [10](10-Automation-Strategy.md) §17 |
| `regression` | Full 31-case set | [10](10-Automation-Strategy.md) §22 |

Every marker corresponds to a real, already-approved execution-selection need (Section 18 of [10]) — none is speculative.

## 28. Traceability Architecture

Every test function's docstring or a dedicated marker argument (e.g., `@pytest.mark.case("AE-UI-TC-024")`, exact mechanism TBD at Step 12) carries its Test Case ID, which in turn is traceable through `TD-*` (Step 8) → `AE-*-SC-*` (Step 6) → `REQ-*` (Step 3) via the documents themselves. This is the concrete implementation of the traceability chain [10-Automation-Strategy.md](10-Automation-Strategy.md) §28 already committed to. The traceability *matrix* itself is not built now, per instruction.

## 29. Parallel Execution Architecture

`pytest-xdist` (RECOMMENDED, not finalized) would provide worker-based parallelism. Applied per [10-Automation-Strategy.md](10-Automation-Strategy.md) §21's classification: SAFE cases (26 of 31) may run under multiple workers; the SERIAL mutation group (`AE-UI-TC-004`, `AE-API-TC-011/012`) must be pinned to run without concurrent overlap — either via a dedicated marker excluded from parallel workers, or a single-worker run for that subset, exact mechanism TBD at Step 12. Shared public AUT state (Section 21) is the binding constraint driving this, not CI speed.

## 30. Retry Strategy

Implements [10-Automation-Strategy.md](10-Automation-Strategy.md) §16 via `pytest-rerunfailures` (RECOMMENDED) or an equivalent, configured for **zero retries locally, a small bounded count in CI** — mirroring TS's own proven `{ci: 2, local: 0}` pattern (artifact-cited, not copied as config). A test that only passes on retry is still investigated per the transient/product/automation classification — retries are a CI convenience for genuinely transient failures, never a quality gate substitute.

## 31. CI/CD Architecture (design only)

```
Trigger (PR / push to main / nightly schedule / release)
        ↓
Checkout repository
        ↓
Set up Python + install dependencies (manager TBD, Section 5)
        ↓
Install Playwright browsers (Chromium for PR/main; + Firefox/WebKit for nightly/release)
        ↓
Run the tier-appropriate test selection (pytest markers, Section 27)
        ↓
Generate pytest-html report
        ↓
Upload report + screenshots/traces as CI artifacts
        ↓
Report pass/fail; CI-RESTRICTED tier only on main/nightly/release, never PR
```

No YAML file exists. Tier composition matches [10-Automation-Strategy.md](10-Automation-Strategy.md) §18/22 exactly.

## 32. Docker Architecture (design only)

| Aspect | Design |
|---|---|
| Why | Reproducibility, local/CI parity, onboarding — unchanged from [10](10-Automation-Strategy.md) §20 |
| Base image | An official Playwright-maintained Python-compatible image (Microsoft publishes `mcr.microsoft.com/playwright/python:<version>`) — **the direct Python-ecosystem analogue** of the TS project's own `mcr.microsoft.com/playwright:v1.61.1-noble` (artifact-cited precedent), not a copy; exact version TBD at Step 12 since no Playwright-Python version is pinned yet |
| Contents | Python runtime, project dependencies, Playwright browser binaries matching Section 18's tiers, project source |
| Environment configuration | Base URL and any future config passed as environment variables at `docker run`/CI time (Section 16) — never baked into the image |
| Test execution model | Default command runs the PR-tier selection (Chromium, non-CI-RESTRICTED); other tiers overridable via command args, mirroring the TS project's own "default Chromium suite, override at `docker run` time" pattern (artifact-cited) |
| Local usage | One-command reproducible run for a contributor without a local Python/Playwright setup |
| CI usage | Same image family used by the CI/CD pipeline (Section 31) for local/CI parity |
| Report/artifact handling | Reports/screenshots/traces written to a mounted or copied-out volume (Section 33's `reports/` directory), not lost inside the container |

No Dockerfile is created. The TS `Dockerfile`'s specific syntax and `npm ci` layer are explicitly **not** carried forward (Node-specific, no Python translation needed).

## 33. Repository / Folder Structure

```
playwright-python-hybrid-framework/
├── .github/
│   └── workflows/                  # (empty until Step 14+/19) GitHub Actions CI/CD
├── docs/                           # This document series (01-11), already populated
├── src/
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── signup_login_page.py
│   │   ├── products_page.py
│   │   ├── product_details_page.py
│   │   └── cart_page.py
│   ├── api/
│   │   ├── base_api_client.py
│   │   ├── products_api_client.py
│   │   ├── brands_api_client.py
│   │   └── auth_api_client.py
│   ├── config/
│   │   └── settings.py             # base URL, timeouts, env-driven config (Section 16)
│   ├── data/
│   │   ├── users.py                # TD-USER-*, TD-AUTH-*
│   │   ├── products.py             # TD-PRODUCT-*, TD-SEARCH-*, TD-CATEGORY-*, TD-BRAND-*
│   │   └── api_payloads.py         # TD-API-* structured payloads
│   └── utils/
│       ├── data_generator.py
│       └── logger.py
├── tests/
│   ├── conftest.py                 # Fixture definitions (Section 14)
│   ├── ui/
│   │   ├── test_home.py
│   │   ├── test_signup_login.py
│   │   ├── test_products.py
│   │   └── test_cart.py
│   ├── api/
│   │   ├── test_products_api.py
│   │   ├── test_brands_api.py
│   │   └── test_auth_api.py
│   └── hybrid/
│       └── test_product_data_consistency.py
├── reports/                        # Generated output only — gitignored
│   ├── html/
│   ├── screenshots/
│   ├── traces/
│   └── videos/
├── pytest.ini or pyproject.toml    # pytest config, markers (Section 27) — TBD which, Step 12
├── requirements.txt or pyproject.toml  # Dependency manifest — TBD, Section 5
├── .env.example
├── .gitignore
└── README.md
```

### Folder Responsibility Matrix

| Folder | Belongs Here | Must NOT Be Here |
|---|---|---|
| `src/pages/` | Page Object classes, locators, page-specific reusable assertions | Test-specific assertions, raw Test Data literals, `sleep()` |
| `src/api/` | API client classes, request/response handling | Test assertions, hard-coded payloads |
| `src/config/` | Base URL, timeouts, env-var reading | Secrets, actual credential values |
| `src/data/` | `TD-*` dataset definitions/builders | Real secrets, generated-at-import-time mutable state |
| `src/utils/` | Generic, reusable helpers with no AUT-specific knowledge | AUT-specific interaction logic (belongs in Pages/API) |
| `tests/` | pytest test functions, fixtures (`conftest.py`) | Reusable business logic that isn't test-specific (belongs in `src/`) |
| `reports/` | Generated evidence only | Anything hand-authored or version-controlled |
| `docs/` | This document series | Source code |

### Dependency Direction

```
tests/  →  src/pages/, src/api/  →  src/config/, src/data/, src/utils/
```

Strictly one-directional: `src/` never imports from `tests/`; `pages/`/`api/` never import from each other (Section 6's parallel-branch rule — the one Hybrid test composes them at the `tests/` level only); `utils/`/`config/`/`data/` never import from `pages/`/`api/`. This prevents the circular-dependency risk the instructions flagged, by construction rather than by convention alone.

## 34. Naming Conventions

Python-idiomatic (`snake_case` modules/functions, `PascalCase` classes) — deliberately **not** a mechanical port of TS's `PascalCase.ts` file-naming (e.g., TS `HomePage.ts` → Python `home_page.py` containing class `HomePage`). Test functions: `test_<test_case_id_slug>_<short_description>`, e.g. `test_ui_tc_006_invalid_login_shows_error`. Fixtures: noun-based, `snake_case` (Section 14 table already follows this).

## 35. Coding Standards

- Type hints used throughout (Python's equivalent of TS's "strict typing wherever practical," `AE-FA-001` §15) — not enforced as unavailable-if-impractical, but the same *principle*.
- Test files stay business-readable; no low-level locator strings inside test functions (only inside Page Objects, per Section 11).
- Prefer Playwright's `get_by_role`/`get_by_label`/`get_by_text` locators (Section 12 of [10]); stable CSS only when justified.
- No hard-coded test data inside test files — always via `src/data/` (Section 15).
- Page objects contain page behavior only, not test-specific assertions (Section 11).
- Tests are independent and safe to reorder (Section 20).
- Clear, consistent naming (Section 34).

## 36. Dependency Management

**Not finalized** — Steps 1–10 never committed to a specific manager. `requirements.txt` (simplest, most universally understood) and `pyproject.toml`-based tooling (Poetry, uv) are both viable; the choice is deferred to Step 12 Project Setup, where actual package installation happens. No dependency is installed in this step.

## 37. Security / Secrets Handling

No API key, token, or session credential exists for the AUT ([02-Application-Analysis.md](02-Application-Analysis.md) §10) — but account passwords (even disposable, test-only ones) and any future CI secret must never be hard-coded. `.env` (real values) is gitignored; `.env.example` (placeholder keys only) is version-controlled. Dummy payment data ([08](08-Test-Data.md) §23) is not currently needed by any automated case (Checkout is `DEFERRED`), so no payment-data handling concern exists yet in this architecture.

## 38. Maintainability Strategy

Directly implements [10-Automation-Strategy.md](10-Automation-Strategy.md) §24: one Page Object per screen, one API Client per resource, fixtures for all setup/teardown, `src/data/` for all data, `src/config/` for all configuration, minimal duplication (Section 6's parallel-branch rule prevents UI/API cross-contamination by construction), small focused test functions, controlled abstractions (no utility exists without a named consumer — Section 22).

## 39. Scalability Strategy

The architecture accommodates future scope growth **without rework**, by construction:

- A `DEFERRED` Checkout case being promoted (e.g., after route verification, [10](10-Automation-Strategy.md) §11) adds a new `CheckoutPage` class and `tests/ui/test_checkout.py` — it does not require restructuring any existing page object, since `CartPage`'s `proceed_to_checkout()` method already exists as the natural hand-off point.
- `updateAccount` being promoted from `MANUAL` to `AUTOMATE` adds one method to the existing `AuthApiClient` — no new class.
- Additional Hybrid cases (`AE-E2E-TC-001/002`, once unblocked) reuse the existing `AuthApiClient`/page-object fixtures exactly as `AE-E2E-TC-003` does — no new Hybrid-specific infrastructure is anticipated to be needed.
- Cross-browser expansion (Section 18) is a CI-tier/config change, not a code change — `pytest-playwright`'s browser parametrization already supports it.

## 40. TypeScript → Python Lessons

**Carried forward** (same architectural pattern, Python-native realization): layered architecture (Test Specs → Fixtures → Pages/API Clients → Utilities/Config), Page Object Model with a `BasePage`, one API Client per resource area with a shared `BaseApiClient`, fixture-provided page objects/API clients, centralized configuration, JSON/structured Test Data separated from test logic, screenshot-on-failure/trace-on-retry/video-on-failure-only evidence tiering, tag-based test selection matching real execution tiers, and the graduated CI cadence (Section 31).

**Improved, with evidence:**

| Improvement | Evidence It's Grounded In |
|---|---|
| Lean Page Object set (5, not 8) — no `CheckoutPage`/`PaymentPage`/`ContactUsPage` | [09](09-Automation-Scope.md) — those areas are `DEFERRED`/`RESTRICTED`, not automated |
| API client library independent of the browser runtime (`httpx`, not `APIRequestContext`) | [10](10-Automation-Strategy.md) §29 flagged this as a genuine, evaluated-now opportunity |
| No dedicated `updateAccount` client method built prematurely | [09](09-Automation-Scope.md) — `MANUAL`, not `AUTOMATE` |
| Explicit `created_account_cleanup` fixture as a structural guarantee, not a `finally`-block convention per test | [10](10-Automation-Strategy.md) §35 named exactly this risk ("if cleanup ever fails silently") — a fixture makes the guarantee structural rather than per-author discipline |
| No `fileUtils`/invoice-handling utility | No automated case touches invoice download (`AE-UI-TC-029` is `DEFERRED`) |

**Not carried forward:** the TS `types/` directory's TypeScript-interface pattern (Python's type hints live inline on functions/dataclasses, not in a separate interface-only module — a language-idiom difference, not a quality judgment), and the TS `Dockerfile`'s literal syntax (Section 32).

## 41. Python-Specific Improvements

Directly realizing [10-Automation-Strategy.md](10-Automation-Strategy.md) §30's design-only proposals, now made architecturally concrete: `pytest`'s native fixture system (Section 14) replaces TS's `test.extend()` pattern; `pytest.mark.parametrize` is the intended mechanism for the repeated unsupported-HTTP-method and category/brand-browsing cases (Section 27's markers, combined with parametrization at the test-function level — exact application at Step 13); a typed account-payload representation (Python `dataclass` or `TypedDict`, TBD at Step 12) reduces the risk of a silent field-name typo across the 5+ cases reusing the 16-field shape (Section 15).

## 42. Architecture Decisions (ADR Log)

| # | Decision | Reason | Alternatives Considered | Evidence/Source | Impact | Revisit Condition |
|---|---|---|---|---|---|---|
| ADR-1 | Use `pytest-playwright` for UI, not a hand-built Playwright wrapper | Official, maintained plugin already provides exactly the fixtures/CLI flags this architecture needs | Custom `conftest.py` browser-launch code | Playwright's own Python tooling ecosystem | Reduces custom code surface | If the plugin's fixture model ever conflicts with a project need |
| ADR-2 | Use `httpx` for the API layer, not Playwright's `APIRequestContext` | Decouples 13 API tests from any browser dependency; realizes [10] §29's flagged opportunity | `requests` (viable, more mature but sync-only and less modern API); `APIRequestContext` (would couple every API test to Playwright) | [10-Automation-Strategy.md](10-Automation-Strategy.md) §29/§30 | Faster, simpler API test execution; one more dependency to manage | If async API testing becomes a real need, `httpx`'s async support is a strict superset — no re-decision needed |
| ADR-3 | Use `pytest-html`, not a port of `@playwright/test`'s built-in reporter | No pytest-native equivalent of the JS reporter exists; `pytest-html` is the standard minimal-dependency answer | Allure (explicitly deferred by [10] §25, inherited from TS's own "optional future enhancement" framing) | [10-Automation-Strategy.md](10-Automation-Strategy.md) §25 | Simple, sufficient reporting for current scope | If richer cross-run trend analysis is ever genuinely needed |
| ADR-4 | 5 Page Objects, not 8 — no Checkout/Payment/Contact Us classes | Matches the actual 31-case approved scope; avoids dead code | Building all 8 "for future use" (rejected — violates Section 3's "build only what's needed" principle) | [09-Automation-Scope.md](09-Automation-Scope.md) | Leaner codebase; Section 39 shows this doesn't block future growth | When any `DEFERRED`/`RESTRICTED` Checkout-area case is promoted |
| ADR-5 | Function-scoped fixtures by default, session-scoped only for stateless/read-only resources | Isolation over speed, given the shared public environment | All-session-scoped (rejected — collision risk); all-function-scoped (rejected — unnecessary overhead for stateless API clients) | [10-Automation-Strategy.md](10-Automation-Strategy.md) §8/§21 | Balances safety and reasonable execution speed | N/A |
| ADR-6 | A dedicated `created_account_cleanup` fixture, not a per-test `try/finally` | Structural cleanup guarantee, closing a named risk | Per-test `try/finally` blocks (rejected — relies on every test author remembering, the exact risk [10] §35 named) | [10-Automation-Strategy.md](10-Automation-Strategy.md) §35 | Every account-mutating test automatically inherits the guarantee | N/A |
| ADR-7 | One-directional dependency rule: `pages/` and `api/` never import each other | Prevents circular dependency and accidental UI/API coupling, by construction | Allowing cross-imports "if convenient" (rejected — would make the one Hybrid test's boundary blurry for every future test) | Explicit instruction; [10] §3/§6 | The Hybrid seam stays visible and intentional, always at the `tests/` level | If a second genuine Hybrid case needs a shared abstraction — evaluate then, don't pre-build now |

## 43. Architecture Risks

Architecture-specific only — not a restatement of the full project risk register ([05](05-Test-Strategy.md), [09](09-Automation-Scope.md), [10](10-Automation-Strategy.md) already own that):

- **Public shared environment:** the entire fixture/isolation design (Sections 14, 20, 21) exists because of this constraint — if it is ever under-implemented at Step 12/13, every mutation-adjacent test inherits real collision risk.
- **Test data collision:** the `unique_user_data` generator (Section 22) is a single point of failure for uniqueness — if its collision-resistance is weaker than assumed, `AE-UI-TC-004`/`AE-API-TC-011` could intermittently fail for reasons unrelated to the AUT.
- **Account/session isolation:** the durable accounts (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) are shared, read-only resources by design — if any future test author accidentally mutates one, every dependent test silently breaks.
- **API/UI coupling:** the one Hybrid test is the only sanctioned crossing point (ADR-7) — if that discipline erodes over time, the clean parallel-branch architecture (Section 6) degrades.
- **Parallel execution:** the SAFE/LIMITED/SERIAL split (Section 29) depends on markers/exclusion being correctly applied at Step 12/13 implementation — a missed marker on a mutating test would reintroduce the exact risk this architecture is designed to prevent.
- **Browser differences:** Firefox/WebKit have never actually been run against this AUT by either project (a [10] §35 finding, inherited here) — the architecture supports it (Section 18), but the first real run is genuinely untested ground.
- **Docker reproducibility:** depends on an official Playwright-Python-compatible base image actually existing with the version this project eventually pins — not yet confirmed at the specific-version level (Section 32).
- **CI reliability:** the graduated tier model (Section 31) is only as good as its marker discipline (Section 27) — a mis-tagged test could run in the wrong tier.
- **Framework complexity:** deliberately kept lean (5 Page Objects, 4 API Clients, ~6 fixtures) for the current 31-case scope — the risk is scope creep during implementation adding structure the current scope doesn't justify (Section 3).
- **Maintenance cost:** concentrated in the same 3 cases [09-Automation-Scope.md](09-Automation-Scope.md) §21 already identified as MEDIUM maintenance risk (`AE-UI-TC-004`, `AE-API-TC-011/012`) — this architecture's cleanup fixture (ADR-6) mitigates but does not eliminate that concentration.

## 44. Implementation Sequence

Per the project's actual master roadmap (not a generic template):

| Step | Focus |
|---|---|
| **Step 12 — Project Setup** | Dependency manager decision, package installation, `pytest.ini`/`pyproject.toml`, initial `conftest.py` skeleton — the first point actual files are created |
| **Step 13 — Core Framework Development** | `BasePage`, `BaseApiClient`, config module, utilities, fixtures (Section 14) |
| **Step 14 — UI Automation** | The 5 Page Objects (Section 11) and their 17 test cases, Wave 1–4 order per [09](09-Automation-Scope.md) §27 |
| **Step 15 — API Automation** | The 4 API Clients (Section 13) and their 13 test cases |
| **Step 16 — Hybrid E2E** | `AE-E2E-TC-003` only |
| **Step 17 — Execution** | First real execution of the full 31-case suite; this is also where the account-creation/deletion authorization gate ([09](09-Automation-Scope.md) §30 item 4) must finally be resolved before Wave 3 cases can run |
| **Step 18 — Defect Documentation** | Per [10-Automation-Strategy.md](10-Automation-Strategy.md) §26's five-way failure classification |
| **Step 19 — CI/CD** | The workflow YAML this document deliberately did not create (Section 31) |
| **Step 20+** | Docker implementation, reporting/observability hardening, QA metrics, test summary, release readiness — per the project's Phase 6–24 roadmap already established in [01-Project-Vision.md](01-Project-Vision.md) §18 |

**Architecture vs. implementation, explicitly distinguished:** this document (Step 11) defines shapes, responsibilities, and boundaries; Step 12 is the first step where any file inside `src/`, `tests/`, or the repository root (other than `docs/`) is actually created.

## 45. Architecture Exit Criteria

- [x] Architecture Objectives defined and traceable to Steps 1–10 (Section 2)
- [x] All 45 requested sections present
- [x] Technology choices either decided-with-rationale or explicitly marked "to be finalized during implementation" (Section 5) — nothing invented
- [x] Folder structure includes responsibility matrix and explicit "must NOT belong here" column (Section 33)
- [x] Dependency direction explicitly defined, avoiding circular dependencies by construction (Section 33, ADR-7)
- [x] UI architecture defines Page Object scope matched to the actual 31-case scope, not the TS baseline's broader set (Section 11)
- [x] API architecture covers exactly the 13 approved endpoints, no invented endpoints (Section 13)
- [x] Hybrid architecture limited to the 1 approved case, no unnecessary complexity (Section 10)
- [x] Fixture architecture defines scopes explicitly (Section 14)
- [x] Test data architecture maps to all 33 Step 8 datasets without inventing new ones (Section 15)
- [x] Docker and CI/CD are design-only — no files created (Sections 31, 32)
- [x] Cross-browser strategy respects Step 5/10 — no claim of every-browser-every-PR (Section 18)
- [x] Parallelization respects the approved SAFE/LIMITED/SERIAL classification (Section 29)
- [x] Traceability architecture defined without building the matrix (Section 28)
- [x] Architecture Decision Log complete, every decision sourced to Steps 1–10 (Section 42)
- [x] Architecture-specific risks only, not a restated risk register (Section 43)
- [x] Implementation sequence uses the project's actual roadmap (Section 44)
- [x] No Python source, test, Dockerfile, CI workflow, or config file created
- [ ] QA Lead Review & Approval

## 46. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 12 — Project Setup.
