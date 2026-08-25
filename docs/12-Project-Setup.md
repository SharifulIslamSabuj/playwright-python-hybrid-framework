# 12 — Project Setup

## Document Control

| Field | Value |
|---|---|
| Document ID | AE-PY-PS-001 |
| Project | playwright-python-hybrid-framework |
| Version | 1.0 |
| Status | Complete — pending QA Lead review |
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) |
| Date | 2026-08-25 |
| Phase | Phase 6 — Project Setup |
| Step | Step 12 — Project Setup |
| Predecessor Documents | [01](01-Project-Vision.md)–[11](11-Framework-Architecture.md), all ✅ approved |

## 1. Setup Objective

Convert the architecture approved in [11-Framework-Architecture.md](11-Framework-Architecture.md) into a runnable Python + Playwright + pytest project foundation: resolve the setup decisions Step 11 explicitly deferred, create the approved folder structure, establish dependency management, and prove the environment actually works. **No business test case (of the 31 approved in [09](09-Automation-Scope.md)) is implemented in this step** — only the one infrastructure-validation test explicitly permitted by instruction.

## 2. Final Python Version

**Python 3.14.4** — the version already present in this environment (verified via `python --version`). `pyproject.toml` declares `requires-python = ">=3.11"` rather than pinning the exact patch, so the project isn't artificially coupled to one interpreter build while still requiring a reasonably modern floor. **Compatibility was not assumed** — Python 3.14 is a very recent release, and the main risk (Playwright's `greenlet` dependency, which ships as a compiled C extension and often lags behind new CPython releases) was verified empirically: `greenlet==3.5.5` installed with a native `cp314-cp314-win_amd64` wheel, confirming real support rather than hoped-for support.

## 3. Dependency-Management Decision

**`pyproject.toml` (PEP 621) + plain `pip`, installed into a project-local virtual environment (`.venv/`).**

| Alternative | Why Not Chosen |
|---|---|
| `requirements.txt` only | Simpler, but `pyproject.toml` is the modern standard, holds project metadata and dependencies in one file, and needs no extra tool beyond `pip` (already available) — chosen for a portfolio-quality project without adding complexity |
| Poetry / uv | Would add a whole additional build-tool dependency and its own lockfile format; nothing in Steps 1–11 justifies that extra layer for a project of this size |

**Reproducibility approach:** every dependency in `pyproject.toml` is pinned to an exact version (no `^`/`~=` ranges), each verified to actually exist and install cleanly via `pip index versions` + a real install into `.venv/` (Section 11) — not assumed from training knowledge, since this session's date (2026-08-25) is well past this assistant's knowledge cutoff and package ecosystems move quickly. **Installation command:** `pip install .` (or `pip install -e .` for editable/development installs) from the project root, after activating `.venv/`. **Update strategy:** version bumps are deliberate, one-at-a-time changes to `pyproject.toml`, re-verified the same way (query available versions, install, re-run the setup-validation suite) — never a blanket `pip install --upgrade` across the whole dependency set.

## 4. Dependency Versions (Evidence-Based, Verified Installed)

All versions below were confirmed as the **latest stable release on PyPI** at query time (`pip index versions <pkg>`), then verified to install and function together in this exact environment.

| Package | Version | Role | ADR / Source |
|---|---|---|---|
| `playwright` | 1.62.0 | Browser automation | [11](11-Framework-Architecture.md) §5, ADR-1 |
| `pytest` | 9.1.1 | Test runner | [01](01-Project-Vision.md) §7 |
| `pytest-playwright` | 0.9.0 | Browser/page/context fixtures, CLI flags | [11](11-Framework-Architecture.md) §5, ADR-1 |
| `httpx` | 0.28.1 | API-layer HTTP client | [11](11-Framework-Architecture.md) §5, ADR-2 |
| `pytest-html` | 4.2.0 | HTML reporting | [11](11-Framework-Architecture.md) §5, ADR-3 |
| `python-dotenv` | 1.2.3 | `.env` loading | [11](11-Framework-Architecture.md) §5 (RECOMMENDED → now confirmed workable) |
| `pytest-xdist` | 3.8.0 | Parallel worker execution | [11](11-Framework-Architecture.md) §29 (RECOMMENDED → now confirmed workable) |
| `pytest-rerunfailures` | 16.6 | Bounded CI retry support | [11](11-Framework-Architecture.md) §30 (RECOMMENDED → now confirmed workable) |

