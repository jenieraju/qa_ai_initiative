"""Reusable payment-selection steps decorated with Allure (organization path)."""

import allure
from playwright.sync_api import Page

from src.page_actions.payment_selection_actions import PaymentSelectionPageActions


@allure.step("User verifies payment-selection page is displayed")
def user_verifies_payment_selection_page_is_displayed(page: Page) -> None:
    PaymentSelectionPageActions(page).verify_payment_selection_page_visible()


@allure.step("User completes payment selection with account number '{account_number}'")
def user_completes_payment_selection(page: Page, account_number: str, ifsc: str) -> None:
    PaymentSelectionPageActions(page).complete_payment_selection(account_number, ifsc)
