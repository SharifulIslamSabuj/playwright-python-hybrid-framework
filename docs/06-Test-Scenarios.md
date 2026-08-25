# 06 — Test Scenario Design

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-TSD-001 |
| Document Title | Test Scenario Design |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 3 — Test Design |
| Step | Step 6 — Test Scenario Design |
| Predecessor Documents | [01](01-Project-Vision.md)–[05](05-Test-Strategy.md), all ✅ approved |
| Reference Baseline | TS `AE-TSD-001` (24 UI + 8 API = 32), TS `AE-TC-001` (step detail for context), TS `AE-TDD-001` (data-dependency context), TS `AE-AS-001` (automation-status context) — Priority 2, adapted not copied |

**Purpose:** This document answers *what* must be validated, at the scenario level, based on the approved requirements ([03](03-Requirement-Analysis.md)) and risk-based strategy ([05](05-Test-Strategy.md)). It is one abstraction level above Test Cases (Step 7, "how to execute") and one below the Requirement catalogue. **No step-by-step procedures are written here.**

**Evidence labels:** VERIFIED (Step 2 direct observation), PARTIALLY VERIFIED, REFERENCE-ONLY (TS baseline / not independently confirmed by this project), REQUIRES VERIFICATION (explicitly unconfirmed, to be resolved by executing this very scenario).

## 1. Scenario Design Principles Applied

Functional decomposition (one scenario = one coherent behavior), risk-based prioritization ([05](05-Test-Strategy.md) Section 2), positive **and** negative testing side-by-side, equivalence/boundary-oriented framing where the AUT's own documented parameters support it (Section 8 below), business-rule validation (`BR-*`/`REQ-BUS-*`), API-contract validation against the fully-verified 14-endpoint inventory, UI outcome-focused validation (not re-testing what an API scenario already proves — Section 10), cross-browser tagging without browser-per-scenario duplication (Section 9), explicit data/state dependency tagging (Section 11), and end-to-end business-journey framing (Section 7C) — all traced back to a `REQ-*` ID, never invented.

## 2. Priority Model

| Priority | Meaning | Reserved For |
|---|---|---|
| **P0 — Critical** | Failure would materially block core application use, a critical business flow, or release confidence | Authentication gate, cart-to-checkout boundary, core catalog/cart correctness, and — per [05](05-Test-Strategy.md) Section 2 — the currently-unverified Signup/Login scenarios, precisely *because* their unverified status is itself the highest current risk |
| **P1 — High** | Important business behavior; failure degrades a major journey but doesn't block the application broadly | Search, category/brand browsing, checkout sub-steps, most API positive/negative pairs |
| **P2 — Medium** | Secondary business behavior or ancillary feature | Subscription, product review, recommended items, most account-lifecycle APIs |
| **P3 — Low** | Cosmetic or low-business-impact behavior | Test Cases page navigation, scroll-button behavior (deferred) |

Priority reflects business/risk impact per [05](05-Test-Strategy.md) Section 2 — **not** effort or personal preference; note that several P0 items below are P0 *despite* being unautomated today, because their unverified status is the risk.

## 3. Risk Model Applied

Reusing the risk register from Steps 2–5 (no new register invented):

| Risk (from Steps 2–5) | Effect on Scenario Design |
|---|---|
| Signup/Login verification gap ([03](03-Requirement-Analysis.md) §14) | AE-UI-SC-004/005/006/007/008 elevated to P0 and explicitly tagged "REQUIRES VERIFICATION" rather than assumed |
| Checkout/payment verification gap | AE-UI-SC-022–026 kept P0/P1 for business importance but explicitly FLAGged (Section 15) as dependent on unresolved evidence, not silently treated as ready-to-automate |
| Shared public environment / API state mutation | Every scenario touching account creation/deletion or cart mutation is tagged with a data/state dependency (Section 11) and a shared-environment note (Section 12) |
| Search-relevance anomaly (Step 2 open question) | AE-UI-SC-012 explicitly scoped to include investigating the anomaly, not just "search works" |
| Cross-browser differences | A curated subset is tagged cross-browser-critical (Section 9), not the full set |
| Automation flakiness (AJAX cart removal) | AE-UI-SC-015 explicitly notes the AJAX dependency as a data/state and automation-suitability consideration |

## 4. Scenario Categories

Per instruction, only **A. UI/Functional**, **B. API**, and **C. Hybrid/E2E** are used — no Performance/Security/Accessibility scenarios are created, consistent with [01](01-Project-Vision.md) §10 and [04](04-Test-Plan.md) §4/7.

---

## 5. Category A — UI / Functional Scenarios

Fields: **ID | Module | Scenario | Priority | Risk | Req. Ref. | Baseline Status | Verification Status | Automation Suitability | Notes/Dependencies**

