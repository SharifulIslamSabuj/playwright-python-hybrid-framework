"""ProductsApiClient — products/search endpoints.

Serves AE-API-TC-001/002/005/006, per docs/11-Framework-Architecture.md §13.
Endpoints and methods are exactly those VERIFIED in
docs/02-Application-Analysis.md §10 — none invented.

Methods return the raw httpx.Response; no assertion happens here (that is
each Test Case's own responsibility, implemented at Step 15).
"""

from __future__ import annotations

import httpx

from src.api.base_api_client import BaseApiClient


class ProductsApiClient(BaseApiClient):
    def get_products_list(self) -> httpx.Response:
        """GET /api/productsList — AE-API-TC-001."""
        return self.get("/api/productsList")

    def post_products_list(self) -> httpx.Response:
        """POST /api/productsList — unsupported-method negative case, AE-API-TC-002."""
        return self.post("/api/productsList")

    def search_product(self, search_product: str | None = None) -> httpx.Response:
        """POST /api/searchProduct — AE-API-TC-005 (with `search_product`) and
        AE-API-TC-006 (omit it, by passing None)."""
        data = {"search_product": search_product} if search_product is not None else None
        return self.post("/api/searchProduct", data=data)
