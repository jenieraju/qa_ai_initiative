"""Reusable login steps decorated with Allure."""

import re

import allure
from playwright.sync_api import Page, expect

from src.constants.routes import GROUPS_PATH, LOGIN_PATH
from src.core.auth_storage import DEFAULT_AUTH_PROFILE, save_auth_storage_state
from src.core.session_state import session_state
from src.core.settings import get_settings
from src.page_actions.groups_actions import GroupsPageActions
from src.page_actions.login_actions import LoginPageActions
from src.page_objects.groups_po import GroupsPage


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
    session_state.set_active_profile(DEFAULT_AUTH_PROFILE)
    session_state.metadata["mobile_number"] = mobile_number


@allure.step("User saves authenticated session as profile '{profile_name}'")
def user_saves_authenticated_session(
    page: Page, profile_name: str = DEFAULT_AUTH_PROFILE
) -> None:
    path = save_auth_storage_state(page, profile_name)
    session_state.set_active_profile(profile_name)
    allure.attach(
        str(path),
        name="auth-storage-state",
        attachment_type=allure.attachment_type.TEXT,
    )


def _is_on_authenticated_groups(page: Page) -> bool:
    """True when the Groups list chrome is visible (not a login redirect)."""
    groups = GroupsPage(page)
    try:
        expect(groups.btn_new_group).to_be_visible(timeout=3_000)
        return True
    except AssertionError:
        return False


@allure.step("User ensures they are logged in (reuse session or login)")
def user_ensures_logged_in(page: Page, profile_name: str = DEFAULT_AUTH_PROFILE) -> None:
    """Reuse cookies from auth_profile when present; otherwise UI-login and save state.

    Call after the browser context may already have loaded `.auth/{profile}.json`
    via @pytest.mark.auth_profile. If the session is missing/expired, logs in with
    FEATURE_LOGIN_* credentials and persists a fresh storage state for later tests.
    """
    GroupsPageActions(page).navigate_to_groups_page()
    if _is_on_authenticated_groups(page):
        session_state.set_active_profile(profile_name)
        return

    settings = get_settings()
    if not settings.login_mobile_number or not settings.login_otp:
        raise ValueError(
            "No reusable auth session and FEATURE_LOGIN_MOBILE_NUMBER / "
            "FEATURE_LOGIN_OTP are not set. Run the login test first or configure .env.dev."
        )

    if LOGIN_PATH not in page.url:
        user_navigates_to_login_page(page)
    user_logs_in_with_mobile_and_otp(page, settings.login_mobile_number, settings.login_otp)
    expect(page).to_have_url(re.compile(re.escape(GROUPS_PATH)), timeout=settings.default_timeout_ms)
    user_saves_authenticated_session(page, profile_name)
    GroupsPageActions(page).navigate_to_groups_page()
    if not _is_on_authenticated_groups(page):
        raise AssertionError("Login completed but Groups page did not load")


@allure.step("User verifies invalid mobile number error '{message}'")
def user_verifies_invalid_mobile_number_error(page: Page, message: str) -> None:
    LoginPageActions(page).verify_invalid_mobile_number_error(message)


@allure.step("User verifies invalid OTP error")
def user_verifies_invalid_otp_error(page: Page) -> None:
    LoginPageActions(page).verify_invalid_otp_error()
