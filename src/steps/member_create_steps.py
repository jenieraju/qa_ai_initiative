"""Reusable Add Member form steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.member_create_actions import MemberCreatePageActions


@allure.step("User verifies Add Member form is displayed")
def user_verifies_member_create_page_is_displayed(page: Page) -> None:
    MemberCreatePageActions(page).verify_create_page_visible()


@allure.step("User completes member basic details for '{member_name}'")
def user_completes_member_basic_details(page: Page, member_name: str, mobile_number: str) -> None:
    MemberCreatePageActions(page).complete_basic_details(member_name, mobile_number)


@allure.step("User verifies member was created successfully")
def user_verifies_member_created_successfully(page: Page) -> None:
    MemberCreatePageActions(page).verify_member_created_successfully()
