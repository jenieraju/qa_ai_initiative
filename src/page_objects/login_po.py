"""Login page object — locators only.

TODO: Replace placeholder locators once the real login flow and selectors are provided.
All page.locator() / page.get_by_*() calls must live in this file only.
"""

from playwright.sync_api import Locator

from src.core.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the application login screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        # TODO: Update selectors after reviewing the real login page.
        self.input_email = self.get_by_data_test_id("login-email")
        self.input_password = self.get_by_data_test_id("login-password")
        self.btn_login = self.get_by_data_test_id("login-submit")
        self.msg_error = self.get_by_data_test_id("login-error")
        self.lbl_page_title = self.get_by_text("Sign in", exact=True)

    def _loc_error_message(self, message: str) -> Locator:
        return self.msg_error.filter(has_text=message)
