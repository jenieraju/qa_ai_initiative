"""Onboarding account-selection page actions — business logic and interactions."""

from playwright.sync_api import Page

from src.constants.messages import (
    SECTION_TITLE_REFERRAL_CODE,
    SECTION_TITLE_SELECT_ACCOUNT,
    TITLE_REFERRAL_CODE,
    TITLE_SELECT_ACCOUNT,
)
from src.core.assert_helper import assert_element_has_text, assert_page_title
from src.core.page_actions import PageActions
from src.page_objects.onboarding_po import OnboardingPage


class OnboardingPageActions(PageActions):
    """Actions for the new-user account-selection screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = OnboardingPage(page)

    def verify_referral_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_REFERRAL_CODE)
        assert_page_title(self.page, TITLE_REFERRAL_CODE)

    def skip_referral(self) -> None:
        self.click(self.po.lnk_skip_referral)

    def verify_account_selection_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_SELECT_ACCOUNT)
        assert_page_title(self.page, TITLE_SELECT_ACCOUNT)

    def enter_profile_name(self, profile_name: str) -> None:
        self.fill(self.po.input_profile_name, profile_name)

    def select_individual_account_type(self) -> None:
        self.click(self.po.rdo_account_type_individual)

    def select_organization_account_type(self) -> None:
        self.click(self.po.rdo_account_type_organization)

    def enter_business_name(self, business_name: str) -> None:
        self.fill(self.po.input_business_name, business_name)

    def click_continue(self) -> None:
        self.click(self.po.btn_continue)

    def complete_individual_onboarding(self, profile_name: str, business_name: str) -> None:
        self.enter_profile_name(profile_name)
        self.select_individual_account_type()
        self.enter_business_name(business_name)
        self.click_continue()

    def complete_organization_onboarding(self, profile_name: str, organization_name: str) -> None:
        self.enter_profile_name(profile_name)
        self.select_organization_account_type()
        self.enter_business_name(organization_name)
        self.click_continue()
