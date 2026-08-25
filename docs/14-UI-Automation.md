# 14 — UI Automation

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-UIA-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 7 — UI Automation |
| Step | Step 14 — UI Automation |
| Predecessor Documents | [01](01-Project-Vision.md)–[13](13-Core-Framework-Development.md), all ✅ approved |

## 1. Step 14 Objective

Implement the approved UI automation scope — the 17 `AUTOMATE` UI Test Cases from [09-Automation-Scope.md](09-Automation-Scope.md) — using the framework built in Step 13. Of those 17, **12 were implementable this step**; 5 remain blocked pending account-creation authorization (Section 8). No `MANUAL`, `DEFERRED`, or `RESTRICTED` case was implemented. No framework redesign, no TS project modification, no automation-scope change.

## 2. Approved UI Automation Scope

From [09-Automation-Scope.md](09-Automation-Scope.md) §5: 17 `AUTOMATE`, 1 `MANUAL` (`AE-UI-TC-010`), 11 `DEFERRED`/`RESTRICTED` among the 29 total UI Test Cases. This step implements exactly the `AUTOMATE` subset — no `MANUAL`/`DEFERRED`/`RESTRICTED` case was touched.

## 3. Test Case → Scenario → Requirement → Test Data → Page Object Traceability

Built before any code was written, per instruction. **Implemented this step (12):**

| Test Case | Scenario | Requirement | Test Data | Page Object(s) | Priority |
|---|---|---|---|---|---|
| AE-UI-TC-001 | AE-UI-SC-001 | REQ-FUNC-HM-001–006 | None | HomePage | P1 |
| AE-UI-TC-006 | AE-UI-SC-006 | REQ-FUNC-SL-004 | TD-USER-INVALID-001 | SignupLoginPage | P0 |
| AE-UI-TC-011 | AE-UI-SC-011 | REQ-FUNC-PR-001/002 | TD-PRODUCT-001 | ProductsPage, ProductDetailsPage | P0 |
| AE-UI-TC-012 | AE-UI-SC-012 | REQ-FUNC-PR-003/004 | TD-SEARCH-VALID-001 | ProductsPage | P1 |
| AE-UI-TC-013 | AE-UI-SC-012 | REQ-FUNC-PR-004 | TD-SEARCH-NOMATCH-001 | ProductsPage | P2 |
| AE-UI-TC-015 | AE-UI-SC-013 | REQ-FUNC-CT-001/004 | TD-PRODUCT-002, TD-PRODUCT-003 | ProductDetailsPage, CartPage | P0 |
| AE-UI-TC-016 | AE-UI-SC-014 | REQ-FUNC-CT-002 | TD-PRODUCT-001, TD-CART-QTY-VALID | ProductDetailsPage, CartPage | P1 |
| AE-UI-TC-018 | AE-UI-SC-015 | REQ-FUNC-CT-003 | TD-PRODUCT-001 | ProductDetailsPage, CartPage | P0 |
| AE-UI-TC-019 | AE-UI-SC-016 | REQ-FUNC-PR-005 | TD-CATEGORY-001, TD-CATEGORY-002 | ProductsPage | P2 |
| AE-UI-TC-020 | AE-UI-SC-017 | REQ-FUNC-PR-006 | TD-BRAND-001, TD-BRAND-002 | ProductsPage | P2 |
| AE-UI-TC-023 | AE-UI-SC-020 | Recommended Items, REQ-FUNC-CT-001 | None | HomePage, CartPage | P2 |
| AE-UI-TC-024 | AE-UI-SC-021 | REQ-FUNC-CO-001, REQ-BUS-004, BR-003 | TD-PRODUCT-001 | ProductDetailsPage, CartPage | P0 |

**Blocked this step (5)** — see Section 8: AE-UI-TC-004, 005, 007, 008, 021.

