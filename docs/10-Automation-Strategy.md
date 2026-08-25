# 10 — Automation Strategy

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-AUTOS-001 |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Date | 2026-08-25 |
| Phase | Phase 4 — Automation Planning |
| Step | Step 10 — Automation Strategy |
| Predecessor Documents | [01](01-Project-Vision.md)–[09](09-Automation-Scope.md), all ✅ approved |
| Reference (not template) | TS `AE-AS-001`, `AE-TS-001`, `AE-FA-001`, `AE-TC-001`, `AE-TDD-001`, plus actual TS artifacts (`package.json`, `Dockerfile`, `playwright.config.ts`, `src/config/testConfig.ts`, `.github/workflows/playwright.yml`) |

## 1. Strategy Objective

This document defines **how** the 31 Test Cases approved for automation in [09-Automation-Scope.md](09-Automation-Scope.md) will actually be executed as a Playwright + Python suite — layer assignment, organization, data supply, state control, failure diagnostics, local/CI/Docker execution, cross-browser handling, regression maintenance, flaky-test control, and quality measurement. **The 31-test scope is accepted as-is; this document does not revisit, inflate, or shrink it.** No framework code, dependency, or configuration file is created here.

## 2. Automation Principles

| Principle | Application in this project |
|---|---|
| Risk-based automation | Section 5 of [09](09-Automation-Scope.md) already applied this — this document inherits it, not re-derives it |
| Business-value-driven | Every automated case traces to a `REQ-*` with Critical/High/Medium priority (Section 28) |
| API-first where appropriate | Section 4 below — 13 of 31 cases are API-only, deliberately, not incidentally |
| UI only where UI behavior must be validated | Section 5 — UI automation targets user-facing outcomes, not re-proving what the API layer already proves |
| Hybrid only where combined validation adds value | Section 6 — exactly 1 case, per [09](09-Automation-Scope.md) §10's own justification discipline |
| Avoid redundant UI coverage | [06-Test-Scenarios.md](06-Test-Scenarios.md) §10's duplication-control rule carries forward unchanged |
| Stable locators | Section 12 |
| Deterministic assertions | Section 13 — every automated case's expected result is already VERIFIED or confirmed low-risk-to-verify-on-first-run (per [09](09-Automation-Scope.md) §5's rationale column) |
| Independent tests | Section 8 |
| Data isolation | Section 8/9, built directly on [08-Test-Data.md](08-Test-Data.md) |
| Minimal shared state | Section 9 |
| Maintainability, readability, reusability | Section 24 |
| Fast feedback | Section 18/22 — tiered execution, not one monolithic suite |
| Diagnostic failures | Section 15 |
| No blind retries | Section 16 |
| No false-positive suppression | Section 16/26 — a passing-on-retry test is investigated, not trusted by default |

## 3. Automation Layer Strategy

| Layer | Role | Count (from [09](09-Automation-Scope.md)) |
|---|---|---|
| **Layer 1 — API** | Fast, precise, stateless-first validation of the 14-endpoint surface | 13 |
| **Layer 2 — UI** | User-facing behavior that only exists at the UI (navigation, form interaction, rendered state, client-side messages) | 17 |
| **Layer 3 — Hybrid E2E** | Combined validation only where neither layer alone is sufficient | 1 |

**Why this project should not become a UI-only automation suite:** a UI-only suite would re-implement every API-verifiable fact (product data, brand data, credential checks) through a slower, more brittle, browser-dependent path, and would still not exercise the 4 negative-HTTP-method and 2 missing-parameter API contracts at all, since those have no UI equivalent. The 92.9% API automation ratio ([09](09-Automation-Scope.md) §26) exists because API-layer validation is strictly better for anything that doesn't require rendering.

**Layer selection rule for a given requirement:**
- **API** — the requirement is about backend contract/data correctness and no user-facing rendering is under test (e.g., `REQ-API-001` product list contract).
- **UI** — the requirement is about what a user actually sees or can do, and no API exists to verify it independently (e.g., the checkout-gate modal text, `REQ-UI-003`).
- **Hybrid** — the requirement's real risk lives at the *seam* between the two layers (e.g., `REQ-E2E-003`: does the UI correctly render what the API returns?) — never merely because both layers happen to be involved.

## 4. API Automation Strategy (13 cases)

| Sub-area | Strategy |
|---|---|
| API client strategy | A small set of reusable request-building functions per resource area (products, brands, search, auth, account) — not one client class per endpoint. Concrete module/class shape is a Step 11 decision; this document commits only to "encapsulate endpoint calls, don't repeat request logic in tests" — the same principle TS `AE-FA-001` §9 states, applied without importing its `APIRequestContext`-specific class design. |
| Request construction | Built from [08-Test-Data.md](08-Test-Data.md) `TD-API-*` datasets — no literal payload inline in a test. |
| Response validation | Every API test asserts **both** status code and body/message content — status-only assertions are insufficient (carried from [05](05-Test-Strategy.md) §5). |
| Status-code validation | 200/201 for positive cases, 400/404/405 for the 6 negative cases already VERIFIED in Step 2. |
| Response-body validation | Structural presence (e.g., "is a list," "contains the expected message string") — not brittle full-body equality, since the AUT's full response shape beyond the VERIFIED fields is not independently modeled. |
| Schema validation | Noted as a future enhancement, not Phase-1 scope — matches TS `AE-TS-001` §4 ("Schema validation (future)"), a decision this project independently agrees with rather than inherits blindly. |
| Negative API testing | 6 of the 13 automated API cases are negative (405 ×3, 400 ×2, 404 ×1) — a deliberately high negative ratio, reflecting that the AUT's own API documentation treats negative scenarios as first-class. |
| Authentication-related API testing | `verifyLogin` (valid/invalid/missing-email) — stateless credential checks, no session/token involved (Section 10). |
| API test data | Exactly [08-Test-Data.md](08-Test-Data.md)'s `TD-API-*` family — no new data introduced here. |
| Mutation safety | See table below — 2 of 13 mutate state; both paired with mandatory cleanup. |
| Cleanup | `createAccount` (API-TC-011) is never executed without `deleteAccount` (API-TC-012) in the same run — enforced as a test-design rule now, as a fixture-teardown guarantee at Step 11. |
| API test isolation | Each API test generates or references data independently — no API test depends on another API test's side effect except the deliberate TC-011→TC-012 pairing. |
| API execution frequency | Section 22 — 11 of 13 are PR-eligible; the mutating pair is MAIN/NIGHTLY only, per [09](09-Automation-Scope.md) §6/§19. |
| API parallelization | The 11 stateless cases are SAFE to parallelize; the mutating pair is SERIAL (Section 21). |
| API reporting | Same evidence expectations as UI (Section 15), plus mandatory capture of the full request/response pair on any API failure — not optional. |

