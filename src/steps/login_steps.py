"""Reusable login steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.core.session_state import session_state
from src.page_actions.login_actions import LoginPageActions


@allure.step("User navigates to login page")
def user_navigates_to_login_page(page: Page) -> None:
    LoginPageActions(page).navigate_to_login_page()


@allure.step("User logs in with email '{email}'")
def user_logs_in_with_credentials(page: Page, email: str, password: str) -> None:
    actions = LoginPageActions(page)
    actions.login_with_credentials(email, password)
    session_state.set_active_profile("default", user_email=email)


@allure.step("User verifies login page is displayed")
def user_verifies_login_page_is_displayed(page: Page) -> None:
    LoginPageActions(page).verify_login_form_visible()


@allure.step("User verifies login error message '{message}'")
def user_verifies_login_error_message(page: Page, message: str) -> None:
    LoginPageActions(page).verify_error_message_visible(message)
