"""Brands API — Automation Scope AUTOMATE cases: AE-API-TC-003, 004.

See tests/api/test_products_api.py's module docstring for why every
assertion checks both `response.status_code == 200` (constant transport
status on this AUT) and the body's `responseCode` field.
"""

from __future__ import annotations

import pytest

from src.api.brands_api_client import BrandsApiClient


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
def test_ae_api_tc_003_get_brands_list(brands_api: BrandsApiClient) -> None:
    """Test Case: AE-API-TC-003
    Scenario: AE-API-SC-003
    Requirement: REQ-API-003
    Test Data: None

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 200;
    body contains a non-empty `brands` list, each item exposing id/brand.
    """
    response = brands_api.get_brands_list()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0
    first = body["brands"][0]
    assert "id" in first
    assert "brand" in first


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_ae_api_tc_004_put_brands_list_unsupported_method(brands_api: BrandsApiClient) -> None:
    """Test Case: AE-API-TC-004
    Scenario: AE-API-SC-004
    Requirement: REQ-API-004
    Test Data: None

    Expected Result (docs/07-Test-Cases.md, VERIFIED): responseCode 405,
    message "This request method is not supported."
    """
    response = brands_api.put_brands_list()

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."
