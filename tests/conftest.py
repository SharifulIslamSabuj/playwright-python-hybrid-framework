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

from collections.abc import Generator
from typing import Any

import pytest

from src.api.auth_api_client import AuthApiClient
from src.api.brands_api_client import BrandsApiClient
from src.api.products_api_client import ProductsApiClient
from src.config.settings import Settings, settings as _settings
from src.data.models import NewUserPayload
from src.data.users import build_new_user_payload
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