No new Test Case ID, Scenario ID, or Requirement ID was invented — every row above is a direct, unmodified reference into [06](06-Test-Scenarios.md)/[07](07-Test-Cases.md)/[03](03-Requirement-Analysis.md).

## 4. Test Data Mapping

All from [08-Test-Data.md](08-Test-Data.md) — no new Test Data requirement invented. `TD-USER-INVALID-001` is realized via `src/data/users.py::INVALID_CREDENTIALS` (from Step 13). `TD-PRODUCT-001/002/003`, `TD-SEARCH-VALID-001`/`NOMATCH-001`, `TD-CATEGORY-001/002`, `TD-BRAND-001/002`, `TD-CART-QTY-VALID` are newly materialized this step in `src/data/products.py`, with values **directly re-verified against the live catalog during implementation** (Section 9), not assumed from Step 2's earlier pass — consistent with [08](08-Test-Data.md) §10's own note that catalog data is ENVIRONMENT-SENSITIVE.

## 5. Page Objects Implemented / Extended

All 5 skeletons from Step 13 were completed with real locators and actions — no Page Object beyond the approved 5 was created:

| Page Object | Locators/Actions Added | Serves |
|---|---|---|
| `HomePage` | `category_panel`, `brands_panel`, `featured_items_section`, `recommended_items_carousel`, `subscription_email_input`, `add_first_recommended_item_to_cart()`, `added_to_cart_modal`, `go_to_cart_from_modal()` | TC-001, 023 |
| `SignupLoginPage` | `login_email_input`/`login_password_input`/`login_button` (via `data-qa` attributes), `login_error_message`, `login()` | TC-006 |
| `ProductsPage` | `search_input`/`search_button`/`results_heading`/`product_cards`, `search()`, `open_first_product_details()`, `category_panel`, `open_category()`, `open_brand()` | TC-011, 012, 013, 019, 020 |
| `ProductDetailsPage` | `product_name`/`category_text`/`price`/`quantity_input`/`add_to_cart_button`/`availability_text`/`condition_text`/`brand_text`, `set_quantity()`, `add_to_cart()`, `added_to_cart_modal`, `go_to_cart_from_modal()` | TC-011, 015, 016, 018, 024 |
| `CartPage` | `row()`/`row_price()`/`row_quantity()`/`row_total()`/`line_item_rows`, `remove_item()`, `empty_cart_message`, `proceed_to_checkout_link`, `checkout_gate_modal`/`checkout_gate_message`/`checkout_gate_register_login_link`/`checkout_gate_continue_on_cart_button`, `click_proceed_to_checkout()` | TC-015, 016, 018, 024 |

`BasePage` (Step 13) required one change — see Section 13. No business assertion was added to any Page Object; every `expect(...)` call lives in the test files (Section 6), consistent with [11-Framework-Architecture.md](11-Framework-Architecture.md) §11's ownership split.

## 6. UI Tests Implemented

| File | Tests |
|---|---|
| `tests/ui/test_home.py` | `test_ae_ui_tc_001_home_page_core_elements_visible`, `test_ae_ui_tc_023_add_recommended_item_to_cart` |
| `tests/ui/test_signup_login.py` | `test_ae_ui_tc_006_login_with_invalid_credentials` |
| `tests/ui/test_products.py` | `test_ae_ui_tc_011_view_all_products_and_product_details`, `test_ae_ui_tc_012_search_with_valid_matching_keyword`, `test_ae_ui_tc_013_search_with_non_matching_keyword`, `test_ae_ui_tc_019_view_category_products_and_switch_category`, `test_ae_ui_tc_020_view_brand_products_and_switch_brand` |
| `tests/ui/test_cart.py` | `test_ae_ui_tc_015_add_multiple_products_verify_totals`, `test_ae_ui_tc_016_set_and_verify_cart_quantity`, `test_ae_ui_tc_018_remove_product_from_cart`, `test_ae_ui_tc_024_checkout_gate_blocks_unauthenticated_access` |

