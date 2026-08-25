# 19 — CI/CD

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-CICD-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 14 — CI/CD Implementation |
| Step | Step 19 — CI/CD |
| Predecessor Documents | [01](01-Project-Vision.md)–[18](18-Defect-Documentation.md), all ✅ approved |

## 1. Objective

Implement the CI/CD foundation already designed (not invented) in [05-Test-Strategy.md](05-Test-Strategy.md), [10-Automation-Strategy.md §18-22](10-Automation-Strategy.md), [11-Framework-Architecture.md §27/§29-31](11-Framework-Architecture.md), and [12-Project-Setup.md](12-Project-Setup.md), so the 22 currently implemented, approved automated Test Cases run reproducibly in CI with appropriate tiering, diagnostics, reporting, failure handling, and environment controls. This is the first step in which a GitHub Actions workflow file is created — every prior document explicitly deferred it ([10 §19](10-Automation-Strategy.md): "No GitHub Actions... workflow file exists yet"; [11 §31](11-Framework-Architecture.md): "No YAML file exists").

**Step 19 scope was subsequently confirmed by the QA Lead to be explicitly three CI/CD platforms** — GitHub Actions, Jenkins, and Azure DevOps — all orchestrating the identical, unforked Python + Playwright + Pytest framework and the identical 22-case approved suite. Sections 6-9 below cover GitHub Actions (implemented first); Sections 6a-6c cover Jenkins and Azure DevOps, added to complete the three-platform scope without redesigning or modifying the already-approved GitHub Actions workflow (verified unchanged in Section 10).

## 2. Source Documents Used

Read in the order specified by the QA Lead: [18](18-Defect-Documentation.md) → [17](17-Execution-Report.md) → [16](16-Hybrid-E2E-Automation.md) → [15](15-API-Automation.md) → [14](14-UI-Automation.md) → [13](13-Core-Framework-Development.md) → [11](11-Framework-Architecture.md) → [10](10-Automation-Strategy.md) → [09](09-Automation-Scope.md) → [04](04-Test-Plan.md) → [05](05-Test-Strategy.md). Plus direct inspection of the actual current project artifacts: `pyproject.toml`, `.gitignore`, `.env.example`, `src/config/settings.py`, `tests/conftest.py`, all 8 test files, and the `reports/` directory structure. The TypeScript reference project was not re-inspected directly this step — its precedent is already fully absorbed into [10](10-Automation-Strategy.md)/[11](11-Framework-Architecture.md), which this step implements rather than re-deriving.

## 3. Pre-Implementation State (as actually found)

| Item | Finding |
|---|---|
| `.github/workflows/` | Did not exist |
| Dockerfile | Did not exist anywhere in the project |
| `pyproject.toml` markers | 8 markers registered (`smoke, ui, api, hybrid, negative, regression, ci_restricted, cross_browser`), matching [11 §27](11-Framework-Architecture.md) exactly |
| Marker application on the 22 implemented tests | **Only `smoke` (1 test) and layer markers (`ui`/`api`/`hybrid`) and `negative` were actually applied.** `regression`, `ci_restricted`, and `cross_browser` were registered but applied to **zero** tests — see Section 4 |
| `pytest-rerunfailures`, `pytest-xdist` | Installed as dependencies, but not wired into `addopts` or any CI mechanism (correct — [10 §16](10-Automation-Strategy.md): CI-only, not a local default) |
| `WORKERS`/`RETRIES` env vars | Defined in `.env.example`/`settings.py` but not consumed by any pytest hook — inert placeholders, mechanism genuinely left "TBD at Step 12" per [11 §29/§30](11-Framework-Architecture.md), never actually wired |
| Dependency installation mechanism | No `[build-system]` table in `pyproject.toml` — the project is not set up as an installable package; local execution installs the pinned `[project.dependencies]` directly into a venv |

## 4. Implementation Gap Found and Closed (not a docs contradiction)

[11-Framework-Architecture.md §27](11-Framework-Architecture.md) states markers should have been "correctly applied at Step 12/13 implementation," and [§457](11-Framework-Architecture.md) explicitly names a missed marker as a real risk to the whole tiered-CI design. In practice, only 1 of the 22 implemented tests carried its full intended marker set. This is **not a contradiction between approved documents** — [10](10-Automation-Strategy.md) and [11](11-Framework-Architecture.md) agree exactly on what the markers should be — it is a gap between the design and the actual `tests/` code, discovered while inspecting the current project state per instruction.

