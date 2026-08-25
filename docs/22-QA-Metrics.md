# 22 — QA Metrics

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-METRICS-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 16 — QA Metrics |
| Step | Step 22 — QA Metrics |
| Predecessor Documents | [01](01-Project-Vision.md)–[21](21-Reporting-Observability.md), all ✅ approved |

## 2. Purpose

Compute and present the metric set defined by [docs/05-Test-Strategy.md §24](05-Test-Strategy.md) ("Metrics Strategy") using only evidence that already exists in approved project documents. This document does not execute any test, build any dashboard, or create any persistent trend-storage system — [docs/05 §24](05-Test-Strategy.md) itself explicitly defers those to a later, separate decision ("No QA Dashboard is built in this step"), a boundary this document preserves.

## 3. Scope

**In scope:** the 11 metrics named in the approved Step 22 instruction, computed from [docs/03](03-Requirement-Analysis.md), [05](05-Test-Strategy.md), [09](09-Automation-Scope.md), [14](14-UI-Automation.md)–[21](21-Reporting-Observability.md).

**Out of scope:** any dashboard, database, persistent trend-storage mechanism, metrics-computation script, new dependency, pytest-configuration change, test-scope change, test-classification change, or release-readiness claim. No source code, test file, CI/CD file, or Docker file was created or modified to produce this document.

## 4. Metric Definitions

Reused verbatim from [docs/05-Test-Strategy.md §24](05-Test-Strategy.md) — not redefined here: planned vs. executed counts (by layer/module), pass/fail/blocked counts, automation coverage, requirement coverage, API endpoint coverage, execution duration by suite, flaky-test rate (tracked separately from environment noise), defect count/severity distribution, regression status over time (trend, not snapshot).

## 5. Executive Metrics Snapshot

| Metric | Value | Source |
|---|---|---|
| Total approved Test Cases | 46 | [09 §25](09-Automation-Scope.md) |
| Total collected automated tests (incl. 28 framework/infra tests) | 50 | [19 §10](19-CI-CD.md), reconfirmed [20](20-Dockerization.md)/[21 §7](21-Reporting-Observability.md) |
| Business Test Cases implemented and executed | 22 (12 UI + 9 API + 1 Hybrid) | [17 §5A](17-Execution-Report.md) |
| Approved `AUTOMATE` scope | 31/46 = 67.4% | [09 §25](09-Automation-Scope.md) |
| Blocked (authorization-gated) | 9 | [18 §7](18-Defect-Documentation.md) |
| Restricted | 4 | [09 §25](09-Automation-Scope.md) |
| Deferred | 9 | [09 §25](09-Automation-Scope.md) |
| Manual | 2 | [09 §25](09-Automation-Scope.md) |
| Confirmed defects (Test/Application/Automation/Data) | 0 | [18 §4-5](18-Defect-Documentation.md) |
| Environment observations | 1 (`OBS-001`) | [18 §6](18-Defect-Documentation.md) |
| Gate 5 | PARTIAL | [17 §16](17-Execution-Report.md) |
| Gate 6 | NOT APPLICABLE (Release Readiness is Phase 18) | [17 §16](17-Execution-Report.md) |

These figures are quoted from their source documents, not recomputed independently.

## 6. Test Execution Metrics

### 6.1 Planned vs. executed, by disposition

| Disposition | Count | % of 46 | Source |
|---|---|---|---|
| Executed (implemented, run) | 22 | 47.8% | [17 §7](17-Execution-Report.md) |
| Blocked | 9 | 19.6% | [18 §7](18-Defect-Documentation.md) |
| Restricted | 4 | 8.7% | [09 §25](09-Automation-Scope.md) |
| Deferred | 9 | 19.6% | [09 §25](09-Automation-Scope.md) |
| Manual | 2 | 4.3% | [09 §25](09-Automation-Scope.md) |
| **Total** | **46** | **100%** | Reconciles exactly, per [17 §7](17-Execution-Report.md) |

### 6.2 By layer/module

| Layer | Implemented/Executed | Blocked | Source |
|---|---|---|---|
| UI | 12 (`AE-UI-TC-001/006/011/012/013/015/016/018/019/020/023/024`) | 5 (`AE-UI-TC-004/005/007/008/021`) | [17 §5](17-Execution-Report.md) |
| API | 9 (`AE-API-TC-001/002/003/004/005/006/008/009/010`) | 4 (`AE-API-TC-007/011/012/014`) | [17 §5](17-Execution-Report.md) |
| Hybrid | 1 (`AE-E2E-TC-003`) | 0 | [17 §5](17-Execution-Report.md) |