**Read-only vs. state-mutating split:**

| Read-only (11) | State-mutating (2) |
|---|---|
| `productsList` (GET+POST/405), `brandsList` (GET+PUT/405), `searchProduct` (valid+missing-param), `verifyLogin` (valid/invalid/missing-email/DELETE-405), `getUserDetailByEmail` | `createAccount`, `deleteAccount` (mandatory pair) |

## 5. UI Automation Strategy (17 cases)

| Module | Cases | Strategy Note |
|---|---|---|
| Home | 1 | Zero-precondition smoke check — element presence only, no interaction chain |
| Login/Signup/Logout | 4 | Form-fill → submit → assert a single deterministic signal; the account-creation case is the one exception requiring the Step 9 authorization gate |
| Products/Details/Search/Category/Brand | 8 | Navigation-driven, read-mostly; assertions target rendered business data (name, price, category path), not DOM structure |
| Cart | 3 | Add/set-quantity/remove — assert line and total values, not incidental styling |
| Checkout gate | 1 | The single VERIFIED, deterministic Checkout-area case — asserted purely on the modal's exact text |
| Recommended Items / cart-after-login | 2 | Extensions of already-verified add-to-cart and login patterns |

**Interaction/assertion principles:** navigate via explicit routes where known (Step 2 verified several — `/products`, `/view_cart`, `/login`, `/contact_us`), assert on rendered business values rather than DOM structure, use Playwright's built-in auto-waiting and locator-level assertions instead of manual polling, treat every form submission as `fill → submit → assert one specific outcome` rather than chaining multiple unrelated checks into one test, and keep each test scoped to one browser context so no test's state leaks into another's (Section 8).

