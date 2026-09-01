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

## 16. Post-Approval Addendum — Step 4–9 Findings (2026-08-27)

**Disclosed, not a silent correction.** Sections 1–14 above describe the CI/CD state as approved at Step 19 (2026-08-25), when 22 of 31 `AUTOMATE` cases were implemented and 0 carried `ci_restricted`. That state has since evolved through Steps 4–9 of this session — the facts below supersede specific figures and claims above; nothing in Sections 1–14 was rewritten.

**All 31 `AUTOMATE` cases are now implemented** (see [18 §14](18-Defect-Documentation.md), [23 §13](23-Test-Summary-Report.md)), including the 3 that now carry `ci_restricted`: `AE-UI-TC-004`, `AE-API-TC-011`, `AE-API-TC-012` (verified by direct inspection of `tests/ui/test_signup_login.py` and `tests/api/test_auth_api.py`). This supersedes §4's table row ("`ci_restricted` | ... | **None**") and §6/§10's "0 currently carry `ci_restricted`" / "22/50" collection figures.

**Section 7 is superseded, not contradicted — this is the outcome it explicitly predicted.** §7 stated: "The moment the 3 CI-RESTRICTED cases are implemented and marked, `nightly_regression` picks them up automatically." That has now happened: `nightly_regression` (`-m regression`, no exclusion) includes those 3 cases; `pr_main_regression` (`-m "regression and not ci_restricted"`) still excludes them. The two jobs are no longer identical in composition.

**The workflow now has 4 jobs, not 3.** A `full_project_validation` job (`workflow_dispatch`, unfiltered `pytest -v`, all three browsers installed) was added — see [18 §14](18-Defect-Documentation.md) and the real GitHub Actions run cited there (`33037686550`, `60/61 passed, 1 skipped`).

**Secrets wiring changed (§139 superseded).** The workflow-level `DURABLE_VALID_USER_EMAIL`/`DURABLE_VALID_USER_PASSWORD`/`DURABLE_EXISTING_USER_EMAIL` `${{ secrets.* }}` bindings described in §139 were removed — the disposable-account architecture ([18 §14](18-Defect-Documentation.md)) means no business case ever consumes them, so the forward-compatible plumbing was dead weight. In its place, `ACCOUNT_CREATION_EXECUTION_AUTHORIZED` is now wired job-scoped into `nightly_regression` and `full_project_validation`, gating disposable-account creation only — no durable-account secret is provisioned or referenced anywhere in `ci.yml`.

**`release_validation`'s browser-selection mechanism changed.** Bare `--browser=X` (as designed in §6) was replaced with `--override-ini="addopts=...--browser=X"` to fix a real CLI-flag-accumulation defect (pytest-playwright's `--browser` is additive, not replacing; commit `830d804`) — same intent (one browser engine per matrix leg), corrected mechanism.

**Open, non-blocking discrepancy — `cross_browser` marker (§45/§48 vs. actual code).** §48's table and [10-Automation-Strategy.md §17](10-Automation-Strategy.md) both define the curated cross-browser subset as exactly 4 cases (`AE-UI-TC-006/015/018/024`). Direct inspection of `tests/ui/test_signup_login.py` shows a 5th case, `AE-UI-TC-005`, also carries `@pytest.mark.cross_browser` (added during this session's Step 4 implementation). This is disclosed here, not silently resolved: per this closure task's explicit instruction not to modify test/production logic, the marker itself is left as-is. A future step should have the QA Lead decide whether to update [10 §17](10-Automation-Strategy.md)'s definition to include `AE-UI-TC-005`, or remove the marker — either is a one-line change, deferred to that decision rather than made unilaterally here.

**`Jenkinsfile` / `azure-pipelines.yml` — not updated, disclosed gap.** Both still describe the Step-19 22-case/"0 `ci_restricted`" state (§6b/§6c) and were not touched this session. Per §6a, **neither platform has ever been externally executed**, so this gap has zero effect on real CI behavior today. Bringing them to parity with `ci.yml`'s current state would be a non-trivial rewrite of two full pipeline files — outside this closure task's documentation-correction scope (no code/config behavior change was invited here) — and is flagged for a future step rather than fixed now.

**§13 and §14's exit-criteria "22...no more, no fewer" language** is superseded by the above: the implemented, CI-executed count is now 31/31, not 22/31.

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-27 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |

