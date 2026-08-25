"""SignupLoginPage.

Serves AE-UI-TC-006 in this step (invalid login — the only Signup/Login case
currently implementable without account-creation authorization; see
docs/14-UI-Automation.md §8 for TC-004/005/007/008's blocked status).

Locators verified live during Step 14 implementation (2026-08-25): the
login/signup forms expose dedicated `data-qa` test attributes
(`login-email`, `login-password`, `login-button`, `signup-name`,
`signup-email`, `signup-button`) — a genuine testability feature Step 2's
original analysis did not surface (it recorded "no data-testid attributes
observed anywhere on the AUT"). This finding is documented in
docs/14-UI-Automation.md as a correction to that earlier record, and these
attributes are used here as the rank-1 locator per
docs/11-Framework-Architecture.md §12's own hierarchy.
"""

from __future__ import annotations

from playwright.sync_api import Locator

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
