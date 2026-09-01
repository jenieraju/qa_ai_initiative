"""Reusable groups list steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.groups_actions import GroupsPageActions


@allure.step("User navigates to groups page")
def user_navigates_to_groups_page(page: Page) -> None:
    GroupsPageActions(page).navigate_to_groups_page()


@allure.step("User verifies groups page is displayed")
def user_verifies_groups_page_is_displayed(page: Page) -> None:
    GroupsPageActions(page).verify_groups_page_visible()


@allure.step("User clicks New Group")
def user_clicks_new_group(page: Page) -> None:
    GroupsPageActions(page).click_new_group()


@allure.step("User verifies group '{group_name}' is listed")
def user_verifies_group_is_listed(page: Page, group_name: str) -> None:
    GroupsPageActions(page).verify_group_listed(group_name)


@allure.step("User counts groups on the groups list")
def user_counts_groups_on_list(page: Page) -> int:
    GroupsPageActions(page).navigate_to_groups_page()
    GroupsPageActions(page).verify_groups_page_visible()
    return GroupsPageActions(page).count_listed_groups()
