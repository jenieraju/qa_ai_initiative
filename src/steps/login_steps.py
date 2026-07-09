"""Reusable login steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.core.session_state import session_state
from src.page_actions.login_actions import LoginPageActions


@allure.step("User navigates to login page")
def user_navigates_to_login_page(page: Page) -> None:
    LoginPageActions(page).navigate_to_login_page()


@allure.step("User verifies login page is displayed")
def user_verifies_login_page_is_displayed(page: Page) -> None:
    LoginPageActions(page).verify_login_page_visible()


@allure.step("User submits mobile number '{mobile_number}'")
def user_submits_mobile_number(page: Page, mobile_number: str) -> None:
    LoginPageActions(page).submit_mobile_number(mobile_number)


@allure.step("User verifies OTP verification page is displayed")
def user_verifies_otp_page_is_displayed(page: Page) -> None:
    LoginPageActions(page).verify_otp_page_visible()


@allure.step("User submits OTP")
def user_submits_otp(page: Page, otp: str) -> None:
    LoginPageActions(page).submit_otp(otp)


@allure.step("User logs in with mobile number '{mobile_number}' and OTP")
def user_logs_in_with_mobile_and_otp(page: Page, mobile_number: str, otp: str) -> None:
    actions = LoginPageActions(page)
    actions.login_with_mobile_and_otp(mobile_number, otp)
    session_state.set_active_profile("default")
    session_state.metadata["mobile_number"] = mobile_number


@allure.step("User verifies invalid mobile number error '{message}'")
def user_verifies_invalid_mobile_number_error(page: Page, message: str) -> None:
    LoginPageActions(page).verify_invalid_mobile_number_error(message)


@allure.step("User verifies invalid OTP error")
def user_verifies_invalid_otp_error(page: Page) -> None:
    LoginPageActions(page).verify_invalid_otp_error()