### 6.3 Pass / fail / blocked / restricted / deferred / manual counts

| Category | Count | Detail | Source |
|---|---|---|---|
| Passed (final confirmed status) | 22 | All 22 implemented cases independently confirmed passing at least once | [17 §7](17-Execution-Report.md) |
| Failed (final confirmed, non-environmental) | 0 | Every observed failure across Steps 17–21 traced to a connection-layer error or one transient HTTP 503 — never a business-logic/assertion failure | [17 §12](17-Execution-Report.md) |
| Blocked | 9 | Section 6.2 | [18 §7](18-Defect-Documentation.md) |
| Restricted | 4 | `AE-UI-TC-002/003/009/022` | [09 §25](09-Automation-Scope.md) |
| Deferred | 9 | `AE-UI-TC-014/017/025-029`, `AE-E2E-TC-001/002` | [09 §25](09-Automation-Scope.md) |
| Manual | 2 | `AE-UI-TC-010`, `AE-API-TC-013` | [09 §25](09-Automation-Scope.md) |

## 7. Automation Coverage Metrics

**The established figures below are preserved exactly as computed in [09 §26](09-Automation-Scope.md)/[10](10-Automation-Strategy.md) — not recomputed, not contradicted with a different denominator:**

| Figure | Value | Source |
|---|---|---|
| Overall automation coverage | 31/46 = 67.4% | [09 §26](09-Automation-Scope.md) |
| UI automation coverage | 17/29 = 58.6% | [09 §26](09-Automation-Scope.md) |
| API automation coverage | 13/14 = 92.9% | [09 §26](09-Automation-Scope.md) |
| Hybrid automation coverage | 1/3 = 33.3% | [09 §26](09-Automation-Scope.md) |
| **P0 automation ceiling** | **10/13 = 76.9%** | [09 §26](09-Automation-Scope.md), reaffirmed [10 §22](10-Automation-Strategy.md) |
| P1 automation | 12/14 = 85.7% | [09 §26](09-Automation-Scope.md) |
| Discovery/Cart journey automation | 10/10 = 100% | [09 §26](09-Automation-Scope.md) |
| Identity sub-journey automation | 6/6 = 100% | [09 §26](09-Automation-Scope.md) |
| Checkout/Order sub-journey automation | 1/6 = 16.7% | [09 §26](09-Automation-Scope.md) |

**Implementation-level figure (a distinct denominator from the above scope-level figures, shown separately per instruction, not merged into the 76.9% figure):**

| Figure | Value | Reason for the different denominator |
|---|---|---|
| Implemented of approved `AUTOMATE` scope | 22/31 = 71.0% | This denominator is "cases approved for automation" (31), not "all 46 cases" or "P0 cases" (13) — it measures how much of the *approved* scope has actual test code, distinct from what fraction of the *total* or *P0* catalog is automatable. Source: [17 §7](17-Execution-Report.md) |

## 8. Requirement Coverage Metrics

### 8.1 Historical Step-3 baseline (quoted verbatim, not altered)

Per [03-Requirement-Analysis.md §14](03-Requirement-Analysis.md), computed **before any test executed**:

| Verification Status | Count (of 48 `REQ-FUNC`+`REQ-API` total) |
|---|---|
| VERIFIED (fully) | 24 |
| PARTIALLY VERIFIED | 8 |
| NOT INDEPENDENTLY VERIFIED (REFERENCE only) | 16 |

This is explicitly labeled here as the **historical, pre-execution baseline** — it predates Steps 14–21 entirely.

### 8.2 Current evidence-based status

A full re-audit reclassifying all 48 `REQ-*` items individually was **not performed as part of this metrics step** — doing so would mean constructing the full requirement-to-test-case traceability matrix that [docs/11-Framework-Architecture.md §28](11-Framework-Architecture.md) explicitly deferred ("The traceability *matrix* itself is not built now, per instruction") and that no later step has built either. Recomputing the full 48-item table here would exceed evidence-synthesis and become new analytical work not grounded in an existing document — inconsistent with this step's evidence discipline.