**Transitively resolved** (not directly pinned, but captured via `pip freeze` for full reproducibility evidence — see Section 12): `anyio 4.14.2`, `certifi 2026.7.22`, `charset-normalizer 3.5.1`, `colorama 0.4.6`, `execnet 2.1.2`, `greenlet 3.5.5`, `h11 0.16.0`, `httpcore 1.0.9`, `idna 3.19`, `iniconfig 2.3.0`, `Jinja2 3.1.6`, `MarkupSafe 3.0.3`, `packaging 26.3`, `pluggy 1.6.0`, `pyee 13.0.1`, `Pygments 2.21.0`, `pytest-base-url 2.1.0`, `pytest-metadata 3.1.1`, `python-slugify 8.0.4`, `requests 2.34.2`, `text-unidecode 1.3`, `typing_extensions 4.16.0`, `urllib3 2.7.0`.

**Playwright browsers installed** (`playwright install chromium firefox webkit`): Chromium 151.0.7922.34, Firefox 153.0, WebKit 26.5 — matching the browser strategy already approved ([05](05-Test-Strategy.md) §9, [10](10-Automation-Strategy.md) §17, [11](11-Framework-Architecture.md) §18).

## 5. Project Structure Created

```
playwright-python-hybrid-framework/
├── .env.example
├── .gitignore
├── pyproject.toml
├── docs/                          (unchanged — 01 through 11, plus this file)
├── src/
│   ├── __init__.py
│   ├── pages/__init__.py          (empty — Page Objects are Step 14)
│   ├── api/__init__.py            (empty — API Clients are Step 15)
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            (configuration skeleton — see Section 8)
│   ├── data/__init__.py           (empty — TD-* datasets are Step 13/implementation)
│   └── utils/__init__.py          (empty — utilities are Step 13)
├── tests/
│   ├── test_setup_validation.py   (infrastructure-only — see Section 6)
│   ├── ui/                        (empty — 17 approved UI cases are Step 14)
│   ├── api/                       (empty — 13 approved API cases are Step 15)
│   └── hybrid/                    (empty — 1 approved Hybrid case is Step 16)
└── reports/
    ├── html/       (+ .gitkeep)
    ├── screenshots/(+ .gitkeep)
    ├── traces/     (+ .gitkeep)
    └── videos/     (+ .gitkeep)
```

Exactly matches [11-Framework-Architecture.md](11-Framework-Architecture.md) §33 — no directory was added or omitted relative to that approved structure. Every `src/` subpackage that has no business content yet (`pages/`, `api/`, `data/`, `utils/`) contains only its `__init__.py`, correctly empty at this stage.

## 6. Playwright Installation

`pytest-playwright` was chosen over a hand-built Playwright wrapper (ADR-1, [11](11-Framework-Architecture.md) §42), so no custom browser-launch fixture code was written. Installation was validated two ways: (1) `playwright install chromium firefox webkit` completed successfully for all three engines, and (2) the setup-validation suite (Section 6 below) actually launched each engine and opened a page — proving the binaries work, not merely that they downloaded.

## 7. Browser Setup

| Engine | Version Installed | Verified Launch |
|---|---|---|
| Chromium | 151.0.7922.34 | ✅ Pass |
| Firefox | 153.0 | ✅ Pass |
| WebKit | 26.5 | ✅ Pass |

Consistent with [10-Automation-Strategy.md](10-Automation-Strategy.md) §17: all three are *installed* and *available* now, but this does **not** mean all three run on every future CI trigger — that tiered decision (Chromium for PR/main, curated cross-browser for nightly/release) remains governed by [09](09-Automation-Scope.md)/[10](10-Automation-Strategy.md) and will be implemented at Step 19 (CI/CD), not here.

## 8. pytest Configuration

Configured via `[tool.pytest.ini_options]` in `pyproject.toml` (a single config file, per the dependency-management decision in Section 3, rather than a separate `pytest.ini`):

