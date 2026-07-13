"""Payment-selection page object — locators only (organization onboarding path).

Covers AUTH.SELECT_PAYMENT ("/select-payment"): bank account verification
(BankInfo) followed by onboarding submission.
All page.locator() / page.get_by_*() calls must live in this file only.
"""

from src.core.base_page import BasePage


class PaymentSelectionPage(BasePage):
    """Page object for the bank-account verification screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.lbl_section_title = self.get_by_data_test_id("authentication_title")
        self.input_account_number = self.get_by_placeholder("Enter your account number")
        self.input_confirm_account_number = self.get_by_placeholder("Confirm account number")
        self.input_ifsc = self.get_by_placeholder("Enter IFSC code")
        self.btn_verify_account = self.get_by_button("Verify Account")
        self.btn_proceed = self.get_by_button("Proceed")
        self.msg_bank_error = self.get_by_data_test_id("error_text")
