"""Auth (verifyLogin/createAccount/deleteAccount/getUserDetailByEmail)
API — Automation Scope AUTOMATE cases in this file: AE-API-TC-007, 008,
009, 010, 011, 012, 014.

AE-API-TC-007/011/012/014 all consume `shared_registered_account`
(tests/conftest.py) — one real account, created once per test session (by
AE-API-TC-011 itself, the first test to request the fixture) and reused by
every other account-dependent Test Case across both this file and
tests/ui/test_signup_login.py, deleted last by AE-API-TC-012. Gated by
`account_creation_authorized` (tests/conftest.py) — this project's AI
assistant never sets that gate itself (docs/09-Automation-Scope.md
§12/§30 item 4; docs/07-Test-Cases.md AE-API-TC-011's own recorded
statement).

AE-API-TC-011 and AE-API-TC-012 are separate test functions (not combined
into one, unlike the prior implementation) so each Test Case ID has its
own independently-visible pytest result and its own real assertion on the
create/delete response — `SharedAccountState.create_response`
(tests/conftest.py) is what lets AE-API-TC-011 assert on a creation the
fixture performed, without re-performing it. Their required execution
order (create before every dependent test, delete after all of them) is
enforced by the `pytest_collection_modifyitems` hook in tests/conftest.py,
since plain file/definition-order collection can't guarantee ordering
across the tests/api/ and tests/ui/ modules that share this account.

AE-API-TC-013 (updateAccount) is MANUAL per docs/09-Automation-Scope.md §5
and is intentionally never implemented — `AuthApiClient.update_account`
does not exist (verified by
tests/test_framework_foundation.py::test_auth_api_client_does_not_implement_update_account).
"""

from __future__ import annotations

import pytest

from src.api.auth_api_client import AuthApiClient
from src.data.users import INVALID_CREDENTIALS
from tests.conftest import SharedAccountState


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.regression
def test_ae_api_tc_008_verify_login_invalid_credentials(auth_api: AuthApiClient) -> None:
    """Test Case: AE-API-TC-008
    Scenario: AE-API-SC-008
    Requirement: REQ-API-010
    Test Data: TD-USER-INVALID-001 (fabricated, non-existent credentials)

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 404,
    message "User not found!"
    """
    response = auth_api.verify_login(
        INVALID_CREDENTIALS["email"], INVALID_CREDENTIALS["password"]
    )

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_ae_api_tc_009_verify_login_missing_email(auth_api: AuthApiClient) -> None:
    """Test Case: AE-API-TC-009
    Scenario: AE-API-SC-009
    Requirement: REQ-API-008
    Test Data: TD-AUTH-MISSING-EMAIL-001 (password only, email omitted)

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 400,
    message "Bad request, email or password parameter is missing in POST
    request."
    """
    response = auth_api.verify_login(None, INVALID_CREDENTIALS["password"])

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, email or password parameter is missing in POST request."


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_ae_api_tc_010_delete_verify_login_unsupported_method(auth_api: AuthApiClient) -> None:
    """Test Case: AE-API-TC-010
    Scenario: AE-API-SC-010
    Requirement: REQ-API-009
    Test Data: None

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 405,
    message "This request method is not supported."
    """
    response = auth_api.delete_verify_login()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."


@pytest.mark.api
@pytest.mark.regression
def test_ae_api_tc_007_verify_login_valid_credentials(
    auth_api: AuthApiClient, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-API-TC-007
    Scenario: AE-API-SC-007
    Requirement: REQ-API-007
    Test Data: the session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, VERIFIED at the documentation
    level): responseCode 200, message "User exists!"

    Depends on AE-API-TC-011 having created the shared account first — this
    project's `pytest_collection_modifyitems` hook (tests/conftest.py)
    guarantees that ordering. Gated transitively by
    `account_creation_authorized` (via `shared_registered_account`).
    """
    account = shared_registered_account.payload
    response = auth_api.verify_login(account["email"], account["password"])

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.ci_restricted
def test_ae_api_tc_011_create_account(
    shared_registered_account: SharedAccountState,
) -> None:
    """Test Case: AE-API-TC-011 (createAccount)
    Scenario: AE-API-SC-011
    Requirement: REQ-API-011
    Test Data: dynamically generated (FULL_DYNAMIC) — see
    `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, VERIFIED at the documentation
    level): HTTP 201, message "User created!"

    The account-creation lifecycle is now shared: the first test in the
    session to request `shared_registered_account` triggers the real
    `createAccount` call, which `pytest_collection_modifyitems`
    (tests/conftest.py) guarantees is this test — so this assertion is
    always checking the response from a call this Test Case itself caused,
    not one performed earlier by an unrelated test.
    """
    response = shared_registered_account.create_response

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 201
    assert body["message"] == "User created!"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.ci_restricted
def test_ae_api_tc_012_delete_account(
    auth_api: AuthApiClient, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-API-TC-012 (deleteAccount)
    Scenario: AE-API-SC-012
    Requirement: REQ-API-012
    Test Data: the session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, VERIFIED at the documentation
    level): HTTP 200, message "Account deleted!"

    This is the FINAL lifecycle operation: `pytest_collection_modifyitems`
    (tests/conftest.py) orders this test to run after every other test
    that depends on `shared_registered_account`, so the account is only
    ever deleted once every dependent Test Case has finished using it.
    Performs the real delete call itself and marks
    `shared_registered_account.deleted = True` so the fixture's own
    session-teardown safety net does not attempt a redundant second delete.
    """
    account = shared_registered_account.payload
    response = auth_api.delete_account(account["email"], account["password"])

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "Account deleted!"

    shared_registered_account.deleted = True


@pytest.mark.api
@pytest.mark.regression
def test_ae_api_tc_014_get_user_detail_by_email(
    auth_api: AuthApiClient, shared_registered_account: SharedAccountState
) -> None:
    """Test Case: AE-API-TC-014
    Scenario: AE-API-SC-014
    Requirement: REQ-API-014
    Test Data: the session's `shared_registered_account` (tests/conftest.py)

    Expected Result (docs/07-Test-Cases.md, VERIFIED at the documentation
    level): HTTP 200, JSON user detail body. The exact nested body shape
    beyond `responseCode` is NOT asserted here — this project has never
    obtained a real "found" response to verify it against (VERIFIED,
    2026-08-26: a live, read-only probe against a deliberately non-existent
    email confirms the error-path envelope is
    {"responseCode": ..., "message": ...}, but the success-path `user`
    object shape remains unconfirmed), consistent with not asserting
    unverified specifics elsewhere in this project.

    Depends on AE-API-TC-011 having created the shared account first (see
    AE-API-TC-007's docstring — same ordering guarantee).
    """
    account = shared_registered_account.payload
    response = auth_api.get_user_detail_by_email(account["email"])

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