Since CI tier selection is impossible without these markers (`smoke`/`regression`/`cross_browser`/`ci_restricted` drive every job's test selection in Section 6), completing this marker application was necessary to implement the already-approved design, not an expansion of it. **22 `@pytest.mark.regression` additions, 6 `@pytest.mark.smoke` additions, and 4 `@pytest.mark.cross_browser` additions were made across the 8 existing test files** — purely additive decorator changes, zero modification to any test's logic, locators, or assertions. Verified via local execution (Section 9): all 22 tests remain functionally identical.

| Marker | Cases (design, [10 §18/§23](10-Automation-Strategy.md), [11 §27](11-Framework-Architecture.md)) | Implemented subset now marked |
|---|---|---|
| `smoke` | UI-001/006/011/024, API-001/003/007/008 (8 cases) | UI-001/006/011/024, API-001/003/008 (7 of 8 — API-007 is blocked, unimplemented) |
| `cross_browser` | UI-006/015/018/024 (4 cases, [10 §17](10-Automation-Strategy.md)) | All 4 — all implemented |
| `ci_restricted` | UI-004, API-011/012 (3 cases, [11 §27](11-Framework-Architecture.md)) | **None** — all 3 are blocked, unimplemented (correct: this marker legitimately applies to zero currently-runnable tests) |
| `regression` | Full 31-case approved set ([11 §27](11-Framework-Architecture.md)) | All 22 implemented cases |

## 5. Minor Discrepancy Noted (disclosed, not resolved here)

While cross-referencing [09-Automation-Scope.md §19](09-Automation-Scope.md) against [10-Automation-Strategy.md §21](10-Automation-Strategy.md), a small inconsistency was found: [09](09-Automation-Scope.md) classifies `AE-API-TC-007` and `AE-API-TC-014` as parallelization-SAFE, while [10 §21](10-Automation-Strategy.md) classifies both as LIMITED. Both cases are among the 9 currently blocked, unimplemented cases ([18-Defect-Documentation.md §7](18-Defect-Documentation.md), `BLK-002`), so this discrepancy has **zero effect on the current CI implementation** — no implemented test's execution is affected either way. Per instruction, this is disclosed rather than silently resolved; no edit was made to [09](09-Automation-Scope.md) or [10](10-Automation-Strategy.md). It should be revisited whenever `AE-API-TC-007`/`014` are eventually implemented, once the account-provisioning blocker (`BLK-001`/`BLK-002`) is resolved.

## 6. CI/CD Workflow Design

One file, `.github/workflows/ci.yml`, three jobs, matching [10-Automation-Strategy.md §22](10-Automation-Strategy.md)'s four regression tiers (PR and Main share one job, since their approved composition is identical):

| Job | Trigger | Test Selection | Browser(s) | Composition Today |
|---|---|---|---|---|
| `pr_main_regression` | `pull_request` (into `main`), `push` to `main` | `-m "regression and not ci_restricted"` | Chromium | Exactly the 22 implemented cases (0 currently carry `ci_restricted`) |
| `nightly_regression` | `schedule` (daily, `02:00 UTC` — exact time not specified anywhere in [01](01-Project-Vision.md)–[18](18-Defect-Documentation.md); chosen as a reasonable Step 19 implementation default) | `-m regression` (no exclusion) | Chromium | Identical 22 today — see Section 7 for why this is still correct |
| `release_validation` | `workflow_dispatch` (manual — see Section 8) | Chromium leg: `-m regression`. Firefox/WebKit legs: `-m cross_browser` | Chromium + Firefox + WebKit (matrix) | Full 22-case Chromium regression + the 4-case curated subset on Firefox/WebKit |

Every job begins with a **Tier 1** step (`tests/test_setup_validation.py tests/test_framework_foundation.py`, run by path, not marker — these are framework-health checks, not `AUTOMATE` business cases, and intentionally carry no business-tier marker), exactly mirroring [17-Execution-Report.md §6](17-Execution-Report.md)'s own tier separation.

**No placeholder or skip entry exists for any of the 9 blocked cases** — they have no test code, so they simply cannot and do not appear in any job's collected test list (verified in Section 9).

## 6a. Platform Status Summary

The project has **not** been pushed to any Git remote (no GitHub repository, no Jenkins controller, no Azure DevOps organization/project exists for it). Accordingly, none of the three platforms has ever been externally executed — every result in this document is local, static, or structural validation only. No repository URL, Jenkins credential/controller/agent, Azure DevOps organization/project/service connection, pipeline ID, or webhook configuration is invented anywhere in this document or in the three CI/CD files.

| Platform | File | Implemented Locally | Locally Validated | Ready for External Execution | Externally Executed |
|---|---|---|---|---|---|
| GitHub Actions | `.github/workflows/ci.yml` | Yes | Yes (Section 10) | Yes — requires pushing this repository to GitHub and (optionally) configuring the `DURABLE_*` repository secrets once account provisioning is ever authorized | **NO** |
| Jenkins | `Jenkinsfile` | Yes | Yes, structurally (Section 6c/10) | Yes — requires a Jenkins controller with a Multibranch Pipeline or Pipeline job pointed at this repository, and an agent with Python 3.11+ | **NO** |
| Azure DevOps | `azure-pipelines.yml` | Yes | Yes (Section 10) | Yes — requires an Azure DevOps organization/project with this repository connected as a pipeline | **NO** |

## 6b. Jenkins — Design

`Jenkinsfile` (repository root) is a declarative pipeline implementing the same tiering/retry/artifact strategy as `.github/workflows/ci.yml`, adapted to Jenkins' idioms:

| Aspect | Implementation | Matches GitHub Actions via |
|---|---|---|
| Stages | Checkout → Verify Python Runtime → Install Dependencies → Install Playwright Browsers → Framework Foundation Checks (Tier 1, gated by a boolean parameter) → Run Approved Automated Regression Suite | Same stage sequence as each `ci.yml` job |
| Test selection | `MARKER_EXPRESSION` string parameter, default `'regression and not ci_restricted'` — identical default to the GitHub Actions PR/Main job | Same pytest marker mechanism (Section 4); can only filter the existing 50-test collection, never expand it |
| Browser | `BROWSER` choice parameter (`chromium`/`firefox`/`webkit`), default `chromium` | Matches [10 §17](10-Automation-Strategy.md) |
| Dependency install | Same `tomllib`-based extraction from `pyproject.toml` as `ci.yml`, via `pip install --user` (Jenkins agents are commonly long-lived/shared, unlike GitHub's ephemeral hosted runners — `--user` avoids polluting a shared agent's global Python, a deliberate, disclosed platform-specific adaptation) | Single source of truth preserved |
| Retries | `--reruns 2 --reruns-delay 3` | Identical values to `ci.yml` (Section 9's `{ci: 2, local: 0}` precedent) |
| Parallelism | None (no `-n`/xdist flag) | Same durable conservative stance as `ci.yml` (Section 9) |
| Artifact handling | `archiveArtifacts` for `reports/html/**`, `reports/screenshots/**`, `reports/traces/**` (`allowEmptyArchive: true`) in a `post { always { ... } }` block, so evidence survives a failed build | Same evidence set as `ci.yml`'s `upload-artifact` step |
| Optional HTML report view | `publishHTML` (HTML Publisher Plugin), wrapped in `try/catch` — **not assumed installed on any concrete Jenkins instance**; its absence never fails the build, since `archiveArtifacts` is the load-bearing evidence mechanism either way | N/A — this is a Jenkins-specific convenience with no GitHub Actions equivalent needed |
| Failure propagation | Native: a non-zero pytest exit fails the `sh` step → fails the stage → fails the build. No custom exit-code handling, no swallowed (`returnStatus`) failures anywhere in the file | Same principle as `ci.yml`'s default `run:` step behavior |
| Cleanup | `deleteDir()` in `post { cleanup { ... } }` — a Jenkins core step, no plugin dependency | Conceptually parallel to a hosted runner's automatic teardown |
| Secrets | **No `credentials()` binding is used.** Referencing a Jenkins credential ID that does not exist in any configured credential store would be inventing Jenkins infrastructure, which the QA Lead's instruction explicitly forbids. `AUT_BASE_URL`/`API_BASE_URL` are plain (non-secret) environment values only | Deliberately less than `ci.yml`'s `${{ secrets.* }}` wiring — disclosed as a platform difference, not an oversight (Section 6c) |
| Agent | `agent any` — no specific label, controller, or pre-provisioned agent is assumed to exist | N/A |

## 6c. Azure DevOps — Design

`azure-pipelines.yml` (repository root) implements the same strategy as a YAML pipeline:

| Aspect | Implementation | Matches GitHub Actions / Jenkins via |
|---|---|---|
| Trigger | `trigger: branches: include: [main]` (CI trigger), `pr: branches: include: [main]` (PR trigger), `docs/*`/`*.md` path-excluded so documentation-only commits don't trigger a run | Same branch scope as `ci.yml`'s `pull_request`/`push` triggers |
| Agent pool | `pool: vmImage: 'ubuntu-latest'` — a Microsoft-hosted agent; no self-hosted pool, organization, project, or service connection referenced | Matches `ci.yml`'s `runs-on: ubuntu-latest` |
| Test selection | `markerExpression` pipeline parameter, default `'regression and not ci_restricted'` — identical default to GitHub Actions and Jenkins | Same pytest marker mechanism (Section 4) |
| Browser | `browser` parameter (`chromium`/`firefox`/`webkit`), default `chromium` | Matches [10 §17](10-Automation-Strategy.md) |
| Foundation checks | Conditionally included via a `${{ if eq(parameters.runFoundationChecks, true) }}:` template expression, matching Jenkins' `RUN_FOUNDATION_CHECKS` boolean parameter | Same Tier 1 step as the other two platforms |
| Dependency install | Same `tomllib`-based extraction from `pyproject.toml` | Single source of truth preserved across all three files |
| Retries | `--reruns 2 --reruns-delay 3` | Identical values across all three platforms |
| Parallelism | None | Same durable conservative stance |
| Artifact handling | `PublishBuildArtifacts@1` publishing the whole `reports` directory, `condition: always()` so it runs even after the pytest step fails | Same evidence set as `ci.yml`/`Jenkinsfile` |
| Failure propagation | Native: a non-zero exit from a `script:` step fails the job by default (`continueOnError` is not set anywhere) | Same principle as the other two platforms |
| Cleanup | An explicit `rm -rf reports/html/* reports/screenshots/* reports/traces/*` step, `condition: always()` — disclosed as non-functionally-necessary on an ephemeral Microsoft-hosted agent (which is torn down regardless), kept for parity with the Jenkinsfile's explicit cleanup stage and to satisfy the requested "Cleanup" stage explicitly | Parallels Jenkins' `deleteDir()` |
| Secrets | **No variable group or secret variable is referenced.** Wiring one would require an Azure DevOps Library/variable group that does not exist in any configured organization, which the QA Lead's instruction explicitly forbids inventing. `AUT_BASE_URL`/`API_BASE_URL` are plain pipeline variables only | Same disclosed platform difference as Jenkins (Section 6b) |

## 7. Why the Nightly Job Currently Duplicates the PR/Main Job

[10-Automation-Strategy.md §22](10-Automation-Strategy.md) defines Nightly as "Full 31-case set including the CI-RESTRICTED pair... environment-instability canary value **independent of code changes**." Since 0 of the 3 CI-RESTRICTED cases are implemented, `-m regression` and `-m "regression and not ci_restricted"` currently select the identical 22 tests. This is disclosed explicitly rather than hidden: the Nightly job's present value is exactly the canary purpose the design already names (an unattended daily run that will surface AUT/environment issues like [OBS-001](18-Defect-Documentation.md) independent of any pull request), not broader test coverage. The moment the 3 CI-RESTRICTED cases are implemented and marked, `nightly_regression` picks them up automatically — no workflow change will be required.

## 8. Docker — Explicitly Deferred, Not Implemented

Per [11-Framework-Architecture.md §44](11-Framework-Architecture.md): `Step 20+ | Docker implementation...`. Docker is **not** assigned to Step 19. No Dockerfile was created. CI in this step runs directly on GitHub-hosted `ubuntu-latest` runners with Python installed via `actions/setup-python`, independent of Docker — this is a valid, common intermediate state and does not block CI from functioning; Docker (Step 20+) will later provide local/CI parity on top of this already-working pipeline, per [10-Automation-Strategy.md §20](10-Automation-Strategy.md)'s own framing of Docker as an *additional* reproducibility layer, not a CI prerequisite.

**Release trigger note:** no git-tag or release-branch convention has ever been approved in [01](01-Project-Vision.md)–[18](18-Defect-Documentation.md), so the Release tier uses a manual `workflow_dispatch` trigger rather than inventing an automatic release process the project never defined.

## 9. Implementation Details

- **Dependency installation:** `pyproject.toml` has no `[build-system]` table (confirmed by inspection, Section 3) — the project is not packaged/installable. Rather than duplicating the pinned dependency list into the YAML (a drift risk) or adding packaging metadata not requested by any approved document, dependencies are installed directly from `[project.dependencies]` using Python's standard-library `tomllib` (available since Python 3.11, matching `requires-python`) as a one-line extraction, keeping `pyproject.toml` the single source of truth. Verified locally (Section 10) to extract the exact 8 pinned packages correctly.
- **Python version:** `3.14`, matching the local development environment ([17-Execution-Report.md §3](17-Execution-Report.md): Python 3.14.4).
- **Browser installation:** `python -m playwright install --with-deps <browser>` — Chromium only for PR/Main/Nightly; matrix-selected engine for the Release job, per [10 §17](10-Automation-Strategy.md).
- **Invocation form:** `python -m pytest`, not bare `pytest` — this matters: the project's absolute imports (`from src.pages...`) resolve because `python -m` inserts the current working directory onto `sys.path`; this is the exact invocation form already proven locally throughout [17-Execution-Report.md](17-Execution-Report.md), preserved here rather than risking an import break with a different invocation style.
- **Parallelism:** No `-n`/`pytest-xdist` flag is used anywhere. [10 §21](10-Automation-Strategy.md) and [11 §29](11-Framework-Architecture.md) both cite the TS project's `workers: 1` choice as a "durable strategic stance, not provisional," driven by the single shared public AUT — a stance now reinforced by the live network instability observed in [17](17-Execution-Report.md)/[OBS-001](18-Defect-Documentation.md). Running multiple parallel workers against an already-unstable shared endpoint would only compound the risk, so serial execution is used in every job.
- **Retries:** `--reruns 2 --reruns-delay 3`, CI-only — matches the explicit `{ci: 2, local: 0}` precedent cited in [11 §30](11-Framework-Architecture.md). `pyproject.toml`'s local `addopts` were **not** modified — local runs remain retry-free by default, per [10 §16](10-Automation-Strategy.md).
- **Reporting:** `pytest-html`, matching [10 §25](10-Automation-Strategy.md)/ADR-3 — no Allure or other reporting stack introduced.
- **Diagnostics:** screenshots (`only-on-failure`) and traces (`retain-on-failure`) already configured in `pyproject.toml`'s `addopts` — inherited unchanged by every CI job, matching [10 §15](10-Automation-Strategy.md).
- **Artifact upload:** `actions/upload-artifact@v4`, `if: always()` (so evidence survives a failed job), covering `reports/html/`, `reports/screenshots/`, `reports/traces/`, 14-day retention (a reasonable Step 19 implementation choice — [10 §19](10-Automation-Strategy.md) explicitly left the exact retention window as "a Step 11/14 decision," never actually fixed by either of those steps). Logs are the job's own console output ([src/utils/logger.py](../src/utils/logger.py) writes to stdout with no file handler) — already retained natively by GitHub Actions; no separate log-file upload was added.
- **Secrets handling:** `AUT_BASE_URL`/`API_BASE_URL` are plain env vars (public URLs, not secrets — matching `.env.example`). `DURABLE_VALID_USER_EMAIL`/`DURABLE_VALID_USER_PASSWORD`/`DURABLE_EXISTING_USER_EMAIL` are wired from `${{ secrets.* }}` — currently unset in this repository (no GitHub secret has been configured), and **no currently implemented test consumes them** (only the 9 blocked cases would). This wiring is forward-compatible plumbing only: it changes nothing about today's CI behavior, does not create an account, and does not weaken the authorization gate in any way ([18-Defect-Documentation.md §7](18-Defect-Documentation.md), `BLK-001`/`BLK-002` remain open exactly as before).
- **Failure vs. environment distinction:** no automatic AUT-defect classification was implemented — per instruction, that judgment remains a manual QA/investigation step (as demonstrated throughout [17-Execution-Report.md §12](17-Execution-Report.md)). CI's job is to preserve evidence (HTML report, screenshots, traces, console log), not to auto-classify a failure's root cause.

## 10. Local Validation Performed

| Check | Result |
|---|---|
| YAML syntax | Parsed successfully with `yaml.safe_load` after fixing one real syntax error (an unquoted step name containing a colon, `"Install dependencies (single source of truth: pyproject.toml)"`, which YAML's scanner rejected — corrected by quoting the string). Final structure verified: 3 jobs, correct `if:` triggers, correct matrix, `on:`/`env:` sections parse as intended. |
| Dependency-extraction command | Executed locally with the exact `tomllib` one-liner used in the workflow — correctly produced all 8 pinned dependencies. |
| pytest collection (no scope change) | Total collected: **50** (unchanged from before this step's marker edits). `-m regression`: **22/50**. `-m smoke`: **7/50**. `-m cross_browser`: **4/50**. `-m ci_restricted`: **0/50**. `-m "regression and not ci_restricted"`: **22/50**. All counts match Section 4's design exactly. |
| Existing 22 tests unaffected | Full local run of `-m "regression and not ci_restricted"` performed twice in immediate succession: run 1 = 10 failed/12 passed; run 2 = a **different** set of 10 failed/12 passed. Every failure in both runs was a connection-layer error (`net::ERR_CONNECTION_RESET`, `net::ERR_SOCKET_NOT_CONNECTED`, `httpx.ReadError`/`ConnectError` wrapping `WinError 10054`) — the same signature as [OBS-001](18-Defect-Documentation.md). Since two runs of *identical* code produced two *different* failing subsets, the cause cannot be the marker changes (inert metadata) — it is the same live network instability [17-Execution-Report.md](17-Execution-Report.md) already documented, still active during this session. |
| Bounded-retry policy validated | Re-ran with the exact CI policy (`--reruns 2 --reruns-delay 3`): **21 passed, 1 failed, 10 reruns** — the policy recovered 9 of the 10 originally-failing tests. The 1 residual failure (`AE-UI-TC-001`) was then re-run in complete isolation and **passed cleanly** (`1 passed in 5.88s`), confirming it was the same transient network noise, not a defect. **Net result: all 22 implemented tests confirmed functionally intact — 22 passed, 0 genuine failures, across this validation session.** |
| No secret leakage | `ci.yml` contains no hard-coded credential — only `${{ secrets.* }}` references, which resolve to empty/unset in this repository today. `.env` remains gitignored and was never created. |
| No accidental scope expansion | pytest collection total unchanged at 50 before and after all edits; no new test function was added; no blocked/restricted/deferred/manual case gained a test. |
| Existing architecture rules intact | No import was added between `src/pages/` and `src/api/`; no test file's assertions, locators, or fixtures were touched — only marker decorators. |
| docs/01–18 unchanged | File modification timestamps confirmed identical to their pre-Step-19 state (Section 12). |
| TypeScript project unchanged | `git status --short` in the TS project directory returned clean (no output). |

### 10a. Jenkins / Azure DevOps Extension — Local Validation

| Check | Result |
|---|---|
| `azure-pipelines.yml` YAML syntax | Parsed successfully with `yaml.safe_load` — top-level `trigger`/`pr`/`pool`/`parameters`/`variables`/`stages` keys confirmed present with expected values; the single job's 7-step list (including the `${{ if eq(...) }}:` conditional template block) confirmed structurally intact. |
| `.github/workflows/ci.yml` re-verified unchanged | Re-parsed with the same `yaml.safe_load` check used in Section 10 — still valid, still exactly the 3 jobs (`pr_main_regression`, `nightly_regression`, `release_validation`) from the original implementation. **No modification was made to this file.** |
| `Jenkinsfile` syntax | **No Groovy interpreter, Jenkins installation, or Jenkins CLI (`declarative-linter`) is available in this environment** (`groovy` is not on PATH; Docker Desktop is installed but its daemon is not running, and starting it merely to lint one file was judged disproportionate). Real Jenkins declarative-pipeline validation therefore was **not** performed and is **not claimed**. What was actually performed: (1) brace/paren/bracket balance check — `{`=34/`}`=34, `(`=49/`)`=49, `[`=6/`]`=6, all balanced; (2) triple-quoted string balance — both `'''` and `"""` counts even (2 each); (3) confirmed presence of every required declarative-pipeline top-level block (`pipeline {`, `agent`, `parameters {`, `environment {`, `stages {`, `post {`) exactly where expected. This is a structural/lexical smoke test, **not** a substitute for Jenkins' own Pipeline Syntax validator or a real Jenkins job run. |
| Same pytest entry point across all three platforms | Confirmed by direct inspection: `ci.yml` uses `python -m pytest`, `Jenkinsfile` uses `python3 -m pytest`, `azure-pipelines.yml` uses `python -m pytest` — all module-invocation form (not bare `pytest`), preserving the `sys.path` behavior Section 9 already identified as required for the project's absolute imports to resolve. |
| Marker selection consistent | All three platforms default the business regression selection to the identical expression `regression and not ci_restricted`, and all three expose `chromium` as the default browser. Verified by direct text inspection of all three files side by side. |
| Artifact/report paths consistent | All three platforms preserve and publish `reports/html/`, `reports/screenshots/`, `reports/traces/` — the same three directories `pyproject.toml`'s `addopts` and `src/config/settings.py`'s `report_dir_path` already write to; no platform introduces a divergent report location. |
| Non-zero pytest exit fails the pipeline (all 3 platforms) | GitHub Actions: default `run:` step behavior (Section 9, unchanged). Jenkins: `sh` step throws on non-zero exit with no `returnStatus: true` anywhere in the file, which fails the stage/build natively. Azure DevOps: `script:` step fails the job by default with no `continueOnError: true` set anywhere in the file. Confirmed by direct inspection of all three files — no swallowed exit code exists in any of them. |
| No secrets hard-coded (all 3 platforms) | `ci.yml` references `${{ secrets.* }}` only (Section 9). `Jenkinsfile` and `azure-pipelines.yml` deliberately reference **no** credential/variable-group mechanism at all, since inventing a Jenkins credential ID or an Azure DevOps variable group that doesn't exist in any real controller/organization was explicitly out of scope (Sections 6b/6c) — confirmed by direct inspection: neither file contains `credentials(`, a variable-group reference, or any literal-looking secret value. |
| No test scope expansion (this extension) | pytest collection re-confirmed at exactly **50** total after adding `Jenkinsfile` and `azure-pipelines.yml` (neither file is Python and neither is collected by pytest) — identical to the count before this extension. |
| docs/01–18 unchanged (this extension) | File modification timestamps re-confirmed identical to their state before this extension began. |
| TypeScript project unchanged (this extension) | `git status --short` in the TS project directory re-confirmed clean. |
| No existing test logic changed (this extension) | Zero edits were made to any file under `tests/`, `src/`, or `pyproject.toml` during this extension — only two new root-level files (`Jenkinsfile`, `azure-pipelines.yml`) were created, plus this document. |

## 11. Final Local Regression Summary (this validation session)

| Outcome | Count | Detail |
|---|---|---|
| Passed (final confirmed state) | 22 | All 12 UI + 9 API + 1 Hybrid — every implemented case confirmed passing, either directly or after bounded rerun/isolated re-confirmation |
| Failed (genuine, non-environmental) | 0 | No assertion or content-based failure occurred at any point this session |
| Environmental/infrastructure failures observed (raw attempts, before rerun/isolation) | 10 in run 1, 10 (different set) in run 2, 1 residual after the reruns pass | All `net::ERR_CONNECTION_RESET`/`ERR_SOCKET_NOT_CONNECTED`/`httpx` `WinError 10054` — consistent with [OBS-001](18-Defect-Documentation.md), not a new finding |
| Skipped | 0 | No implemented test is configured to skip |
| Blocked / not represented in executable CI | 9 | `AE-UI-TC-004/005/007/008/021`, `AE-API-TC-007/011/012/014` — no test code exists; cannot appear in any CI job |

## 12. File Safety Verification

- `docs/01-Project-Vision.md` through `docs/18-Defect-Documentation.md`: file modification timestamps confirmed unchanged from their state at the start of this step. No edit was made to any of them.
- TypeScript reference project (`playwright-typescript-hybrid-framework`): `git status --short` returned clean.
- Files created this step: `.github/workflows/ci.yml`, `docs/19-CI-CD.md`, plus (this extension) `Jenkinsfile` and `azure-pipelines.yml`.
- Files modified this step: 8 test files (`tests/ui/test_home.py`, `test_signup_login.py`, `test_products.py`, `test_cart.py`; `tests/api/test_products_api.py`, `test_brands_api.py`, `test_auth_api.py`; `tests/hybrid/test_product_data_consistency.py`) — marker decorators only, disclosed in full in Section 4, verified behavior-preserving in Section 10.
- `pyproject.toml`, `src/`, `.env.example`, `.gitignore`, and (this extension) `.github/workflows/ci.yml` itself: **not modified**.
- No debug/scratch artifact remains — three throwaway local-validation HTML reports generated during this step's testing were removed (`reports/` is gitignored regardless, but removed for cleanliness). The temporary `pyyaml` package installed into `.venv` purely to validate `ci.yml`/`azure-pipelines.yml` locally was uninstalled again immediately after each validation pass, leaving the environment as found.
- No secret exposed — confirmed in Section 10 / 10a.

## 13. What This Step Does Not Do

- Does not implement Docker (Section 8 — explicitly Step 20+).
- Does not create any test for the 9 blocked cases, and does not skip-mark them to manufacture false coverage.
- Does not change the 46-case total scope, the 31-case `AUTOMATE` scope, or the 22-case implemented count.
- Does not change Gate 5 (still PARTIAL) or Gate 6 (still not release approval) — this document makes no release-readiness claim.
- Does not classify any environmental/network failure as an AUT defect — Section 10/11 explicitly attribute all observed failures to the same [OBS-001](18-Defect-Documentation.md) environmental cause already established.
- Does not use unlimited retries — bounded at 2, CI-only, exactly as designed.

## 14. Step 19 Exit Criteria

- [x] CI/CD workflow exists (`.github/workflows/ci.yml`) and is structurally valid (Section 10)
- [x] It runs exactly the 22 currently implemented, approved automated cases — no more, no fewer (Sections 6, 10)
- [x] Browser/environment setup is reproducible (`actions/setup-python`, pinned Python version, `playwright install --with-deps`)
- [x] Reporting and failure artifacts configured (`pytest-html`, screenshot/trace CLI flags, `upload-artifact` with `if: always()`)
- [x] Retry/parallelism behavior matches the approved strategy (bounded CI-only reruns=2; no parallel workers, matching the durable conservative stance)
- [x] Secrets handled safely (Section 9 — no hard-coded value, empty/unused today, no behavior change)
- [x] Network/environment failures not misclassified as AUT failures (Sections 10, 11, 13)
- [x] Local validation confirms the framework remains healthy — all 22 implemented tests confirmed functionally intact (Sections 10, 11)
- [x] `docs/19-CI-CD.md` accurately records what was implemented, what was verified, and what remains deferred (this document)
- [x] `docs/01–18` unchanged; the one discovered minor cross-document discrepancy (Section 5) was disclosed, not silently edited
- [x] TypeScript project untouched
- [x] **Jenkins (`Jenkinsfile`) implemented, orchestrating the same unforked test suite, structurally validated as far as technically possible without a Jenkins instance (Sections 6b, 10a)**
- [x] **Azure DevOps (`azure-pipelines.yml`) implemented, orchestrating the same unforked test suite, YAML-validated (Sections 6c, 10a)**
- [x] **GitHub Actions workflow verified unchanged and consistent with the Jenkins/Azure DevOps execution strategy (Section 10a)**
- [x] **All three platforms confirmed to invoke the same `-m pytest` entry point, the same default marker expression, and the same report/artifact directories (Section 10a)**
- [x] **No platform has been externally executed; none is claimed to have been (Section 6a)**
- [x] **No repository URL, Jenkins credential/controller/agent, or Azure DevOps organization/project/service connection was invented (Sections 6b, 6c)**
- [ ] QA Lead approval — required before Step 20

## 15. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 20. Per instruction, this step does not proceed further on its own.
