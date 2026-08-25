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

TEST_ACCOUNT_PASSWORD is disposable test-account data, not a real secret —
per docs/11-Framework-Architecture.md §37, no application secret exists to
protect (the AUT requires none). This mirrors docs/08-Test-Data.md §23's own
distinction and the previous TypeScript project's own committed users.json
convention (REFERENCE KNOWLEDGE: the practice of committing disposable
test-account passwords in test data, not the literal value).
"""

from __future__ import annotations

from src.data.models import Credentials, NewUserPayload
from src.utils.data_generator import generate_unique_email

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
