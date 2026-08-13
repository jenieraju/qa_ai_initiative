"""Login page object (mobile + OTP).

Live-confirmed 2026-08-13 via real browser session against
https://web.dev.cofee.life/login (explicit permission given, real login
completed end-to-end). Two corrections versus the first draft: the terms
checkbox was missing entirely (Continue stays disabled until it's checked),
and the OTP boxes use data-testid="otpVerify_otpInputs" (shared across all
6 single-character inputs, not one unique id each) - not the "OtpInput
component, unconfirmed" placeholder from before.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements ---
        self.mobile_input = self.page.get_by_placeholder("Enter your mobile number")
        self.terms_checkbox = self.page.get_by_role("checkbox")
        self.continue_btn = self.page.get_by_role("button", name="Continue")
        self.invalid_mobile_error = self.page.get_by_text("Invalid mobile number")
        self.otp_error_toast = self.page.get_by_text("Error in OTP")
        # All 6 OTP digit boxes share this test id - index into it with .nth(i).
        self.otp_boxes = self.page.get_by_test_id("otpVerify_otpInputs")

    def goto_login(self) -> None:
        self.goto("login")

    def fill_mobile_and_continue(self, mobile: str) -> None:
        self.mobile_input.fill(mobile)
        self.terms_checkbox.check()
        self.continue_btn.click()

    def fill_otp_and_continue(self, otp: str) -> None:
        # Bulk-typing into one box does NOT auto-advance focus - each digit
        # must be clicked into its own box individually (live-confirmed).
        for i, digit in enumerate(otp):
            box = self.otp_boxes.nth(i)
            box.click()
            box.type(digit)
        self.continue_btn.click()
