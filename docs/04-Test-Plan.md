# 04 — Test Plan

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-TP-001 |
| Document Title | Master Test Plan |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 2 — Test Planning |
| Step | Step 4 — Test Plan |
| Predecessor Documents | [01-Project-Vision.md](01-Project-Vision.md) ✅, [02-Application-Analysis.md](02-Application-Analysis.md) ✅, [03-Requirement-Analysis.md](03-Requirement-Analysis.md) ✅ |
| Reference Baseline | `playwright-typescript-hybrid-framework/docs/AE-TP-001_Master_Test_Plan.docx` (Priority 1 source — adapted, not copied) |

**Evidence labeling** (consistent with Steps 2–3): **VERIFIED OBSERVATION**, **REFERENCE KNOWLEDGE (TS baseline)**, **INFERENCE**. Anything not so labeled is a direct Test Plan decision made at this step.

## 2. Purpose

This Test Plan defines the overall QA testing approach for the `playwright-python-hybrid-framework` project: what will be tested, what will not, why, and how — establishing scope, levels, types, environment, data approach, entry/exit criteria, risk handling, and execution/reporting intent before Test Strategy (Step 5), Test Design (Steps 6–8), and Automation Planning (Steps 9–10) begin. It adapts the previous TypeScript project's approved Master Test Plan (AE-TP-001) as its planning baseline, per [01-Project-Vision.md](01-Project-Vision.md) Section 12 (Python Re-engineering Philosophy) — reusing its QA thinking, not its implementation choices.

## 3. Test Objectives