## 17. Post-Approval Addendum — Allure CI Integration (2026-08-27)

**Disclosed, not a silent correction.** Sections 1–16 above describe the CI/CD state through this session's Steps 4–9. Allure reporting was implemented after that, in a separate, later set of changes — this addendum documents it without rewriting anything above.

**Every pytest-executing job now follows this sequence, added purely additively:**

```
pytest execution
  ↓
Allure raw result generation (reports/allure-results/) — inherited automatically via
  pyproject.toml addopts in every job except release_validation, whose --override-ini
  string explicitly re-adds --alluredir=reports/allure-results (it replaces addopts
  wholesale, same mechanism as the existing browser-flag fix)
  ↓
Allure CLI installation (allure-commandline@2.39.0, official npm distribution —
  not a third-party GitHub Action)
  ↓
Allure HTML generation (allure generate reports/allure-results --clean -o reports/allure-report,
  guarded: skipped with a log message, not an error, if no results exist)
  ↓
Upload test evidence (existing actions/upload-artifact@v4 step, extended — not replaced)
```

**Four report/evidence locations are now uploaded in every job's evidence artifact:** `reports/html/` (pytest-html, unchanged), `reports/artifacts/` (Playwright screenshots/traces, unchanged), `reports/allure-results/` (new), `reports/allure-report/` (new). None of the pre-existing three were removed or altered.

**Job-result semantics, verified by real execution, not assumed:** the two new steps (`Install Allure CLI`, `Generate Allure HTML report`) carry `if: always()` (so they still run after a test failure — a report is still produced) and `continue-on-error: true` (so neither can ever flip the job's pass/fail signal). A real controlled GitHub Actions failure (run `33088035585`) confirmed this exactly: the pytest step failed, the job's overall conclusion was `failure`, and both Allure steps independently completed with `conclusion: success` — the failure was never masked, and Allure tooling never became the pass/fail authority.

**No GitHub Pages publishing and no cross-run history are configured.** Each run's Allure report is generated fresh (`--clean`) and uploaded as a standalone artifact with the same 14-day retention as the rest of the evidence — this was a deliberate scope boundary (evaluated and rejected: a third-party publishing Action, since most such Actions' core value proposition is history via `gh-pages`, which was out of scope here), not an oversight.

**Failure evidence flow, confirmed end-to-end by a real controlled CI failure:** a genuine pytest failure → Playwright screenshot (`test-failed-1.png`) + `trace.zip` written to `reports/artifacts/` (unchanged mechanism) → both attached to the corresponding failed test's Allure data (via `tests/conftest.py`, during fixture teardown — see [docs/21 §18](21-Reporting-Observability.md)) → `pytest-html`'s pre-existing Links column still links to both files independently → all evidence preserved in the uploaded CI artifact. Verified by downloading and directly inspecting the real artifact, not inferred from workflow YAML.

**`Jenkinsfile`/`azure-pipelines.yml` were not updated** — consistent with §16's already-disclosed gap (neither platform has ever been externally executed), this Allure work adds no new divergence beyond what was already open.

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-27 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |

## 18. Post-Approval Addendum — Full Cross-Browser CI Matrix Baseline (2026-08-31)

**Disclosed, not a silent correction.** Sections 1–17 above remain exactly as originally approved. This addendum documents an entirely new job, `full_cross_browser_validation`, added additively to `ci.yml` and validated through a dedicated multi-phase real-execution campaign (local design/implementation phases followed by real GitHub Actions validation across 5 independent triggers spanning 15 browser-leg executions). It does not modify or supersede anything in Sections 1–17 — `pr_main_regression`, `nightly_regression`, and `release_validation` are untouched.

### 18.1 What This Job Is

