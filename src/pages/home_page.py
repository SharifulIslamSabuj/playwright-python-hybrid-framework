"""HomePage.

Serves AE-UI-TC-001 (home smoke) and AE-UI-TC-023 (add recommended item to
cart), per docs/11-Framework-Architecture.md §11.

Locators verified live against https://automationexercise.com during Step 14
implementation (2026-08-25) — DOM structure confirmed via direct inspection,
not assumed from Step 2's earlier, less exhaustive pass.
"""

from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class HomePage(BasePage):
    """The Automation Exercise home page."""

    def open(self) -> None:
        self.goto()

    @property
    def category_panel(self) -> Locator:
        return self.page.locator(".category-products")

    @property
    def brands_panel(self) -> Locator:
        return self.page.locator(".brands-name")

    @property
    def featured_items_section(self) -> Locator:
        return self.page.locator(".features_items")

    @property
    def recommended_items_carousel(self) -> Locator:
        return self.page.locator("#recommended-item-carousel")

    @property
    def subscription_email_input(self) -> Locator:
        return self.page.get_by_role("textbox", name="Your email address")

    @property
    def added_to_cart_modal(self) -> Locator:
        return self.page.locator(".modal-content")

    def add_first_recommended_item_to_cart(self) -> None:
        """Adds the first *visible* recommended-carousel item (docs/07
        AE-UI-TC-023).

        Uses a `visible=true` filter rather than scoping to `.item.active` —
        Bootstrap's carousel.js briefly assigns the `.active` class to both
        the outgoing and incoming slide during its CSS transition, a real,
        VERIFIED race discovered during Step 14 implementation. Filtering on
        actual visibility instead of the transitional CSS class sidesteps it.
        """
        self.page.locator("#recommended-item-carousel .add-to-cart >> visible=true").first.click()

    def go_to_cart_from_modal(self) -> None:
        """Waits for the "Added!" confirmation modal and follows its "View
        Cart" link — the reliable completion signal for the add-to-cart AJAX
        call. Callers must NOT navigate to the cart page independently right
        after `add_first_recommended_item_to_cart()`: doing so races the
        in-flight AJAX request and can abort it before the server records
        the item, a second real, VERIFIED bug found during Step 14
        implementation (docs/14-UI-Automation.md documents it in full)."""
        self.added_to_cart_modal.get_by_role("link", name="View Cart").click()
