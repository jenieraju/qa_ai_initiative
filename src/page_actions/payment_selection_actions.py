"""Payment-selection page actions — business logic and interactions (organization path)."""

from playwright.sync_api import Page

from src.constants.messages import SECTION_TITLE_SELECT_PAYMENT, TITLE_SELECT_PAYMENT
from src.core.assert_helper import (
    assert_element_has_text,
    assert_element_visible,
    assert_page_title,
)
from src.core.page_actions import PageActions
from src.page_objects.payment_selection_po import PaymentSelectionPage


class PaymentSelectionPageActions(PageActions):
    """Actions for the bank-account verification screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = PaymentSelectionPage(page)

    def verify_payment_selection_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_section_title)
        assert_element_has_text(self.po.lbl_section_title, SECTION_TITLE_SELECT_PAYMENT)
        assert_page_title(self.page, TITLE_SELECT_PAYMENT)

    def enter_bank_details(self, account_number: str, ifsc: str) -> None:
        self.fill(self.po.input_account_number, account_number)
        self.fill(self.po.input_confirm_account_number, account_number)
        self.fill(self.po.input_ifsc, ifsc)

    def click_verify_account(self) -> None:
        self.click(self.po.btn_verify_account)

    def click_proceed(self) -> None:
        self.click(self.po.btn_proceed)

    def verify_bank_account_verified(self) -> None:
        assert_element_visible(self.po.btn_proceed)

    def complete_payment_selection(self, account_number: str, ifsc: str) -> None:
        self.enter_bank_details(account_number, ifsc)
        self.click_verify_account()
        self.verify_bank_account_verified()
        self.click_proceed()

    def verify_bank_error(self, message: str) -> None:
        assert_element_has_text(self.po.msg_bank_error, message)