A `workflow_dispatch`-triggered job that runs the **entire collected test suite** (minus the 3 `requires_all_browsers`-marked infra-only nodes, which need all 3 engines in one job and remain `full_project_validation`'s exclusive responsibility) against **all three Playwright browsers**, in parallel, per browser:

```
matrix.browser: [chromium, firefox, webkit]    fail-fast: false
    │
    ├── install exactly one browser binary per leg (separate runner VM per leg)
    ├── python -m pytest -v -m "not requires_all_browsers"
    │     --override-ini="addopts=...--dist=loadgroup --browser=${{ matrix.browser }}"
    │     -n 2
    │     --reruns 2 --reruns-delay 3
    │     --html=reports/html/${{ matrix.browser }}/report.html
    ├── Allure raw results  → reports/allure-results/${{ matrix.browser }}/
    ├── Allure generated report → reports/allure-report/${{ matrix.browser }}/
    └── upload-artifact: full-cross-browser-validation-${{ matrix.browser }}-${{ github.run_id }}
```

Collected count per leg is **58**, not 61 — `61 − 3 (requires_all_browsers) = 58`, real and consistent across every real-CI run observed. Browser selection uses the same `--override-ini` mechanism §247 already established for `release_validation` (a bare `--browser=X` accumulates with `pyproject.toml`'s baked-in `chromium` default rather than replacing it) — re-verified with zero accumulation in every real run checked.

### 18.2 Shared-Account Safety Under This Matrix

`tests/conftest.py`'s `shared_registered_account` fixture (session-scoped) and its `pytest_collection_modifyitems` hook are **unmodified** by this work — this section documents their proven behavior under the new matrix, not a change to them.

- **Creator**: `test_ae_api_tc_011_create_account` — sorted first among the 8 account-lifecycle tests.
- **Dependents** (6): `test_ae_api_tc_007_verify_login_valid_credentials`, `test_ae_api_tc_014_get_user_detail_by_email`, `test_ae_ui_tc_005_login_with_valid_credentials`, `test_ae_ui_tc_007_logout_from_authenticated_session`, `test_ae_ui_tc_008_register_with_already_registered_email`, `test_ae_ui_tc_021_search_add_to_cart_persists_after_login`.
- **Deleter**: `test_ae_api_tc_012_delete_account` — sorted last.

Two mechanisms make this safe under `-n 2`, both load-bearing:

1. **`@pytest.hookimpl(tryfirst=True)`** on the ordering hook — required because `pytest-xdist`'s own `WorkerInteractor.pytest_collection_modifyitems` (which encodes `xdist_group` into each item's nodeid) runs in the same worker process and, without `tryfirst`, could run *before* this project's own hook has added the marker, seeing nothing to group (STEP 18's own empirically-discovered finding, unchanged, re-verified every real-CI run this addendum covers).
2. **`xdist_group(name="shared_registered_account")`**, applied to all 8 dependent items — forces them onto one worker, since the fixture is session-scoped *per worker process*, not per whole run.

**Real-CI evidence** (not local-only): in every real run checked — Phase 11 (1 run), Phase 13.1 (1 run), Phase 15 (3 runs) — all 8 tagged nodes appeared on `[gw0]` in the console log, creator first, deleter last, zero exceptions across 15 independent leg-executions. No account-related failure, corruption, or orphaned state was observed in any real CI run.

### 18.3 Retry Behavior — What Is Actually Proven

`--reruns 2 --reruns-delay 3` is the same bounded-retry policy Section 9 already established for the other jobs, reused here unchanged.

**PROVEN by real GitHub Actions execution** (not inferred): a genuine first-attempt failure, retried, and passed. On 2026-08-31, WebKit's `test_ae_ui_tc_011_view_all_products_and_product_details[webkit]` failed on attempt 1 (`AssertionError: Locator expected to be visible`, `.product-information h2`, 5000ms timeout — the exact known signature, §18.5), was retried (`RERUN` in the console log), and passed on attempt 2. Verified end-to-end: raw Allure recorded **two** result entries for this test (one `"status": "failed"`, one `"status": "passed"`, ~13s apart) — 59 raw files instead of 58 for that one leg — while the **generated** Allure report correctly reconciled this back to `total: 58`, showing the test in its final, passed state. Real screenshot (368,622 bytes) and a real, valid trace archive (independently verified with Python's `zipfile.testzip()` — zero corruption, 126 entries) for the failed first attempt were both uploaded in that run's WebKit artifact, and confirmed absent from the Chromium/Firefox artifacts of the same run.

**NOT PROVEN**: behavior when a test fails through *all* retry attempts and the leg genuinely fails as a result. No such event has occurred in any real CI run of this job to date. This is an explicit, disclosed evidence limitation — not assumed, not claimed, not manufactured.

### 18.4 Reporting & Artifact Flow

The evidence chain is the same one [docs/21 §18](21-Reporting-Observability.md) already documents (`pytest → raw Allure → generated Allure → pytest-html → GitHub artifact`), now additionally proven **browser-scoped and running 3× concurrently** without cross-contamination:

