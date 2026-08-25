# 16 — Hybrid E2E Automation

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-HYBRID-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 9 — Hybrid E2E |
| Step | Step 16 — Hybrid E2E Automation |
| Predecessor Documents | [01](01-Project-Vision.md)–[15](15-API-Automation.md), all ✅ approved |

## 1. Objective

Implement the single Hybrid Test Case approved for automation in Step 9, reusing the existing `ProductsApiClient` (Step 13/15) and `ProductsPage` (Step 13/14) unmodified in their core responsibilities, orchestrated entirely from the Hybrid test layer, with architectural separation preserved.

## 2. Approved Hybrid Automation Scope

Directly confirmed by re-reading [09-Automation-Scope.md](09-Automation-Scope.md) before any code was written (not assumed from memory, per instruction):

| Case | Classification |
|---|---|
| AE-E2E-TC-001 | **DEFERRED** — sequenced after AE-UI-TC-005 (Login) stabilizes; not implemented |
| AE-E2E-TC-002 | **DEFERRED** — blocked on Checkout route/flow resolution; not implemented |
| AE-E2E-TC-003 | **AUTOMATE** — the only approved Hybrid case; implemented this step |

## 3. Exact Hybrid Test Case ID

**AE-E2E-TC-003.**

## 4. Business Flow

Per [07-Test-Cases.md](07-Test-Cases.md), [08-Test-Data.md](08-Test-Data.md) §20, [10-Automation-Strategy.md](10-Automation-Strategy.md) §6, and [11-Framework-Architecture.md](11-Framework-Architecture.md) §10:

1. **Business objective:** prove the Products page renders the same catalog data (name, price) the backend API actually holds — removing reliance on hard-coded UI expectations and catching a UI/backend rendering mismatch neither a pure-UI nor a pure-API test could catch alone.
2. **Preconditions:** none — unauthenticated, no cart state, no prior data setup required.
3. **API responsibility:** retrieve the full product list via `GET /api/productsList` (the same endpoint `AE-API-TC-001` exercises, reused for a different purpose here, not re-implemented).
4. **UI responsibility:** render the Products page and expose the same name/price fields for every visible product.
5. **Required Test Data:** none static — the API's own live response *is* the oracle for the comparison (per [08-Test-Data.md](08-Test-Data.md) §20: "the API response and UI rendering must be captured from the same point in time").
6. **Expected API evidence:** `responseCode` 200, a non-empty `products` array.
7. **Expected UI evidence:** a non-empty set of rendered product cards, each with a name and price.
8. **Cleanup requirement:** none — entirely read-only on both sides; no state is created or mutated.
9. **Traceability requirement:** `REQ-E2E-003` → `AE-E2E-SC-003` → `AE-E2E-TC-003` → this test, stated in the test's own docstring (Section 13) — no second traceability mechanism introduced.

## 5. API / UI Responsibility Split

| Layer | Responsibility | Component (reused, unmodified in its core contract) |
|---|---|---|
| API | Data retrieval (oracle) | `ProductsApiClient.get_products_list()` |
| UI | Rendering (subject under test) | `ProductsPage.get_rendered_products()` (new method, DOM-reading only — Section 8) |
| Hybrid test | Orchestration + comparison | `tests/hybrid/test_product_data_consistency.py` |

No HTTP call exists inside `ProductsPage`. No browser/DOM call exists inside `ProductsApiClient`. The comparison logic itself lives only in the test, per instruction rule 5.

## 6. Test Data Used

None static. Per [08-Test-Data.md](08-Test-Data.md) §20's own design (no new Hybrid-only dataset), the live API response is captured and used directly as the comparison oracle — using a static `TD-PRODUCT-*` literal here would defeat the test's actual purpose (catching drift between whatever the catalog *currently* contains and what the UI renders).

## 7. Preconditions

None. Unauthenticated session; no cart, account, or prior navigation state required.

## 8. Implementation Architecture