| ID | Module | Scenario | Priority | Risk | Req. Ref. | Baseline Status | Verification Status | Automation Suitability | Notes/Dependencies |
|---|---|---|---|---|---|---|---|---|---|
| AE-UI-SC-001 | Home | Home page loads with navigation, categories, brands, featured/recommended items, and subscription block all visible | P1 | Low | REQ-FUNC-HM-001–006 | **PROPOSE NEW** (TS baseline had no dedicated Home scenario — gap identified in [05](05-Test-Strategy.md) §7) | VERIFIED (Step 2) | HIGH | No data dependency; ideal smoke-suite anchor |
| AE-UI-SC-002 | Home / Subscription | Subscribe via Home page footer, confirm success signal | P2 | Low | REQ-FUNC-HM-007 | RETAIN (TS AE-UI-010) | VERIFIED field presence; submission REQUIRES VERIFICATION | HIGH | Requires a disposable/non-spam-sensitive email; do not use a real personal address |
| AE-UI-SC-003 | Cart / Subscription | Subscribe via Cart page footer, confirm success signal | P2 | Low | REQ-FUNC-HM-007 | **CONSOLIDATE (proposed)** — recommend merging with SC-002 as one parametrized scenario across two entry points (TS AE-UI-011) | VERIFIED field presence; submission REQUIRES VERIFICATION | HIGH | Same data note as SC-002; kept as a separate row here pending QA Lead decision on the consolidation |
| AE-UI-SC-004 | Signup / Account | Register a new user with valid account + address information; confirm account creation and logged-in state; delete account | **P0** | High (verification gap) | REQ-FUNC-SL-001, REQ-FUNC-SL-006 | RETAIN, **MODIFY** (priority elevated, reframed as a verification-priority scenario) (TS AE-UI-001) | **REQUIRES VERIFICATION** | HIGH once verified | New unique user data; must include a verified cleanup (delete) step; this is the single highest-value UI scenario to execute first per [05](05-Test-Strategy.md) §2 |
| AE-UI-SC-005 | Login | Log in with valid credentials, confirm logged-in state | **P0** | High (verification gap) | REQ-FUNC-SL-003 | RETAIN, MODIFY (priority elevated) (TS AE-UI-002) | **REQUIRES VERIFICATION** | HIGH once verified | Depends on a valid account existing (from SC-004 or a pre-provisioned reusable account) |
| AE-UI-SC-006 | Login | Log in with invalid credentials, confirm exact error message | **P0** | Medium (negative path, but well-understood) | REQ-FUNC-SL-004 | RETAIN (TS AE-UI-003) | **VERIFIED** (Step 2 — exact text confirmed) | HIGH | No account dependency — fabricated credentials only; strongest, cheapest P0 scenario to automate first |
| AE-UI-SC-007 | Logout | Log out from an authenticated session, confirm redirect/state | P1 | Medium (verification gap) | REQ-FUNC-SL-005/006 | RETAIN, MODIFY (TS AE-UI-004) | **REQUIRES VERIFICATION** | HIGH once verified | Depends on SC-005 |
| AE-UI-SC-008 | Signup (negative) | Register using an already-registered email; confirm rejection and error message | P1 | Medium | REQ-FUNC-SL-002 | RETAIN (TS AE-UI-005) | **REQUIRES VERIFICATION** (TS text "Email Address already exist!" is REFERENCE-only) | HIGH once verified | Requires one durable, known-existing account |
| AE-UI-SC-009 | Contact Us | Submit Contact Us form with name/email/subject/message and file upload, confirm success | P2 | Low | REQ-FUNC-CU-001/002/004 | RETAIN (TS AE-UI-006) | Fields VERIFIED; submission **REQUIRES VERIFICATION** | HIGH | Sends a real message to the site's feedback channel — confirm acceptable before automating in CI |
| AE-UI-SC-010 | Test Cases page | Navigate to the site's own published Test Cases page and confirm it renders | P3 | Low | Navigation only, no `REQ-*` | RETAIN, **FLAG** (TS AE-UI-007) | VERIFIED (Step 2) | LOW | **Recommend deprioritizing/deferring** — this validates a QA-reference page on the AUT itself, not a business feature (Step 2 §3); low value beyond a smoke check |
| AE-UI-SC-011 | Products | View All Products page; view Product Details (name, category, price, availability, condition, brand) | P0 | Low | REQ-FUNC-PR-001/002 | RETAIN (TS AE-UI-008) | **VERIFIED** (Step 2) | HIGH | No account dependency |
| AE-UI-SC-012 | Search | Search a valid keyword; verify results are relevant; **investigate the unresolved search-relevance anomaly** (Step 2/3 open question) as part of expected-result definition | P1 | Medium (open question) | REQ-FUNC-PR-003/004 | RETAIN, MODIFY (scope expanded) (TS AE-UI-009) | PARTIALLY VERIFIED | MEDIUM until the matching rule is understood | No account dependency; Test Case (Step 7) must define what "relevant" means once investigated |
| AE-UI-SC-013 | Cart | Add multiple products to cart; verify price/quantity/line totals and cart total | P0 | Medium | REQ-FUNC-CT-001/004 | RETAIN (TS AE-UI-012) | PARTIALLY VERIFIED (single item only) | HIGH | No account dependency |
| AE-UI-SC-014 | Cart | Set/verify a specific product quantity in cart | P1 | Medium | REQ-FUNC-CT-002 | RETAIN (TS AE-UI-013) | PARTIALLY VERIFIED | HIGH | No account dependency |
| AE-UI-SC-015 | Cart | Remove a product from cart, confirm it no longer appears | P0 | Low | REQ-FUNC-CT-003 | RETAIN (TS AE-UI-017) | **VERIFIED** (Step 2 — AJAX-driven) | HIGH | No account dependency; automation must wait on the client-side update, not a page load (REQ-UI-005) |
| AE-UI-SC-016 | Categories | Browse a category, switch to another category/sub-category | P2 | Low | REQ-FUNC-PR-005 | RETAIN (TS AE-UI-018) | VERIFIED at route level | HIGH | Category-ID-to-name mapping still an open question (Section 15) — affects Test Case design, not this scenario's validity |
| AE-UI-SC-017 | Brands | Browse a brand, switch to another brand | P2 | Low | REQ-FUNC-PR-006 | RETAIN (TS AE-UI-019) | **VERIFIED** | HIGH | No account dependency |
| AE-UI-SC-018 | Search + Cart + Login | Add searched products to cart; verify they remain in cart after logging in | P1 | High (depends on Login) | REQ-FUNC-PR-003, REQ-FUNC-CT-005 | RETAIN (TS AE-UI-020) | **REQUIRES VERIFICATION** | MEDIUM until Login verified | Depends on SC-005 |
| AE-UI-SC-019 | Product Review | Submit a review on a product detail page, confirm success | P2 | Low | Product Review (no dedicated `REQ-FUNC` beyond module inventory) | RETAIN (TS AE-UI-021) | Fields VERIFIED; submission REQUIRES VERIFICATION | HIGH | No account dependency observed |
| AE-UI-SC-020 | Recommended Items | Add a recommended-section item to cart, confirm it appears correctly on the cart page | P2 | Low | Recommended Items, REQ-FUNC-CT-001 | RETAIN (TS AE-UI-022) | Extension of an already-VERIFIED pattern (add-to-cart) | HIGH | No account dependency |
| AE-UI-SC-021 | Checkout gate | Attempt checkout while unauthenticated; confirm the exact Register/Login gate modal and its two options | **P0** | High (this IS the strongest checkout evidence we have) | REQ-FUNC-CO-001, REQ-BUS-004, BR-003 | **PROPOSE NEW** — previously only implicit inside larger E2E flows (e.g., TS TC-14); promoted to a standalone scenario | **VERIFIED** (Step 2) | HIGH | No account dependency; cheapest, highest-confidence P0 Checkout-area scenario — recommend automating this before any full checkout E2E |
| AE-UI-SC-022 | Checkout (E2E) | Full order placement: add to cart → checkout → **register during checkout** → address → payment → confirmation → invoice → cleanup | P0 | **High** (major evidence gap) | REQ-FUNC-CO-002–006 | RETAIN, **FLAG** (TS AE-UI-014) | **REQUIRES VERIFICATION** — depends on resolving the `/checkout` vs `/view_cart` route question ([03](03-Requirement-Analysis.md) §5 row 1) | LOW until the route/flow is independently confirmed | New unique user + verified cleanup; do not automate before manual/exploratory verification |
| AE-UI-SC-023 | Checkout (E2E) | Full order placement: **register before checkout**, then checkout → address → payment → confirmation → invoice → cleanup | P0 | High | REQ-FUNC-CO-002–006 | RETAIN, FLAG, **CONSOLIDATE-candidate** with SC-022/024 (TS AE-UI-015) | REQUIRES VERIFICATION | LOW until verified | Same dependency as SC-022; recommend evaluating whether SC-022/023/024 become one parametrized scenario once the core flow is confirmed |
| AE-UI-SC-024 | Checkout (E2E) | Full order placement: **login before checkout** (existing user) → checkout → address → payment → confirmation → invoice | P0 | High | REQ-FUNC-CO-002–006 | RETAIN, FLAG, CONSOLIDATE-candidate (TS AE-UI-016) | REQUIRES VERIFICATION | LOW until verified | Depends on SC-005 (Login) and the same checkout-route question as SC-022 |
| AE-UI-SC-025 | Checkout | Verify delivery and billing address shown at checkout match the address entered at registration | P1 | High | REQ-FUNC-CO-002/003 | RETAIN, FLAG (TS AE-UI-023) | REQUIRES VERIFICATION | LOW until verified | Depends on SC-004/SC-022 structure being confirmed first |
| AE-UI-SC-026 | Order / Invoice | Download invoice after a completed order, confirm the file is produced | P2 | Medium | REQ-FUNC-CO-006 | RETAIN, FLAG (TS AE-UI-024) | REQUIRES VERIFICATION | LOW until verified | Depends on SC-022/023/024 completing; also introduces a file-download environment dependency (browser download directory) — a framework concern for later |

