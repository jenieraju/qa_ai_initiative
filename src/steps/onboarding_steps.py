"""Reusable onboarding account-selection steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.onboarding_actions import OnboardingPageActions


@allure.step("User verifies referral code page is displayed")
def user_verifies_referral_page_is_displayed(page: Page) -> None:
    OnboardingPageActions(page).verify_referral_page_visible()


@allure.step("User skips referral code")
def user_skips_referral_code(page: Page) -> None:
    OnboardingPageActions(page).skip_referral()


@allure.step("User verifies account-selection page is displayed")
def user_verifies_account_selection_page_is_displayed(page: Page) -> None:
    OnboardingPageActions(page).verify_account_selection_page_visible()


@allure.step("User completes individual onboarding as '{profile_name}'")
def user_completes_individual_onboarding(page: Page, profile_name: str, business_name: str) -> None:
    OnboardingPageActions(page).complete_individual_onboarding(profile_name, business_name)


@allure.step("User completes organization onboarding as '{profile_name}'")
def user_completes_organization_onboarding(
    page: Page, profile_name: str, organization_name: str
) -> None:
    OnboardingPageActions(page).complete_organization_onboarding(profile_name, organization_name)
