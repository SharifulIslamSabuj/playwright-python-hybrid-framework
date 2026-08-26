"""Signup/Login module — Automation Scope AUTOMATE cases in this file:
AE-UI-TC-004, 005, 006, 007, 008, 021.

AE-UI-TC-004 (create/delete a real account, its own self-contained
lifecycle — see its own docstring) is gated by `account_creation_authorized`
(tests/conftest.py). AE-UI-TC-005/007/008/021 consume the session's
`shared_registered_account` (tests/conftest.py) — one real account created
once by AE-API-TC-011 and reused across every dependent Test Case in both
this file and tests/api/test_auth_api.py, per the account-lifecycle
architecture: create once → reuse everywhere → delete last
(AE-API-TC-012). None of these gates is ever set by this project's AI
assistant itself (docs/09-Automation-Scope.md §12/§30 item 4;
docs/07-Test-Cases.md AE-API-TC-011). Absent that provisioning, each
cleanly skips with a documented reason rather than failing or fabricating
a result.

AE-UI-TC-004 is data-driven: parametrized over `DataMode`
(src/data/users.py) — ddt-only, hybrid, full-dynamic — via
`build_user_data`, so the same approved registration flow is validated
against three distinct data-supply strategies rather than one hard-coded
profile. Test logic and test data stay fully separated: the test body is
identical across all 3 modes. This is a separate concern from the shared
account above: TC-004 validates the registration FLOW itself (its own
approved create→verify→delete lifecycle, per docs/07), so it always
creates and deletes its own throwaway account regardless of data mode; it
never hands that account to the other tests.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from src.data.products import PRODUCT_3, SEARCH_KEYWORD_VALID
from src.data.users import (
    INVALID_CREDENTIALS,
    REGISTRATION_PROFILE_NAMES,
    DataMode,
    build_user_data,
)
from src.pages.cart_page import CartPage
from src.pages.product_details_page import ProductDetailsPage
from src.pages.products_page import ProductsPage
from src.pages.signup_login_page import SignupLoginPage
from tests.conftest import SharedAccountState


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.cross_browser
@pytest.mark.regression
def test_ae_ui_tc_006_login_with_invalid_credentials(signup_login_page: SignupLoginPage) -> None:
    """Test Case: AE-UI-TC-006
    Scenario: AE-UI-SC-006
    Requirement: REQ-FUNC-SL-004
    Test Data: TD-USER-INVALID-001 (fabricated, non-existent credentials)

    Expected Result (docs/07-Test-Cases.md, VERIFIED Step 2 and re-verified
    live during this step): user remains on /login and the inline message
    "Your email or password is incorrect!" is displayed.
    """
    signup_login_page.open()

    signup_login_page.login(
        INVALID_CREDENTIALS["email"], INVALID_CREDENTIALS["password"]
    )

    expect(signup_login_page.login_error_message).to_have_text(
        "Your email or password is incorrect!"
    )
    expect(signup_login_page.page).to_have_url(signup_login_page.resolve_url("login"))


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.ci_restricted
@pytest.mark.parametrize(
    "data_mode, profile_index",
    [
        (DataMode.DDT_ONLY, 0),
        (DataMode.HYBRID, 1),
        (DataMode.FULL_DYNAMIC, 0),
    ],
    ids=[
        f"ddt-only-{REGISTRATION_PROFILE_NAMES[0]}",
        f"hybrid-{REGISTRATION_PROFILE_NAMES[1]}",
        "full-dynamic",
    ],
)
def test_ae_ui_tc_004_register_new_user_full_lifecycle(
    signup_login_page: SignupLoginPage,
    account_creation_authorized: None,
    created_account_cleanup: list[dict[str, str]],
    data_mode: DataMode,
    profile_index: int,
    request: pytest.FixtureRequest,
) -> None:
    """Test Case: AE-UI-TC-004
    Scenario: AE-UI-SC-004
    Requirement: REQ-FUNC-SL-001, REQ-FUNC-SL-006
    Test Data: TD-USER-NEW-001 — DDT: `build_user_data` (src/data/users.py),
    exercised across all 3 data-supply strategies in one test
    implementation: `ddt-only` (profile data unmodified), `hybrid`
    (DDT profile + runtime-generated name/mobile), `full-dynamic` (every
    field runtime-generated except an already-VERIFIED country/state/city
    pairing). Same approved business flow, same assertions, across all 3 —
    DDT parameterizes the *data*, not the Test Case's expected behavior.

    Expected Result (docs/07-Test-Cases.md, REQUIRES VERIFICATION — exact
    wording unconfirmed by this project): distinct account-created,
    logged-in, and account-deleted confirmations are each shown.

    Gated by `account_creation_authorized` (tests/conftest.py) — skips
    unless ACCOUNT_CREATION_EXECUTION_AUTHORIZED=true is explicitly set by
    a human operator in their own environment. Also registered with
    `created_account_cleanup` as a safety net in case the UI-driven
    deletion below does not complete (docs/10-Automation-Strategy.md §35).
    """
    user_data = build_user_data(request.node.name, data_mode, profile_index)

    signup_login_page.open()
    signup_login_page.signup(user_data["name"], user_data["email"])

    signup_login_page.fill_account_information(user_data)
    signup_login_page.submit_create_account()
    created_account_cleanup.append(
        {"email": user_data["email"], "password": user_data["password"]}
    )

    expect(signup_login_page.account_created_heading).to_be_visible()
    signup_login_page.confirm_account_created()

    expect(signup_login_page.logged_in_as_indicator).to_be_visible()

    signup_login_page.delete_account()
    expect(signup_login_page.account_deleted_heading).to_be_visible()


@pytest.mark.ui
@pytest.mark.cross_browser
@pytest.mark.regression
def test_ae_ui_tc_005_login_with_valid_credentials(
    signup_login_page: SignupLoginPage, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-UI-TC-005
    Scenario: AE-UI-SC-005
    Requirement: REQ-FUNC-SL-003
    Test Data: the session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, REQUIRES VERIFICATION): user
    reaches an authenticated state with a "Logged in as [name]" signal.

    Depends on AE-API-TC-011 having created the shared account first —
    `pytest_collection_modifyitems` (tests/conftest.py) guarantees that
    ordering across both this file and tests/api/test_auth_api.py.
    """
    account = shared_registered_account.payload
    signup_login_page.open()
    signup_login_page.login(account["email"], account["password"])

    expect(signup_login_page.logged_in_as_indicator).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_007_logout_from_authenticated_session(
    signup_login_page: SignupLoginPage, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-UI-TC-007
    Scenario: AE-UI-SC-007
    Requirement: REQ-FUNC-SL-005, REQ-FUNC-SL-006
    Test Data: the session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, REQUIRES VERIFICATION): user
    returns to an unauthenticated state with /login reachable again.

    Same account-lifecycle ordering guarantee as AE-UI-TC-005.
    """
    account = shared_registered_account.payload
    signup_login_page.open()
    signup_login_page.login(account["email"], account["password"])
    expect(signup_login_page.logged_in_as_indicator).to_be_visible()

    signup_login_page.logout()

    expect(signup_login_page.page).to_have_url(signup_login_page.resolve_url("login"))


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_ae_ui_tc_008_register_with_already_registered_email(
    signup_login_page: SignupLoginPage, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-UI-TC-008
    Scenario: AE-UI-SC-008
    Requirement: REQ-FUNC-SL-002
    Test Data: the session's `shared_registered_account` email
    (tests/conftest.py) — genuinely already-registered, not fabricated.

    Expected Result (docs/07-Test-Cases.md, REQUIRES VERIFICATION — TS
    baseline references "Email Address already exist!"): registration is
    rejected with an error message; no new account is created.

    Same account-lifecycle ordering guarantee as AE-UI-TC-005. Creates no
    account itself: the whole point of this negative case is that signup
    is rejected before any account would be created.
    """
    account_email = shared_registered_account.payload["email"]
    signup_login_page.open()
    signup_login_page.signup("Automation Duplicate Check", account_email)

    expect(signup_login_page.signup_error_message).to_have_text(
        "Email Address already exist!"
    )


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_021_search_add_to_cart_persists_after_login(
    products_page: ProductsPage,
    product_details_page: ProductDetailsPage,
    cart_page: CartPage,
    signup_login_page: SignupLoginPage,
    shared_registered_account: SharedAccountState,
) -> None:
    """Test Case: AE-UI-TC-021
    Scenario: AE-UI-SC-018
    Requirement: REQ-FUNC-PR-003, REQ-FUNC-CT-005
    Test Data: TD-SEARCH-VALID-001 ("dress", matching PRODUCT_3), the
    session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, REQUIRES VERIFICATION): cart
    contents persist across the login transition.

    Same account-lifecycle ordering guarantee as AE-UI-TC-005.
    """
    account = shared_registered_account.payload
    products_page.open()
    products_page.search(SEARCH_KEYWORD_VALID)
    expect(products_page.product_cards.first).to_be_visible()

    product_details_page.open(PRODUCT_3["id"])
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()
    expect(cart_page.row(PRODUCT_3["id"])).to_be_visible()

    signup_login_page.open()
    signup_login_page.login(account["email"], account["password"])
    expect(signup_login_page.logged_in_as_indicator).to_be_visible()

    cart_page.open()
    expect(cart_page.row(PRODUCT_3["id"])).to_be_visible()