**Explicitly avoided:** arbitrary `sleep()`/fixed waits (Section 14), brittle XPath as a first choice (Section 12), long CSS descendant chains, assertions on implementation details (e.g., internal class names) rather than user-visible outcomes, and UI navigation used only to reach a state that an API call could establish faster (e.g., this project deliberately does *not* plan to drive account creation through 8+ UI form fields when the goal is merely "have a valid account" — that is exactly what Hybrid/API-assisted setup exists for, per Section 3's layer-selection rule, even though only 1 case is currently *scoped* as Hybrid).

## 6. Hybrid E2E Strategy (1 case — AE-E2E-TC-003)

| Aspect | Detail |
|---|---|
| API responsibility | `GET /api/productsList` — retrieve the authoritative product list |
| UI responsibility | Render the Products page and expose the same product names/prices for comparison |
| State transfer | Read-only — the API response becomes the *expected* value set the UI assertion is checked against; no state is created or mutated by either side |
| Why combination provides value | Neither layer alone has an independent oracle: a pure UI test would need hard-coded expected values (brittle against catalog changes); a pure API test never renders anything, so it can't catch a UI-only rendering defect |
| Why pure UI would be less efficient | Hard-coded expected product data goes stale the moment the demo catalog changes — the API call removes that maintenance burden entirely |
| Why pure API would not validate the full requirement | `REQ-E2E-003` is specifically about UI/backend **consistency**, which by definition requires observing both sides in the same test |

No additional Hybrid test is introduced here. `AE-E2E-TC-001`/`002` remain `DEFERRED` exactly as [09-Automation-Scope.md](09-Automation-Scope.md) §5 decided — this document does not revisit that.

## 7. Test Data Strategy (aligned to Step 8 — nothing new introduced)

| Data Class (from [08](08-Test-Data.md)) | Automation Handling |
|---|---|
| Static (e.g., `TD-USER-INVALID-001`, `TD-BRAND-001/002`) | Fixed literal values in a configuration/data module |
| Dynamic/durable (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) | Provisioned once (outside the routine PR-triggered run — Section 9), then reused read-only |
| Generated/runtime (`TD-USER-NEW-*`) | Produced by a data-generation helper at test-run time (Section 30), never reused across runs |
| API-sourced (`TD-PRODUCT-*`) | Fetched live via the Layer-1 API client at test setup, not hard-coded (per [05](05-Test-Strategy.md) §10, restated here as binding for implementation) |
| Environment-specific | None currently exist (only one environment — [04](04-Test-Plan.md) §10); reserved for future use |
| Reusable builders | Recommended specifically for the repeated 16-field account-creation shape ([08](08-Test-Data.md) §22) — a data builder, not a copy-pasted literal, for `TD-USER-NEW-*`/`TD-USER-UPDATE-001` |

No Test Data requirement is added, removed, or altered — every dataset referenced above already exists in [08-Test-Data.md](08-Test-Data.md).

## 8. Test Isolation Strategy

- **Browser context isolation:** each UI test runs in its own Playwright browser context (a Playwright-native capability), so cookies/storage never leak between tests even when run in the same worker process.
- **Fixtures:** provide each test exactly the data/state it declares needing — no test silently depends on another test's setup.
- **Account isolation:** generated accounts (`TD-USER-NEW-*`) are unique per test; the two durable accounts (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) are shared **read-only** across tests (Section 9).
- **Cart isolation:** each cart-touching test establishes its own cart state; no test assumes a cart is empty or populated from a prior test's leftovers.
- **API state:** the mutating pair (`createAccount`/`deleteAccount`) always completes within a single test's boundary — no API state is expected to persist as a precondition for a *different* test.
- **Cleanup:** enforced in the same test (or its fixture teardown, at Step 11), not as a separate "cleanup job."

**Cannot safely run in parallel with each other (from [09](09-Automation-Scope.md) §20):** the account-mutating pair (`AE-UI-TC-004`, `AE-API-TC-011/012`) run SERIAL; any two cases both writing to the *same* durable account's session state (e.g., two concurrent logout attempts) run LIMITED, not fully parallel.

## 9. Shared Environment Strategy

No staging environment exists — every control below is designed against the single live public instance ([02](02-Application-Analysis.md) §14).

| Concern | Control |
|---|---|
| State mutation | Confined to exactly 2 of 31 cases (`AE-UI-TC-004`, `AE-API-TC-011`, paired with `AE-API-TC-012` cleanup) — everything else is read-only |
| Account collisions | Uniquely generated emails for every account-creating case; the two durable accounts are provisioned once, outside routine execution, never re-created per run |
| Cart collisions | Each test establishes and (where verified possible) tears down its own cart state; no cross-test cart sharing |
| Destructive APIs | `deleteAccount` only ever targets the account `createAccount` just made in the same test — never a shared or durable account |
| Contact Us side effects | `AE-UI-TC-009` is `RESTRICTED` — **not automated in this strategy at all** |
| Subscription side effects | `AE-UI-TC-002/003` are `RESTRICTED` — **not automated** |
| Product Review side effects | `AE-UI-TC-022` is `RESTRICTED` — **not automated** (the gap [09](09-Automation-Scope.md) §13 caught and corrected) |
| Checkout uncertainty | `AE-UI-TC-025–029` remain `DEFERRED` — **not automated**; Section 11 below states how this changes in the future |

## 10. Authentication Strategy

- **Valid login:** UI (`AE-UI-TC-005`) and API (`AE-API-TC-007`) both automated, using the durable `TD-USER-VALID-001` account.
- **Invalid login:** UI (`AE-UI-TC-006`) and API (`AE-API-TC-008`) automated with fabricated, non-existent credentials — no account dependency at all.
- **Session state:** Playwright's per-context cookie/storage handling is the mechanism; no custom session-management code is designed here (Step 11 concern).
- **Authenticated browser context:** a login helper (fixture, at Step 11) will exist so authenticated-state tests don't each repeat the login UI flow — but the login flow itself (`AE-UI-TC-005`) must still be independently tested un-shortcut, since it is the thing under test there.
- **Account lifecycle:** creation (`AE-UI-TC-004`, `AE-API-TC-011`) and deletion (`AE-API-TC-012`) are both scoped and automated, but **this strategy does not execute them** — per [09](09-Automation-Scope.md) §12/§30 item 4, the required QA Lead execution authorization has not yet been granted, and this document does not create any account either.
- **API-assisted setup:** recommended (Section 6, Section 30) as the eventual mechanism for provisioning the durable accounts once execution is authorized, rather than a one-time manual signup — a Python-specific opportunity, not implemented here.

**No account is created during this strategy phase**, consistent with instruction.

## 11. Checkout Strategy

**Checkout is not claimed as automated.** Of the 6 Checkout-area cases, only `AE-UI-TC-024` (the authentication gate) is `AUTOMATE`; the other 5 are `DEFERRED`. No payment behavior, address-confirmation UI, order-confirmation message, or invoice-download mechanism is described here as fact — [09-Automation-Scope.md](09-Automation-Scope.md) §12 already drew this line and this document does not soften it.

**How Checkout automation will be added later, if its prerequisites are verified:**
1. A direct, exploratory (non-automated) verification pass resolves the `/checkout` vs. `/view_cart` route question and observes the actual address/payment/confirmation/invoice UI.
2. [07-Test-Cases.md](07-Test-Cases.md)'s existing `AE-UI-TC-025–029` cards are updated with real expected results (not new cases — the design already exists).
3. [09-Automation-Scope.md](09-Automation-Scope.md) is revisited to reclassify some or all of them from `DEFERRED` to `AUTOMATE`, under the same evidence-based process used throughout this project.
4. Only then does this Automation Strategy document (or its successor revision) define their execution layer/frequency/CI tier.

This is a **future re-entry path**, not a commitment made now.

## 12. Locator Strategy

Preference order, most to least preferred:

| Rank | Locator Type | Status for This AUT |
|---|---|---|
| 1 | `data-testid` / dedicated test attributes | **Not verified to exist** — Step 2's direct inspection found no such attributes anywhere on the AUT; this project does not assume them |
| 2 | Accessible roles (`getByRole`) | **Preferred, and already proven workable** — every accessibility-tree read performed throughout Steps 2–9 successfully used role/label-based identification |
| 3 | Labels/placeholders (`getByLabel`) | Used wherever a form field has one (confirmed present on login/signup/search/contact forms) |
| 4 | Stable text (`getByText`) | Used for deterministic, already-VERIFIED messages (e.g., the checkout-gate modal text, the invalid-login error) |
| 5 | Stable attributes | Fallback for non-form elements without a clear role/label |
| 6 | CSS | Used only when 1–5 don't apply, kept as short/shallow as possible |
| 7 | XPath | Last resort only, with a documented reason in the test/code — never a default choice |

**Maintenance principle:** a locator change on the AUT should require changing exactly one place (a Page Object method, at Step 11), never a scattered set of inline locators across multiple test files.

## 13. Assertion Strategy

| Assertion Type | Approach |
|---|---|
| Functional | Assert the business outcome (e.g., "cart total equals sum of line items"), not incidental page state |
| API | Status code **and** message/body content together (Section 4) |
| UI | Rendered, user-visible values — text, presence/absence of an element, navigational outcome |
| Business-rule | E.g., `REQ-BUS-004`/`BR-003` (checkout requires auth) asserted via the exact gate modal, not an inferred side effect |
| Negative | Assert the specific rejection signal (error text, status code) — not merely "the happy path didn't happen" |
| Boundary | Not currently applicable to any `AUTOMATE` case — the one boundary case identified (`AE-UI-TC-017`, quantity) is `DEFERRED` precisely because no boundary value is confirmed |
| State | Assert cart/account state via the same mechanism a real user would observe it (rendered cart page, `getUserDetailByEmail` response) — not by inspecting internal implementation |

**Over- vs. under-assertion:** each test asserts the one or two outcomes its Test Case description names (Section 8 of [07](07-Test-Cases.md)) — not every incidental detail on the page (over-assertion inflates maintenance cost for no risk reduction), and not merely "no error was thrown" (under-assertion misses the actual behavior under test).

## 14. Waiting / Synchronization Strategy

Playwright's auto-waiting (actionability checks before every interaction) and locator-level assertions (`expect(locator).toHaveText(...)`, which retry internally) are the default and expected mechanism for every case in scope. Explicit waits are justified only where a specific, understood asynchronous behavior exists — the one confirmed example in this project's evidence is the AJAX-driven cart-removal update (`AE-UI-TC-018`, REQ-UI-005), which must wait on the DOM update itself, not a navigation event. **No arbitrary `sleep()`/fixed-duration wait is planned for any of the 31 cases** — if one is ever found necessary during implementation, it must be documented with the specific reason, per instruction, not silently added.

## 15. Failure Diagnostics

| Artifact | When Collected |
|---|---|
| Screenshot | Every UI test failure (cheap, always valuable) |
| Trace | On retry only (not every run) — expensive enough to reserve for the case that already failed once |
| Video | Not enabled by default — reserved for a specific investigation, not blanket collection, since it is the most expensive artifact for the least incremental diagnostic value over trace+screenshot |
| Console information | Captured for UI failures where available |
| Network information | Captured for UI failures involving the one known AJAX interaction (cart removal) and for any Hybrid failure |
| API request/response evidence | **Mandatory**, not optional, for every API/Hybrid failure (Section 4) |
| Logs | Captured for every failure, any layer |

Not every expensive artifact is enabled blindly — video is explicitly the one deliberately withheld by default, matching the cost/value judgment already reasoned in [05-Test-Strategy.md](05-Test-Strategy.md) §17.

## 16. Retry Strategy

| Environment | Policy |
|---|---|
| Local | Minimal/no retries — a failing test should fail immediately during development, not mask itself |
| CI | Limited, bounded retries — justified only as symptom management for genuinely transient infrastructure issues (per [05](05-Test-Strategy.md) §16), never as a substitute for fixing a real problem |

**Flaky-test classification (unchanged from [05-Test-Strategy.md](05-Test-Strategy.md) §16):** transient infrastructure failure / real product defect / automation defect — a test that only passes on retry is investigated and classified into one of these three before being trusted again, not silently accepted as "passing." **Quarantine:** a confirmed-flaky test is removed from the trusted/gating suite and tracked separately until root-caused, exactly as already defined in Step 5 — this document does not redefine that policy, only reaffirms it applies to the concrete 31-case scope now on the table.

## 17. Browser Strategy

| Tier | Browser(s) | Role |
|---|---|---|
| Local development | Chromium (primary), others on demand | Fastest inner-loop feedback |
| CI — PR gate | Chromium only | Matches [09](09-Automation-Scope.md) §18/19's PR-eligible tier |
| CI — main/nightly regression | Chromium (full regression); Firefox/WebKit reserved for the scheduled/release tier, not every main-branch push | Consistent with [05](05-Test-Strategy.md) §7/§9's already-approved graduated model |
| Release validation | Chromium + Firefox + WebKit, curated subset (the business-critical cases named in [06](06-Test-Scenarios.md) §9: invalid login, cart add/remove, checkout gate) | Full cross-browser commitment reserved for the highest-confidence gate |

**No claim is made that all browsers run on every PR** — that would contradict both the approved Test Strategy and the direct evidence that even the TS project's own CI never ran Firefox/WebKit despite having them configured ([05](05-Test-Strategy.md) §7 finding).

## 18. Execution Strategy

| Mode | Composition | Tags (illustrative, not implemented) |
|---|---|---|
| Smoke | `AE-UI-TC-001/006/011/024`; `AE-API-TC-001/003/007/008` | `smoke` |
| API | All 13 automated API cases | `api` |
| UI | All 17 automated UI cases (excluding the mutating pair when run in the PR tier) | `ui` |
| Hybrid | `AE-E2E-TC-003` | `e2e`, `hybrid` |
| Regression | Smoke + UI + API, Chromium | `regression` |
| Cross-browser | The curated Section 17 subset | `cross-browser` |
| Release | Full regression + cross-browser + the CI-RESTRICTED mutating pair | `release`, `critical` |

Tags exist only where they provide genuine execution-selection value (each row above corresponds to a real, distinct CI trigger in Section 19) — no tag is proposed merely for taxonomy's sake.

## 19. CI/CD Strategy (design only — no workflow created)

| Stage | Content |
|---|---|
| Dependency installation | Python package installation from a project manifest (exact tool — pip/poetry/uv — is a Step 11 decision) |
| Browser installation | Playwright's own browser-install step, scoped to Chromium for PR/main tiers and all three engines for the release tier |
| Test execution | Tiered per Section 18 — smoke+critical on PR, full Chromium regression on main, scheduled full+cross-browser nightly, everything (incl. the CI-RESTRICTED pair) on release |
| Parallelization | Section 21 |
| Retries | Section 16 — CI-only, bounded |
| Reporting | Section 25 |
| Artifact collection | Screenshots always, traces on retry, HTML report every run — uploaded as CI artifacts with a bounded retention window (exact days a Step 11/14 decision) |
| Failure handling | A failure in the CI-SAFE tier gates the pipeline; a failure in the CI-RESTRICTED tier is visible but handled with the same non-blocking-where-appropriate judgment TS's own workflow demonstrated for its one known AUT limitation ([05](05-Test-Strategy.md) §13) — applied here only if a comparably well-understood, confirmed-non-fixable case is ever identified, not as a general escape hatch |

No GitHub Actions (or other) workflow file exists yet.

## 20. Docker Strategy (design only — no Dockerfile created)

Docker is an **approved project requirement** ([01](01-Project-Vision.md), [04](04-Test-Plan.md) §23, [05](05-Test-Strategy.md) §12). Its role here:

- **Reproducible execution:** one image definition, so "it fails in CI" is never explainable by "different Python/browser version than local."
- **Environment consistency:** OS-level dependencies, Python version, and Playwright browser binaries pinned together.
- **Onboarding:** a portfolio reviewer or new contributor runs the suite with one command.
- **CI consistency:** the same image (or equivalent) used locally and in CI, so a CI-only failure is genuinely suspicious rather than expected.
- **Browser/runtime consistency:** matches Section 17's browser tiers — the image must support Chromium at minimum, all three engines for the release tier.

**Local Docker execution:** intended default path for anyone running the full suite outside active development (mirrors the TS project's proven `docker run` pattern — REFERENCE (TS artifact), not copied).
**CI Docker execution:** the CI pipeline's execution environment should be the same image family used locally, once implemented.
**Browser dependency strategy:** prefer an official Playwright-maintained base image (the TS project's own `mcr.microsoft.com/playwright:v1.61.1-noble` choice is cited as **proven precedent for this exact application**, not adopted verbatim — a Python-compatible equivalent is a Step 11 decision).
**Environment variable strategy:** base URL and any future configuration externalized via environment variables, never hard-coded into the image or the test code (per [04](04-Test-Plan.md) §10, [08](08-Test-Data.md) §23).

**Explicitly not copied:** the TS project's specific `Dockerfile` syntax, its exact base-image tag, and its `npm ci`-based dependency layer — these are TypeScript/Node-specific and have no direct Python translation worth preserving as-is.

## 21. Parallelization Strategy

| Category | Classification | Basis |
|---|---|---|
| All 11 read-only API cases, all UI cases except the 4 with a durable-account or mutation dependency | **SAFE** | No shared mutable state |
| `AE-UI-TC-005/007/008/021`, `AE-API-TC-007/014` | **LIMITED** | Share a durable account — safe alongside unrelated tests, not alongside each other if any mutates session state |
| `AE-UI-TC-004`, `AE-API-TC-011/012` | **SERIAL** | Unique-data generation/destruction pair — conservative serialization, matching the TS project's own proven choice to run `workers: 1` in CI despite local parallel capability ([05](05-Test-Strategy.md) §14 finding) |

**CI worker strategy:** favors reliability over raw speed for anything touching shared state — the same explicit trade-off already decided in [05-Test-Strategy.md](05-Test-Strategy.md) §14, applied here to the concrete 31-case set rather than restated abstractly. **Data collision prevention:** uniquely-generated identifiers (Section 7/9) are the primary mechanism; SERIAL execution for the mutating pair is the backstop, not the primary control.

## 22. Regression Strategy

| Tier | Composition | Frequency |
|---|---|---|
| PR regression | Smoke + all CI-SAFE cases (28 of 31), Chromium | Every Pull Request |
| Main branch regression | Same as PR, Chromium | Every push to main |
| Nightly regression | Full 31-case set including the CI-RESTRICTED mutating pair, Chromium; environment-instability canary value independent of code changes | Daily |
| Release regression | Full 31-case set + curated cross-browser subset (Section 17) | Per release cycle |

This mirrors — without copying the implementation of — the TS project's own proven graduated cadence ([05](05-Test-Strategy.md) §7).

## 23. Smoke Strategy

A small, fast layer confirming the application and framework are both fundamentally working: `AE-UI-TC-001` (Home availability), `AE-UI-TC-006` (critical negative-auth UI health), `AE-UI-TC-011` (critical catalog UI health), `AE-UI-TC-024` (critical Checkout-gate UI health), and `AE-API-TC-001/003/007/008` (critical API availability, including one authenticated-adjacent check). **8 of 31 cases** — deliberately far short of the full regression suite, answering only "is anything fundamentally broken?" in the shortest possible time.

## 24. Maintainability Strategy

Principles only — **no folder structure or code architecture is designed here** (Step 11 owns that):

- **Page Object principles:** one class per screen/business area, encapsulating locators and interactions, kept free of test-assertion logic except where an assertion is genuinely page-specific and reusable (REFERENCE KNOWLEDGE — principle only, from TS `AE-FA-001` §6, not its class names).
- **Reusable API clients:** one module/class per resource area (products, brands, search, auth, account) — same principle-only reuse from TS `AE-FA-001` §9.
- **Fixtures:** provide ready-to-use page objects/API clients and guarantee teardown (especially account cleanup) — Pytest-idiomatic fixture scoping, not a port of TS's fixture files.
- **Test data builders:** for the repeated account-creation shape (Section 7).
- **Utilities:** shared helpers (e.g., timestamp/unique-ID generation) kept small and single-purpose.
- **Configuration separation:** base URL, timeouts, and environment flags centralized, never scattered across test files.
- **Naming standards:** test/method/fixture names should make the requirement and module traceable at a glance (Section 28).
- **Minimal duplication:** a behavior proven at Layer 1 is not re-proven identically at Layer 2 (Section 3).

## 25. Reporting Strategy

**Requirements only — no tool installed/configured here:**

- Execution summary: pass/fail/skip counts by layer and module.
- Duration: per test and per suite, to monitor whether the PR-gate tier stays fast as the suite grows.
- Failure evidence: per Section 15.
- Browser: which engine each result ran under.
- Environment: which CI tier/trigger produced the result.
- Test category: layer (UI/API/Hybrid) and tag (Section 18).
- Traceability: requirement/scenario/case ID visible in the report, not just a bare test name.

**Candidate tools (not installed):** Playwright's native HTML report is the proven, zero-additional-dependency baseline (REFERENCE (TS artifact) — TS's own `reporter: 'html'` choice, cited as evidence this is sufficient for this application's scale). Allure is noted as a possible future enhancement **only if** richer cross-run trend reporting becomes genuinely needed — exactly the same "optional future enhancement" status TS `AE-FA-001` §12 itself assigned it, not a status this project invented independently.

## 26. Observability Strategy

| Failure Category | Distinguishing Signal | Root-Cause Path |
|---|---|---|
| Test failure (assertion didn't hold) | Specific, named assertion mismatch in the report | Compare against the VERIFIED expected value; if it still doesn't match, escalate to Application failure |
| Application failure | AUT behavior differs from a `REQ-*`-documented, VERIFIED fact | Documented as an observation (Section 27 of [10]... no fix channel exists — [04](04-Test-Plan.md) §16) |
| Environment failure | Network/availability issue unrelated to code or assertions | Re-run once (Section 16); track frequency, don't file as a defect |
| Automation failure | Locator/synchronization/logic error in our own test code | Fixed directly — the one category this project fully owns and controls |
| Data failure | Collision, stale reference, or failed cleanup (Section 9) | Traced to the specific `TD-*` dataset; distinct from an application defect |

This five-way split directly extends [05-Test-Strategy.md](05-Test-Strategy.md) §18's four-way classification with the "Data failure" category [08-Test-Data.md](08-Test-Data.md) surfaced as a distinct, real risk (cart/subscription cleanup gaps) — an evidence-based refinement, not an arbitrary addition.

## 27. Security / Performance / Accessibility Boundary

Unchanged from [04-Test-Plan.md](04-Test-Plan.md) §4/§7 and [01-Project-Vision.md](01-Project-Vision.md) §10: **not committed scope.** No automation strategy element in this document touches performance, security, or accessibility testing. They remain Future Scope only, mentioned here solely to confirm this document does not silently expand into them.

## 28. Traceability Strategy

Full chain: `Requirement → Scenario → Test Case → Test Data → Automation Scope → Automation Implementation → Execution → Defect → Release Evidence`. The first five links already exist and are stable ([03](03-Requirement-Analysis.md)→[06](06-Test-Scenarios.md)→[07](07-Test-Cases.md)→[08](08-Test-Data.md)→[09](09-Automation-Scope.md)). **This document adds the discipline for the remaining links:** every automated test's name/tag (Step 11 implementation) must encode its Test Case ID (e.g., a test named or tagged with `AE-API-TC-007`), so execution results (Phase 12) and any resulting defect (Phase 13) can be traced back through the entire chain to `REQ-API-007` without manual cross-referencing — extending, not duplicating, the traceability approach already committed to in [05-Test-Strategy.md](05-Test-Strategy.md) §19.

## 29. TypeScript → Python Learning

**What we intentionally carry forward** (supported by TS's actual artifacts/docs, not assumption):

- **Graduated CI cadence** (PR fast-gate → main broader → nightly canary → release full) — proven in TS's real `.github/workflows/playwright.yml`.
- **Conservative CI parallelism** — TS's own `workers: 1` in CI despite `fullyParallel: true` locally (`playwright.config.ts`), directly informing Section 21.
- **CI-only, bounded retries** (`retries: { ci: 2, local: 0 }` in TS `testConfig.ts`) — directly informing Section 16.
- **Screenshot-on-failure, trace-on-retry, video-on-failure-only** evidence tiering (TS `playwright.config.ts`) — informing Section 15, adopted as a cost/value pattern, not literal config.
- **Page Object Model + fixture-provided page objects/API clients** as an architectural principle (TS `AE-FA-001` §6/§7) — the *pattern*, not the TypeScript class hierarchy.
- **Playwright HTML report as the sufficient default**, with Allure explicitly deferred as optional (TS `AE-FA-001` §12) — this project reaches the same conclusion independently, corroborated by TS's own stated reasoning.
- **Official Playwright-maintained Docker base image** as a low-risk starting point (TS `Dockerfile`) — precedent, not the literal file.

**What we intentionally improve** (each grounded in a specific gap this project independently found, not asserted for its own sake):

- **Side-effect awareness for Contact Us/Subscription/Review.** TS's own CI ran its Contact Us test in full regression with only a narrow, unrelated "known limitation" carve-out (a client-side readiness race) — it did **not** flag or restrict the test for the real-message-sent side effect at all. This project's [09-Automation-Scope.md](09-Automation-Scope.md) independently identified that side effect (and extended the same reasoning to Product Review, which TS automated without comment) and restricted all three accordingly — a genuine, evidence-based improvement in shared-environment discipline, not a stylistic preference.
- **Checkout verification-before-automation discipline.** TS's baseline automated all 5 Checkout E2E scenarios directly from its own documentation, apparently without the same level of independent live-behavior verification this project performed in Step 2 (which found the underlying route/flow genuinely unconfirmed). This project defers those cases until directly verified, rather than automating against assumed behavior.
- **API-surface breadth.** TS's Phase-1-automated API scope stopped at 8 endpoints; this project independently verified and automates 13 of the same 14 documented endpoints, promoting the previously-deferred negative and account-lifecycle cases on the strength of its own direct evidence.
- **Faster, browser-independent API testing (potential).** Python's `requests`/`httpx` option (Section 30) could let the API suite run without any browser context at all — something TS's `APIRequestContext`-based approach, tied to the Playwright Node runtime, does not offer as cleanly. This is a **potential** improvement, evaluated properly at Step 11, not yet proven.

## 30. Python-Specific Engineering Direction (design only)

- **Pytest integration:** fixtures for page objects, API clients, and authenticated/durable-account state, following Pytest's native fixture-scoping model rather than porting a TypeScript fixture pattern.
- **Parametrization:** the repeated unsupported-HTTP-method and category/brand-browsing cases (Section 3's "avoid redundant coverage" principle, applied structurally) are natural candidates for `pytest.mark.parametrize` — one test function, multiple data rows, rather than near-duplicate functions.
- **Python data generation:** a small, dependency-free generator (or `Faker`, if justified by future scale — [08](08-Test-Data.md) §22 already reasoned this isn't justified yet) for unique account emails.
- **API/UI integration:** a shared data-provisioning helper usable by both the one active Hybrid case and any future ones once Checkout/Login unblock further Hybrid work.
- **Reusable helper functions:** small, single-purpose (Section 24) — not large "utils" catch-alls.
- **Typed models where valuable:** e.g., a typed representation of the 16-field account payload, reducing the chance of a silent field-name typo across the 5+ cases that reuse that shape — genuinely valuable given Python's optional static typing, and not something the TS project's own `user.types.ts` did any differently in principle (REFERENCE KNOWLEDGE: the *pattern* of typed request/response models is carried forward, not the TypeScript interfaces themselves).
- **Environment management:** `.env`/environment-variable based configuration (Section 20), consistent with the TS project's own `.env.example` precedent (artifact-level observation) without copying its contents.

None of the above is implemented in this document.

## 31. Quality Gates

| Gate | Requirement |
|---|---|
| Determinism | A test must produce the same result on repeated runs against unchanged application/code — a test that doesn't is quarantined (Section 16), not merged |
| Meaningful assertion | Every test asserts a specific, named business outcome (Section 13) — no "test passed because nothing threw an exception" |
| No unexplained hard waits | Any deviation from auto-waiting must be documented with its reason (Section 14) |
| No sensitive data committed | Enforced per [08-Test-Data.md](08-Test-Data.md) §23 — dummy-only payment/credential data, environment variables for anything real |
| No uncontrolled destructive action | Every mutating test is paired with verified cleanup (Sections 4, 8, 9) |
| Traceability required | Every automated test cites its Test Case ID (Section 28) |
| Review required | No automated test merges without review (Section 32) |
| CI suitability assessed | Every test carries the CI tier already assigned in [09-Automation-Scope.md](09-Automation-Scope.md) §6/§18 |
| Failure diagnostics available | Section 15's evidence set is present for every test, not added later |

## 32. Automation Governance

- **Code review:** every automated test change requires review before merge (standard practice, not unique to this project — stated for completeness).
- **Test review:** a new automated test must be checked against Section 31's quality gates before being accepted into the regression suite.
- **Naming conventions:** test names/tags encode the Test Case ID and module (Section 28).
- **Ownership:** the QA Lead retains final authority over automation scope and quality decisions ([01](01-Project-Vision.md) §19); the AI Assistant's role remains advisory/execution-support.
- **Change control:** any change to the 31-case scope after this step requires an explicit, documented QA Lead-approved update to [09-Automation-Scope.md](09-Automation-Scope.md) — this strategy document does not silently expand or shrink it.
- **Flaky test handling:** per Section 16 — quarantine, root-cause, then re-entry; never silent retry-to-green.
- **Scope changes:** any reclassification (e.g., a `DEFERRED` Checkout case becoming `AUTOMATE` once verified, per Section 11) is itself a scope change requiring the same QA Lead review.
- **Deferred-test review:** the 9 `DEFERRED` cases should be periodically revisited (Section 35 risk) rather than left indefinitely — a governance responsibility, not a one-time note.

## 33. Strategy Success Criteria

Measurable, and explicitly not padded to look impressive:

- The approved 31-test scope is implemented as designed (Sections 4–6), with no case silently dropped or added beyond [09-Automation-Scope.md](09-Automation-Scope.md)'s classification.
- Critical-path (P0) automation reaches the 76.9% already established as the ceiling by current evidence ([09](09-Automation-Scope.md) §26) — not 100%, since 3 P0 cases are genuinely blocked.
- API coverage reaches 92.9% (13/14) as already established.
- UI coverage reaches 58.6% (17/29) as already established.
- Every automated test is deterministic across at least 2 consecutive local runs before being considered CI-ready (Section 31).
- PR-gate execution time stays materially faster than full regression (a qualitative target — no specific number is invented, since no implementation exists yet to measure against).
- CI reliability: the PR-gate tier's pass rate reflects real code/application state, not environment noise — measured via the flaky-test quarantine rate (Section 16) trending toward zero over time, not an absolute number set now.
- Docker reproducibility: local and CI execution produce the same result for the same commit — a binary, verifiable property once Step 11/14 implement it.
- Diagnostics are sufficient to resolve a failure without re-running blind (Section 15) — verified qualitatively during framework hardening (Phase 11), not numerically here.
- Architecture remains maintainable per Section 24's principles — assessed via code review (Section 32), not a numeric metric.

## 34. Decision Log

| # | Decision | Reason | Evidence | Impact | Revisit Condition |
|---|---|---|---|---|---|
| 1 | 31-test automation scope accepted unchanged | Explicit instruction; scope decisions belong to Step 9, not this step | [09](09-Automation-Scope.md) | This document designs *how*, not *what* | Only via a formal [09] revision |
| 2 | API-first strategy | 92.9% of API surface independently verified, mostly stateless — highest-value, lowest-cost layer | [09](09-Automation-Scope.md) §26 | 13 of 31 cases are API-only | N/A |
| 3 | UI reserved for user-facing-only validation | Avoids redundant coverage (Section 3) | [06](06-Test-Scenarios.md) §10 | 17 UI cases target rendering/interaction specifically | N/A |
| 4 | Hybrid limited to 1 case | Only 1 of 3 designed Hybrid cases has no identity/checkout dependency | [09](09-Automation-Scope.md) §10 | Hybrid coverage stays at 33% deliberately | Revisit once Login/Checkout resolve |
| 5 | Shared-environment protection (unique data, paired cleanup, SERIAL mutation) | Single public instance, no staging | [02](02-Application-Analysis.md) §14 | Slower mutation-path execution, safer overall | N/A |
| 6 | Checkout automation excluded pending verification | Route/flow genuinely unconfirmed | [03](03-Requirement-Analysis.md) §5 row 1/4 | Largest coverage gap in this strategy | Direct exploratory verification (Section 11) |
| 7 | Contact/Subscription excluded from automation entirely | No verified cleanup; real, permanent side effects | [08](08-Test-Data.md) §24/30 | 3 fewer automated cases than TS baseline | If a moderation/removal path is ever confirmed |
| 8 | Product Review excluded from automation entirely | Same side-effect risk, newly identified in [09] | [09](09-Automation-Scope.md) §13 | 1 fewer automated case than TS baseline | Same condition as #7 |
| 9 | Conservative (SERIAL for mutation, LIMITED for durable-account) parallelization | Matches TS's own proven CI choice; shared environment | TS `playwright.config.ts`/`testConfig.ts` (artifact) | Slightly slower CI for the affected subset | N/A — this is a durable strategic stance, not provisional |
| 10 | Docker as an approved capability, design-only at this step | Explicit project requirement; implementation belongs to Step 11+ | [01](01-Project-Vision.md), [04](04-Test-Plan.md) §23 | No Dockerfile exists yet | Step 11 |
| 11 | Cross-browser limited to a curated subset, release/scheduled tier only | Matches already-approved [05] §9/§13; TS's own CI never actually ran non-Chromium | TS `.github/workflows/playwright.yml` (artifact) | Firefox/WebKit are not a PR-blocking commitment | N/A |

## 35. Risks (automation-strategy-specific only)

- **Shared public environment:** every mutating case (2 of 31) carries residual collision/side-effect risk despite unique-data and cleanup controls.
- **State mutation compounding:** if the `createAccount`/`deleteAccount` cleanup pairing ever silently fails, orphaned accounts accumulate on a system this project does not own.
- **Checkout uncertainty persisting:** if the exploratory verification in Section 11 is never actually performed, 5 designed cases remain permanently unautomated, quietly capping P0 coverage at 76.9% indefinitely.
- **Test data collisions:** the two durable, shared accounts (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) are a single point of contention if two LIMITED-parallelization tests run concurrently by mistake.
- **Cross-browser instability:** Firefox/WebKit have never actually been exercised against this AUT by either project — the first real cross-browser run could surface genuinely new findings, not just confirm Chromium results.
- **CI runtime growth:** as cases move from Wave 1 through Wave 5 ([09](09-Automation-Scope.md) §27), PR-gate execution time must be actively watched, not assumed to stay fast.
- **Flaky tests masking real issues:** the bounded CI retry policy (Section 16) is a known, accepted risk surface — it must never be allowed to silently grow more permissive over time.
- **Browser dependency drift:** local/CI/Docker environments could diverge if Docker implementation (Step 11+) doesn't keep browser binary versions pinned consistently.
- **Docker compatibility:** an official Playwright-maintained Python-compatible image must actually exist and behave as expected — not yet confirmed, only planned (Section 20).
- **Maintenance cost concentration:** the account-mutation-adjacent cases (`AE-UI-TC-004`, `AE-API-TC-011/012`) carry the highest maintenance risk of the 31 ([09](09-Automation-Scope.md) §21) and deserve disproportionate review attention once implemented.

## 36. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 10 Exit Criteria

- [x] Steps 1–9 reviewed
- [x] Approved 31-test scope respected, unchanged (Section 1, Decision #1)
- [x] No scope expansion introduced anywhere in this document
- [x] UI/API/Hybrid strategy defined (Sections 4–6)
- [x] Test data strategy aligned with, not divergent from, Step 8 (Section 7)
- [x] Shared-environment risks addressed (Section 9)
- [x] Checkout uncertainty preserved (Section 11)
- [x] Contact/Subscription side effects preserved (Section 9, Decision #7)
- [x] Product Review side effect preserved (Section 9, Decision #8)
- [x] Docker strategy included, design-only (Section 20)
- [x] CI strategy included, design-only (Section 19)
- [x] Cross-browser strategy included (Section 17)
- [x] Parallelization strategy included (Section 21)
- [x] Failure diagnostics defined (Section 15)
- [x] Retry strategy defined (Section 16)
- [x] Reporting strategy defined (Section 25)
- [x] Traceability defined (Section 28)
- [x] TypeScript lessons supported by cited evidence, not assumption (Section 29)
- [x] Python-specific direction defined without implementation (Section 30)
- [x] No code, framework files, dependencies, Docker files, or CI workflows created
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 11 — Framework Architecture.
