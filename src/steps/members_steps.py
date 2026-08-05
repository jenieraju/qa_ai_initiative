"""Reusable members list steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.members_actions import MembersPageActions


@allure.step("User navigates to members page")
def user_navigates_to_members_page(page: Page) -> None:
    MembersPageActions(page).navigate_to_members_page()


@allure.step("User verifies members page is displayed")
def user_verifies_members_page_is_displayed(page: Page) -> None:
    MembersPageActions(page).verify_members_page_visible()


@allure.step("User clicks Add Member")
def user_clicks_add_member(page: Page) -> None:
    MembersPageActions(page).click_add_member()


@allure.step("User verifies member '{member_name}' is listed")
def user_verifies_member_is_listed(page: Page, member_name: str) -> None:
    MembersPageActions(page).verify_member_listed(member_name)
