# 07 — Test Case Design

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-TC-001 |
| Document Title | Test Case Design |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 3 — Test Design |
| Step | Step 7 — Test Case Design |
| Predecessor Documents | [01](01-Project-Vision.md)–[06](06-Test-Scenarios.md), all ✅ approved (Step 6 approved with controlled scope) |

## 2. Purpose

Converts the 43 scenario candidates approved-with-controlled-scope in [06-Test-Scenarios.md](06-Test-Scenarios.md) into execution-level Test Cases: concrete preconditions, steps, and observable expected results. **A Test Case answers *how*; it does not decide *whether* the behavior gets automated** — that remains Step 9.

## 3. Scope

Every one of the 43 Step-6 scenarios is evaluated. Several scenarios warrant more than one Test Case (additional negative/boundary coverage identified during design — Sections 9–11); none are force-fit to hit 32 or 43. **No Test Case in this document is automation-approved.** Every single case below carries `Automation Approval Status: Not Yet Automation-Approved (pending Step 9)` — this is stated once here and is implicit throughout; it is not repeated as a per-case sentence to keep cards readable, but it applies uniformly and without exception.

## 4. Source Documents Reviewed

**Current Python project:** [01-Project-Vision.md](01-Project-Vision.md), [02-Application-Analysis.md](02-Application-Analysis.md), [03-Requirement-Analysis.md](03-Requirement-Analysis.md), [04-Test-Plan.md](04-Test-Plan.md), [05-Test-Strategy.md](05-Test-Strategy.md), [06-Test-Scenarios.md](06-Test-Scenarios.md) — all six reviewed and used as direct input.

**Previous TypeScript project** (Priority 2, `playwright-typescript-hybrid-framework/docs/`, already extracted and read across Steps 3–6, re-consulted here): `AE-PV-001`, `AE-AA-001`, `AE-RA-001`, `AE-TP-001`, `AE-TS-001`, `AE-TSD-001`, `AE-TC-001` (step-level detail — used to understand existing execution granularity, e.g. exact checkout sub-steps and error strings, never copied verbatim as fact), `AE-TDD-001` (data-category reference only), `AE-AS-001` (baseline/deferral status).

Where current Python evidence (Steps 2–6) differs from the TS baseline, this document follows the current approved Python documents and flags the difference explicitly (Section 15).

## 5. Test Case Design Principles

Scenario → Test Case is a one-to-many relationship where justified: a scenario is expanded into more than one Test Case only when a genuinely distinct positive, negative, or boundary condition adds coverage value (e.g., the search scenario yields a valid-keyword case, a non-matching-keyword case, and a dedicated anomaly-investigation case — three different things worth knowing separately). Every step is atomic and observable (`Action → Expected`); no step reads "verify everything works." Every expected result is a specific, checkable outcome — where the exact AUT message/behavior is not yet independently confirmed, the expected result is written honestly as **"requires verification"** rather than invented (Section 12).

## 6. ID Convention

`AE-UI-TC-0xx`, `AE-API-TC-0xx`, `AE-E2E-TC-0xx` — sequential within category, independent of the old TS IDs. Every Test Case cites its Scenario ID (`AE-*-SC-0xx` from Step 6) and Requirement ID (`REQ-*` from Step 3).

## 7. Priority Model

Identical to [06-Test-Scenarios.md](06-Test-Scenarios.md) §2 — P0 Critical / P1 High / P2 Medium / P3 Low, driven by business/risk impact, not execution difficulty. A case is not P0 because it is hard to automate (e.g., the Checkout E2E cases remain P0 for business importance despite being currently unautomatable).

---

## 8. Test Case Inventory (Master Summary)

| TC ID | Scenario | Title | Type | Priority | Baseline Status | Verification Status | Automation Suitability |
|---|---|---|---|---|---|---|---|
| AE-UI-TC-001 | SC-001 | Home page core elements visible | Smoke/Positive | P1 | Python Proposed | Verified | HIGH |
| AE-UI-TC-002 | SC-002 | Subscribe — Home footer | Positive | P2 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-003 | SC-003 | Subscribe — Cart footer | Positive | P2 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-004 | SC-004 | Register new user (full lifecycle) | Positive/E2E | P0 | TS Baseline | Requires Verification | HIGH (once verified) |
| AE-UI-TC-005 | SC-005 | Login — valid credentials | Positive | P0 | TS Baseline | Requires Verification | HIGH (once verified) |
| AE-UI-TC-006 | SC-006 | Login — invalid credentials | Negative | P0 | TS Baseline | Verified | HIGH |
| AE-UI-TC-007 | SC-007 | Logout | Positive | P1 | TS Baseline | Requires Verification | HIGH (once verified) |
| AE-UI-TC-008 | SC-008 | Register — duplicate email | Negative | P1 | TS Baseline | Requires Verification | HIGH (once verified) |
| AE-UI-TC-009 | SC-009 | Contact Us — valid submission | Positive | P2 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-010 | SC-010 | Test Cases page navigation | Positive/Smoke | P3 | TS Baseline | Verified | HIGH (low value) |
| AE-UI-TC-011 | SC-011 | View all products + product details | Positive | P0 | TS Baseline | Verified | HIGH |
| AE-UI-TC-012 | SC-012 | Search — valid matching keyword | Positive | P1 | TS Baseline | Verified | HIGH |
| AE-UI-TC-013 | SC-012 | Search — non-matching keyword / empty result | Negative | P2 | Python Proposed | Requires Verification | MEDIUM |
| AE-UI-TC-014 | SC-012 | Search — investigate relevance anomaly | Diagnostic | P2 | Python Proposed | Requires Verification | NOT RECOMMENDED (investigative) |
| AE-UI-TC-015 | SC-013 | Add multiple products, verify totals | Positive | P0 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-016 | SC-014 | Set/verify product quantity in cart | Positive | P1 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-017 | SC-014 | Invalid/boundary cart quantity | Negative/Boundary | P2 | Python Proposed | Requires Verification | MEDIUM |
| AE-UI-TC-018 | SC-015 | Remove product from cart | Positive | P0 | TS Baseline | Verified | HIGH |
| AE-UI-TC-019 | SC-016 | View category products, switch category | Positive | P2 | TS Baseline | Verified | HIGH |
| AE-UI-TC-020 | SC-017 | View brand products, switch brand | Positive | P2 | TS Baseline | Verified | HIGH |
| AE-UI-TC-021 | SC-018 | Search + cart persists after login | Positive/E2E | P1 | TS Baseline | Requires Verification | MEDIUM |
| AE-UI-TC-022 | SC-019 | Submit product review | Positive | P2 | TS Baseline | Partially Verified | HIGH |
| AE-UI-TC-023 | SC-020 | Add recommended item to cart | Positive | P2 | TS Baseline | Verified (pattern) | HIGH |
| AE-UI-TC-024 | SC-021 | Checkout gate — unauthenticated | Negative/Critical | P0 | Python Proposed | Verified | HIGH |
| AE-UI-TC-025 | SC-022 | Checkout E2E — register during checkout | Positive/E2E | P0 | TS Baseline | Requires Verification | LOW |
| AE-UI-TC-026 | SC-023 | Checkout E2E — register before checkout | Positive/E2E | P0 | TS Baseline | Requires Verification | LOW |
| AE-UI-TC-027 | SC-024 | Checkout E2E — login before checkout | Positive/E2E | P0 | TS Baseline | Requires Verification | LOW |
| AE-UI-TC-028 | SC-025 | Verify checkout address matches registration | Positive | P1 | TS Baseline | Requires Verification | LOW |
| AE-UI-TC-029 | SC-026 | Download invoice after order | Positive | P2 | TS Baseline | Requires Verification | LOW |
| AE-API-TC-001 | SC-001 | GET productsList | Positive | P0 | TS Baseline | Verified | HIGH |
| AE-API-TC-002 | SC-002 | POST productsList → 405 | Negative | P2 | TS Baseline | Verified | HIGH |
| AE-API-TC-003 | SC-003 | GET brandsList | Positive | P1 | TS Baseline | Verified | HIGH |
| AE-API-TC-004 | SC-004 | PUT brandsList → 405 | Negative | P2 | TS Baseline | Verified | HIGH |
| AE-API-TC-005 | SC-005 | POST searchProduct — valid param | Positive | P1 | TS Baseline | Verified | HIGH |
| AE-API-TC-006 | SC-006 | POST searchProduct — missing param | Negative | P1 | TS Baseline | Verified | HIGH |
| AE-API-TC-007 | SC-007 | POST verifyLogin — valid | Positive | P0 | TS Baseline | Verified | HIGH |
| AE-API-TC-008 | SC-008 | POST verifyLogin — invalid | Negative | P1 | TS Baseline | Verified | HIGH |
| AE-API-TC-009 | SC-009 | POST verifyLogin — missing email | Negative | P2 | Python Proposed | Verified | HIGH |
| AE-API-TC-010 | SC-010 | DELETE verifyLogin → 405 | Negative | P3 | Python Proposed | Verified | HIGH |
| AE-API-TC-011 | SC-011 | POST createAccount | Positive/State-Mutating | P0 | Python Proposed | Verified (doc); Execution Restricted | HIGH (once authorized) |
| AE-API-TC-012 | SC-012 | DELETE deleteAccount | Positive/Cleanup | P1 | Python Proposed | Verified (doc); Execution Restricted | HIGH (once authorized) |
| AE-API-TC-013 | SC-013 | PUT updateAccount | Positive/State-Mutating | P2 | Python Proposed | Verified (doc); Execution Restricted | MEDIUM (once authorized) |
| AE-API-TC-014 | SC-014 | GET getUserDetailByEmail | Positive | P2 | Python Proposed | Verified (doc); Execution Restricted | HIGH (once authorized) |
| AE-E2E-TC-001 | SC-001 | Login for API-provisioned account | Hybrid | P1 | Python Proposed | Not started | MEDIUM (sequenced) |
| AE-E2E-TC-002 | SC-002 | Checkout for API-provisioned account | Hybrid | P2 | Python Proposed | Not started | LOW (blocked) |
| AE-E2E-TC-003 | SC-003 | UI product data vs. API oracle cross-check | Hybrid | P1 | Python Proposed | Not started | HIGH (unblocked) |

