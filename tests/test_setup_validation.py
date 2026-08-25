"""Infrastructure/setup validation only — NOT an Automation Exercise test case.

Deliberately kept out of tests/ui, tests/api, and tests/hybrid (which are
reserved for the 31 approved automated business test cases per
docs/09-Automation-Scope.md and docs/11-Framework-Architecture.md §26) so it
is never mistaken for one of them and never counted toward automation
coverage. It exists solely to prove, at Step 12 (Project Setup), that the
Python + Playwright + pytest foundation is actually runnable: dependencies
import, configuration loads, and each approved browser engine can launch.

This file is expected to be removed or relocated once the real framework
foundation (Step 13) supersedes the need for a standalone infra check.
"""

from __future__ import annotations

import httpx
import pytest
from playwright.sync_api import Playwright

from src.config.settings import settings


def test_configuration_loads_with_expected_defaults() -> None:
    """The settings module resolves without error and has sane defaults."""
    assert settings.aut_base_url == "https://automationexercise.com"
    assert settings.api_base_url == "https://automationexercise.com"
    assert settings.browser in {"chromium", "firefox", "webkit"}
    assert isinstance(settings.headless, bool)
    assert settings.default_timeout_ms > 0
    assert settings.retries >= 0
    assert settings.workers >= 1


def test_httpx_client_importable_and_constructible() -> None:
    """The API-layer dependency (ADR-2, docs/11 §5/§42) is usable."""
    client = httpx.Client(base_url=settings.api_base_url)
    assert client.base_url == settings.api_base_url
    client.close()


@pytest.mark.requires_all_browsers
@pytest.mark.parametrize("engine_name", ["chromium", "firefox", "webkit"])
def test_playwright_browser_launches(engine_name: str, playwright: Playwright) -> None:
    """Each browser engine approved in docs/05 §9 / docs/10 §17 actually launches.

    Parametrized on ``engine_name`` (not ``browser_name``) because
    pytest-playwright already reserves the ``browser_name`` fixture name for
    its own CLI-driven (--browser) parametrization.

    Uses pytest-playwright's own session-scoped ``playwright`` fixture rather
    than opening a second, independent ``sync_playwright()`` context manager
    (the original Step 12 approach) — once the plugin's fixtures are active
    elsewhere in the same session (as they are from Step 13 onward), a second
    manually-opened sync context raises "Sync API inside the asyncio loop".
    Discovered and fixed during Step 13 (docs/13-Core-Framework-
    Development.md records this as a genuine finding, not a silent edit).

    This is the one place all three engines run together — a one-time
    infrastructure check, not a precedent for routine cross-browser execution
    (which remains curated and tiered per docs/10-Automation-Strategy.md §17).
    """
    browser_type = getattr(playwright, engine_name)
    browser = browser_type.launch(headless=settings.headless)
    page = browser.new_page()
    assert page is not None
    browser.close()
