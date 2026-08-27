"""TEMPORARY — STEP 14 GAP B: real GitHub Actions failure-path validation.

NOT part of the permanent test suite. Not a business Test Case, not
approved scope, carries no marker (deliberately excluded from every
marker-filtered CI job: pr_main_regression, nightly_regression, and
release_validation all select by marker/explicit path and will never
collect this file). Picked up only by full_project_validation's
unfiltered `pytest -v`, the one job already wired with Allure CLI
install/generate + the existing artifact upload.

Removed immediately after the real CI evidence is collected — see the
STEP 14 GAP B report for the cleanup commit SHA.
"""

from __future__ import annotations

from src.pages.home_page import HomePage


def test_step14_ci_failure_validation(home_page: HomePage) -> None:
    home_page.open()
    assert False, "STEP 14 CI FAILURE VALIDATION — intentional failure"
