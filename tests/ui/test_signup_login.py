"""Signup/Login module — Automation Scope AUTOMATE cases in this file:
AE-UI-TC-006 only.

AE-UI-TC-004/005/007/008 remain BLOCKED this step — see
docs/14-UI-Automation.md §8 for the full rationale (no QA-Lead
authorization yet to create/delete a real account or provision the durable
TD-USER-VALID-001/TD-USER-EXISTING-001 accounts).
"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from src.data.users import INVALID_CREDENTIALS
from src.pages.signup_login_page import SignupLoginPage


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
