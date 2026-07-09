"""Base page object with shared locator helpers."""

from playwright.sync_api import Locator, Page

from src.core.settings import get_settings


class BasePage:
    """Base class for all page objects — locators only, no business logic."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.settings = get_settings()

    def goto(self, path: str = "/") -> None:
        """Navigate to a path relative to BASE_URL."""
        base = self.settings.base_url.rstrip("/")
        normalized = path if path.startswith("/") else f"/{path}"
        self.page.goto(f"{base}{normalized}")

    def get_by_locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def get_by_button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def get_by_data_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    def get_by_placeholder(self, text: str) -> Locator:
        return self.page.get_by_placeholder(text)