**Deferred (not part of the active Python scenario set — reaffirmed, not silently dropped):**

| Source | Item | Status | Rationale |
|---|---|---|---|
| TS TC-25 | Verify Scroll Up using Arrow button and Scroll Down | **DEFER** | Low business risk, mainly cosmetic UI behavior — TS baseline's own rationale still holds; no new evidence changes this |
| TS TC-26 | Verify Scroll Up without Arrow button and Scroll Down | **DEFER** | Same as above |

---

## 6. Category B — API Scenarios

All request/response facts below are **VERIFIED** directly from `/api_list` in Step 2 — none are invented.

### B1. Baseline (retained from TS's 8 Phase-1-automated API scenarios)

| ID | Endpoint | Scenario | Priority | Req. Ref. | Baseline Status | Verification Status | Automation Suitability | Notes/Dependencies |
|---|---|---|---|---|---|---|---|---|
| AE-API-SC-001 | GET `/api/productsList` | Retrieve all products, confirm 200 + product list JSON | P0 | REQ-API-001 | RETAIN (TS AE-API-001) | VERIFIED | HIGH | No data dependency; read-only |
| AE-API-SC-002 | POST `/api/productsList` | Confirm unsupported method returns 405 | P2 | REQ-API-002 | RETAIN (TS AE-API-002) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-003 | GET `/api/brandsList` | Retrieve all brands, confirm 200 + brand list JSON | P1 | REQ-API-003 | RETAIN (TS AE-API-003) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-004 | PUT `/api/brandsList` | Confirm unsupported method returns 405 | P2 | REQ-API-004 | RETAIN (TS AE-API-004) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-005 | POST `/api/searchProduct` | Search with valid `search_product` param, confirm 200 + results | P1 | REQ-API-005 | RETAIN (TS AE-API-005) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-006 | POST `/api/searchProduct` | Omit `search_product` param, confirm 400 + missing-parameter message | P1 | REQ-API-006 | RETAIN (TS AE-API-006) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-007 | POST `/api/verifyLogin` | Valid email/password, confirm 200 + "User exists!" | **P0** | REQ-API-007 | RETAIN (TS AE-API-007) | VERIFIED | HIGH | **Requires one known-valid account** — ties this API scenario to the same Signup/Login verification-gap dependency as the UI scenarios |
| AE-API-SC-008 | POST `/api/verifyLogin` | Invalid email/password, confirm 404 + "User not found!" | P1 | REQ-API-010 | RETAIN (TS AE-API-008, sourced from TS API-10) | VERIFIED | HIGH | No data dependency — fabricated credentials only |

