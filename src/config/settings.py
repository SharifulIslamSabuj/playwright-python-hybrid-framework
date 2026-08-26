"""Centralized configuration foundation.

Implements docs/11-Framework-Architecture.md §16 (Configuration Architecture).
Every value is environment-variable driven with a sensible default, so no
value is ever hard-coded in test/page/API code. This module is the single
place execution configuration is read from.

Finalized at Step 13 (Core Framework Development) on top of the skeleton
created at Step 12 (Project Setup): adds computed report-artifact paths
consumed by the reporting/diagnostics foundation (docs/13 §J). Still
contains no business logic, page object, or API client code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Loads a local .env if present; safe no-op otherwise (e.g., in CI, where
# real configuration is supplied directly as environment variables).
load_dotenv()


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    """Execution configuration, resolved once at import time.

    Field-by-field mapping to docs/11-Framework-Architecture.md §16:
    base URL, browser, headless/headed, timeout, retries, workers, report dir.
    """

    aut_base_url: str = os.getenv("AUT_BASE_URL", "https://automationexercise.com")
    api_base_url: str = os.getenv("API_BASE_URL", "https://automationexercise.com")

    browser: str = os.getenv("BROWSER", "chromium")
    headless: bool = _env_bool("HEADLESS", True)

    default_timeout_ms: int = _env_int("DEFAULT_TIMEOUT_MS", 30_000)
    expect_timeout_ms: int = _env_int("EXPECT_TIMEOUT_MS", 5_000)

    retries: int = _env_int("RETRIES", 0)
    workers: int = _env_int("WORKERS", 1)

    report_dir: str = os.getenv("REPORT_DIR", "reports")

    # Durable accounts (docs/08-Test-Data.md §7). Intentionally may be empty
    # until QA-Lead-authorized provisioning occurs (docs/09-Automation-Scope.md
    # §12/§30 item 4) — consuming code must handle the empty case explicitly
    # rather than assume a value exists.
    durable_valid_user_email: str = os.getenv("DURABLE_VALID_USER_EMAIL", "")
    durable_valid_user_password: str = os.getenv("DURABLE_VALID_USER_PASSWORD", "")
    durable_existing_user_email: str = os.getenv("DURABLE_EXISTING_USER_EMAIL", "")

    # Separate, narrower gate from the three durable-account fields above:
    # this one covers actually CREATING or DELETING an account (AE-UI-TC-004,
    # AE-API-TC-011/012), not merely reading/logging into one that already
    # exists. Defaults False and must never be defaulted True — see
    # docs/09-Automation-Scope.md §12/§30 item 4 and docs/07-Test-Cases.md
    # AE-API-TC-011 ("this assistant does not perform account creation
    # unilaterally"). Setting this to true is a human operator's own choice
    # in their own execution environment; it is never set by this project's
    # AI assistant itself under any circumstance.
    account_creation_execution_authorized: bool = _env_bool(
        "ACCOUNT_CREATION_EXECUTION_AUTHORIZED", False
    )

    @property
    def report_dir_path(self) -> Path:
        return Path(self.report_dir)

    @property
    def screenshots_dir(self) -> Path:
        return self.report_dir_path / "screenshots"

    @property
    def traces_dir(self) -> Path:
        return self.report_dir_path / "traces"

    @property
    def videos_dir(self) -> Path:
        return self.report_dir_path / "videos"

    @property
    def html_report_path(self) -> Path:
        return self.report_dir_path / "html" / "report.html"

    def has_durable_valid_account(self) -> bool:
        """False until the account is provisioned under QA Lead authorization
        (docs/09-Automation-Scope.md §12/§30 item 4). Callers must check this
        explicitly rather than assume the credential fields are populated."""
        return bool(self.durable_valid_user_email and self.durable_valid_user_password)

    def has_durable_existing_account(self) -> bool:
        return bool(self.durable_existing_user_email)

    def has_account_creation_execution_authorization(self) -> bool:
        """False unless a human operator has explicitly set
        ACCOUNT_CREATION_EXECUTION_AUTHORIZED=true in their own environment.
        Callers must check this explicitly before creating or deleting a
        real account — never assume it."""
        return self.account_creation_execution_authorized


settings = Settings()
