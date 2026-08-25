"""Auth (verifyLogin) API — Automation Scope AUTOMATE cases implemented this
step: AE-API-TC-008, 009, 010.

AE-API-TC-007 (verifyLogin, valid credentials) remains BLOCKED — it
requires the durable TD-USER-VALID-001 account, which is not provisioned
pending the same QA-Lead authorization gate documented for the UI layer in
docs/14-UI-Automation.md §8 (docs/09-Automation-Scope.md §12/§30 item 4).

AE-API-TC-011/012 (createAccount/deleteAccount) and AE-API-TC-014
(getUserDetailByEmail) are likewise BLOCKED for the same reason — see
docs/15-API-Automation.md §16.

AE-API-TC-013 (updateAccount) is MANUAL per docs/09-Automation-Scope.md §5
and is intentionally never implemented — `AuthApiClient.update_account`
does not exist (verified by
tests/test_framework_foundation.py::test_auth_api_client_does_not_implement_update_account).
"""

from __future__ import annotations

import pytest

from src.api.auth_api_client import AuthApiClient
from src.data.users import INVALID_CREDENTIALS


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