### B2. Proposed additions (beyond the 8-scenario baseline — explicitly flagged for QA Lead / Step 9 approval)

These 6 correspond exactly to the endpoints the TS baseline deferred (AE-AS-001 §6) *because* they were unverified at the time. This project has since independently VERIFIED all 6 at the documentation level (Step 2), which is materially stronger evidence than existed when the TS project deferred them — that is the basis for proposing them, not a desire to inflate scenario count.

| ID | Endpoint | Scenario | Priority | Req. Ref. | Baseline Status | Verification Status | Automation Suitability | Notes/Dependencies |
|---|---|---|---|---|---|---|---|---|
| AE-API-SC-009 | POST `/api/verifyLogin` | Omit email param, confirm 400 + missing-parameter message | P2 | REQ-API-008 | **PROPOSE NEW** (was TS-deferred; now independently VERIFIED, stronger evidence basis) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-010 | DELETE `/api/verifyLogin` | Confirm unsupported method returns 405 | P3 | REQ-API-009 | **PROPOSE NEW** (same rationale) | VERIFIED | HIGH | No data dependency |
| AE-API-SC-011 | POST `/api/createAccount` | Create account with full field set, confirm 201 + "User created!" | **P0** | REQ-API-011 | **PROPOSE NEW** — highest strategic value: this is the key to closing the Signup verification gap and enabling Hybrid scenarios | Documentation-level VERIFIED; **execution requires QA-Lead-directed test-account creation** (this assistant may not perform account creation unilaterally) | HIGH, once execution is authorized | **State-mutating** — must always pair with SC-012 cleanup in the same test |
| AE-API-SC-012 | DELETE `/api/deleteAccount` | Delete a previously created account, confirm 200 + "Account deleted!" | P1 | REQ-API-012 | **PROPOSE NEW** | Documentation-level VERIFIED; execution requires an account created via SC-011 | HIGH | Must never run standalone without a corresponding created account — cleanup-only scenario |
| AE-API-SC-013 | PUT `/api/updateAccount` | Update an existing account's fields, confirm 200 + "User updated!" | P2 | REQ-API-013 | **PROPOSE NEW** | Documentation-level VERIFIED | MEDIUM | State-mutating; requires SC-011 account and SC-012-style cleanup |
| AE-API-SC-014 | GET `/api/getUserDetailByEmail` | Retrieve account details by email, confirm 200 + user JSON | P2 | REQ-API-014 | **PROPOSE NEW** | Documentation-level VERIFIED | HIGH | Read-only once an account exists; valuable as a Hybrid-scenario oracle (Section 7) |

---

## 7. Category C — Hybrid / E2E Scenarios

Each justified individually per [05](05-Test-Strategy.md) §6 — none included merely to demonstrate "UI and API in one test."

