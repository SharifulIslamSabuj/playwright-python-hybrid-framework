"""Product test-data foundation (TD-PRODUCT-*, TD-SEARCH-*, TD-CATEGORY-*,
TD-BRAND-*, TD-CART-*) per docs/08-Test-Data.md §10-13.

Values below were directly VERIFIED against the live catalog during Step 14
implementation (2026-08-25) — not invented, and not carried over unchanged
from Step 2's earlier pass (product/price text is re-confirmed here since
[08-Test-Data.md] §10 flags catalog data as ENVIRONMENT-SENSITIVE).

These are STATIC references, a deliberate, documented simplification for
Step 14 (UI-only): [05-Test-Strategy.md] §10 and [08-Test-Data.md] §10
recommend live API-sourcing instead, but the API client layer's read
methods are not yet exercised by any test until Step 15 (API Automation).
Migrating these constants to live-sourced values is a natural, low-risk
follow-up once Step 15 lands — tracked as a known limitation in
docs/14-UI-Automation.md, not silently deferred.
"""

from __future__ import annotations

# TD-PRODUCT-001/002/003 — three distinct, verified catalog products.
# Names are stored with normalized (single) whitespace, matching how
# Playwright's text assertions normalize whitespace when comparing.
PRODUCT_1 = {"id": 1, "name": "Blue Top", "price": "Rs. 500"}
PRODUCT_2 = {"id": 2, "name": "Men Tshirt", "price": "Rs. 400"}
PRODUCT_3 = {"id": 3, "name": "Sleeveless Dress", "price": "Rs. 1000"}

# TD-SEARCH-VALID-001 / TD-SEARCH-NOMATCH-001 (docs/08-Test-Data.md §11)
SEARCH_KEYWORD_VALID = "dress"
SEARCH_KEYWORD_NO_MATCH = "zzzznonexistentproductxyz123"

# TD-CATEGORY-001/002 (docs/08-Test-Data.md §12) — VERIFIED route + names;
# the category-ID-to-name mapping question from docs/03 §12 is resolved for
# these two specific entries by this direct verification.
CATEGORY_TOP_LEVEL = "Women"
CATEGORY_SUB_1 = "Dress"
CATEGORY_SUB_2 = "Tops"

# TD-BRAND-001/002 (docs/08-Test-Data.md §12) — VERIFIED hrefs.
BRAND_1_HREF = "/brand_products/Polo"
BRAND_1_NAME = "Polo"
BRAND_2_HREF = "/brand_products/H&M"
BRAND_2_NAME = "H&M"

# TD-CART-QTY-VALID (docs/08-Test-Data.md §13) — REFERENCE-BASED value
# (the TS project's own example quantity), reused here for consistency;
# the AUT places no documented upper bound this project has observed.
CART_QUANTITY_VALID = 4
