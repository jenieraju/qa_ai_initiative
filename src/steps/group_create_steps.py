"""Reusable group-creation wizard steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.group_create_actions import GroupCreatePageActions


@allure.step("User verifies group create page is displayed")
def user_verifies_group_create_page_is_displayed(page: Page) -> None:
    GroupCreatePageActions(page).verify_create_page_visible()


@allure.step("User completes group basic details for '{group_name}'")
def user_completes_group_basic_details(page: Page, group_name: str, amount: str) -> None:
    GroupCreatePageActions(page).complete_basic_details(group_name, amount)


@allure.step("User verifies group was created successfully")
def user_verifies_group_created_successfully(page: Page) -> None:
    GroupCreatePageActions(page).verify_group_created_successfully()