**Execution Status for every case above: NOT EXECUTED.** No pass/fail claim, and no defect, is made anywhere in this document.

---

## 9. UI Test Cases (Detail)

#### AE-UI-TC-001 — Home page core elements visible
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-001 / REQ-FUNC-HM-001–006 |
| Priority / Risk | P1 / Low |
| Browser Scope | Cross-Browser |
| Preconditions | None (unauthenticated) |
| Test Data | None |

**Steps:** 1. Navigate to `https://automationexercise.com`. 2. Observe the navigation bar. 3. Observe the category panel, brand panel, featured items grid, recommended items, and subscription block.
**Expected Result:** Home page loads; navigation bar shows Home/Products/Cart/Signup-Login/Test Cases/API Testing/Video Tutorials/Contact us; category panel shows Women/Men/Kids; brand panel and featured/recommended items render; subscription email input and submit button are present.
**Notes:** No cleanup required. Ideal smoke-suite anchor (Automation Suitability HIGH, no data dependency).

#### AE-UI-TC-002 — Subscribe from Home page footer
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-002 / REQ-FUNC-HM-007 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | Home page loaded |
| Test Data | TD-SUBSCRIPTION-001 (disposable email — never a real personal address) |

**Steps:** 1. Navigate to Home. 2. Enter a disposable email into the subscription input. 3. Click Submit.
**Expected Result:** A success confirmation is presented — **exact text requires verification**, not invented.
**Notes:** Sends real subscription data to a public system; confirm acceptable for CI before automating (mirrors [04](04-Test-Plan.md) §16 note on the analogous Contact Us case).

#### AE-UI-TC-003 — Subscribe from Cart page footer
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-003 / REQ-FUNC-HM-007 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | Cart page loaded (empty or non-empty) |
| Test Data | TD-SUBSCRIPTION-001 |

**Steps:** 1. Navigate to `/view_cart`. 2. Enter a disposable email into the subscription input. 3. Click Submit.
**Expected Result:** Same success confirmation as AE-UI-TC-002 — **exact text requires verification**.
**Notes:** Flagged in [06](06-Test-Scenarios.md) §15 as a **CONSOLIDATE (proposed)** candidate with TC-002 — kept as a distinct case pending QA Lead decision.

#### AE-UI-TC-004 — Register new user (full lifecycle: create, verify, delete)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-004 / REQ-FUNC-SL-001, REQ-FUNC-SL-006 |
| Priority / Risk | **P0** / High (verification gap — highest-value case to execute first per [05](05-Test-Strategy.md) §2) |
| Browser Scope | Cross-Browser (once stable on Chromium) |
| Preconditions | None |
| Test Data | TD-USER-NEW-001 (uniquely generated name/email + full address field set per the verified `createAccount` schema) |

**Steps:** 1. Navigate to Home, click Signup/Login. 2. Enter unique name and email in the Signup form, click Signup. 3. Fill account information (title, password, DOB) and address details. 4. Click Create Account. 5. Confirm account-created signal, click Continue. 6. Confirm a "logged in as [name]" signal is shown. 7. Delete the account via the account-deletion UI control. 8. Confirm an account-deleted signal.
**Expected Result:** Steps 5–8 each produce a distinct, observable confirmation — **exact wording requires verification** (TS baseline references "ACCOUNT CREATED!"/"ACCOUNT DELETED!" text, REFERENCE-ONLY, not independently confirmed by this project).
**Cleanup:** Step 7–8 **is** the cleanup — this case is only valid if the deletion sub-steps are confirmed to succeed.
**Notes:** Data-mutating; must use a uniquely generated email every execution (Section 13). This is the single most important case to execute first, since AE-UI-TC-005/007/008/021/025/026/027/028/029 and AE-API-TC-007/AE-E2E-TC-001/002 all depend, directly or indirectly, on Signup/Login behavior being confirmed.

#### AE-UI-TC-005 — Login with valid credentials
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-005 / REQ-FUNC-SL-003 |
| Priority / Risk | **P0** / High (verification gap) |
| Browser Scope | Cross-Browser |
| Preconditions | A valid, existing account (from AE-UI-TC-004 or a pre-provisioned reusable account) |
| Test Data | TD-USER-VALID-001 |

