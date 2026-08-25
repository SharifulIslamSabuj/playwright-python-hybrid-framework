# 08 — Test Data Design

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-TDD-001 |
| Document Title | Test Data Design |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 3 — Test Design |
| Step | Step 8 — Test Data Design |
| Predecessor Documents | [01](01-Project-Vision.md)–[07](07-Test-Cases.md), all ✅ approved |

## 2. Purpose

Defines the data model — not a random-value list — needed to execute the 46 Test Cases approved in [07-Test-Cases.md](07-Test-Cases.md): `Test Case → Data Requirement → Data Set → Data Source → Data Lifecycle → Cleanup Requirement → Execution Constraint`. This document creates **no accounts, no cart state, no API mutations** — it only designs the data that later execution phases will use.

## 3. Test Data Design Principles

Reusability (one dataset serves every Test Case that needs it, not one-off literals per case), traceability (every dataset cites the Test Case IDs that depend on it), uniqueness where the shared environment demands it (account-creating data only — Section 8), isolation (no dataset is shared *mutably* across concurrently-running cases), maintainability (logical `TD-*` references in Test Cases, not embedded raw values — already applied throughout [07-Test-Cases.md](07-Test-Cases.md)), minimal duplication (one canonical dataset per purpose, e.g., one `TD-USER-VALID-001` reused by 6 Test Cases rather than 6 near-identical literals), safe execution (dummy-only payment/PII data, explicit cleanup pairing for every mutating dataset), environment awareness (single shared public instance — every dataset below is designed with that constraint, not against it), and deterministic execution where the AUT's behavior is actually known to be deterministic (Section 20 draws this line explicitly rather than assuming it).

## 4. Source Documents Reviewed

**Current Python project:** [01](01-Project-Vision.md)–[07](07-Test-Cases.md) — all six reviewed; the 46 Test Case cards in [07-Test-Cases.md](07-Test-Cases.md) §9–11 are the direct source of every `TD-*` reference used here (this document formalizes what Step 7 already referenced by placeholder, it does not introduce new Test Case dependencies).

**Previous TypeScript project** (Priority 2): `AE-TDD-001` (Test Data Design — read in full, including its User/Address/Product-Search/Contact/Subscription/Checkout-Payment/API-payload/JSON-template/governance sections), `AE-TC-001` (Test Case Design, for step-level data usage context), `AE-RA-001` (Requirement Analysis), `AE-TSD-001` (Test Scenario Design), `AE-AS-001` (Automation Scope) — all previously extracted and re-consulted here. TS's specific data *values* (e.g., search keyword "tshirt," dummy card `4111111111111111`) are treated as **REFERENCE-BASED options**, not requirements — this project designs its own dataset, using TS values only where they don't conflict with this project's own Step 2 evidence (e.g., Step 2's independently observed search anomaly used "dress," not "tshirt," so both are retained as distinct, separately-purposed datasets rather than one silently replacing the other).

## 5. Test Data Classification

