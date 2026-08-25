# 05 — Test Strategy

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-TS-001 |
| Document Title | Test Strategy |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 2 — Test Planning |
| Step | Step 5 — Test Strategy |
| Predecessor Documents | [01-Project-Vision.md](01-Project-Vision.md) ✅, [02-Application-Analysis.md](02-Application-Analysis.md) ✅, [03-Requirement-Analysis.md](03-Requirement-Analysis.md) ✅, [04-Test-Plan.md](04-Test-Plan.md) ✅ |
| Reference Baseline | `playwright-typescript-hybrid-framework/docs/AE-TS-001_Test_Strategy.docx` (Priority 2 — adapted, not copied), plus its actual `playwright.config.ts`, `src/config/testConfig.ts`, and `.github/workflows/playwright.yml` (inspected directly as evidence, per instruction) |

**Evidence labeling:** **VERIFIED OBSERVATION**, **REFERENCE KNOWLEDGE (TS baseline)**, **REFERENCE (TS artifact)** — evidence from directly inspecting the TS project's actual config/CI files rather than its narrative docs, **INFERENCE**. This document does not restate the Test Plan's *what*; it answers *how*.

## 0. Relationship to the Test Plan

[04-Test-Plan.md](04-Test-Plan.md) defines scope, objectives, environment, and criteria. This Test Strategy defines the operating model: how risk drives priority, how the four testing layers interact, when each regression tier runs, how flakiness is told apart from real defects, and how CI/Docker/parallelism are used without endangering the single shared public environment identified throughout Steps 2–4. Where a Test Plan section is only referenced (not repeated), it is cited by section number rather than restated.

## 1. Testing Strategy Model

This project uses a **requirement-based, risk-weighted, layered testing model**:

- **Requirement-based:** every planned test traces to a `REQ-*` item in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) — no test is designed "because the TS baseline had one" without a live requirement behind it.
- **Risk-weighted prioritization:** test depth and execution frequency scale with the risk register in Section 6, not uniformly across modules.
- **Layered (Section 7):** API validation, UI functional validation, critical E2E journeys, and cross-browser regression are treated as four distinct layers with different costs and different jobs, not one undifferentiated "automation suite."
- **UI/API/Hybrid separation:** each layer is validated independently first; Hybrid is added only where it earns its place (Section 10), avoiding the anti-pattern of treating "uses both UI and API" as a virtue in itself.
- **Early API validation:** because all 14 API endpoints are already independently VERIFIED at the documentation level ([02-Application-Analysis.md](02-Application-Analysis.md) Section 10) and require no account/session state for 10 of the 14, API validation is the cheapest, fastest layer to stand up and is prioritized early — well before UI automation needs to exist to get first signal.
- **E2E for critical journeys only:** full end-to-end (search → cart → checkout → order) is reserved for the handful of journeys where business risk justifies its cost, not applied broadly.
- **Regression-focused automation:** the discovery/cart modules already well-verified in Step 2 are the natural first regression backbone; Signup/Login/Checkout — the largely-unverified 16 of 48 requirements flagged in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14 — are targeted for *verification* before they can be trusted as *regression*.
- **Cross-browser validation:** applied selectively (Section 13), not to every test.
- **Failure diagnostics and continuous CI/CD feedback:** every layer is designed to fail loudly and specifically (Section 21), and to run automatically on the cadence defined in Section 17.

**Why this model fits Automation Exercise specifically:** the application is a single, publicly shared, stateful demo instance with no staging environment, no database access, and 16 of 48 known requirements still unverified. A model that treated "more automation everywhere" as the goal would multiply exposure to shared-state risk before verification risk is even resolved. A risk-weighted, layered model instead spends effort where the requirement evidence is weakest (Signup/Login/Checkout) and where the cost of validation is lowest (stateless API reads), which is a materially different allocation than simply re-implementing the TS baseline's 32 tests in Python.

## 2. Risk-Based Testing Strategy

