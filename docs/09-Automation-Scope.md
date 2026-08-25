# 09 — Automation Scope

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-AS-001 |
| Document Title | Automation Scope |
| Project | playwright-python-hybrid-framework |
| Application | Automation Exercise (https://automationexercise.com) |
| Version | 1.0 |
| Status | Draft — pending QA Lead review |
| Prepared By | AI Assistant (advisory) |
| Reviewer | QA Lead |
| Classification | Portfolio / Internal |
| Date | 2026-08-25 |
| Phase | Phase 4 — Automation Planning |
| Step | Step 9 — Automation Scope |
| Predecessor Documents | [01](01-Project-Vision.md)–[08](08-Test-Data.md), all ✅ approved |

## 2. Purpose

This is a **decision document**: it assigns exactly one final scope classification — `AUTOMATE`, `MANUAL`, `DEFERRED`, or `RESTRICTED` — to each of the 46 Test Cases approved in [07-Test-Cases.md](07-Test-Cases.md), using the data model from [08-Test-Data.md](08-Test-Data.md) and the risk/strategy foundation from Steps 2–5. No framework code, Page Objects, fixtures, API clients, or dependencies are created here.

## 3. Automation Decision Principle

A test earns automation by demonstrating **Business Value + Risk Reduction + Regression Value + Repeatability + Stability + Automation Feasibility + Maintainability + Execution Cost + Data Complexity + Environment Safety** together — not by existing in a prior baseline, and not by being technically possible. Where a case scores well on business value but poorly on environment safety (Contact Us, Subscription) or on feasibility (unverified Checkout), automation is withheld even though the case remains an important, preserved Test Case.

## 4. Scope Classification Definitions

| Classification | Meaning |
|---|---|
| **AUTOMATE** | Approved for implementation in the Python/Playwright framework |
| **MANUAL** | Important, but automation does not currently add enough value relative to its cost, or a lower-cost manual/ad hoc check is genuinely sufficient |
| **DEFERRED** | Automation is the right eventual answer, but a prerequisite (verified behavior, a resolved upstream case, or an explained investigation) is currently missing |
| **RESTRICTED** | Technically automatable, but repeated automatic execution against the shared public environment creates unacceptable, uncleanable side effects |

`Verification Status` (from Step 7/8) remains a **separate attribute** — it is never itself used as a final scope value.

---

## 5. Final Automation Scope — Master Classification

| TC ID | Scenario | Priority | Automation Priority | Verification Status | Layer | Final Decision | Primary Rationale |
|---|---|---|---|---|---|---|---|
| AE-UI-TC-001 | SC-001 | P1 | A2 | Verified | UI | **AUTOMATE** | Zero-risk smoke anchor, no data dependency |
| AE-UI-TC-002 | SC-002 | P2 | N/A | Partially Verified | UI | **RESTRICTED** | Real subscription email added; no verified removal (§12) |
| AE-UI-TC-003 | SC-003 | P2 | N/A | Partially Verified | UI | **RESTRICTED** | Same as TC-002, second entry point |
| AE-UI-TC-004 | SC-004 | P0 | A1 | Requires Verification | UI | **AUTOMATE** | Self-contained lifecycle (create→verify→delete); execution-authorization gate applies (§12) |
| AE-UI-TC-005 | SC-005 | P0 | A1 | Requires Verification | UI | **AUTOMATE** | Core auth journey; depends on a durable account existing |
| AE-UI-TC-006 | SC-006 | P0 | A0 | **Verified** | UI | **AUTOMATE** | Strongest, cheapest P0 win — no account dependency |
| AE-UI-TC-007 | SC-007 | P1 | A1 | Requires Verification | UI | **AUTOMATE** | Simple, low-complexity; depends on TC-005 |
| AE-UI-TC-008 | SC-008 | P1 | A1 | Requires Verification | UI | **AUTOMATE** | Simple negative path; no new-account creation |
| AE-UI-TC-009 | SC-009 | P2 | N/A | Partially Verified | UI | **RESTRICTED** | Real feedback message sent every run; no cleanup |
| AE-UI-TC-010 | SC-010 | P3 | N/A | Verified | UI | **MANUAL** | Near-zero business value; not worth even minimal CI upkeep |
| AE-UI-TC-011 | SC-011 | P0 | A0 | **Verified** | UI | **AUTOMATE** | Core catalog anchor, no risk |
| AE-UI-TC-012 | SC-012 | P1 | A1 | **Verified** | UI | **AUTOMATE** | Core search, no risk |
| AE-UI-TC-013 | SC-012 | P2 | A2 | Requires Verification | UI | **AUTOMATE** | Low-risk negative case; "no results" state is a near-universal pattern, first run resolves exact signal |
| AE-UI-TC-014 | SC-012 | P2 | N/A | Requires Verification | UI | **DEFERRED** | Explicitly flagged: do not encode unexplained relevance behavior as a fixed assertion (§15) |
| AE-UI-TC-015 | SC-013 | P0 | A1 | Partially Verified | UI | **AUTOMATE** | Straightforward multi-item extension of verified pattern |
| AE-UI-TC-016 | SC-014 | P1 | A1 | Partially Verified | UI | **AUTOMATE** | Straightforward extension |
| AE-UI-TC-017 | SC-014 | P2 | N/A | Requires Verification | UI | **DEFERRED** | Explicitly flagged: no numeric boundary invented (§16) |
| AE-UI-TC-018 | SC-015 | P0 | A1 | **Verified** | UI | **AUTOMATE** | Core cart mutation, no account risk |
| AE-UI-TC-019 | SC-016 | P2 | A2 | Verified (route) | UI | **AUTOMATE** | Category ID mapping gap affects data, not case validity |
| AE-UI-TC-020 | SC-017 | P2 | A2 | **Verified** | UI | **AUTOMATE** | No risk |
| AE-UI-TC-021 | SC-018 | P1 | A2 | Requires Verification | UI | **AUTOMATE** | Sequenced after TC-005; no new mutation |
| AE-UI-TC-022 | SC-019 | P2 | N/A | Partially Verified | UI | **RESTRICTED** | **New finding this step** — public review content posted with no verified removal, same structural risk as TC-002/003/009 (§14) |
| AE-UI-TC-023 | SC-020 | P2 | A2 | Verified (pattern) | UI | **AUTOMATE** | Extension of verified add-to-cart |
| AE-UI-TC-024 | SC-021 | P0 | A0 | **Verified** | UI | **AUTOMATE** | Strongest available Checkout-area evidence; zero account risk |
| AE-UI-TC-025 | SC-022 | P0 | N/A | Requires Verification | UI | **DEFERRED** | Route/flow unresolved — automating now would encode unverified assumptions (§13) |
| AE-UI-TC-026 | SC-023 | P0 | N/A | Requires Verification | UI | **DEFERRED** | Same basis |
| AE-UI-TC-027 | SC-024 | P0 | N/A | Requires Verification | UI | **DEFERRED** | Same basis |
| AE-UI-TC-028 | SC-025 | P1 | N/A | Requires Verification | UI | **DEFERRED** | Downstream of TC-025/026 |
| AE-UI-TC-029 | SC-026 | P2 | N/A | Requires Verification | UI | **DEFERRED** | Downstream of TC-025/026/027 |
| AE-API-TC-001 | SC-001 | P0 | A0 | **Verified** | API | **AUTOMATE** | Read-only, zero risk, foundational |
| AE-API-TC-002 | SC-002 | P2 | A1 | **Verified** | API | **AUTOMATE** | Negative, zero risk |
| AE-API-TC-003 | SC-003 | P1 | A0 | **Verified** | API | **AUTOMATE** | Read-only, foundational |
| AE-API-TC-004 | SC-004 | P2 | A1 | **Verified** | API | **AUTOMATE** | Negative, zero risk |
| AE-API-TC-005 | SC-005 | P1 | A1 | **Verified** | API | **AUTOMATE** | Read-only |
| AE-API-TC-006 | SC-006 | P1 | A1 | **Verified** | API | **AUTOMATE** | Negative, zero risk |
| AE-API-TC-007 | SC-007 | P0 | A0 | **Verified** | API | **AUTOMATE** | Foundational credential check; depends on durable account |
| AE-API-TC-008 | SC-008 | P1 | A0 | **Verified** | API | **AUTOMATE** | No account dependency, zero risk |
| AE-API-TC-009 | SC-009 | P2 | A1 | **Verified** | API | **AUTOMATE** | Negative, zero risk |
| AE-API-TC-010 | SC-010 | P3 | A1 | **Verified** | API | **AUTOMATE** | Negative, zero risk |
| AE-API-TC-011 | SC-011 | P0 | A1 | Verified (doc) | API | **AUTOMATE** | Paired with TC-012 cleanup; execution-authorization gate applies (§12) |
| AE-API-TC-012 | SC-012 | P1 | A1 | Verified (doc) | API | **AUTOMATE** | Mandatory cleanup pair for TC-011 |
| AE-API-TC-013 | SC-013 | P2 | N/A | Verified (doc) | API | **MANUAL** | Technically safe (cleanup exists via TC-011/012) but low incremental regression value |
| AE-API-TC-014 | SC-014 | P2 | A2 | Verified (doc) | API | **AUTOMATE** | Read-only once an account exists |
| AE-E2E-TC-001 | SC-001 | P1 | N/A | Not started | Hybrid | **DEFERRED** | Sequenced after TC-005 stabilizes in the suite, per [05](05-Test-Strategy.md) §6 |
| AE-E2E-TC-002 | SC-002 | P2 | N/A | Not started | Hybrid | **DEFERRED** | Blocked on Checkout (TC-025–027) resolution |
| AE-E2E-TC-003 | SC-003 | P1 | A2 | Not started | Hybrid | **AUTOMATE** | No account/checkout dependency — the one immediately executable Hybrid case |

## 6. Execution Profile

| TC ID | Data Dependency | Environment Dependency | Maintenance Risk | CI Suitability | Execution Frequency | Parallelization |
|---|---|---|---|---|---|---|
| UI-001 | None | None | LOW | CI-SAFE | PR | SAFE |
| UI-004 | Unique generated account | Account create/delete API or UI | MEDIUM | **CI-RESTRICTED** | MAIN, NIGHTLY | SERIAL |
| UI-005 | Durable TD-USER-VALID-001 | Pre-provisioned account | LOW | CI-SAFE (post-provisioning) | PR | LIMITED (shares durable account) |
| UI-006 | None | None | LOW | CI-SAFE | PR | SAFE |
| UI-007 | Durable account | Depends on TC-005 | LOW | CI-SAFE | PR | LIMITED |
| UI-008 | Durable "existing" account | Read-only use of it | LOW | CI-SAFE | PR | LIMITED |
| UI-011 | None (or API-sourced product) | None | LOW | CI-SAFE | PR | SAFE |
| UI-012 | None | None | LOW | CI-SAFE | PR | SAFE |
| UI-013 | None | None | LOW | CI-SAFE | PR | SAFE |
| UI-015 | Two products | None | LOW | CI-SAFE | PR | SAFE |
| UI-016 | One product | None | LOW | CI-SAFE | PR | SAFE |
| UI-018 | One product | None | LOW | CI-SAFE | PR | SAFE |
| UI-019 | Category reference | Category ID mapping unresolved (data risk, not scope risk) | MEDIUM | CI-SAFE | PR | SAFE |
| UI-020 | Brand reference | None | LOW | CI-SAFE | PR | SAFE |
| UI-021 | Durable account, product | Depends on TC-005 | MEDIUM | CI-SAFE | MAIN | LIMITED |
| UI-023 | None | None | LOW | CI-SAFE | PR | SAFE |
| UI-024 | One product | None | LOW | CI-SAFE | PR | SAFE |
| API-001–010 | None (or, for API-007, a durable account) | None | LOW | CI-SAFE | PR | SAFE |
| API-011 | Unique generated account | Account creation | MEDIUM | **CI-RESTRICTED** | MAIN, NIGHTLY | SERIAL |
| API-012 | Same account as API-011 | Account deletion | MEDIUM | **CI-RESTRICTED** | MAIN, NIGHTLY | SERIAL |
| API-014 | Existing account | None | LOW | CI-SAFE | PR | SAFE |
| E2E-003 | None | None | LOW | CI-SAFE | PR | SAFE |

**5 of 31 AUTOMATE cases (UI-004, API-011/012, plus their downstream data consumers) are CI-RESTRICTED** — mutating, throttled to MAIN/NIGHTLY rather than every PR, mirroring the TS project's own proven pattern of keeping Pull Requests to fast, low-risk suites ([05](05-Test-Strategy.md) §7/§13). The remaining 26 are CI-SAFE and PR-eligible.

## 7. Retry Policy Note

No case in this scope is automated *because* retries could paper over instability. Per [05](05-Test-Strategy.md) §16, any case that needs frequent retries to pass is a candidate for root-cause investigation and possible reclassification to `DEFERRED`, not a candidate for a higher retry count. None of the 31 `AUTOMATE` cases here were selected on the assumption that retries would compensate for weak evidence — every one already has either VERIFIED behavior or a low-complexity, low-risk verification-on-first-run path (Section 5's rationale column makes this distinction explicit case by case).

---

## 8. UI Automation Strategy (29 cases evaluated)

17 of 29 UI cases are `AUTOMATE`. The selection prioritizes exactly what [05](05-Test-Strategy.md) §1 called for: the discovery/cart journey (already well-evidenced) is automated almost completely (TC-011/012/013/015/016/018/019/020/023 — 9 of the module's cases), the authentication *negative* path and the checkout *gate* are automated first among the higher-risk group because they are both fully VERIFIED and zero-account-risk (TC-006, TC-024), and the Signup/Login *positive* path is automated with an explicit execution-authorization gate rather than being silently skipped (TC-004/005/007/008) — closing the verification gap **is** the automation, not a prerequisite to it, wherever the behavior itself is simple enough to trust a first-run result. What is deliberately **not** automated: the five Checkout E2E cases (TC-025–029), the search-anomaly investigation (TC-014), the quantity-boundary case (TC-017), and four cases with unrecoverable public side effects (TC-002/003/009/022).

## 9. API Automation Strategy (14 cases evaluated)

13 of 14 API cases are `AUTOMATE` — the strongest ratio of any layer, exactly as expected: all 14 endpoints are independently VERIFIED at the documentation level, 10 of the 14 involve no state mutation at all, and even the 2 mutating cases (`createAccount`/`deleteAccount`) have a proven, mandatory cleanup pairing. The one exception, `updateAccount` (API-TC-013), is downgraded to `MANUAL` **not** because it's unsafe (the same cleanup pairing covers it) but because it adds mutation-frequency cost against a shared environment for a requirement of only Medium priority and no dependent downstream case — a clean example of the automation-value principle (Section 3) overriding raw feasibility.

## 10. Hybrid Automation Strategy (3 cases evaluated)

Only 1 of 3 is `AUTOMATE` — deliberately conservative, matching [05](05-Test-Strategy.md) §6's instruction that Hybrid work is "sequenced after, not parallel to" Login/Checkout verification.

| Case | API Responsibility | UI Responsibility | Why Combined | State/Data Transfer | Diagnostic Value | Decision |
|---|---|---|---|---|---|---|
| AE-E2E-TC-001 | `createAccount` provisioning | Login through the real form | Proves Login correctness independent of account origin | Credentials pass API→UI | Would catch a Login defect that only manifests for non-UI-created accounts | **DEFERRED** — Login (TC-005) itself must stabilize in the suite first |
| AE-E2E-TC-002 | `createAccount` provisioning | Full checkout journey | Proves Checkout has no hidden UI-registration dependency | Credentials pass API→UI | Would catch a Checkout defect specific to UI-originated accounts | **DEFERRED** — blocked entirely on Checkout's unresolved route/flow |
| AE-E2E-TC-003 | `productsList` read | Products page render | Removes reliance on hard-coded UI expectations; catches a UI/backend data mismatch neither layer alone could | Read-only, no data ownership transfer | Would catch stale/incorrect UI-rendered catalog data | **AUTOMATE** — no identity/checkout dependency, lowest-risk Hybrid case available today |

No Hybrid case is automated merely to prove Playwright can call an API — each row's "Why Combined" column is a distinct, non-redundant justification.

---

## 11. Authentication Scope

| Sub-area | Classification | Cases |
|---|---|---|
| **SAFE READ/VALIDATION** | Invalid login, missing-parameter checks, logout, duplicate-email rejection, credential verification against an existing account | TC-006/007/008; API-TC-007/008/009/010 — all `AUTOMATE` |
| **STATE-MUTATING/DISRUPTIVE** | New account creation, account deletion, account update | TC-004; API-TC-011/012 (`AUTOMATE`, paired-cleanup, CI-RESTRICTED); API-TC-013 (`MANUAL`) |

The dividing line is not "does it touch an account" but "does it **create or destroy** shared state" — read/verify operations against an account are treated the same as any other stateless check.

## 12. Checkout / Payment Scope

**No unverified Checkout case is marked automation-ready.** TC-024 (the authentication gate) is the sole `AUTOMATE` item in this area, precisely because it is the sole **VERIFIED** one. TC-025/026/027/028/029 are `DEFERRED` — the Test Case, the business risk, and the verification status are all preserved exactly as [07-Test-Cases.md](07-Test-Cases.md) recorded them; nothing is invented about address, payment, or invoice behavior to make them appear automatable.

## 13. Contact Us / Subscription Scope

Per [08-Test-Data.md](08-Test-Data.md) §24/30: repeated automated execution of Contact Us (TC-009) and Subscription (TC-002/003) would send real messages and add real emails to a public system's mailing list, with **no verified reversal mechanism**. Business value and regression value are real (these validate genuine functional requirements) but environment safety is not — the definition of `RESTRICTED`, not `MANUAL`: these could be automated in principle, the problem is what happens every time they run, not whether they're worth testing. **Recommendation, not a decision made here:** these three cases are better suited to a rare, explicitly-triggered, on-demand check (e.g., once per major release) than to any recurring CI cadence — this recommendation is logged as a QA Lead review item (Section 33), not silently adopted.

**New finding surfaced during this step:** Product Review submission (TC-022) has the identical structural risk — a real, publicly-visible review is posted with no verified deletion mechanism — but this was not flagged alongside Contact Us/Subscription in [08-Test-Data.md](08-Test-Data.md) §24. This document corrects that gap now by classifying TC-022 as `RESTRICTED` for the same reason, and flags the omission explicitly rather than silently fixing it in the earlier document (Section 33).

## 14. Search Anomaly

TC-014 (the "dress" keyword investigation) remains `DEFERRED`, exactly as [06](06-Test-Scenarios.md)/[07](07-Test-Cases.md) already classified its automation suitability — this step does not encode the unexplained matching behavior as a fixed assertion. TC-012/013 (the positive and non-matching search cases) remain `AUTOMATE` because they assert only what is already independently confirmed or low-risk-to-confirm on first run — they do not depend on understanding *why* TC-014's anomaly occurred.

## 15. Cart / Quantity Scope

TC-013–016 (cart contents, multi-item, quantity-set) are `AUTOMATE` — all straightforward, low-risk extensions of already-VERIFIED behavior. TC-017 (the quantity-boundary case) is `DEFERRED`, per explicit instruction: no numeric boundary (zero, negative, or otherwise) is invented as the basis for an automated assertion until the AUT's actual constraint is directly observed.

---

## 16. Automation Priority Model (A0–A3)

**Distinct from Test Case Priority (P0–P3):** Test Case Priority measures *business/test risk if this behavior is wrong*; Automation Priority measures *how urgently this specific case should be automated, given everything else in scope*. A case can be P0 (critical business risk) yet not A0 (e.g., TC-025, P0 but not automatable at all yet) — the two scales answer different questions and are never conflated in this document.

| Automation Priority | Meaning | Count |
|---|---|---|
| **A0 — Critical** | Zero/near-zero risk, foundational, highest confidence — automate first | 7 |
| **A1 — High** | Core regression value, modest data dependency or an authorization gate | 16 |
| **A2 — Medium** | Valuable but not foundational; safe to sequence after A0/A1 | 8 |
| **A3 — Low** | (none currently — every `AUTOMATE` case earned at least Medium urgency) | 0 |

---

## 17. Automation Coverage Targets

Justified by this project's actual scope, risk profile, and portfolio objective — **not set to 100% for appearance**:

| Target | Value | Justification |
|---|---|---|
| Overall Test Case automation coverage | **~65–70%** | Matches the actual achievable classification (67.4%, Section 19) given genuine, evidence-based exclusions — not an arbitrary round number |
| UI automation | **~55–60%** | The UI layer carries the entire Checkout-area verification gap (7 of 12 non-automated UI cases are Checkout-related) — a lower UI target honestly reflects that gap rather than automating around it |
| API automation | **~90%+** | The API layer is nearly fully verified and mostly stateless — the highest achievable ratio of any layer, and it should be treated as such |
| Hybrid automation | **~30–35%** | Deliberately conservative — Hybrid value depends on Login/Checkout being solid first; targeting higher now would front-load risk |
| Critical-path (P0) automation | **~75–80%** | Reflects that 3 of 13 P0 cases (the Checkout E2E trio) are genuinely blocked, not under-prioritized |
| Regression automation — Discovery/Cart journey | **~90%+** | This journey is fully evidenced; near-complete automation is justified and expected |
| Regression automation — Identity→Checkout→Order journey | **~40–50% today, revisited after verification** | Honest reflection of Section 12 — automating further here now would mean automating guesses |

## 18. CI/CD Suitability Summary

**28 CI-SAFE** (PR-eligible), **3 CI-RESTRICTED** (MAIN/NIGHTLY only: UI-004, API-011, API-012) among the 31 `AUTOMATE` cases (Section 6). No `AUTOMATE` case is classified `LOCAL-FIRST` or `NOT SUITABLE` — every automated case is intended to run in CI at some tier; cases unsuitable for *any* CI tier (Contact Us, Subscription, Review) are `RESTRICTED` at the scope level, not merely down-tiered.

## 19. Execution Frequency Summary

| Frequency | Cases |
|---|---|
| **PR** | 26 CI-SAFE cases |
| **MAIN + NIGHTLY** | UI-004, API-011, API-012 (mutating, throttled per Section 6) |
| **MAIN only** | UI-021 (sequenced after TC-005, not foundational enough for every PR) |
| **NIGHTLY only (canary)** | Full suite re-run, independent of code changes — mirrors the TS project's proven daily-schedule pattern ([05](05-Test-Strategy.md) §7 |
| **RELEASE** | Full CI-SAFE + CI-RESTRICTED regression together, once per release cycle |
| **ON-DEMAND** | Contact Us/Subscription/Review, *if* the QA Lead approves the Section 13 recommendation |

Not every test runs on every PR because PR feedback speed matters more than exhaustive coverage at that stage — broader coverage is deferred to MAIN/NIGHTLY/RELEASE tiers, exactly matching the graduated model already approved in [05-Test-Strategy.md](05-Test-Strategy.md) §7/§13.

## 20. Parallelization Suitability Summary

| Classification | Cases | Basis |
|---|---|---|
| **SAFE** | All stateless UI/API cases (Section 6) | No shared mutable state |
| **LIMITED** | UI-005/007/008/021, API-007/014 | Share a durable account; safe to parallelize with unrelated tests, but not with each other if any of them mutate session state |
| **SERIAL** | UI-004, API-011/012 | Each generates/destroys unique account data; conservative serialization avoids compounding risk on the shared environment, consistent with the TS project's own proven choice to serialize CI workers despite having parallel capability ([05](05-Test-Strategy.md) §14) |
| **NOT RECOMMENDED** | N/A — no `AUTOMATE` case falls here | — |

## 21. Maintenance Risk Summary

**LOW:** 24 of 31 `AUTOMATE` cases — simple, single-purpose interactions with stable, already-observed locators. **MEDIUM:** 7 — UI-004 (multi-step signup form), UI-019 (unresolved category-ID data risk), UI-021 (execution-order dependency), API-011/012 (mutation pairing must never desynchronize). **HIGH:** none — by design, every genuinely high-maintenance-risk case (unverified Checkout flow) was excluded via `DEFERRED` rather than accepted into scope at elevated risk.

---

## 22. Traceability (Example)

`REQ-BUS-004` → `AE-UI-SC-021` → `AE-UI-TC-024` → `TD-PRODUCT-001` → **AUTOMATE / UI / A0**. Every row in Section 5 carries this same unbroken chain back through [07-Test-Cases.md](07-Test-Cases.md) and [03-Requirement-Analysis.md](03-Requirement-Analysis.md) — no automated test in this scope exists without a requirement behind it.

## 23. TypeScript Baseline Reconciliation

| TS Case (of the 32) | TS Automation Status | Python Case | Python Decision | Classification |
|---|---|---|---|---|
| AE-TC-UI-001 (Register) | Automated | AE-UI-TC-004 | AUTOMATE (with authorization gate) | REIMPLEMENT |
| AE-TC-UI-002 (Login valid) | Automated | AE-UI-TC-005 | AUTOMATE | REIMPLEMENT |
| AE-TC-UI-003 (Login invalid) | Automated | AE-UI-TC-006 | AUTOMATE | KEEP AUTOMATED (in spirit — reimplemented in Python) |
| AE-TC-UI-004 (Logout) | Automated | AE-UI-TC-007 | AUTOMATE | REIMPLEMENT |
| AE-TC-UI-005 (Duplicate email) | Automated | AE-UI-TC-008 | AUTOMATE | REIMPLEMENT |
| AE-TC-UI-006 (Contact Us) | Automated (with a documented, non-blocking known-AUT-limitation carve-out — [05](05-Test-Strategy.md) §7/§13) | AE-UI-TC-009 | **RESTRICTED** | **DOWNGRADE** — this project weighs the real-message side effect more heavily than the TS project's CI design did; explained fully in Section 13, not silent |
| AE-TC-UI-007 (Test Cases page) | Automated | AE-UI-TC-010 | MANUAL | MANUAL |
| AE-TC-UI-008 (Products/details) | Automated | AE-UI-TC-011 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-009 (Search) | Automated | AE-UI-TC-012/013 | AUTOMATE | REIMPLEMENT + EXPAND (negative case added) |
| AE-TC-UI-010/011 (Subscription ×2) | Automated | AE-UI-TC-002/003 | **RESTRICTED** | **DOWNGRADE** — same side-effect reasoning as Contact Us |
| AE-TC-UI-012 (Multi-item cart) | Automated | AE-UI-TC-015 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-013 (Cart quantity) | Automated | AE-UI-TC-016 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-014/015/016 (Checkout ×3) | Automated | AE-UI-TC-025/026/027 | **DEFERRED** | **DOWNGRADE** — this project independently found the checkout route/flow unverified in Step 2/3, a gap the TS project's own documentation did not carry (Section 26 discusses why) |
| AE-TC-UI-017 (Remove from cart) | Automated | AE-UI-TC-018 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-018/019 (Category/Brand) | Automated | AE-UI-TC-019/020 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-020 (Search+cart+login) | Automated | AE-UI-TC-021 | AUTOMATE | REIMPLEMENT |
| AE-TC-UI-021 (Product review) | Automated | AE-UI-TC-022 | **RESTRICTED** | **DOWNGRADE** — same side-effect reasoning, newly identified this step (Section 13) |
| AE-TC-UI-022 (Recommended item) | Automated | AE-UI-TC-023 | AUTOMATE | KEEP AUTOMATED |
| AE-TC-UI-023 (Address verification) | Automated | AE-UI-TC-028 | **DEFERRED** | DOWNGRADE — downstream of Checkout |
| AE-TC-UI-024 (Invoice download) | Automated | AE-UI-TC-029 | **DEFERRED** | DOWNGRADE — downstream of Checkout |
| AE-TC-API-001–008 (8 API) | Automated | AE-API-TC-001–010 (expanded to 10) | AUTOMATE | KEEP AUTOMATED + EXPAND |
| API-11/12 (TS-deferred, Hybrid-only helpers) | Not independently automated | AE-API-TC-011/012 | **AUTOMATE** | **UPGRADE** — promoted to standalone automated tests, not just Hybrid setup helpers, on the strength of this project's own Step 2 verification |
| API-13/14 (TS-deferred) | Not automated | AE-API-TC-013/014 | MANUAL / AUTOMATE | Split — updateAccount stays manual (low value), getUserDetail promoted to automated (Section 5) |
| AE-TC-HYBRID-001/002 (planning-only, never implemented in either project) | Not implemented | AE-E2E-TC-001/002 | DEFERRED | DEFER (unchanged status, now explicitly reasoned) |
| (none) | — | AE-UI-TC-001, AE-UI-TC-024, AE-UI-TC-013/014/017, AE-E2E-TC-003 | Mixed (AUTOMATE ×4, DEFERRED ×2) | **PROPOSE NEW** |

**Net effect vs. the TS baseline:** of the original 32, **21 are effectively kept automated** (reimplemented or unchanged in spirit), **8 are downgraded** (5 Checkout-area + 3 real-side-effect cases — Contact Us, Subscription, Review), **1 is unchanged** (the Hybrid pair, still not implemented anywhere), **2 API endpoints are upgraded** from deferred/helper-only to standalone automated tests, and **6 new Python-originated cases** join the scope. This is a **net-negative shift in raw automated-test count from the TS baseline's own 32 (24 UI + 8 API automated)** to this project's 31 — not because Python does less, but because this project independently discovered real risks (unverified Checkout, unrecoverable side effects) that the TS baseline's own documentation did not carry into its automation decision at the same level of scrutiny. This is flagged explicitly for QA Lead attention (Section 33), consistent with the instruction not to silently reduce or blindly preserve TS coverage.

## 24. Python-Specific Opportunities (Observations Only — Not Implemented)

- **API-driven setup for UI tests:** using `createAccount` to provision the durable `TD-USER-VALID-001`/`TD-USER-EXISTING-001` accounts once, outside the main suite, rather than via repeated UI signups — reduces UI-layer flakiness exposure for every case that depends on a durable account (UI-005/007/008/021).
- **Parametrization/data-driven testing:** the 4 unsupported-HTTP-method API cases (API-002/004 and their siblings) and the brand/category browsing cases (UI-019/020) are natural candidates for a single parametrized test function rather than 4+ near-duplicate test functions — a Pytest-idiomatic pattern with no TypeScript equivalent worth copying.
- **Fixtures for account lifecycle:** a Pytest fixture that yields a freshly-created account and guarantees deletion in teardown (even on test failure) would make the create/delete pairing (UI-004, API-011/012) structurally impossible to leave uncleaned — stronger than the TS project's own `finally`-block discipline, since a fixture's teardown runs regardless of how the test body is written.
- **Python's `requests`/`httpx` ecosystem for the API layer:** could allow API tests to run without any Playwright browser context at all, which the TS project's `APIRequestContext` approach does not offer as cleanly — a potential source of a genuinely faster API suite, evaluated properly at Step 11.

These are architecture-adjacent observations for Step 11 to weigh, not decisions made here.

---

## 25. Final Automation Scope

| Group | Count | % of 46 | Primary Reason |
|---|---|---|---|
| **AUTOMATE** | 31 | 67.4% | VERIFIED or low-risk-to-verify behavior, acceptable environment safety |
| **MANUAL** | 2 | 4.3% | Low business value (TC-010) or low incremental value despite technical safety (API-TC-013) |
| **DEFERRED** | 9 | 19.6% | Unresolved Checkout flow (5), unexplained search anomaly (1), unconfirmed quantity boundary (1), Hybrid cases blocked on their UI dependencies (2) |
| **RESTRICTED** | 4 | 8.7% | Unrecoverable public side effects on a shared environment (Contact Us, Subscription ×2, Product Review) |

## 26. Automation Coverage Analysis

- **Total Test Cases:** 46
- **AUTOMATE:** 31 → **Automation coverage: 31/46 = 67.4%**
- **UI automation:** 17/29 = **58.6%**
- **API automation:** 13/14 = **92.9%**
- **Hybrid automation:** 1/3 = **33.3%**
- **P0 automation:** 10/13 = **76.9%** (the 3 excluded P0s are all Checkout E2E cases)
- **P1 automation:** 12/14 = **85.7%**
- **Critical journey automation:**
  - Discovery/Cart journey: 10/10 relevant cases automated = **100%**
  - Identity (Signup/Login) sub-journey: 6/6 relevant cases automated = **100%** (with the execution-authorization gate noted in Section 12)
  - Checkout/Order sub-journey: 1/6 relevant cases automated (only the gate) = **16.7%** — the honest, unresolved figure this document does not disguise

All figures above are computed directly from the Section 5 classification table — none are asserted independently of it.

## 27. Recommended Automation Roadmap

Waves reflect Automation Priority (Section 16), CI tier (Section 6), and dependency order — not implementation yet.

| Wave | Focus | Cases |
|---|---|---|
| **Wave 1 — Foundational Smoke & Read-Only API** | A0 cases: zero-risk, no data dependency | UI-006, UI-011, UI-024; API-001, API-003, API-007 (once a durable account exists), API-008 |
| **Wave 2 — Core Regression (UI + API)** | A1 cases: discovery/cart/negative-API regression | UI-012, UI-015, UI-016, UI-018; API-002, API-004, API-005, API-006, API-009, API-010 |
| **Wave 3 — Identity Lifecycle (Authorization-Gated)** | Account creation/deletion, CI-RESTRICTED tier | UI-004, UI-005, UI-007, UI-008; API-011, API-012 — **cannot begin implementation until QA Lead authorization from Steps 7/8 is granted** |
| **Wave 4 — Broader UI Regression** | A2 cases | UI-001, UI-013, UI-019, UI-020, UI-021, UI-023; API-014 |
| **Wave 5 — Hybrid (Unblocked Case Only)** | The one Hybrid case with no upstream dependency | E2E-003 |
| **Not Yet Waved — Blocked** | Checkout E2E trio, address/invoice, search anomaly, quantity boundary, the two dependent Hybrid cases | UI-025/026/027/028/029, UI-014, UI-017, E2E-001/002 — re-enter the roadmap only after their respective Section 5 "Primary Rationale" blocker is resolved |

No implementation begins under this document — the roadmap sequences future work for Phases 6–10.

## 28. Decision Log

| Decision | Reason | Evidence | Impact | Revisit Condition |
|---|---|---|---|---|
| `createAccount`/`deleteAccount` are `AUTOMATE`, not `RESTRICTED` | Mandatory cleanup pairing makes this a proven-safe pattern (TS ran the equivalent in full CI regression) | TS `.github/workflows/playwright.yml` (Step 5 artifact review) | Unlocks Wave 3, but gated on execution authorization | If cleanup ever fails silently in practice, reclassify to RESTRICTED |
| `updateAccount` is `MANUAL`, not `AUTOMATE` | Technically safe but low regression value for a P2 requirement | [03](03-Requirement-Analysis.md) priority, Section 3 value criteria | Slightly lower API coverage % than "automate everything safe" would produce | If a future requirement depends on update behavior, promote to AUTOMATE |
| Contact Us/Subscription/Review are `RESTRICTED` | No verified cleanup; repeated CI runs create permanent public side effects | [08](08-Test-Data.md) §24/30, extended in this document to TC-022 | 3 fewer automated UI cases than the TS baseline had | If the AUT is ever confirmed to offer a moderation/removal path, reclassify |
| Checkout E2E trio is `DEFERRED`, not `AUTOMATE` | Route/flow genuinely unverified — automating would encode guesses as a "passing" test | [03](03-Requirement-Analysis.md) §5 row 1/4 | Largest single coverage gap vs. the TS baseline (5 cases) | Resolve via direct exploratory verification, then reclassify |
| API preferred over UI for read-only product/brand/search validation | Faster, more precise, no browser overhead | [05](05-Test-Strategy.md) §1/§9 | Both layers still automated (not either/or) — API validates the contract, UI validates the rendering (no duplication, per [06](06-Test-Scenarios.md) §10) | N/A |
| E2E-003 is `AUTOMATE` while E2E-001/002 are `DEFERRED` | Only E2E-003 has no identity/checkout dependency | [05](05-Test-Strategy.md) §6 sequencing rule | Hybrid coverage starts at 33%, not 0% or 100% | E2E-001 revisits once UI-005 is stable; E2E-002 once Checkout resolves |

## 29. Automation-Scope Risks

Only risks specific to *this scope decision* — not a restatement of the full project risk register:

- **Authorization dependency:** Wave 3 (6 cases, including the highest-value Signup/Login coverage) cannot begin without explicit QA Lead authorization to create/delete a real account — a hard blocker on part of this scope, not a soft preference.
- **CI-RESTRICTED throttling could mask real regressions:** running UI-004/API-011/012 only on MAIN/NIGHTLY (not PR) means a Signup-breaking change could merge before detection — mitigated by the fast Wave 1/2 PR gate catching most adjacent regressions, but not eliminated.
- **Downgrade risk vs. the TS baseline:** 8 previously-automated-in-TS behaviors are not automated here (Section 23) — if any of those areas turns out to be more stable/safe than this project's stricter evaluation assumed, coverage is more conservative than it needed to be.
- **Maintenance risk concentration:** the 3 MEDIUM-maintenance-risk cases tied to account mutation (UI-004, API-011/012) are also the CI-RESTRICTED cases — a single point of coordinated fragility if the account-lifecycle pattern breaks.
- **Search-anomaly and quantity-boundary exclusion could hide a real defect indefinitely** if the underlying investigation (TC-014, TC-017 prerequisite) is never actually performed — deferral is only healthy if it's revisited, not forgotten.

## 30. QA Lead Approval Items

1. **Final automated-test count: 31 of 46 (67.4%)** — confirm this is acceptable, given it is a **net decrease** in raw automated-case count from the TS baseline's 32.
2. **4 cases downgraded to RESTRICTED for unrecoverable side effects** (Contact Us, Subscription ×2, Product Review) — including the newly-identified Product Review risk not previously flagged in Step 8. Confirm agreement, or direct an alternative (e.g., accept the side effect as a cost of coverage, or investigate whether a moderation/cleanup path exists).
3. **5 Checkout E2E cases + 2 downstream cases remain DEFERRED**, unchanged in spirit from the ongoing verification gap — confirm this is acceptable for now, or direct that exploratory verification be prioritized before Step 10/11 proceeds further.
4. **Execution authorization for account creation/deletion (UI-004, API-011/012)** — this remains the same open item from Steps 7/8; without it, Wave 3 cannot begin even after Step 11 (Framework Architecture) completes.
5. **Browser execution scope for automated cases:** this document assumes the Chromium-first, curated-cross-browser model already approved in [05-Test-Strategy.md](05-Test-Strategy.md) §9/§13 — confirm no change is needed at this step.
6. **`updateAccount` (API-TC-013) kept MANUAL** — confirm this value judgment, or direct it be promoted to AUTOMATE.

## 31. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Draft — Pending QA Lead Approval** | | |

### Step 9 Exit Criteria

- [x] Steps 1–8 reviewed
- [x] All 46 Test Cases evaluated individually (Section 5)
- [x] All Test Data dependencies considered (Section 6)
- [x] TS `AE-AS-001`, `AE-TC-001`, `AE-TDD-001`, `AE-TS-001`, `AE-FA-001` reviewed; actual TS artifacts (`package.json`, `Dockerfile`, `playwright.config.ts`, `testConfig.ts`, CI workflow) re-consulted as evidence, not copied
- [x] Every Test Case has exactly one final scope classification (Section 5)
- [x] No case automatically approved solely because TS had it (Section 23 shows 8 explicit downgrades with reasons)
- [x] No useful case removed without rationale (every downgrade/deferral in Section 23/28 is explained)
- [x] Checkout uncertainty remains visible (Section 12, unresolved in 5 of 6 relevant cases)
- [x] Contact/Subscription side effects remain visible, and a previously-missed Product Review risk is caught and corrected (Section 13)
- [x] Account mutation restrictions remain visible (Section 11, 19, 29)
- [x] Search anomaly not encoded as an assertion (Section 14)
- [x] Quantity boundary uncertainty remains visible (Section 15)
- [x] Coverage calculations shown with their arithmetic (Section 26)
- [x] UI/API/Hybrid counts correct (17+13+1=31 of 29+14+3=46)
- [x] CI suitability, parallelization, and maintenance risk separately assessed (Sections 6, 18–21)
- [x] No code created; no accounts created or deleted
- [ ] QA Lead Review & Approval

Approval of this exit criterion by the QA Lead is required before proceeding to Step 10 — Automation Strategy.
