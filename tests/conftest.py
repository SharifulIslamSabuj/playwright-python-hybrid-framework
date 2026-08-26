"""Framework fixtures.

Implements docs/11-Framework-Architecture.md §14 (Fixture Architecture).
Browser/context/page lifecycle is intentionally NOT reimplemented here —
`pytest-playwright` already provides the `page` fixture (ADR-1,
docs/11 §5/§42); this file only adds the fixtures the architecture layers
on top of it.

Fixture scopes follow docs/11 §14 exactly: function-scoped by default
(isolation over speed, given the shared public AUT — docs/10-Automation-
Strategy.md §8/§21), session-scoped only for genuinely stateless/read-only
resources (the API clients themselves, and the durable accounts' *data*,
never mutable state).

Contains no test assertions and no business Test Case logic — only setup/
teardown plumbing, per docs/11 §7 (fixtures depend on Page Objects/API
Clients, not the other way around).
"""

from __future__ import annotations

import dataclasses
import os
import re
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from src.api.auth_api_client import AuthApiClient
from src.api.brands_api_client import BrandsApiClient
from src.api.products_api_client import ProductsApiClient
from src.config.settings import Settings, settings as _settings
from src.data.models import NewUserPayload
from src.data.users import DataMode, build_new_user_payload, build_user_data
from src.pages.cart_page import CartPage
from src.pages.home_page import HomePage
from src.pages.product_details_page import ProductDetailsPage
from src.pages.products_page import ProductsPage
from src.pages.signup_login_page import SignupLoginPage
from src.utils.logger import get_logger

_logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Configuration access
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Expose the centralized configuration singleton to tests/fixtures
    that prefer requesting it as a fixture over importing it directly."""
    return _settings


# ---------------------------------------------------------------------------
# Page Object fixtures (function-scoped: depend on the function-scoped
# `page` fixture supplied by pytest-playwright)
# ---------------------------------------------------------------------------


@pytest.fixture
def home_page(page: Any) -> HomePage:
    return HomePage(page)


@pytest.fixture
def signup_login_page(page: Any) -> SignupLoginPage:
    return SignupLoginPage(page)


@pytest.fixture
def products_page(page: Any) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def product_details_page(page: Any) -> ProductDetailsPage:
    return ProductDetailsPage(page)


@pytest.fixture
def cart_page(page: Any) -> CartPage:
    return CartPage(page)


# ---------------------------------------------------------------------------
# API client fixtures (session-scoped: stateless wrappers, safe to reuse —
# docs/11-Framework-Architecture.md §14)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def products_api() -> Generator[ProductsApiClient, None, None]:
    client = ProductsApiClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def brands_api() -> Generator[BrandsApiClient, None, None]:
    client = BrandsApiClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_api() -> Generator[AuthApiClient, None, None]:
    client = AuthApiClient()
    yield client
    client.close()


# ---------------------------------------------------------------------------
# Test data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def unique_user_data(request: pytest.FixtureRequest) -> NewUserPayload:
    """A freshly generated TD-USER-NEW-*-shaped payload (docs/08-Test-Data.md
    §7), tagged with the requesting test's name for traceability
    (docs/11-Framework-Architecture.md §28). Produces data only — creates no
    account (see src/data/users.py)."""
    return build_new_user_payload(scenario=request.node.name)


@pytest.fixture(scope="session")
def durable_valid_account(settings: Settings) -> dict[str, str]:
    """TD-USER-VALID-001 (docs/08-Test-Data.md §7): a pre-provisioned,
    reusable account. Skips any dependent test with a clear message if the
    account has not yet been provisioned — provisioning requires QA Lead
    authorization not yet granted (docs/09-Automation-Scope.md §12/§30
    item 4), so this fixture must never invent a value."""
    if not settings.has_durable_valid_account():
        pytest.skip(
            "TD-USER-VALID-001 is not provisioned (DURABLE_VALID_USER_EMAIL/"
            "PASSWORD unset) — see docs/09-Automation-Scope.md §30 item 4."
        )
    return {
        "email": settings.durable_valid_user_email,
        "password": settings.durable_valid_user_password,
    }


@pytest.fixture(scope="session")
def durable_existing_account(settings: Settings) -> str:
    """TD-USER-EXISTING-001 (docs/08-Test-Data.md §7): a durable, known-
    already-registered email used only for the duplicate-registration
    negative case. Same provisioning dependency as `durable_valid_account`."""
    if not settings.has_durable_existing_account():
        pytest.skip(
            "TD-USER-EXISTING-001 is not provisioned (DURABLE_EXISTING_USER_EMAIL "
            "unset) — see docs/09-Automation-Scope.md §30 item 4."
        )
    return settings.durable_existing_user_email


@pytest.fixture(scope="session")
def account_creation_authorized(settings: Settings) -> None:
    """Gates AE-UI-TC-004 and (transitively, via `shared_registered_account`
    below) every account-dependent Test Case — the ones that actually
    create or delete a real account, as opposed to reading/logging into one
    that already exists (see `durable_valid_account` above).

    Session-scoped, not function-scoped: `shared_registered_account` below
    is itself session-scoped (one account for the whole session) and would
    raise pytest's ScopeMismatchError if it depended on a narrower-scoped
    fixture (VERIFIED — this exact error was hit and fixed during the
    account-lifecycle refactor). Safe to widen: this fixture only reads
    `settings` (already session-scoped) and calls `pytest.skip()`, neither
    of which depends on per-test state.

    Skips with a clear, documented reason unless
    ACCOUNT_CREATION_EXECUTION_AUTHORIZED is explicitly set to true in the
    executing environment (docs/09-Automation-Scope.md §12/§30 item 4).
    This is a human operator's own environment configuration; this
    project's AI assistant never sets it — per docs/07-Test-Cases.md
    AE-API-TC-011's own recorded statement, "this assistant does not
    perform account creation unilaterally." Never invent or default this
    to true."""
    if not settings.has_account_creation_execution_authorization():
        pytest.skip(
            "Account creation/deletion execution is not authorized in this "
            "environment (ACCOUNT_CREATION_EXECUTION_AUTHORIZED unset) — see "
            "docs/09-Automation-Scope.md §12/§30 item 4 and "
            "docs/07-Test-Cases.md AE-API-TC-011."
        )


# ---------------------------------------------------------------------------
# Shared account-lifecycle fixture
#
# `durable_valid_account`/`durable_existing_account` above remain fully
# defined and usable — they are not obsolete as a *capability* (a human
# operator may still prefer pointing tests at a real, durably-provisioned
# account), but they are no longer what AE-UI-TC-005/007/008/021 and
# AE-API-TC-007/014 consume. Those 6 cases, plus AE-API-TC-011/012, now
# share ONE account created once per test session, per the account-
# lifecycle architecture requirement: create once → reuse across every
# dependent test → delete last. `account_creation_authorized` is NOT
# obsolete either — it is still the sole real-account-mutation gate, now
# guarding this fixture instead of guarding TC-004/API-011/012 individually.
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class SharedAccountState:
    """The single account AE-UI-TC-005/007/008/021, AE-API-TC-007/011/012/014
    share for the duration of one test session. `create_response` lets
    AE-API-TC-011 make a genuine assertion about the creation this fixture
    performed, without AE-API-TC-011 having to perform the creation itself
    (it already happened, once, the first time any dependent test requested
    this fixture) — the same "fixture performs the mechanical action, the
    Test Case makes its own real assertion on the recorded result" split
    already used by `pytest_runtest_makereport` elsewhere in this file.
    `deleted` lets AE-API-TC-012 signal it already performed the real
    deletion, so this fixture's own teardown (the unconditional safety net,
    same pattern as `created_account_cleanup`) does not attempt a second,
    redundant delete call."""

    payload: NewUserPayload
    create_response: Any
    deleted: bool = False


@pytest.fixture(scope="session")
def shared_registered_account(
    auth_api: AuthApiClient, account_creation_authorized: None
) -> Generator[SharedAccountState, None, None]:
    """Creates exactly one real account (FULL_DYNAMIC-generated data, via
    `build_user_data` — no hard-coded credentials) the first time any
    dependent test requests it in this session, via the real `createAccount`
    API (not the UI — API creation is the reliable, fast foundation shared
    by both UI- and API-layer dependent tests). Session-scoped, so every
    Test Case that requests it across both tests/ui/ and tests/api/ receives
    the SAME account — this is what lets AE-UI-TC-005/007/021,
    AE-API-TC-007/014 log into a real identity without needing a durable,
    human-provisioned one, and what lets AE-UI-TC-008 use a genuinely
    already-registered email.

    Teardown deletes the account exactly once, at the very end of the
    session, unless AE-API-TC-012 already performed the real deletion
    itself (see `SharedAccountState.deleted`) — this fixture's own delete
    call is an unconditional safety net (docs/10-Automation-Strategy.md
    §35), not the primary mechanism; see `pytest_collection_modifyitems`
    below for what orders AE-API-TC-012 to run last among the tests that
    depend on this fixture.

    Gated by `account_creation_authorized`, unchanged — this fixture
    performs real account creation, so the same authorization control
    still applies (see that fixture's own docstring)."""
    payload = build_user_data("shared_account_session", DataMode.FULL_DYNAMIC)
    create_response = auth_api.create_account(payload)
    state = SharedAccountState(payload=payload, create_response=create_response)
    yield state
    if not state.deleted:
        try:
            response = auth_api.delete_account(payload["email"], payload["password"])
            _logger.info(
                "Session cleanup: deleted shared account %s -> HTTP %s",
                payload["email"], response.status_code,
            )
        except Exception:
            _logger.exception(
                "Session cleanup FAILED for shared account %s — requires manual follow-up",
                payload["email"],
            )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Orders the shared-account lifecycle correctly across modules, which
    plain pytest file/definition-order collection cannot guarantee on its
    own (tests/api/ and tests/ui/ collect as separate modules): the
    account-creating test (AE-API-TC-011) must run before every other test
    that consumes `shared_registered_account`, and the account-deleting
    test (AE-API-TC-012) must run after all of them — the "create once, use
    by many, delete last" lifecycle this architecture requires.

    A stable sort keyed by lifecycle phase: any item NOT using
    `shared_registered_account` is phase 1 (unaffected — Python's stable
    sort preserves its original relative position among other phase-1
    items, so no unrelated test's ordering changes)."""

    def _phase(item: pytest.Item) -> int:
        if "shared_registered_account" not in getattr(item, "fixturenames", ()):
            return 1
        if item.name.startswith("test_ae_api_tc_011_create_account"):
            return 0
        if item.name.startswith("test_ae_api_tc_012_delete_account"):
            return 2
        return 1

    items.sort(key=_phase)


# ---------------------------------------------------------------------------
# Cleanup fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def created_account_cleanup(auth_api: AuthApiClient) -> Generator[list[dict[str, str]], None, None]:
    """Guarantees deletion of any account a test registers here, even if the
    test itself fails — closing the risk named in docs/10-Automation-
    Strategy.md §35 ("if cleanup ever fails silently...") structurally
    rather than relying on a per-test try/finally (ADR-6, docs/11 §42).

    Usage: a future business Test Case creates an account, then appends
    {"email": ..., "password": ...} to this fixture's yielded list. Nothing
    in this fixture itself creates or deletes an account unless a test
    explicitly registers one — it performs no AUT interaction on its own.
    """
    created: list[dict[str, str]] = []
    yield created
    for account in created:
        try:
            response = auth_api.delete_account(account["email"], account["password"])
            _logger.info(
                "Cleanup: deleted account %s -> HTTP %s", account["email"], response.status_code
            )
        except Exception:
            # Never re-raise from teardown: a cleanup failure must not mask
            # a genuine assertion failure that already occurred earlier in
            # the test (matches the TS project's own AE-TC-API-007 pattern,
            # docs/05-Test-Strategy.md §29 REFERENCE KNOWLEDGE).
            _logger.exception("Cleanup FAILED for account %s — requires manual follow-up", account["email"])


# ---------------------------------------------------------------------------
# Reporting & Observability (docs/21-Reporting-Observability.md, implementing
# the two docs/10-Automation-Strategy.md §25 requirements the baseline
# pytest-html/pytest-metadata setup did not yet satisfy: Test Case ID
# traceability visible in the report, and execution-platform/environment
# metadata identifying which CI tier/trigger produced a given report).
#
# Hook APIs verified directly against the installed packages' own source
# (.venv/Lib/site-packages/pytest_html/hooks.py,
# .venv/Lib/site-packages/pytest_metadata/hooks.py) rather than assumed.
# No test file is modified, and no existing docstring is rewritten — these
# hooks only read what each test already documents (docs/11 §28's existing
# "Test Case: AE-*-TC-*" docstring convention).
# ---------------------------------------------------------------------------

_TEST_CASE_ID_PATTERN = re.compile(r"Test Case:\s*(AE-[\w-]*?TC-\d+)")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, Any, None]:
    """Captures each test's Test Case ID (parsed from its existing docstring)
    onto the report object, so `pytest_html_results_table_row` below can
    render it without re-parsing source at report-generation time. Runs for
    every collected item, including the 2 infrastructure test files that
    carry no `AE-*-TC-*` docstring — those simply produce no match, handled
    gracefully as an empty string (rendered as "N/A" in the row hook), never
    an error."""
    outcome = yield
    report = outcome.get_result()
    docstring = getattr(getattr(item, "function", None), "__doc__", None) or ""
    match = _TEST_CASE_ID_PATTERN.search(docstring)
    report.test_case_id = match.group(1) if match else ""


def pytest_html_results_table_header(cells: list[str]) -> None:
    """Adds a 'Test Case ID' column immediately after the existing 'Test'
    column (index 2 of the 4 default columns: Result, Test, Duration,
    Links — verified against pytest_html/report_data.py's own default
    header list, not assumed)."""
    cells.insert(2, "<th>Test Case ID</th>")


_ARTIFACT_ROOT = Path("reports/artifacts")
_HTML_REPORT_DIR = Path("reports/html")


def _normalize(text: str) -> str:
    """Lowercase, alphanumeric-only normalization — used to match a pytest
    nodeid against a pytest-playwright artifact folder name without
    depending on pytest-playwright's own private slugification algorithm
    (per instruction). Empirically verified: pytest-playwright's folder name
    is the nodeid with every separator character (/, ::, ., _, [, ]) replaced
    by '-' — stripping all non-alphanumeric characters from both sides
    yields the same string regardless of which separator character it used."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _find_artifact_dir(nodeid: str) -> Path | None:
    """Locates the artifact directory pytest-playwright wrote for this test
    under the configured --output directory (reports/artifacts, per
    pyproject.toml), using the robust normalization above rather than any
    private internal. Returns None if no matching directory exists —
    handled gracefully by the caller, never raised."""
    if not _ARTIFACT_ROOT.is_dir():
        return None
    target = _normalize(nodeid)
    for candidate in _ARTIFACT_ROOT.iterdir():
        if not candidate.is_dir():
            continue
        normalized_candidate = _normalize(candidate.name)
        if normalized_candidate == target or target.startswith(normalized_candidate):
            return candidate
    return None


def pytest_html_results_table_row(report: pytest.TestReport, cells: list[str]) -> None:
    """Renders the Test Case ID captured above into the corresponding row
    cell, at the same index the header hook inserted its column. Gracefully
    shows 'N/A' for the 2 infrastructure test files (no business Test Case
    ID applies to them) rather than failing.

    Also links any real screenshot/trace evidence pytest-playwright wrote
    for a failed test (docs/21-Reporting-Observability.md follow-up,
    identified during whole-project runtime validation: the capture
    mechanism already worked, but nothing ever linked it from the report).
    Reuses this same existing hook rather than adding a second reporting
    mechanism. Never raises — a missing/unmatched artifact directory simply
    leaves the Links column as pytest-html's own default (usually empty),
    exactly as before this change."""
    if report.failed:
        artifact_dir = _find_artifact_dir(report.nodeid)
        if artifact_dir is not None:
            links = "".join(
                f'<a href="{os.path.relpath(f, _HTML_REPORT_DIR).replace(os.sep, "/")}" '
                f'target="_blank">{f.name}</a> '
                for f in sorted(artifact_dir.iterdir())
                if f.is_file()
            )
            if links:
                cells[-1] = f'<td class="col-links">{links}</td>'

    test_case_id = getattr(report, "test_case_id", "") or "N/A"
    cells.insert(2, f'<td class="col-testcaseid">{test_case_id}</td>')


def _detect_execution_platform() -> str:
    """Derives which platform produced this run from standard environment
    signals each platform injects automatically, with no change to any of
    the three existing CI/CD files or the Dockerfile:
      - GitHub Actions always sets `GITHUB_ACTIONS=true` (GitHub Docs,
        "Variables reference").
      - Jenkins always sets `JENKINS_URL`/`BUILD_NUMBER` for every job.
      - Azure DevOps always sets `TF_BUILD=True` (Microsoft Learn,
        "Predefined variables").
      - Docker creates `/.dockerenv` inside every container — the
        standard, widely-used in-container detection marker.
    A CI-platform signal takes priority over the Docker signal: "which CI
    tier/trigger produced this" (docs/10 §25) is the more specific fact
    when a CI job also happens to execute inside a container."""
    if os.environ.get("GITHUB_ACTIONS"):
        return "GitHub Actions"
    if os.environ.get("JENKINS_URL") or os.environ.get("BUILD_NUMBER"):
        return "Jenkins"
    if os.environ.get("TF_BUILD"):
        return "Azure DevOps"
    if os.path.exists("/.dockerenv"):
        return "Docker"
    return "Local"


def pytest_metadata(metadata: dict, config: pytest.Config) -> None:
    """Adds the docs/10 §25 'which CI tier/trigger produced the result'
    field to pytest-metadata's Environment table — the one piece the
    baseline setup (Python/Platform/Packages/Base URL) did not provide.
    Jenkins' own raw BUILD_NUMBER/JOB_NAME/etc. are already surfaced
    automatically by pytest-metadata's built-in Jenkins CI detection
    (pytest_metadata/ci/jenkins.py) — not duplicated here. GitHub Actions
    and Azure DevOps have no built-in pytest-metadata CI detection, so
    their commonly useful trigger/run fields are added explicitly, using
    only variable names verified against each platform's own current
    documentation."""
    platform_name = _detect_execution_platform()
    metadata["Execution Platform"] = platform_name

    if platform_name == "GitHub Actions":
        for label, env_name in (
            ("GitHub Workflow", "GITHUB_WORKFLOW"),
            ("GitHub Event", "GITHUB_EVENT_NAME"),
            ("GitHub Ref", "GITHUB_REF_NAME"),
            ("GitHub Run ID", "GITHUB_RUN_ID"),
        ):
            value = os.environ.get(env_name)
            if value:
                metadata[label] = value

    elif platform_name == "Azure DevOps":
        for label, env_name in (
            ("Azure Build ID", "BUILD_BUILDID"),
            ("Azure Build Reason", "BUILD_REASON"),
            ("Azure Agent Name", "AGENT_NAME"),
            ("Azure Source Branch", "BUILD_SOURCEBRANCH"),
        ):
            value = os.environ.get(env_name)
            if value:
                metadata[label] = value