| ID | Scenario | Justification (why UI-only or API-only is insufficient) | Priority | Req. Ref. | Baseline Status | Verification Status | Automation Suitability | Notes/Dependencies |
|---|---|---|---|---|---|---|---|---|
| AE-E2E-SC-001 | Provision an account via `createAccount` API, then verify that account logs in correctly through the UI | Proves Login correctness is independent of *how* the account was created, and provisions test accounts faster/more reliably than UI signup — pure UI testing can't isolate this distinction, pure API testing never exercises the actual login UI | P1 | REQ-E2E-001 | REFERENCE-ONLY — planning-approved in TS but **never implemented even there** (TS AE-AS-001 §13) | Not started | MEDIUM — sequence **after** AE-UI-SC-005 (Login) is independently verified, per [05](05-Test-Strategy.md) §6 | Depends on AE-API-SC-011/012 and AE-UI-SC-005 |
| AE-E2E-SC-002 | Provision an account via `createAccount` API, then complete the full Checkout journey through the UI | Confirms Checkout has no hidden dependency on the UI registration flow specifically, while reducing the setup cost of an expensive E2E test | P2 | REQ-E2E-002 | REFERENCE-ONLY — same planning-only status as above | Not started | LOW until AE-UI-SC-022/023/024 (Checkout) is independently verified — currently blocked by the same route/flow open question | Depends on AE-API-SC-011/012 and AE-UI-SC-022–024 |
| AE-E2E-SC-003 | Cross-check UI-rendered product listing data (name/price) against `GET /api/productsList` as an independent oracle | Removes reliance on hard-coded expected values in UI tests, and would catch a UI/backend data-rendering mismatch that neither a pure UI test (no independent source of truth) nor a pure API test (never renders anything) could catch alone | P1 | REQ-E2E-003 | **New in this project** (Step 2/3) — not present in TS baseline | Not started | **HIGH — not gated by the Signup/Login verification gap**, unlike SC-001/002; this is the one Hybrid scenario with no identity-flow dependency and could reasonably be attempted earliest | Depends on AE-UI-SC-011 and AE-API-SC-001 only — no account required |

---

## 8. Negative, Boundary, and Equivalence Coverage

**Negative scenarios represented above** (all traced to VERIFIED or documented behavior, none invented): invalid login (SC-006), duplicate-email registration (SC-008), missing search parameter (SC-006 API/SC-006), missing `verifyLogin` email parameter (SC-009 API), unsupported HTTP methods on 4 endpoints (SC-002/004/010 API), invalid `verifyLogin` credentials (SC-008 API).