- Every path (`reports/{artifacts,allure-results,allure-report,html}/${{ matrix.browser }}`) and the artifact name itself (`full-cross-browser-validation-${{ matrix.browser }}-${{ github.run_id }}`) carries the browser token — confirmed unique per leg, per run, via the GitHub Artifacts API, in every run checked.
- **Zero cross-browser contamination** found in any explicit check performed (Allure JSON `browser_name`/node-id, generated-report `data/` contents, HTML content, artifact directory structure) — this is one of the most heavily re-verified claims in the project's history at this point.
- **Clean-run artifact contents**: `allure-results/<browser>/`, `allure-report/<browser>/`, `html/<browser>/` only — no `artifacts/<browser>/` (screenshots/traces) directory, correctly, since `if-no-files-found: ignore` omits it when nothing failed.
- **Failure-run artifact contents**: the above three, plus `artifacts/<browser>/` containing the real screenshot/trace, only for the browser(s) that actually failed — confirmed by direct example (§18.3).
- **Video**: absent in every run checked, by design (no `--video` flag anywhere in the effective command) — never a defect, never enabled by this work.

### 18.5 Known-Risk Register

**WebKit `TC-011`** (`test_ae_ui_tc_011_view_all_products_and_product_details[webkit]`) — **classification: Intermittent WebKit-specific compatibility/timing risk — root cause not conclusively proven.** Signature: `AssertionError: Locator expected to be visible`, locator `.product-information h2`, `to_be_visible` timeout 5000ms, `Error: element(s) not found`. Evidence spans local isolation runs (mixed pass/fail across many independent sessions) and real CI (multiple clean passes; one real fail→retry→pass event, §18.3). **Not marked resolved by any passing run — including the one that passed via retry.** Do not increase its timeout, add a wait, change its selector, or add a test-specific retry without new root-cause evidence.

**Firefox context-teardown race** — signature `Playwright.../Protocol error (Browser.removeBrowserContext): can't access property "_maybeDontRestoreTabs", this._windows[aWindow.__SSi] is undefined`, surfacing as an Allure `broken`-status teardown-phase error (not a `failed` assertion). **Historical occurrence: one local session only.** Not reproduced in any subsequent local run or any real CI run of this job. Not called fixed (no code change was ever made to address it); not called an active/deterministic defect (it has not recurred despite many further opportunities to).

**Persistent failure after exhausting all retries** — **classification: NOT PROVEN / NOT OBSERVED.** No real CI run of this job has ever failed a leg after retries were exhausted. This is an evidence limitation to be closed opportunistically by future real usage, not something to manufacture.

**OBS-001-class environmental instability** (`httpx.ReadError`/`ConnectError`/`WinError 10054`, `NS_ERROR_ABORT`, `SSL connect error`, Cloudflare 522, `ERR_CONNECTION_RESET`/`ERR_SOCKET_NOT_CONNECTED`) — observed extensively in **local** execution sessions and, separately, in a **sibling job** (`release_validation`) during two different real-CI trigger events. **Never observed in this job's own real-CI executions to date.** Sibling-job failures are disclosed for transparency but are not treated as evidence about this job's own reliability absent a direct causal link.

### 18.6 Failure Triage Guide

When a leg of this job fails, classify using the exact signature before acting — do not default to any single category:

| Category | Signal | Action |
|---|---|---|
| **A — Assertion failure** | `AssertionError` in test body, product/page content did not match expectation | Investigate as a potential product or test-data issue; do not assume browser-specific |
| **B — Fixture/setup/teardown error** | Allure `status: "broken"`, error outside the test's own `assert`/`expect` call (e.g., during `context.close()`, fixture setup) | Investigate separately from assertion failures — often browser/driver-level, not test-logic |
| **C — WebKit `TC-011`** | Exact signature in §18.5, WebKit only | Compare the exact signature before classifying; do not assume every WebKit failure is this known risk, and do not assume a WebKit pass means it's fixed |
| **D — OBS-001/environmental** | Any signature listed in §18.5's environmental row, on **any** browser or layer (API or UI) | Confirm via reproducibility (rerun in isolation) and cross-test/cross-browser breadth (same signature on unrelated tests = environmental, not a single test's defect) before classifying — never classify solely because "a test failed" |
| **E — Retry event** | Console shows `RERUN`, final result is `passed` | The final `PASSED` is real, but the underlying first-attempt failure is real too — record and compare its signature against the known-risk register; a pass-via-retry never erases a historical intermittent event from the record |