- **`ProductsApiClient`** — zero changes. `get_products_list()` (Step 13) called exactly as `AE-API-TC-001` calls it.
- **`ProductsPage.get_rendered_products()`** — new method (Section 12 covers why it was needed and how it evolved). Reads `.productinfo p`/`.productinfo h2` text for every `.product-image-wrapper` card. Pure DOM reading, no assertions, no HTTP.
- **`BasePage.block_third_party_ads()`** — new, generic, reusable method (Section 12/20) added to the shared foundation, not to `ProductsPage` specifically, since it's a browser-level (Playwright network routing) capability with no AUT-specific business logic — consistent with [11-Framework-Architecture.md](11-Framework-Architecture.md) §12's "generic browser operations belong in `BasePage`" rule. Invoked only by the Hybrid test, not globally, so it cannot silently alter any already-passing Step 14 UI test's behavior.
- **The Hybrid test** — the only file in the entire project that imports both `src.api.*` and `src.pages.*` (Section 24 confirms this is still the *only* such file, preserving ADR-7 from [11-Framework-Architecture.md](11-Framework-Architecture.md) §42).

No new abstraction layer, no second fixture system, no new dependency was introduced.

## 9. Fixtures Used

`products_api` (session-scoped, Step 13) and `products_page` (function-scoped, Step 13/14) — both reused directly from `tests/conftest.py`, unmodified. No new fixture was added for this step.

## 10. Page Objects Used

`ProductsPage` only (extended with one new method — Section 8/12).

## 11. API Clients Used

`ProductsApiClient` only (unmodified).

## 12. Test Implementation

`tests/hybrid/test_product_data_consistency.py::test_ae_e2e_tc_003_ui_product_listing_matches_api_product_data`. Sequence: call the API, assert transport status and `responseCode` separately (Section 17 explains why), capture the API's (name, price) pairs; navigate the UI (with ad-blocking active — Section 20), capture the UI's (name, price) pairs; assert no UI-rendered pair is absent from the API's data, and assert the two counts match. This is a genuine cross-layer defect-catching assertion — not "something was returned."

**Implementation had to overcome two real, evidence-based obstacles before it could produce a meaningful result (full detail in Section 20):** (1) a whitespace-representation difference between layers, and (2) third-party ad-script DOM injection that corrupted bulk text extraction. Both are documented as findings, not silently patched away.

## 13. Traceability Mapping

`REQ-E2E-003` → `AE-E2E-SC-003` → `AE-E2E-TC-003` → (no static `TD-*`, live API response as oracle) → `test_ae_e2e_tc_003_ui_product_listing_matches_api_product_data` — stated directly in the test's own docstring, the same mechanism used throughout Steps 14–15, no second system introduced.

## 14. Execution Commands

```bash
# Collection check
pytest tests/hybrid --collect-only -q

# Hybrid test in isolation
pytest tests/hybrid -v --html=reports/html/hybrid_suite.html --self-contained-html

# Determinism (repeated)
pytest tests/hybrid -v   # run 2
pytest tests/hybrid -v   # run 3

# Complete existing suite
pytest -v
```

## 15. Independent Execution Results

First isolated run **failed** with a genuine, evidence-based finding (Section 20) — not a framework/harness problem. After the finding was root-caused and fixed (network-level ad blocking, Section 20), the isolated run **passed**: `1 passed`.

## 16. Determinism Results

3 consecutive isolated runs after the fix: **1 passed, 1 passed, 1 passed** — fully deterministic.

## 17. Cross-Browser Results

**Not executed on Firefox/WebKit, by design.** `AE-E2E-TC-003` is not part of the curated cross-browser subset already approved in [05-Test-Strategy.md](05-Test-Strategy.md) §9 / [10-Automation-Strategy.md](10-Automation-Strategy.md) §17 (invalid login, cart add/remove, checkout gate — [09-Automation-Scope.md](09-Automation-Scope.md) §6 lists `E2E-003` as PR-tier, `CI-SAFE`, not `cross_browser`-tagged). Its flow (page load + text extraction) is also not the class of Bootstrap-animation-timing sensitivity that motivated the curated subset in the first place. Per instruction — "execute the approved browser coverage defined by the strategy" — no coverage beyond Chromium is currently approved for this case, so none was added unilaterally.