**Boundary/equivalence areas identified as valuable** (no exact values fixed here — that is Step 8):
- **Search input:** an empty search, a non-matching keyword, and the already-flagged "unexpectedly matching" keyword (Section 15) form a natural equivalence set for AE-UI-SC-012/AE-API-SC-005/006.
- **Login input:** valid / invalid-but-well-formed / malformed-email equivalence classes for AE-UI-SC-005/006 and AE-API-SC-007/008/009.
- **Signup fields:** required vs. optional field boundaries (the `createAccount` API's 16-field payload gives a concrete, VERIFIED field list to partition against — REQ-API-011).
- **Contact form:** required-field boundary (name/email/subject/message vs. optional file upload) for AE-UI-SC-009.
- **Cart quantity:** the open question from [03](03-Requirement-Analysis.md) §12 (does the app reject negative/zero quantity?) makes this a genuine boundary candidate for AE-UI-SC-014, not just a nominal check.
- **Cart state:** empty cart vs. single-item vs. multi-item as equivalence classes across AE-UI-SC-013/015.

No boundary value or exact test data is fixed in this document — that belongs to Step 8 (Test Data Design).

## 9. Cross-Browser Consideration

No scenario above is duplicated per browser. Per the approved strategy ([05](05-Test-Strategy.md) §9), scenarios are classified instead:

| Classification | Scenarios | Rationale |
|---|---|---|
| **Critical cross-browser candidates** (Layer 4, run on Chromium + Firefox + WebKit at scheduled/release cadence) | AE-UI-SC-006 (invalid login), AE-UI-SC-013/015 (cart add/remove), AE-UI-SC-021 (checkout gate) | These are the customer-facing, business-critical, already-VERIFIED-on-Chromium behaviors where an engine-specific rendering/interaction difference would matter most |
| **Cross-browser candidates, lower priority** | AE-UI-SC-011, 012, 016, 017 (catalog/search/category/brand) | Business-relevant but lower risk of engine-specific divergence |
| **Browser-independent** (Chromium-only is sufficient) | All API scenarios (Category B — no browser involved), AE-UI-SC-001/002/003/009/010/019 (content-driven, low interaction complexity) | Running these cross-browser would add cost without meaningfully reducing risk |

## 10. Duplication Control

Applied per [05](05-Test-Strategy.md) §4: where an API scenario already validates a data contract, the corresponding UI scenario is scoped to **user-facing outcome**, not repeated assertions. Concretely:
- AE-API-SC-001 (products list) validates the data contract; AE-UI-SC-011 validates that the *page* renders it correctly — not a second check of the JSON.
- AE-API-SC-005/006 (search) validate the request/response contract; AE-UI-SC-012 validates the *user-visible* result list and investigates the relevance anomaly — not a repeat of the API's status-code assertions.
- AE-API-SC-007/008 (verifyLogin) validate the credential-check contract; AE-UI-SC-005/006 validate the *UI's* rendering of success/failure — deliberately not redundant, since the UI login form is not proven to call this same API internally.

**Consolidation candidates identified** (proposed, not executed): AE-UI-SC-002/003 (subscription, two entry points) and AE-UI-SC-022/023/024 (three checkout-entry variants) — see Section 15 for the explicit proposal and required QA Lead decision.

## 11. Business Journey Coverage

| Journey | Scenarios | Status |
|---|---|---|
| Browse → Search → Product Details → Cart | AE-UI-SC-011, 012, 013 | Largely VERIFIED/PARTIALLY VERIFIED — lowest-risk journey |
| User → Signup → Login → Browse → Cart → Checkout | AE-UI-SC-004, 005, 011, 013, 021, 022/023/024 | **REQUIRES VERIFICATION beyond the checkout gate** — do not assume the full journey works end-to-end; SC-021 (the gate itself) is the one VERIFIED link in this chain |
| User → Contact Us | AE-UI-SC-009 | Fields VERIFIED; outcome REQUIRES VERIFICATION |
| API → Product/Brand discovery | AE-API-SC-001, 003, 005 | VERIFIED |
| API → Authentication/account operation | AE-API-SC-007, 008, 009, 011–014 | Credential-check VERIFIED; account-lifecycle documentation-VERIFIED, execution pending authorization |

No Checkout/Payment behavior is assumed beyond what SC-021 (the gate) already proves — the rest of that journey is explicitly marked REQUIRES VERIFICATION throughout this document, not silently treated as working.

## 12. Data / State Dependencies

| Dependency Type | Scenarios | Notes |
|---|---|---|
| Existing/reusable valid user | AE-UI-SC-005, 007, 018; AE-API-SC-007 | Needed before these can execute |
| New unique user (with mandatory cleanup) | AE-UI-SC-004, 022, 023; AE-API-SC-011/012 | Must never be created without a matching delete step |
| Known-existing user (for duplicate-email negative test) | AE-UI-SC-008 | One durable account reserved for this purpose |
| Product/catalog data | AE-UI-SC-011–020, 026; AE-API-SC-001/005 | Preferably sourced live via API rather than hard-coded (per [05](05-Test-Strategy.md) §10) |
| Cart state | AE-UI-SC-013, 014, 015, 018, 020, 022–024 | Each must establish its own cart state, not inherit another test's |
| Account state (logged-in session) | AE-UI-SC-007, 018, 024; AE-E2E-SC-001/002 | Depends on Login (SC-005) being verified first |
| API-generated state | AE-E2E-SC-001/002 | Depends on AE-API-SC-011 |
| Cleanup required | AE-UI-SC-004, 022, 023, 024; AE-API-SC-011 (paired with SC-012) | Explicit teardown, not optional |

No actual test data values are created here — Step 8 owns that.

## 13. Shared Environment Considerations

Flagged per instruction — Automation Exercise is a single public shared instance ([02](02-Application-Analysis.md) §14):

- **Data mutation occurs in:** AE-UI-SC-004/008/022/023/024, AE-API-SC-011/013.
- **Account creation occurs in:** AE-UI-SC-004/022/023, AE-API-SC-011, AE-E2E-SC-001/002.
- **Account deletion occurs in:** AE-UI-SC-004/022/023/024 (as part of cleanup), AE-API-SC-012.
- **Cart state may persist across a session and could leak between tests if not isolated:** AE-UI-SC-013/014/015/018/020/022–024 — each must use independent product/quantity choices or explicit cart-clearing.
- **Concurrent execution could conflict:** any scenario in this list that creates or mutates an account or cart must not run in parallel with another instance of itself without uniquely-generated data (per [05](05-Test-Strategy.md) §14/15).

These flags are carried forward as direct input to Step 8 (Test Data Design) and Step 11 (Framework Architecture) — they are not resolved in this document.

---

## 14. TypeScript Baseline Reconciliation

Full reconciliation of everything the TS project ever documented (32 approved + 2 deferred UI + 6 deferred API = 40 items) against this project's scenario catalogue.

| TS Source | TS Title | Python Scenario | Status |
|---|---|---|---|
| AE-UI-001 | Register new user | AE-UI-SC-004 | RETAIN, MODIFY (priority elevated, verification-first framing) |
| AE-UI-002 | Login valid | AE-UI-SC-005 | RETAIN, MODIFY |
| AE-UI-003 | Login invalid | AE-UI-SC-006 | RETAIN |
| AE-UI-004 | Logout | AE-UI-SC-007 | RETAIN, MODIFY |
| AE-UI-005 | Register existing email | AE-UI-SC-008 | RETAIN |
| AE-UI-006 | Contact Us | AE-UI-SC-009 | RETAIN |
| AE-UI-007 | Test Cases page nav | AE-UI-SC-010 | RETAIN, FLAG (recommend deprioritize) |
| AE-UI-008 | All products / product details | AE-UI-SC-011 | RETAIN |
| AE-UI-009 | Search product | AE-UI-SC-012 | RETAIN, MODIFY (scope expanded) |
| AE-UI-010 | Subscribe — Home | AE-UI-SC-002 | RETAIN |
| AE-UI-011 | Subscribe — Cart | AE-UI-SC-003 | CONSOLIDATE (proposed) |
| AE-UI-012 | Add multiple products to cart | AE-UI-SC-013 | RETAIN |
| AE-UI-013 | Verify cart quantity | AE-UI-SC-014 | RETAIN |
| AE-UI-014 | Checkout — register during | AE-UI-SC-022 | RETAIN, FLAG |
| AE-UI-015 | Checkout — register before | AE-UI-SC-023 | RETAIN, FLAG |
| AE-UI-016 | Checkout — login before | AE-UI-SC-024 | RETAIN, FLAG |
| AE-UI-017 | Remove from cart | AE-UI-SC-015 | RETAIN |
| AE-UI-018 | View category products | AE-UI-SC-016 | RETAIN |
| AE-UI-019 | View brand products | AE-UI-SC-017 | RETAIN |
| AE-UI-020 | Search + cart after login | AE-UI-SC-018 | RETAIN |
| AE-UI-021 | Add product review | AE-UI-SC-019 | RETAIN |
| AE-UI-022 | Add recommended item | AE-UI-SC-020 | RETAIN |
| AE-UI-023 | Verify checkout address | AE-UI-SC-025 | RETAIN, FLAG |
| AE-UI-024 | Download invoice | AE-UI-SC-026 | RETAIN, FLAG |
| TC-25 | Scroll up with arrow | — | DEFER (reaffirmed) |
| TC-26 | Scroll up without arrow | — | DEFER (reaffirmed) |
| AE-API-001 | GET productsList | AE-API-SC-001 | RETAIN |
| AE-API-002 | POST productsList (405) | AE-API-SC-002 | RETAIN |
| AE-API-003 | GET brandsList | AE-API-SC-003 | RETAIN |
| AE-API-004 | PUT brandsList (405) | AE-API-SC-004 | RETAIN |
| AE-API-005 | Search valid | AE-API-SC-005 | RETAIN |
| AE-API-006 | Search missing param | AE-API-SC-006 | RETAIN |
| AE-API-007 | verifyLogin valid | AE-API-SC-007 | RETAIN |
| AE-API-008 (src API-10) | verifyLogin invalid | AE-API-SC-008 | RETAIN |
| API-08 (deferred) | verifyLogin missing email | AE-API-SC-009 | **PROPOSE NEW** (promoted — now independently verified) |
| API-09 (deferred) | DELETE verifyLogin (405) | AE-API-SC-010 | **PROPOSE NEW** (promoted) |
| API-11 (deferred) | createAccount | AE-API-SC-011 | **PROPOSE NEW** (promoted) |
| API-12 (deferred) | deleteAccount | AE-API-SC-012 | **PROPOSE NEW** (promoted) |
| API-13 (deferred) | updateAccount | AE-API-SC-013 | **PROPOSE NEW** (promoted) |
| API-14 (deferred) | getUserDetailByEmail | AE-API-SC-014 | **PROPOSE NEW** (promoted) |
| AE-TC-HYBRID-001 (planning-only) | Login via API-provisioned account | AE-E2E-SC-001 | RETAIN as proposal (still not implemented anywhere) |
| AE-TC-HYBRID-002 (planning-only) | Checkout for API-provisioned account | AE-E2E-SC-002 | RETAIN as proposal (still not implemented anywhere) |
| — | (no TS equivalent) | AE-E2E-SC-003 | **PROPOSE NEW** (Python-originated) |
| — | (no TS equivalent) | AE-UI-SC-001 (Home) | **PROPOSE NEW** (Python-originated) |
| — | (no TS equivalent) | AE-UI-SC-021 (Checkout gate) | **PROPOSE NEW** (Python-originated) |

**No item above was silently deleted or added** — every status change (MODIFY, FLAG, CONSOLIDATE, PROPOSE NEW) carries its rationale inline in Sections 5–7 above, and every promotion of a previously-deferred item is justified by this project's stronger, independently-gathered verification evidence (Step 2), not by preference.

## 15. Coverage Target and Baseline Impact

**Current, unchanged reference baseline: 24 UI + 8 API = 32.** This document does **not** silently alter that number.

**If all proposals in this document were approved**, the Python project's scenario catalogue would be:
- UI: 24 retained/modified/flagged + 2 proposed new (Home, Checkout gate) = **26** (or 25 if the SC-002/003 consolidation is also approved)
- API: 8 retained + 6 proposed new = **14**
- Hybrid/E2E: 0 baselined (TS never implemented its 2) + 3 proposed = **3**
- **Total if fully approved: 43** (vs. the 32 reference baseline)

This is presented as an **explicit proposal for QA Lead decision**, not an automatic scope change. The rationale in every case is either (a) closing an identified coverage gap ([05](05-Test-Strategy.md) §7 "TS baseline had no dedicated Home scenario"), (b) promoting a previously-deferred item on the strength of new evidence this project independently gathered (all 6 API additions), or (c) capturing a scenario this project's own analysis surfaced that the TS baseline never considered (AE-E2E-SC-003, AE-UI-SC-021). Formal acceptance of any of these into the automation baseline remains **Step 9 — Automation Scope**.

## 16. Scenario Summary

| Category | Count (proposed catalogue) | P0 | P1 | P2 | P3 |
|---|---|---|---|---|---|
| UI | 26 | 10 | 7 | 8 | 1 |
| API | 14 | 3 | 5 | 5 | 1 |
| Hybrid/E2E | 3 | 0 | 2 | 1 | 0 |
| **Total** | **43** | **13** | **14** | **14** | **2** |

| Reconciliation Outcome | Count |
|---|---|
| Baseline (TS-approved 32) | 32 |
| RETAIN (unchanged in substance) | 16 |
| RETAIN + MODIFY (priority/scope adjusted) | 8 |
| CONSOLIDATE (proposed, not executed) | 1 pair (2 scenarios → proposed as 1) |
| FLAG (dependent on unresolved evidence) | 6 (all Checkout-area) |
| DEFER (reaffirmed) | 2 |
| PROPOSE NEW (promoted from TS-deferred, stronger evidence) | 6 (all API) |
| PROPOSE NEW (Python-originated, no TS equivalent) | 3 |
| PROPOSE (Hybrid, carried from TS planning-only, still unimplemented anywhere) | 2 |

## 17. Coverage Analysis

| Area | Coverage Status |
|---|---|
| Business Requirements (`REQ-BUS-*`, 5) | Covered by scenario design (BUS-004 authentication-gate is the strongest, VERIFIED via AE-UI-SC-021) |
| Functional Requirements (`REQ-FUNC-*`, 34) | Covered by AE-UI-SC-001–026; **16 of 34's underlying evidence is REQUIRES VERIFICATION**, not yet Not Covered — the scenario exists, the proof does not |
| API Requirements (`REQ-API-*`, 14) | **Fully covered** by AE-API-SC-001–014 (8 baseline + 6 proposed) |
| UI Requirements (`REQ-UI-*`, 8) | Covered indirectly through UI scenario design choices (locator strategy, deterministic-message assertions, AJAX handling in SC-015) — not separately scenario'd, since these are cross-cutting design principles, not standalone user-facing behaviors |
| Hybrid Requirements (`REQ-E2E-*`, 3) | Covered by proposals AE-E2E-SC-001–003; **Not Covered by any executed test anywhere** — genuinely new ground |
| High-risk areas (Signup/Login/Checkout) | **Requires Verification** — explicitly and repeatedly flagged, not hidden |
| Critical business journeys (Section 11) | Discovery/Cart journey: Covered/Partially Covered. Identity→Checkout→Order journey: **Partially Covered at best** — only the authentication gate is proven |

No gap is hidden: the 16-of-48 verification gap from [03](03-Requirement-Analysis.md) §14 is fully reflected in this scenario set's REQUIRES VERIFICATION tags.

## 18. Open Questions

Carried forward, not resolved — matching [03](03-Requirement-Analysis.md) §12:

1. Is `/checkout` a distinct route from `/view_cart`? Directly blocks Test Case design for AE-UI-SC-022/023/024.
2. What is the exact checkout flow beyond the authentication gate (address, payment, confirmation, invoice)? Blocks AE-UI-SC-022–026.
3. Why did a search for "dress" return a non-obviously-matching result? Directly scoped into AE-UI-SC-012.
4. Is the TS-documented duplicate-email error text ("Email Address already exist!") still accurate? Affects AE-UI-SC-008's expected result.
5. Does the application enforce non-negative product quantity? Affects AE-UI-SC-014's boundary design (Section 8).
6. What is the actual session-persistence/logout behavior? Affects AE-UI-SC-007/018.
7. Is the category-ID-to-name mapping for `/category_products/{id}` stable? Affects AE-UI-SC-016's Test Case design.
8. Does Contact Us/Subscription perform client-side validation, and what does success actually display? Affects AE-UI-SC-002/003/009.

## 19. Decisions Requiring QA Lead Approval

Only genuine decisions — nothing manufactured:

1. **Scope change from 32 to up to 43 scenarios** (Section 15) — specifically: approve/reject the 6 promoted API scenarios (SC-009–014), the 3 Python-originated scenarios (Home, Checkout gate, product-data oracle Hybrid), and the 2 carried-forward-but-never-implemented Hybrid scenarios.
2. **Consolidation proposal:** AE-UI-SC-002/003 (subscription, two entry points) into one parametrized scenario.
3. **Consolidation proposal:** AE-UI-SC-022/023/024 (three checkout-entry variants) into a data-driven single scenario, once the underlying flow is verified.
4. **Deprioritization proposal:** AE-UI-SC-010 (Test Cases page navigation) — recommend confirming this stays P3/low-value rather than being carried at its original TS priority.
5. **Sequencing confirmation:** that AE-UI-SC-004/005/006 (Signup/Login) and AE-UI-SC-021 (Checkout gate) should be the first scenarios executed/verified, ahead of the full Checkout E2E scenarios (SC-022–026) and both Hybrid scenarios that depend on them — consistent with [05](05-Test-Strategy.md) but not yet formally re-confirmed at this step.
6. **Authorization for AE-API-SC-011/012 execution:** these require actually creating and deleting a test account via API — this assistant cannot authorize or perform that unilaterally; explicit QA Lead direction is needed before Step 7/9 treats them as executable.

## 20. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 6 Exit Checklist

- [x] Steps 1–5 reviewed and used as direct basis
- [x] TS `AE-TSD-001`, `AE-TC-001`, `AE-TDD-001`, `AE-AS-001` reviewed (cumulative with prior steps)
- [x] All 14 verified API endpoints considered (Section 6)
- [x] All verified application modules considered (Section 5)
- [x] 32-test baseline explicitly reconciled, not silently changed (Section 14)
- [x] No scenario copied blindly — every RETAIN/MODIFY/FLAG/PROPOSE carries its own rationale
- [x] No unsupported application behavior invented — REQUIRES VERIFICATION used wherever evidence is incomplete
- [x] Signup/Login/Checkout verification gaps clearly identified and elevated in priority (Sections 3, 5, 17)
- [x] UI, API, and Hybrid scenarios kept in separate categories (Sections 5–7)
- [x] Every Hybrid scenario carries explicit justification (Section 7)
- [x] Negative scenarios represented (Section 8)
- [x] Risk-based priority applied throughout (Sections 2–3)
- [x] Requirement traceability included in every scenario row
- [x] Automation suitability marked preliminary only — Step 9 owns the final decision
- [x] No Test Data created (Step 8 remains untouched)
- [x] No Test Cases created (Step 7 remains untouched)
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 7 — Test Case Design.
