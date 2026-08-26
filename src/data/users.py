"""User/account test-data foundation.

Implements the builder pattern recommended in docs/08-Test-Data.md §22 for
the repeated 16-field account-creation shape (TD-USER-NEW-*), plus the two
fixed, non-account-creating datasets that are safe to define now
(TD-USER-INVALID-001, already VERIFIED usable per docs/08 §7/§26).

Deliberately NOT the full 33-dataset TD-* catalog from docs/08-Test-Data.md
— only the foundation this step's architecture requires. Datasets tied to
account creation (TD-USER-NEW-002/003/004) and Checkout/Contact/Subscription
data are added when the business Test Cases that need them are implemented
(Steps 14+), consistent with "do not create all final TD-* datasets in this
step" (Step 13 instructions, Section G).

The registration DDT dataset (`REGISTRATION_PROFILES`) is sourced from
tests/data/registration_test_data.xlsx via src/data/excel_reader.py —
Excel, not this module, is the authoritative DDT source; this module only
adapts the Excel rows into the `NewUserPayload` shape and provides the
DDT_ONLY/HYBRID/FULL_DYNAMIC data-strategy layer built on top of it.

TEST_ACCOUNT_PASSWORD is disposable test-account data, not a real secret —
per docs/11-Framework-Architecture.md §37, no application secret exists to
protect (the AUT requires none). This mirrors docs/08-Test-Data.md §23's own
distinction and the previous TypeScript project's own committed users.json
convention (REFERENCE KNOWLEDGE: the practice of committing disposable
test-account passwords in test data, not the literal value).
"""

from __future__ import annotations

import random
from enum import Enum

from src.data.excel_reader import read_registration_profiles
from src.data.models import Credentials, NewUserPayload
from src.utils.data_generator import (
    generate_company_name,
    generate_first_name,
    generate_last_name,
    generate_mobile_number,
    generate_password,
    generate_street_address,
    generate_unique_email,
)

TEST_ACCOUNT_PASSWORD = "AeAutomation@2026"

# REFERENCE-BASED template (docs/08-Test-Data.md §7, TD-ADDRESS-001) — field
# *names* are VERIFIED against the createAccount API schema; these specific
# values are placeholder test data, not required by the AUT.
ADDRESS_TEMPLATE: dict[str, str] = {
    "title": "Mr",
    "birth_date": "10",
    "birth_month": "May",
    "birth_year": "1990",
    "firstname": "Automation",
    "lastname": "Engineer",
    "company": "QA Automation",
    "address1": "123 Test Automation Street",
    "address2": "Suite 456",
    "country": "United States",
    "zipcode": "94105",
    "state": "California",
    "city": "San Francisco",
    "mobile_number": "1234567890",
}

# TD-USER-INVALID-001 (docs/08-Test-Data.md §7) — fabricated, never a real
# account. VERIFIED usable per Step 2's own execution of this exact negative
# login case.
INVALID_CREDENTIALS: Credentials = {
    "email": "invalid_user_ae_automation@testmail.com",
    "password": "WrongPassword123",
}

# DDT dataset for the account-creation Test Cases (AE-UI-TC-004,
# AE-API-TC-011/012), sourced from tests/data/registration_test_data.xlsx
# (Excel is now the authoritative DDT source, per the Excel-DDT migration —
# no registration profile data is hardcoded in this module anymore; the
# ADDRESS_TEMPLATE constant above remains only as `build_new_user_payload`'s
# separate, pre-existing single-profile data, untouched by this migration).
# Two structurally distinct, equally-valid registration profiles, both
# satisfying the createAccount schema (docs/02-Application-Analysis.md §10,
# VERIFIED) — only the concrete data differs, per docs/08-Test-Data.md §22's
# builder-pattern intent. `read_registration_profiles` fails fast
# (`ExcelDataError`) at import time if the workbook is missing/malformed,
# so a broken DDT source is caught at collection, not mid-test.
_EXCEL_PROFILES: list[dict[str, str]] = read_registration_profiles()

# Excel-sourced profile names, in file row order — used for pytest
# parametrize IDs elsewhere so the DDT dataset's own identifiers (not a
# separately hand-maintained id list) drive traceability (Phase 6/9 of the
# Excel-DDT migration: "meaningful pytest IDs... from Excel").
REGISTRATION_PROFILE_NAMES: list[str] = [p["profile_name"] for p in _EXCEL_PROFILES]

# The NewUserPayload-shaped 14-key profile dicts `build_user_data` below
# consumes — identical shape to the old hardcoded list, metadata
# (test_data_id/profile_name) stripped since those aren't payload fields.
REGISTRATION_PROFILES: list[dict[str, str]] = [
    {k: v for k, v in profile.items() if k not in ("test_data_id", "profile_name")}
    for profile in _EXCEL_PROFILES
]


class DataMode(str, Enum):
    """The three registration data-supply strategies AE-UI-TC-004 and
    AE-API-TC-011/012 are parametrized over. Only `identity` fields
    (name/email/password/mobile) are ever runtime-generated in DDT_ONLY —
    everything else always traces back to a VERIFIED-schema profile in
    `REGISTRATION_PROFILES`, so no mode can produce a value the AUT's
    createAccount schema hasn't already been confirmed to accept
    (docs/02-Application-Analysis.md §10)."""

    DDT_ONLY = "ddt-only"
    HYBRID = "hybrid"
    FULL_DYNAMIC = "full-dynamic"