**Steps:** 1. Navigate to `/login`. 2. Enter valid email and password in the Login form. 3. Click Login.
**Expected Result:** User reaches an authenticated state with a "logged in as [name]" signal — **exact UI signal requires verification**.
**Notes:** Blocked until a valid account exists (AE-UI-TC-004 or an equivalent pre-provisioned account).

#### AE-UI-TC-006 — Login with invalid credentials
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-006 / REQ-FUNC-SL-004 |
| Priority / Risk | **P0** / Medium |
| Browser Scope | Cross-Browser |
| Preconditions | None |
| Test Data | TD-USER-INVALID-001 (fabricated, non-existent email/password) |

**Steps:** 1. Navigate to `/login`. 2. Enter a fabricated, non-existent email and password. 3. Click Login.
**Expected Result:** User remains on `/login` (no navigation) and the inline message **"Your email or password is incorrect!"** is displayed — **VERIFIED**, Step 2.
**Notes:** No account dependency; cheapest, strongest P0 case — recommend first in execution order alongside AE-UI-TC-024 and AE-API-TC-001/007.

#### AE-UI-TC-007 — Logout from an authenticated session
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-007 / REQ-FUNC-SL-005/006 |
| Priority / Risk | P1 / Medium (verification gap) |
| Browser Scope | Chromium |
| Preconditions | User authenticated (AE-UI-TC-005) |
| Test Data | TD-USER-VALID-001 |

**Steps:** 1. Complete AE-UI-TC-005 to reach an authenticated state. 2. Click Logout.
**Expected Result:** User returns to an unauthenticated state, with `/login` (or equivalent) reachable again — **exact redirect target requires verification**.
**Notes:** Depends entirely on AE-UI-TC-005.

#### AE-UI-TC-008 — Register with an already-registered email
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-008 / REQ-FUNC-SL-002 |
| Priority / Risk | P1 / Medium |
| Browser Scope | Chromium |
| Preconditions | A known, durable, already-registered account |
| Test Data | TD-USER-EXISTING-001 |

**Steps:** 1. Navigate to `/login`. 2. Enter a new name with the already-registered email in the Signup form. 3. Click Signup.
**Expected Result:** Registration is rejected with an error message — TS baseline references **"Email Address already exist!"**, marked here as **REQUIRES VERIFICATION** since this project has not independently confirmed it.
**Notes:** Requires one durable reusable "existing user" account (Section 13).

#### AE-UI-TC-009 — Submit Contact Us form with file upload
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-009 / REQ-FUNC-CU-001/002/004 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-CONTACT-001 (name, disposable email, subject, message), TD-FILE-001 (small sample text file) |

**Steps:** 1. Navigate to `/contact_us`. 2. Enter name, email, subject, message. 3. Attach TD-FILE-001. 4. Click Submit and accept any browser confirmation dialog.
**Expected Result:** A success confirmation is displayed — **exact text requires verification**.
**Notes:** Sends a real message to the site's feedback channel — confirm CI-appropriateness before automating (same caveat as TC-002/003).

#### AE-UI-TC-010 — Navigate to the Test Cases page
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-010 / Navigation only |
| Priority / Risk | P3 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | None |

**Steps:** 1. Navigate to Home. 2. Click "Test Cases" in the navigation bar.
**Expected Result:** The site's own published Test Cases page renders — **VERIFIED**, Step 2.
**Notes:** Low business value (validates a QA-reference page on the AUT itself, not a product feature) — [06](06-Test-Scenarios.md) recommends deprioritizing; retained here at P3 pending that QA Lead decision.

#### AE-UI-TC-011 — View all products and product detail fields
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-011 / REQ-FUNC-PR-001/002 |
| Priority / Risk | **P0** / Low |
| Browser Scope | Cross-Browser |
| Preconditions | None |
| Test Data | TD-PRODUCT-001 (any catalog product, preferably sourced live via AE-API-TC-001) |

**Steps:** 1. Navigate to `/products`. 2. Confirm the product grid renders. 3. Click "View Product" on any item. 4. Confirm name, category path, price, quantity input, Add to Cart, Availability, Condition, and Brand are all present.
**Expected Result:** All fields listed in Step 4 render with non-empty values — **VERIFIED**, Step 2.
**Notes:** No account dependency; high-confidence regression anchor.

#### AE-UI-TC-012 — Search with a valid, matching keyword
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-012 / REQ-FUNC-PR-003/004 |
| Priority / Risk | P1 / Medium |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-SEARCH-VALID-001 (e.g., a keyword matching a known product name) |

**Steps:** 1. Navigate to `/products`. 2. Enter TD-SEARCH-VALID-001 in the search box. 3. Submit the search.
**Expected Result:** A "SEARCHED PRODUCTS" section renders containing at least the products whose names contain the keyword — **VERIFIED functional**, Step 2; full relevance-rule correctness is addressed separately in TC-014.
**Notes:** No account dependency.

#### AE-UI-TC-013 — Search with a non-matching keyword
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-012 / REQ-FUNC-PR-004 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-SEARCH-NOMATCH-001 (a keyword expected to match nothing in the catalog) |

**Steps:** 1. Navigate to `/products`. 2. Enter TD-SEARCH-NOMATCH-001. 3. Submit the search.
**Expected Result:** An empty or "no results" state is shown — **REQUIRES VERIFICATION** (not yet independently observed; this project has only observed a positive-match result).
**Notes:** New negative case identified during Step 7 design, not present in the TS baseline's positive-only search coverage.

#### AE-UI-TC-014 — Investigate the search-relevance anomaly
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-012 / REQ-FUNC-PR-004 |
| Priority / Risk | P2 / Medium (open question) |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-SEARCH-ANOMALY-001 (the keyword "dress," which in Step 2 returned "Sleeves Top and Short - Blue & Pink" without an obvious name match) |

**Steps:** 1. Navigate to `/products`. 2. Search TD-SEARCH-ANOMALY-001. 3. For each returned item, inspect its name, category, and (via AE-API-TC-005) its full product record to determine which field actually matched.
**Expected Result:** Not defined as pass/fail — this is a diagnostic case whose outcome is a documented explanation of the matching rule, feeding back into TC-012's expected-result definition.
**Notes:** Automation Suitability **NOT RECOMMENDED** as a standing regression test until the root cause is known; valuable once as a manual/exploratory investigation.

#### AE-UI-TC-015 — Add multiple products to cart, verify totals
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-013 / REQ-FUNC-CT-001/004 |
| Priority / Risk | **P0** / Medium |
| Browser Scope | Cross-Browser |
| Preconditions | None |
| Test Data | TD-PRODUCT-002, TD-PRODUCT-003 (two distinct catalog products) |

**Steps:** 1. Add TD-PRODUCT-002 to cart from its detail page. 2. Add TD-PRODUCT-003 to cart. 3. Navigate to `/view_cart`. 4. Confirm both line items, their individual prices, and a correct summed cart total.
**Expected Result:** Both items appear with correct price × quantity line totals and a correct cart-level total — **PARTIALLY VERIFIED**, Step 2 confirmed this only for a single item.
**Notes:** Extends Step 2's single-item evidence to the multi-item case explicitly called out as untested in [03](03-Requirement-Analysis.md) §14.

