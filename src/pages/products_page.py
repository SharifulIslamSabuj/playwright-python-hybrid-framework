"""ProductsPage.

Serves AE-UI-TC-011 (listing part), 012 (search), 013 (search negative),
019 (category), 020 (brand), per docs/11-Framework-Architecture.md §11.

Locators verified live against https://automationexercise.com during Step 14
implementation (2026-08-25).
"""

from __future__ import annotations

from playwright.sync_api import Locator

from src.pages.base_page import BasePage


class ProductsPage(BasePage):
    """The Automation Exercise all-products / search / category / brand page."""

    def open(self) -> None:
        self.goto("products")

    @property
    def search_input(self) -> Locator:
        return self.page.locator("#search_product")

    @property
    def search_button(self) -> Locator:
        return self.page.locator("#submit_search")

    @property
    def results_heading(self) -> Locator:
        """Shared by the search, category, and brand result pages — all three
        render the same `.title.text-center` heading element."""
        return self.page.locator(".title.text-center")

    @property
    def product_cards(self) -> Locator:
        return self.page.locator(".product-image-wrapper")

    def get_rendered_products(self) -> list[dict[str, str]]:
        """Extracts {name, price} for every rendered product card.

        The UI-side half of AE-E2E-TC-003's cross-layer comparison
        (docs/07-Test-Cases.md, docs/16-Hybrid-E2E-Automation.md): DOM
        reading belongs in the Page Object, not duplicated inline in the
        Hybrid test (docs/11-Framework-Architecture.md §11). No HTTP call
        is made here — this method only reads what the browser already
        rendered. Locators verified live during Step 14 implementation:
        each `.product-image-wrapper` card's name/price live in
        `.productinfo p` / `.productinfo h2` respectively.
        """
        cards = self.product_cards
        count = cards.count()
        return [
            {
                "name": cards.nth(i).locator(".productinfo p").inner_text(),
                "price": cards.nth(i).locator(".productinfo h2").inner_text(),
            }
            for i in range(count)
        ]

    def search(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        self.search_button.click()

    def open_first_product_details(self) -> None:
        """AE-UI-TC-011: click "View Product" on the first listed item."""
        self.product_cards.first.get_by_role("link", name="View Product").click()

    @property
    def category_panel(self) -> Locator:
        return self.page.locator(".category-products")

    def open_category(self, top_level_name: str, sub_category_name: str) -> None:
        """Expands the named top-level accordion panel (e.g. "Women"), then
        clicks the named sub-category link (e.g. "Dress") — the panel must
        be expanded first, since Bootstrap's `.collapse` hides it until then
        and Playwright will not click a non-actionable (hidden) element.

        Two deliberate departures from a plain `get_by_role("link", name=...)`
        call, both VERIFIED during Step 14 implementation:

        1. Scoped to `.category_panel`, not the whole page — the live
           `/products` page was found to carry third-party ad/interstitial-
           injected elements with `role="link"` and `aria-label`s like
           "Women's Clothing"/"Women's T-Shirts" (Google-vignette-style DOM
           injection, the same class of environmental noise flagged for the
           cart page in docs/02-Application-Analysis.md §13). An unscoped
           role query for "Women" matches these too, breaking the locator.
        2. `exact=False` (the default) — the real category link's accessible
           name is polluted by its adjacent Font Awesome icon span (icon
           fonts can contribute generated-content characters to the
           computed accessible name), so an `exact=True` match against the
           plain text never succeeds even when scoped correctly.

        This is documented in docs/14-UI-Automation.md as a genuine,
        evidence-based finding, not a stylistic locator preference.
        """
        self.category_panel.get_by_role("link", name=top_level_name).click()
        self.category_panel.get_by_role("link", name=sub_category_name).click()

    def open_brand(self, brand_href: str) -> None:
        """Brand link accessible names include a result-count badge (e.g.
        "(6)Polo"), so href-based matching is used instead of by-name role
        matching — a deliberate, documented exception to the role-first
        locator preference (docs/11-Framework-Architecture.md §12 rank 5:
        "stable attributes," justified here by the badge-count text)."""
        self.page.locator(f'a[href="{brand_href}"]').first.click()
