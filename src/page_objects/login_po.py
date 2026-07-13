"""Login page object — locators only.

Login is a single route (AUTH.LOGIN, "/login") that renders two states in
sequence: mobile-number entry (LoginInput) then OTP entry (OtpVerification).
Locators for both states live here since they share one page/route.
All page.locator() / page.get_by_*() calls must live in this file only.
"""

from src.constants.messages import MSG_INVALID_OTP
from src.core.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the application login + OTP verification screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators: shared AuthSection chrome ---
        self.lbl_section_title = self.get_by_data_test_id("authentication_title")
        self.lbl_section_description = self.get_by_data_test_id("authentication_description")
        self.btn_continue = self.get_by_button("Continue")
        self.msg_input_error = self.get_by_data_test_id("error_text")

        # --- Locators: mobile-number entry state ---
        self.input_mobile_number = self.get_by_placeholder("Enter your mobile number")
        self.chk_agree_terms = self.get_by_data_test_id("login_agreeTerms")

        # --- Locators: OTP entry state (6 single-digit boxes, shared test id) ---
        self.input_otp_boxes = self.get_by_data_test_id("otpVerify_otpInputs")
        self.msg_otp_invalid = self.get_by_text(MSG_INVALID_OTP)
