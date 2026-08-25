# Dockerfile — additive Dockerization of the existing Python + Playwright +
# Pytest hybrid framework (docs/20-Dockerization.md). Provides a reproducible
# local execution environment for the SAME 22 currently implemented,
# approved automated Test Cases the three existing CI/CD platforms already
# run — this is not a second test framework and does not change any test
# logic, locator, assertion, or the approved automation scope.
#
# Base image verified against the actual Microsoft Container Registry tag
# list (mcr.microsoft.com/v2/playwright/python/tags/list) before use, per
# instruction — not guessed. playwright==1.62.0 is pinned exactly in
# pyproject.toml; v1.62.0-noble (Ubuntu 24.04 LTS) is confirmed published
# and bundles matching Chromium/Firefox/WebKit binaries pre-installed, so
# no separate `playwright install` step is needed (docs/20-Dockerization.md
# §3/§5).
FROM mcr.microsoft.com/playwright/python:v1.62.0-noble

# WORKDIR is the directory the project's absolute imports (from src.pages...)
# resolve against once `python -m pytest` inserts it onto sys.path — the
# exact same mechanism already relied on locally and in all three existing
# CI/CD platforms (docs/19-CI-CD.md §9). Any WORKDIR name works as long as
# it is where src/ and tests/ end up; /app is a plain, conventional choice.
WORKDIR /app

# pyproject.toml is copied first, as its own layer, purely for Docker build
# cache efficiency (a source-only change does not force dependencies to
# reinstall) — a standard Docker practice, not a change to the project's
# dependency source of truth.
COPY pyproject.toml ./

# No [build-system] table exists in pyproject.toml (the project is not
# packaged/installable — docs/12-Project-Setup.md), so dependencies are
# installed directly from [project.dependencies] using the stdlib tomllib
# (Python 3.11+) — the identical single-source-of-truth technique already
# used, unmodified, by .github/workflows/ci.yml, Jenkinsfile, and
# azure-pipelines.yml. No requirements.txt is created; pyproject.toml is not
# modified.
RUN python -m pip install --upgrade pip \
    && pip install $(python -c "import tomllib; print(' '.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")

# Full project source. .dockerignore excludes .git/, .venv/, .env and other
# host-only/secret-shaped files — no credential ever enters the build
# context, let alone the image (docs/20-Dockerization.md §9).
COPY . .

# No environment variable is set here: AUT_BASE_URL/API_BASE_URL are public,
# non-secret URLs whose defaults already live in src/config/settings.py
# (os.getenv(..., "https://automationexercise.com")) — duplicating them here
# would be exactly the kind of unnecessary duplication the project avoids
# elsewhere. Runtime configuration remains fully environment-injected via
# `docker run -e VAR=value` / `--env-file`; the durable-account credentials
# (docs/09-Automation-Scope.md §12/§30 item 4) are never baked in and are
# not consumed by any of the 22 currently implemented tests regardless.

# Default command: the same PR-tier selection every existing CI/CD platform
# already runs by default (docs/11-Framework-Architecture.md §32 explicitly
# specifies this as Docker's default; docs/19-CI-CD.md §6). Chromium is the
# default browser via pyproject.toml's own addopts (--browser=chromium) —
# not repeated here, since duplicating that would contradict the "do not
# duplicate configuration that already exists in pyproject.toml" instruction.
# `python -m pytest`, not bare `pytest`, preserving the exact import
# resolution mechanism this project depends on. Overridable at `docker run`
# time exactly like the TS reference project's own cited "override at
# docker run time" pattern — e.g. to select the cross_browser tier or a
# different --browser engine.
CMD ["python", "-m", "pytest", "-m", "regression and not ci_restricted"]