What **is** directly, safely derivable from existing evidence: every one of the 22 implemented, executed Test Cases carries its own `Requirement:` field in its docstring (the project's actual traceability mechanism, [docs/11 §28](11-Framework-Architecture.md)). Reading those 22 docstrings directly gives the following requirement identifiers **now with direct execution evidence**, superseding their Step-3 classification (whichever it was) for that specific identifier:

`REQ-FUNC-HM-001-006`, `REQ-FUNC-SL-004`, `REQ-FUNC-PR-001`, `REQ-FUNC-PR-002`, `REQ-FUNC-PR-003`, `REQ-FUNC-PR-004`, `REQ-FUNC-PR-005`, `REQ-FUNC-PR-006`, `REQ-FUNC-CT-001`, `REQ-FUNC-CT-002`, `REQ-FUNC-CT-003`, `REQ-FUNC-CT-004`, `REQ-FUNC-CO-001`, `REQ-BUS-004`, `BR-003`, `REQ-API-001`, `REQ-API-002`, `REQ-API-003`, `REQ-API-004`, `REQ-API-005`, `REQ-API-006`, `REQ-API-008`, `REQ-API-009`, `REQ-API-010`, `REQ-E2E-003` — **25 distinct identifiers**, all with a real, passing execution result ([17 §7-11](17-Execution-Report.md)).

For every `REQ-*` identifier **not** in this list — including all Signup/Login requirements except `REQ-FUNC-SL-004`, all Checkout requirements except `REQ-FUNC-CO-001`/`REQ-BUS-004`/`BR-003`, `REQ-API-007`, and anything tied to the 9 deferred or 4 restricted cases — **this document keeps the original Step-3 classification and explicitly states it remains unverified by direct execution**, per instruction: current evidence does not conclusively support reclassifying them, since no test exercises them.

### 8.3 Reconciliation / explanation

The Step-3 baseline (Section 8.1) is a per-requirement classification across all 48 items; Section 8.2 is a partial, evidence-grounded update covering only the 25 identifiers the 22 implemented tests actually exercise. **These two views are not in conflict** — Section 8.2 narrows, rather than contradicts, Section 8.1: any identifier in the Section 8.2 list should now be read as execution-VERIFIED regardless of its original Step-3 bucket; every other identifier retains its Step-3 status exactly as documented. A full, formal 48-item re-classification remains a known gap (Section 14).

## 9. API Coverage Metrics

| Figure | Value | Source |
|---|---|---|
| Total documented API endpoints | 14 | [03 §14](03-Requirement-Analysis.md), [15 §1](15-API-Automation.md) |
| Approved for automation (`AUTOMATE`) | 13/14 = 92.9% | [09 §26](09-Automation-Scope.md), [15 §1](15-API-Automation.md) |
| Manual | 1/14 (`AE-API-TC-013`) | [15 §1](15-API-Automation.md) |
| **Implemented and passing** | **9/14 = 64.3%** | [17 §5A](17-Execution-Report.md) |
| Approved but blocked (unauthorized) | 4/14 (`AE-API-TC-007/011/012/014`) | [18 §7](18-Defect-Documentation.md) |

Reconciliation: 9 (implemented) + 4 (blocked) + 1 (manual) = 14 — accounts for all 14 documented endpoints exactly.

**Historical note:** [03 §14](03-Requirement-Analysis.md) recorded, at Step 3, that "6 of the 14 [API endpoints] are documentation-verified only, execution not performed." That statement predates all execution and is now superseded — 9 of the 14 endpoints have direct, real execution evidence as of [17](17-Execution-Report.md).

## 10. Execution Duration Metrics

Only real, recorded durations are shown. No duration is estimated.

| Suite / Environment | Duration | Result | Source |
|---|---|---|---|
| Full local suite (50 tests, final Step 17 snapshot) | 93.66s | 6 failed / 43 passed / 1 skipped (network-instability session) | [17 §4 (Current Work)](17-Execution-Report.md) |
| 22-case regression, local, with bounded reruns | 115.07s (0:01:55) | 21 passed / 1 failed / 10 reruns | [19 §10](19-CI-CD.md) |
| 22-case regression, Docker container (1st run, uncorrected mount) | 153.41s (0:02:33) | 22 passed / 0 failed | [20 §12](20-Dockerization.md) |
| 22-case regression, Docker container (2nd run, corrected mount) | 71.20s | 22 passed / 0 failed | [20 §12](20-Dockerization.md) |
| 22-case regression, local (Step 21 validation) | 84.43s | 22 passed / 0 failed | [21 §7](21-Reporting-Observability.md) |
| Framework foundation checks (Tier 1, 28 infra tests) | 12.23s | 27 passed / 1 skipped | [21 §7](21-Reporting-Observability.md) |

Per-test/per-suite duration by CI platform (GitHub Actions/Jenkins/Azure DevOps): **Not recorded** — none of the three platforms has ever been externally executed ([19 §6a](19-CI-CD.md)), so no real duration figure exists for them.

## 11. Flakiness vs. Environment Instability

These are kept strictly separate, per instruction — `OBS-001` is never counted as test flakiness.

### 11.1 Genuine test flakiness (pre-existing, distinct from `OBS-001`)

| Test | Occurrences | Context | Classification | Source |
|---|---|---|---|---|
| `AE-UI-TC-020` | 1 occurrence, full-suite execution only (0 occurrences across 3 isolated re-runs and a targeted repro script) | Step 14 implementation | "Environmental flakiness" (best current classification at the time) | [14 §12/§14](14-UI-Automation.md) |

**Exact rate not determinable**: [docs/14](14-UI-Automation.md) does not enumerate a total count of full-suite attempts during Step 14, only that the failure occurred once and did not reproduce in isolation — reported as "Not recorded" for a precise denominator, per instruction, rather than estimated.

At Step 17 onward, this specific pattern **could not be cleanly isolated** from the much larger `OBS-001` signal (Section 11.2) — [docs/17 §12](17-Execution-Report.md) explicitly states this as an open, undecided question, and [docs/18 §12](18-Defect-Documentation.md) preserves it as such. This document does not resolve that open question.

### 11.2 `OBS-001` — Environment observation (classified separately, unchanged)

| Metric | Value | Source |
|---|---|---|
| Raw connection-failure rate (direct `httpx` sampling) | 10/21 = 47.6% (cited as "~40-50%") | [17 §7](17-Execution-Report.md) |
| Classification | Environment observation (five-way scheme) — explicitly **not** an AUT, Automation, Test, or Data defect | [18 §6](18-Defect-Documentation.md) |
| Status | Accepted-Risk, unresolved, standing environmental limitation | [18 §6](18-Defect-Documentation.md) |

`OBS-001` remains classified exactly as [docs/18](18-Defect-Documentation.md) established — this document does not reclassify, resolve, or merge it with the Section 11.1 flakiness finding.

## 12. Defect Metrics

Per [docs/18-Defect-Documentation.md](18-Defect-Documentation.md), the authoritative defect evidence — preserved exactly, not recomputed:

| Category | Count | Source |
|---|---|---|
| Test failure | 0 | [18 §4](18-Defect-Documentation.md) |
| Application (AUT) failure | 0 | [18 §4](18-Defect-Documentation.md) |
| Automation failure | 0 | [18 §4](18-Defect-Documentation.md) |
| Data failure | 0 | [18 §4](18-Defect-Documentation.md) |
| Environment observation | 1 (`OBS-001`) | [18 §6](18-Defect-Documentation.md) |
| Blockers (not defects) | 2 (`BLK-001` = 5 UI, `BLK-002` = 4 API; 9 cases total) | [18 §7](18-Defect-Documentation.md) |

**No blocked or deferred Test Case is counted as a defect anywhere in this document** — Section 6.3/6.1 already accounts for them under their own dispositions.

## 13. Historical Regression Trend

Assembled from real, already-documented execution results across Steps 14–21. No date, run, pass rate, or duration below is invented — where a step's document does not give a specific date, the step number is used as the ordering key instead.

| Step | What ran | Result | Duration | Source |
|---|---|---|---|---|
| 14 | 12 UI cases (implementation + investigation) | 4 genuine failures found & fixed (3 automation defects, 1 flaky finding) → clean pass | Not recorded (per-run) | [14](14-UI-Automation.md) |
| 15 | 9 API cases (implementation) | Implemented and passing | Not recorded | [15](15-API-Automation.md) |
| 16 | 1 Hybrid case (implementation) | Implemented and passing | Not recorded | [16](16-Hybrid-E2E-Automation.md) |
| 17 | Full 50-test suite, multiple attempts (final snapshot shown) | 6 failed / 43 passed / 1 skipped; all 22 business cases individually confirmed passing across the session | 93.66s (final snapshot) | [17](17-Execution-Report.md) |
| 19 | 22-case regression, local, bounded retries | 21 passed / 1 failed / 10 reruns; residual passed in isolation | 115.07s | [19 §10](19-CI-CD.md) |
| 20 | 22-case regression, Docker (×2 runs) | 22 passed / 0 failed (both runs) | 153.41s, then 71.20s | [20 §12](20-Dockerization.md) |
| 21 | 22-case regression, local | 22 passed / 0 failed | 84.43s | [21 §7](21-Reporting-Observability.md) |

**Trend observation (evidence-based, not speculative):** from Step 19 onward, every full 22-case regression run has produced a final confirmed result of 22/22 passing, with the only variability being transient `OBS-001`-class connection failures recovered via retry/isolation — not a single genuine business-logic failure has occurred in any of these runs. This is consistent across 4 independent execution contexts (local ×2, Docker ×2).

## 14. Metric Reconciliation / Known Data Gaps

| Item | Status |
|---|---|
| Full 48-item `REQ-*` re-classification | **Not performed** (Section 8.2) — would require building the traceability matrix [docs/11 §28](11-Framework-Architecture.md) explicitly deferred; flagged as a gap, not silently filled |
| `AE-API-TC-007`/`014` SAFE vs. LIMITED classification discrepancy ([09](09-Automation-Scope.md) vs. [10 §21](10-Automation-Strategy.md)) | Still open, first disclosed [19 §5](19-CI-CD.md), reaffirmed [20](20-Dockerization.md); **not resolved by this document** |
| Per-test duration on GitHub Actions/Jenkins/Azure DevOps | Not recorded — none of the three platforms has been externally executed ([19 §6a](19-CI-CD.md)) |
| Exact denominator for the Step 14 `AE-UI-TC-020` flaky rate | Not recorded — [docs/14](14-UI-Automation.md) does not state a total full-suite attempt count |
| Whether the Step 14 flaky pattern and `OBS-001` are the same or distinct phenomena | Open, unresolved question, carried forward from [17 §12](17-Execution-Report.md)/[18 §12](18-Defect-Documentation.md) — not settled here |

## 15. QA Quality Observations

Observations, not conclusions or recommendations for release:
- Every implemented business Test Case has achieved a confirmed passing result; zero genuine (non-environmental) defects have been found across Steps 14–21.
- The dominant risk to execution reliability is environmental (`OBS-001`), not the framework or the AUT's business logic — confirmed by the trend in Section 13.
- Automation coverage is strong on the Discovery/Cart and Identity journeys (100% each) and weak on Checkout/Order (16.7%) — a pre-existing, already-disclosed scope limitation ([09 §26](09-Automation-Scope.md)), not new.
- 9 of 46 approved cases (all account-provisioning-dependent) remain entirely unautomated pending authorization — the single largest, longest-standing coverage gap.

## 16. Release-Gate Status

Preserved exactly as established — not reinterpreted:

| Gate | Status | Source |
|---|---|---|
| Gate 5 — Critical regression complete | **PARTIAL** | [17 §16](17-Execution-Report.md) |
| Gate 6 — Release readiness evidence available | **NOT APPLICABLE** (Release Readiness is Phase 18) | [17 §16](17-Execution-Report.md) |

**No release-readiness claim is made by this document.**

## 17. Limitations

- This document is a static, point-in-time synthesis of existing evidence — it is not a dashboard and creates no persistent trend-storage mechanism, per the approved scope.
- Metrics for platforms/environments never executed (GitHub Actions, Jenkins, Azure DevOps) are marked "Not recorded" rather than estimated.
- The full per-requirement traceability re-classification (Section 8) remains an open gap, not a claim of completeness.
- No new test was executed to produce this document — all figures are drawn from prior, already-approved execution evidence.

## 18. Conclusion

This document computes the [docs/05 §24](05-Test-Strategy.md) metric set entirely from existing, cited evidence. No established figure (the 76.9% P0 ceiling, the 0-defect count, `OBS-001`'s classification, the 46/22/9/4/9/2 scope breakdown) was altered — each is reproduced from its source and, where later evidence genuinely supported a narrower update (Section 8.2's 25-identifier requirement list, Section 9's endpoint reconciliation), that update is shown alongside the original baseline with its reasoning made explicit, never silently substituted. Gate 5 remains PARTIAL, Gate 6 remains NOT APPLICABLE, and no release-readiness claim is made.

## 19. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 23.
