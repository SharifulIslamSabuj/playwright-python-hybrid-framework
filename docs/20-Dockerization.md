# 20 — Dockerization

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-DOCKER-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | **Implemented, statically validated, and now live-validated (runtime re-validation, 2026-08-25): image built successfully, 50 tests collected in-container, 22/22 passed on the default selection, report persistence confirmed on host, no secret found in the image. See Sections 10–15 and 20.** |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 (implementation); 2026-08-25 (runtime re-validation, same day, later session) |
| Phase | Step 20 — Dockerization (Docker has no dedicated phase number of its own in the roadmap — [docs/01-Project-Vision.md:60](01-Project-Vision.md) names Phase 15 as "Reporting & Observability"; corrected here per Step 21 QA Lead authorization) |
| Step | Step 20 — Dockerization |
| Predecessor Documents | [01](01-Project-Vision.md)–[19](19-CI-CD.md), all ✅ approved |

## 1. Objective

Containerize the existing Playwright + Python hybrid automation framework for reproducible local execution, per the design already approved (not invented) in [04-Test-Plan.md §23](04-Test-Plan.md), [05-Test-Strategy.md §12](05-Test-Strategy.md), [10-Automation-Strategy.md §20](10-Automation-Strategy.md), and [11-Framework-Architecture.md §32/§44](11-Framework-Architecture.md). This is additive: it does not redesign the framework, change any test logic, or replace GitHub Actions, Jenkins, or Azure DevOps ([docs/19-CI-CD.md](19-CI-CD.md), all three left unmodified — verified in Section 17).

## 2. Scope

Exactly 3 files created: `Dockerfile`, `.dockerignore`, this document. No other file was created. The container orchestrates the same, unforked `tests/` suite the three existing CI/CD platforms already run — the same 22 currently implemented, approved automated Test Cases, selected by the same pytest markers. No test logic was added, removed, rewritten, or weakened. The approved 46-case scope (22 executed / 9 blocked / 4 restricted / 9 deferred / 2 manual) is unchanged and is not re-executed or reclassified by this step.

## 3. Verified Playwright Base Image/Tag

`playwright==1.62.0` is pinned exactly in `pyproject.toml`. Per instruction, the corresponding Docker tag was **verified, not guessed**:

