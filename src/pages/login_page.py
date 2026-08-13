"""Login page object (mobile + OTP). See context/ui-auth.md - OTP box selector unconfirmed."""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements ---
        self.mobile_input = self.page.get_by_placeholder("Enter your mobile number")
        self.continue_btn = self.page.get_by_role("button", name="Continue")
        self.invalid_mobile_error = self.page.get_by_text("Invalid mobile number")
        self.otp_error_toast = self.page.get_by_text("Error in OTP")
        # OTP input boxes: exact selector unconfirmed (context/ui-auth.md Open Questions) -
        # OtpInput component, no data-testid found in source read this pass.

    def goto_login(self) -> None:
        self.goto("login")

    def fill_mobile_and_continue(self, mobile: str) -> None:
        self.mobile_input.fill(mobile)
        self.continue_btn.click()

    def fill_otp_and_continue(self, otp: str) -> None:
        # NOTE: OTP box selector unconfirmed - needs a live-inspected DOM check
        # before this method is usable. Placeholder raises until resolved.
        raise NotImplementedError(
            "OTP input selector not confirmed in context/ui-auth.md - "
            "resolve via live DOM inspection before use."
        )
