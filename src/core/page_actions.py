"""Base page actions with shared interaction helpers.

Low-level primitives (click/fill/hover/waits) are intentionally undecorated —
only the Steps layer (src/steps/) carries @allure.step, per AGENTS.md.
"""

from playwright.sync_api import Locator, Page

from src.core.settings import get_settings


class PageActions:
    """Base class for page actions — business logic and interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.settings = get_settings()

    def click(self, locator: Locator, *, timeout: int | None = None, force: bool = False) -> None:
        locator.click(timeout=timeout or self.settings.default_timeout_ms, force=force)

    def fill(self, locator: Locator, value: str, *, timeout: int | None = None) -> None:
        locator.fill(value, timeout=timeout or self.settings.default_timeout_ms)

    def hover(self, locator: Locator, *, timeout: int | None = None) -> None:
        locator.hover(timeout=timeout or self.settings.default_timeout_ms)

    def wait_for_element_visible(self, locator: Locator, *, timeout: int | None = None) -> Locator:
        timeout_ms = timeout or self.settings.default_timeout_ms
        locator.wait_for(state="visible", timeout=timeout_ms)
        return locator

    def wait_for_spinner_to_disappear(
        self, spinner: Locator, *, timeout: int | None = None
    ) -> None:
        """Wait until a loading spinner is hidden or detached."""
        timeout_ms = timeout or self.settings.default_timeout_ms
        try:
            spinner.wait_for(state="hidden", timeout=timeout_ms)
        except Exception:
            spinner.wait_for(state="detached", timeout=timeout_ms)
