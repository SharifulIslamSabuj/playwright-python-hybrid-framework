"""SignupLoginPage.

Serves AE-UI-TC-004/005/006/007/008/021, per docs/11-Framework-
Architecture.md §11.

Locators verified live during Step 14 implementation (2026-08-25): the
login/signup forms expose dedicated `data-qa` test attributes
(`login-email`, `login-password`, `login-button`, `signup-name`,
`signup-email`, `signup-button`) — a genuine testability feature Step 2's
original analysis did not surface (it recorded "no data-testid attributes
observed anywhere on the AUT"). This finding is documented in
docs/14-UI-Automation.md as a correction to that earlier record, and these
attributes are used here as the rank-1 locator per
docs/11-Framework-Architecture.md §12's own hierarchy.

The "Enter Account Information" form's 20 fields (title/password/DOB/name/
address) were additionally verified live during Phase 18 Step 4
implementation (2026-08-26), by navigating up to but never submitting this
page — confirmed via direct DOM inspection that every field carries the
same `data-qa` convention. The four post-submit locators (account-created/
account-deleted headings, logged-in-as indicator, logout link) could NOT be
verified this way, since reaching them requires actually creating/logging
into an account — an action this project does not execute (see
`account_creation_authorized` in tests/conftest.py). They are implemented
using this AUT's own consistent `data-qa`/URL-path convention, verified
everywhere else on this page, and are explicitly marked UNVERIFIED below —
the same "REQUIRES VERIFICATION" status docs/07-Test-Cases.md already
assigns these exact expected results, not silently upgraded to VERIFIED.
"""

from __future__ import annotations

from playwright.sync_api import Locator

from src.data.models import NewUserPayload
from src.pages.base_page import BasePage


class SignupLoginPage(BasePage):
    """The Automation Exercise combined signup/login page (/login)."""

    def open(self) -> None:
        self.goto("login")

    @property
    def login_email_input(self) -> Locator:
        return self.page.locator('[data-qa="login-email"]')

    @property
    def login_password_input(self) -> Locator:
        return self.page.locator('[data-qa="login-password"]')

    @property
    def login_button(self) -> Locator:
        return self.page.locator('[data-qa="login-button"]')

    @property
    def login_error_message(self) -> Locator:
        return self.page.locator(".login-form p")

    @property
    def signup_error_message(self) -> Locator:
        """UNVERIFIED — see module docstring. Structurally mirrors
        `login_error_message` (`.login-form p`), the parallel column on the
        same two-column page."""
        return self.page.locator(".signup-form p")

    @property
    def signup_name_input(self) -> Locator:
        return self.page.locator('[data-qa="signup-name"]')

    @property
    def signup_email_input(self) -> Locator:
        return self.page.locator('[data-qa="signup-email"]')

    @property
    def signup_button(self) -> Locator:
        return self.page.locator('[data-qa="signup-button"]')

    def login(self, email: str, password: str) -> None:
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()

    def signup(self, name: str, email: str) -> None:
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

    # --- Enter Account Information page (VERIFIED live, 2026-08-26) ---

    @property
    def title_mr_radio(self) -> Locator:
        return self.page.locator("#id_gender1")

    @property
    def title_mrs_radio(self) -> Locator:
        return self.page.locator("#id_gender2")

    @property
    def account_password_input(self) -> Locator:
        return self.page.locator('[data-qa="password"]')

    @property
    def days_select(self) -> Locator:
        return self.page.locator('[data-qa="days"]')

    @property
    def months_select(self) -> Locator:
        return self.page.locator('[data-qa="months"]')

    @property
    def years_select(self) -> Locator:
        return self.page.locator('[data-qa="years"]')

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator('[data-qa="first_name"]')

    @property
    def last_name_input(self) -> Locator:
        return self.page.locator('[data-qa="last_name"]')

    @property
    def company_input(self) -> Locator:
        return self.page.locator('[data-qa="company"]')

    @property
    def address1_input(self) -> Locator:
        return self.page.locator('[data-qa="address"]')

    @property
    def address2_input(self) -> Locator:
        return self.page.locator('[data-qa="address2"]')

    @property
    def country_select(self) -> Locator:
        return self.page.locator('[data-qa="country"]')

    @property
    def state_input(self) -> Locator:
        return self.page.locator('[data-qa="state"]')

    @property
    def city_input(self) -> Locator:
        return self.page.locator('[data-qa="city"]')

    @property
    def zipcode_input(self) -> Locator:
        return self.page.locator('[data-qa="zipcode"]')

    @property
    def mobile_number_input(self) -> Locator:
        return self.page.locator('[data-qa="mobile_number"]')

    @property
    def create_account_button(self) -> Locator:
        return self.page.locator('[data-qa="create-account"]')

    def fill_account_information(self, payload: NewUserPayload) -> None:
        """Fills every field of the Account Information + Address
        Information form. Does not submit — see `submit_create_account`."""
        (self.title_mr_radio if payload["title"] == "Mr" else self.title_mrs_radio).check()
        self.account_password_input.fill(payload["password"])
        self.days_select.select_option(label=payload["birth_date"])
        self.months_select.select_option(label=payload["birth_month"])
        self.years_select.select_option(label=payload["birth_year"])
        self.first_name_input.fill(payload["firstname"])
        self.last_name_input.fill(payload["lastname"])
        self.company_input.fill(payload["company"])
        self.address1_input.fill(payload["address1"])
        self.address2_input.fill(payload["address2"])
        self.country_select.select_option(label=payload["country"])
        self.state_input.fill(payload["state"])
        self.city_input.fill(payload["city"])
        self.zipcode_input.fill(payload["zipcode"])
        self.mobile_number_input.fill(payload["mobile_number"])

    def submit_create_account(self) -> None:
        """Performs the actual, real account-creation submission. Only ever
        reached in a test gated by the `account_creation_authorized`
        fixture (tests/conftest.py) — see that fixture's docstring."""
        self.create_account_button.click()

    # --- Post-submit / authenticated-state locators (UNVERIFIED — see
    # module docstring; matches docs/07-Test-Cases.md's own "REQUIRES
    # VERIFICATION" status for these exact expected results) ---

    @property
    def account_created_heading(self) -> Locator:
        return self.page.locator('[data-qa="account-created"]')

    @property
    def continue_button(self) -> Locator:
        return self.page.locator('[data-qa="continue-button"]')

    @property
    def logged_in_as_indicator(self) -> Locator:
        return self.page.get_by_text("Logged in as", exact=False)

    @property
    def logout_link(self) -> Locator:
        return self.page.locator('a[href="/logout"]')

    @property
    def delete_account_link(self) -> Locator:
        return self.page.locator('a[href="/delete_account"]')

    @property
    def account_deleted_heading(self) -> Locator:
        return self.page.locator('[data-qa="account-deleted"]')

    def confirm_account_created(self) -> None:
        self.continue_button.click()

    def logout(self) -> None:
        self.logout_link.click()

    def delete_account(self) -> None:
        self.delete_account_link.click()
