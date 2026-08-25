"""BasePage — the shared UI interaction foundation.

Implements docs/11-Framework-Architecture.md §12: common navigation, wait/
assertion helpers built on Playwright's own auto-waiting, and generic
element-presence checks reused by every concrete page object (docs/11 §11).

Contains no page-specific locators and no business logic — those belong
exclusively to concrete page classes (Step 14). Contains no test
assertions in the pass/fail sense (docs/11 §11's "test responsibilities" vs
"page-object responsibilities" split) — only reusable, generic helpers that
a test or a page-specific method can build on.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from src.config.settings import settings


class BasePage:
    """Shared foundation every concrete page object inherits from."""

    def __init__(self, page: Page) -> None:
        self.page = page

    @staticmethod
    def resolve_url(path: str = "") -> str:
        """Pure URL-joining logic, factored out of `goto` so it can be
        verified without any network call (docs/13-Core-Framework-
        Development.md validation)."""
        if not path:
            return settings.aut_base_url
        return settings.aut_base_url.rstrip("/") + "/" + path.lstrip("/")

    def goto(self, path: str = "") -> None:
        """Navigate relative to the configured AUT base URL.

        Uses Playwright's own navigation + auto-waiting — no manual sleep.
        Deliberately uses the default `wait_until="load"`, not
        `"networkidle"`: `networkidle` was tried during Step 14
        implementation as a response to one transient full-suite failure
        (docs/14-UI-Automation.md §13), but it made the Home page reliably
        time out instead — this AUT carries continuous third-party ad/
        tracker network activity (consistent with the ad-injected DOM
        elements found on /products, same §13), so the network never goes
        idle within any reasonable timeout. `load` plus Playwright's own
        per-locator auto-waiting is the correct, VERIFIED synchronization
        strategy for this specific AUT.
        """
        self.page.goto(self.resolve_url(path))

    def wait_for_load(self) -> None:
        """Wait for the page to reach a stable, interactable state."""
        self.page.wait_for_load_state("load")

    def is_visible(self, locator: Locator) -> bool:
        """A boolean visibility check for conditional logic in a page method.

        For an assertion a test should fail on, use `expect_visible`
        instead — this method is for branching, not verification.
        """
        return locator.is_visible()

    def get_text(self, locator: Locator) -> str:
        """Return a locator's visible text, waiting for it to be actionable."""
        return locator.inner_text()

    def expect_visible(self, locator: Locator) -> None:
        """A reusable, page-specific-assertion-grade visibility check.

        Concrete page objects may call this for assertions genuinely shared
        across multiple Test Cases (docs/11 §11) — a test-specific assertion
        that only one Test Case cares about still belongs in the test itself.
        """
        expect(locator).to_be_visible(timeout=settings.expect_timeout_ms)

    def expect_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_have_text(text, timeout=settings.expect_timeout_ms)

    # Google Ads / Ad Traffic Quality / Funding Choices — the AUT genuinely
    # serves these (VERIFIED via live network capture during Step 16
    # implementation, docs/16-Hybrid-E2E-Automation.md §20), and their
    # "vignette"/annotation script mutates arbitrary text-bearing elements
    # on the page (including inside product-name paragraphs) by injecting
    # `class="google-anno"`/`"google-anno-skip"` elements as DIRECT CHILDREN
    # of the original text node — polluting both role-based accessible-name
    # queries (found in Step 14, docs/14-UI-Automation.md §12 item 2) and
    # plain `.inner_text()` extraction (found in Step 16). Not the AUT's own
    # content; a third-party ad-quality/annotation system it embeds.
    _AD_DOMAIN_FRAGMENTS = (
        "googlesyndication.com",
        "doubleclick.net",
        "adtrafficquality.google",
        "fundingchoicesmessages.google.com",
    )

    def block_third_party_ads(self) -> None:
        """Blocks the specific, VERIFIED ad-network domains responsible for
        the DOM-mutating annotation injection above, at the network level —
        preventing the mutation from ever happening, rather than trying to
        filter or race against it after the fact. A generic, reusable
        browser-level capability (Playwright network routing), not AUT
        business logic — but only invoked where a test actually needs
        pollution-free bulk text extraction (currently: the Hybrid test,
        AE-E2E-TC-003), not applied globally, so it cannot silently change
        the behavior of already-passing Step 14 UI tests that never needed
        it. Fonts, analytics beacons, and other non-ad third-party requests
        are deliberately left unblocked — this targets only the confirmed
        injection source, not third-party traffic in general.
        """

        def _handle(route):
            if any(fragment in route.request.url for fragment in self._AD_DOMAIN_FRAGMENTS):
                route.abort()
            else:
                route.continue_()

        self.page.route("**/*", _handle)