## 18. Full Regression Results

`pytest -v` (full suite): **49 passed, 1 skipped (pre-existing, unrelated), 0 failed**, 99.20s. All 12 Step 14 UI tests and all 9 Step 15 API tests re-ran and passed identically alongside the new Hybrid test — zero regression.

**One additional flaky-test occurrence observed during final verification, recorded honestly rather than omitted:** a subsequent full-suite re-run (performed as part of this step's closing checks) showed one failure in `test_ae_ui_tc_019_view_category_products_and_switch_category` — a recurrence of the same pre-existing environmental flakiness class already disclosed in [14-UI-Automation.md](14-UI-Automation.md) §12 (item 4)/§14, which previously affected the sibling test `AE-UI-TC-020` once under full-suite load and was never fully root-caused (traced to low-frequency public-site variability, not a locator defect — `networkidle` was tried and rejected as a fix in Step 14 for the same reason). This step's changes did not touch `ProductsPage.open_category()` or anything else `AE-UI-TC-019` depends on — Step 16 only added new methods (`get_rendered_products()`, `block_third_party_ads()`). Investigated the same way Step 14 investigated its occurrence: 3 consecutive isolated re-runs of `AE-UI-TC-019` all passed cleanly, and a further full-suite re-run afterward was clean (49 passed, 1 skipped, 0 failed). Recorded as a second data point for the same known, disclosed, low-frequency risk — not a new defect, and not chased further with an ad hoc fix; per [05-Test-Strategy.md](05-Test-Strategy.md) §16, the correct mechanism for this class of issue is the already-approved CI-only bounded-retry policy, still pending implementation at Step 19.

## 19. AUT Pass/Fail/Block/Restricted/Skipped Status

- **AUT passed:** the underlying business behavior is confirmed correct — the live Products page, once third-party ad noise is excluded, renders exactly the 34 products the API reports, with matching names and prices.
- **AUT failed:** none, in the final state. The *first* run's failure (Section 20) was root-caused to third-party ad-script interference and an extraction-robustness gap, not to the AUT's own product-rendering logic being wrong.
- **Blocked:** `AE-E2E-TC-001`/`002` (Section 27) — not attempted, per the already-approved `DEFERRED` classification.
- **Restricted:** none applicable to this case.
- **Skipped:** none for the implemented case.

## 20. Defects / Observations Discovered

**Two distinct, fully-evidenced findings**, both investigated to root cause before any fix was applied — neither was worked around blindly, and neither was resolved by weakening the test's assertions:

**Finding 1 — Whitespace representation differs between layers (minor).** For at least one product ("Men Tshirt" / "Sleeveless Dress"), the live DOM originally appeared to contain a non-breaking space (`\xa0`) where the API's JSON contains a regular space. Investigation (Section 20, Finding 2) showed this specific artifact was actually a byproduct of Finding 2's DOM injection (an injected element rendered as a space-like character in `.inner_text()`), not an independent AUT template inconsistency — once Finding 2 was fixed, this artifact disappeared entirely and all 34 names matched byte-for-byte. Recorded here for completeness; not a standalone defect.

**Finding 2 — Major: `automationexercise.com` genuinely embeds live Google Ads / Ad Traffic Quality / Funding Choices infrastructure, which mutates product-name DOM elements.** VERIFIED via direct network capture during implementation (not assumed): the live page loads real requests to `pagead2.googlesyndication.com` (Google AdSense), `googleads.g.doubleclick.net`, `ep1/ep2.adtrafficquality.google` (Google's ad-fraud/"Sodar" quality scripts), and `fundingchoicesmessages.google.com` (Google consent/Funding Choices messaging) — confirming this is real, production ad-tech the site operator has embedded, not a browser or test-tool artifact. Direct DOM inspection showed this ad infrastructure's own annotation/"vignette" system injects elements such as:

```html
<p>Sleeves Printed Top - White<div class="google-anno-skip google-anno-sc" role="link"
   aria-label="Product Photography Service" data-google-vignette="false" ...>...</div></p>
<p><a href="#" class="google-anno" data-google-vignette="false" ...>...</a></p>  <!-- wraps/replaces original text -->
```

**directly as children of, or wrapping, the original product-name text nodes** — for roughly 6–8 of the 34 products at any given page load. This is a **generalization and confirmation** of the third-party DOM-pollution risk Step 14 already flagged for the category sidebar (role-based locator pollution, [14-UI-Automation.md](14-UI-Automation.md) §12/13): it is now confirmed to affect **plain text-content extraction** too, and to occur **inside individual product listings**, not just the sidebar. This is recorded as an **observation for QA Lead awareness**, not a confirmed application defect — it is genuine, live behavior of a third-party ad system the site itself has chosen to embed, and this project has no channel to change that (consistent with [04-Test-Plan.md](04-Test-Plan.md) §16's established framing for third-party AUT behavior).

**Resolution:** `BasePage.block_third_party_ads()` (Section 8/12) blocks the 4 confirmed ad-domain fragments at the Playwright network-routing level before navigation. VERIFIED to fully eliminate the injection (0 `google-anno`/`google-anno-skip` elements found after blocking, across a direct standalone check) and to restore all 34 product names to an exact, byte-for-byte match against the API's data. This is standard, principled test-automation practice — excluding known-irrelevant, non-deterministic third-party ad/tracking traffic from a test that is specifically about validating the AUT's *own* data — not an assertion weakening; the comparison logic itself was never touched.

## 21. Framework Issues Discovered and Fixed

- **`ProductsPage` had no method to extract rendered catalog data as structured data** (only interaction methods existed from Step 14, which never needed this). Added `get_rendered_products()` — a genuine, necessary architecture completion, not scope creep, since [11-Framework-Architecture.md](11-Framework-Architecture.md) §10 already specified this exact capability ("`products_page.get_rendered_products()`") as part of the approved Hybrid architecture.
- **No prior test in this project performed bulk (34-item) text extraction**, so the third-party ad-injection risk (Finding 2) had never been triggered before — Steps 14/15's tests each touch at most 1–2 products via targeted, scoped interactions, which happened not to intersect with an injected element. This step's larger surface area is what first fully exposed the issue.

## 22. Scope Deviations

None from the approved automation scope, strategy, or architecture. `BasePage.block_third_party_ads()` is an *architecture completion* (a generic browser capability, exactly the kind of thing [11-Framework-Architecture.md](11-Framework-Architecture.md) §12 anticipated `BasePage` would hold), not a scope expansion — it automates nothing new; it removes noise from an already-approved test.

## 23. Environment / Shared-State Limitations

- **No account, cart, or any other state was created or mutated** — the entire flow is read-only on both layers.
- **The third-party ad-injection pattern (Finding 2) is itself an environment limitation** worth carrying forward: any *future* test performing bulk DOM text extraction on this AUT should reuse `block_third_party_ads()` rather than rediscover this issue.
- **The live catalog's exact product set is not under this project's control** — the test is deliberately designed (no static `TD-PRODUCT-*` literal) to remain correct even if the catalog changes, since it compares against whatever the API returns *at the moment of the test run*, not a fixed expectation.

## 24. Architecture Validation

- `pages/` never imports `api/`; `api/` never imports `pages/` — confirmed via direct grep across both directories, zero matches.
- The Hybrid test is the **only** file importing both `src.api.*` and `src.pages.*` in the entire project — preserving [11-Framework-Architecture.md](11-Framework-Architecture.md) §42 ADR-7 exactly as designed.
- No test imports another test — confirmed via direct grep.
- No arbitrary `wait_for_timeout`/`time.sleep` in any new or modified file — confirmed.
- Reporting/diagnostics configuration reused unchanged from Step 13 (`pytest-html`, screenshot-on-failure, trace-retain-on-failure via `pyproject.toml` `addopts`) — nothing was reconfigured.

## 25. Secret-Handling Validation

Pattern-based scan across all new/modified files (`tests/hybrid/*`, `src/pages/base_page.py`, `src/pages/products_page.py`) for `password=`/`api_key=`/`secret=`/`token=`-style literals: **zero matches**. No credential of any kind is used by this test — it is fully unauthenticated.

## 26. Regression Impact

Full suite grew from 49 to 50 collected tests (1 new Hybrid test added), pass count grew from 48 to 49, skip count unchanged at 1, fail count unchanged at 0. All 21 previously-implemented tests (12 UI + 9 API) re-ran and passed identically — zero regression from this step's changes.

## 27. Remaining Hybrid Cases and Why They Remain Unimplemented

| Case | Status | Reason |
|---|---|---|
| AE-E2E-TC-001 | `DEFERRED` (unchanged) | Per [09-Automation-Scope.md](09-Automation-Scope.md)/[10-Automation-Strategy.md](10-Automation-Strategy.md) §6, sequenced after `AE-UI-TC-005` (Login) is independently stable — `AE-UI-TC-005` remains blocked on the account-provisioning authorization gate ([14-UI-Automation.md](14-UI-Automation.md) §8), which has not changed since Step 14/15. **Not implemented, not worked around, not reclassified.** |
| AE-E2E-TC-002 | `DEFERRED` (unchanged) | Blocked entirely on the unresolved Checkout route/flow ([03-Requirement-Analysis.md](03-Requirement-Analysis.md) §5 rows 1/4) — unchanged since Step 9. **Not implemented, not worked around, not reclassified.** |

Both blockers are identical in nature to ones already documented in Steps 9, 14, and 15 — no new blocker was discovered, and none of the existing ones were resolved by this step (this step's scope did not touch Login or Checkout).

## 28. Step 16 Exit Criteria

- [x] Steps 1–15 reviewed; the exact approved Hybrid Test Case ID confirmed by reading [09-Automation-Scope.md](09-Automation-Scope.md) directly, not assumed from memory
- [x] Only `AE-E2E-TC-003` implemented; `AE-E2E-TC-001`/`002` not implemented, not worked around, not reclassified
- [x] API interaction (data retrieval) and UI interaction (rendering validation) both present and correctly separated
- [x] Existing `ProductsApiClient`/`ProductsPage`/fixtures/configuration/test-data architecture reused; no second architecture introduced
- [x] No HTTP implementation inside any Page Object; no browser/UI implementation inside any API client
- [x] Orchestration and comparison logic kept entirely inside the Hybrid test
- [x] No unnecessary abstraction introduced; `block_third_party_ads()` added only because implementation genuinely required it, and placed in the architecturally correct location
- [x] No new dependency added
- [x] No arbitrary sleeps
- [x] Existing reporting/diagnostic configuration reused unchanged
- [x] Traceability preserved via the existing docstring mechanism — no second system
- [x] Transport-level HTTP status and the AUT's own `responseCode` asserted separately, per the Step 15 finding
- [x] A genuine AUT/environment discrepancy (third-party ad injection) was found, root-caused, and fixed via a principled, disclosed mechanism — not by weakening any assertion
- [x] Test run independently, and at least twice for determinism (run 3 times total, all passed after the fix)
- [x] Approved browser coverage respected — no unapproved cross-browser expansion
- [x] Complete regression suite run; all previously-passing UI and API tests confirmed still passing
- [x] Architecture violations checked — none found
- [x] Secret exposure checked — none found
- [x] No unintended file changed (confirmed; two stray debug scripts created during investigation were found and removed before finalizing)
- [x] docs/01–15 unmodified
- [x] TypeScript project unmodified
- [ ] QA Lead Review & Approval

## 29. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 17 — Execution.
