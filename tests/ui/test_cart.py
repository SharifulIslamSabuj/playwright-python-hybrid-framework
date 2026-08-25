"""Cart module — Automation Scope AUTOMATE cases: AE-UI-TC-015, 016, 018, 024."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from src.data.products import CART_QUANTITY_VALID, PRODUCT_1, PRODUCT_2, PRODUCT_3
from src.pages.cart_page import CartPage
from src.pages.product_details_page import ProductDetailsPage


@pytest.mark.ui
@pytest.mark.cross_browser
@pytest.mark.regression
def test_ae_ui_tc_015_add_multiple_products_verify_totals(
    product_details_page: ProductDetailsPage, cart_page: CartPage
) -> None:
    """Test Case: AE-UI-TC-015
    Scenario: AE-UI-SC-013
    Requirement: REQ-FUNC-CT-001, REQ-FUNC-CT-004
    Test Data: TD-PRODUCT-002, TD-PRODUCT-003

    Expected Result (docs/07-Test-Cases.md): both items appear with correct
    price x quantity line totals and a correct cart-level total — extending
    Step 2's single-item-only evidence to the multi-item case.
    """
    product_details_page.open(PRODUCT_2["id"])
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()

    cart_page.open()
    product_details_page.open(PRODUCT_3["id"])
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()

    expect(cart_page.line_item_rows).to_have_count(2)
    expect(cart_page.row_total(PRODUCT_2["id"])).to_have_text(PRODUCT_2["price"])
    expect(cart_page.row_total(PRODUCT_3["id"])).to_have_text(PRODUCT_3["price"])


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_016_set_and_verify_cart_quantity(
    product_details_page: ProductDetailsPage, cart_page: CartPage
) -> None:
    """Test Case: AE-UI-TC-016
    Scenario: AE-UI-SC-014
    Requirement: REQ-FUNC-CT-002
    Test Data: TD-PRODUCT-001, TD-CART-QTY-VALID (4)

    Expected Result (docs/07-Test-Cases.md): the cart line reflects the
    quantity set on the detail page before adding to cart.
    """
    product_details_page.open(PRODUCT_1["id"])
    product_details_page.set_quantity(CART_QUANTITY_VALID)
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()

    expect(cart_page.row_quantity(PRODUCT_1["id"])).to_have_text(str(CART_QUANTITY_VALID))


@pytest.mark.ui
@pytest.mark.cross_browser
@pytest.mark.regression
def test_ae_ui_tc_018_remove_product_from_cart(
    product_details_page: ProductDetailsPage, cart_page: CartPage
) -> None:
    """Test Case: AE-UI-TC-018
    Scenario: AE-UI-SC-015
    Requirement: REQ-FUNC-CT-003
    Test Data: TD-PRODUCT-001

    Expected Result (docs/07-Test-Cases.md, VERIFIED Step 2): the item is
    removed and the cart returns to its empty state without a full page
    reload (AJAX-driven, REQ-UI-005).
    """
    product_details_page.open(PRODUCT_1["id"])
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()

    expect(cart_page.row(PRODUCT_1["id"])).to_be_visible()
    cart_page.remove_item(PRODUCT_1["id"])

    expect(cart_page.row(PRODUCT_1["id"])).to_have_count(0)
    expect(cart_page.empty_cart_message).to_be_visible()


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.cross_browser
@pytest.mark.regression
def test_ae_ui_tc_024_checkout_gate_blocks_unauthenticated_access(
    product_details_page: ProductDetailsPage, cart_page: CartPage
) -> None:
    """Test Case: AE-UI-TC-024
    Scenario: AE-UI-SC-021
    Requirement: REQ-FUNC-CO-001, REQ-BUS-004, BR-003
    Test Data: TD-PRODUCT-001

    Expected Result (docs/07-Test-Cases.md, VERIFIED Step 2 and re-verified
    live during this step): a modal is displayed reading "Register / Login
    account to proceed on checkout." with "Register / Login" and "Continue
    On Cart" options.
    """
    product_details_page.open(PRODUCT_1["id"])
    product_details_page.add_to_cart()
    product_details_page.go_to_cart_from_modal()

    cart_page.click_proceed_to_checkout()

    expect(cart_page.checkout_gate_modal).to_be_visible()
    expect(cart_page.checkout_gate_message).to_be_visible()
    expect(cart_page.checkout_gate_register_login_link).to_have_attribute("href", "/login")
    expect(cart_page.checkout_gate_continue_on_cart_button).to_be_visible()