- A web search initially suggested `v1.62.0`/`v1.62.0-noble` tags exist, but also surfaced [microsoft/playwright issue #41987](https://github.com/microsoft/playwright/issues/41987), which reported v1.62.0 Docker images as **missing** as of 2026-07-25.
- Rather than trust either the search summary or the (potentially stale) issue at face value, the **actual Microsoft Container Registry tag-list API** was queried directly: `https://mcr.microsoft.com/v2/playwright/python/tags/list`. This returned the real, current tag catalog, confirming `v1.62.0`, `v1.62.0-amd64`, `v1.62.0-arm64`, `v1.62.0-jammy`, `v1.62.0-noble`, and `v1.62.0-resolute` (plus per-architecture variants) are all **currently published** — the July gap reported in the GitHub issue had evidently been resolved by the time of this check.

**Selected tag: `mcr.microsoft.com/playwright/python:v1.62.0-noble`** (Ubuntu 24.04 LTS) — pinned explicitly to a specific OS codename rather than the floating `v1.62.0` tag, for reproducibility, mirroring the specificity of the TS reference project's own cited `v1.61.1-noble` precedent ([10-Automation-Strategy.md §20](10-Automation-Strategy.md)) without copying it verbatim.

**Disclosed limitation:** this verification was performed via the registry's tag-list API and cross-checked against a web search — it is a real, primary-source check of what the registry currently serves, but it is **not** the same as an actual successful `docker pull`/`docker build` against that tag (Section 10 explains why that step could not be completed this session).

## 4. Docker Architecture

Per the QA Lead's explicit direction and the pre-existing approved design: **one `Dockerfile`, single-stage build, no docker-compose, official Playwright Python image, Linux container, Chromium as the default execution browser.** No separate browser-specific Dockerfiles were created — Firefox/WebKit remain reachable via a `--browser=` runtime override, exactly as the three existing CI/CD platforms already do it. Docker-compose was evaluated and rejected: nothing in this project needs a second service (no local database, mock server, or dependency beyond the public AUT), so introducing compose would be exactly the "unnecessary complexity" the QA Lead's instructions forbid.

## 5. Dockerfile Design

| Instruction | Purpose |
|---|---|
| `FROM mcr.microsoft.com/playwright/python:v1.62.0-noble` | Verified base image (Section 3). Bundles Chromium/Firefox/WebKit binaries matching the pinned Playwright version — **no separate `playwright install` step is needed or included**, since the image tag already matches `playwright==1.62.0` exactly. |
| `WORKDIR /app` | The directory `src/` and `tests/` are copied into — the same directory `python -m pytest`'s working-directory-based `sys.path` insertion resolves `from src.pages...` against ([docs/19-CI-CD.md §9](19-CI-CD.md)). |
| `COPY pyproject.toml ./` (before the rest) | Standard Docker layer-caching practice — a source-only change doesn't force a dependency reinstall. Does not change the dependency source of truth. |
| `RUN pip install $(python -c "import tomllib; ...")` | The **identical** `tomllib`-based extraction from `pyproject.toml`'s `[project.dependencies]` already used, unmodified, by `.github/workflows/ci.yml`, `Jenkinsfile`, and `azure-pipelines.yml` — no `requirements.txt` created, `pyproject.toml` not modified, single source of truth preserved across all four execution surfaces. |
| `COPY . .` | Full project source, filtered by `.dockerignore` (Section 6) — no secret or host-only artifact enters the build context. |
| *(no `ENV` for AUT_BASE_URL/API_BASE_URL)* | Deliberate: `src/config/settings.py` already defaults both to `https://automationexercise.com` via `os.getenv(..., default)`. Hard-coding the same value again in the Dockerfile would be exactly the "do not duplicate configuration that already exists" the instructions warn against — the Python code's own default already covers it identically. |
| `CMD ["python", "-m", "pytest", "-m", "regression and not ci_restricted"]` | The same PR-tier default every existing CI/CD platform already runs ([docs/19-CI-CD.md §6](19-CI-CD.md)), using the required **module-invocation form** (`python -m pytest`, never bare `pytest`) that preserves the project's import resolution. Chromium applies via `pyproject.toml`'s own `addopts` (`--browser=chromium`), not repeated here. Fully overridable at `docker run` time (e.g., a different `-m` expression or `--browser`), mirroring the TS reference project's own cited "override at `docker run` time" pattern. |

## 6. .dockerignore Design

Contains exactly the minimum exclusion list specified by the QA Lead — `.git/`, `.venv/`, `venv/`, `env/`, `.pytest_cache/`, `__pycache__/`, `*.pyc`, `reports/*`, `.env`, `.env.local`, `.env.*.local`, `.vscode/`, `.idea/`, `test-results/`, `playwright-report/`, `.playwright/` — nothing more. Per explicit instruction, `docs/`, `pyproject.toml`, `src/`, `tests/`, and the three CI/CD files are **not** excluded (no specific technical reason exists to exclude them; an earlier draft of this file mistakenly added `docs/` and `.github/` exclusions "to keep the build context small," which was corrected before finalizing — the instruction explicitly named that reasoning insufficient). `reports/*` and `.env`/`.env.*.local` are the two exclusions doing the real work: the first keeps host-generated report artifacts out of the build context (Section 9), the second is the actual mechanism enforcing "never bake a credential into the image."

## 7. Dependency Installation Strategy

Unchanged in principle from [docs/19-CI-CD.md §9](19-CI-CD.md): no `[build-system]` table exists in `pyproject.toml` (confirmed by inspection — the project is not packaged/installable), so the Dockerfile reads `[project.dependencies]` directly with the standard-library `tomllib`, identically to all three existing CI/CD files. `pyproject.toml` itself was not modified in any way.

## 8. Runtime Environment Configuration

No environment variable is baked into the image. `AUT_BASE_URL`/`API_BASE_URL` rely on `src/config/settings.py`'s existing safe defaults. Any override (browser, timeouts, `DURABLE_*` credentials once QA-Lead-authorized provisioning ever occurs) is supplied at `docker run` time via `-e`/`--env-file`, never inside the image — matching [docs/10 §20](10-Automation-Strategy.md)/[docs/11 §32](11-Framework-Architecture.md) exactly. No currently implemented test consumes the `DURABLE_*` variables regardless (only the 9 blocked cases would — Section 15 preserves their blocker status unchanged).

## 9. Report Persistence

Design (per [docs/11 §32](11-Framework-Architecture.md): "mounted or copied-out volume... not lost inside the container"): a host bind mount, e.g.

```
docker run --rm -v "$(pwd)/reports:/app/reports" <image>
```

(or the equivalent Windows syntax, e.g. `-v "${PWD}\reports:/app/reports"` in PowerShell). `.gitignore` was **not** modified to accomplish this — `reports/` was already gitignored before this step ([docs/11 §33](11-Framework-Architecture.md), unchanged since Step 13). **This mount behavior is documented but not yet verified by an actual run — see Section 13.**

## 10. Docker Build Evidence

**Originally NOT AVAILABLE** (see the retained history below) — **now obtained via a runtime re-validation pass later the same day (2026-08-25), after Docker Desktop became functional on this machine.**

**Original blocker (retained for the record):** Docker Desktop's backend initially failed to start. Root cause (confirmed via `%LOCALAPPDATA%\Docker\backend.error.json`): the backend's unrelated "Inference Manager" component failed during startup while trying to remove two stale runtime socket files (`dockerInference`, `userAnalyticsOtlpHttp.sock`, both corrupted/orphaned Windows reparse points dated 2026-08-08). Remediation attempted at the time — `Remove-Item -Force`, `cmd /c del /f /q`, and a full `wsl --shutdown` + retry — all failed. No further invasive remediation (reinstall, registry edits, reboot) was attempted without QA Lead direction. The QA Lead was asked directly and approved proceeding with static validation only at that time.

**Runtime re-validation (this pass):** `docker version`/`docker info` confirmed the daemon available (`Server: Docker Desktop 4.69.0`, `Engine 29.4.0`). Ran:

```
docker build -t playwright-python-hybrid-framework:v1.62.0-noble-validation .
```

from the existing project root as build context, using the existing, unmodified `Dockerfile`. **Result: build succeeded (exit code 0).** All 5 build steps completed: base-image layers, `WORKDIR /app`, `COPY pyproject.toml ./`, the `tomllib`-based dependency install (`RUN ... pip install $(python -c "import tomllib; ...")`), and `COPY . .`. The dependency-install layer output confirmed all 8 pinned packages installed at their exact pinned versions (`playwright-1.62.0`, `pytest-9.1.1`, `pytest-playwright-0.9.0`, `httpx-0.28.1`, `pytest-html-4.2.0`, `python-dotenv-1.2.3`, `pytest-xdist-3.8.0`, `pytest-rerunfailures-16.6`) — matching `pyproject.toml` exactly, confirming the `tomllib` extraction mechanism works correctly inside the container. Final image: `playwright-python-hybrid-framework:v1.62.0-noble-validation`, confirmed present via `docker images` (3.82GB disk / 1.11GB content — consistent with the size risk already disclosed in the original audit, given the base image bundles three browser engines). **Image was built locally only — not pushed to any registry (Section 18).**

## 11. Test Collection Evidence

**Obtained.** Ran inside the built container:

```
docker run --rm playwright-python-hybrid-framework:v1.62.0-noble-validation python -m pytest --collect-only -q
```

**Actual result: `50 tests collected in 0.11s`** — matching the expected count exactly, confirmed live, not assumed. `platform linux -- Python 3.12.3` in the session header confirms this genuinely executed inside the Linux container (not a Windows fallback or a stale host result).

## 12. Docker Execution Evidence

**Obtained.** Ran the container using its existing, unmodified default `CMD` (no override):

```
docker run --rm -v "E:\Real Life SQA Projects\playwright-python-hybrid-framework\reports:/app/reports" playwright-python-hybrid-framework:v1.62.0-noble-validation
```

Output confirmed the default selection is exactly `-m "regression and not ci_restricted"` on Chromium, unmodified: `collected 50 items / 28 deselected / 22 selected`. **Actual result: `22 passed, 28 deselected in 71.20s` — 0 failed.** (An initial run using a Git-Bash-style `$(pwd)` mount path also completed with the identical `22 passed, 28 deselected` result in 153.41s before the mount-path issue in Section 13 was discovered and corrected — the pass/fail outcome itself was identical and unaffected by the mount problem, since the mount only affects where the report is written, not test execution.) No `--reruns` override was needed or applied — the existing bounded-retry policy (`--reruns 2 --reruns-delay 3`, identical to all three CI platforms) remains available as a `docker run` argument override exactly as designed, but this run passed cleanly with zero failures, so it was not exercised. No test suite modification of any kind was made to obtain this result.

**Failure classification:** not applicable this run — zero failures occurred, so no Test/Application/Environment/Automation/Data classification was needed. No OBS-001-pattern connection error was observed in either container run; the public AUT was reachable and stable throughout this validation window. This is reported as a real, time-bound observation ("stable during this run"), not a claim that OBS-001 is resolved or that future runs won't encounter it (Section 15).

## 13. Report-Volume Evidence

**Obtained — with one real, disclosed finding along the way.**

An initial attempt used Git Bash's `-v "$(pwd)/reports:/app/reports"`, which expands to a Unix-style path (`/e/Real Life SQA Projects/playwright-python-hybrid-framework/reports`). **This mount silently failed to bridge to the host**: a container run that wrote a uniquely-named marker file to `/app/reports/` reported success *inside* the container, but the file never appeared on the host afterward — confirmed by direct `ls` check. This is consistent with the space in `Real Life SQA Projects` breaking Docker Desktop's path translation for a Git-Bash-style volume source.

**Corrected approach:** using an explicit Windows-style absolute host path instead — `-v "E:\Real Life SQA Projects\playwright-python-hybrid-framework\reports:/app/reports"` — a second marker-file test confirmed the file appeared on the host immediately with a fresh timestamp. The actual regression run (Section 12) was then re-run with this corrected mount syntax, and **`reports/html/report.html` on the host was confirmed updated**: file size changed from 32,792 → 52,145 bytes, modification time matched the container run's wall-clock time exactly, and the file's content was confirmed to contain `Linux` (the container's platform string) rather than the prior Windows-generated report's content. `reports/screenshots/`, `reports/traces/`, `reports/videos/` were checked and remained empty — correctly, since this run had zero test failures and Playwright only writes these artifacts for a failing test.

**Documented correction for future use:** the bind-mount syntax that reliably works on this Windows/Docker-Desktop/Git-Bash combination is the explicit Windows-style absolute path, not `$(pwd)` when the path contains spaces. No project file was changed to reflect this — it is operational/runtime guidance, not a defect in the `Dockerfile`, `.dockerignore`, or any test.

## 14. Secret/Security Verification

Static verification (performed at original implementation, independent of the daemon):

- `Dockerfile` and `.dockerignore` were both grep-scanned for credential-shaped literals (`password`, `secret`, `token`, `credential`, `DURABLE_.*=`, `api[_-]?key`) — only comments discussing the *concept* matched; zero literal secret values exist in either file.
- Confirmed `.dockerignore` excludes `.env`, `.env.local`, `.env.*.local`, and `.git/` — the actual enforcement mechanism preventing a real credential (if one ever existed on the host) from entering the build context.
- Confirmed the Dockerfile sets no `ENV`/`ARG` carrying any credential-shaped value (Section 8).

**Live image inspection (this runtime re-validation pass, now closing the gap noted above):**

- `docker history --no-trunc playwright-python-hybrid-framework:v1.62.0-noble-validation` — every layer inspected. The project-specific layers exactly match the `Dockerfile`'s 5 instructions (`WORKDIR /app`, `COPY pyproject.toml ./`, the `tomllib` `RUN pip install ...`, `COPY . .`, the `CMD`) — no hidden or unexpected layer, no injected credential in any layer command.
- `docker inspect ... --format '{{json .Config.Env}}'` → `["PATH=...", "LANG=C.UTF-8", "LC_ALL=C.UTF-8", "PLAYWRIGHT_BROWSERS_PATH=/ms-playwright"]` — all 4 inherited from the official base image; **zero** application-specific environment variables were added by this project's `Dockerfile`, confirming Section 8's "no `ENV` baked in" design was actually honored in the built artifact, not just on paper.
- Full `docker inspect` output grep-scanned for `password|secret|token|credential|DURABLE` — **none found**.
- Confirmed inside a running container (`find /app -maxdepth 1 -iname '.env*'`) that only `.env.example` exists in the image filesystem — a non-secret template with empty `DURABLE_*` values — and no real `.env` file is present, confirming `.dockerignore`'s exclusion worked as designed in the actual built image, not just in theory.

**No real credential value was found anywhere; none is displayed here, consistent with instruction (there was none to redact).**

## 15. Network/OBS-001 Classification

**Original session:** not applicable — no container execution occurred, so no network-layer failure of the `OBS-001` kind could be observed. The blocker described in Section 10's retained history was a **local Docker Desktop backend startup failure**, entirely distinct from `OBS-001` (which concerns connectivity to `automationexercise.com`) — never conflated.

**This runtime re-validation pass:** both container regression runs (Section 12) completed with **zero failures** — no `net::ERR_CONNECTION_RESET`, no `httpx` connection error, no `OBS-001`-signature failure was observed. This is reported honestly as a real, time-bound observation for this specific validation window, not as evidence that `OBS-001` is resolved — the public AUT's stability is outside this project's control and has been documented since Step 17 as intermittent, not constant. `OBS-001` itself remains unchanged, unresolved, and is not reclassified by this step. Had a connection-layer failure occurred during either container run, it would have been classified exactly as `OBS-001` already is — Environment, not AUT/Automation/Docker — per instruction; that classification simply was not exercised this pass because no such failure occurred.

## 16. Files Created

1. `Dockerfile` (repo root)
2. `.dockerignore` (repo root)
3. `docs/20-Dockerization.md` (this document)

No other file was created.

## 17. Files Explicitly Confirmed Unchanged

Verified via file-modification timestamps (identical to their pre-Step-20 state) and `git status`/`git diff` where applicable:

- `docs/01-Project-Vision.md` through `docs/19-CI-CD.md` — all 19 files, timestamps unchanged.
- `.github/workflows/ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` — timestamps unchanged; **not opened for editing at any point this step**.
- `pyproject.toml` — timestamp unchanged.
- `src/`, `tests/` — zero edits made; `git status --short` shows no modification to any file under either directory.
- `.env.example` — untouched.
- TypeScript reference project (`playwright-typescript-hybrid-framework`) — `git status --short` returned clean.

`git status --short` in this project, at the time of writing, shows only `Dockerfile`, `.dockerignore`, and `docs/20-Dockerization.md` as new/untracked — nothing else.

## 18. Docker Registry Status

**The Docker image was not built (Section 10), and therefore was never pushed to Docker Hub, GitHub Container Registry, or any other registry.** No registry account, namespace, or credential of any kind was created, referenced, or invented.

## 19. CI/CD Integration Status

**None.** `.github/workflows/ci.yml`, `Jenkinsfile`, and `azure-pipelines.yml` were not modified to build or run this image — per explicit instruction, Docker remains a separate, additive local-execution path this step, not wired into any of the three existing pipelines. This is disclosed as a deliberate non-change, not an oversight.

## 20. Step 20 Exit Criteria

- [x] Exactly 3 files created (`Dockerfile`, `.dockerignore`, this document) — no more, no fewer
- [x] Base image tag verified against the live MCR registry API, not guessed (Section 3)
- [x] Single Dockerfile, single-stage, no docker-compose, official Playwright Python image, Chromium default (Sections 4–5)
- [x] `python -m pytest` (module form) preserved as the entry point; not replaced with bare `pytest` (Section 5)
- [x] Default command represents the existing PR-tier selection (`regression and not ci_restricted`) (Section 5)
- [x] Dependency installation reuses the exact existing `tomllib`/`pyproject.toml` mechanism; no `requirements.txt`, no `pyproject.toml` edit (Section 7)
- [x] No secret baked into the image or present in the Dockerfile/.dockerignore (Section 14)
- [x] `.dockerignore` matches the specified minimum list exactly; no unjustified extra exclusion of docs/CI/pyproject.toml (Section 6)
- [x] **Docker image built successfully — MET via runtime re-validation (Section 10): `docker build` exit code 0, image `playwright-python-hybrid-framework:v1.62.0-noble-validation` confirmed present**
- [x] **In-container test collection confirmed at 50 — MET (Section 11): `50 tests collected in 0.11s`, live output, not assumed**
- [x] **Default regression execution run and observed — MET (Section 12): `22 passed, 28 deselected, 0 failed` on the unmodified default CMD; no test suite change made**
- [x] **Report bind-mount persistence observed on the host — MET (Section 13), after correcting a real Git-Bash path-translation issue found and documented along the way; `reports/html/report.html` confirmed updated with Linux-platform content on the host**
- [x] `docs/01–19` unchanged (Section 17)
- [x] `.github/workflows/ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` unchanged (Section 17)
- [x] `pyproject.toml`, `src/`, `tests/`, `.env.example` unchanged (Section 17)
- [x] TypeScript reference project unchanged (Section 17)
- [x] No Docker image pushed to any registry (Section 18)
- [x] No CI/CD platform modified to use Docker (Section 19)
- [x] No docker-compose, no Kubernetes manifests, introduced
- [x] 46-case scope, 9 blockers, OBS-001, five-way classification, Gate 5 = PARTIAL, Gate 6 = no release approval — all preserved unchanged; nothing executed, re-executed, or reclassified
- [x] No release-readiness claim made
- [ ] QA Lead approval — still required before Step 21

**Overall status: Docker is implemented, statically validated, and now live-validated. All 4 previously-unmet live-validation criteria were closed in a runtime re-validation pass on 2026-08-25 once Docker Desktop became functional on this machine: real `docker build` (success), real in-container `--collect-only` (50 tests), real default-CMD execution (22/22 passed, 0 failures), and real host report persistence (confirmed after correcting a genuine Git-Bash volume-mount path issue, documented in Section 13). The image was built and run locally only — never pushed to any registry (Section 18) — and none of the three existing CI/CD platforms were modified to use it (Section 19).**

## 21. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete (static scope) — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete (static validation) / Live validation deferred — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 21. Live Docker build/execution validation remains an open item to close before this step can be considered fully, not just statically, complete.
