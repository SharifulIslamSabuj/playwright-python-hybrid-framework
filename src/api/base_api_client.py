"""BaseApiClient — the shared API request/response foundation.

Implements docs/11-Framework-Architecture.md §13: base URL handling,
timeout handling, and shared request methods. Uses httpx (ADR-2,
docs/11 §5/§42) rather than Playwright's APIRequestContext, so API tests
carry no browser dependency.

No authentication header is configured — none of the 14 documented
endpoints requires one (docs/02-Application-Analysis.md §10, VERIFIED);
credentials, where relevant (verifyLogin), travel as request parameters,
not headers.

Returns raw httpx.Response objects from every method — this class performs
no status-code or body assertion itself (docs/11 §13: "the client does not
itself assert; assertions remain in the test function"). It contains no
test assertions and no business-endpoint knowledge; that belongs to the
concrete clients (ProductsApiClient, BrandsApiClient, AuthApiClient).
"""

from __future__ import annotations

from typing import Any

import httpx

from src.config.settings import settings
from src.utils.logger import get_logger

_logger = get_logger(__name__)


class BaseApiClient:
    """Thin, reusable wrapper around an httpx.Client for one base URL."""

    def __init__(self, base_url: str | None = None, timeout_ms: int | None = None) -> None:
        resolved_base_url = base_url or settings.api_base_url
        resolved_timeout_s = (timeout_ms or settings.default_timeout_ms) / 1000
        self._client = httpx.Client(base_url=resolved_base_url, timeout=resolved_timeout_s)

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, data: dict[str, Any] | None = None, **kwargs: Any) -> httpx.Response:
        # The AUT's documented API (docs/02-Application-Analysis.md §10) takes
        # request *parameters*, not a JSON body — form-encoding via `data=`
        # matches its actual, verified request shape.
        return self._request("POST", path, data=data, **kwargs)

    def put(self, path: str, data: dict[str, Any] | None = None, **kwargs: Any) -> httpx.Response:
        return self._request("PUT", path, data=data, **kwargs)

    def delete(self, path: str, data: dict[str, Any] | None = None, **kwargs: Any) -> httpx.Response:
        return self._request("DELETE", path, data=data, **kwargs)

    @property
    def base_url(self) -> str:
        return str(self._client.base_url)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "BaseApiClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        _logger.debug("API request: %s %s %s", method, path, {k: v for k, v in kwargs.items() if k != "data"} or "")
        response = self._client.request(method, path, **kwargs)
        _logger.debug("API response: %s %s -> %s", method, path, response.status_code)
        return response