# Country/state/city triples used by FULL_DYNAMIC — deliberately reused from
# REGISTRATION_PROFILES rather than invented, since only "United States" and
# "Canada" (among this project's live-verified country dropdown options,
# docs/14-UI-Automation.md) have a state/city pairing this project has
# actually exercised. FULL_DYNAMIC varies name/company/address-line/mobile
# freely but stays within already-VERIFIED country/state/city combinations.
_FULL_DYNAMIC_LOCATIONS: list[tuple[str, str, str]] = [
    (p["country"], p["state"], p["city"]) for p in REGISTRATION_PROFILES
]


def _hybrid_overrides() -> dict[str, str]:
    """HYBRID mode's runtime-generated fields — identity-ish values that
    are meaningful to regenerate per execution, layered onto a DDT profile
    that supplies everything else (address/company/locale)."""
    return {
        "firstname": generate_first_name(),
        "lastname": generate_last_name(),
        "mobile_number": generate_mobile_number(),
    }


def _full_dynamic_profile() -> dict[str, str]:
    """FULL_DYNAMIC mode's complete profile — every field generated, except
    country/state/city, which are drawn from an already-VERIFIED pairing
    (see `_FULL_DYNAMIC_LOCATIONS` above) rather than invented."""
    country, state, city = random.choice(_FULL_DYNAMIC_LOCATIONS)
    return {
        "title": random.choice(["Mr", "Mrs"]),
        "birth_date": str(random.randint(1, 28)),
        "birth_month": random.choice(
            [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ]
        ),
        "birth_year": str(random.randint(1970, 2005)),
        "firstname": generate_first_name(),
        "lastname": generate_last_name(),
        "company": generate_company_name(),
        "address1": generate_street_address(),
        "address2": f"Unit {random.randint(1, 99)}",
        "country": country,
        "state": state,
        "city": city,
        "zipcode": REGISTRATION_PROFILES[0]["zipcode"] if country == REGISTRATION_PROFILES[0]["country"] else REGISTRATION_PROFILES[1]["zipcode"],
        "mobile_number": generate_mobile_number(),
    }


def build_user_data(scenario: str, mode: DataMode, profile_index: int = 0) -> NewUserPayload:
    """Single entry point for all three data-supply strategies — the
    registration test logic (AE-UI-TC-004, AE-API-TC-011/012) is identical
    across modes; only this function's internal branch changes what data
    it returns:

    - DDT_ONLY: every field from `REGISTRATION_PROFILES[profile_index]`,
      unmodified (except the always-fresh email/password every mode needs).
    - HYBRID: the same DDT profile, with firstname/lastname/mobile_number
      overridden by runtime-generated values.
    - FULL_DYNAMIC: every field runtime-generated, except country/state/
      city, which stay within an already-VERIFIED pairing.

    A fresh, unique email is generated in every mode (docs/08-Test-Data.md
    §8) — account-creation executions must never reuse an email regardless
    of data strategy. Returns a payload only — no network call, no account
    created, the same non-side-effecting contract every builder in this
    module has."""
    if mode is DataMode.DDT_ONLY:
        profile = dict(REGISTRATION_PROFILES[profile_index])
        password = TEST_ACCOUNT_PASSWORD
    elif mode is DataMode.HYBRID:
        profile = dict(REGISTRATION_PROFILES[profile_index])
        profile.update(_hybrid_overrides())
        password = generate_password()
    elif mode is DataMode.FULL_DYNAMIC:
        profile = _full_dynamic_profile()
        password = generate_password()
    else:  # pragma: no cover - exhaustive Enum, defensive only
        raise ValueError(f"Unknown DataMode: {mode!r}")

    email = generate_unique_email(f"{scenario}_{mode.value}")
    return NewUserPayload(
        name=f'{profile["firstname"]} {profile["lastname"]}',
        email=email,
        password=password,
        title=profile["title"],
        birth_date=profile["birth_date"],
        birth_month=profile["birth_month"],
        birth_year=profile["birth_year"],
        firstname=profile["firstname"],
        lastname=profile["lastname"],
        company=profile["company"],
        address1=profile["address1"],
        address2=profile["address2"],
        country=profile["country"],
        zipcode=profile["zipcode"],
        state=profile["state"],
        city=profile["city"],
        mobile_number=profile["mobile_number"],
    )


def build_new_user_payload(scenario: str) -> NewUserPayload:
    """Build a TD-USER-NEW-*-shaped payload with a freshly generated, unique
    email (docs/08-Test-Data.md §8 uniqueness strategy). `scenario` should
    identify the calling Test Case/fixture (e.g. "ui_tc_004") so generated
    emails stay traceable, matching docs/11-Framework-Architecture.md §28.

    Returns a payload only — this function performs no network call and
    creates no account. Actually creating the account remains the
    responsibility of a future, explicitly authorized business Test Case
    (docs/09-Automation-Scope.md §12/§30 item 4).
    """
    email = generate_unique_email(scenario)
    return NewUserPayload(
        name="Automation User",
        email=email,
        password=TEST_ACCOUNT_PASSWORD,
        title=ADDRESS_TEMPLATE["title"],
        birth_date=ADDRESS_TEMPLATE["birth_date"],
        birth_month=ADDRESS_TEMPLATE["birth_month"],
        birth_year=ADDRESS_TEMPLATE["birth_year"],
        firstname=ADDRESS_TEMPLATE["firstname"],
        lastname=ADDRESS_TEMPLATE["lastname"],
        company=ADDRESS_TEMPLATE["company"],
        address1=ADDRESS_TEMPLATE["address1"],
        address2=ADDRESS_TEMPLATE["address2"],
        country=ADDRESS_TEMPLATE["country"],
        zipcode=ADDRESS_TEMPLATE["zipcode"],
        state=ADDRESS_TEMPLATE["state"],
        city=ADDRESS_TEMPLATE["city"],
        mobile_number=ADDRESS_TEMPLATE["mobile_number"],
    )
