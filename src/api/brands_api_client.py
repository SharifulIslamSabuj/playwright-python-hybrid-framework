"""BrandsApiClient — brands endpoint.

Serves AE-API-TC-003/004, per docs/11-Framework-Architecture.md §13.
"""

from __future__ import annotations

import httpx

from src.api.base_api_client import BaseApiClient


class BrandsApiClient(BaseApiClient):
    def get_brands_list(self) -> httpx.Response:
        """GET /api/brandsList — AE-API-TC-003."""
        return self.get("/api/brandsList")

    def put_brands_list(self) -> httpx.Response:
        """PUT /api/brandsList — unsupported-method negative case, AE-API-TC-004."""
        return self.put("/api/brandsList")