#### AE-UI-TC-016 — Set and verify a specific cart quantity
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-014 / REQ-FUNC-CT-002 |
| Priority / Risk | P1 / Medium |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-PRODUCT-001, quantity = 4 (matching the TS baseline's own example value, REFERENCE-ONLY) |

**Steps:** 1. Open TD-PRODUCT-001's detail page. 2. Set quantity to 4 in the quantity input. 3. Click Add to Cart. 4. Navigate to `/view_cart`. 5. Confirm the line shows quantity 4 and the correct line total.
**Expected Result:** Quantity and line total reflect 4 units — **PARTIALLY VERIFIED**, Step 2 only observed the default quantity of 1.
**Notes:** No account dependency.

#### AE-UI-TC-017 — Invalid/boundary cart quantity
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-014 / REQ-FUNC-CT-002 |
| Priority / Risk | P2 / Medium (open question) |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-QUANTITY-INVALID-001 (a zero or negative value — exact boundary not yet defined, per [06](06-Test-Scenarios.md) §8) |

**Steps:** 1. Open a product detail page. 2. Attempt to set the quantity input to TD-QUANTITY-INVALID-001. 3. Attempt to add to cart.
**Expected Result:** Not yet known — **REQUIRES VERIFICATION** whether the field rejects the input, clamps it, or accepts it; this project makes no claim about which, per Open Question 5 ([03](03-Requirement-Analysis.md) §12, TS `BR-004` is REFERENCE-ONLY).
**Notes:** New boundary case identified during Step 7 design; no numeric boundary is invented.

#### AE-UI-TC-018 — Remove a product from the cart
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-015 / REQ-FUNC-CT-003 |
| Priority / Risk | **P0** / Low |
| Browser Scope | Cross-Browser |
| Preconditions | At least one product already in cart |
| Test Data | TD-PRODUCT-001 |

**Steps:** 1. Add TD-PRODUCT-001 to cart. 2. Navigate to `/view_cart`. 3. Click the remove control on the line item.
**Expected Result:** The item is removed and the cart returns to its empty state **without a full page reload** (client-side/AJAX-driven) — **VERIFIED**, Step 2.
**Notes:** Automation must wait on the client-side DOM update, not a navigation event (REQ-UI-005).

#### AE-UI-TC-019 — View category products and switch category
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-016 / REQ-FUNC-PR-005 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-CATEGORY-001, TD-CATEGORY-002 |

**Steps:** 1. Navigate to Home or Products. 2. Click a category link (e.g., Women). 3. Confirm the category product listing renders. 4. Click a different category/sub-category link. 5. Confirm the listing updates.
**Expected Result:** Category-scoped product listings render and update correctly — **VERIFIED at route level**, Step 2; category-ID-to-name mapping remains an open question affecting exact `TD-CATEGORY-*` values (Step 8).
**Notes:** No account dependency.

#### AE-UI-TC-020 — View brand products and switch brand
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-017 / REQ-FUNC-PR-006 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-BRAND-001 (e.g., "Polo"), TD-BRAND-002 (e.g., "H&M") |

**Steps:** 1. From a product detail page or Products page, click a brand link. 2. Confirm the brand product listing renders. 3. Click a different brand link. 4. Confirm the listing updates.
**Expected Result:** Brand-scoped listings render and update correctly — **VERIFIED**, Step 2.
**Notes:** No account dependency.

#### AE-UI-TC-021 — Search, add to cart, verify persistence after login
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-018 / REQ-FUNC-PR-003, REQ-FUNC-CT-005 |
| Priority / Risk | P1 / High (depends on Login) |
| Browser Scope | Chromium |
| Preconditions | A valid account (AE-UI-TC-004/005) |
| Test Data | TD-SEARCH-VALID-001, TD-USER-VALID-001 |

**Steps:** 1. Search and add a product to cart while unauthenticated. 2. Log in (AE-UI-TC-005). 3. Return to `/view_cart`. 4. Confirm the previously added item is still present.
**Expected Result:** Cart contents persist across the login transition — **REQUIRES VERIFICATION** (session-persistence behavior is unconfirmed, [03](03-Requirement-Analysis.md) REQ-FUNC-SL-006/CT-005).
**Notes:** Blocked on AE-UI-TC-005.

#### AE-UI-TC-022 — Submit a product review
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-019 / Product Review (module-level) |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | TD-REVIEW-001 (name, disposable email, review text) |

**Steps:** 1. Open a product detail page. 2. Scroll to the review form. 3. Enter name, email, and review text. 4. Click Submit.
**Expected Result:** A success confirmation is displayed — **exact text requires verification**.
**Notes:** No account dependency observed in Step 2; fields verified present, submission not yet exercised.

#### AE-UI-TC-023 — Add a recommended item to cart
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-020 / Recommended Items, REQ-FUNC-CT-001 |
| Priority / Risk | P2 / Low |
| Browser Scope | Chromium |
| Preconditions | None |
| Test Data | None — item selected from the Home page's Recommended Items carousel |

**Steps:** 1. Navigate to Home. 2. Locate the Recommended Items section. 3. Click Add to Cart on an item. 4. Navigate to `/view_cart`.
**Expected Result:** The item appears correctly on the cart page, following the same confirmed add-to-cart pattern as AE-UI-TC-015 — HIGH confidence by pattern extension, not independently re-verified.
**Notes:** No account dependency.

#### AE-UI-TC-024 — Checkout gate blocks unauthenticated access
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-021 / REQ-FUNC-CO-001, REQ-BUS-004, BR-003 |
| Priority / Risk | **P0** / High (strongest available Checkout-area evidence) |
| Browser Scope | Cross-Browser |
| Preconditions | Unauthenticated session, at least one item in cart |
| Test Data | TD-PRODUCT-001 |

**Steps:** 1. Add TD-PRODUCT-001 to cart. 2. Navigate to `/view_cart`. 3. Click "Proceed To Checkout."
**Expected Result:** A modal is displayed reading **"Register / Login account to proceed on checkout."** with "Register / Login" and "Continue On Cart" options — **VERIFIED**, Step 2.
**Notes:** No account dependency; recommend automating before any Checkout E2E case (TC-025–029).

#### AE-UI-TC-025 — Checkout E2E: register during checkout
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-022 / REQ-FUNC-CO-002–006 |
| Priority / Risk | **P0** / **High — major evidence gap** |
| Browser Scope | Chromium only, until verified |
| Preconditions | Unauthenticated session, item in cart |
| Test Data | TD-PRODUCT-001, TD-USER-NEW-002, TD-CHECKOUT-001 (order comment, dummy payment details — never real payment data) |

**Steps:** 1. Add product to cart, click Proceed To Checkout. 2. From the gate (AE-UI-TC-024), choose Register/Login and complete registration inline. 3. Return to cart, click Proceed To Checkout again. 4. Confirm address details and order review. 5. Enter order comment, click Place Order. 6. Enter payment details, confirm order. 7. Delete the account created in Step 2.
**Expected Result:** **REQUIRES VERIFICATION at every step from 3 onward** — this project has not confirmed whether `/checkout` is a distinct route from `/view_cart` ([03](03-Requirement-Analysis.md) §5 row 1), nor the exact address/payment/confirmation UI. No expected text is invented.
**Cleanup:** Step 7 is mandatory — account must be deleted regardless of outcome.
**Notes:** Do **not** automate before manual/exploratory verification resolves the route/flow question.

#### AE-UI-TC-026 — Checkout E2E: register before checkout
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-023 / REQ-FUNC-CO-002–006 |
| Priority / Risk | **P0** / High |
| Browser Scope | Chromium only, until verified |
| Preconditions | None |
| Test Data | TD-USER-NEW-003, TD-PRODUCT-001, TD-CHECKOUT-001 |

**Steps:** 1. Register a new account (AE-UI-TC-004 pattern, without deleting yet). 2. Add product to cart. 3. Click Proceed To Checkout. 4. Confirm address details and order review. 5. Enter order comment, click Place Order. 6. Enter payment details, confirm order. 7. Delete the account.
**Expected Result:** **REQUIRES VERIFICATION**, same basis as AE-UI-TC-025.
**Cleanup:** Step 7 mandatory.
**Notes:** [06](06-Test-Scenarios.md) flags TC-025/026/027 as a **CONSOLIDATE-candidate** once the core flow is verified — kept distinct here pending that decision.

#### AE-UI-TC-027 — Checkout E2E: login before checkout
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-024 / REQ-FUNC-CO-002–006 |
| Priority / Risk | **P0** / High |
| Browser Scope | Chromium only, until verified |
| Preconditions | A valid, existing account |
| Test Data | TD-USER-VALID-001, TD-PRODUCT-001, TD-CHECKOUT-001 |

**Steps:** 1. Log in (AE-UI-TC-005). 2. Add product to cart. 3. Click Proceed To Checkout. 4. Confirm address details and order review. 5. Enter order comment, click Place Order. 6. Enter payment details, confirm order.
**Expected Result:** **REQUIRES VERIFICATION**, same basis as AE-UI-TC-025/026.
**Notes:** Depends on AE-UI-TC-005 succeeding first.

#### AE-UI-TC-028 — Verify checkout address matches registration
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-025 / REQ-FUNC-CO-002/003 |
| Priority / Risk | P1 / High |
| Browser Scope | Chromium |
| Preconditions | A new account with complete address information |
| Test Data | TD-USER-NEW-004 (with full address fields) |

**Steps:** 1. Register a new account with complete address data. 2. Add a product to cart. 3. Proceed to checkout. 4. Compare the displayed delivery and billing addresses against the registration data.
**Expected Result:** Displayed addresses match registration input — **REQUIRES VERIFICATION**; entirely dependent on AE-UI-TC-025/026's underlying flow being confirmed first.
**Notes:** Not executable in isolation.

#### AE-UI-TC-029 — Download invoice after a completed order
| Field | Value |
|---|---|
| Scenario / Requirement | AE-UI-SC-026 / REQ-FUNC-CO-006 |
| Priority / Risk | P2 / Medium |
| Browser Scope | Chromium |
| Preconditions | A completed order (AE-UI-TC-025/026/027) |
| Test Data | Same as the completing checkout case |

**Steps:** 1. Complete an order (any of TC-025/026/027). 2. Locate and click a "Download Invoice" control. 3. Confirm a file is produced in the configured download location.
**Expected Result:** **REQUIRES VERIFICATION** — depends entirely on order completion being confirmed first; also introduces a browser-download-directory environment dependency, a Framework Architecture concern, not resolved here.
**Notes:** Lowest-priority Checkout-area case to execute, since it is furthest downstream of the unresolved flow.

---

## 10. API Test Cases (Detail)

#### AE-API-TC-001 — GET /api/productsList
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-001 / REQ-API-001 |
| Priority / Risk | **P0** / Low |
| Endpoint / Method | `/api/productsList` / GET |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `GET /api/productsList`.
**Expected Result:** HTTP 200; response body is a JSON product list — **VERIFIED**, Step 2.
**Notes:** No cleanup; ideal for the fastest-feedback API smoke check.

#### AE-API-TC-002 — POST /api/productsList (unsupported method)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-002 / REQ-API-002 |
| Priority / Risk | P2 / Low |
| Endpoint / Method | `/api/productsList` / POST |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `POST /api/productsList` (no body required).
**Expected Result:** HTTP 405, message "This request method is not supported." — **VERIFIED**, Step 2.
**Notes:** No cleanup.

#### AE-API-TC-003 — GET /api/brandsList
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-003 / REQ-API-003 |
| Priority / Risk | P1 / Low |
| Endpoint / Method | `/api/brandsList` / GET |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `GET /api/brandsList`.
**Expected Result:** HTTP 200; response body is a JSON brand list — **VERIFIED**, Step 2.
**Notes:** No cleanup.

#### AE-API-TC-004 — PUT /api/brandsList (unsupported method)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-004 / REQ-API-004 |
| Priority / Risk | P2 / Low |
| Endpoint / Method | `/api/brandsList` / PUT |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `PUT /api/brandsList`.
**Expected Result:** HTTP 405, message "This request method is not supported." — **VERIFIED**, Step 2.
**Notes:** No cleanup.

#### AE-API-TC-005 — POST /api/searchProduct (valid parameter)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-005 / REQ-API-005 |
| Priority / Risk | P1 / Low |
| Endpoint / Method | `/api/searchProduct` / POST |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `POST /api/searchProduct` with `search_product = TD-SEARCH-VALID-001`.
**Expected Result:** HTTP 200; response body is a JSON list of matching products — **VERIFIED**, Step 2. Also usable as the oracle for AE-UI-TC-014's investigation.
**Notes:** No cleanup.

#### AE-API-TC-006 — POST /api/searchProduct (missing parameter)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-006 / REQ-API-006 |
| Priority / Risk | P1 / Low |
| Endpoint / Method | `/api/searchProduct` / POST |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `POST /api/searchProduct` with no `search_product` parameter.
**Expected Result:** HTTP 400, message "Bad request, search_product parameter is missing in POST request." — **VERIFIED**, Step 2.
**Notes:** No cleanup.

#### AE-API-TC-007 — POST /api/verifyLogin (valid)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-007 / REQ-API-007 |
| Priority / Risk | **P0** / High (shares the Signup/Login dependency) |
| Endpoint / Method | `/api/verifyLogin` / POST |
| Auth | Credentials as parameters |
| Preconditions | A valid, existing account |

**Steps:** 1. Send `POST /api/verifyLogin` with `email`/`password` for TD-USER-VALID-001.
**Expected Result:** HTTP 200, message "User exists!" — **VERIFIED (documentation)**, Step 2; **execution blocked until a valid account exists** (same dependency as AE-UI-TC-004/005).
**Notes:** No cleanup; read-only against an existing account.

#### AE-API-TC-008 — POST /api/verifyLogin (invalid)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-008 / REQ-API-010 |
| Priority / Risk | P1 / Low |
| Endpoint / Method | `/api/verifyLogin` / POST |
| Auth | Credentials as parameters |
| Preconditions | None |

**Steps:** 1. Send `POST /api/verifyLogin` with fabricated `email`/`password`.
**Expected Result:** HTTP 404, message "User not found!" — **VERIFIED**, Step 2.
**Notes:** No account dependency; no cleanup.

#### AE-API-TC-009 — POST /api/verifyLogin (missing email)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-009 / REQ-API-008 |
| Priority / Risk | P2 / Low |
| Endpoint / Method | `/api/verifyLogin` / POST |
| Auth | `password` only |
| Preconditions | None |

**Steps:** 1. Send `POST /api/verifyLogin` with `password` but no `email`.
**Expected Result:** HTTP 400, message "Bad request, email or password parameter is missing in POST request." — **VERIFIED**, Step 2 (promoted from TS-deferred status per [06](06-Test-Scenarios.md) §14).
**Notes:** No cleanup.

#### AE-API-TC-010 — DELETE /api/verifyLogin (unsupported method)
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-010 / REQ-API-009 |
| Priority / Risk | P3 / Low |
| Endpoint / Method | `/api/verifyLogin` / DELETE |
| Auth | None |
| Preconditions | None |

**Steps:** 1. Send `DELETE /api/verifyLogin`.
**Expected Result:** HTTP 405, message "This request method is not supported." — **VERIFIED**, Step 2 (promoted from TS-deferred).
**Notes:** No cleanup.

#### AE-API-TC-011 — POST /api/createAccount
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-011 / REQ-API-011 |
| Priority / Risk | **P0** / High (state-mutating, shared environment) |
| Endpoint / Method | `/api/createAccount` / POST |
| Auth | None (open endpoint) |
| Preconditions | Uniquely generated account data |

**Steps:** 1. Send `POST /api/createAccount` with the full 16-field payload (name, email, password, title, birth_date/month/year, firstname, lastname, company, address1, address2, country, zipcode, state, city, mobile_number) using TD-USER-NEW-001.
**Expected Result:** HTTP 201, message "User created!" — **VERIFIED at the documentation level only**, Step 2. **This project may not execute this case (create a real account) without explicit QA Lead authorization** — this assistant does not perform account creation unilaterally.
**Cleanup:** Must always pair with AE-API-TC-012 in the same test run.
**Notes:** Highest-strategic-value proposed API case — unblocks Signup verification and both Hybrid Login-related cases.

#### AE-API-TC-012 — DELETE /api/deleteAccount
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-012 / REQ-API-012 |
| Priority / Risk | P1 / Medium |
| Endpoint / Method | `/api/deleteAccount` / DELETE |
| Auth | `email`/`password` |
| Preconditions | An account created via AE-API-TC-011 |

**Steps:** 1. Send `DELETE /api/deleteAccount` with the `email`/`password` used in AE-API-TC-011.
**Expected Result:** HTTP 200, message "Account deleted!" — **VERIFIED at the documentation level only**; same execution-authorization restriction as TC-011.
**Notes:** Never runs standalone — this **is** the cleanup for TC-011 and must never be skipped once TC-011 runs.

#### AE-API-TC-013 — PUT /api/updateAccount
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-013 / REQ-API-013 |
| Priority / Risk | P2 / Medium |
| Endpoint / Method | `/api/updateAccount` / PUT |
| Auth | Credentials as part of payload |
| Preconditions | An account created via AE-API-TC-011 |

**Steps:** 1. Send `PUT /api/updateAccount` with the same 16-field shape as `createAccount`, changing at least one field, for the account from AE-API-TC-011.
**Expected Result:** HTTP 200, message "User updated!" — **VERIFIED at the documentation level only**; execution requires the same authorization as TC-011/012.
**Cleanup:** The account must still be deleted via AE-API-TC-012 afterward.
**Notes:** State-mutating; must not run without the TC-011/012 pairing.

#### AE-API-TC-014 — GET /api/getUserDetailByEmail
| Field | Value |
|---|---|
| Scenario / Requirement | AE-API-SC-014 / REQ-API-014 |
| Priority / Risk | P2 / Low |
| Endpoint / Method | `/api/getUserDetailByEmail` / GET |
| Auth | `email` parameter |
| Preconditions | An existing account |

**Steps:** 1. Send `GET /api/getUserDetailByEmail?email=...` for an existing account (from AE-API-TC-011 or TD-USER-VALID-001).
**Expected Result:** HTTP 200, JSON user detail body — **VERIFIED at the documentation level only**; read-only once an account exists, so execution is lower-risk than TC-011/012/013 but still requires that account to exist first.
**Notes:** Valuable as the read-side oracle for a future Hybrid profile-verification pattern.

---

## 11. Hybrid / E2E Test Cases (Detail)

#### AE-E2E-TC-001 — Login for an API-provisioned account
| Field | Value |
|---|---|
| Scenario / Requirement | AE-E2E-SC-001 / REQ-E2E-001 |
| Priority / Risk | P1 / Medium |
| Baseline Status | Python Proposed (TS planning-only, never implemented there either) |

**What API does:** Creates a uniquely-identified account via `POST /api/createAccount` (AE-API-TC-011), bypassing the UI signup form entirely.
**What UI does:** Logs in through the actual `/login` UI form using the API-created credentials (same interaction as AE-UI-TC-005), then confirms the authenticated-state signal.
**Why both layers are needed:** A pure API test never exercises the login *UI*; a pure UI test that also does UI-based signup can't isolate "does Login work" from "does Signup work" — this test proves Login correctness independent of how the account was created, and is faster/more reliable to set up than UI-driven signup.
**State flow:** API creates account → UI consumes the same email/password → API deletes the account in cleanup.
**Steps:** 1. Execute AE-API-TC-011 to create an account. 2. Navigate to `/login` and log in with those credentials. 3. Confirm the authenticated-state UI signal. 4. Execute AE-API-TC-012 to delete the account.
**Expected Result:** Login succeeds via the UI for an account that never touched the UI signup form — **not started**; sequenced strictly **after** AE-UI-TC-005 is independently confirmed working, per [05](05-Test-Strategy.md) §6.
**Notes:** Blocked on both AE-API-TC-011/012 authorization and AE-UI-TC-005 verification.

#### AE-E2E-TC-002 — Checkout completion for an API-provisioned account
| Field | Value |
|---|---|
| Scenario / Requirement | AE-E2E-SC-002 / REQ-E2E-002 |
| Priority / Risk | P2 / Medium |
| Baseline Status | Python Proposed (TS planning-only, never implemented there either) |

**What API does:** Creates a uniquely-identified account (`createAccount`), as in AE-E2E-TC-001.
**What UI does:** Completes the full Checkout journey (login → cart → checkout → address → payment → confirmation) as in AE-UI-TC-027.
**Why both layers are needed:** Confirms Checkout has no hidden dependency on the *UI* registration flow specifically, while reducing the setup cost of an already-expensive E2E test.
**State flow:** API creates account → UI performs the entire checkout journey using it → API deletes the account in cleanup regardless of checkout outcome.
**Steps:** 1. Execute AE-API-TC-011. 2. Perform AE-UI-TC-027's steps using the API-created account. 3. Execute AE-API-TC-012.
**Expected Result:** **Not started; currently blocked** on AE-UI-TC-022/023/024/027 (Checkout) being independently verified — the same route/flow open question applies here as there.
**Notes:** Lowest-readiness case in this document — do not schedule before the Checkout-area verification gap closes.

#### AE-E2E-TC-003 — UI product listing vs. API product data cross-check
| Field | Value |
|---|---|
| Scenario / Requirement | AE-E2E-SC-003 / REQ-E2E-003 |
| Priority / Risk | P1 / Low |
| Baseline Status | Python Proposed (new — no TS equivalent) |

**What API does:** Retrieves the full product list via `GET /api/productsList` (AE-API-TC-001).
**What UI does:** Renders the Products page (AE-UI-TC-011).
**Why both layers are needed:** Removes reliance on hard-coded expected values in UI assertions; catches a UI/backend rendering mismatch that neither layer alone could catch (a pure UI test has no independent source of truth; a pure API test never renders anything).
**State flow:** API result used as the oracle → UI values compared against it — no state is created or mutated by either side.
**Steps:** 1. Execute AE-API-TC-001, capture product names/prices. 2. Execute AE-UI-TC-011, capture the same fields as rendered. 3. Compare the two sets for consistency.
**Expected Result:** UI-rendered names/prices match the API's data — **not started**, but **not blocked** by the Signup/Login gap, unlike TC-001/002 above; this is the one Hybrid case with no identity-flow dependency and the most immediately executable once Step 9 approves it.
**Notes:** No account, no cleanup, no data mutation — the lowest-risk Hybrid case in this document.

---

## 12. Verification-Dependent Cases (Consolidated View)

Every case below has `Verification Status = Requires Verification` and must **not** be treated as automation-ready regardless of any other field:

| TC ID | Unknown | Depends On |
|---|---|---|
| AE-UI-TC-004/005/007/008 | Exact Signup/Login UI signals and error text | Direct execution under QA Lead direction |
| AE-UI-TC-013/017 | Non-matching-search and invalid-quantity behavior | Direct execution |
| AE-UI-TC-021 | Cart/session persistence across login | AE-UI-TC-005 |
| AE-UI-TC-022/025/026/027/028/029 | `/checkout` route identity, address/payment/confirmation/invoice UI | Direct exploratory verification, independent of any other case |
| AE-API-TC-011/012/013/014 | Live execution behavior (documentation-verified only) | **QA Lead authorization** — this assistant cannot self-authorize account creation/deletion |
| AE-E2E-TC-001/002 | Everything their dependent UI/API cases depend on | See above |

No expected result for any of these cases states a specific message/behavior as fact where it is not already Step-2-VERIFIED.

## 13. Shared Environment / Data Dependencies

| Concern | Cases |
|---|---|
| Account creation | AE-UI-TC-004/025/026/028; AE-API-TC-011; AE-E2E-TC-001/002 |
| Account deletion (cleanup) | AE-UI-TC-004/025/026 (Step 7/postcondition); AE-API-TC-012; AE-E2E-TC-001/002 |
| Requires a durable, reusable existing account | AE-UI-TC-005/007/021/027; AE-API-TC-007/008/014; AE-E2E-TC-001 |
| Requires a durable, known-existing account (for duplicate-email negative) | AE-UI-TC-008 |
| Cart state mutation | AE-UI-TC-015/016/017/018/021/023/025–027 |
| API state mutation | AE-API-TC-011/012/013 |
| Collision risk if run concurrently without unique data | Every case in the two rows above — must use uniquely generated identifiers per [05](05-Test-Strategy.md) §10/§15 |
| Execution-order dependency (explicitly, by design) | AE-UI-TC-007 (needs TC-005), AE-UI-TC-021 (needs TC-005), AE-UI-TC-025–029 (chained), AE-API-TC-012/013 (needs TC-011), AE-E2E-TC-001/002 (needs both layers) — each is documented, not accidental |
| Parallelization concern | Any two cases above sharing the *same* durable reusable account must not run concurrently; uniquely-generated-data cases are safe to parallelize per [05](05-Test-Strategy.md) §14 |

No destructive operation (account creation or deletion) was executed while producing this document — this step is design-only, per instruction.

## 14. Traceability Summary

Full chain example: `REQ-BUS-004` → `AE-UI-SC-021` → `AE-UI-TC-024`. Every Test Case in Section 8 carries its Scenario and Requirement reference inline — no case exists without both. Critical (`P0`) requirements without full case coverage are all explicitly explained: the Checkout-area `P0` cases (TC-025–027) exist and are documented, but their Automation Suitability is LOW and Verification Status is Requires Verification — they are **covered by design, not yet covered by evidence** (Section 16).

## 15. TypeScript Baseline Reconciliation (Test Case Level)

| TS Test Case | Python Test Case(s) | Status | Note |
|---|---|---|---|
| AE-TC-UI-001 | AE-UI-TC-004 | RETAIN + MODIFY | Priority elevated to P0; framed as verification-priority |
| AE-TC-UI-002 | AE-UI-TC-005 | RETAIN + MODIFY | Same |
| AE-TC-UI-003 | AE-UI-TC-006 | RETAIN | Already independently VERIFIED with exact text |
| AE-TC-UI-004 | AE-UI-TC-007 | RETAIN + MODIFY | Verification-dependent |
| AE-TC-UI-005 | AE-UI-TC-008 | RETAIN | Exact error text downgraded from TS's stated fact to REQUIRES VERIFICATION |
| AE-TC-UI-006 | AE-UI-TC-009 | RETAIN | — |
| AE-TC-UI-007 | AE-UI-TC-010 | RETAIN, FLAG | Low value, P3 |
| AE-TC-UI-008 | AE-UI-TC-011 | RETAIN | Already VERIFIED |
| AE-TC-UI-009 | AE-UI-TC-012 | RETAIN + MODIFY | Split — anomaly investigation extracted as TC-014 |
| AE-TC-UI-010 | AE-UI-TC-002 | RETAIN | — |
| AE-TC-UI-011 | AE-UI-TC-003 | RETAIN, CONSOLIDATE-candidate | With TC-002 |
| AE-TC-UI-012 | AE-UI-TC-015 | RETAIN | Extended to genuinely multi-item |
| AE-TC-UI-013 | AE-UI-TC-016 | RETAIN | — |
| AE-TC-UI-014 | AE-UI-TC-025 | RETAIN, FLAG | Route/flow dependency explicit |
| AE-TC-UI-015 | AE-UI-TC-026 | RETAIN, FLAG | Same |
| AE-TC-UI-016 | AE-UI-TC-027 | RETAIN, FLAG | Same |
| AE-TC-UI-017 | AE-UI-TC-018 | RETAIN | Already VERIFIED |
| AE-TC-UI-018 | AE-UI-TC-019 | RETAIN | — |
| AE-TC-UI-019 | AE-UI-TC-020 | RETAIN | — |
| AE-TC-UI-020 | AE-UI-TC-021 | RETAIN | — |
| AE-TC-UI-021 | AE-UI-TC-022 | RETAIN | — |
| AE-TC-UI-022 | AE-UI-TC-023 | RETAIN | — |
| AE-TC-UI-023 | AE-UI-TC-028 | RETAIN, FLAG | — |
| AE-TC-UI-024 | AE-UI-TC-029 | RETAIN, FLAG | — |
| TC-25/26 | — | DEFER (reaffirmed) | No Test Case produced |
| AE-TC-API-001–008 | AE-API-TC-001–010 | RETAIN + EXPAND | 2 new negative cases (TC-009/010) promoted from TS-deferred |
| API-11–14 (TS-deferred) | AE-API-TC-011–014 | **PROPOSE NEW** | Promoted on stronger Python evidence ([06](06-Test-Scenarios.md) §14) |
| AE-TC-HYBRID-001/002 (TS planning-only) | AE-E2E-TC-001/002 | RETAIN as proposal | Still unimplemented anywhere |
| (none) | AE-E2E-TC-003 | **PROPOSE NEW** | Python-originated |
| (none) | AE-UI-TC-001, AE-UI-TC-024 | **PROPOSE NEW** | Python-originated (Home smoke, Checkout gate) |
| (none) | AE-UI-TC-013, 014, 017 | **PROPOSE NEW** | Additional negative/boundary/diagnostic coverage identified in Step 7 design, no TS equivalent |

No previous TS coverage was silently dropped — every TS Test Case has an explicit Python successor or an explicit DEFER with restated rationale.

## 16. Coverage Analysis

| Area | Status |
|---|---|
| Business Requirements (`REQ-BUS-*`) | COVERED by design (strongest: AE-UI-TC-024 for REQ-BUS-004, already VERIFIED) |
| Functional Requirements (`REQ-FUNC-*`) | COVERED by design; **16 of 34 remain REQUIRES VERIFICATION** at the evidence level (Section 12) |
| API Requirements (`REQ-API-*`) | **Fully COVERED** by design (14/14); execution of 4 (createAccount/deleteAccount/updateAccount, plus getUserDetailByEmail's dependency on one of those) restricted pending authorization |
| UI Requirements (`REQ-UI-*`) | COVERED as cross-cutting design choices embedded in case steps (e.g., AE-UI-TC-018's AJAX-aware step), not separately cased |
| Hybrid Requirements (`REQ-E2E-*`) | COVERED by design (3/3); **NOT COVERED by any execution anywhere**, including the prior TS project |
| Negative coverage | COVERED — invalid login, duplicate email, missing API parameters, unsupported methods, non-matching search, invalid quantity |
| Boundary/equivalence coverage | PARTIALLY COVERED — search and quantity equivalence classes identified (Section 5 in [06](06-Test-Scenarios.md)); exact boundary values deferred to Step 8 |
| Critical business journeys | Discovery/Cart: COVERED. Identity→Checkout→Order: **PARTIALLY COVERED** — only the authentication gate (TC-024) has real evidence; TC-025–029 exist as designed cases but REQUIRE VERIFICATION before they mean anything as regression |
| Risk coverage | All risks from Steps 2–5 are reflected in priority/flag assignments throughout Sections 9–11 |

No gap is hidden — the REQUIRES VERIFICATION tag is used consistently rather than papering over unknowns.

## 17. Automation Suitability Summary

| Suitability | Case Count | Representative Cases |
|---|---|---|
| HIGH | 27 | AE-UI-TC-001/006/011/015/018/024; all read-only API cases (TC-001–010); AE-E2E-TC-003 once approved |
| MEDIUM | 6 | AE-UI-TC-013/017/021; AE-API-TC-013; AE-E2E-TC-001 |
| LOW | 6 | AE-UI-TC-025–029; AE-E2E-TC-002 |
| NOT RECOMMENDED | 1 | AE-UI-TC-014 (investigative, not a standing regression test) |
| REQUIRES VERIFICATION / Execution Restricted | 6 (overlaps with above where noted) | AE-UI-TC-004/005/007/008; AE-API-TC-011/012/013/014 |

**This classification is preliminary only** — Step 9 (Automation Scope) makes the binding decision on which cases actually get automated and in what order, using this table as input, not as a pre-approval.

## 18. Open Questions

Unchanged from [06](06-Test-Scenarios.md) §18 — restated here only where a specific Test Case now depends on the answer:

1. `/checkout` vs. `/view_cart` route identity — blocks AE-UI-TC-025/026/027.
2. Exact address/payment/confirmation/invoice UI — blocks AE-UI-TC-025–029.
3. Search-relevance matching rule — the subject of AE-UI-TC-014 itself.
4. Exact duplicate-email error text — affects AE-UI-TC-008's expected result.
5. Cart quantity boundary behavior — the subject of AE-UI-TC-017 itself.
6. Session-persistence/logout mechanics — affects AE-UI-TC-007/021.
7. Category-ID-to-name mapping stability — affects AE-UI-TC-019's Step 8 data.
8. Contact Us / Subscription client-side validation and success message — affects AE-UI-TC-002/003/009.

## 19. Decisions Requiring QA Lead Approval

1. **Authorize execution of AE-API-TC-011/012/013 (and, by extension, AE-UI-TC-004/025/026/028 and AE-E2E-TC-001/002)** — all require creating and/or deleting a real account on the shared public system; this assistant cannot authorize this itself.
2. **Confirm execution priority order:** this document recommends AE-UI-TC-006, AE-UI-TC-024, and the read-only API cases (TC-001–010) first (zero data-mutation risk, already VERIFIED or high-confidence), then AE-UI-TC-004/005 (unlocks most of the rest), before any Checkout E2E case.
3. **Consolidation proposals carried from Step 6:** AE-UI-TC-002/003 (subscription) and AE-UI-TC-025/026/027 (checkout-entry variants) — confirm whether to consolidate once the underlying flow is verified.
4. **New cases beyond the original 32/43:** AE-UI-TC-013/014/017 (search/quantity negative & diagnostic) and the full API/Hybrid expansion (Section 15) — confirm these are welcome additions to the design, independent of their eventual Step 9 automation status.
5. **AE-UI-TC-014's classification as NOT RECOMMENDED for standing automation** — confirm this is acceptable, or direct that it be re-scoped once the anomaly is explained.
6. **AE-UI-TC-010's continued low priority (P3)** — confirm the recommendation to deprioritize this case, carried from [06](06-Test-Scenarios.md) §19.

## 20. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 7 Exit Criteria

- [x] Steps 1–6 reviewed and used as direct basis
- [x] TS `AE-TC-001`, `AE-TDD-001`, `AE-AS-001` reviewed for context (cumulative with prior steps)
- [x] All 43 Step-6 scenarios evaluated; 46 Test Cases produced (not forced to 32 or 43)
- [x] 32-test baseline reconciled at the Test Case level (Section 15), nothing silently dropped
- [x] Every Test Case maps to a Scenario ID and a Requirement ID
- [x] Expected results are evidence-based; unverified behavior explicitly marked, never invented
- [x] Checkout/Payment uncertainty preserved throughout (Sections 9, 12)
- [x] Account mutation risks identified for every relevant case (Section 13); no account created or deleted in this step
- [x] Test Data references are logical placeholders only (`TD-*`); no Test Data document created
- [x] No automation code, Page Objects, API clients, fixtures, Docker, or CI/CD files created
- [x] Every case shows Execution Status: NOT EXECUTED; no pass/fail or defect claimed
- [x] Coverage gaps made visible, not hidden (Section 16)
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 8 — Test Data Design.
