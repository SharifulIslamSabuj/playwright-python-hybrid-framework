"""Products/Search API — Automation Scope AUTOMATE cases: AE-API-TC-001,
002, 005, 006.

IMPORTANT, VERIFIED-during-implementation API behavior (see
docs/15-API-Automation.md §11 for full detail): every endpoint on this AUT
returns HTTP 200 at the transport layer, **always** — the documented
status code (200/400/404/405) is carried only inside the JSON response
body as a `responseCode` field. Every test below therefore asserts BOTH
`response.status_code == 200` (the real, constant transport status) AND
`body["responseCode"] == <documented code>` (the AUT's own status
signal) — asserting only `response.status_code` against the documented
code would be asserting something this AUT never actually does.
"""

from __future__ import annotations

import pytest

from src.api.products_api_client import ProductsApiClient
from src.data.products import SEARCH_KEYWORD_VALID


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
def test_ae_api_tc_001_get_products_list(products_api: ProductsApiClient) -> None:
    """Test Case: AE-API-TC-001
    Scenario: AE-API-SC-001
    Requirement: REQ-API-001
    Test Data: None

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 200;
    body contains a non-empty `products` list, each item exposing the
    VERIFIED fields id/name/price/brand/category.
    """
    response = products_api.get_products_list()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0
    first = body["products"][0]
    for key in ("id", "name", "price", "brand", "category"):
        assert key in first


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_ae_api_tc_002_post_products_list_unsupported_method(products_api: ProductsApiClient) -> None:
    """Test Case: AE-API-TC-002
    Scenario: AE-API-SC-002
    Requirement: REQ-API-002
    Test Data: None

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 405,
    message "This request method is not supported."
    """
    response = products_api.post_products_list()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."


@pytest.mark.api
@pytest.mark.regression
def test_ae_api_tc_005_search_product_valid_parameter(products_api: ProductsApiClient) -> None:
    """Test Case: AE-API-TC-005
    Scenario: AE-API-SC-005
    Requirement: REQ-API-005
    Test Data: TD-SEARCH-VALID-001 ("dress")

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 200;
    body contains a non-empty `products` list. This test deliberately does
    NOT assert that every returned product's name contains the keyword —
    docs/03-Requirement-Analysis.md §5 row 5 and docs/14-UI-Automation.md
    §9 both record the search-relevance rule as unresolved; asserting a
    stricter relationship here would assume the very thing still unverified.
    """
    response = products_api.search_product(SEARCH_KEYWORD_VALID)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_ae_api_tc_006_search_product_missing_parameter(products_api: ProductsApiClient) -> None:
    """Test Case: AE-API-TC-006
    Scenario: AE-API-SC-006
    Requirement: REQ-API-006
    Test Data: None (deliberately omitted parameter)

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 400,
    message "Bad request, search_product parameter is missing in POST
    request."
    """
    response = products_api.search_product(None)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert body["message"] == "Bad request, search_product parameter is missing in POST request."
