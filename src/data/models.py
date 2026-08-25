"""Typed data models for AUT payloads.

Implements the "typed models where valuable" opportunity named in
docs/11-Framework-Architecture.md §41: a single, typed shape for the
16-field account payload (verified against the live `createAccount`/
`updateAccount` API schema in docs/02-Application-Analysis.md §10) reduces
the risk of a silent field-name typo across the 5+ Test Cases
(docs/08-Test-Data.md §7/§28) that reuse this exact shape.

This module defines shape only — no data values live here.
"""

from __future__ import annotations

from typing import TypedDict


class NewUserPayload(TypedDict):
    """The full account payload accepted by POST /api/createAccount and
    PUT /api/updateAccount (docs/02-Application-Analysis.md §10, VERIFIED)."""

    name: str
    email: str
    password: str
    title: str
    birth_date: str
    birth_month: str
    birth_year: str
    firstname: str
    lastname: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str


class Credentials(TypedDict):
    """A bare email/password pair, e.g. for /api/verifyLogin or UI login."""

    email: str
    password: str