Of the 20 candidate categories, all are represented — the 46 Test Cases in [07-Test-Cases.md](07-Test-Cases.md) span User/Account, Authentication, Invalid Authentication, Duplicate Account, Product, Search, Category, Brand, Product Detail (folded into Product Data, Section 9), Cart, Quantity/Boundary, Checkout, Order (folded into Checkout, Section 13), Contact Us, Subscription, API Request, API Negative, API Mutation, Hybrid E2E, and Browser/Environment (folded into Section 20, since it's a cross-cutting classification, not a standalone dataset) data. No category is added beyond what the approved Test Cases actually require.

## 6. Test Data ID Convention

**This document formalizes, and does not rename, the exact `TD-*` placeholders already referenced throughout the approved [07-Test-Cases.md](07-Test-Cases.md).** Renaming them now would silently break the traceability that document already established and approved. New IDs introduced in this step (where Step 7 referenced a concept but not yet a formal ID — e.g., structured API payloads) follow the same pattern: `TD-<CATEGORY>-<QUALIFIER>-<seq>`, e.g. `TD-USER-VALID-001`, `TD-API-PAYLOAD-CREATEACCOUNT-001`. No TS project ID (`USER-VALID-001`, `ADDR-001`, `PROD-SEARCH-001`, etc.) is reused verbatim — every ID here is this project's own, even where the underlying *value* is REFERENCE-BASED on a TS example.

---

## 7. User / Account Data

| Data ID | Purpose | Required Fields | Type | Static/Dynamic | Uniqueness | Cleanup | Related TCs | Verification Status |
|---|---|---|---|---|---|---|---|---|
| TD-USER-VALID-001 | A durable, reusable, already-registered account for login/logout/API-verify scenarios | email, password | Credential pair | Static (provisioned once, reused) | Not unique — deliberately durable | None (never deleted) | AE-UI-TC-005/007/021/027; AE-API-TC-007/014 | RECOMMENDED — this account does not exist yet; it must be provisioned via AE-UI-TC-004 or AE-API-TC-011 (both execution-restricted, Section 18) before it can serve as "existing" |
| TD-USER-NEW-001 | Disposable account for the primary Signup lifecycle case | name, email, password, title, birth_date/month/year, firstname, lastname, company, address1, address2, country, zipcode, state, city, mobile_number | Full account record | Dynamic (generated per run) | **Required — unique email per execution** | **Required** — delete same run | AE-UI-TC-004; AE-API-TC-011/012/013 | RECOMMENDED structure — field *names* VERIFIED (Step 2, `createAccount` API schema); field *values* not yet fixed (Section 21) |
| TD-USER-NEW-002 | Disposable account for "register during checkout" | Same shape as TD-USER-NEW-001 | Full account record | Dynamic | Required — unique | Required | AE-UI-TC-025 | RECOMMENDED — same structure caveat |
| TD-USER-NEW-003 | Disposable account for "register before checkout" | Same shape | Full account record | Dynamic | Required — unique | Required | AE-UI-TC-026 | RECOMMENDED |
| TD-USER-NEW-004 | Disposable account with complete, distinctive address fields, for address-match verification | Same shape, address fields must be non-generic enough to distinguish a match from a coincidence | Full account record | Dynamic | Required — unique | Required | AE-UI-TC-028 | RECOMMENDED |
| TD-USER-EXISTING-001 | One durable, known-already-registered email, used only to trigger the duplicate-registration negative path | email only (password not needed for this negative case) | Email reference | Static (provisioned once) | Deliberately **not** unique — its whole purpose is to already exist | None | AE-UI-TC-008 | RECOMMENDED — must be provisioned once via AE-UI-TC-004/AE-API-TC-011 first, then never deleted |
| TD-USER-INVALID-001 | Fabricated, non-existent credentials for negative login | email, password (both fabricated, never a real account) | Credential pair | Static (fixed fabricated value is fine — nothing to collide with) | Not applicable | None | AE-UI-TC-006; AE-API-TC-008 | VERIFIED usable — Step 2 already executed this exact style of negative login successfully |
| TD-USER-UPDATE-001 | Modified field set for `updateAccount`, applied to the account from TD-USER-NEW-001 | Same 16-field shape, at least one field changed from the original | Full account record | Dynamic (derived from TD-USER-NEW-001 at runtime) | Inherits TD-USER-NEW-001's uniqueness | Same account, deleted via TD-USER-NEW-001's cleanup | AE-API-TC-013 | RECOMMENDED |
| TD-ADDRESS-001 | Address field set reused across every account-creation dataset above | title, firstname, lastname, company, address1, address2, country, state, city, zipcode, mobile_number | Address record | Static template, dynamic where combined with a unique email | N/A on its own | N/A | Embedded in TD-USER-NEW-00x | REFERENCE-BASED — field *names* VERIFIED via `createAccount` API (Step 2); example values are a REFERENCE-BASED starting point adapted from TS `AE-TDD-001` §7, not independently required by the AUT |

## 8. Unique User Data Strategy

**Recommended automation strategy (not yet a verified application requirement):** generate account emails at runtime using a collision-resistant pattern — e.g., a timestamp or UUID embedded in the local part, following the same shape TS `AE-TDD-001` §5 used (`ae_[scenario]_[timestamp]@...`). This is a **RECOMMENDED** engineering practice for working safely against a shared public system, not a confirmed constraint the AUT itself imposes (this project has not tested what happens with a colliding non-unique email beyond the single duplicate-registration case, TD-USER-EXISTING-001, which is intentionally non-unique).

**Why uniqueness matters here specifically:**
- **Collision:** two test runs (this project's own retries, or unrelated public users of the same demo site) could otherwise register the same email, causing an unrelated failure that looks like a product defect.
- **Test dependency:** a hard-coded email shared across multiple Test Cases would silently couple them — one test's leftover state would affect another's outcome, violating the isolation principle in [05](05-Test-Strategy.md) §15.
- **False failures:** a "duplicate email" error appearing on what was meant to be a fresh-registration test is exactly the kind of environment-caused false failure [05](05-Test-Strategy.md) §16 already warns against conflating with a real defect.
- **Cleanup problems:** unique, timestamp-tagged emails make it possible to identify and clean up orphaned test accounts later, even if a test's own cleanup step failed.

This section states a **strategy recommendation**, not a data value — no actual generator is implemented here (Step 11/implementation phase).

## 9. Authentication Data

| Data ID | Purpose | Related TD | Related TCs | Verification Status |
|---|---|---|---|---|
| TD-AUTH-VALID-001 | Valid login credential pair | = TD-USER-VALID-001's credentials | AE-UI-TC-005; AE-API-TC-007 | RECOMMENDED (depends on TD-USER-VALID-001 existing) |
| TD-AUTH-INVALID-001 | Invalid login credential pair | = TD-USER-INVALID-001 | AE-UI-TC-006; AE-API-TC-008 | VERIFIED usable |
| TD-AUTH-MISSING-EMAIL-001 | Password only, no email — negative parameter case | password field only, no email | AE-API-TC-009 | VERIFIED — Step 2 confirmed the 400 response this data is meant to trigger |

No exact authentication error message is invented here beyond what Step 2 already VERIFIED (Section 28 restates the gaps).

## 10. Product Data

**Preferred source:** live-fetched via `GET /api/productsList` (AE-API-TC-001) at test setup time, rather than hard-coded IDs — per [05](05-Test-Strategy.md) §10, this reduces brittleness against the demo catalog changing without notice ([03](03-Requirement-Analysis.md) §11).

| Data ID | Reference | Purpose | Source | Stability | Related TCs |
|---|---|---|---|---|---|
| TD-PRODUCT-001 | "First available product" (selection rule, not a fixed ID) | General-purpose single-product cases | API-sourced (recommended) or observed (Step 2 used product id 1, "Blue Top") | ENVIRONMENT-SENSITIVE — catalog could change | AE-UI-TC-011/016/018/024; AE-API-TC-005 context; AE-UI-TC-025/026/027 |
| TD-PRODUCT-002 | "Second available product" | Multi-item cart case | API-sourced (recommended) | ENVIRONMENT-SENSITIVE | AE-UI-TC-015 |
| TD-PRODUCT-003 | "Third available product" or any product distinct from TD-PRODUCT-002 | Multi-item cart case | API-sourced (recommended) | ENVIRONMENT-SENSITIVE | AE-UI-TC-015 |

**Selection-rule design (REFERENCE-BASED on TS `AE-TDD-001` §8's "first available product" pattern, adapted):** rather than fixing literal product IDs in this document (which would become stale the moment the catalog changes), Test Cases should select "the first product returned by `GET /api/productsList`" or equivalent at runtime — an implementation detail for Step 11, stated here only as a data-sourcing principle.

## 11. Search Data

| Data ID | Value / Rule | Purpose | Related TCs | Verification Status |
|---|---|---|---|---|
| TD-SEARCH-VALID-001 | A keyword expected to match at least one catalog item (e.g., a substring of a known product name) | Positive search validation | AE-UI-TC-012/021; AE-API-TC-005 | VERIFIED functional (Step 2 confirmed search works); the *specific* keyword value is RECOMMENDED, not fixed as fact |
| TD-SEARCH-NOMATCH-001 | A keyword not expected to match any current catalog item | Negative search validation | AE-UI-TC-013 | REQUIRES VERIFICATION — no non-matching search has been independently executed yet; the "no results" UI state itself is unconfirmed |
| TD-SEARCH-ANOMALY-001 | The keyword **"dress"** — VERIFIED to have returned at least one non-obviously-matching result in Step 2 (e.g., "Sleeves Top and Short - Blue & Pink") | Diagnostic investigation of the search-relevance rule | AE-UI-TC-014 | **VERIFIED as the trigger case** — this is Step 2's own direct observation, not a TS value; kept deliberately distinct from TS's REFERENCE-BASED "tshirt"/"top"/"jean" keyword set, since neither this project nor TS independently confirmed those specific keywords behave identically |

**No search ranking or relevance rule is invented** — TD-SEARCH-ANOMALY-001 exists precisely to investigate one, not assume one.

## 12. Category and Brand Data

| Data ID | Value | Purpose | Related TCs | Verification Status |
|---|---|---|---|---|
| TD-CATEGORY-001 | A category link under "Women," "Men," or "Kids" (exact ID mapping not fixed) | Category browsing/switching | AE-UI-TC-019 | REQUIRES VERIFICATION — Step 2 confirmed the `/category_products/{id}` route works, but the ID-to-name mapping is undocumented and not fixed here as fact |
| TD-CATEGORY-002 | A second, distinct category/sub-category link | Category-switch validation | AE-UI-TC-019 | REQUIRES VERIFICATION, same basis |
| TD-BRAND-001 | "Polo" | Brand browsing | AE-UI-TC-020 | **VERIFIED** — Step 2 directly observed this exact brand name and its `/brand_products/Polo` route |
| TD-BRAND-002 | "H&M" | Brand-switch validation | AE-UI-TC-020 | **VERIFIED** — Step 2 directly observed this brand and its route |

Brand names/routes are stronger evidence than category IDs precisely because Step 2 directly read them off the live page; category IDs were never enumerated beyond the one tested route.

## 13. Cart Data

| Data ID | Value / Rule | Purpose | Related TCs | Verification Status |
|---|---|---|---|---|
| TD-CART-SINGLE-001 | TD-PRODUCT-001, quantity 1 (default) | Baseline single-item cart | AE-UI-TC-018/024 | VERIFIED (Step 2) |
| TD-CART-MULTI-001 | TD-PRODUCT-002 + TD-PRODUCT-003, quantity 1 each | Multi-item cart / totals | AE-UI-TC-015 | PARTIALLY VERIFIED — single-item math confirmed, multi-item not yet |
| TD-CART-QTY-VALID | Quantity = 4 (REFERENCE-BASED on TS `AE-TDD-001` §8's own example value, not independently re-derived) | Positive quantity-set case | AE-UI-TC-016 | REFERENCE-BASED, PARTIALLY VERIFIED (Step 2 only confirmed the default quantity of 1) |
| TD-CART-QTY-BOUNDARY-CANDIDATE | Zero or a negative value — **exact number intentionally not fixed** | Boundary/negative quantity case | AE-UI-TC-017 | **REQUIRES VERIFICATION** — no minimum/maximum is invented; this dataset exists to discover the actual rule, not assume one (matches Open Question 5, [03](03-Requirement-Analysis.md) §12) |
| TD-CART-EMPTY-001 | No items in cart | Empty-cart state / baseline for TC-018's precondition-then-removal flow | AE-UI-TC-018 (post-condition), AE-UI-TC-021 (baseline) | VERIFIED — Step 2 directly observed the exact empty-cart message |

## 14. Checkout / Order Data

Checkout is a **known verification gap** ([03](03-Requirement-Analysis.md) §5 row 4; [07](07-Test-Cases.md) §12) — no field below is invented as fact.

| Data ID | Field(s) | Value | Verification Status | Related TCs |
|---|---|---|---|---|
| TD-CHECKOUT-001 | Order comment | e.g., "Please deliver during business hours." (REFERENCE-BASED, TS `AE-TDD-001` §11 example, freely reusable — it's arbitrary free text with no business rule attached) | RECOMMENDED value; whether an order-comment field even exists on this AUT is itself **REQUIRES VERIFICATION** | AE-UI-TC-025/026/027 |
| TD-PAYMENT-001 | Name on card, card number, CVC, expiry month/year | **Dummy values only** — e.g., a well-known test card pattern such as `4111111111111111` (REFERENCE-BASED, TS `AE-TDD-001` §11; this is a widely-used, non-functional placeholder card number pattern, never real payment data) | REQUIRES VERIFICATION whether the AUT's payment form accepts this shape at all — payment mechanics are unconfirmed by this project (Section 22 restates the sensitive-data rule) | AE-UI-TC-025/026/027 |
| TD-INVOICE-001 | Expected artifact: a downloaded file, triggered via browser download | Type/behavior only, no fixed filename or format | REQUIRES VERIFICATION — invoice download itself is unconfirmed ([07](07-Test-Cases.md) TC-029) | AE-UI-TC-029 |

**No checkout/payment requirement is fabricated.** Every field above is either directly reused from Step 7's already-approved Test Cases or explicitly marked unconfirmed.

## 15. Contact Us Data

| Data ID | Field | Value | Verification Status | Related TCs |
|---|---|---|---|---|
| TD-CONTACT-001 | Name, email, subject, message | e.g., "Automation QA User" / a disposable test email / "Automation Test Contact Request" / a clearly-marked automated test message (REFERENCE-BASED, TS `AE-TDD-001` §9 shape, adapted with a disposable rather than a fixed recurring email to avoid repeated real submissions to the same address) | Fields VERIFIED present (Step 2); submission outcome REQUIRES VERIFICATION | AE-UI-TC-009 |
| TD-FILE-001 | Small sample upload file | A short, harmless `.txt` file (no fixed content specified here) | RECOMMENDED — file-upload field VERIFIED present (Step 2); acceptance behavior unconfirmed | AE-UI-TC-009 |

No mandatory-field validation rule is asserted as fact — [07](07-Test-Cases.md) TC-009 does not test the empty-field negative path, since Step 6/7 did not identify it as an approved case; if desired, that would be a scope addition for a future step, not silently added here.

## 16. Subscription Data

| Data ID | Value | Purpose | Verification Status | Related TCs |
|---|---|---|---|---|
| TD-SUBSCRIPTION-001 | One disposable email, reused for both entry points (Home and Cart footers) | Positive subscription | Field presence VERIFIED (Step 2); submission outcome REQUIRES VERIFICATION | AE-UI-TC-002/003 |

**Note:** [07](07-Test-Cases.md) already used a single `TD-SUBSCRIPTION-001` for both TC-002 and TC-003, consistent with the CONSOLIDATE-candidate proposal from [06](06-Test-Scenarios.md) §15/19 — this document does not decide that consolidation, only reflects that the same dataset already serves both cases whether or not they are formally merged. No invalid-email or duplicate-subscription dataset is defined, since no approved Test Case currently exercises that path — adding one would be a scope question for a future step, not invented here.

---

## 17. API Test Data

All 14 endpoints, using only VERIFIED (Step 2) field names — no field is invented.

| Data ID | Endpoint | Method | Data | Related TC |
|---|---|---|---|---|
| TD-API-001 | `/api/productsList` | GET | None | AE-API-TC-001 |
| TD-API-002 | `/api/productsList` | POST | None (method itself is the test condition) | AE-API-TC-002 |
| TD-API-003 | `/api/brandsList` | GET | None | AE-API-TC-003 |
| TD-API-004 | `/api/brandsList` | PUT | None | AE-API-TC-004 |
| TD-API-005 | `/api/searchProduct` | POST | `search_product` = TD-SEARCH-VALID-001 | AE-API-TC-005 |
| TD-API-006 | `/api/searchProduct` | POST | (no `search_product`) | AE-API-TC-006 |
| TD-API-007 | `/api/verifyLogin` | POST | `email`/`password` = TD-AUTH-VALID-001 | AE-API-TC-007 |
| TD-API-008 | `/api/verifyLogin` | POST | `email`/`password` = TD-AUTH-INVALID-001 | AE-API-TC-008 |
| TD-API-009 | `/api/verifyLogin` | POST | = TD-AUTH-MISSING-EMAIL-001 | AE-API-TC-009 |
| TD-API-010 | `/api/verifyLogin` | DELETE | None | AE-API-TC-010 |
| TD-API-PAYLOAD-CREATEACCOUNT-001 | `/api/createAccount` | POST | Full 16-field payload = TD-USER-NEW-001 | AE-API-TC-011 |
| TD-API-PAYLOAD-DELETEACCOUNT-001 | `/api/deleteAccount` | DELETE | `email`/`password` = the account created by TD-API-PAYLOAD-CREATEACCOUNT-001 | AE-API-TC-012 |
| TD-API-PAYLOAD-UPDATEACCOUNT-001 | `/api/updateAccount` | PUT | Full payload = TD-USER-UPDATE-001 | AE-API-TC-013 |
| TD-API-014 | `/api/getUserDetailByEmail` | GET | `email` = an existing account's email | AE-API-TC-014 |

## 18. API Negative Data

Consolidated view of the negative-path subset (already itemized above, grouped here per instruction):

| Data ID | Represents | Expected (VERIFIED, Step 2) |
|---|---|---|
| TD-API-002 | Unsupported method (POST on productsList) | 405, "This request method is not supported." |
| TD-API-004 | Unsupported method (PUT on brandsList) | 405, same message |
| TD-API-006 | Missing required parameter (`search_product`) | 400, "Bad request, search_product parameter is missing in POST request." |
| TD-API-008 | Invalid credentials | 404, "User not found!" |
| TD-API-009 | Missing required parameter (`email`) | 400, "Bad request, email or password parameter is missing in POST request." |
| TD-API-010 | Unsupported method (DELETE on verifyLogin) | 405, "This request method is not supported." |

All 6 negative datasets above correspond to responses **VERIFIED directly** in Step 2 — none are invented.

## 19. API Mutation Data

**Documentation entries only — none of the following were executed while producing this document; no account was created or deleted.**

| Data ID | Operation | Required Data | Uniqueness | State Dependency | Cleanup | Execution Restriction | Shared-Environment Risk |
|---|---|---|---|---|---|---|---|
| TD-API-PAYLOAD-CREATEACCOUNT-001 | Create account | Full 16-field payload (TD-USER-NEW-001) | **Required** | None (creates new state) | Must pair with TD-API-PAYLOAD-DELETEACCOUNT-001 in the same run | **This assistant cannot execute this unilaterally — requires explicit QA Lead authorization**, per [07](07-Test-Cases.md) §19 item 1 | Real, persistent record on a shared public system until deleted |
| TD-API-PAYLOAD-UPDATEACCOUNT-001 | Update account | Modified 16-field payload (TD-USER-UPDATE-001) | Inherits from the account being updated | Requires an existing account (from Create) | Underlying account still requires deletion afterward | Same restriction | Modifies real shared data |
| TD-API-PAYLOAD-DELETEACCOUNT-001 | Delete account | `email`/`password` | N/A (targets an existing unique account) | Requires the account to exist | **Is** the cleanup — never run standalone | Same restriction | Removes real shared data — the resolving action, not a new risk |

## 20. Hybrid E2E Data

| Data ID | API-Created/Prepared State | UI Action | UI/API Verification | Why Data Must Be Shared Between Layers | Related TC |
|---|---|---|---|---|---|
| Reuses TD-USER-NEW-001 + TD-API-PAYLOAD-CREATEACCOUNT-001/DELETEACCOUNT-001 | Account provisioned via API | UI login using the same credentials | UI-rendered authenticated state | The whole point is that the *same* credentials cross from the API-creation call into the UI login form — a fabricated or mismatched credential would invalidate the test's entire premise | AE-E2E-TC-001 |
| Same as above, plus TD-PRODUCT-001, TD-CHECKOUT-001 | Account provisioned via API | UI performs full checkout journey | UI-rendered order confirmation | Same reasoning, extended through the full checkout flow | AE-E2E-TC-002 |
| TD-API-001 (product list) | None (read-only) | UI renders Products page (TD-PRODUCT-001 context) | UI values compared against the API response captured in the same run | The API response and the UI rendering must be captured from the **same** point in time for the comparison to be meaningful — an API call from a different moment could reflect a catalog that has since changed | AE-E2E-TC-003 |

No new Hybrid-only dataset is introduced — every Hybrid Test Case is fully satisfied by data already defined in Sections 7–17, consistent with how TS `AE-TDD-001` §19 handled its own two Hybrid cases (REFERENCE KNOWLEDGE for this design choice, not for the specific values).

---

## 21. Static vs. Dynamic Data

| Classification | Meaning | Examples from This Document |
|---|---|---|
| **STATIC** | Fixed value, safe to reuse indefinitely, no collision risk | TD-USER-INVALID-001, TD-BRAND-001/002, TD-SEARCH-ANOMALY-001, TD-CONTACT-001's message text |
| **DYNAMIC** | Must vary per execution to avoid collision, but not necessarily "generated" (could be manually rotated) | TD-USER-EXISTING-001 (provisioned once, then durable — dynamic only at provisioning time) |
| **GENERATED / RUNTIME-GENERATED** | Produced programmatically at test-run time, never reused across runs | TD-USER-NEW-001/002/003/004, TD-API-PAYLOAD-CREATEACCOUNT-001's email field |
| **API-SOURCED** | Retrieved live from the AUT's own API rather than hard-coded | TD-PRODUCT-001/002/003 (recommended sourcing) |
| **ENVIRONMENT-SOURCED** | Not applicable to any current dataset — no environment-specific (per-deployment) values exist yet, since there is only one environment ([04](04-Test-Plan.md) §10); this classification is reserved for future use if a staging environment is ever introduced |

**No source is claimed stable unless VERIFIED** — product/category data is explicitly flagged ENVIRONMENT-SENSITIVE (Section 10/12) rather than assumed permanent.

## 22. Data Generation Strategy

Recommendations for the future automation framework — **design only, nothing implemented, no packages installed**:

- **Runtime-generated unique users:** a timestamp- or UUID-based email suffix, applied to every `TD-USER-NEW-*` dataset (Section 8).
- **Deterministic values where appropriate:** static datasets (Section 21) should remain literal, fixed values in configuration — generating them at runtime would add complexity with no benefit.
- **Faker-style generated data:** justified only for high-volume/varied data needs (e.g., if boundary testing eventually needs many distinct invalid inputs); not currently justified for this project's scale — a plain generator function is simpler and sufficient for the account-uniqueness need alone.
- **API-sourced IDs:** preferred over hard-coded product/category references (Sections 10/12), fetched once per test run and reused within that run.
- **Environment variables for sensitive configuration:** base URL and any future credentials/config should be externalized, not hard-coded in test files (Section 23).
- **Centralized test data objects:** the `TD-*` catalogue in this document is the design-time version of what should become one or more centralized data modules/files in the framework — not scattered literals inside test logic.
- **Data builders/factories:** worth considering specifically for the `TD-USER-NEW-*` family (Section 7), since they all share the same 16-field shape with only the email/address varying — a builder reduces duplication there. Not recommended elsewhere in this catalogue, where the datasets are few and simple enough that a builder would be unnecessary abstraction ([05](05-Test-Strategy.md) §21, "controlled abstractions").

## 23. Sensitive Data Handling

- **Passwords:** every password value in this document is a disposable test-account password, never a real credential. No specific value is fixed here (Section 21 leaves exact literals to implementation) — but whatever value is chosen must never be a password reused anywhere outside this test context.
- **Authentication data:** TD-AUTH-* datasets (Section 9) are either fabricated-invalid or reused-test-account credentials — never real user data.
- **Payment data (TD-PAYMENT-001):** explicitly dummy-only (Section 14) — this project will never enter real card data, matching [04-Test-Plan.md](04-Test-Plan.md) §24's prohibition.
- **API credentials:** not applicable — all 14 verified endpoints require no API key/token ([02](02-Application-Analysis.md) §10); this is stated as a current fact, not a permanent guarantee.
- **Secrets in Git:** no real secret exists to protect yet, since the AUT requires none. This section is a **forward-looking governance rule**, not a response to an existing secret: if any future credential (e.g., a CI-only reporting token) is introduced, it must live in environment variables or a secrets manager, never committed to the repository — consistent with [05-Test-Strategy.md](05-Test-Strategy.md) §12's Docker/CI environment-consistency principle.
- **Environment variables:** base URL and any future runtime configuration should be externalized per [04-Test-Plan.md](04-Test-Plan.md) §10 ("to be finalized during framework setup") — not decided here, only flagged as the mechanism of choice.

## 24. Data Cleanup Strategy

| Dataset | Cleanup Required? | Mechanism | Timing | Failure Recovery | Shared-Environment Risk |
|---|---|---|---|---|---|
| TD-USER-NEW-001/002/003/004 | **Yes** | UI "Delete Account" (AE-UI-TC-004 pattern) or API `deleteAccount` (AE-API-TC-012) | End of the same test/run | If cleanup fails, the failure must be surfaced (logged, not silently swallowed) — an orphaned account is a real, persistent cost on a shared public system | High if unmanaged |
| TD-USER-EXISTING-001 | **No** — deliberately durable | N/A (kept intentionally) | N/A | N/A | Low — one long-lived account, not accumulating |
| TD-USER-VALID-001 | **No** — deliberately durable, reused across many cases | N/A | N/A | N/A | Low |
| TD-API-PAYLOAD-CREATEACCOUNT-001 / UPDATEACCOUNT-001 | **Yes** | API `deleteAccount` | Same run, regardless of test outcome | Same as above | High — API-level mutation on shared data |
| TD-CART-*, TD-CART-QTY-* | **MANUAL / ENVIRONMENT-DEPENDENT CLEANUP** — no verified API exists to clear a cart programmatically; cart state is presumed session-scoped, but this is **REQUIRES VERIFICATION**, not confirmed | Removing items via UI (AE-UI-TC-018) or ending the session | End of test | If a test leaves cart items behind, a subsequent test in the same session could see unexpected state — this is a real, currently-unmitigated risk | Medium |
| TD-SUBSCRIPTION-001, TD-CONTACT-001 | **No verified deletion mechanism** — subscribing/contacting has no documented reversal | MANUAL / ENVIRONMENT-DEPENDENT CLEANUP (i.e., none available) | N/A | N/A — a real, permanent side effect on the AUT's mailing list/feedback inbox each time these are executed | Low individually, but repeated CI runs would accumulate real subscriptions/messages — flagged as a genuine constraint (Section 29), not solved here |

**No API is claimed to support cleanup unless VERIFIED** — `deleteAccount` is VERIFIED at the documentation level (Step 2); no cart-clearing or subscription-removal API was ever observed to exist, and none is invented here.

## 25. Test Data Isolation

- **Test independence:** every dataset above is scoped to the Test Case(s) that need it — no dataset is designed to carry state *between* unrelated cases.
- **Avoid shared mutable data:** the only datasets reused across multiple cases (TD-USER-VALID-001, TD-USER-EXISTING-001, TD-PRODUCT-*, TD-BRAND-*) are all **read-only in practice** from each consuming test's point of view — none of those cases mutate them.
- **Unique account strategy:** Section 8 — every account-*creating* dataset is uniquely generated; only the two deliberately-durable, read-only accounts are shared.
- **Read-only product preference:** Section 10 — product data is sourced, not mutated, by every consuming case.
- **Cleanup:** Section 24.
- **State reset:** no verified mechanism exists to reset cart/session state outside normal UI interaction (Section 24) — this is a design constraint carried forward, not resolved by wishful assumption.
- **Parallel execution considerations:** directly aligned with [05-Test-Strategy.md](05-Test-Strategy.md) §14/15 — datasets marked "Required — unique" above are safe to use in parallel test runs; the two durable shared accounts (TD-USER-VALID-001, TD-USER-EXISTING-001) must **not** be used by two concurrently-running tests that both mutate session/auth state (e.g., two simultaneous logout tests), since they share the same underlying account.

---

## 26. Test Data Inventory (Master)

| Data ID | Category | Purpose | Type | Source | Lifecycle | Unique? | Cleanup? | Related TCs | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| TD-USER-VALID-001 | User/Account | Reusable valid login | Static | Manually provisioned | Durable | No | No | UI-005/007/021/027, API-007/014 | RECOMMENDED, pending provisioning |
| TD-USER-NEW-001 | User/Account | Primary signup lifecycle | Generated | Runtime | Single-run | Yes | Yes | UI-004, API-011/012/013 | RECOMMENDED |
| TD-USER-NEW-002 | User/Account | Register-during-checkout | Generated | Runtime | Single-run | Yes | Yes | UI-025 | RECOMMENDED |
| TD-USER-NEW-003 | User/Account | Register-before-checkout | Generated | Runtime | Single-run | Yes | Yes | UI-026 | RECOMMENDED |
| TD-USER-NEW-004 | User/Account | Address-match verification | Generated | Runtime | Single-run | Yes | Yes | UI-028 | RECOMMENDED |
| TD-USER-EXISTING-001 | User/Account | Duplicate-email negative | Static (after provisioning) | Manually provisioned once | Durable | No (intentionally) | No | UI-008 | RECOMMENDED, pending provisioning |
| TD-USER-INVALID-001 | Auth/Invalid | Negative login | Static | Fixed fabricated value | Permanent | N/A | No | UI-006, API-008 | VERIFIED usable |
| TD-USER-UPDATE-001 | User/Account | Update-account payload | Generated (derived) | Runtime | Single-run | Inherits parent | Inherits parent | API-013 | RECOMMENDED |
| TD-ADDRESS-001 | User/Account | Shared address template | Static template | REFERENCE-BASED | Embedded | N/A | N/A | Embedded in TD-USER-NEW-00x | REFERENCE-BASED |
| TD-AUTH-VALID-001 | Authentication | Valid credential pair | = TD-USER-VALID-001 | — | — | — | — | UI-005, API-007 | RECOMMENDED |
| TD-AUTH-INVALID-001 | Authentication | Invalid credential pair | = TD-USER-INVALID-001 | — | — | — | — | UI-006, API-008 | VERIFIED usable |
| TD-AUTH-MISSING-EMAIL-001 | Authentication | Missing-parameter negative | Static | Fixed | Permanent | No | No | API-009 | VERIFIED |
| TD-PRODUCT-001/002/003 | Product | General product references | API-sourced (recommended) | Runtime (recommended) | Per-run | No | No | UI-011/015/016/018/024/025-027, API-005 | ENVIRONMENT-SENSITIVE |
| TD-SEARCH-VALID-001 | Search | Positive search | RECOMMENDED literal | Config | Static | No | No | UI-012/021, API-005 | VERIFIED functional, value RECOMMENDED |
| TD-SEARCH-NOMATCH-001 | Search | Negative search | RECOMMENDED literal | Config | Static | No | No | UI-013 | REQUIRES VERIFICATION |
| TD-SEARCH-ANOMALY-001 | Search | Diagnostic — "dress" | VERIFIED literal | Step 2 observation | Static | No | No | UI-014 | **VERIFIED** |
| TD-CATEGORY-001/002 | Category | Category browsing | RECOMMENDED, unmapped | Config | Static | No | No | UI-019 | REQUIRES VERIFICATION |
| TD-BRAND-001/002 | Brand | "Polo"/"H&M" | VERIFIED literal | Step 2 observation | Static | No | No | UI-020 | **VERIFIED** |
| TD-CART-SINGLE-001 | Cart | Baseline cart | Derived | Runtime | Per-test | No | UI removal | UI-018/024 | VERIFIED |
| TD-CART-MULTI-001 | Cart | Multi-item cart | Derived | Runtime | Per-test | No | UI removal | UI-015 | PARTIALLY VERIFIED |
| TD-CART-QTY-VALID | Cart/Boundary | Quantity = 4 | REFERENCE-BASED literal | TS example | Static | No | No | UI-016 | REFERENCE-BASED |
| TD-CART-QTY-BOUNDARY-CANDIDATE | Cart/Boundary | Invalid quantity | Unfixed | To be determined | Static | No | No | UI-017 | **REQUIRES VERIFICATION** |
| TD-CART-EMPTY-001 | Cart | Empty state | Observed | Step 2 | Static | No | No | UI-018/021 | VERIFIED |
| TD-CHECKOUT-001 | Checkout | Order comment | REFERENCE-BASED literal | TS example | Static | No | No | UI-025/026/027 | REQUIRES VERIFICATION (field existence) |
| TD-PAYMENT-001 | Checkout | Dummy payment fields | REFERENCE-BASED literal, dummy only | TS example | Static | No | No | UI-025/026/027 | REQUIRES VERIFICATION |
| TD-INVOICE-001 | Order | Expected download artifact | Behavioral, unfixed | — | — | No | No | UI-029 | REQUIRES VERIFICATION |
| TD-CONTACT-001 | Contact Us | Full contact form data | REFERENCE-BASED, adapted | TS example | Static | No (email disposable) | No | UI-009 | Fields VERIFIED, submission REQUIRES VERIFICATION |
| TD-FILE-001 | Contact Us | Sample upload file | RECOMMENDED | — | Static | No | No | UI-009 | RECOMMENDED |
| TD-SUBSCRIPTION-001 | Subscription | Disposable email | RECOMMENDED | — | Static (or per-run disposable) | Recommended unique-ish | No | UI-002/003 | Field VERIFIED, submission REQUIRES VERIFICATION |
| TD-API-001 through TD-API-010 | API | Request/negative data for 10 stateless endpoints | VERIFIED shapes | Step 2 | Static | No | No | API-001–010 | **VERIFIED** |
| TD-API-PAYLOAD-CREATEACCOUNT-001 | API Mutation | Full createAccount payload | = TD-USER-NEW-001 | Runtime | Single-run | Yes | Yes | API-011 | VERIFIED (doc); execution restricted |
| TD-API-PAYLOAD-DELETEACCOUNT-001 | API Mutation | deleteAccount call | Derived | Runtime | Single-run | N/A | Is the cleanup | API-012 | VERIFIED (doc); execution restricted |
| TD-API-PAYLOAD-UPDATEACCOUNT-001 | API Mutation | Full updateAccount payload | = TD-USER-UPDATE-001 | Runtime | Single-run | Inherits | Inherits | API-013 | VERIFIED (doc); execution restricted |
| TD-API-014 | API | getUserDetailByEmail | Reused email | Runtime | Per-run | No | No | API-014 | VERIFIED (doc); execution restricted |

**33 distinct Test Data definitions** — a deliberately compact data model, not a padded spreadsheet, covering every one of the 46 approved Test Cases.

## 27. Test Data Matrix

**Matrix 1 — Coverage by category:**

| Test Data Category | Positive | Negative | Boundary |
|---|---|---|---|
| User/Account | TD-USER-VALID-001, TD-USER-NEW-001–004 | TD-USER-INVALID-001, TD-USER-EXISTING-001 | — |
| Authentication | TD-AUTH-VALID-001 | TD-AUTH-INVALID-001, TD-AUTH-MISSING-EMAIL-001 | — |
| Product | TD-PRODUCT-001–003 | — | — |
| Search | TD-SEARCH-VALID-001 | TD-SEARCH-NOMATCH-001 | TD-SEARCH-ANOMALY-001 (diagnostic) |
| Category/Brand | TD-CATEGORY-001/002, TD-BRAND-001/002 | — | — |
| Cart | TD-CART-SINGLE-001, TD-CART-MULTI-001, TD-CART-QTY-VALID | — | TD-CART-QTY-BOUNDARY-CANDIDATE |
| Checkout/Order | TD-CHECKOUT-001, TD-PAYMENT-001, TD-INVOICE-001 | — | — |
| Contact Us | TD-CONTACT-001, TD-FILE-001 | — | — |
| Subscription | TD-SUBSCRIPTION-001 | — | — |
| API (stateless) | TD-API-001/003/005/007/014 | TD-API-002/004/006/008/009/010 | — |
| API (mutation) | TD-API-PAYLOAD-CREATEACCOUNT/UPDATEACCOUNT-001 | — | — |

**Matrix 2 — Test Case group data profile:**

| Test Case Group | Data Dependency | Static/Dynamic | Cleanup |
|---|---|---|---|
| Home / Smoke | None | — | No |
| Signup/Login/Logout | TD-USER-* (Section 7), TD-AUTH-* | Mixed (durable + generated) | Yes, for generated accounts |
| Products/Search/Category/Brand | TD-PRODUCT-*, TD-SEARCH-*, TD-CATEGORY-*, TD-BRAND-* | Mostly static/API-sourced | No |
| Cart | TD-CART-*, TD-PRODUCT-* | Dynamic per test | Manual/environment-dependent |
| Checkout/Order/Invoice | TD-USER-NEW-*, TD-CHECKOUT-001, TD-PAYMENT-001, TD-INVOICE-001 | Dynamic | Yes (account) + manual (order, unverified) |
| Contact Us / Subscription | TD-CONTACT-001, TD-FILE-001, TD-SUBSCRIPTION-001 | Static/disposable | No verified mechanism |
| API (stateless) | TD-API-001–010 | Static | No |
| API (mutation) | TD-API-PAYLOAD-* | Dynamic | Yes, mandatory |
| Hybrid | Reuses all of the above | Mixed | Inherits from the layer that created it |

## 28. Test Case → Test Data Traceability

Every one of the 46 Test Cases in [07-Test-Cases.md](07-Test-Cases.md) is covered — no data-dependent case is left unexplained.

| TC ID | Test Data | TC ID | Test Data | TC ID | Test Data |
|---|---|---|---|---|---|
| AE-UI-TC-001 | None | AE-UI-TC-017 | TD-CART-QTY-BOUNDARY-CANDIDATE | AE-API-TC-004 | TD-API-004 |
| AE-UI-TC-002 | TD-SUBSCRIPTION-001 | AE-UI-TC-018 | TD-PRODUCT-001, TD-CART-EMPTY-001 | AE-API-TC-005 | TD-API-005 |
| AE-UI-TC-003 | TD-SUBSCRIPTION-001 | AE-UI-TC-019 | TD-CATEGORY-001/002 | AE-API-TC-006 | TD-API-006 |
| AE-UI-TC-004 | TD-USER-NEW-001 | AE-UI-TC-020 | TD-BRAND-001/002 | AE-API-TC-007 | TD-API-007 |
| AE-UI-TC-005 | TD-USER-VALID-001 / TD-AUTH-VALID-001 | AE-UI-TC-021 | TD-SEARCH-VALID-001, TD-USER-VALID-001 | AE-API-TC-008 | TD-API-008 |
| AE-UI-TC-006 | TD-USER-INVALID-001 / TD-AUTH-INVALID-001 | AE-UI-TC-022 | (review text, no fixed TD ID — free text) | AE-API-TC-009 | TD-API-009 |
| AE-UI-TC-007 | TD-USER-VALID-001 | AE-UI-TC-023 | None (Recommended Items selection) | AE-API-TC-010 | TD-API-010 |
| AE-UI-TC-008 | TD-USER-EXISTING-001 | AE-UI-TC-024 | TD-PRODUCT-001 | AE-API-TC-011 | TD-API-PAYLOAD-CREATEACCOUNT-001 |
| AE-UI-TC-009 | TD-CONTACT-001, TD-FILE-001 | AE-UI-TC-025 | TD-PRODUCT-001, TD-USER-NEW-002, TD-CHECKOUT-001, TD-PAYMENT-001 | AE-API-TC-012 | TD-API-PAYLOAD-DELETEACCOUNT-001 |
| AE-UI-TC-010 | None | AE-UI-TC-026 | TD-USER-NEW-003, TD-PRODUCT-001, TD-CHECKOUT-001, TD-PAYMENT-001 | AE-API-TC-013 | TD-API-PAYLOAD-UPDATEACCOUNT-001 |
| AE-UI-TC-011 | TD-PRODUCT-001 | AE-UI-TC-027 | TD-USER-VALID-001, TD-PRODUCT-001, TD-CHECKOUT-001, TD-PAYMENT-001 | AE-API-TC-014 | TD-API-014 |
| AE-UI-TC-012 | TD-SEARCH-VALID-001 | AE-UI-TC-028 | TD-USER-NEW-004 | AE-E2E-TC-001 | TD-USER-NEW-001, TD-API-PAYLOAD-CREATEACCOUNT/DELETEACCOUNT-001 |
| AE-UI-TC-013 | TD-SEARCH-NOMATCH-001 | AE-UI-TC-029 | (inherits from completing checkout TC) | AE-E2E-TC-002 | Same + TD-PRODUCT-001, TD-CHECKOUT-001, TD-PAYMENT-001 |
| AE-UI-TC-014 | TD-SEARCH-ANOMALY-001 | AE-API-TC-001 | TD-API-001 | AE-E2E-TC-003 | TD-API-001, TD-PRODUCT-001 |
| AE-UI-TC-015 | TD-PRODUCT-002/003, TD-CART-MULTI-001 | AE-API-TC-002 | TD-API-002 | | |
| AE-UI-TC-016 | TD-PRODUCT-001, TD-CART-QTY-VALID | AE-API-TC-003 | TD-API-003 | | |

## 29. Verification Gaps

Every REQUIRES VERIFICATION item from this document, consolidated:

| Data ID | Unknown |
|---|---|
| TD-USER-* (creation flow) | Whether the exact UI/error signals TS documented still hold |
| TD-SEARCH-NOMATCH-001 | Whether the AUT shows an explicit "no results" state |
| TD-CATEGORY-001/002 | The category-ID-to-name mapping |
| TD-CART-QTY-BOUNDARY-CANDIDATE | Whether an invalid quantity is rejected, clamped, or accepted |
| TD-CHECKOUT-001 / TD-PAYMENT-001 / TD-INVOICE-001 | Whether these fields even exist as described, and their exact behavior |
| TD-CONTACT-001 / TD-SUBSCRIPTION-001 | Exact success-message text |

This table is a direct restatement of [07-Test-Cases.md](07-Test-Cases.md) §12/§18 at the data level — nothing new is left unresolved that wasn't already flagged.

## 30. Risks / Constraints

Carried forward, not re-derived:

- **Shared public environment** ([02](02-Application-Analysis.md) §14) — every generated/mutating dataset in this document is designed around that constraint (uniqueness, mandatory cleanup).
- **No verified cart-clearing or subscription-reversal mechanism** (Section 24) — a genuine, currently-unmitigated gap; repeated CI execution of TD-CONTACT-001/TD-SUBSCRIPTION-001-dependent cases will leave permanent side effects on the AUT.
- **Account mutation requires explicit authorization** ([07](07-Test-Cases.md) §19) — this document's TD-API-PAYLOAD-* and TD-USER-NEW-* datasets are fully designed but cannot be exercised without that authorization.
- **Checkout/payment fields are unconfirmed** — TD-CHECKOUT-001/TD-PAYMENT-001/TD-INVOICE-001 are RECOMMENDED starting points only.
- **Environment-sensitive product/category references** — TD-PRODUCT-*/TD-CATEGORY-* could go stale if the demo catalog changes.

## 31. QA Lead Review Items

1. **Provisioning the two durable accounts** (TD-USER-VALID-001, TD-USER-EXISTING-001) requires the same account-creation authorization already pending from Step 7 — this document cannot resolve that, only restate the dependency.
2. **TD-CONTACT-001/TD-SUBSCRIPTION-001 have no verified reversal mechanism** — confirm whether repeated real submissions to the AUT's feedback/mailing systems during future automated runs is acceptable, or whether these cases should run less frequently than the rest of the suite.
3. **TD-CART-QTY-BOUNDARY-CANDIDATE's exact value is undefined** — confirm this should stay unresolved until directly investigated, rather than guessed at now.
4. **TD-PAYMENT-001's dummy card value is REFERENCE-BASED on the TS project's example** — confirm reuse of that same placeholder pattern is acceptable, or direct an alternative.

## 32. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 8 Exit Criteria

- [x] Steps 1–7 reviewed
- [x] TS `AE-TDD-001` (full document, including previously-unread §8–19), `AE-TC-001`, `AE-AS-001` reviewed
- [x] All 46 Test Cases considered; every data-dependent case has a `TD-*` reference (Section 28)
- [x] No unsupported application constraint invented — every unconfirmed field/value marked REQUIRES VERIFICATION or RECOMMENDED, never asserted as fact
- [x] Shared-environment risks documented (Sections 8, 24, 25, 30)
- [x] Account mutation data explicitly execution-restricted (Section 19)
- [x] Checkout/payment uncertainty preserved (Section 14)
- [x] Static vs. dynamic data clearly separated (Section 21)
- [x] Cleanup requirements documented per dataset (Section 24)
- [x] Sensitive-data handling documented (Section 23)
- [x] Test Data IDs consistent with, not divergent from, the already-approved Step 7 placeholders (Section 6)
- [x] Traceability complete (Section 28)
- [x] No account/data mutation occurred while producing this document
- [x] No automation code, dependencies, or other files created
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 9 — Automation Scope.