### 18.7 Operational Runbook

1. Trigger via `workflow_dispatch` (`gh workflow run CI --ref main` or the GitHub UI).
2. Confirm all 3 `Full Cross-Browser Validation (<browser>)` jobs appear and run independently (`fail-fast: false` — one leg failing must not cancel the others).
3. Confirm each leg's console shows `2 workers [58 items]` — if the collected count differs from 58, investigate before trusting the run's results.
4. Confirm `created: 2/2 workers` and `scheduling tests via LoadGroupScheduling` when investigating xdist-related behavior specifically.
5. Read each leg's final pytest summary line (`N passed, M skipped, ...`).
6. Check for any `RERUN` line — note it even if the final result is green (§18.6, Category E).
7. Download the relevant browser's artifact (`full-cross-browser-validation-<browser>-<run_id>`) — never assume another browser's artifact is relevant.
8. If investigating a failure, inspect the raw Allure JSON in `allure-results/<browser>/` first — it has the most precise `statusDetails`.
9. Cross-check against the generated Allure report (`allure-report/<browser>/`) for a human-readable view.
10. Cross-check the `html/<browser>/report.html` for a third, independent view of the same result.
11. If a screenshot/trace exists under `artifacts/<browser>/`, inspect it before forming a conclusion.
12. Compare the exact failure signature against §18.5's risk register before classifying.
13. Do not modify test/framework/CI code until the evidence supports a specific, justified change — an intermittent risk observed once is not, by itself, grounds for a fix.

### 18.8 Components Validated — Change Only With Re-Validation

| Component | Why it matters | Re-validation required if changed |
|---|---|---|
| Browser matrix (`[chromium, firefox, webkit]`) | The 15-leg real-CI evidence base is specific to these 3 engines | Re-prove matrix expansion, browser selection, and isolation for any added/removed engine |
| `--override-ini` browser-selection mechanism | Prevents a real, previously-occurring browser-accumulation bug (§247) | Re-check for zero accumulation on every leg |
| `-n 2` | The specific worker count actually observed in every real run | A different count needs its own real-CI proof, not an assumed linear scale-up |
| `--dist=loadgroup` | Required for `xdist_group` to function at all; silent failure mode if removed | Re-verify shared-account grouping under `-n` |
| `@pytest.hookimpl(tryfirst=True)` (STEP 18) | Empirically-required; its absence silently reintroduces cross-worker account-test splitting with no visible error until it corrupts a run | Re-run a real `-n 2` execution and confirm `[gwN]` grouping directly from the console |
| `shared_registered_account` grouping | The entire disposable-account safety model depends on it | Re-verify creator-first/deleter-last/same-worker under `-n` |
| Retry policy (`--reruns 2 --reruns-delay 3`) | Determines what failure classes get silently absorbed into a green result | Re-assess which risks the new values would mask |
| Browser-scoped report paths | Prevents 3 concurrent legs from colliding | Re-run the 6-direction contamination check |
| Browser-scoped artifact names | Same reasoning, at the GitHub-artifact level | Re-confirm uniqueness via the Artifacts API |
| Allure generation step (`if [ -d ... ] && [ -n "$(ls -A ...)" ]` guard, `--clean`) | Load-bearing for correct per-leg isolation | Re-check raw-vs-generated reconciliation |
| Artifact upload step (path list, `if-no-files-found: ignore`) | Changing the path list can silently drop an evidence type with no error | Re-confirm all 4 evidence types still upload correctly |
| `ACCOUNT_CREATION_EXECUTION_AUTHORIZED` gate | The sole mechanism preventing unauthorized real account creation in CI | Treat as a security-relevant change requiring explicit re-authorization, not just re-testing |

### 18.9 Explicit Anti-Patterns

- Do not remove `--dist=loadgroup` casually — it silently breaks account-lifecycle safety with no immediate visible symptom.
- Do not change worker count without a fresh real-CI validation.
- Do not remove `tryfirst=True` — reintroduces STEP 18's original, empirically-confirmed grouping bug.
- Do not move the account creator/deleter tests arbitrarily — their ordering is enforced by the collection hook, not file position, but the hook's own phase logic assumes their exact function names.
- Do not remove browser-specific report paths, or merge artifacts from different browsers manually.
- Do not treat a retry-pass as proof the underlying test is fixed (§18.3/§18.6 Category E).
- Do not classify every WebKit failure as a framework bug, or every connection error as a browser bug — always compare the exact signature first (§18.6).
- Do not delete or overwrite failure evidence before it has been analyzed.
- Do not introduce a new retry count without re-validating what failure classes it would newly mask or newly expose.

