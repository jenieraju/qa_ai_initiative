"""Reusable Quick Collect steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.quick_collect_actions import QuickCollectPageActions


@allure.step("User navigates to the Quick Collect create-link page")
def user_navigates_to_quick_collect_page(page: Page) -> None:
    QuickCollectPageActions(page).navigate_to_create_link_page()


@allure.step("User verifies the Quick Collect create-link page is displayed")
def user_verifies_quick_collect_page_is_displayed(page: Page) -> None:
    QuickCollectPageActions(page).verify_create_link_page_visible()


@allure.step("User enters fee amount '{amount}' and note '{note}'")
def user_enters_amount_and_note(page: Page, amount: str, note: str) -> None:
    actions = QuickCollectPageActions(page)
    actions.enter_amount(amount)
    actions.enter_note(note)


@allure.step("User enters fee amount '{amount}'")
def user_enters_amount(page: Page, amount: str) -> None:
    QuickCollectPageActions(page).enter_amount(amount)


@allure.step("User verifies the CTA reads 'Send' (payers will be notified)")
def user_verifies_cta_is_send(page: Page) -> None:
    QuickCollectPageActions(page).verify_cta_is_send()


@allure.step("User suppresses payer notifications")
def user_suppresses_payer_notifications(page: Page) -> None:
    QuickCollectPageActions(page).suppress_payer_notifications()


@allure.step("User verifies the CTA reads 'Create' (notifications suppressed)")
def user_verifies_cta_is_create(page: Page) -> None:
    QuickCollectPageActions(page).verify_cta_is_create()


@allure.step("User searches for payer '{payer_name}'")
def user_searches_for_payer(page: Page, payer_name: str) -> None:
    QuickCollectPageActions(page).search_payer(payer_name)


@allure.step("User verifies payer '{payer_name}' is listed")
def user_verifies_payer_is_listed(page: Page, payer_name: str) -> None:
    QuickCollectPageActions(page).verify_payer_listed(payer_name)


@allure.step("User verifies payer '{payer_name}' is not listed")
def user_verifies_payer_is_not_listed(page: Page, payer_name: str) -> None:
    QuickCollectPageActions(page).verify_payer_not_listed(payer_name)


@allure.step("User selects payer '{payer_name}'")
def user_selects_payer(page: Page, payer_name: str) -> None:
    QuickCollectPageActions(page).select_payer(payer_name)


@allure.step("User verifies the allowed-amount hint is displayed")
def user_verifies_amount_range_hint(page: Page) -> None:
    QuickCollectPageActions(page).verify_amount_range_hint_visible()


@allure.step("User verifies the payment link can be submitted")
def user_verifies_submission_is_allowed(page: Page) -> None:
    actions = QuickCollectPageActions(page)
    assert (
        actions.is_create_cta_enabled()
    ), "The Create CTA is disabled, but the form should accept this input."


@allure.step("User verifies the payment link cannot be submitted")
def user_verifies_submission_is_blocked(page: Page) -> None:
    actions = QuickCollectPageActions(page)
    assert (
        not actions.is_create_cta_enabled()
    ), "The Create CTA is actionable, but the form should block submission here."


@allure.step("User submits the payment link")
def user_submits_payment_link(page: Page) -> None:
    QuickCollectPageActions(page).submit_suppressed()


@allure.step("User verifies the confirmation dialog is displayed")
def user_verifies_confirmation_dialog_is_displayed(page: Page) -> None:
    QuickCollectPageActions(page).verify_confirm_dialog_visible()


@allure.step("User confirms the payment link creation")
def user_confirms_payment_link_creation(page: Page) -> None:
    QuickCollectPageActions(page).confirm_submission()


@allure.step("User cancels the payment link creation")
def user_cancels_payment_link_creation(page: Page) -> None:
    QuickCollectPageActions(page).cancel_submission()


@allure.step("User verifies the confirmation dialog is dismissed")
def user_verifies_confirmation_dialog_is_dismissed(page: Page) -> None:
    QuickCollectPageActions(page).verify_confirm_dialog_hidden()


@allure.step("User creates a Quick Collect link for '{payer_name}' of amount '{amount}'")
def user_creates_quick_collect_link(page: Page, payer_name: str, amount: str, note: str) -> None:
    """Full happy path with notifications suppressed — see the actions docstring."""
    actions = QuickCollectPageActions(page)
    actions.enter_amount(amount)
    actions.enter_note(note)
    actions.suppress_payer_notifications()
    actions.select_payer(payer_name)
    actions.submit_suppressed()
    actions.verify_confirm_dialog_visible()
    actions.confirm_submission()


@allure.step("User verifies the payment link was created successfully")
def user_verifies_payment_link_created(page: Page) -> None:
    QuickCollectPageActions(page).verify_link_created_successfully()


@allure.step("User verifies the success page shows amount '{amount}'")
def user_verifies_success_shows_amount(page: Page, amount: str) -> None:
    QuickCollectPageActions(page).verify_success_shows_amount(amount)


@allure.step("User starts another payment link from the success page")
def user_clicks_create_new_link(page: Page) -> None:
    QuickCollectPageActions(page).click_create_new_link()


@allure.step("User leaves the success page via 'Go To Home'")
def user_clicks_go_to_home(page: Page) -> None:
    QuickCollectPageActions(page).click_go_to_home()