12 tests, one file per module (not a monolithic file), matching [11-Framework-Architecture.md](11-Framework-Architecture.md) §26. Every test's docstring states its Test Case/Scenario/Requirement/Test Data IDs and the VERIFIED expected result it asserts (Section 3's traceability mechanism, per [11] §28 — no second system introduced). Assertions target business-visible outcomes (cart totals, modal text, page headings, product field values) — never "page loaded" or "no exception."

## 7. Implementation Order (Waves)

Followed [09](09-Automation-Scope.md) §27 / [10](10-Automation-Strategy.md), adapted to what was actually authorized:

- **Wave 1 (A0, foundational):** TC-006, TC-011, TC-024 — implemented.
- **Wave 2 (A1, core regression):** TC-012, TC-015, TC-016, TC-018 — implemented.
- **Wave 3 (identity lifecycle, authorization-gated):** TC-004, 005, 007, 008 — **not implemented**, per Section 8.
- **Wave 4 (A2, broader regression):** TC-001, TC-013, TC-019, TC-020, TC-023 — implemented (TC-021, also Wave 4, is blocked — Section 8).

## 8. Test Cases Intentionally NOT Implemented, and Why

| Test Case | Step 9 Classification | Reason Not Implemented This Step |
|---|---|---|
| AE-UI-TC-004 | AUTOMATE (execution-authorization gate) | Requires creating and deleting a real account on the shared public AUT. No explicit QA Lead authorization has been given anywhere in this project's history to date — [09-Automation-Scope.md](09-Automation-Scope.md) §30 item 4 and [13-Core-Framework-Development.md](13-Core-Framework-Development.md) §15 both flagged this as still pending. **BLOCKED**, not silently reclassified. |
| AE-UI-TC-005 | AUTOMATE (execution-authorization gate) | Depends on `TD-USER-VALID-001`, which can only be provisioned via TC-004 or the equally-gated `AE-API-TC-011`. **BLOCKED** (transitive). |
| AE-UI-TC-007 | AUTOMATE (execution-authorization gate) | Depends on TC-005 (must be logged in to log out). **BLOCKED** (transitive). |
| AE-UI-TC-008 | AUTOMATE (execution-authorization gate) | Depends on `TD-USER-EXISTING-001`, a durable pre-registered account — same unprovisioned status as TC-005's dependency. **BLOCKED**. |
| AE-UI-TC-021 | AUTOMATE (execution-authorization gate) | Depends on TC-005 (search+cart persistence *after login*). **BLOCKED** (transitive). |
| AE-UI-TC-010 | MANUAL (Step 9) | Out of this step's scope by definition — only `AUTOMATE` cases are implemented in Step 14. |
| AE-UI-TC-002/003/009/022 | RESTRICTED (Step 9) | Unrecoverable public side effects (Subscription, Contact Us, Product Review) — never in scope for automation. |
| AE-UI-TC-014/017/025–029 | DEFERRED (Step 9) | Unresolved search anomaly, quantity boundary, and Checkout route/flow — never in scope for automation until their respective blockers resolve. |

**No AUTOMATE case's classification was silently changed.** The 5 blocked cases remain `AUTOMATE` in [09-Automation-Scope.md](09-Automation-Scope.md) — this document records that their *execution* is currently blocked, which is a separate, narrower fact than a scope reclassification, and does not modify Step 9.

## 9. Restricted / Manual / Deferred Cases Encountered

Covered fully in Section 8. No restricted case was executed. No account was created or deleted. No Contact Us, Subscription, or Product Review submission was made. Checkout was exercised **only** up to the already-approved authentication gate (TC-024) — no address, payment, or order-confirmation behavior was invented or assumed.

## 10. Browser Execution Performed

