"""CartPage.

Serves AE-UI-TC-015/016 (view), 018 (remove), 024 (checkout gate), per
docs/11-Framework-Architecture.md §11.

Locators verified live against https://automationexercise.com/view_cart
during Step 14 implementation (2026-08-25), including the exact checkout-
gate modal text (unchanged from Step 2's original VERIFIED observation)
and the cart-removal delete control (`a.cart_quantity_delete`, icon-only —
no accessible name, hence the CSS/attribute-based locator per
docs/11-Framework-Architecture.md §12 rank 5/6).
"""

from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class CartPage(BasePage):
    """The Automation Exercise cart page (/view_cart)."""

    def open(self) -> None:
        self.goto("view_cart")

    @property
    def line_item_rows(self) -> Locator:
        return self.page.locator("#cart_info_table tbody tr")

    def row(self, product_id: int) -> Locator:
        return self.page.locator(f"#product-{product_id}")

    def row_price(self, product_id: int) -> Locator:
        return self.row(product_id).locator(".cart_price")

    def row_quantity(self, product_id: int) -> Locator:
        return self.row(product_id).locator(".cart_quantity button")

    def row_total(self, product_id: int) -> Locator:
        return self.row(product_id).locator(".cart_total_price")

    def remove_item(self, product_id: int) -> None:
        """Triggers the AUT's AJAX-driven removal (REQ-UI-005) — the row
        disappears without a page navigation, so callers should assert on
        the row/empty-cart state rather than a load event."""
        self.row(product_id).locator(".cart_quantity_delete").click()

    @property
    def empty_cart_message(self) -> Locator:
        return self.page.get_by_text("Cart is empty!", exact=False)

    @property
    def proceed_to_checkout_link(self) -> Locator:
        """`<a class="btn btn-default check_out">Proceed To Checkout</a>` has
        no `href` attribute (VERIFIED during Step 14 implementation) — an
        `<a>` without `href` is not assigned the implicit ARIA `link` role by
        browsers, so `get_by_role("link", ...)` never matches it despite it
        being visibly a link-styled control. Text-based matching is used
        instead, a documented, deliberate departure from the role-first
        preference (docs/11-Framework-Architecture.md §12), justified by
        this specific, VERIFIED markup gap."""
        return self.page.get_by_text("Proceed To Checkout", exact=True)

    @property
    def checkout_gate_modal(self) -> Locator:
        return self.page.locator("#checkoutModal")

    @property
    def checkout_gate_message(self) -> Locator:
        return self.checkout_gate_modal.get_by_text(
            "Register / Login account to proceed on checkout.", exact=False
        )

    @property
    def checkout_gate_register_login_link(self) -> Locator:
        return self.checkout_gate_modal.get_by_role("link", name="Register / Login")

    @property
    def checkout_gate_continue_on_cart_button(self) -> Locator:
        return self.checkout_gate_modal.get_by_role("button", name="Continue On Cart")

    def click_proceed_to_checkout(self) -> None:
        self.proceed_to_checkout_link.click()
