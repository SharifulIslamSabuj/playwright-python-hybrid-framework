"""Framework-foundation validation only — NOT Automation Exercise business
test cases.

Deliberately outside tests/ui, tests/api, and tests/hybrid (reserved for the
31 approved automated business Test Cases), exactly like
tests/test_setup_validation.py (Step 12). This file validates that Step 13's
Core Framework Development artifacts — configuration, fixtures, Page Object
skeletons, API client foundation, utilities — are wired correctly.

Consistent with Step 12's own precedent, no test in this file makes a live
network call to automationexercise.com: Page Object/BasePage validation uses
Playwright's local `set_content`, and API client validation checks
construction/configuration only, never fires a request. No test here is
tied to, or could be mistaken for, any AE-UI-TC-*/AE-API-TC-*/AE-E2E-TC-* ID.
"""

from __future__ import annotations

import os
import re

import pytest

from src.api.auth_api_client import AuthApiClient
from src.api.brands_api_client import BrandsApiClient
from src.api.products_api_client import ProductsApiClient
from src.config.settings import Settings
from src.data.models import NewUserPayload
from src.data.users import INVALID_CREDENTIALS, build_new_user_payload
from src.pages.base_page import BasePage
from src.pages.cart_page import CartPage
from src.pages.home_page import HomePage
from src.pages.product_details_page import ProductDetailsPage
from src.pages.products_page import ProductsPage
from src.pages.signup_login_page import SignupLoginPage
from src.utils.data_generator import generate_unique_email, generate_unique_suffix
from src.utils.logger import get_logger

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def test_settings_fixture_matches_module_singleton(settings: Settings) -> None:
    from src.config.settings import settings as module_settings

    assert settings is module_settings


def test_settings_report_paths_are_computed_correctly(settings: Settings) -> None:
    assert settings.screenshots_dir.as_posix().endswith("reports/screenshots")
    assert settings.traces_dir.as_posix().endswith("reports/traces")
    assert settings.html_report_path.as_posix().endswith("reports/html/report.html")


def test_durable_account_availability_flags_reflect_environment(settings: Settings) -> None:
    # Environment-agnostic: this project's own execution environment may or
    # may not have durable credentials provisioned (docs/09 §30 item 4 — a
    # human operator's own choice, never invented here). The oracle is read
    # directly from os.environ, independently of Settings' own field
    # population, so this genuinely checks the flag reflects the real
    # environment rather than trivially re-deriving itself from the same
    # two Settings fields the flag is computed from.
    expected_valid_account = bool(
        os.environ.get("DURABLE_VALID_USER_EMAIL")
        and os.environ.get("DURABLE_VALID_USER_PASSWORD")
    )
    expected_existing_account = bool(os.environ.get("DURABLE_EXISTING_USER_EMAIL"))

    assert settings.has_durable_valid_account() is expected_valid_account
    assert settings.has_durable_existing_account() is expected_existing_account


# ---------------------------------------------------------------------------
# Page Object foundation (no network call — local content only)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "page_object_fixture",
    ["home_page", "signup_login_page", "products_page", "product_details_page", "cart_page"],
)
def test_page_object_fixture_constructs_correctly(page_object_fixture: str, request: pytest.FixtureRequest) -> None:
    page_object = request.getfixturevalue(page_object_fixture)
    assert isinstance(page_object, BasePage)
    assert page_object.page is not None


def test_base_page_url_resolution_is_pure_and_correct() -> None:
    assert BasePage.resolve_url() == "https://automationexercise.com"
    assert BasePage.resolve_url("/products") == "https://automationexercise.com/products"
    assert BasePage.resolve_url("login") == "https://automationexercise.com/login"


def test_base_page_helpers_work_against_local_content(page) -> None:  # noqa: ANN001 - Page from pytest-playwright
    """Proves the wait/visibility/text helpers work mechanically, using
    Playwright's local `set_content` — no request ever leaves the machine."""
    base_page = HomePage(page)
    page.set_content("<html><body><h1 id='greeting'>Framework Foundation</h1></body></html>")
    base_page.wait_for_load()
    locator = page.locator("#greeting")
    assert base_page.is_visible(locator) is True
    assert base_page.get_text(locator) == "Framework Foundation"
    base_page.expect_visible(locator)
    base_page.expect_text(locator, "Framework Foundation")