Derived from [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Sections 6–8, kept realistic for a portfolio-scale project:

1. Validate the functional requirements catalogued as REQ-FUNC-* that are within approved scope, prioritizing the modules already independently VERIFIED in Step 2 (Home, Products, Cart-add/remove, Contact Us fields).
2. Validate the API surface catalogued as REQ-API-* against its documented status codes and messages (all 14 endpoints, differentiating Phase-1-automatable from future-scope per the TS baseline — see Section 9).
3. Validate the important user journeys identified in Requirement Analysis Section 6.1 (business requirements) and Section 8 (traceability), including closing the "NOT INDEPENDENTLY VERIFIED" gap around Signup/Login/Checkout identified in that document's Section 14.
4. Identify functional risks and open questions still outstanding from Step 2/3 (e.g., the `/checkout` vs `/view_cart` route question, search-relevance behavior) through direct, planned test execution rather than continued assumption.
5. Support regression confidence for the discovery-and-cart journey, which is already well-understood and stable.
6. Establish a documented basis for evaluating UI, API, and Hybrid automation suitability — not to declare automation scope final (that remains Step 9).
7. Produce reviewable test evidence (results, logs, screenshots/traces) suitable for a QA/SDET portfolio artifact.

**Scope honesty:** As a single-environment, publicly shared demo application project executed by one contributor, this Test Plan does **not** claim to produce enterprise-grade release sign-off, statistically representative regression coverage, or a guarantee of production-quality software — it demonstrates professional QA planning and execution practice against a realistic application. This mirrors the TS baseline's own stated purpose (AE-PV-001 §7, "Portfolio Objectives").

## 4. Test Scope

Aligned strictly to [03-Requirement-Analysis.md](03-Requirement-Analysis.md); nothing here exceeds that document's catalogue.

**In Scope**
- Functional testing of REQ-FUNC-* modules: Home, Signup/Login/Account, Products (listing/detail/search/category/brand/review), Cart, Checkout, Contact Us, Subscription.
- API testing of all 14 REQ-API-* endpoints (documentation/behavior-level testing; see Section 9 for automation-baseline status distinction).
- Hybrid/E2E testing opportunities per REQ-E2E-* (currently reference-only/proposed — see Section 9).
- Cross-browser UI execution (Section 11).
- CI/CD-driven execution (Section 22).
- Docker-based reproducible execution (Section 23).
- Reporting and failure evidence capture (Section 21).

**Out of Scope**
- Performance, load, and stress testing.
- Security and penetration testing.
- Accessibility (a11y) testing.
- Mobile-native application testing.
- Visual regression testing.
- Database-level or backend-log validation (no access exists — [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11).
- Real payment-gateway validation (payment is a simulated/demo flow — Section 24).

This list matches [01-Project-Vision.md](01-Project-Vision.md) Section 10 and TS AE-TP-001 §4 ("Out of Scope") with no additions or removals.

**Future Scope**
- The 6 API endpoints TS baseline marks deferred (`verifyLogin` without email, `DELETE verifyLogin`, `createAccount`, `deleteAccount`, `updateAccount`, `getUserDetailByEmail` as standalone tests) — REFERENCE, TS AE-AS-001 §6.
- The two scroll-behavior UI scenarios (TC-25/26) deferred in the TS baseline — REFERENCE, TS AE-TSD-001 §7.
- Hybrid scenarios REQ-E2E-001/002 (planning-only even in the TS project — no Hybrid code exists there either) and REQ-E2E-003 (newly proposed in this project's Step 2/3, not yet approved).
- Any expansion of out-of-scope items above, only if explicitly re-scoped by the QA Lead in a future step.

## 5. Application Areas in Scope

Directly from [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 6.2/6.3 — no unsupported module included:

| Area | In Scope? | Requirement Reference |
|---|---|---|
| Home | Yes | REQ-FUNC-HM-001–007 |
| Signup / Login | Yes | REQ-FUNC-SL-001–006 |
| Account lifecycle (create/update/delete via API) | Yes, at API-documentation level; UI account-lifecycle deferred per Section 9 | REQ-API-011–014 |
| Products (listing) | Yes | REQ-FUNC-PR-001 |
| Product Details | Yes | REQ-FUNC-PR-002 |
| Search | Yes | REQ-FUNC-PR-003/004, REQ-API-005/006 |
| Categories | Yes | REQ-FUNC-PR-005 |
| Brands | Yes | REQ-FUNC-PR-006, REQ-API-003/004 |
| Cart | Yes | REQ-FUNC-CT-001–005 |
| Checkout | Yes (largely unverified — see Section 17 risk) | REQ-FUNC-CO-001–006 |
| Order / Invoice | Yes (unverified — REFERENCE only) | REQ-FUNC-CO-006 |
| Contact Us | Yes | REQ-FUNC-CU-001–004 |
| Subscription | Yes | REQ-FUNC-HM-007 |
| APIs (all 14) | Yes | REQ-API-001–014 |

## 6. Test Levels

| Level | Applicable? | Notes |
|---|---|---|
| Component / Unit-level testing | **Not applicable** | This project has no access to the AUT's internal source code; there is nothing to unit-test. This distinction is deliberate — we test the deployed application through its public UI and API surfaces only, not internal application code. |
| API-level testing | Applicable | Direct validation of the 14 documented `/api/*` endpoints (REQ-API-*), independent of the UI. |
| UI-level testing | Applicable | Browser-driven validation of REQ-FUNC-* behavior via Playwright. |
| Integration testing | Applicable, in a limited sense | Understood here as verifying that UI-visible behavior is consistent with API-visible data (e.g., product listings), not as integration between internal application services we do not control. |
| End-to-End testing | Applicable | Multi-step user journeys spanning several modules (e.g., search → cart → checkout gate). |

**Application testing vs. automation framework testing — explicit distinction:** This Test Plan governs testing of the *Automation Exercise application's behavior*. It does not plan or govern testing of the Python framework's own internal code (e.g., unit tests for a future page-object helper). Framework-internal quality practices, if any, belong to Framework Architecture (Step 11/Phase 5) and Framework Hardening (Phase 11), not to this document.

## 7. Test Types

| Test Type | Status | Basis |
|---|---|---|
| Functional Testing | In Scope | REQ-FUNC-*, REQ-API-* |
| UI Testing | In Scope | REQ-FUNC-*, REQ-UI-* |
| API Testing | In Scope | REQ-API-* |
| Integration Testing | In Scope (limited sense, per Section 6) | REQ-E2E-* |
| Hybrid E2E Testing | In Scope, opportunistic | REQ-E2E-* (currently reference/proposed only — Section 9) |
| Smoke Testing | In Scope | Home + core navigation, mirroring TS AE-AA-001 §7 "Smoke Suite" concept |
| Regression Testing | In Scope | Applied to the discovery/cart modules already well-verified per [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14 |
| Negative Testing | In Scope | Invalid login, missing API parameters, unsupported HTTP methods (REQ-API-002/004/006/008/009) |
| Boundary-focused testing | In Scope, where applicable | E.g., product quantity edge values (REQ-FUNC-CT-002) — flagged as an open question in Step 3, to be resolved via actual boundary tests |
| Cross-browser Testing | In Scope | Section 11 |
| Compatibility Testing | In Scope, narrowly | Limited to Playwright-supported browser engines; not OS/device-matrix compatibility testing |
| Reliability / Stability Testing | In Scope, narrowly | Understood as automation-suite stability (flakiness reduction) rather than AUT load/soak testing |
| Performance Testing | **Future Scope** — not committed | Per [01-Project-Vision.md](01-Project-Vision.md) Section 10 |
| Security Testing | **Future Scope** — not committed | Per [01-Project-Vision.md](01-Project-Vision.md) Section 10 |
| Accessibility Testing | **Future Scope** — not committed | Per [01-Project-Vision.md](01-Project-Vision.md) Section 10 |
| Usability Testing | **Not planned** | No usability research capability exists in this project; not listed even as future scope |

## 8. Test Approach

#### UI
Playwright for browser automation, Pytest as the test runner, a Page Object Model for maintainability, fixture-based setup/teardown, explicit assertions against the deterministic UI signals verified in Step 2 (e.g., the checkout-gate modal text, the invalid-login error text), test isolation per test function/module, and a locator strategy preferring accessible roles/labels over brittle CSS/text selectors (per REQ-UI-001). **Specific library choices (e.g., which assertion helper, which fixture scoping pattern) are Framework Architecture decisions (Step 11) and are intentionally not locked here.**

#### API
A Python HTTP/API-request approach (exact library — e.g., `httpx`, `requests`, or Playwright's own `APIRequestContext` via `playwright-python` — is a Step 5/11 decision, not made here) validating: HTTP status codes, response message/body content, and request-parameter handling (positive and negative), consistent with REQ-API-*. Schema validation is noted as a "future" concern, mirroring TS AE-TS-001 §4 ("Schema validation (future)") rather than a Phase-1 commitment.

#### Hybrid E2E
Where a UI-facing outcome can be more reliably or efficiently set up via API (e.g., data provisioning) and then verified via UI, or where API state can serve as an independent oracle for UI-rendered data, a Hybrid test is appropriate — following the same justification discipline the TS baseline used (AE-AS-001 §13: "every Hybrid test case must independently justify its own value," not merely combine UI and API for its own sake). Concrete Hybrid scenarios are not finalized in this Test Plan; see Section 9 and REQ-E2E-* in [03-Requirement-Analysis.md](03-Requirement-Analysis.md).

## 9. Test Automation Scope

**Reference baseline (Priority 1, TS AE-AS-001/AE-TSD-001):** 24 UI + 8 API = **32 Phase-1 tests**.

This Test Plan does **not** change this baseline. It is carried forward as an existing point of reference for what a comparable automation scope looked like in the prior project — not as a requirement or commitment for this Python project, whose own automation scope will be formally decided in **Phase 4, Step 9 (Automation Scope)**.

**Observations for future Step 9 consideration (not decisions made here):**
- **Observation:** [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 14 shows 16 of 48 functional/API requirements are currently reference-only (not independently verified) — disproportionately concentrated in Signup/Login and Checkout. **Recommendation:** Step 9 should weigh whether closing this verification gap (under QA Lead-directed, disposable test-account execution) takes priority over simply re-implementing the TS baseline's 32 scenarios as-is.
- **Observation:** All 14 API endpoints are now independently verified at the documentation level (Step 2), 6 more than the TS baseline's Phase-1-automated 8. **Recommendation:** Step 9 should explicitly decide whether the Python project automates only the same 8, or a different subset, given this stronger evidence base — this is a Step 9 decision, not made here.
- **Observation:** The TS Hybrid scenarios (REQ-E2E-001/002) were never implemented even in the TS project (planning-only). **Recommendation:** Step 9/10 should treat them as available prior art, not proven working code.

No baseline number is altered by this Test Plan.

## 10. Test Environment

| Aspect | Value | Status |
|---|---|---|
| Operating System | Windows 11 (current development environment) | VERIFIED — matches this project's actual working environment |
| Python Runtime | Python 3.x | To be finalized during framework setup (Step 6/Phase 6) — a specific pinned version is not yet selected |
| Test Framework | Pytest | Established in [01-Project-Vision.md](01-Project-Vision.md) Section 7 |
| Browser Automation | Playwright (Python) | Established in [01-Project-Vision.md](01-Project-Vision.md) Section 7 |
| Application Environment | Single public shared instance at `https://automationexercise.com` | VERIFIED, no staging/private environment exists ([02-Application-Analysis.md](02-Application-Analysis.md) Section 14) |
| Execution Modes | Local, headless, headed, Docker, CI/CD | Planned — implementation not yet started |

Exact package/browser-binary versions are intentionally **not locked** in this document — "to be finalized during framework setup," consistent with instruction.

## 11. Browser Coverage

**Planned coverage:** Chromium, Firefox, and WebKit — the three engines Playwright natively supports.

**Purpose of cross-browser validation:** to detect rendering or interaction differences across engines for business-critical flows (cart, checkout gate, login), consistent with the general QA principle carried forward from the TS baseline (REQ-NFR-AUTO-001 in [03-Requirement-Analysis.md](03-Requirement-Analysis.md)) that customer-facing e-commerce behavior should not silently vary by browser.

**⚠️ Conflict identified between two TS baseline documents (not silently reconciled):** TS `AE-TP-001` §8 ("Test Environment") states browsers as **"Chrome, Firefox, Edge."** TS `AE-FA-001` §"Browsers" states **"Chromium, Firefox, WebKit as supported by Playwright. Edge can be added through channel configuration."** These two TS documents disagree with each other on the third browser (Edge vs. WebKit as the baseline third engine). This Test Plan follows **`AE-FA-001`'s framing** (Chromium/Firefox/WebKit as the native Playwright trio, Edge as an optional channel addition) because it is corroborated by direct, Priority-1 artifact-level evidence: the TS project's own `package.json` defines `test:chromium`, `test:firefox`, and `test:webkit` scripts, with no `test:edge` script present. This is a **documented deviation from `AE-TP-001`**, not a silent correction — the QA Lead should confirm this interpretation is acceptable.

**No execution has occurred yet.** This section states planned coverage only.

## 12. Test Data Management

High-level categories only, per [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 9 (Test Data Requirements) — detailed Test Data Design remains Step 8:

- Valid users (pre-existing, reusable)
- Invalid users (deliberately incorrect credentials)
- New/dynamic users (unique per run, for registration/cleanup flows)
- Existing users (for duplicate-registration negative testing)
- Product data (identifiers, names, categories, brands, prices)
- Search data (matching keyword, non-matching keyword, missing-parameter case)
- Cart data (quantities, totals)
- Checkout data (order comments, dummy payment details — no real payment data, ever)
- Contact form data (name, email, subject, message, sample upload file)
- Subscription data (email address)
- API payloads — positive, for all documented request shapes
- API payloads — negative (missing parameters, invalid values, unsupported methods)

No detailed data values, files, or naming conventions are defined here.

## 13. Test Data Isolation

- **Public shared environment:** All test data is created against the single live, publicly shared instance ([02-Application-Analysis.md](02-Application-Analysis.md) Section 14) — there is no isolated per-run environment.
- **Account/data collision:** New-user tests must use uniquely generated identifiers (e.g., timestamped emails) to avoid collision with other users of the same public practice site, consistent with TS baseline discipline (AE-TDD-001 §5).
- **State mutation:** `createAccount`/`updateAccount`/`deleteAccount` and cart/order actions mutate real, shared backend state (REQ-API-011–013; [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11).
- **Cleanup:** Any account created for testing must be deleted (via UI or `deleteAccount` API) as part of the same test's teardown wherever practical, to avoid accumulating orphaned data on a shared public system.
- **Dynamic data:** Search keywords, product IDs, and category mappings may shift if the site's demo catalog changes without notice ([03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11, "Demo/public data may change or reset").
- **Repeatability:** Because the environment is shared and not fully under this project's control, 100% deterministic repeatability across all runs cannot be guaranteed — this is a **known limitation**, not a defect of the test design.

## 14. Entry Criteria

**Documentation entry criteria (for this Test Plan itself to be actionable):**
- Steps 1–3 (Project Vision, Application Analysis, Requirement Analysis) approved by the QA Lead.
- This Test Plan reviewed and approved.

**Execution entry criteria (before any actual test execution begins, in later phases):**
- Test Strategy (Step 5), Test Scenario Design (Step 6), Test Case Design (Step 7), and Test Data Design (Step 8) completed and approved.
- Automation Scope (Step 9) formally decided.
- Framework Architecture (Step 11) and initial framework setup (Phase 6/7) completed to the point that tests can actually run.
- Target application (`automationexercise.com`) confirmed reachable at execution time.
- Required test data (accounts, product references) prepared per the eventual Test Data Design.

No execution entry criterion is claimed as already met by this document.

## 15. Exit Criteria

- All test cases planned for the approved automation scope (once Step 9 finalizes it) have been executed at least once.
- All Critical- and High-priority requirements from [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 13 have either passing evidence or a documented, QA-Lead-accepted exception.
- No unresolved Blocker- or Critical-severity defect exists without documented QA Lead acceptance (Section 16).
- Regression pass completed for the discovery/cart modules identified as stable in Step 3.
- Test results, defects, and a Test Summary Report (a later-phase deliverable) have been reviewed by the QA Lead.

This Test Plan does **not** set a "zero defects" exit bar — it requires documented resolution or accepted risk, consistent with realistic QA practice on a public demo application with known environmental limitations.

## 16. Defect Management

| Stage | Description |
|---|---|
| Identification | A defect is any observed deviation from a documented REQ-FUNC-*/REQ-API-* requirement or from application behavior VERIFIED in Step 2, discovered during planned test execution. |
| Severity | Blocker / Critical / Major / Minor / Trivial — assigned by business impact (e.g., a broken checkout gate is Critical; a cosmetic footer issue is Trivial). |
| Priority | Urgent / High / Medium / Low — assigned by how soon it must be addressed relative to release/portfolio timelines. |
| Reproduction | Each defect must include exact reproduction steps, expected vs. actual result, and the requirement ID it violates. |
| Evidence | Screenshots, trace files, request/response logs (for API defects), and console output where relevant (Section 21). |
| Tracking | Defects tracked in a lightweight, project-appropriate log (mechanism to be decided at Phase 13 — Defect Management; not finalized here). |
| Retest | Fixes (application-side, where the AUT is public and out of this project's control, or test-design-side, where the issue is in our own test logic) are retested before closure. |
| Closure | A defect is closed only with retest evidence attached. |
| Regression Verification | Closed defects are candidates for inclusion in the regression set to catch recurrence. |

**Important distinction:** because Automation Exercise is a third-party public demo application, most "defects" this project can act on are **test-design defects** (wrong assumption, brittle locator, incorrect expected value) rather than application bugs we can get fixed. Genuine AUT behavior anomalies (e.g., the unexplained search-match case from Step 2) will be documented as **observations**, not filed as fixable defects, since there is no channel to remediate third-party application code.

## 17. Risk Management

Carried forward from [02-Application-Analysis.md](02-Application-Analysis.md) Section 13 and [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Sections 5/11, plus TS AE-AA-001 §8 / AE-AS-001 §9 (Priority 1) for structure.

| Risk | Impact | Likelihood | Mitigation | Contingency |
|---|---|---|---|---|
| Single shared public environment (no staging) | Test runs affect real shared data; unrelated third-party activity could affect results | Medium | Minimize state-mutating operations; use disposable, uniquely-identified data | Document affected runs as environment-related, not framework defects |
| Account/API state mutation (`createAccount`/`deleteAccount`/`updateAccount`) | Orphaned or colliding data on a shared public system | Medium | Cleanup in test teardown; unique data generation | Manual cleanup pass if automated cleanup fails |
| Checkout/payment behavior still largely unverified (Section 5 traceability gap) | Test design for Checkout may be based on incorrect assumptions until directly verified | High (currently) | Prioritize direct verification of Checkout/Order/Invoice flow early in Test Design/Execution | Re-scope Checkout test cases if actual behavior differs from TS-baseline reference |
| Demo site availability/stability | Test failures may reflect environment issues, not framework or application defects | Medium | Retry strategy (framework-level, decided at Step 11), clear failure categorization | Re-run before filing; note environment flakiness separately from defects |
| Dynamic/changing demo catalog data | Hard-coded product IDs, categories, or prices could become stale | Low–Medium | Prefer data retrieved at runtime (e.g., via API) over hard-coded IDs where practical | Refresh test data references if catalog changes are detected |
| Cross-browser behavioral differences | A flow verified in one engine may not hold in another | Medium | Cross-browser execution per Section 11 | Track browser-specific defects separately; do not assume Chromium-only results generalize |
| Automation flakiness (synchronization, e.g., the AJAX cart-removal behavior noted in Step 2) | Intermittent false failures | Medium | Explicit wait/assertion strategy for known-AJAX interactions (REQ-UI-005) | Quarantine and investigate flaky tests rather than silently retrying indefinitely |
| Unverified requirements presented as REFERENCE only (16 of 48, per Step 3 Section 14) | Test design risk if reference assumptions turn out to be wrong | Medium–High | Direct verification prioritized in Test Design/Execution phases | Update Requirement Analysis (Step 3) if verification contradicts current reference data |

No risk above is invented outside what Steps 2–3 or the TS baseline already documented.

## 18. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| QA Lead | Owns scope, quality decisions, document approvals, risk acceptance, and any release recommendation. Final authority on all items in this plan. |
| Senior QA Engineer | Test strategy input, test design review, defect triage judgment (role to be staffed as the project proceeds). |
| Test Automation Engineer | Framework implementation, automated test development, CI/CD and Docker execution setup (later phases). |
| AI Assistant (this session) | Documentation drafting, analysis support, and — once explicitly authorized — implementation assistance. Does **not** independently decide scope, accept risk, or approve documents; all such decisions remain with the QA Lead, consistent with [01-Project-Vision.md](01-Project-Vision.md) Section 19 (Governance). |

## 19. Test Deliverables

Planned only — none of the following exist yet beyond what is explicitly marked complete:

| Deliverable | Status |
|---|---|
| Project Vision | ✅ Complete (Step 1) |
| Application Analysis | ✅ Complete (Step 2) |
| Requirement Analysis | ✅ Complete (Step 3) |
| Test Plan (this document) | 🔶 Draft, pending approval (Step 4) |
| Test Strategy | Planned (Step 5) |
| Test Scenarios | Planned (Step 6) |
| Test Cases | Planned (Step 7) |
| Test Data | Planned (Step 8) |
| Automation Scope | Planned (Step 9) |
| Automation Strategy | Planned (Step 10) |
| Framework Architecture | Planned (Step 11) |
| Automated Tests (UI/API/Hybrid) | Planned (Phases 6–10) |
| Test Execution Results | Planned (Phase 12) |
| Defect Report | Planned (Phase 13) |
| CI/CD Evidence | Planned (Phase 14) |
| Docker Execution Evidence | Planned (Phase 6/14, alongside CI/CD) |
| QA Metrics | Planned (Phase 16) |
| Test Summary Report | Planned (Phase 17) |
| Release Readiness Report | Planned (Phase 18) |

## 20. Test Execution Approach

Planned modes — none executed yet:

- **Local execution** — headed (visual debugging) and headless (routine runs).
- **Smoke execution** — a fast subset covering Home/navigation/core-page availability.
- **Regression execution** — the broader, stable discovery/cart-focused set.
- **Tagged/filtered execution** — running a subset by module, priority, or test type (mechanism decided at Step 11).
- **Cross-browser execution** — Chromium, Firefox, WebKit (Section 11).
- **Docker execution** — via a reproducible container image (Section 23).
- **CI/CD execution** — triggered automatically on relevant events (Section 22).

No claim of successful execution is made anywhere in this document.

## 21. Reporting

High-level expectations only — implementation mechanism is a Step 11 (Framework Architecture) decision:

- Clear pass/fail summary per run, with counts by module/type.
- Failure diagnostics sufficient to reproduce without re-running blind: at minimum a screenshot at failure point; trace or video capture for UI failures where practical; request/response detail for API failures.
- Human-readable report output (HTML-based reporting, consistent with the TS baseline's approach, or an equivalent Python-ecosystem tool — the **specific tool is not finalized here**, only the expectation that one will exist).
- Console/log output retained for troubleshooting.
- Report artifacts retained per CI/CD run (Section 22).

## 22. CI/CD

**Planned role of CI/CD** (not implemented in this step):
- Automated execution of the test suite on relevant triggers (e.g., push, pull request, manual trigger — exact trigger policy is a later decision).
- Execution of the regression set on a defined cadence.
- Automatic generation and retention of test reports as pipeline artifacts.
- Visibility of failures to the QA Lead/contributor without requiring local re-execution.
- A CI provider is expected (GitHub Actions is the TS baseline's proven choice and a reasonable starting assumption for continuity — REFERENCE, TS AE-TP-001 §9, TS AE-FA-001 §14 — but the final choice remains a Phase 14 decision, not locked here).

No CI/CD configuration file is created in this step.

## 23. Docker

Docker **is** included as a planned execution capability, per instruction, with the following intended role:

- **Reproducible test environment:** eliminate "works on my machine" variance by pinning the OS/browser/runtime environment inside a container image.
- **Consistent browser/runtime environment:** align local, CI, and any future execution to the same underlying image rather than relying on each machine's own installed browser/Python versions.
- **Local execution:** a documented, one-command way to run the suite without manual environment setup.
- **CI execution:** the same image (or an equivalent) used in CI/CD, so CI and local results are directly comparable.
- **Dependency isolation:** avoid polluting the host machine with test-only dependencies and browser binaries.

**Reference precedent (Priority 1, not copied):** the TS baseline project already implements this pattern — a `Dockerfile` based on the official Playwright base image, with `npm ci` for dependency installation and a default command running the Chromium suite. This confirms containerized execution is a proven, achievable pattern for this application and this class of framework; the Python project's own Docker approach (base image, dependency manager, default command) is a **Step 11/implementation-phase decision**, not made here.

No Docker file is created in this step.

## 24. Constraints and Limitations

Carried forward only from Steps 2–3 — nothing new invented:

- **Constraint:** No dedicated staging/private environment exists; all testing targets the single shared public instance ([02-Application-Analysis.md](02-Application-Analysis.md) Section 14).
- **Constraint:** No database or backend log access — all evidence must be UI- or API-visible ([03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 11).
- **Constraint:** This project may not unilaterally create accounts or authenticate with credentials outside an explicitly QA-Lead-directed, appropriately scoped execution step (operating boundary noted throughout Steps 2–3).
- **Limitation:** Checkout/payment/order/invoice behavior remains largely unverified by this project as of this Test Plan (Section 17 risk) — test design for this area carries elevated uncertainty until directly executed.
- **Limitation:** No API versioning, rate-limiting, or authentication-token scheme is documented for the AUT's API surface ([02-Application-Analysis.md](02-Application-Analysis.md) Section 10).
- **Limitation:** Demo/public data (products, categories) may change or reset without notice.
- **Limitation:** Payment gateway behavior cannot be fully validated — it is a simulated/demo flow, not real payment processing.

These are documented as limitations to plan around, **not** restated as testable requirements.

## 25. Assumptions

Carried forward from [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 10, relevant to test planning:

- **ASSUMPTION:** The Automation Exercise application remains publicly accessible and behaviorally stable for the duration of this project.
- **ASSUMPTION:** The application's published `/api/*` endpoints remain available and behave as documented on `/api_list`.
- **ASSUMPTION:** Disposable test accounts can be created and deleted via the UI and/or `createAccount`/`deleteAccount` APIs once execution activities begin — not yet exercised by this project.
- **ASSUMPTION:** The checkout/payment/order/invoice flow behaves as documented in the TS baseline (address confirmation → order review → simulated payment → confirmation → invoice download) — carried forward, not verified.
- **ASSUMPTION:** Payment is fully simulated with no real financial processing.
- **ASSUMPTION:** A CI provider equivalent to GitHub Actions and a container runtime (Docker) will be available in the execution environment when Phases 6/14 are reached.

## 26. Test Completion / Acceptance

The planned test cycle is considered complete when:
- All test cases in the approved automation scope (per the eventual Step 9 decision) have executed at least once with recorded results.
- Every Critical/High-priority requirement in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 13 has either verified-passing evidence or a QA-Lead-accepted documented exception.
- All identified defects are logged with severity/priority and either resolved, retested, or explicitly accepted as known limitations by the QA Lead.
- A Test Summary Report (Phase 17 deliverable) has been produced and reviewed.
- The QA Lead has explicitly signed off that the cycle's evidence is sufficient for its stated portfolio/demonstration purpose — not that the application is defect-free.

## 27. Traceability

High-level mapping only — detailed test-case-level traceability belongs to Steps 6–7.

| Requirement Category (Step 3) | Test Scope (Section 4/5) | Test Type (Section 7) | Planned Execution (Section 20) |
|---|---|---|---|
| REQ-BUS-* (5) | Application areas in scope, holistically | Functional, E2E | Regression + smoke |
| REQ-FUNC-* (34) | Home, Signup/Login, Products, Cart, Checkout, Contact Us | Functional, UI, Negative, Boundary | Smoke (Home/nav) + Regression (all modules) |
| REQ-API-* (14) | All documented `/api/*` endpoints | API, Negative | API suite, tagged execution |
| REQ-UI-* (8) | Automation-facing UI behavior (locators, deterministic messages, AJAX handling) | UI, Cross-browser, Reliability | Cross-browser suite |
| REQ-E2E-* (3) | Hybrid opportunities (currently reference/proposed) | Hybrid E2E | Future scope — not yet in planned execution |
| REQ-NFR-APP-* (2) | Application availability/stability (observational) | N/A — monitored, not tested | N/A |
| REQ-NFR-AUTO-* (6) | Framework-level goals (cross-browser, CI/CD, reporting, maintainability, repeatability, Docker) | Cross-browser, Reliability | CI/CD + Docker execution |

Full requirement-by-requirement traceability already exists in [03-Requirement-Analysis.md](03-Requirement-Analysis.md) Section 8 and is not duplicated here.

## 28. Test Plan Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 4 Exit Checklist

- [x] Previous TypeScript Test Plan and related QA documents reviewed (Section 1, Section 11 conflict callout)
- [x] Current Requirement Analysis reviewed and used as primary basis (throughout)
- [x] Step 2 risks/limitations carried forward (Sections 17, 24)
- [x] 24 UI + 8 API (32-test) baseline referenced and left unchanged (Section 9)
- [x] Docker included as a planned capability, not implemented (Section 23)
- [x] CI/CD included as a planned capability, not implemented (Section 22)
- [x] No framework/library implementation decisions locked prematurely (Sections 8, 10, 21, 22, 23 explicitly defer to later steps)
- [x] Assumptions explicitly labeled (Section 25)
- [x] Limitations explicitly labeled, not restated as requirements (Section 24)
- [x] Entry and exit criteria are measurable and realistic, no "zero defects" bar (Sections 14–15)
- [x] No unsupported application requirements invented (all traced to Steps 2/3 or TS baseline)
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 5 — Test Strategy.
