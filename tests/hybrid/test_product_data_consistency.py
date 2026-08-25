"""Hybrid E2E — the single Automation Scope AUTOMATE Hybrid case: AE-E2E-TC-003.

AE-E2E-TC-001 and AE-E2E-TC-002 remain DEFERRED (docs/09-Automation-Scope.md
§5) and are NOT implemented here or anywhere in this project — see
docs/16-Hybrid-E2E-Automation.md §27 for why.

Architecture: this test is the ONLY place the API and UI layers are used
together in the same test (docs/11-Framework-Architecture.md §10, ADR-7).
It orchestrates two already-existing, unmodified components —
`ProductsApiClient.get_products_list()` (Step 13/15) and
`ProductsPage.get_rendered_products()` (Step 14/16, DOM-reading only, no
HTTP) — without adding a new abstraction layer. No HTTP call is made by
the Page Object; no DOM/browser call is made by the API client.

Per docs/15-API-Automation.md §11's VERIFIED finding, the transport-level
HTTP status and the AUT's own `responseCode` (in the JSON body) are two
separate facts on this AUT and are asserted separately below.
"""

from __future__ import annotations

import pytest

from src.api.products_api_client import ProductsApiClient
from src.pages.products_page import ProductsPage


@pytest.mark.hybrid
@pytest.mark.regression
def test_ae_e2e_tc_003_ui_product_listing_matches_api_product_data(
    products_api: ProductsApiClient, products_page: ProductsPage
) -> None:
    """Test Case: AE-E2E-TC-003
    Scenario: AE-E2E-SC-003
    Requirement: REQ-E2E-003
    Test Data: None (read-only; API result is captured live as the oracle
    for the UI comparison, per docs/08-Test-Data.md §20 — no static
    TD-PRODUCT-* literal is used, since the whole point is comparing
    against whatever the live catalog actually contains right now)

    Business objective: prove the Products page renders the same catalog
    data (name, price) the backend API actually holds — removing reliance
    on hard-coded UI expectations and catching a UI/backend rendering
    mismatch that neither a pure-UI nor a pure-API test could catch alone
    (docs/07-Test-Cases.md AE-E2E-TC-003, docs/10-Automation-Strategy.md §6,
    docs/11-Framework-Architecture.md §10).

    Expected Result: every product rendered on the UI has a matching
    (name, price) pair in the API's product list, and the two sides report
    the same product count.
    """
    # --- API layer: retrieve the oracle data (AE-API-TC-001's endpoint,
    # reused unmodified — this is not a re-implementation of AE-API-TC-001,
    # it is the same client method used for a different purpose here) ---
    api_response = products_api.get_products_list()

    # Transport status and the AUT's own responseCode are two separate
    # facts on this AUT (docs/15-API-Automation.md §11) — asserted
    # separately, not conflated.
    assert api_response.status_code == 200
    api_body = api_response.json()
    assert api_body["responseCode"] == 200
    api_products = api_body["products"]
    assert len(api_products) > 0
    api_pairs = {(product["name"], product["price"]) for product in api_products}

    # --- UI layer: retrieve what a real user actually sees ---
    # block_third_party_ads() is called BEFORE navigation: the AUT genuinely
    # embeds Google Ads/Ad-Traffic-Quality/Funding-Choices scripts (VERIFIED
    # via live network capture — docs/16-Hybrid-E2E-Automation.md §20) whose
    # annotation system mutates product-name text nodes by injecting
    # `google-anno`/`google-anno-skip` elements directly inside them. Without
    # this, bulk text extraction across all 34 products is non-deterministic
    # ad noise, not genuine AUT/UI data — blocking the specific, confirmed ad
    # domains is standard, principled test practice for a deterministic
    # cross-layer comparison, not a weakened assertion (the comparison logic
    # itself is unchanged; only third-party ad noise is excluded).
    products_page.block_third_party_ads()
    products_page.open()
    ui_products = products_page.get_rendered_products()
    assert len(ui_products) > 0
    ui_pairs = {(product["name"], product["price"]) for product in ui_products}

    # --- Cross-layer assertion: the actual value of this Hybrid test.
    # Not a weakened "something was returned" check — this fails if the UI
    # renders any (name, price) combination the API's own data does not
    # contain, which a UI-only or API-only test could not detect. ---
    mismatched = ui_pairs - api_pairs
    assert not mismatched, (
        "UI rendered product(s) not found in the API's product data — "
        f"possible UI/backend data mismatch: {mismatched}"
    )
    assert len(ui_products) == len(api_products), (
        f"UI rendered {len(ui_products)} products but the API reports "
        f"{len(api_products)} — count mismatch between layers"
    )