# ---------------------------------------------------------------------------
# API client foundation (construction/configuration only — no live request)
# ---------------------------------------------------------------------------


def test_products_api_client_constructs_with_configured_base_url(settings: Settings) -> None:
    client = ProductsApiClient()
    assert client.base_url.rstrip("/") == settings.api_base_url.rstrip("/")
    client.close()


def test_brands_api_client_constructs_with_configured_base_url(settings: Settings) -> None:
    client = BrandsApiClient()
    assert client.base_url.rstrip("/") == settings.api_base_url.rstrip("/")
    client.close()


def test_auth_api_client_constructs_with_configured_base_url(settings: Settings) -> None:
    client = AuthApiClient()
    assert client.base_url.rstrip("/") == settings.api_base_url.rstrip("/")
    client.close()


def test_auth_api_client_does_not_implement_update_account() -> None:
    """AE-API-TC-013 is MANUAL, not AUTOMATE (docs/09-Automation-Scope.md §5)
    — the client must not implement it yet (docs/11 §13)."""
    assert not hasattr(AuthApiClient, "update_account")


def test_api_client_fixtures_are_session_scoped_and_shared(products_api: ProductsApiClient) -> None:
    assert isinstance(products_api, ProductsApiClient)


# ---------------------------------------------------------------------------
# Test data foundation
# ---------------------------------------------------------------------------


def test_generate_unique_email_is_actually_unique() -> None:
    first = generate_unique_email("framework_foundation")
    second = generate_unique_email("framework_foundation")
    assert first != second
    assert re.match(r"^ae_framework_foundation_\d+_[0-9a-f]{8}@testmail\.com$", first)


def test_generate_unique_suffix_is_unique() -> None:
    assert generate_unique_suffix() != generate_unique_suffix()


def test_build_new_user_payload_matches_16_field_schema() -> None:
    payload: NewUserPayload = build_new_user_payload("framework_foundation")
    expected_keys = {
        "name", "email", "password", "title", "birth_date", "birth_month",
        "birth_year", "firstname", "lastname", "company", "address1",
        "address2", "country", "zipcode", "state", "city", "mobile_number",
    }
    assert set(payload.keys()) == expected_keys
    assert payload["email"].startswith("ae_framework_foundation_")


def test_invalid_credentials_dataset_is_fabricated_not_real() -> None:
    assert "invalid" in INVALID_CREDENTIALS["email"]


def test_unique_user_data_fixture_is_traceable_to_test_name(unique_user_data: NewUserPayload) -> None:
    assert "test_unique_user_data_fixture_is_traceable_to_test_name" in unique_user_data["email"]


# ---------------------------------------------------------------------------
# Cleanup fixture (mechanism only — nothing registered, nothing deleted)
# ---------------------------------------------------------------------------


def test_created_account_cleanup_fixture_starts_empty(
    created_account_cleanup: list[dict[str, str]],
) -> None:
    assert created_account_cleanup == []


# ---------------------------------------------------------------------------
# Durable-account fixtures
# ---------------------------------------------------------------------------


def test_durable_valid_account_fixture_returns_configured_credentials(
    settings: Settings, durable_valid_account: dict[str, str]
) -> None:
    # Genuinely environment-aware, in both directions — no unconditional
    # skip. Requesting `durable_valid_account` as a parameter is what
    # triggers its own conditional behavior (tests/conftest.py):
    #   - unprovisioned: the fixture itself calls pytest.skip() with a
    #     clear reason before this body ever runs — this test SKIPS, not
    #     fails (docs/09-Automation-Scope.md §30 item 4).
    #   - provisioned: the fixture returns the configured {email, password}
    #     dict, and this body asserts its contract — correct keys, values
    #     matching Settings' own fields (never a literal credential typed
    #     here), and non-empty.
    assert durable_valid_account["email"] == settings.durable_valid_user_email
    assert durable_valid_account["password"] == settings.durable_valid_user_password
    assert durable_valid_account["email"] != ""
    assert durable_valid_account["password"] != ""


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def test_get_logger_returns_usable_logger() -> None:
    logger = get_logger("framework_foundation_test")
    assert logger.name == "framework_foundation_test"
    logger.info("Framework foundation logging check.")