| Tier | Browser(s) | Cases | Result |
|---|---|---|---|
| Primary (full suite) | Chromium | All 12 implemented cases | 12/12 passed (Section 11) |
| Curated cross-browser subset ([05](05-Test-Strategy.md) §9 / [10](10-Automation-Strategy.md) §17: invalid login, cart add/remove, checkout gate) | Firefox | TC-006, TC-015, TC-018, TC-024 | 4/4 passed |
| Curated cross-browser subset | WebKit | TC-006, TC-015, TC-018, TC-024 | 4/4 passed |

**No claim of full cross-browser coverage is made** — only the curated subset already approved for cross-browser execution was run on Firefox/WebKit, exactly matching the tiered strategy; the remaining 8 cases were validated on Chromium only, per [10-Automation-Strategy.md](10-Automation-Strategy.md) §17's explicit "not every browser on every trigger" rule.

## 11. Execution Results

| Metric | Result |
|---|---|
| UI Test Cases implemented | 12 |
| Passed (Chromium, final clean runs) | 12/12, confirmed on 2 consecutive full runs |
| Passed (Firefox, curated subset) | 4/4 |
| Passed (WebKit, curated subset) | 4/4 |
| Failed (final state) | 0 |
| Skipped | 0 (of the 12 implemented) |
| Not executed | 5 (blocked — Section 8) |
| Full framework regression (setup validation + framework foundation + UI) | 39 passed, 1 deliberately-skipped, 0 failed |

**Distinguishing AUT vs. framework vs. blocked, per instruction:**
- **AUT passed:** all 12 implemented cases' underlying business behavior is confirmed correct — the checkout gate, invalid-login error, search (including the newly-resolved no-match behavior), cart math, and category/brand browsing all behave as [07-Test-Cases.md](07-Test-Cases.md) expected or as newly VERIFIED in this step.
- **AUT failed:** none. No test failure in this step was ultimately attributed to incorrect AUT business behavior.
- **Blocked:** 5 cases (Section 8), blocked on authorization/data dependency, not on any AUT or framework defect.
- **Skipped:** none among the 12 implemented (the durable-account skip test from Step 13 is a framework-foundation test, not a business case, and is unaffected by this step).
- **Not executed:** the 5 blocked cases, plus everything outside the 17 `AUTOMATE` UI scope (by design).

Success is not claimed merely because `pytest` exited 0 — every failure below was individually investigated to determine whether it was an automation defect, a genuine AUT behavior needing verification, or environmental flakiness, before being called "resolved."

## 12. Failure Analysis

Four distinct, genuine failures were found and investigated during implementation — **none were hidden with retries, and no assertion was weakened to make a failure disappear.**

| # | Test | Symptom | Root Cause (VERIFIED) | Classification | Fix |
|---|---|---|---|---|---|
| 1 | TC-024 | `Locator.click` timeout on "Proceed To Checkout" | `<a class="btn btn-default check_out">Proceed To Checkout</a>` has **no `href` attribute** — browsers do not assign the implicit ARIA `link` role to an `<a>` without `href`, so `get_by_role("link", ...)` never matched it | **Automation defect** (locator strategy) | Switched to `get_by_text("Proceed To Checkout", exact=True)`; documented in `CartPage` |
| 2 | TC-019 | `Locator.click` timeout on category link "Women" (`exact=True`) | Two causes, both VERIFIED: (a) the live `/products` page carries **third-party ad/interstitial-injected DOM elements** with `role="link"` and `aria-label`s like "Women's Clothing"/"Women's T-Shirts" (Google-vignette-style injection), polluting an unscoped role query; (b) the real link's computed accessible name is affected by its adjacent Font Awesome icon span, so even scoped, `exact=True` never matched | **Automation defect** (locator strategy) **+ genuine environmental finding** | Scoped the query to `.category-products` and switched to `exact=False`; documented in `ProductsPage` |
| 3 | TC-023 | Cart had 0 rows after "adding" a recommended item, no exception raised | **Race condition**: the add-to-cart click fires an AJAX request; the test then immediately navigated to `/view_cart` via a fresh `page.goto()`, which could abort the in-flight AJAX request before the server recorded it | **Automation defect** (missing synchronization) | Route through the "Added!" confirmation modal's "View Cart" link (the same reliable pattern already used by `ProductDetailsPage`) instead of an independent navigation; added `HomePage.go_to_cart_from_modal()` |
| 4 | TC-020 (once, full-suite only) | `Locator.click` timeout on brand "Tops"/`.category-products` sub-link | **Unresolved** — see below | **Environmental flakiness** (best current classification) | None applied; documented, not hidden |

