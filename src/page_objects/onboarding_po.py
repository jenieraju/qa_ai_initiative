"""Onboarding account-selection page object — locators only.

Covers AUTH.SELECT_ACCOUNT ("/select-account"), which renders two states in
sequence for a brand-new user: referral code entry (ReferralCode) then the
account-selection form (AccountSelection: name, account type, business name).
All page.locator() / page.get_by_*() calls must live in this file only.
"""

from src.constants.messages import ACCOUNT_TYPE_INDIVIDUAL, ACCOUNT_TYPE_ORGANIZATION
from src.core.base_page import BasePage


class OnboardingPage(BasePage):
    """Page object for the new-user account-selection screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators: shared AuthSection chrome ---
        self.lbl_section_title = self.get_by_data_test_id("authentication_title")
        self.btn_continue = self.get_by_button("Continue")

        # --- Locators: referral code state ---
        self.input_referral_code_boxes = self.get_by_data_test_id("otpVerify_otpInputs")
        self.lnk_skip_referral = self.get_by_text("Skip Referral", exact=True)

        # --- Locators: account-selection form state ---
        self.input_profile_name = self.get_by_placeholder("Enter your name")
        self.rdo_account_type_individual = self.get_by_text(ACCOUNT_TYPE_INDIVIDUAL, exact=True)
        self.rdo_account_type_organization = self.get_by_text(ACCOUNT_TYPE_ORGANIZATION, exact=True)
        # Shared placeholder for both IndividualInfo.displayName and
        # OrganizationInfo.organizationName — only one renders at a time.
        self.input_business_name = self.get_by_placeholder("Enter your business name")
