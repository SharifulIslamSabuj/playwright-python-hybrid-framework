"""Unique-value generation for dynamic test data.

Implements docs/11-Framework-Architecture.md §22 and the uniqueness strategy
recommended (not asserted as an AUT requirement) in docs/08-Test-Data.md §8:
timestamp-suffixed emails to avoid collision on the shared public
environment, reducing test-dependency and false-failure risk.

Generic and AUT-agnostic: knows nothing about the createAccount payload
shape (that belongs to src/data/, per docs/11 §22's separation rule).
"""

from __future__ import annotations

import time
import uuid


def generate_unique_email(scenario: str, domain: str = "testmail.com") -> str:
    """A collision-resistant email for account-creating test data.

    Pattern: ae_<scenario>_<millisecond-timestamp>_<short-uuid>@<domain>.
    The scenario tag keeps generated addresses traceable back to the
    Test Case/fixture that produced them, matching the naming discipline
    already established in docs/08-Test-Data.md §8 (REFERENCE-BASED on the
    TS project's own pattern, reimplemented independently here).
    """
    safe_scenario = "".join(ch for ch in scenario.lower() if ch.isalnum() or ch == "_") or "run"
    timestamp_ms = int(time.time() * 1000)
    short_uuid = uuid.uuid4().hex[:8]
    return f"ae_{safe_scenario}_{timestamp_ms}_{short_uuid}@{domain}"


def generate_unique_suffix() -> str:
    """A short, collision-resistant suffix for any other uniquely-identified
    test value (e.g., a display name) that isn't an email address."""
    return f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}"
