"""Products module — Automation Scope AUTOMATE cases: AE-UI-TC-011, 012, 013,
019, 020.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from src.data.products import (
    BRAND_1_HREF,
    BRAND_1_NAME,
    BRAND_2_HREF,
    BRAND_2_NAME,
    CATEGORY_SUB_1,
    CATEGORY_SUB_2,
    CATEGORY_TOP_LEVEL,
    SEARCH_KEYWORD_NO_MATCH,
    SEARCH_KEYWORD_VALID,
)
from src.pages.product_details_page import ProductDetailsPage
from src.pages.products_page import ProductsPage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_ae_ui_tc_011_view_all_products_and_product_details(
    products_page: ProductsPage, product_details_page: ProductDetailsPage
) -> None:
    """Test Case: AE-UI-TC-011
    Scenario: AE-UI-SC-011
    Requirement: REQ-FUNC-PR-001, REQ-FUNC-PR-002
    Test Data: TD-PRODUCT-001

    Expected Result (docs/07-Test-Cases.md): the product grid renders; the
    detail page shows name, category path, price, quantity input, Add to
    Cart, Availability, Condition, and Brand — all with non-empty values.
    """
    products_page.open()
    expect(products_page.product_cards.first).to_be_visible()

    products_page.open_first_product_details()

    expect(product_details_page.product_name).to_be_visible()
    expect(product_details_page.product_name).not_to_have_text("")
    expect(product_details_page.category_text).to_contain_text("Category:")
    expect(product_details_page.price).to_contain_text("Rs.")
    expect(product_details_page.quantity_input).to_be_visible()
    expect(product_details_page.add_to_cart_button).to_be_visible()
    expect(product_details_page.availability_text).to_contain_text("Availability")
    expect(product_details_page.condition_text).to_contain_text("Condition")
    expect(product_details_page.brand_text).to_contain_text("Brand")


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_012_search_with_valid_matching_keyword(products_page: ProductsPage) -> None:
    """Test Case: AE-UI-TC-012
    Scenario: AE-UI-SC-012
    Requirement: REQ-FUNC-PR-003, REQ-FUNC-PR-004
    Test Data: TD-SEARCH-VALID-001 ("dress")

    Expected Result (docs/07-Test-Cases.md): a "Searched Products" section
    renders containing at least one result.
    """
    products_page.open()
    products_page.search(SEARCH_KEYWORD_VALID)

    expect(products_page.results_heading).to_have_text("Searched Products")
    expect(products_page.product_cards.first).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_ae_ui_tc_013_search_with_non_matching_keyword(products_page: ProductsPage) -> None:
    """Test Case: AE-UI-TC-013
    Scenario: AE-UI-SC-012
    Requirement: REQ-FUNC-PR-004
    Test Data: TD-SEARCH-NOMATCH-001

    Expected Result — RESOLVED during Step 14 implementation (previously
    REQUIRES VERIFICATION per docs/07-Test-Cases.md): the "Searched
    Products" heading still renders, but zero product cards are shown.
    There is no dedicated "no results found" message — this is a genuine,
    now-VERIFIED finding, recorded in docs/14-UI-Automation.md.
    """
    products_page.open()
    products_page.search(SEARCH_KEYWORD_NO_MATCH)

    expect(products_page.results_heading).to_have_text("Searched Products")
    expect(products_page.product_cards).to_have_count(0)


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_019_view_category_products_and_switch_category(products_page: ProductsPage) -> None:
    """Test Case: AE-UI-TC-019
    Scenario: AE-UI-SC-016
    Requirement: REQ-FUNC-PR-005
    Test Data: TD-CATEGORY-001 (Women > Dress), TD-CATEGORY-002 (Women > Tops)

    Expected Result (docs/07-Test-Cases.md): category-scoped product
    listings render and update when switching sub-category.

    Calls `block_third_party_ads()` before the first navigation: CONFIRMED
    root cause of a real CI failure (GitHub Actions run 33021750130,
    2026-08-26) via direct screenshot evidence — a full-screen third-party
    ad/survey vignette (a Google-served "Answer questions to support great
    content" overlay in one occurrence, a JustAnswer chat prompt in the
    other) intercepted the click on the test's SECOND navigation in both
    failures, matching the same confirmed ad-injection source already
    documented for the Hybrid test (docs/16-Hybrid-E2E-Automation.md §20).
    Vignette-style ads characteristically trigger after a prior page view
    in the same session — consistent with both failures occurring on the
    second `products_page.open()` call, never the first. This blocks the
    confirmed ad domains at the network level (no business assertion
    changed, no wait/retry/sleep added) rather than working around a
    symptom.
    """
    products_page.block_third_party_ads()
    products_page.open()

    products_page.open_category(CATEGORY_TOP_LEVEL, CATEGORY_SUB_1)
    expect(products_page.results_heading).to_contain_text(f"{CATEGORY_SUB_1} Products")
    expect(products_page.product_cards.first).to_be_visible()

    products_page.open()
    products_page.open_category(CATEGORY_TOP_LEVEL, CATEGORY_SUB_2)
    expect(products_page.results_heading).to_contain_text(f"{CATEGORY_SUB_2} Products")
    expect(products_page.product_cards.first).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_ae_ui_tc_020_view_brand_products_and_switch_brand(products_page: ProductsPage) -> None:
    """Test Case: AE-UI-TC-020
    Scenario: AE-UI-SC-017
    Requirement: REQ-FUNC-PR-006
    Test Data: TD-BRAND-001 (Polo), TD-BRAND-002 (H&M)

    Expected Result (docs/07-Test-Cases.md): brand-scoped listings render
    and update when switching brand.

    Calls `block_third_party_ads()` before the first navigation — same
    confirmed root cause and evidence as AE-UI-TC-019 above (GitHub
    Actions run 33021750130): a third-party ad vignette intercepted the
    click on this test's second navigation.
    """
    products_page.block_third_party_ads()
    products_page.open()

    products_page.open_brand(BRAND_1_HREF)
    expect(products_page.results_heading).to_contain_text(f"{BRAND_1_NAME} Products")
    expect(products_page.product_cards.first).to_be_visible()

    products_page.open()
    products_page.open_brand(BRAND_2_HREF)
    expect(products_page.results_heading).to_contain_text(f"{BRAND_2_NAME} Products")
    expect(products_page.product_cards.first).to_be_visible()
