"""AuthApiClient — login-verification and account-lifecycle endpoints.

Serves AE-API-TC-007/008/009/010/011/012/014, per
docs/11-Framework-Architecture.md §13.

`update_account` (PUT /api/updateAccount) is deliberately NOT implemented —
it serves only AE-API-TC-013, which docs/09-Automation-Scope.md §5
classifies MANUAL, not AUTOMATE. Implementing it now would be unused code
against a case this project has not approved for automation
(docs/11-Framework-Architecture.md §13's own stated rule).

`create_account`/`delete_account` build requests only — calling them still
performs a real, state-mutating HTTP request against the shared public AUT.
Per docs/09-Automation-Scope.md §12/§30 item 4, that execution requires
explicit QA Lead authorization; this module defines the capability, it does
not exercise it (no test in this project calls these two methods yet).
"""

from __future__ import annotations

import httpx

from src.api.base_api_client import BaseApiClient
from src.data.models import NewUserPayload


class AuthApiClient(BaseApiClient):
    def verify_login(self, email: str | None, password: str | None) -> httpx.Response:
        """POST /api/verifyLogin — AE-API-TC-007 (valid), 008 (invalid), and
        009 (omit email, by passing None)."""
        data: dict[str, str] = {}
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password
        return self.post("/api/verifyLogin", data=data or None)

    def delete_verify_login(self) -> httpx.Response:
        """DELETE /api/verifyLogin — unsupported-method negative case, AE-API-TC-010."""
        return self.delete("/api/verifyLogin")

    def create_account(self, payload: NewUserPayload) -> httpx.Response:
        """POST /api/createAccount — AE-API-TC-011.

        State-mutating; execution-restricted (see module docstring).
        """
        return self.post("/api/createAccount", data=dict(payload))

    def delete_account(self, email: str, password: str) -> httpx.Response:
        """DELETE /api/deleteAccount — AE-API-TC-012.

        Must always be paired with a prior create_account call for the same
        account (docs/11-Framework-Architecture.md §13/§14).
        """
        return self.delete("/api/deleteAccount", data={"email": email, "password": password})

    def get_user_detail_by_email(self, email: str) -> httpx.Response:
        """GET /api/getUserDetailByEmail — AE-API-TC-014."""
        return self.get("/api/getUserDetailByEmail", params={"email": email})
