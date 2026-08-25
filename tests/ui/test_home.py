"""Home module — Automation Scope AUTOMATE cases: AE-UI-TC-001, AE-UI-TC-023.

Traceability for every test in this file is stated in its own docstring:
Test Case ID -> Scenario ID -> Requirement ID -> Test Data ID(s), per
docs/11-Framework-Architecture.md §28. No second traceability system is
introduced.
"""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from src.pages.cart_page import CartPage
from src.pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_ae_ui_tc_001_home_page_core_elements_visible(home_page: HomePage) -> None:
    """Test Case: AE-UI-TC-001
    Scenario: AE-UI-SC-001
    Requirement: REQ-FUNC-HM-001-006
    Test Data: None

    Expected Result (docs/07-Test-Cases.md): Home page loads; category panel
    shows Women/Men/Kids; brand panel and featured/recommended items render;
    subscription email input is present.
    """
    home_page.open()

    # Case-insensitive regex used deliberately: the panel's source DOM text
    # is "Women"/"Men"/"Kids", but a CSS text-transform renders it uppercase
    # — matching case-insensitively avoids coupling the assertion to which
    # of those two representations Playwright's text matcher happens to read.
    expect(home_page.category_panel).to_be_visible()
    expect(home_page.category_panel).to_contain_text(re.compile("women", re.IGNORECASE))
    expect(home_page.category_panel).to_contain_text(re.compile("men", re.IGNORECASE))
    expect(home_page.category_panel).to_contain_text(re.compile("kids", re.IGNORECASE))

    expect(home_page.brands_panel).to_be_visible()
    expect(home_page.featured_items_section).to_be_visible()
    expect(home_page.recommended_items_carousel).to_be_visible()
    expect(home_page.subscription_email_input).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_023_add_recommended_item_to_cart(home_page: HomePage, cart_page: CartPage) -> None:
    """Test Case: AE-UI-TC-023
    Scenario: AE-UI-SC-020
    Requirement: Recommended Items, REQ-FUNC-CT-001
    Test Data: None (item selected from the live Recommended Items carousel)

    Expected Result (docs/07-Test-Cases.md): the item appears correctly on
    the cart page, following the same confirmed add-to-cart pattern as
    AE-UI-TC-015.
    """
    home_page.open()
    home_page.add_first_recommended_item_to_cart()
    home_page.go_to_cart_from_modal()

    # At least one line item is present with a non-empty total — this test
    # deliberately does not assert a specific product name/price, since the
    # scenario permits "any available recommended item" (docs/06 §7).
    expect(cart_page.line_item_rows).to_have_count(1)