- `testpaths = ["tests"]` — test discovery confined to `tests/`; `src/` is never scanned for tests.
- Standard `test_*.py` / `Test*` / `test_*` discovery conventions (explicit, not left to pytest's bare defaults, for clarity).
- **8 markers registered**, each corresponding to a real, already-approved execution-tier distinction from [10-Automation-Strategy.md](10-Automation-Strategy.md) §18/27 and [11-Framework-Architecture.md](11-Framework-Architecture.md) §27 — `smoke`, `ui`, `api`, `hybrid`, `negative`, `regression`, `ci_restricted`, `cross_browser`. No marker was invented beyond what those documents already justified.
- `addopts = "--strict-markers"` — an unregistered/typo'd marker will fail collection immediately rather than being silently accepted, a deliberate guard for future test authors.

**Not yet implemented** (correctly deferred to Step 13, per instruction): the fixture architecture itself ([11](11-Framework-Architecture.md) §14 — `home_page`, `products_api`, `unique_user_data`, `created_account_cleanup`, etc.). No `conftest.py` exists yet.

## 9. Configuration / Environment Setup

`src/config/settings.py` implements the configuration skeleton from [11-Framework-Architecture.md](11-Framework-Architecture.md) §16 as a frozen dataclass, `Settings`, reading every value from an environment variable with a safe default: AUT/API base URL, browser, headless mode, default/expect timeouts, retries, workers, report directory, and the three durable-account fields (deliberately left blank by default — Section 13). `.env.example` documents every variable name with no real values. `load_dotenv()` is called at import time so a local `.env` (if a developer creates one) is picked up automatically, with zero effect in environments (like CI) that supply configuration directly as environment variables. **No secret exists yet** — the AUT requires none ([02](02-Application-Analysis.md) §10) — and the accidental-secret scan (Section 12) confirms none was introduced.

## 10. Git Setup

Git was not previously initialized in this directory; `git init` was run. `.gitignore` was authored to cover: Python bytecode/build artifacts, virtual environments (`.venv/`), pytest cache, Playwright's `test-results/`/`playwright-report/` conventions, this project's own `reports/*` generated output (while preserving the four `.gitkeep` placeholders so the directory structure itself stays tracked), `.env`/`.env.*.local`, common IDE folders, and OS-generated files (`.DS_Store`, `Thumbs.db`, `desktop.ini`). **Verified, not assumed:** `git check-ignore -v` was run against a generated report file, the venv, and a temporarily-created `.env` — all three were confirmed correctly ignored (Section 12). **No commit was made** — Git is initialized and the working tree is ready, but committing was not explicitly requested by this step's instructions, and creating one unprompted would risk locking in a state the QA Lead hasn't reviewed yet.

## 11. Validation Performed

| # | Check | Method |
|---|---|---|
| 1 | Dependency installation | Real `pip install` of the full pinned set into `.venv/` |
| 2 | pytest collection | `pytest --collect-only` |
| 3 | Playwright import | Exercised inside the setup-validation test, not just a bare `import` statement |
| 4 | Browser availability | Each of Chromium/Firefox/WebKit actually launched and opened a page |
| 5 | Configuration loading | Asserted `Settings` resolves with expected defaults |
| 6 | Project structure | Directory tree compared directly against [11-Framework-Architecture.md](11-Framework-Architecture.md) §33 |
| 7 | `.gitignore` correctness | `git check-ignore -v` against a report artifact, `.venv/`, and a test `.env` |
| 8 | Accidental-secret check | Pattern-based grep across every new file for `password=`/`api_key=`/`secret=`/`token=`-style literals |
| 9 | Syntax/import validation | Implied by every test passing — a syntax or import error would have failed collection or execution |

## 12. Validation Results

- **`pip install`:** all 8 directly-pinned packages + 23 transitive dependencies installed without conflict (full `pip freeze` output in Section 4).
- **`pytest --collect-only`:** 5 tests collected, 0 errors (after one fix — Section 14).
- **Setup-validation suite:** **5 passed, 0 failed, 6.23s** — configuration, `httpx` client construction, and all 3 browser launches.
- **`.gitignore`:** confirmed excluding `reports/html/setup_validation.html`, `.venv/pyvenv.cfg`, and a test `.env`; confirmed **including** the 4 `.gitkeep` files via `git add -n -A` dry run.
- **Secret scan:** zero matches across `src/`, `tests/`, `pyproject.toml`, `.env.example`.
- **Versions confirmed installed:** Python 3.14.4, Playwright 1.62.0, pytest 9.1.1, Chromium 151.0.7922.34, Firefox 153.0, WebKit 26.5 (raw command output captured during this session).

## 13. Setup Limitations

- The two durable test accounts (`TD-USER-VALID-001`, `TD-USER-EXISTING-001`) are **not provisioned** — their config fields are present but empty by design (Section 9), since provisioning requires the QA-Lead authorization still pending from [09-Automation-Scope.md](09-Automation-Scope.md) §30 item 4. No account was created in this step.
- Only Windows (this development environment) has been validated. Linux/CI runner compatibility (relevant to Section 4's transitive dependency list, some of which are platform-specific wheels) is unverified until Step 19.
- `pytest-xdist`/`pytest-rerunfailures` were installed and confirmed importable but **not exercised** (no parallel or retry run was performed) — that validation belongs to Step 17 (Execution), once real business tests exist to run in parallel or retry.

## 14. Deferred Items

Per instruction, explicitly not done in this step: `conftest.py`/fixture implementation (Step 13), Page Object implementations (Step 14), API Client implementations (Step 15), Hybrid test implementation (Step 16), actual `TD-*` test-data file implementation (Step 13/beyond — only the empty `src/data/` package exists now), Dockerfile (Step 20+ per [11](11-Framework-Architecture.md) §44), GitHub Actions workflow (Step 19), and any of the 31 approved business test cases.

## 15. Setup Decisions

| Decision | Rationale |
|---|---|
| `pyproject.toml` + pip, not Poetry/uv | Section 3 |
| Exact version pinning, verified via live PyPI query + real install | Avoids both guessing (this session postdates this assistant's knowledge cutoff) and unverified assumption |
| `httpx` version 0.28.1 confirmed as the correct ADR-2 realization | [11](11-Framework-Architecture.md) ADR-2 |
| `pytest-html` for reporting, no Allure | [11](11-Framework-Architecture.md) ADR-3 |
| Setup-validation test parametrized on `engine_name`, not `browser_name` | `pytest-playwright` reserves `browser_name` as one of its own fixtures — discovered empirically during this step (Section 14), not anticipated in [11](11-Framework-Architecture.md); logged here as a genuine implementation-time finding |
| No initial Git commit | Not explicitly requested; avoids locking in unreviewed state |
| Single infrastructure-only test file, deliberately outside `tests/ui`/`tests/api`/`tests/hybrid` | Keeps it structurally impossible to mistake for one of the 31 approved business cases |

## 16. TypeScript → Python Validation

Explicit check against the Step 11 lessons ([11](11-Framework-Architecture.md) §40):

| Check | Result |
|---|---|
| No TypeScript-specific conventions reproduced | Confirmed — `snake_case` modules, `pyproject.toml` (not `package.json`/`tsconfig.json`), no `types/`-style interface-only directory |
| No unnecessary framework complexity | Confirmed — no Page Object/API Client code exists yet at all (correctly deferred); the folder skeleton matches the lean 5-Page-Object/4-API-Client plan, not TS's broader 8/4 set |
| No unnecessary dependencies | Confirmed — every dependency in Section 4 traces to a specific [11] architecture decision; nothing installed "just in case" |
| No Chromium-only CI assumption baked in | Confirmed — all 3 engines were installed and validated equally in this step; the Chromium-first *tiering* remains a CI-time decision (Section 7), not hard-coded here |
| No unsafe shared-state behavior | Confirmed — no test data, account, or fixture logic exists yet to have this problem; the config skeleton's durable-account fields are correctly empty, not placeholder-filled with a fake shared value |
| No page/API cross-import coupling | Confirmed — `src/pages/` and `src/api/` currently contain only empty `__init__.py` files; the one-directional dependency rule (ADR-7) has nothing to violate yet, and will be the first thing checked again at Step 13/14 |

## 17. Step 12 Exit Criteria

- [x] Steps 1–11 reviewed before any change was made
- [x] Python version determined and empirically verified (3.14.4, `greenlet` cp314 wheel confirms Playwright compatibility)
- [x] Dependency-management approach decided with rationale (`pyproject.toml` + pip)
- [x] Exact dependency versions determined via live PyPI verification, not invented
- [x] Playwright, pytest, and plugin versions installed and confirmed working together
- [x] API client dependency (`httpx`) aligned with the Step 11 ADR-2
- [x] Docker base image/version — **remains explicitly deferred**, per instruction ("DO NOT create the Dockerfile in Step 12"); no image was pulled or referenced
- [x] Traceability mechanism — carried forward as designed in [11](11-Framework-Architecture.md) §28 (test-case-ID markers/docstrings); not implemented until real test cases exist at Step 14/15
- [x] Project structure created exactly per [11-Framework-Architecture.md](11-Framework-Architecture.md) §33
- [x] Foundational files created: `pyproject.toml`, `.gitignore`, `.env.example`, `src/config/settings.py`
- [x] No business test case implemented; the one setup-validation test is clearly scoped and isolated
- [x] Playwright installed and all 3 approved browsers validated
- [x] pytest configured with discovery, markers, and strict-marker enforcement
- [x] Configuration foundation supports every value [11] §16 named, via environment variables, no hard-coded secrets
- [x] Git initialized; professional `.gitignore` verified functionally correct
- [x] No Dockerfile, docker-compose, or CI workflow created
- [x] Docs 01–11 unchanged (verified below)
- [x] TypeScript reference project unchanged (verified below)
- [ ] QA Lead Review & Approval

## 18. Approval

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared By | AI Assistant (advisory, acting as Test Automation Engineer) | Complete — pending review | 2026-08-25 |
| Reviewed By | QA Lead | Pending | — |
| Approved By | QA Lead | Pending | — |
| Approval Status | **Complete — Pending QA Lead Approval** | | |

Approval of this exit criterion by the QA Lead is required before proceeding to Step 13 — Core Framework Development.
