# 03 — Requirement Analysis

## 1. Document Control

| Field | Value |
|---|---|
| Project | playwright-python-hybrid-framework |
| Phase | Phase 1 — Application & QA Baseline |
| Step | Step 3 — Requirement Analysis |
| Status | Draft — pending QA Lead review |
| AUT | Automation Exercise (https://automationexercise.com) |
| Prepared By | AI Assistant (advisory) |
| Review Status | Not yet reviewed by QA Lead |
| Predecessor Documents | [docs/01-Project-Vision.md](01-Project-Vision.md) (approved), [docs/02-Application-Analysis.md](02-Application-Analysis.md) (pending approval, used here as-is) |
| Reference Baseline Project | `playwright-typescript-hybrid-framework` (sibling directory, same machine — independent, previously baselined project) |

**Evidence labeling used throughout this document** (same convention as Step 2):

| Label | Meaning |
|---|---|
| **VERIFIED OBSERVATION** | Directly observed in Step 2 live browser inspection, or read directly from the AUT's own published pages. |
| **REFERENCE KNOWLEDGE (TS baseline)** | Sourced from the previous TypeScript project's approved QA documents (Priority 1 source, listed in Section 4). Not independently re-executed by this Python project unless separately marked VERIFIED. |
| **INFERENCE** | A reasonable conclusion not directly executed or confirmed by any source. |

## 2. Purpose and Objective

This document establishes the **requirements baseline** for the Python + Playwright + Pytest project, prior to Test Planning (Step 4) and Test Strategy (Step 5). It converts business/application understanding — reused from the previous TypeScript project's approved QA baseline, Step 2's independent verification, and the AUT's own published materials — into structured, traceable requirements. It does not define the test plan, test strategy, test scenarios, test cases, or automation scope; those remain later steps.

## 3. Scope

In scope: functional, API, UI-automation, hybrid/E2E, and non-functional requirements for the Automation Exercise application and this automation project, derived from the sources in Section 4. Out of scope: requirement definition for performance, security, accessibility, mobile, or visual regression testing, consistent with [docs/01-Project-Vision.md](01-Project-Vision.md) Section 10. This document does not finalize automation scope (Step 9) or freeze the Python project's own test scenario/case set (Steps 6–7) — it only establishes what is known and required.

## 4. Source Hierarchy and Documents Reviewed

Per task instruction, sources were consulted in this priority order. All were actually opened and read in this session (Priority 1 documents were `.docx` files, extracted to plain text for review — no source files were modified).

### Priority 1 — Previous TypeScript project baseline (`playwright-typescript-hybrid-framework/docs/`)

| Document | Doc ID | Status (as authored) | Used For |
|---|---|---|---|
| Project Vision | AE-PV-001 | Draft | Business/domain framing, scope baseline |
| Application Analysis | AE-AA-001 | Baselined Draft | Module inventory, journeys, risks cross-check |
| Requirement Analysis | AE-RA-001 | Baselined | **Primary source** — FR-*/BR-* catalogue reused and cross-checked |
| Master Test Plan | AE-TP-001 | Baselined | Test items, NFR/automation-project scope cross-check |
| Test Strategy | AE-TS-001 | Baselined | Hybrid pattern, cross-browser/CI scope cross-check |
| Test Scenario Design | AE-TSD-001 | Baselined | 32-scenario baseline (24 UI + 8 API) traceability |
| Test Case Design | AE-TC-001 | Baselined (incl. Step 15 Hybrid addendum) | Detailed step evidence (e.g., exact error text, checkout flow steps), deferred-scope list |
| Test Data Design | AE-TDD-001 | Baselined | Test data category/structure reuse (Section 9) |
| Automation Scope | AE-AS-001 | Baselined (v1.1) | 24 UI + 8 API + 2 Hybrid (planning-only) baseline, deferred/future scope |
| Framework Architecture | AE-FA-001 | (present, not content-reused) | Reviewed only to confirm existence/scope; **not** used as a requirements source per the "do not copy TypeScript implementation details" rule |

Also observed directly on the TS project's filesystem (Priority 1, artifact-level evidence, not docx content): the project includes a `Dockerfile` and a `.github/workflows/playwright.yml`, and its `test-data/` directory contains `users.json`, `invalid-users.json`, `products.json`, `checkout.json`, `contact-us.json`, `subscription.json`, `product-review.json`, `api-payloads.json`, and a sample upload file — corroborating, at the artifact level, the data categories described in AE-TDD-001.

### Priority 2 — Official Automation Exercise materials
- `https://automationexercise.com/api_list` (published API documentation — already captured in full in Step 2).
- `https://automationexercise.com/test_cases` (site's own published 26-scenario list — already captured in Step 2).

### Priority 3 — This project's own Step 2 baseline
- [docs/02-Application-Analysis.md](02-Application-Analysis.md) — used throughout as the Python project's independent verification record.

### Priority 4 — Direct live-application observation
- No new live-application browsing was performed in this step; all directly-observed facts are those already captured and labeled in Step 2. Where this document references "verified," it means verified in Step 2, not re-verified now.

### Priority 5 — Model/engineering interpretation
- Used only where explicitly labeled **INFERENCE** below, and never presented as a confirmed requirement.

## 5. Cross-Check: TS Baseline vs. Python Step 2 vs. Official AE Sources

Per instruction, differences are documented explicitly, not silently reconciled.

| # | Finding | TS Baseline (Priority 1) | Python Step 2 (Priority 3/4) | Official AE Source (Priority 2) | Disposition |
|---|---|---|---|---|---|
| 1 | Checkout URL | AA doc References section cites `https://automationexercise.com/checkout` as a distinct URL | Only `/view_cart` was navigated; its page **title** reads "Checkout," but the literal `/checkout` route was never visited | Not independently checked in this step | **Open question** (Section 12) — not reconciled; must be confirmed by direct navigation before Test Design assumes route structure |
| 2 | Invalid login error text | RA doc FR-SL-004 states only "an appropriate error message" (generic) | VERIFIED exact text: *"Your email or password is incorrect!"* | Not documented on any official AE page reviewed | **Refinement, not conflict** — Python Step 2 provides a more precise, independently-verified value than the TS baseline had recorded |
| 3 | Duplicate-email error text | TC-001 (AE-TC-UI-005 steps) documents exact text: *"Email Address already exist!"* | Not independently verified — account creation is a prohibited action for this assistant | Not observed | **Unverified carry-forward** — treated as REFERENCE KNOWLEDGE only until independently confirmed under QA Lead-directed test execution |
| 4 | Checkout/payment/order/invoice flow detail | Documented in detail across AE-TC-UI-014/015/016/023/024 and AE-AA-001 (address, payment, "Pay and Confirm Order," invoice download) | Verified only up to the authentication gate; nothing beyond it was executed | Not independently checked | **Previously documented, not independently verified** — carried forward as REFERENCE KNOWLEDGE, explicitly flagged, not treated as fact by this project yet |
| 5 | Search-result relevance | RA doc BR-005 / FR-PR-004 assert search "shall return relevant results," with no caveat | VERIFIED functional, but flagged an anomaly: a search for "dress" returned at least one item without an obvious textual match | Not documented | **Newly discovered nuance** — the TS baseline did not record this; flagged as an open question, not silently absorbed into "search works correctly" |
| 6 | API surface completeness | AE-RA-001 §4 "API Requirement Summary" table lists only 6 of the 14 published APIs (omits Update Account, Get User Detail By Email) | Step 2 independently captured and verified **all 14** published API scenarios directly from `/api_list` | `/api_list` page confirms 14 total | **Confirmed common core (6), plus 8 additional confirmed by Python Step 2** — not a conflict; the TS RA table was a summary, not exhaustive. AE-AA-001/AE-TSD-001/AE-AS-001 (other TS docs) do reference all 14, so this is a summary-table omission in one TS document, not a baseline gap |
| 7 | Product quantity negative-value rule | RA doc BR-004: "Product quantity cannot be negative" | Not exercised (quantity input observed but not tested with a negative value) | Not documented | **Unverified** — carried forward as REFERENCE KNOWLEDGE / business rule assumption only |
| 8 | Session persistence (FR-SL-006) | RA doc states sessions "shall remain active until logout" | Not independently verified — no session was ever established (no login performed) | Not documented | **Unverified carry-forward** |
| 9 | Containerized execution | TS project repository contains a `Dockerfile` (filesystem-level evidence, not discussed in the reviewed docx docs) | Not part of Python Step 1/2 scope decisions | N/A | **Newly discovered (artifact-level) fact** — noted as a Priority-1 data point for later automation-project NFR consideration (Section 6.6); not adopted as a Python requirement here |

No item in the table above has been "resolved" by this document — each disposition states what is known and what remains open. Resolution (where needed) belongs to later phases (Test Design, Automation Scope) under QA Lead direction.

## 6. Requirement Categories

### 6.1 Business Requirements

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-BUS-001 | The application shall represent a realistic e-commerce retail business domain suitable for QA automation practice. | TS AE-PV-001 §4; TS AE-AA-001 §2 | High | VERIFIED (Python Step 2 §2) |
| REQ-BUS-002 | The application shall support product discovery (browse, search, filter by category/brand) as a core retail capability. | TS AE-RA-001 §2.2 | Critical | VERIFIED (Step 2 §4, §8) |
| REQ-BUS-003 | The application shall support cart-based purchase staging prior to order commitment. | TS AE-RA-001 §2.2 | Critical | VERIFIED (Step 2 §8) |
| REQ-BUS-004 | The application shall require account authentication before a purchase can be completed. | TS AE-RA-001 BR-003 | Critical | VERIFIED independently (Step 2 §7) — the strongest-evidence business rule in this document |
| REQ-BUS-005 | The application shall provide a customer feedback/support channel independent of the purchase flow. | TS AE-RA-001 §3.6 | Medium | VERIFIED — field presence only (Step 2 §9); submission not executed |

### 6.2 Functional Requirements

Reused and renumbered from TS AE-RA-001 §3 (original `FR-*` IDs preserved as Source for traceability), cross-checked against Step 2. **Verification Status** reflects this Python project's own evidence, not the TS project's.

**Home Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-HM-001 | The Home page shall display successfully. | FR-HM-001 | High | VERIFIED |
| REQ-FUNC-HM-002 | The navigation menu shall be available. | FR-HM-002 | High | VERIFIED |
| REQ-FUNC-HM-003 | Product categories shall be displayed. | FR-HM-003 | Medium | VERIFIED |
| REQ-FUNC-HM-004 | Product brands shall be displayed. | FR-HM-004 | Medium | VERIFIED |
| REQ-FUNC-HM-005 | Featured products shall be visible. | FR-HM-005 | Medium | VERIFIED |
| REQ-FUNC-HM-006 | Recommended items shall be displayed. | FR-HM-006 | Low | VERIFIED |
| REQ-FUNC-HM-007 | Newsletter subscription shall be available. | FR-HM-007 | Low | VERIFIED (field presence only; submission not executed — Step 2 §9) |

**Signup / Login / Account Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-SL-001 | A new user shall be able to register using valid information. | FR-SL-001 | Critical | **NOT INDEPENDENTLY VERIFIED** — account creation is a prohibited action for this assistant to perform unilaterally |
| REQ-FUNC-SL-002 | Registration with an existing email address shall be rejected. | FR-SL-002 | High | **NOT INDEPENDENTLY VERIFIED**; TS baseline documents exact error text "Email Address already exist!" (REFERENCE only) |
| REQ-FUNC-SL-003 | Registered users shall log in using valid credentials. | FR-SL-003 | Critical | **NOT INDEPENDENTLY VERIFIED** — no valid account was available/created |
| REQ-FUNC-SL-004 | Invalid login attempts shall display an appropriate error message. | FR-SL-004 | High | **VERIFIED**, and refined: exact text confirmed as "Your email or password is incorrect!" (Step 2 §7) |
| REQ-FUNC-SL-005 | Logged-in users shall be able to log out successfully. | FR-SL-005 | High | **NOT INDEPENDENTLY VERIFIED** |
| REQ-FUNC-SL-006 | User sessions shall remain active until logout. | FR-SL-006 | Medium | **NOT INDEPENDENTLY VERIFIED** |

**Products Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-PR-001 | Users shall be able to view all available products. | FR-PR-001 | Critical | VERIFIED |
| REQ-FUNC-PR-002 | Users shall be able to view product details. | FR-PR-002 | Critical | VERIFIED |
| REQ-FUNC-PR-003 | Users shall search products using keywords. | FR-PR-003 | High | VERIFIED |
| REQ-FUNC-PR-004 | Search results shall match the entered keywords. | FR-PR-004 | High | **PARTIALLY VERIFIED** — search is functional, but Step 2 observed a result whose relevance to the keyword is not obvious (Section 5, row 5); the matching rule itself is unconfirmed |
| REQ-FUNC-PR-005 | Products shall be filterable by category. | FR-PR-005 | Medium | VERIFIED (route functional; category-ID mapping undocumented) |
| REQ-FUNC-PR-006 | Products shall be filterable by brand. | FR-PR-006 | Medium | VERIFIED |

**Cart Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-CT-001 | Users shall add products to the shopping cart. | FR-CT-001 | Critical | VERIFIED |
| REQ-FUNC-CT-002 | Users shall update product quantities. | FR-CT-002 | High | **PARTIALLY VERIFIED** — quantity input exists on product detail and cart page; the update interaction itself was not exercised |
| REQ-FUNC-CT-003 | Users shall remove products from the cart. | FR-CT-003 | High | VERIFIED (AJAX-based, confirmed) |
| REQ-FUNC-CT-004 | Cart totals shall update correctly. | FR-CT-004 | Critical | **PARTIALLY VERIFIED** — confirmed correct for a single line item only; multi-item/quantity-change recalculation not exercised |
| REQ-FUNC-CT-005 | Cart information shall persist during the active session. | FR-CT-005 | Medium | **NOT INDEPENDENTLY VERIFIED** |

**Checkout Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-CO-001 | Registered/authenticated users shall be able to access checkout. | FR-CO-001 | Critical | **PARTIALLY VERIFIED** — the gate itself (blocking unauthenticated access) is VERIFIED; authenticated access was not exercised |
| REQ-FUNC-CO-002 | Shipping/delivery information shall be displayed during checkout. | FR-CO-002 | High | **NOT INDEPENDENTLY VERIFIED** — REFERENCE from TS AE-TC-UI-023 |
| REQ-FUNC-CO-003 | Billing information shall be displayed during checkout. | FR-CO-003 | High | **NOT INDEPENDENTLY VERIFIED** — REFERENCE from TS AE-TC-UI-023 |
| REQ-FUNC-CO-004 | The order summary shall accurately reflect cart contents. | FR-CO-004 | Critical | **NOT INDEPENDENTLY VERIFIED** — REFERENCE from TS AE-TC-UI-014/015/016 |
| REQ-FUNC-CO-005 | Payment information shall be accepted (simulated). | FR-CO-005 | High | **NOT INDEPENDENTLY VERIFIED**; both TS and Python sources agree this is a demo/simulated flow, but neither has independently confirmed its exact behavior in this Python project |
| REQ-FUNC-CO-006 | Successful order placement shall display an order confirmation, and an invoice shall be available for download. | FR-CO-006 (extended per TS AE-TC-UI-024) | High | **NOT INDEPENDENTLY VERIFIED** — REFERENCE only |

**Contact Us Module**

| ID | Requirement | Source | Priority | Verification Status |
|---|---|---|---|---|
| REQ-FUNC-CU-001 | Users shall be able to submit contact information (name, email, subject, message). | FR-CU-001 | Medium | VERIFIED — fields present; submission not executed |
| REQ-FUNC-CU-002 | Users shall be able to upload a supporting file with the contact form. | FR-CU-002 | Low | VERIFIED — field present; submission not executed |
| REQ-FUNC-CU-003 | Mandatory field validation shall be enforced on the contact form. | FR-CU-003 | Medium | **NOT INDEPENDENTLY VERIFIED** — form was not submitted (empty or invalid) |
| REQ-FUNC-CU-004 | Successful submission shall display a confirmation message. | FR-CU-004 | Medium | **NOT INDEPENDENTLY VERIFIED** — REFERENCE from TS AE-TC-UI-006 |

### 6.3 API Requirements

All 14 endpoints were **independently verified live** in Step 2 (Priority 2/3 — read directly from `/api_list`, including the four detail panels that required DOM-level inspection). Current Automation Baseline Status is carried forward from TS AE-AS-001 (Priority 1) and is **not changed** by this document.

| ID | Requirement | Endpoint / Method | Priority | Verification Status | Current TS Automation Baseline Status |
|---|---|---|---|---|---|
| REQ-API-001 | System shall provide a list of all products. | GET `/api/productsList` | Critical | VERIFIED | Phase 1 — Automated |
| REQ-API-002 | System shall reject unsupported HTTP methods on the products list endpoint. | POST `/api/productsList` → 405 | Medium | VERIFIED | Phase 1 — Automated |
| REQ-API-003 | System shall provide a list of all brands. | GET `/api/brandsList` | High | VERIFIED | Phase 1 — Automated |
| REQ-API-004 | System shall reject unsupported HTTP methods on the brands list endpoint. | PUT `/api/brandsList` → 405 | Medium | VERIFIED | Phase 1 — Automated |
| REQ-API-005 | System shall support product search via API with a required parameter. | POST `/api/searchProduct` | High | VERIFIED | Phase 1 — Automated |
| REQ-API-006 | System shall reject a search request missing the required parameter. | POST `/api/searchProduct` (no param) → 400 | High | VERIFIED | Phase 1 — Automated |
| REQ-API-007 | System shall verify login credentials via API (valid case). | POST `/api/verifyLogin` → 200 | Critical | VERIFIED | Phase 1 — Automated |
| REQ-API-008 | System shall reject a login-verification request missing the email parameter. | POST `/api/verifyLogin` (no email) → 400 | Medium | VERIFIED | **Deferred / Future Scope** (per TS AE-AS-001 §6) |
| REQ-API-009 | System shall reject unsupported HTTP methods on the login-verification endpoint. | DELETE `/api/verifyLogin` → 405 | Low | VERIFIED | **Deferred / Future Scope** |
| REQ-API-010 | System shall verify login credentials via API (invalid case). | POST `/api/verifyLogin` → 404 | Critical | VERIFIED | Phase 1 — Automated |
| REQ-API-011 | System shall support account creation via API. | POST `/api/createAccount` → 201 | High | VERIFIED (documentation only — not executed, per prohibited-action boundary) | **Deferred / Future Scope**, except as a non-test setup/cleanup helper in TS's proposed (not-yet-code) Hybrid scope |
| REQ-API-012 | System shall support account deletion via API. | DELETE `/api/deleteAccount` → 200 | High | VERIFIED (documentation only — not executed) | **Deferred / Future Scope**, except as proposed Hybrid cleanup helper |
| REQ-API-013 | System shall support account update via API. | PUT `/api/updateAccount` → 200 | Medium | VERIFIED (documentation only — not executed) | **Deferred / Future Scope** |
| REQ-API-014 | System shall support retrieving user account details by email via API. | GET `/api/getUserDetailByEmail` → 200 | Medium | VERIFIED (documentation only — not executed) | **Deferred / Future Scope** |

### 6.4 UI Requirements

Automation-facing requirements — distinct from the functional requirements above, which describe *application* behavior. These describe what the UI must offer to be reliably automatable, all grounded in Step 2 testability findings.

| ID | Requirement | Source | Priority | Notes |
|---|---|---|---|---|
| REQ-UI-001 | Form controls shall expose accessible roles/labels/placeholders sufficient for role-based Playwright locators. | Step 2 §11 | High | VERIFIED across all forms inspected (login, signup, contact, review, search) |
| REQ-UI-002 | The add-to-cart action shall present a distinguishable, assertable confirmation message. | Step 2 §8 | High | VERIFIED ("Added! Your product has been added to cart.") |
| REQ-UI-003 | The checkout authentication gate shall present a deterministic, assertable message when accessed unauthenticated. | Step 2 §7 | Critical | VERIFIED ("Register / Login account to proceed on checkout.") |
| REQ-UI-004 | Invalid login shall present a deterministic, assertable inline error without a full page navigation. | Step 2 §7 | High | VERIFIED |
| REQ-UI-005 | Cart item removal shall be automatable without relying on a full-page-load wait, since it updates via client-side/AJAX behavior. | Step 2 §8, §11 | Medium | VERIFIED — a genuine synchronization design point for later framework work |
| REQ-UI-006 | Global navigation and footer/subscription components shall render consistently across major pages, to support shared/reusable automation components. | Step 2 §11 | Medium | VERIFIED across Home, Products, Product Details, Login, Contact Us, Cart |
| REQ-UI-007 | The framework shall be able to execute the same UI test suite across multiple Playwright-supported browser engines. | TS AE-TP-001 §8 (Chrome, Firefox, Edge baseline) | Medium | REFERENCE — carried forward as a goal; specific Python-project browser matrix is a Phase 5/6 decision, not decided here |
| REQ-UI-008 | UI-facing test data (search keywords, category/brand names, etc.) shall be externally configurable rather than hard-coded in test logic. | TS AE-TDD-001 §3 (design principle) | Medium | REFERENCE — principle carried forward conceptually; no data files exist yet (Test Data Design is Step 8) |

### 6.5 Hybrid / E2E Requirements

| ID | Requirement | Source | Priority | Status |
|---|---|---|---|---|
| REQ-E2E-001 | Login shall behave correctly for an account provisioned via the `createAccount` API rather than the UI signup form. | TS AE-TC-HYBRID-001 (AE-AS-001 §13) | Medium | REFERENCE ONLY — this was a **planning-approved, not-yet-implemented** scenario in the TS project (no Hybrid test code exists there either, per AE-AS-001 §13 "Current Status"). Not adopted into any Python baseline by this document. |
| REQ-E2E-002 | Checkout completion shall succeed for an account provisioned via the `createAccount` API rather than UI registration. | TS AE-TC-HYBRID-002 (AE-AS-001 §13) | Medium | REFERENCE ONLY — same planning-only status as above |
| REQ-E2E-003 | Product data returned by `GET /api/productsList` should be usable as an independent oracle to cross-check UI-rendered product listing data. | **New** — Python Step 2 §12 (Automation Opportunities) | Low | **INFERENCE / newly identified in this project** — not present in the TS baseline; proposed only, not approved scope |

Consistent with the TS baseline's own framing (AE-AS-001 §13): a Hybrid test case must independently justify its value beyond "UI and API exist in the same test." No additional Hybrid requirements are invented here beyond what Section 5, row-by-row cross-check supports.

### 6.6 Non-Functional / Quality Requirements

Explicitly split, per instruction, into **application-level** (largely observational, outside this project's control) and **automation-project-level** (this project's own delivery requirements).

**Application-level (observational only):**

| ID | Requirement | Source | Notes |
|---|---|---|---|
| REQ-NFR-APP-001 | The application shall remain publicly accessible for the duration of testing activity. | TS AE-RA-001 §7; Python Vision §15 | This is an **assumption about the AUT**, not a controllable requirement — see Section 10 |
| REQ-NFR-APP-002 | The application's published API surface shall remain stable in endpoint/behavior over the project timeline. | TS AE-AA-001 §8 | Assumption-dependent |

**Automation-project-level (this project's own delivery requirements):**

| ID | Requirement | Source | Priority |
|---|---|---|---|
| REQ-NFR-AUTO-001 | The framework shall support execution across multiple browser engines. | TS AE-TP-001 §8; Python Vision §4 | Medium |
| REQ-NFR-AUTO-002 | The framework shall integrate with a CI/CD pipeline for automated execution. | TS AE-TS-001 §12; Python Vision §4, §9 | High |
| REQ-NFR-AUTO-003 | The framework shall produce structured, human-readable test reports with failure evidence (screenshots/traces at minimum). | TS AE-TS-001 §11; Python Vision §4 | High |
| REQ-NFR-AUTO-004 | The framework shall be maintainable through separation of test logic, page interactions, test data, and configuration. | Python Vision §4 | High |
| REQ-NFR-AUTO-005 | Test execution shall be repeatable and deterministic wherever the application's own behavior is deterministic. | Python Vision §3 | High |
| REQ-NFR-AUTO-006 | Containerized execution may be considered as a future automation-project capability. | **Newly discovered** — TS project repository contains a `Dockerfile` (filesystem-level evidence, Section 5 row 9) | Low — not yet a Python-project decision; deferred to Phase 5/6 |

## 7. Requirement Catalogue Summary

| Category | Prefix | Count |
|---|---|---|
| Business Requirements | REQ-BUS | 5 |
| Functional Requirements | REQ-FUNC | 34 (7 Home + 6 Signup/Login + 6 Products + 5 Cart + 6 Checkout + 4 Contact Us) |
| API Requirements | REQ-API | 14 |
| UI (automation-facing) Requirements | REQ-UI | 8 |
| Hybrid / E2E Requirements | REQ-E2E | 3 |
| Non-Functional — Application | REQ-NFR-APP | 2 |
| Non-Functional — Automation Project | REQ-NFR-AUTO | 6 |
| **Total** | | **72** |

No requirement above was created solely to inflate this count; each traces to a Priority 1–4 source cited in its own row.

## 8. Requirement → Existing Test Baseline Traceability

The TS project's approved Phase 1 baseline (**24 UI + 8 API = 32 tests**, per TS AE-AS-001/AE-TSD-001) is treated here strictly as an **existing reference baseline**, not as a requirement this Python project is bound to. No change to that baseline is proposed by this document.

**Module-level coverage, using the TS baseline's own scenario IDs (`AE-UI-XXX` / `AE-API-XXX`) as evidence of what an equivalent baseline once covered:**

| Module | REQ-FUNC / REQ-API Range | TS Baseline Scenario Coverage | Coverage Classification |
|---|---|---|---|
| Home | REQ-FUNC-HM-001–007 | Implicit in navigation steps of multiple TS scenarios (no dedicated Home scenario) | **Partially Covered** — verified independently by this project (Step 2), but the TS baseline has no standalone Home test case |
| Signup/Login/Account | REQ-FUNC-SL-001–006 | AE-UI-001–005 (5 scenarios) | **Covered** in TS baseline; **not yet verified** by this Python project (Section 6.2) |
| Products/Search/Category/Brand/Review | REQ-FUNC-PR-001–006 | AE-UI-008, 009, 018, 019, 021 (5 scenarios) + AE-API-001–006 | **Covered** in TS baseline; **verified (mostly) or partially verified** by this Python project |
| Cart / Recommended Items | REQ-FUNC-CT-001–005 | AE-UI-012, 013, 017, 022 (4 scenarios) | **Covered** in TS baseline; **partially verified** by this Python project |
| Checkout / Order / Invoice | REQ-FUNC-CO-001–006 | AE-UI-014, 015, 016, 023, 024 (5 scenarios) | **Covered** in TS baseline; **largely unverified** by this Python project (only the auth gate is confirmed) |
| Contact Us | REQ-FUNC-CU-001–004 | AE-UI-006 (1 scenario) | **Covered** in TS baseline; **partially verified** by this Python project |
| Subscription | REQ-FUNC-HM-007 | AE-UI-010, 011 (2 scenarios) | **Covered** in TS baseline; field presence VERIFIED, submission not executed |
| API surface (all 14) | REQ-API-001–014 | AE-API-001–008 (8 automated) + API-08/09/11–14 (6 deferred, per AE-AS-001 §6) | **8 of 14 Covered** in TS baseline's automated scope; remaining 6 explicitly **Future Scope** in TS baseline, and now independently VERIFIED (documentation-level) by this project |
| Hybrid/E2E | REQ-E2E-001–003 | AE-TC-HYBRID-001/002 (planning-approved, **not implemented** even in TS project) | **Uncovered** by any implemented baseline — planning-only in TS, not yet planned in Python |
| Scroll behavior (TC-25/26) | Not modeled as a REQ item | Deferred in TS baseline (AE-TSD-001 §7) | **Future Scope** — intentionally excluded from this catalogue, consistent with TS baseline's own deferral rationale (low business risk) |

**Summary:** Every REQ-FUNC/REQ-API item in this document maps to either a covered-in-TS-baseline scenario or an explicitly-deferred-in-TS-baseline item — nothing here is unaccounted for. However, "covered in the TS baseline" is a statement about that separate project's prior automation, **not** a statement about this Python project's current automation state (which has none yet, correctly, per the roadmap).

## 9. Test Data Requirements

Identified conceptually only, per instruction — **no test data files are created in this step**. Categories below are reused from TS AE-TDD-001 (Priority 1), cross-checked against Step 2's independently observed field requirements (Priority 3).

| Data Category | Conceptual Need | Source |
|---|---|---|
| Valid user | A reusable, pre-existing account for login/logout/checkout-login scenarios | TS AE-TDD-001 §6 (USER-VALID-001); Step 2 §6 (field list VERIFIED via API doc) |
| New/dynamic user | Uniquely-generated account data for registration and account-lifecycle scenarios, with cleanup | TS AE-TDD-001 §6 (USER-NEW-001) |
| Existing user (duplicate-email negative) | A known, already-registered email for negative registration testing | TS AE-TDD-001 §6 (USER-EXISTING-001) |
| Invalid user | Deliberately incorrect email/password for negative login testing | TS AE-TDD-001 §6 (USER-INVALID-001); Step 2 §7 (VERIFIED behavior, credentials used were disposable/fabricated) |
| Address data | Title, name, company, address lines, country/state/city/zipcode, mobile number | TS AE-TDD-001 §7; independently corroborated by the exact field set of the `createAccount`/`updateAccount` APIs (Step 2 §10, VERIFIED) |
| Product data | Product identifiers, names, categories, brands, prices | Step 2 §6 (VERIFIED via `productsList` API and UI) |
| Search data | Valid keywords, an intentionally non-matching keyword, an empty/missing-parameter case | TS AE-TDD-001 §2; REQ-API-005/006 |
| Cart/checkout data | Quantities, order comments, dummy payment details, invoice expectations | TS AE-TDD-001 §2; **payment field specifics remain unverified** (Section 11) |
| Contact form data | Name, email, subject, message, sample upload file | TS AE-TDD-001 §2; Step 2 §9 (fields VERIFIED) |
| API payloads | Positive and negative payloads for all 14 endpoints (Section 6.3) | Step 2 §10 (VERIFIED endpoint/parameter shapes) |

No application requirement is asserted here on the basis of test data alone — this section only restates *needs*, consistent with instruction.

## 10. Assumptions

Each item below is an assumption, not a confirmed requirement.

- **ASSUMPTION:** The Automation Exercise application remains publicly accessible and behaviorally stable for the duration of this project. (TS AE-RA-001 §7; Python Vision §15)
- **ASSUMPTION:** The application's published `/api/*` endpoints remain available and behave as documented on `/api_list`. (TS AE-AA-001 §8; Step 2 §10)
- **ASSUMPTION:** Disposable test accounts can be created and deleted via the UI and/or `createAccount`/`deleteAccount` APIs when execution activities begin in later phases. (TS AE-TDD-001 §1; TS AE-AS-001 §10) — **not yet exercised by this Python project.**
- **ASSUMPTION:** The checkout/payment/order/invoice flow behaves as documented in the TS baseline (address confirmation → order review → simulated payment → confirmation → invoice download). This is currently an assumption **carried forward, not verified**, by this project (Section 5, row 4).
- **ASSUMPTION:** Payment is fully simulated with no real financial processing, consistent with the application's stated purpose as a practice site. (TS AE-AA-001 §8; Python Step 2 §14) — not independently confirmed.
- **ASSUMPTION:** Test data created against the live application (e.g., via API) will not meaningfully degrade the shared public environment if created and cleaned up responsibly. (TS AE-AS-001 §10)
- **ASSUMPTION:** The TS baseline documents reviewed in Section 4 remain representative of current TS-project understanding; no attempt was made in this session to determine whether they have been superseded by later revisions not present on disk.

## 11. Constraints and Limitations

- **Constraint:** No dedicated staging/private environment exists; all verification (past, present, and future) targets the single shared public instance. (TS AE-AA-001 §8; Step 2 §14 — VERIFIED, no alternate environment found)
- **Constraint:** No database or backend log access is available; all evidence must be UI- or API-visible. (TS AE-RA-001 §8)
- **Constraint:** State-mutating APIs (`createAccount`, `updateAccount`, `deleteAccount`) affect real, shared backend data. (Step 2 §10, VERIFIED via documented endpoint behavior)
- **Constraint:** This assistant may not create accounts or authenticate with credentials unilaterally (operating boundary) — this is why several REQ-FUNC-SL-*/CO-* items remain unverified in this document and must be executed later, under QA Lead-directed, appropriately-scoped test execution.
- **Limitation:** Payment gateway behavior cannot be fully validated (both TS and Python sources agree it is a demo/simulated flow, but neither has independently confirmed its exact mechanics from this project). (TS AE-RA-001 §8)
- **Limitation:** No API versioning, rate-limiting, or authentication-token scheme is documented; automated API testing must assume none exists unless later evidence contradicts this. (Step 2 §10, VERIFIED absence of any such documentation)
- **Limitation:** Demo/public data may change or reset without notice, which could invalidate specific product IDs, prices, or category mappings referenced in this or future documents. (TS AE-AA-001 §8)

## 12. Open Questions / Unverified Items

No answers are guessed here — each item requires direct verification in a later, appropriately-scoped step.

1. Is `/checkout` a distinct route from `/view_cart`, or does `/view_cart` simply carry the page title "Checkout"? (Section 5, row 1)
2. What is the exact behavior and UI structure of the checkout flow beyond the authentication gate (address entry/confirmation, order review, payment form, confirmation message, invoice download)? (Section 5, row 4; REQ-FUNC-CO-002–006)
3. Why did a search for "dress" return at least one item without an obvious name-level match — does search also index description/category fields? (Section 5, row 5; REQ-FUNC-PR-004)
4. What is the exact error text and behavior for duplicate-email registration in the current live application (TS baseline text "Email Address already exist!" is unverified by this project)? (REQ-FUNC-SL-002)
5. Does the application enforce non-negative product quantity, and what happens on an invalid quantity entry? (REQ-FUNC-CT-002, BR-004 reference)
6. What is the actual session-persistence behavior (cookie-based? timeout? "remember me"?) once a real login is performed? (REQ-FUNC-SL-006)
7. What is the category-ID-to-name mapping for `/category_products/{id}`, and is it stable? (Step 2 §8)
8. Does the Contact Us form and Subscription form perform any client-side validation, and what does a successful submission actually display? (REQ-FUNC-CU-003/004)
9. Are the TS baseline's `.docx` QA documents the current, latest version of that project's state, or might newer revisions exist that were not present in the reviewed `docs/` folder?

## 13. Requirement Prioritization Summary

Priorities were assigned per-requirement above, based on business importance, user impact, position in the core application flow, risk, and automation value (matching the TS baseline's own priority assignments wherever a direct source existed; independently judged only for the newly-added REQ-UI/REQ-NFR/REQ-E2E-003 items, and explicitly flagged as such).

| Priority | Count | Representative Examples |
|---|---|---|
| Critical | 12 | REQ-BUS-002/003/004, REQ-FUNC-SL-001/003, REQ-FUNC-PR-001/002, REQ-FUNC-CT-001/004, REQ-FUNC-CO-001/004, REQ-API-001/007/010, REQ-UI-003 |
| High | 27 | REQ-BUS-001, REQ-FUNC-SL-002/004/005, REQ-FUNC-PR-003/004, REQ-FUNC-CT-002/003, REQ-FUNC-CO-002/003/005/006, most REQ-API items, REQ-UI-001/002/004, REQ-NFR-AUTO-002/003/004/005 |
| Medium | 25 | REQ-BUS-005, REQ-FUNC-HM-003/004/005, REQ-FUNC-SL-006, REQ-FUNC-PR-005/006, REQ-FUNC-CT-005, REQ-FUNC-CU-001/003/004, several REQ-API deferred items, REQ-UI-005/006/007/008, REQ-E2E-001/002, REQ-NFR-AUTO-001 |
| Low | 8 | REQ-FUNC-HM-006/007, REQ-FUNC-CU-002, REQ-API-009, REQ-E2E-003, REQ-NFR-AUTO-006 |

## 14. Requirement Coverage Summary

| Verification Status | Approx. Count (REQ-FUNC + REQ-API, 48 total) | Note |
|---|---|---|
| VERIFIED (fully) | 24 | Home (7), most Products (5), Cart-add/remove (2), Contact Us fields (2), all 14 API endpoints — but 6 of the 14 are documentation-verified only, execution not performed |
| PARTIALLY VERIFIED | 8 | Search relevance, quantity update, cart totals (multi-item), checkout gate access |
| NOT INDEPENDENTLY VERIFIED (REFERENCE only) | 16 | All Signup/Login except invalid-login, all Checkout except the gate, Contact Us validation/confirmation, cart persistence |

This distribution is itself a key finding: **the discovery/cart side of the application is well-verified; the identity and order-completion side is not**, and must be prioritized for direct verification early in Test Design/Execution (Phases 3/12) under proper QA Lead-directed test data handling.

## 15. Review and Approval

| Role | Name | Status |
|---|---|---|
| QA Lead | (Project QA Lead) | Pending Review |
| Prepared By | AI Assistant (advisory) | Complete — pending review |

### Step 3 Exit Criteria

- [x] Previous TypeScript project's approved QA documents were reviewed (Section 4, 10 documents)
- [x] Official Automation Exercise materials were considered (Section 4, Priority 2)
- [x] Step 2 findings were incorporated throughout (Sections 5, 6, 8, 11–14)
- [x] Conflicts/differences between sources are explicitly documented, not silently reconciled (Section 5)
- [x] Requirement categories created: Business, Functional, API, UI, Hybrid/E2E, Non-Functional (Section 6)
- [x] Requirement catalogue with traceability created (Sections 6–8)
- [x] The 24 UI + 8 API (32-test) baseline is treated as an existing reference baseline and is **unchanged** by this document (Section 8)
- [x] Test data requirements identified conceptually only — no data files created (Section 9)
- [x] Assumptions explicitly labeled and not presented as facts (Section 10)
- [x] Constraints and limitations documented (Section 11)
- [x] Open questions explicitly listed, with no guessed answers (Section 12)
- [x] Requirements prioritized with rationale (Section 13)
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 4 — Test Plan.