**Item 4 in detail:** this failure appeared exactly once, only during full-suite execution (never in 3 isolated re-runs, never in a targeted two-navigation repro script built specifically to reproduce it). A `networkidle`-based navigation-wait was tried as a fix and **made things worse** — it caused the Home page to reliably time out, because this AUT carries continuous third-party ad/tracker network activity (consistent with finding #2's ad-injection evidence) that never lets `networkidle` settle. That change was reverted (Section 13). The current, honest conclusion is that this is low-frequency environmental variability on the shared public demo site under rapid sequential load (12 tests in ~70–140 seconds), not a reproducible locator or logic defect — consistent with the risk already named in [02](02-Application-Analysis.md)/[05](05-Test-Strategy.md)/[10](10-Automation-Strategy.md) throughout this project. It is **not papered over**: Section 14 records it explicitly as a flaky-test observation, and [05-Test-Strategy.md](05-Test-Strategy.md) §16's already-approved CI-only bounded-retry policy (not built in this step — that belongs to CI/CD, Step 19) is the correct, already-designed mechanism for this exact class of issue.

## 13. Defects / Observations Discovered

Beyond the four failures above, this step **resolved two previously-open verification gaps** from earlier documents:

- **Search "no results" behavior (Open Question, [03](03-Requirement-Analysis.md) §12 / [07](07-Test-Cases.md) TC-013) — RESOLVED.** VERIFIED: a non-matching search still renders the "Searched Products" heading, but with **zero** product cards and **no dedicated "no results" message**. `test_ae_ui_tc_013` now asserts this directly.
- **`data-qa` test attributes exist on the AUT — a correction to Step 2's record.** Step 2's original analysis stated "no `data-testid` attributes observed anywhere on the AUT." This step found `data-qa="login-email"`/`"login-password"`/`"login-button"`/`"signup-name"`/`"signup-email"`/`"signup-button"` on the `/login` page specifically (confirmed absent on `/products`). This is disclosed here as a correction, not silently folded into Step 2 (which is not modified). `SignupLoginPage` uses these as its rank-1 locators, per [11-Framework-Architecture.md](11-Framework-Architecture.md) §12's own hierarchy.
- **Third-party ad/interstitial DOM injection on `/products`** — a new, generalized instance of the same class of noise Step 2 flagged for the cart page ("Building Materials & Supplies" text). This one is more consequential: the injected elements carry `role="link"` and category-mimicking `aria-label`s, which can silently break *any* future unscoped role-based locator on that page, not just cause incidental text noise. Recommended for QA Lead attention (Section 20).
- **The "Proceed To Checkout" control has no `href`** — a minor but genuine AUT markup/testability observation, not a functional defect (the control still works via a click handler) but worth noting for anyone else automating this AUT with role-based locators by default.

No application defect was found that this project has any channel to get fixed — all of the above are either now-resolved documentation gaps or testability observations about a third-party public site, consistent with [04-Test-Plan.md](04-Test-Plan.md) §16's framing.

## 14. Flaky-Test Observations

One: `test_ae_ui_tc_020_view_brand_products_and_switch_brand`, exactly as detailed in Section 12, item 4. Frequency observed: 1 failure in approximately 6 full-suite executions across this step's implementation session (roughly 15–20%, a small sample — not a statistically confident rate, stated honestly as an order-of-magnitude observation, not a precise metric). No other test in this step showed any non-deterministic behavior across all runs performed.

## 15. Side-Effect / Environment Observations

- **No account was created or deleted.** No Contact Us message was sent. No subscription email was submitted. No product review was posted. Verified by direct review of every test file in this step (none call any of those flows) and by the fact that `created_account_cleanup` (Step 13) was never invoked with a registered account in any test this step.
- **Cart mutations were real** (as intended — that's what TC-015/016/018/023/024 test) but are session-scoped to each test's own fresh browser context; nothing persists beyond that context, and no cart-clearing mechanism was needed since carts are not shared across contexts.
- **Third-party ad/tracker network activity is continuous** on this AUT (Section 12, item 4) — a now-documented, load-bearing fact for any future synchronization strategy decisions (e.g., ruling out `networkidle` as a general-purpose wait strategy for this specific AUT).

## 16. TypeScript → Python Implementation Lessons

**Confirmed from [11-Framework-Architecture.md](11-Framework-Architecture.md) §40, now with direct implementation evidence:** the lean, 5-Page-Object design (no `CheckoutPage`/`PaymentPage`/`ContactUsPage`) proved sufficient for all 12 implementable cases without any gap — no case needed a page object outside the planned 5. The Page Object / test assertion-ownership split ([11] §11) held cleanly in practice: not one assertion needed to move into a Page Object, and not one Page Object needed a business-specific assertion helper beyond what `BasePage.expect_visible`/`expect_text` already offered (which, in the end, none of the 12 tests actually needed — they used Playwright's `expect()` directly in each test, which is equally consistent with the architecture's intent). **New lesson, not anticipated in Step 11:** the AUT's use of `href`-less pseudo-links (Section 12, item 1) and ad-injected `role="link"` elements (item 2) are genuinely AUT-specific testability quirks that no amount of architecture planning could have predicted — they were only discoverable by actually implementing and running tests against the live site, reinforcing [05-Test-Strategy.md](05-Test-Strategy.md)'s general principle that verification-through-execution is sometimes the only way to close a gap.

## 17. Deviations from docs/09–11

| Deviation | Nature | Disclosure |
|---|---|---|
| 5 of 17 `AUTOMATE` cases not executed this step | Scope-respecting delay, not a deviation from [09]'s classification | Section 8 — fully documented, [09] itself unmodified |
| `BasePage.goto()` briefly changed to `wait_until="networkidle"`, then reverted | A same-step trial-and-revert, net **zero** deviation from [11-Framework-Architecture.md](11-Framework-Architecture.md) §12's synchronization principles | Section 12/13 — disclosed in full, including why it was wrong |
| Three locator-strategy corrections within Page Objects (Section 12) | Implementation-level fixes, not architectural deviations — [11] §12's locator *hierarchy* (roles/labels/text preferred, CSS/attributes as documented fallback) was followed throughout; only the *application* of that hierarchy was corrected against real AUT markup | Section 12, in each Page Object's own docstring |

No deviation from the approved automation scope ([09]), strategy ([10]), or architecture ([11]) occurred beyond what is listed above, and none required modifying any of those documents.

## 18. Files Created / Modified

**Created:** `tests/ui/test_home.py`, `test_signup_login.py`, `test_products.py`, `test_cart.py`; `src/data/products.py`; `docs/14-UI-Automation.md`.

**Modified (all `src/pages/*`, completing Step 13 skeletons — no other layer touched):** `home_page.py`, `signup_login_page.py`, `products_page.py`, `product_details_page.py`, `cart_page.py`, `base_page.py` (one addition: `resolve_url`/`goto` docstring updated to record the `networkidle` finding — no behavioral change from Step 13's version).

**Not modified:** `src/api/*` (no API logic touched), `src/config/settings.py`, `src/utils/*`, `src/data/models.py`, `src/data/users.py`, `tests/conftest.py`, `tests/test_setup_validation.py`, `tests/test_framework_foundation.py`, and `docs/01`–`13`.

## 19. Validation Results

| Check | Result |
|---|---|
| pytest collection | 12/12 UI tests collected, 0 errors |
| Full existing suite (setup validation + framework foundation + UI) | 39 passed, 1 skipped (unrelated, pre-existing), 0 failed |
| Chromium execution (2 consecutive runs) | 12/12, 12/12 |
| Firefox (curated subset) | 4/4 |
| WebKit (curated subset) | 4/4 |
| Unintended business-side effects | None found (Section 15) |
| Restricted/deferred/manual cases executed | None (Section 9) |
| Determinism | Confirmed via 2 consecutive clean full runs; 1 documented exception (Section 14) |
| No hard-coded secrets | Confirmed — only the pre-existing, documented disposable test password from Step 13 |
| No arbitrary sleeps | Confirmed — zero `wait_for_timeout`/`time.sleep` calls in any new/modified file |
| No `pages/`↔`api/` cross-imports | Confirmed |
| No test imports another test | Confirmed |
| No API logic embedded in UI tests | Confirmed |
| No business logic in `BasePage` | Confirmed — unchanged from Step 13's generic-only helper set |
| docs/01–13 unmodified | Confirmed |
| TypeScript project unmodified | Confirmed (`git status --short` clean) |

## 20. Step 14 Exit Criteria

- [x] Steps 1–13 reviewed; actual Step 13 framework implementation inspected before coding
- [x] Traceability mapping produced before implementation (Section 3)
- [x] No new business Test Case ID invented
- [x] Only `AUTOMATE` UI cases implemented; no `MANUAL`/`DEFERRED`/`RESTRICTED` case implemented
- [x] Implementation followed the approved wave order, adapted honestly around the real authorization blocker (Section 7)
- [x] Blocked cases documented with reasons, not silently reclassified (Section 8)
- [x] Page Objects extended only as required by the 12 implementable cases; architecture boundaries respected
- [x] Test Data sourced from [08-Test-Data.md](08-Test-Data.md); no hard-coded literal bypassed an existing `TD-*` mapping
- [x] No real account created or deleted; no Contact Us/Subscription/Review submission made
- [x] Checkout automation limited to the approved gate case; no payment/route/message invented
- [x] Assertions validate real business-visible behavior, not weak presence checks
- [x] Tests organized under `tests/ui/`, split by module, not monolithic
- [x] Reporting/diagnostics infrastructure reused from Step 13, not redesigned
- [x] Browser coverage matches the approved tiered strategy — no false cross-browser claim
- [x] All failures investigated individually; root causes VERIFIED, not guessed; no failure hidden via retries; one genuine flaky-test finding disclosed rather than suppressed
- [x] No modification to docs/01–13
- [x] No modification to the TypeScript project
- [ ] QA Lead Review & Approval

## 21. QA Lead Approval Checklist

1. **Confirm the 5 blocked cases' handling is acceptable** — they remain `AUTOMATE` in [09] but unexecuted here; re-attempt requires the still-pending account-creation authorization.
2. **Confirm the 3 locator-strategy fixes (Section 12, items 1–3) are acceptable engineering corrections**, not scope changes — all three keep the original Test Case intent and expected result intact.
3. **Confirm the TC-020 flaky-test finding (Section 12 item 4 / Section 14) is acceptable to carry forward** as a known, low-frequency, environment-attributed risk, to be addressed by the already-approved CI retry policy at Step 19, rather than chased further now.
4. **Confirm the two Step 2 corrections (search "no results" behavior resolved; `data-qa` attributes found) are acceptable** to record here without retroactively editing Step 2 itself.
5. **Confirm no objection to the ad-injection finding on `/products`** (Section 13) being carried forward as a testability risk for future automation work on this AUT.

## 22. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 15 — API Automation.
