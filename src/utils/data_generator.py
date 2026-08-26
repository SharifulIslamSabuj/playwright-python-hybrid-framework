"""Unique-value generation for dynamic test data.

Implements docs/11-Framework-Architecture.md §22 and the uniqueness strategy
recommended (not asserted as an AUT requirement) in docs/08-Test-Data.md §8:
timestamp-suffixed emails to avoid collision on the shared public
environment, reducing test-dependency and false-failure risk.

Generic and AUT-agnostic: knows nothing about the createAccount payload
shape (that belongs to src/data/, per docs/11 §22's separation rule).
"""

from __future__ import annotations

import random
import time
import uuid

# Small curated pools, not Faker: this project's dependency list is
# exact-pinned and deliberately minimal (docs/12-Project-Setup.md), and
# these stdlib-only pools satisfy "realistic, not Lorem-Ipsum" without a
# new dependency. Plausible values, not claimed to be real people/places.
_FIRST_NAMES = ("Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Avery")
_LAST_NAMES = ("Mitchell", "Reynolds", "Carter", "Bennett", "Foster", "Hayes", "Coleman", "Brooks")
_STREET_NAMES = ("Maple", "Cedar", "Birch", "Willow", "Elm", "Oak", "Pine", "Aspen")
_COMPANY_SUFFIXES = ("Solutions", "Holdings", "Group", "Labs", "Partners")


def generate_first_name() -> str:
    return random.choice(_FIRST_NAMES)


def generate_last_name() -> str:
    return random.choice(_LAST_NAMES)


def generate_company_name() -> str:
    return f"{random.choice(_LAST_NAMES)} {random.choice(_COMPANY_SUFFIXES)}"


def generate_street_address() -> str:
    return f"{random.randint(10, 9999)} {random.choice(_STREET_NAMES)} Street"


def generate_mobile_number() -> str:
    """10 digits — matches the AUT's `mobile_number` field shape used by
    every existing verified dataset (ADDRESS_TEMPLATE, src/data/users.py)."""
    return "".join(str(random.randint(0, 9)) for _ in range(10))


def generate_zipcode() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(5))


def generate_password() -> str:
    """A syntactically varied but disposable test password — not a secret,
    same non-sensitive status as TEST_ACCOUNT_PASSWORD (src/data/users.py)."""
    return f"Ae{uuid.uuid4().hex[:10]}!1"


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