Reusing the risk register already established in [02-Application-Analysis.md](02-Application-Analysis.md) Section 13, [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11, and [04-Test-Plan.md](04-Test-Plan.md) Section 17 — no new register is invented.

| Risk | Effect on Test Priority | Effect on Test Depth | Effect on Automation Priority | Effect on Regression Frequency | Effect on Failure Investigation | Effect on Release Confidence |
|---|---|---|---|---|---|---|
| Single shared public environment, no staging | Elevate any test that mutates state to higher scrutiny before automating | Prefer read-only/idempotent checks where the requirement allows | Automate read-only flows (product listing, search, brand/category) first | Safe to run frequently | Environment-caused failures must be distinguished from real defects (Section 22) | Cannot claim environment stability; must be stated as a residual risk (Section 27) |
| Account/API state mutation (`createAccount`/`deleteAccount`/`updateAccount`) | High priority to verify *behavior*, low priority to run *frequently* | Each mutating test must include verified cleanup before being trusted for regression | Automate only with a proven cleanup step; do not automate cleanup-less variants | Lower frequency than read-only suites (e.g., not on every PR) | A failed cleanup step is itself a defect class, not noise | Unresolved cleanup gaps reduce confidence disproportionately, since they compound on a shared system |
| Signup/Login verification gap (6 of 6 `REQ-FUNC-SL-*` largely unverified) | **Highest priority in the current backlog** — this blocks trusting any downstream Checkout work | Full functional verification before automation, not automation-first | Do not automate Checkout journeys ahead of verifying Login, since Checkout depends on it | N/A until first verified | Any Login failure must be triaged before touching Checkout | This gap is explicitly named as unresolved — see Section 27 |
| Checkout/payment verification gap (`REQ-FUNC-CO-002–006` reference-only) | High priority, but *sequenced after* Login verification | Depth limited to what can be confirmed without real payment processing | Not a Phase-1 automation-first candidate until verified | N/A until first verified | Payment-adjacent failures require extra care to distinguish "simulated flow behaves unexpectedly" from "framework issue" | Explicitly flagged as unresolved; no release claim can rely on this area yet |
| API state mutation risk (subset of endpoints) | Read endpoints (`productsList`, `brandsList`) get priority over write endpoints for early confidence-building | N/A | Automate read endpoints first (Section 9) | Read endpoints safe for every run; write endpoints throttled | Distinguish a write endpoint's genuine 4xx/5xx from test-data collision | Read-endpoint stability contributes real confidence; write-endpoint stability contributes less until cleanup is proven |
| Environment instability (public demo site) | N/A — applies uniformly | N/A | N/A | Scheduled canary-style runs (Section 17) surface instability independent of code changes, following the TS baseline's proven daily-schedule pattern — **REFERENCE (TS artifact)**, `.github/workflows/playwright.yml` `schedule: cron '0 3 * * *'` | Environment-flagged failures are triaged separately from code-caused failures (Section 20/22) | Environment instability is a residual risk, not something this project can eliminate |
| Cross-browser differences | Applied selectively to business-critical flows, not uniformly (Section 13) | Deeper only where a flow is customer-facing and business-critical | Chromium-first automation, other engines added deliberately | Full cross-browser regression reserved for release-validation cadence, not every PR (Section 11) | Browser-specific failures tracked separately from browser-agnostic ones | Cross-browser pass rate is one input among several, not a gate on its own |
| Automation flakiness (e.g., AJAX cart-removal behavior, Step 2) | N/A | Tests touching known-async interactions get explicit wait strategy, not blind retries | N/A | Flaky tests are quarantined, not silently retried into "passing" (Section 20) | Root-cause required before re-entry to the trusted suite | A suite with unresolved flakiness cannot support a release-confidence claim |

## 3. Testing Layers

No internal application unit/component code exists for us to test (confirmed in [04-Test-Plan.md](04-Test-Plan.md) Section 6) — every layer below tests the deployed, public-facing application through its UI or API surface only.

| Layer | Scope | Role |
|---|---|---|
| **Layer 1 — API / service-level validation** | All 14 documented `/api/*` endpoints (REQ-API-001–014) | Fastest, cheapest, most stateless layer. Establishes a fast-feedback baseline before UI work begins, and independently validates data (e.g., product/brand lists) that Layer 2 also renders — giving Layer 2 an oracle to cross-check against. |
| **Layer 2 — UI functional / page-level validation** | Individual page/module behavior — Home, Products, Product Details, Cart, Contact Us, Signup/Login forms (REQ-FUNC-*, REQ-UI-*) | Validates that a single page or interaction behaves as documented, independent of any larger journey. This is where the currently-unverified Signup/Login gap gets closed first, in isolation, before it's trusted as a dependency for Layer 3. |
| **Layer 3 — Critical end-to-end business journeys** | Multi-step flows spanning modules — e.g., search → add to cart → checkout gate → (once verified) authenticated checkout → order (REQ-BUS-*, REQ-E2E-*) | Reserved for the handful of journeys with real business weight. More expensive to write and maintain than Layer 2, so scope here is deliberately narrow, not exhaustive. |
| **Layer 4 — Cross-browser regression** | A curated subset of Layer 2/3 tests re-run across Chromium/Firefox/WebKit | Confidence that customer-facing behavior doesn't silently vary by engine. Applied to the highest-business-value subset only (Section 13), not the full suite, to control cost. |

This is a **pyramid in cost, not necessarily in count**: Layer 1 (API) is expected to have the largest test count relative to its cost; Layer 3/4 are expected to have the smallest counts relative to their cost, consistent with standard risk-based test-pyramid thinking applied specifically to this application's actual shape (a small number of genuinely critical journeys — checkout being the standout — sitting on top of a broad, cheap, mostly-stateless catalog/API surface).

## 4. UI Testing Strategy

- **Critical user journeys first:** Layer 2/3 automation prioritizes the journeys tied to Critical/High-priority `REQ-*` items ([03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 13), not every navigable page.
- **Stable locator strategy:** prefer accessible role/label/placeholder-based locators, consistent with REQ-UI-001 and the accessibility-tree-based approach already used successfully throughout Steps 2–4's own verification work.
- **Functional assertions over incidental ones:** assert on the deterministic, business-meaningful signals already VERIFIED in Step 2 (e.g., the exact checkout-gate modal text, the exact invalid-login error text) rather than incidental DOM structure.
- **Negative validation is first-class, not an afterthought:** invalid login, missing required fields, and other negative paths are planned alongside positive paths from the start (mirrors REQ-FUNC-SL-004, already the strongest-verified negative case).
- **Navigation validation:** confirm the consistent navigation/footer components (REQ-UI-006) render correctly as a byproduct of other tests, rather than as a large dedicated suite.
- **Data/state validation:** where a UI-rendered value (price, product name) can be cross-checked against the Layer 1 API response, prefer that over hard-coded expected values, reducing maintenance cost when the demo catalog changes.
- **Cross-browser coverage:** applied per Section 13, not per individual UI test.
- **Screenshot/trace evidence on failure:** every UI test failure captures a screenshot at minimum; trace/video capture is reserved for retry attempts, following the proven **REFERENCE (TS artifact)** pattern in `playwright.config.ts` (`screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`, `trace: 'on-first-retry'`) — cited as evidence this pattern works for this application, not adopted verbatim as a Python config decision (that belongs to Framework Architecture, Step 11).
- **Test isolation:** each UI test establishes its own state; no UI test depends on execution order or another test's leftover state (Section 19).
- **Repeatability:** UI tests must tolerate the shared-environment reality (Section 19) — e.g., not assuming a fixed, un-shared cart state.
- **Avoiding unnecessary duplication:** a business behavior already covered by a Layer 1 API test is not redundantly re-asserted at the UI layer unless the UI rendering itself is the thing under test.

No actual UI test cases are written in this document — that is Step 6/7.

## 5. API Testing Strategy

Grounded in the fully-verified 14-endpoint inventory ([02-Application-Analysis.md](02-Application-Analysis.md) Section 10 / [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 6.3):

- **Positive validation:** confirm documented 200/201 responses and payloads for the 8 read/positive-flow endpoints and the account-lifecycle endpoints.
- **Negative validation:** confirm documented 400/404/405 responses (missing parameter, invalid credentials, unsupported method) — the AUT's own API documentation already frames these as first-class scenarios, and this strategy treats them the same way.
- **Status code and response-structure validation:** every API test asserts both the HTTP status and the response message/body shape — status-only assertions are treated as insufficient.
- **Request validation:** confirm required-parameter enforcement (e.g., `search_product`, `email`/`password`) matches documented behavior.
- **Business rule validation where supported:** e.g., BR-003 (checkout requires authentication) is partially testable at the API layer via `verifyLogin`, complementing UI-layer confirmation.
- **State-mutating endpoint handling:** `createAccount`/`updateAccount`/`deleteAccount` (REQ-API-011–013) are treated as a distinct sub-category requiring a proven create → verify → delete cycle in the same test, never a create without a matching cleanup step.
- **API test isolation:** each API test uses independently generated or clearly-scoped data; no API test relies on another API test's side effects.
- **Cleanup strategy:** any test that creates an account is responsible for deleting it, mirroring the discipline already established in the TS baseline (AE-TDD-001 §1) and reinforced by this project's own shared-environment risk analysis (Section 2).
- **API-first validation where practical:** given all 14 endpoints require no browser and 10 require no credentials at all, API validation is sequenced ahead of UI validation for the same underlying data (e.g., product/brand data) wherever both exist, for faster feedback.

No actual API test cases are written here — that is Step 6/7.

## 6. Hybrid E2E Strategy

Hybrid tests combine UI and API **only when doing so provides value a pure UI or pure API test cannot** — not as a demonstration that both can appear in one test. Four value patterns are recognized as strategically justified:

| Pattern | Value | Applies to this project? |
|---|---|---|
| API setup → UI validation | Faster, more reliable test data provisioning than UI-driven signup, isolating the UI test from Signup-flow defects | Yes — candidate once `createAccount` is verified reliable (REQ-E2E-001, currently REFERENCE-only per Step 3) |
| UI action → API verification | Confirms a user-facing action produced the correct backend-visible state | Limited — most AUT actions (cart, checkout) have no corresponding read API to verify against (`view_cart`/checkout state is not exposed via any documented endpoint) |
| API state preparation → UI business flow | Removes slow/flaky UI setup steps from a business-critical journey under test | Yes — candidate for Checkout once both Login and Checkout are independently UI-verified (REQ-E2E-002) |
| UI business action → API response/state verification | Closes the loop between user action and backend confirmation | Not currently achievable — no product/cart mutation API exists, matching the TS baseline's own finding (AE-AS-001 §13, "no product or cart mutation API exists in this application") |

**Strategic decision:** Hybrid work is **sequenced after**, not parallel to, Layer 2 verification of Login and Checkout — a Hybrid test that shortcuts through an unverified UI flow is only as trustworthy as the flow it shortcuts. This is a deliberate departure from treating Hybrid as an equal, independent third pillar from day one; it is treated here as a **force-multiplier applied once its dependencies are proven**, consistent with how the TS baseline itself scoped it (AE-AS-001 §13: Hybrid was *planned* but never implemented, precisely because it depends on the UI/API layers being solid first).

## 7. Regression Strategy

| Suite | Composition | When It Runs |
|---|---|---|
| Smoke | Home/navigation/core-page availability (Section 8) | Local development (fast inner loop), every Pull Request |
| Critical regression | Layer 1 (all stateless API reads) + Layer 2 tests for Critical-priority `REQ-*` items already VERIFIED | Every Pull Request |
| Full regression | All automated tests across all layers, Chromium only | Every push to main; on manual dispatch |
| API regression | Layer 1 in isolation | Any time, cheaply, including local development |
| UI regression | Layer 2 in isolation | Pull Request (smoke subset) and main-branch (full subset) |
| Hybrid regression | Once Hybrid tests exist (Section 6) | Main-branch and scheduled runs only — not PR-gating, since Hybrid depends on the most state-sensitive operations |
| Cross-browser regression | Curated Layer 2/3/4 subset across all 3 engines | Scheduled execution and release validation only — not PR-gating (Section 13) |

**Strategic rationale for this cadence — REFERENCE (TS artifact) precedent:** the TS project's actual `.github/workflows/playwright.yml` implements exactly this shape: Pull Requests run only tagged, fast suites (`@step14` API, `@step15` Hybrid, `@smoke` UI) on Chromium; push-to-main/manual/schedule runs the full stable Chromium regression; a daily `cron` schedule provides environment-instability canary signal independent of code changes. This project adopts the same **strategic shape** (fast PR gate, broader main-branch regression, scheduled canary, release-time cross-browser) as a proven pattern for this exact application — without adopting the TS project's specific tags, file paths, or YAML.

**Notable gap observed in the TS artifact, flagged rather than silently inherited:** although 3 browser projects (chromium/firefox/webkit) are configured in the TS `playwright.config.ts`, the actual CI workflow **only ever executes `--project=chromium`** — Firefox and WebKit are never invoked by any CI job shown in the workflow file. Cross-browser execution in the TS project appears to be a local/manual capability, not an implemented CI regression tier. This project's own cross-browser regression tier (this Section, "Scheduled execution and release validation") is therefore a **planned strategic decision**, not a continuation of a proven CI practice — see Section 31 decision log.

## 8. Smoke Test Strategy

A small, high-value layer confirming the application and framework are both operational: core page availability (Home, Products, Login, Cart, Contact Us) and one representative check per Critical `REQ-*` module — enough to answer "is anything fundamentally broken?" in under a few minutes, not to substitute for regression. The exact test selection is deferred to Test Scenario Design (Step 6); this strategy only commits to the *purpose and size* of the layer, mirroring the TS baseline's own `@smoke`-tagged PR-gate suite as **REFERENCE (TS artifact)** precedent for the pattern (not the specific tests).

## 9. Cross-Browser Strategy

Per [04-Test-Plan.md](04-Test-Plan.md) Section 11 (already approved): **Chromium, Firefox, and WebKit** — Playwright's three native engines. This strategy does **not** revert to the TS Master Test Plan's inconsistent "Chrome/Firefox/Edge" wording; that inconsistency was already identified and resolved in favor of the artifact-corroborated set at the Test Plan step.

- **Primary browser: Chromium.** All Layer 1–3 development and every PR/main-branch regression run against Chromium first — matching both this project's fastest-feedback needs and the TS project's actual proven CI practice (Section 7).
- **Secondary browsers: Firefox and WebKit.** Applied to a curated, business-critical subset (Layer 4) at scheduled/release-validation cadence, not on every run — a deliberately narrower commitment than "full cross-browser CI," precisely because the TS artifact evidence (Section 7) shows even the prior project never fully committed to that in its own CI.
- **Purpose:** detect rendering/interaction differences on the flows customers actually depend on (cart, checkout gate, login) — not to prove general Playwright compatibility, which is already Playwright's own responsibility, not ours.
- **Browser-specific failure analysis:** a Layer 4 failure is first checked against the equivalent Chromium result; if Chromium passes and another engine fails, the failure is triaged as browser-specific before being treated as a general application or automation defect.

No cross-browser execution has occurred yet under this project — this section states strategy only.

## 10. Test Data Strategy

- **Static data:** stable reference values unlikely to change often (e.g., known category/brand names) — low maintenance cost, safe to hard-code initially, migrated to config only if churn is observed.
- **Dynamic/generated data:** any user-account data must be uniquely generated per test run (e.g., timestamp-suffixed emails), mirroring the TS baseline's own data-collision mitigation (AE-TDD-001 §5) and this project's shared-environment risk (Section 2).
- **Existing/reusable users:** a small number of durable, known-valid accounts for login/logout scenarios that don't need uniqueness, reducing account-creation churn on the shared environment.
- **New users:** always paired with a verified cleanup step (Section 5) before being trusted in regression.
- **Product data:** preferentially sourced live from the Layer 1 API rather than hard-coded IDs, to reduce brittleness against catalog drift ([03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11).
- **Search data:** at minimum one matching keyword, one non-matching keyword, and the missing-parameter case (REQ-API-005/006) — plus, given Step 2's unresolved search-relevance anomaly (Open Question in Step 3, Section 12), an explicit test data case designed to probe *why* an unexpected match occurred, not just whether search "works."
- **Cart/checkout data:** quantities and order comments only; **no real payment data is ever used**, consistent with [04-Test-Plan.md](04-Test-Plan.md) Section 24.
- **API payloads (positive/negative):** modeled directly on the documented request shapes for all 14 endpoints (already fully catalogued in Step 2/3).
- **Data collision, shared environment, cleanup, reusability, repeatability, independence:** all governed by the same principle — **any data this project creates on the shared public instance must be uniquely identifiable and independently cleanable**, and any test depending on pre-existing, non-unique data must not assume it is the only consumer of that data.

The actual Test Data Design document (file-level structure, exact values, naming convention) remains Step 8 — this section commits to principles only.

## 11. Environment Strategy

- **Local environment:** the primary inner-loop environment for framework and test development, run headed or headless, against the live public application (no staging exists — [04-Test-Plan.md](04-Test-Plan.md) Section 10).
- **Browser execution:** local Playwright-managed browser binaries during development; the same binaries (via a container image) in Docker/CI, so behavior is not dependent on a developer machine's installed browser versions.
- **Docker environment:** the reproducibility layer connecting local and CI (Section 16) — not a separate testing target, but the mechanism by which "local," "CI," and any future contributor's machine converge on the same runtime.
- **CI/CD environment:** the environment of record for regression evidence (Section 17) — results here, not local results, are what the QA Lead should trust for gating decisions, since only CI guarantees a clean, reproducible starting state.

**Consistency and reproducibility:** achieved by minimizing what varies between these environments (browser version, Python/package versions, OS-level dependencies) via Docker, while accepting the one variable this project cannot control — the live application's own state — as a documented, permanent constraint (Section 30), not something environment strategy can solve.

## 12. Docker Strategy

Docker's strategic role in this project:

- **Reproducibility:** any contributor (or CI runner) gets an identical starting environment, removing "works on my machine" as a failure category.
- **Environment consistency:** pins OS-level dependencies, Python version, and browser binaries together as one versioned unit.
- **Dependency isolation:** test-only dependencies never leak into or depend on the host machine's own Python/Node/browser installations.
- **Browser execution consistency:** the same browser binary versions run locally, in CI, and (if ever needed) on a teammate's machine.
- **Local/CI parity:** the container run locally and the container run in CI should be the same image, so a CI-only failure is meaningfully suspicious (environment-specific) rather than expected.
- **Easier onboarding:** a new contributor (or portfolio reviewer) can run the suite with one command, without first configuring a Python/Playwright toolchain.
- **Reduced environment drift:** over the life of the project, pinned image versions prevent silent drift as Python/Playwright/browser versions update independently on different machines.

**REFERENCE (TS artifact) — proof of concept, not a template:** the TS project's actual `Dockerfile` (already inspected in Step 4) demonstrates this pattern is achievable for this exact application: it builds `FROM mcr.microsoft.com/playwright:v1.61.1-noble` (an official, version-pinned Playwright base image bundling matching browsers), installs dependencies via a cached layer, and defaults to running the Chromium suite, with other suites overridable at `docker run` time. This is cited here only as evidence that containerized execution is proven and low-risk for this application — **the Python project's own base image, dependency manager, and default command are Step 11/implementation-phase decisions**, not made or implied here. No Docker file is created in this step.

## 13. CI/CD Strategy

| Trigger | Strategic Intent | Composition (see Section 7 for suite definitions) |
|---|---|---|
| **Pull Request** | Fast, targeted validation — don't block a contributor on the full suite | Smoke + Critical (Layer 1 + verified Critical Layer 2), Chromium only |
| **Main branch** (post-merge push) | Broader confidence than a PR gate justifies waiting for | Full regression across Layer 1–3, Chromium only |
| **Scheduled execution** | Full regression **and** cross-browser coverage where it earns its cost, independent of code changes — surfaces environment drift/instability | Full regression + Layer 4 cross-browser subset, on a daily-or-similar cadence |
| **Release validation** | Highest-confidence evidence gate before any release-readiness claim | Critical regression (all layers) + full cross-browser Layer 4 + explicit collection of required evidence (Section 21) |

- **Failure visibility:** every run's pass/fail status and a job-level summary must be visible without requiring local reproduction first — mirroring the TS artifact's job-summary pattern as **REFERENCE (TS artifact)** precedent, not a locked implementation.
- **Test reports:** generated every run, human-readable, retained as CI artifacts.
- **Artifacts (screenshots/traces/logs):** retained per run for a bounded period (a specific retention window is an implementation detail for Step 11/14 — the TS artifact's 14-day retention is cited only as a reasonable, proven precedent, not a locked Python decision).
- **Known-AUT-limitation handling — REFERENCE (TS artifact), strategically valuable pattern:** the TS CI workflow runs one known, documented AUT-level limitation test (a Contact Us "client-side readiness race") separately and marks it `continue-on-error`, so it never blocks the pipeline but its result remains visible. This project adopts the **principle** — a confirmed AUT limitation should be observable, not silently hidden, but also must not be allowed to gate CI the same way a real regression would (Section 22 makes this distinction formal).

No CI/CD pipeline is implemented in this step.

## 14. Parallel Execution Strategy

Parallel execution is valuable for reducing wall-clock time, but **this project does not optimize for maximum parallelism at the cost of reliability**, given the shared-public-environment risk already central to this strategy (Section 2).

- **Layer 1 (API, mostly read-only):** safe to parallelize aggressively — no shared mutable state risk for the read endpoints; write endpoints (`createAccount`/`updateAccount`/`deleteAccount`) are parallelized only if each run uses independently unique data.
- **Layer 2/3 (UI):** parallelizable within a single browser engine as long as each test's data is independent (Section 19); tests that touch shared, mutable state (e.g., an account also used by another concurrently-running test) must not run in parallel with each other.
- **Layer 4 (cross-browser):** parallel *across* browser engines is natural and low-risk (different engines don't contend for the same AUT state any differently than sequential runs would); parallel *within* an engine follows the same Layer 2/3 rule.
- **CI resource usage:** **REFERENCE (TS artifact)** — the TS project's own `playwright.config.ts` sets `fullyParallel: true` for local development but `workers: 1` specifically when running in CI (`env.isCI`), i.e., **the prior project deliberately serialized its own CI execution** despite having parallel capability locally. This is strong, directly-relevant precedent that this project's CI strategy should also favor a conservative worker count against the shared public environment, even though the exact number is an implementation decision (Step 11), not fixed here.

**Strategic decision:** local development execution may parallelize freely for speed; CI/CD execution defaults to a conservative concurrency posture unless a given suite is proven safe (e.g., Layer 1 read-only) — reliability against the shared environment outweighs raw CI speed for this project.

## 15. Test Isolation Strategy

Especially important given Automation Exercise is a shared public environment (Section 2):

- **Independent tests:** no test may depend on another test having run first, or on the order tests execute in.
- **State setup:** each test that needs a precondition (a product in cart, a logged-in session) establishes it itself, rather than assuming a prior test left the right state behind.
- **State cleanup:** any state a test creates that could affect another test or persist on the shared environment (an account, a cart addition) is cleaned up by that same test, not left for "someone" to clean up later.
- **Dynamic data:** uniquely-generated identifiers (Section 10) are the primary tool for avoiding collision between this project's own tests and between this project and any other concurrent user of the same public demo site.
- **Avoiding execution-order dependency:** tests must pass individually and in any order/subset — a requirement that also make parallel execution (Section 14) safe by construction rather than by luck.
- **API state mutation:** isolated per test via unique data, exactly as in Section 5/10 — never shared across tests "to save setup time," since that is precisely the kind of shortcut that produces shared-environment collisions.
- **Shared public environment as a first-class design constraint:** unlike a typical enterprise project with a disposable per-run test environment, this project must treat *every* test as a guest on a system other people are using concurrently — isolation here is not just good practice, it is the only thing standing between this project's tests and each other, and between this project and the wider public user base of the demo site.

## 16. Flaky Test Strategy

- **Definition:** a test is flaky if it produces different results (pass/fail) across repeated runs against an unchanged application and unchanged test code, under otherwise equivalent conditions.
- **Identification:** flagged when a test fails, then passes on an immediate, unmodified re-run.
- **Diagnosis:** before any retry-based conclusion is trusted, the failure evidence (Section 21) is reviewed to classify it into one of three categories:

| Category | Definition | Example (grounded in this project) |
|---|---|---|
| **Transient infrastructure/environment failure** | The shared public site or network was momentarily unavailable/slow, unrelated to test logic or application defect | A request timeout during a scheduled canary run, with no corresponding change in application or test code |
| **Real product defect** | The application genuinely behaves inconsistently or incorrectly | The unresolved search-relevance anomaly from Step 2, if it turns out to be non-deterministic rather than a fixed (if surprising) rule |
| **Automation defect** | The test itself has a synchronization/assertion problem | A test that doesn't correctly wait for the AJAX-driven cart-removal update (REQ-UI-005) and asserts too early |

- **Retry philosophy:** retries (**REFERENCE (TS artifact)** precedent: TS `testConfig.ts` sets `retries: { ci: 2, local: 0 }`) are acceptable as a *symptom-management* tool for genuinely transient infrastructure issues, and this project follows the same CI-only, non-zero-locally pattern in principle. **Retries must never be used to hide a real product defect or a real automation defect** — a test that only passes on retry must still be investigated and classified per the table above, not treated as "fixed" by virtue of eventually passing.
- **Quarantine policy:** a test confirmed flaky (not merely retried-and-passed) is removed from the trusted/gating suite and tracked separately until root-caused — it does not silently continue contributing "passing" results to release-confidence reporting (Section 27) while unresolved.
- **Root-cause analysis:** required before a quarantined test re-enters the main suite; the fix must address the category identified above (wait strategy for automation defects, application follow-up/documentation for product defects, resilience adjustment for infrastructure).
- **Re-entry:** only after the root cause is fixed and the test demonstrates stable, repeated passes.

## 17. Failure Diagnostics Strategy

Every test failure, regardless of layer, must produce enough evidence to diagnose without blind re-running:

- **Screenshot:** at minimum, at the point of UI failure.
- **Trace:** collected at least on retry, sufficient to replay the failing interaction step-by-step.
- **Logs:** console/application-level output captured for the failing test.
- **API request/response evidence:** for API/Hybrid failures, the exact request sent and response received (status, body) must be captured — a bare "assertion failed" is not sufficient evidence for this project's standard.
- **Browser information:** which engine (Chromium/Firefox/WebKit) and, where relevant, viewport/device context.
- **Test metadata:** requirement ID(s) under test, module, and priority, so a failure can be immediately weighed for its business impact (Section 2) without cross-referencing separately.

**No specific reporting library is locked here.** The TS artifact's proven pattern (`reporter: 'html'`, `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`) is cited as **REFERENCE (TS artifact)** evidence that this evidence set is achievable with Playwright's native tooling — the Python-equivalent implementation is a Framework Architecture (Step 11) decision.

## 18. Defect Management Strategy

Building on [04-Test-Plan.md](04-Test-Plan.md) Section 16, this strategy adds explicit classification discipline before a failure is even logged as a defect:

| Classification | Who/what is responsible | Strategic handling |
|---|---|---|
| **Application defect** | The AUT itself behaves incorrectly relative to a documented `REQ-*` | Documented as an observation (this project has no channel to get third-party application code fixed — [04-Test-Plan.md](04-Test-Plan.md) Section 16); tracked as a **known limitation** (Section 19) if confirmed and unfixable, following the TS artifact's `continue-on-error`, non-blocking precedent (Section 13) |
| **Automation defect** | Our own test code (bad locator, race condition, wrong assertion) | Logged and fixed like any software defect in our own codebase — the primary category this project can and must resolve directly |
| **Environment/infrastructure failure** | Network blip, site temporarily down, shared-state collision from concurrent public usage | Not logged as a defect; retried/re-run once per Section 16, and tracked in aggregate only if frequency suggests a genuine stability pattern worth escalating |
| **Test-data issue** | Data collision, stale/expired reference data, cleanup failure | Logged against the test data design (a Step 8 artifact), not against the application or the test logic itself |

Triage sequence: reproduce → classify (table above) → assign severity/priority ([04-Test-Plan.md](04-Test-Plan.md) Section 16) → attach evidence (Section 17) → resolve appropriately to its category → retest → regression-verify → close. Application-defect classification never results in a "fix," only a documented, QA-Lead-reviewed limitation entry.

## 19. Traceability Strategy

Chain: **Requirement → Test Scenario → Test Case → Automation → Execution → Defect → Retest → Release Evidence.**

- `REQ-*` IDs originate in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) and do not change identity as they flow downstream.
- Test Scenarios (Step 6) and Test Cases (Step 7) will each cite their originating `REQ-*` ID(s), following the same discipline the TS baseline demonstrated (`AE-UI-XXX`/`AE-API-XXX` → `FR-*` in AE-TSD-001) — **REFERENCE KNOWLEDGE (TS baseline)** pattern, not TS's specific IDs.
- Automation (Steps 9–10 onward) will tag or otherwise link each automated test back to its Test Case ID, so a failing automated test can be traced to a requirement without manual cross-referencing.
- Execution results (Phase 12) roll up by requirement and by module, enabling the coverage-gap reporting already modeled in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14.
- Defects (Section 18) reference the Test Case and `REQ-*` ID that exposed them.
- Retest evidence closes the loop back to the same Test Case.
- Release Evidence (Phase 18) is assembled by rolling this entire chain up to a coverage/pass-rate view per requirement priority — not a bare test-count.

The detailed traceability matrix itself is **not created in this document** — it is maintained incrementally as Steps 6–12 produce the artifacts each link depends on.

## 20. Automation Strategy

**Reference baseline (unchanged): 24 UI + 8 API = 32 Phase-1 tests**, per [04-Test-Plan.md](04-Test-Plan.md) Section 9. This strategy does not alter that number and does not decide the Python project's own automation scope — that remains Step 9.

**What makes a test a good automation candidate, for this project specifically:**

| Factor | Favors Automation | Disfavors Automation (for now) |
|---|---|---|
| Stability | Behavior already VERIFIED and deterministic in Step 2 (e.g., checkout-gate message, invalid-login error) | Behavior still only REFERENCE-only/unverified (e.g., most of Checkout) — automate only after direct verification, not before |
| Repeatability | Read-only or cleanly-cleanable state (products, brands, cart-add/remove) | Operations with no proven cleanup path |
| Business value | Critical/High-priority `REQ-*` items (Section 2/13 of Requirement Analysis) | Low-priority, ancillary items (e.g., scroll-button behavior, already deferred by the TS baseline itself) |
| Regression value | Frequently-relevant, customer-facing flows (cart, search, login) | One-off exploratory checks with little recurring value |
| Maintenance cost | Stable locators (REQ-UI-001), deterministic assertions | Dynamic, ad-like, or third-party content (the unrelated ad text observed on the empty-cart page in Step 2) — a poor automation candidate for assertions |
| Data requirements | Data that can be generated uniquely and cleaned up (Section 10) | Data requiring manual/one-time setup with no repeatable provisioning path |
| Execution frequency | Suited to running on every PR/main-branch build without excessive cost | Suited only to scheduled/release-time cadence (Section 7) |

This table is a **decision framework for Step 9**, not a scope decision made here.

## 21. Maintainability Strategy

Principles only — no folder structure or code architecture is defined here (that is Step 11, Framework Architecture):

- **Reusable components** over duplicated interaction logic.
- **Page objects** (or an equivalent Python/Pytest-idiomatic abstraction — the exact pattern is a Step 11 decision) to isolate UI structure knowledge from test logic.
- **API clients** (or an equivalent request-building abstraction) to isolate endpoint/payload knowledge from test logic, mirroring the *principle* behind the TS baseline's `src/api/clients/` separation — **REFERENCE KNOWLEDGE (TS baseline)**, principle only, not its class structure.
- **Fixtures** for setup/teardown, favoring Pytest-idiomatic fixture scoping over ad hoc setup code.
- **Centralized configuration** (base URL, timeouts, environment flags) rather than values scattered across test files.
- **Test data separation** from test logic, consistent with Section 10.
- **Stable locators** (REQ-UI-001) to minimize churn when the AUT's markup changes.
- **Clear, consistent naming** tied to requirement/module identity, supporting the traceability strategy (Section 19).
- **Avoid duplication** — a behavior validated at Layer 1 is not re-validated identically at Layer 2 "just in case" (Section 4).
- **Small, focused tests** — one behavior per test, favoring diagnosability over broad multi-assertion tests.
- **Controlled abstractions** — introduce a shared helper only once a pattern repeats, not preemptively.

## 22. Quality Gates

| Gate | Evidence Required |
|---|---|
| Gate 1 — Requirements baselined | [03-Requirement-Analysis.md](03-Requirement-Analysis.md) approved (✅ already met) |
| Gate 2 — Test scenarios/cases approved | Steps 6–7 documents approved by QA Lead |
| Gate 3 — Automation scope approved | Step 9 document approved, with the 32-test reference baseline explicitly reconciled (kept, expanded, or adjusted with rationale) |
| Gate 4 — Framework ready | Framework Architecture (Step 11) and initial setup (Phase 6/7) complete enough that tests can execute end-to-end locally |
| Gate 5 — Critical regression complete | All Critical-priority `REQ-*` items have passing evidence or a documented, accepted exception (mirrors [04-Test-Plan.md](04-Test-Plan.md) Section 15) |
| Gate 6 — Release readiness evidence available | Test Summary Report, defect log, and known-limitations list assembled (Phase 17–18) for QA Lead review |

Each gate requires explicit QA Lead sign-off before the next phase proceeds — consistent with the governance model in [01-Project-Vision.md](01-Project-Vision.md) Section 19.

## 23. Release Confidence Strategy

Release confidence will eventually be assessed as a composite of:

- **Test coverage** — proportion of `REQ-*` items with passing, direct (not reference-only) evidence.
- **Critical-path execution** — whether every Critical-priority journey (Section 2) has actually run, not merely been designed.
- **Pass/fail results** — current-state results, not historical/best-ever results.
- **Defect severity distribution** — weighted toward Blocker/Critical items, per [04-Test-Plan.md](04-Test-Plan.md) Section 16.
- **Residual risk** — the unresolved items in Section 2/27, explicitly carried forward rather than assumed away.
- **Environment stability** — signal from scheduled/canary runs (Section 13), not just point-in-time PR results.
- **Regression results** — trend, not a single run.
- **Known limitations** — explicitly listed, not hidden inside a raw pass rate.

**No release recommendation is made in this document** — this section defines the *inputs* to that future judgment call, which belongs to the Release Readiness phase (Phase 18) under QA Lead authority.

## 24. Metrics Strategy

Metrics this project will eventually collect (mechanism/dashboard is a later-phase decision, not created here):

- Planned vs. executed test counts, by layer and by module.
- Pass / fail / blocked counts.
- Automation coverage (automated vs. total planned tests, once Step 9 finalizes scope).
- Requirement coverage (VERIFIED vs. REFERENCE-only `REQ-*` items — directly extending the count already produced in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14).
- API endpoint coverage (of the 14 documented endpoints).
- Execution duration, by suite (Section 7), to monitor whether PR-gate speed stays acceptable as the suite grows.
- Flaky-test rate (Section 16), tracked as its own trend, not folded into the pass rate.
- Defect count and severity distribution (Section 18).
- Regression status over time (trend, not snapshot).

No QA Dashboard is built in this step.

## 25. Security / Performance / Accessibility

Per [04-Test-Plan.md](04-Test-Plan.md) Sections 4 and 7, and [01-Project-Vision.md](01-Project-Vision.md) Section 10: **Security, Performance, and Accessibility testing are not committed scope for this project.** This Test Strategy does not silently expand scope to include them. They remain **Future Scope / potential extension** only, exactly as already decided — no test approach, tooling, or test case is defined for them here, and none should be inferred from the presence of this section.

## 26. Known Limitations

Carried forward, not re-derived, from Steps 2–4 — no new assumption is used to resolve any of them:

- Public shared environment with no staging instance ([02-Application-Analysis.md](02-Application-Analysis.md) Section 14).
- Signup/Login and Checkout/Order/Invoice remain largely unverified (16 of 48 `REQ-FUNC-*`/`REQ-API-*` items — [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14) — this is the single most consequential limitation for this strategy's sequencing decisions (Sections 1, 2, 6, 20).
- Payment behavior cannot be fully validated (simulated flow, unconfirmed exact mechanics — [04-Test-Plan.md](04-Test-Plan.md) Section 24).
- API state mutation affects real, shared backend data ([02-Application-Analysis.md](02-Application-Analysis.md) Section 10).
- Environment instability is possible and outside this project's control ([04-Test-Plan.md](04-Test-Plan.md) Section 17).
- Documented discrepancies between sources remain unresolved by design: the `/checkout` vs. `/view_cart` route question, the TS Master Test Plan's browser-list inconsistency (already resolved procedurally in Step 4, but the underlying TS document itself remains internally inconsistent), and the newly observed gap between the TS project's *documented* cross-browser strategy and its *actual* Chromium-only CI practice (Section 7 of this document).

## 27. Strategy Decision Log

| # | Decision | Rationale | Source/Basis | Impact |
|---|---|---|---|---|
| 1 | Browser strategy = Chromium (primary) + Firefox + WebKit (secondary, curated) | Matches the already-approved Test Plan decision; avoids the TS Master Test Plan's internal Chrome/Firefox/Edge inconsistency | [04-Test-Plan.md](04-Test-Plan.md) §11; TS `AE-FA-001` + `package.json` (artifact-corroborated) | Defines Section 9/13 scope |
| 2 | 24 UI + 8 API (32-test) baseline preserved as reference only | Explicit instruction; final scope belongs to Step 9 | TS `AE-AS-001`/`AE-TSD-001` | Section 20 framework only, not a commitment |
| 3 | Layered API-first, UI-second, Hybrid-last sequencing | All 14 APIs already independently verified and largely stateless; Signup/Login/Checkout UI verification gap must close before Hybrid can be trusted | [02-Application-Analysis.md](02-Application-Analysis.md) §10; [03-Requirement-Analysis.md](03-Requirement-Analysis.md) §14 | Drives Sections 1, 3, 6 |
| 4 | Docker planned as a strategic capability, implementation deferred | Proven precedent exists (TS `Dockerfile`), but Python-specific implementation is a Step 11 concern | TS `Dockerfile` (artifact) | Section 12 |
| 5 | CI/CD planned with a graduated trigger model (PR fast-gate → main broader → scheduled canary → release full) | Directly evidenced as workable for this exact application by the TS project's actual workflow | TS `.github/workflows/playwright.yml` (artifact) | Sections 7, 13 |
| 6 | Risk-based prioritization drives sequencing over "replicate the TS baseline as-is" | 16 of 48 requirements remain unverified; automating unverified behavior first would encode untested assumptions into regression | [03-Requirement-Analysis.md](03-Requirement-Analysis.md) §14 | Sections 1, 2, 6, 20 |
| 7 | Shared-environment precautions govern data, isolation, and parallelism | No staging environment exists; TS project itself serialized CI workers despite parallel capability | [02-Application-Analysis.md](02-Application-Analysis.md) §14; TS `playwright.config.ts`/`testConfig.ts` (artifact) | Sections 10, 14, 15 |
| 8 | Cross-browser CI regression is a genuinely new commitment, not a continuation of proven TS practice | TS CI workflow only ever runs Chromium despite having 3 configured browser projects | TS `.github/workflows/playwright.yml` (artifact) | Sections 7, 9, 13 — flagged for QA Lead awareness, not silently assumed |
| 9 | Retries are CI-only and diagnostic-gated, never a substitute for root-cause | Retries must not mask real defects (explicit instruction); TS precedent shows a deliberate, non-zero-but-bounded CI retry policy | TS `testConfig.ts` (artifact) | Section 16 |
| 10 | Security/Performance/Accessibility remain Future Scope, not silently expanded | Explicit instruction; matches already-approved Test Plan/Vision scope | [01-Project-Vision.md](01-Project-Vision.md) §10; [04-Test-Plan.md](04-Test-Plan.md) §4/7 | Section 25 |

## 28. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 5 Exit Checklist

- [x] Current Python project documents (Steps 1–4) reviewed and used as primary basis
- [x] Previous TS Test Strategy reviewed (Priority 2)
- [x] Previous TS QA baseline (all 10 docs) considered, cumulative with Steps 2–4
- [x] TS artifacts directly inspected where needed: `package.json`, `Dockerfile` (Step 4), `.github/workflows/playwright.yml`, `playwright.config.ts`, `src/config/testConfig.ts` (this step)
- [x] Step 4 Test Plan treated as primary current planning source, not duplicated (Section 0)
- [x] Risk-based strategy included (Section 2)
- [x] UI/API/Hybrid strategy included (Sections 4–6)
- [x] Regression/smoke strategy included (Sections 7–8)
- [x] Chromium/Firefox/WebKit used, not TS's inconsistent wording (Section 9)
- [x] Docker strategy included, no files created (Section 12)
- [x] CI/CD strategy included, no files created (Section 13)
- [x] Parallel execution strategy accounts for shared-environment risk (Section 14)
- [x] Flaky-test strategy included, with explicit transient/product/automation distinction (Section 16)
- [x] Traceability strategy included (Section 19)
- [x] Quality gates defined (Section 22)
- [x] Release-confidence strategy defined without making a release recommendation (Section 23)
- [x] 24 UI + 8 API baseline unchanged (Section 20)
- [x] No scope expansion into Security/Performance/Accessibility (Section 25)
- [x] No implementation started; no source code, dependencies, Docker files, or CI files created
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 6 — Test Scenario Design.