### 18.10 Final Readiness Classification

**READY WITH KNOWN INTERMITTENT RISK.** Every mechanism this job is itself responsible for — matrix expansion, browser selection, collection, xdist worker/scheduling, shared-account grouping, retry handling, Allure/HTML reporting, artifact naming/upload/isolation, cross-browser isolation — has been proven correct and consistent across 5 independent real GitHub Actions triggers and 15 browser-leg executions, including under the one real failure observed to date. The known, unresolved risk is WebKit `TC-011`'s intermittency; the known, disclosed evidence gap is real-CI behavior on a test that fails through all retries. Neither is treated as blocking; neither is hidden.

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-31 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |

## 19. Post-Approval Addendum — STEP 20 Operationalization & Maintenance Handoff (2026-08-31)

**Disclosed, not a silent correction.** Sections 1–18 remain exactly as originally approved; nothing in them is rewritten. STEP 19 (§18) validated the `full_cross_browser_validation` architecture; this addendum operationalizes it for day-to-day use and future maintenance. Where §18 already covers a topic in full (the operational runbook §18.7, the failure triage table §18.6, the change-control table §18.8/§18.9), this addendum cross-references it rather than duplicating it, and adds only what §18 does not yet cover: the operational distinction between all 5 real CI jobs, browser/toolchain upgrade procedure, proportional re-validation rules, and a single final operational-baseline statement.

### 19.1 CI Operational Runbook

Already documented in full at **§18.7** — trigger, matrix-leg verification, collection-count check (58), worker/scheduling evidence, retry-line check, artifact download, Allure/HTML/screenshot/trace inspection order, and the "do not modify until evidence supports it" closing rule. Re-read and re-confirmed accurate against the live `ci.yml` this addendum (§19, re-verified below). Nothing added here beyond one practical addition:

**What a normal successful `full_cross_browser_validation` run looks like** (re-confirmed against real evidence, not assumed): 3 green legs, each console ending in `NN passed, 1 skipped in ...s` (58 collected, 1 expected skip — `test_durable_valid_account_fixture_returns_configured_credentials`, correctly skipped in CI since no durable credentials are configured there), `created: 2/2 workers` and `scheduling tests via LoadGroupScheduling` present in every leg's log, 3 uniquely-named artifacts (`full-cross-browser-validation-<browser>-<run_id>`) uploaded, zero `RERUN` lines. Any deviation from this shape is the trigger to consult §18.6/§19.3.

### 19.2 PR / Main CI Workflow Operations

