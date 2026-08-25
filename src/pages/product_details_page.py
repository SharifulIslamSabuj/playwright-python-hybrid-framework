"""ProductDetailsPage.

Serves the detail-page part of AE-UI-TC-011, plus AE-UI-TC-015/016 (cart
add, quantity) and AE-UI-TC-024 (product used to reach the checkout gate),
per docs/11-Framework-Architecture.md §11.

Locators verified live against https://automationexercise.com/product_details/1
during Step 14 implementation (2026-08-25), including the "Added!" modal's
exact structure (`.modal-content`, `h4.modal-title`, `a[href="/view_cart"]`
containing "View Cart" text).
"""

from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    """The Automation Exercise individual product detail page."""

    def open(self, product_id: int) -> None:
        self.goto(f"product_details/{product_id}")

    @property
    def product_name(self) -> Locator:
        return self.page.locator(".product-information h2")

    @property
    def category_text(self) -> Locator:
        return self.page.locator(".product-information p").first

    @property
    def price(self) -> Locator:
        return self.page.locator(".product-information span span")

    @property
    def quantity_input(self) -> Locator:
        return self.page.locator("#quantity")

    @property
    def add_to_cart_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add to cart")

    @property
    def availability_text(self) -> Locator:
        return self.page.locator(".product-information p", has_text="Availability")

    @property
    def condition_text(self) -> Locator:
        return self.page.locator(".product-information p", has_text="Condition")

    @property
    def brand_text(self) -> Locator:
        return self.page.locator(".product-information p", has_text="Brand")

    @property
    def added_to_cart_modal(self) -> Locator:
        return self.page.locator(".modal-content")

    def set_quantity(self, quantity: int) -> None:
        self.quantity_input.fill(str(quantity))

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def go_to_cart_from_modal(self) -> None:
        self.added_to_cart_modal.get_by_role("link", name="View Cart").click()
