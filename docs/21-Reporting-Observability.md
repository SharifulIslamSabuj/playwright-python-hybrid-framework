# 21 — Reporting & Observability

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-REPORT-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 15 — Reporting & Observability |
| Step | Step 21 — Reporting & Observability |
| Predecessor Documents | [01](01-Project-Vision.md)–[20](20-Dockerization.md), all ✅ approved |

## 1. Objective

Close the two `pytest-html` reporting requirements identified as unmet during the Step 21 discovery audit — Test Case ID traceability and execution-platform/environment metadata — per [docs/10-Automation-Strategy.md §25](10-Automation-Strategy.md), without introducing a dashboard, trend system, external observability platform, or any other Phase 16/17 deliverable.

## 2. Existing Reporting Baseline (before this step)

Already implemented and unchanged by this step:
- `pytest-html` HTML report, self-contained, generated on every run (`--html=... --self-contained-html`, `pyproject.toml` `addopts`).
- Screenshot-on-failure, trace-on-retry (`--screenshot=only-on-failure`, `--tracing=retain-on-failure`).
- A generic `pytest-metadata` Environment table (Python version, platform, installed packages, base URL).
- Execution summary, per-test/per-suite duration, browser-per-result (via Playwright's `[chromium]`/`[firefox]`/`[webkit]` parametrize IDs), and test category (`ui`/`api`/`hybrid` markers) — all already satisfied `docs/10 §25` requirements, confirmed during the audit and not touched here.

## 3. Identified Gaps (confirmed by direct inspection during the audit, not assumed)

Grepped an actual, previously-generated `reports/html/report.html` for `AE-UI-TC`/`AE-API-TC`/`AE-E2E-TC` → **0 matches**. Grepped the Environment table content → generic runtime info only, no field identifying which platform/tier produced the run. These were the two concrete, unmet requirements from [docs/10 §25](10-Automation-Strategy.md):
1. *"Traceability: requirement/scenario/case ID visible in the report, not just a bare test name."*
2. *"Environment: which CI tier/trigger produced the result."*

## 4. Hook API Verification (per instruction — not assumed)

Read directly from the two installed packages' own source before writing any code:
- `.venv/Lib/site-packages/pytest_html/hooks.py` — confirmed the 4.2.0 hookspecs: `pytest_html_results_table_header(cells)`, `pytest_html_results_table_row(report, cells)`, among others.
- `.venv/Lib/site-packages/pytest_html/report_data.py` — confirmed the exact default 4-column header list (`Result, Test, Duration, Links`, indices 0–3), so the new column could be inserted at a specific, correct index (2) rather than guessed.
- `.venv/Lib/site-packages/pytest_html/basereport.py` — confirmed `cells` is a mutable list of raw `<th>`/`<td>` HTML strings, mutated in place by hook implementations.
- `.venv/Lib/site-packages/pytest_metadata/hooks.py` and `plugin.py` — confirmed the `pytest_metadata(metadata, config)` hook is the supported extension point for adding custom Environment-table entries, and that `pytest_metadata/ci/jenkins.py` already auto-surfaces raw Jenkins environment variables (`BUILD_NUMBER`, `JOB_NAME`, `JENKINS_URL`, `GIT_BRANCH`, etc.) with **no code needed from this project** — confirmed no equivalent built-in exists for GitHub Actions or Azure DevOps.
- GitHub Actions' and Azure DevOps' auto-injected environment variable names (`GITHUB_ACTIONS`, `GITHUB_WORKFLOW`, `GITHUB_EVENT_NAME`, `GITHUB_REF_NAME`, `GITHUB_RUN_ID`; `TF_BUILD`, `BUILD_BUILDID`, `BUILD_REASON`, `AGENT_NAME`, `BUILD_SOURCEBRANCH`) were verified against GitHub's own "Variables reference" documentation and Microsoft Learn's "Predefined variables" documentation respectively — not guessed.

## 5. Test Case ID Traceability Implementation

In `tests/conftest.py` (the only file this requirement touches):
- `pytest_runtest_makereport` (a `hookwrapper`) parses each test's **existing, unmodified** docstring with `re.compile(r"Test Case:\s*(AE-[\w-]*?TC-\d+)")`, matching the `Test Case: AE-*-TC-*` convention already established by [docs/11 §28](11-Framework-Architecture.md) — the same convention every business test already follows. The extracted ID (or an empty string if no match) is stored as `report.test_case_id`.
- `pytest_html_results_table_header` inserts a `<th>Test Case ID</th>` column at index 2 (immediately after "Test").
- `pytest_html_results_table_row` inserts the corresponding `<td>` at the same index, falling back to `"N/A"` when no ID was captured.

No test file was modified. No docstring was rewritten or duplicated — the hook only reads what already exists.

## 6. Execution Environment / Platform Metadata Implementation

Also in `tests/conftest.py`:
- `_detect_execution_platform()` checks, in priority order: `GITHUB_ACTIONS` env var (GitHub Actions) → `JENKINS_URL`/`BUILD_NUMBER` (Jenkins) → `TF_BUILD` (Azure DevOps) → `/.dockerenv` file existence (Docker, the standard in-container marker Docker itself creates) → `"Local"` as the fallback. A CI-platform signal takes priority over the Docker signal, since knowing *which CI tier/trigger* produced a run is the more specific, higher-value fact when a CI job also happens to execute inside a container.
- `pytest_metadata(metadata, config)` sets `metadata["Execution Platform"]` to the detected value, and — for GitHub Actions and Azure DevOps only, since Jenkins' equivalent raw fields are already surfaced automatically by `pytest-metadata`'s own built-in detection — adds a small set of verified, commonly useful fields (workflow/event/ref/run-id for GitHub Actions; build ID/reason/agent/branch for Azure DevOps) when those environment variables are actually present.

**No CI/CD file was modified to support this.** Every signal used is a variable each platform already injects into every job automatically — GitHub Actions, Jenkins, and Azure DevOps all do this natively, with no workflow/pipeline configuration required, and Docker's `/.dockerenv` marker is created by the Docker runtime itself, not by this project's `Dockerfile`. The "modify a CI file only if genuinely impossible without it, and stop and report first" condition in the approved scope was never triggered — no such necessity was found.

## 7. Validation Evidence (real execution, not assumed)

| Check | Command | Result |
|---|---|---|
| A. Collection | `python -m pytest --collect-only -q` | **`50 tests collected in 0.06s`** — unchanged |
| B. Full regression run | `python -m pytest -m "regression and not ci_restricted" -v --html=... --self-contained-html` | **`22 passed, 28 deselected in 84.43s`** — 0 failed, identical composition/behavior to the pre-existing baseline (Step 19/20 evidence) |
| C. Test Case ID visibility | Grep the generated report for `AE-[A-Za-z0-9]*-TC-[0-9]+` | **All 22 expected IDs present, each exactly once**, correctly aligned to their test (verified via the raw `resultsTableRow` JSON: e.g. `test_ae_api_tc_008...` → `<td class="col-testcaseid">AE-API-TC-008</td>`) |
| C (infra tests, graceful handling) | `python -m pytest tests/test_setup_validation.py tests/test_framework_foundation.py -v --html=...` | **`27 passed, 1 skipped`** (the 1 skip is the pre-existing, expected `durable_valid_account` unprovisioned-skip — not new). All 28 collected items rendered `N/A` in the Test Case ID column — **zero errors, zero crashes** |
| D. Environment metadata | Grep the generated report for `Execution Platform` | **`"Execution Platform": "Local"`** present in the Environment table for this local validation run |
| E. Regression safety | Compare against the Step 19/20 established baseline | Identical composition (22 selected / 28 deselected) and identical pass count (22/22) — no new failure occurred; nothing to classify |

## 8. Runtime Validation Scope — What Was and Was Not Executed This Step

Per instruction, runtime validation vs. implementation support are kept explicitly separate:

| Platform | Implementation support | Runtime-validated this step |
|---|---|---|
| Local | Full — Test Case ID column + `"Execution Platform": "Local"` | **Yes** — Section 7 |
| Docker | Full — `/.dockerenv` detection implemented | **Not re-executed this step.** (Docker's real report-generation behavior was already runtime-validated in Step 20's re-validation pass, before this feature existed; the detection logic itself was not re-run inside a container this step. Not claimed as validated here.) |
| GitHub Actions | Full — `GITHUB_ACTIONS` detection + workflow/event/ref/run-ID fields implemented, variable names verified against GitHub's own docs | **Not executed** — no GitHub Actions run occurred this step. Implementation support only. |
| Jenkins | Full — `JENKINS_URL`/`BUILD_NUMBER` detection implemented; raw fields come from `pytest-metadata`'s own built-in Jenkins support | **Not executed** — no Jenkins run occurred this step. Implementation support only. |
| Azure DevOps | Full — `TF_BUILD` detection + build ID/reason/agent/branch fields implemented, variable names verified against Microsoft Learn | **Not executed** — no Azure DevOps run occurred this step. Implementation support only. |

## 9. Limitations

- GitHub Actions, Jenkins, and Azure DevOps detection logic is implemented and its input variable names are verified against each platform's own current documentation, but has **not been exercised by an actual run on any of those three platforms** — none has ever been externally executed for this project ([docs/19-CI-CD.md §6a](19-CI-CD.md)), so this remains implementation support, not confirmed runtime behavior, until a real run occurs.
- The Test Case ID regex assumes the existing `Test Case: AE-*-TC-*` docstring convention continues to be followed by any future test; a test written without that exact phrase would render `N/A` (graceful, not an error, but also not traceable).
- No dashboard, trend graph, or cross-run comparison was built — deliberately out of scope (Section 11).

## 10. Risks

- Low. The changes are purely additive to `tests/conftest.py` (115 insertions, 0 deletions, confirmed via `git diff --stat`) and do not alter any fixture, test, or execution path. The main residual risk is the untested-live-on-CI status noted in Section 9, mitigated by the fact that a wrong/missing detection value degrades gracefully to `"Local"` or an absent optional field — it cannot cause a test failure or block a pipeline.

## 11. Future Observability Enhancements — Explicitly Out of Scope

Not built in this step, reserved for Phase 16–17 ("QA metrics and test summary reporting," [docs/01 §18](01-Project-Vision.md)) or later, per the QA Lead's explicit instruction:
- QA metrics dashboard or any persistent trend/history system.
- Allure or any other reporting-stack migration ([docs/10 §25](10-Automation-Strategy.md) already deferred this).
- Database-backed report storage or cross-run comparison.
- Any external observability platform (Grafana, Datadog, etc.).
- Automated failure classification (the five-way scheme remains a manual QA investigation process, per [docs/17](17-Execution-Report.md)/[18](18-Defect-Documentation.md)).

## 12. Files Changed

- `tests/conftest.py` — 115 insertions, 0 deletions (confirmed via `git diff --stat`), purely additive: 6 new module-level functions/hooks appended after the existing `created_account_cleanup` fixture, plus 2 new stdlib imports (`os`, `re`). No existing fixture, import, or line was modified or removed.
- `docs/21-Reporting-Observability.md` — this document.
- `docs/20-Dockerization.md` — one explicitly authorized label correction only (Section 13).

## 13. Documentation Correction (explicitly authorized this step)

`docs/20-Dockerization.md`'s Document Control table previously read `Phase 15 — Dockerization`. This was a genuine labeling error made during Step 20 (Phase 15 is, and always was, "Reporting & Observability" per [docs/01:60](01-Project-Vision.md); Docker has no dedicated phase number of its own in the roadmap — it lives in the unnumbered "Step 20+" bundle per [docs/11 §44](11-Framework-Architecture.md)). Per the QA Lead's explicit authorization this step, the single line was corrected to read `Step 20 — Dockerization` (Phase label removed for that row, since Docker has no dedicated phase number). No other content in `docs/20-Dockerization.md` was touched.

## 14. Files Explicitly Confirmed Untouched

Verified via `git diff --stat` (not just timestamps, now that the repository has a real commit history) — all of the following returned **zero diff**:
- `docs/01-Project-Vision.md` through `docs/19-CI-CD.md` (all 19).
- `.github/workflows/ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`.
- `pyproject.toml`.
- Every file under `src/`.
- Every file under `tests/` other than `conftest.py`.
- `Dockerfile`, `.dockerignore`, `.env.example` — unchanged (not part of this step's scope).
- TypeScript reference project — `git status --short` returned clean.

## 15. Project Governance — Preserved Unchanged

- 46 total Test Cases (22 executed / 9 blocked / 4 restricted / 9 deferred / 2 manual) — unchanged; 50 tests still collect.
- Five-way failure classification (Test / Application / Environment / Automation / Data) — unchanged, not exercised this step (no failure occurred).
- `OBS-001` — unchanged, not reclassified; no OBS-001-pattern failure occurred during this step's validation runs.
- Gate 5 = PARTIAL, Gate 6 = No Release Approval — unchanged.
- No release-readiness claim is made by this document.
- No blocked/deferred/restricted case was executed or reclassified.

## 16. Step 21 Exit Criteria

- [x] pytest-html 4.2.0 hook API verified against the installed package's own source before implementation (Section 4)
- [x] Test Case ID traceability implemented and validated (Section 5, 7)
- [x] Execution-platform metadata implemented and locally validated (Section 6, 7)
- [x] `python -m pytest`, existing markers, `addopts`, Chromium default, retry behavior, report paths, screenshot/trace behavior, and parallelism — all unchanged
- [x] No new dependency added (`pytest-html`/`pytest-metadata` already present)
- [x] `docs/01-19`, the three CI/CD files, `pyproject.toml`, `src/`, `.dockerignore`, `Dockerfile`, `.env.example` confirmed untouched via `git diff`
- [x] Only `tests/conftest.py` modified under `tests/`/`src/`
- [x] 50 tests still collect; 22/28 regression composition and 22/22 pass result unchanged
- [x] No new failure occurred; five-way classification and `OBS-001` preserved unchanged
- [x] `docs/20-Dockerization.md` corrected only as explicitly authorized (Section 13)
- [x] No dashboard, trend system, external observability platform, Allure migration, or database-backed reporting introduced
- [x] No release-readiness claim made
- [ ] QA Lead approval — required before Step 22

## 17. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 22.