Re-read directly from `.github/workflows/ci.yml` this addendum (`on:` block, lines 16–30; each job's own `if:`), not assumed from earlier phases:

| Job | Trigger (`if:`) | Purpose | Blocking? |
|---|---|---|---|
| `pr_main_regression` | `pull_request → main` or `push → main` | Chromium-only regression gate on every PR and every merge to `main` (docs §6) | **Yes** — this is the actual PR/merge gate |
| `nightly_regression` | `schedule` (`0 2 * * *`, daily) | Full regression including `ci_restricted` cases, Chromium only — environment/AUT-availability canary, independent of code changes (docs §7, §120) | No (unattended; investigate failures, don't block on them retroactively) |
| `release_validation` | `workflow_dispatch` | Chromium full regression + Firefox/WebKit curated `cross_browser` subset (docs §6, §64) — manual, pre-release-style check | No (manual, informational) |
| `full_project_validation` | `workflow_dispatch` | All 61 collected nodes, no marker filter, single-browser (Chromium) execution — the only job exercising `requires_all_browsers` (docs §243) | No (manual, informational) |
| `full_cross_browser_validation` | `workflow_dispatch` | **STEP 19's own job** — full 58-node suite × 3 browsers × `-n 2` (§18) | No (manual; not wired into the PR/merge gate — see §19.7) |

**What engineers should inspect on a failure**: for `pr_main_regression`/`nightly_regression`, the single Chromium job's own console + `pytest-html`/Allure artifact (pre-existing mechanism, docs §9/§17 — unaffected by STEP 19). For `full_cross_browser_validation`, follow §18.7's runbook per failing leg. **Which failures are blocking**: only `pr_main_regression`'s own failure blocks a PR/merge — the other four jobs are manual or scheduled and inform, not gate. **Known intermittent risks to check before treating as a defect**: WebKit `TC-011` (§18.5) if the failing leg is WebKit and the signature matches exactly; the Firefox teardown-race signature (§18.5) if a Firefox leg shows a `broken`-status teardown-phase error; any OBS-001 signature (§18.5) on any leg/layer.

**Finding, not a fix**: `full_cross_browser_validation` is `workflow_dispatch`-only — it does not run on every PR or merge. This is exactly how Phase 6/7 designed it (a deliberate scope boundary, not an oversight — §18.1's own design rationale). Documented here as a fact for operational awareness, not flagged as a defect requiring a change.

### 19.3 CI Failure Triage

Already documented in full at **§18.6** (Categories A–E: assertion failure, fixture/teardown error, WebKit `TC-011`, OBS-001/environmental, retry event) — each with its identifying signal and required action. No new category introduced. Restated compactly per this phase's own required format:

| Category | Signal | First action | Rerun appropriate? | Preserve evidence? | Possible framework defect? | Escalate? |
|---|---|---|---|---|---|---|
| A — Assertion failure | `AssertionError` in test body | Read the exact assertion + page/response content | Yes, once, to check reproducibility | Yes | Possibly — investigate signature first | If reproducible and signature is new |
| B — Fixture/teardown error | Allure `status: "broken"`, error outside `assert`/`expect` | Identify which fixture/step failed | Yes | Yes | Possibly, or driver/browser-level (§18.5 Firefox race) | If reproducible |
| C — WebKit `TC-011` | Exact signature: `.product-information h2`, 5000ms timeout, `element(s) not found` | Compare byte-for-byte against §18.5's signature | Already covered by `--reruns 2` | Yes (screenshot/trace) | No — known, classified risk unless signature differs | Only if signature differs from the established one |
| D — OBS-001/environmental | Any signature in §18.5's environmental list, any browser/layer | Check reproducibility + breadth (same signature, different tests) | Yes | Yes | No, if breadth/reproducibility confirm environmental | Only if it starts appearing inside the target job's own real-CI runs (not yet observed, §18.5) |
| E — Retry event | Console `RERUN`, final `passed` | Record it even though the job is green | N/A — already happened | Yes, both attempts' evidence if available | No, by itself | No — but log for pattern-tracking against §18.5 |

**Never** default every failure to environmental, and **never** default every failure to a framework defect — classification follows the exact signature and available evidence, per §18.6's own explicit instruction, unchanged here.

### 19.4 Browser / Playwright Upgrade Rules (new)

No upgrade has been performed. This section defines the **future procedure only**.

| Change | Why it matters | Minimum re-validation | Evidence to check | Compare against |
|---|---|---|---|---|
| Playwright version bump | Changes the underlying browser-automation protocol and bundled browser binaries simultaneously | A read-only collection check (`58` still expected) + one real `workflow_dispatch` run of `full_cross_browser_validation`, all 3 legs | Console `2/2 workers`/`LoadGroupScheduling` lines, pass/fail/skip counts, any new failure signature | The current baseline in §18.1/§18.2 (58 collected, `[gw0]` grouping) and §18.5's risk register |
| Chromium/Firefox/WebKit engine version change (via a Playwright bump, since engines are bundled, not independently pinned) | Any of these could change TC-011's or the Firefox teardown-race's frequency, or introduce a new signature | Same as above, with particular attention to the affected browser's own leg | That leg's exact failure signature, if any | §18.5's exact recorded signatures — a **different** signature is new evidence, not a continuation of the known risk |
| Python version change | Affects the runner's interpreter, not the test logic, but can affect `tomllib`/dependency-install behavior (docs §130/§133) | Confirm `python -m pytest` still resolves imports correctly (a collection-only check is sufficient) | Collection succeeds, no import error | N/A — this is a install/environment-level check, not a behavior re-validation |
| pytest / pytest-xdist version change | Could change scheduling behavior, marker handling, or the `tryfirst=True` interaction (§18.2's own empirically-discovered mechanism) | A real `-n 2` run with explicit console verification of `[gwN]` grouping for the 8 shared-account tests | `created: 2/2 workers`, `LoadGroupScheduling`, `[gw0]` grouping identical to §18.2 | STEP 18's own original grouping-bug history — re-run the exact check that first caught it |

**Acceptance criterion for any upgrade**: no new failure signature appears outside the already-documented risk register (§18.5), and the shared-account grouping/ordering evidence remains identical in shape to what's already established. A different WebKit or Firefox failure signature than the ones on record is **new evidence requiring its own investigation**, not an extension of the existing accepted risk.

### 19.5 Controlled CI Change Protocol

Already documented in full at **§18.8** (12-component table: why each matters, what to re-validate) and **§18.9** (explicit anti-pattern list). Restated as the governing principle, unchanged: **VALIDATED — CHANGE ONLY WITH RE-VALIDATION.** No new component added to the list; no existing entry weakened.

### 19.6 Re-Validation Rules — Proportionality (new)

§18.8 defines *what* to re-check per component; this section adds *how much* validation is proportional to the kind of change:

| Change class | Example | Required validation |
|---|---|---|
| Documentation-only | Fixing a typo in this file, adding a cross-reference | None — no code/CI touched |
| Non-load-bearing CI change | Adding a new unrelated job, changing a job's `name:` display string, adjusting `timeout-minutes` generously upward | Confirm the changed job itself runs correctly once; no need to re-run the full STEP 19 campaign |
| Load-bearing CI change | Any §18.8-listed component (matrix, `-n 2`, `--dist=loadgroup`, `tryfirst=True`, grouping, retry policy, report/artifact paths, Allure generation, upload paths) | The specific re-validation §18.8 names for that component, via one real `workflow_dispatch` run at minimum — not the full 17-phase campaign, but real evidence, not assumption |
| Browser/toolchain upgrade | Playwright, browser engine, Python, pytest/pytest-xdist version bump | §19.4's procedure |
| Security/safety-sensitive change | `ACCOUNT_CREATION_EXECUTION_AUTHORIZED` gate, any secret wiring | Explicit re-authorization by whoever owns that decision, not just a technical re-test (§18.8's own existing framing, restated here for emphasis) |

This is a **proportionality** rule, not a loophole: it exists so a one-line documentation fix doesn't trigger unnecessary re-execution, while anything touching a §18.8-listed mechanism still gets real evidence before being trusted.

### 19.7 Final Operational Baseline & Maintenance Handoff

- **Validated commit**: `f813defd30bfed7acc1690a881a1e41c4336c709` (the commit `full_cross_browser_validation` was added in; `HEAD == origin/main` at every phase's close through this addendum).
- **Browser matrix**: `chromium`, `firefox`, `webkit`.
- **Worker count**: `-n 2`.
- **Scheduling mode**: `--dist=loadgroup` (`LoadGroupScheduling`).
- **Retry policy**: `--reruns 2 --reruns-delay 3`.
- **Report/artifact isolation model**: browser-scoped paths (`reports/{artifacts,allure-results,allure-report,html}/<browser>`), browser-scoped artifact names (`full-cross-browser-validation-<browser>-<run_id>`).
- **Current known risks**: WebKit `TC-011` (intermittent, unresolved); Firefox teardown race (single historical occurrence, Phase 5 only); persistent-failure-after-retries (not proven/not observed) — all three preserved exactly as §18.5/STEP 19's final closure report classified them, unchanged by this addendum.
- **Current evidence limitations**: real-CI behavior on a test that fails through all retries (never observed); pytest-html's internal structured schema (never fully parsed at the field level, content-presence only); real-CI reliability sample (5 triggers/15 leg-executions — meaningful, not exhaustive); sibling-job behavior (observed incidentally, outside this job's own direct scope).
- **Documentation location**: this file, `docs/19-CI-CD.md` §18 (architecture/design/evidence) and §19 (this section — operational/maintenance).
- **What future engineers MUST NOT change casually**: the 12 components listed in §18.8, without the matching re-validation from §18.8/§19.6.
- **What evidence to preserve when a failure occurs**: the failing leg's raw Allure JSON, generated Allure report, HTML report, and (if present) screenshot/trace — download the artifact before any rerun that could produce a fresh, overwriting run; classify per §19.3 before concluding anything.
- **Ownership**: not assigned to a named individual in any project document — whoever operates this repository's CI going forward inherits this baseline and the §18.8/§19.6 re-validation obligations; no owner is invented here.

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-31 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
