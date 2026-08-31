"""Quick Collect page actions — business logic and interactions."""

from playwright.sync_api import Page, expect

from src.constants.messages import (
    MSG_QUICK_COLLECT_LINK_CREATED,
    TITLE_QUICK_COLLECT,
)
from src.constants.routes import QUICK_COLLECT_CREATE_LINK_PATH
from src.core.assert_helper import (
    assert_element_hidden,
    assert_element_visible,
    assert_page_title,
)
from src.core.page_actions import PageActions
from src.page_objects.quick_collect_po import QuickCollectPage


class QuickCollectPageActions(PageActions):
    """Actions for the Quick Collect create-link and success screens."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = QuickCollectPage(page)

    # --- navigation / page state ---

    def navigate_to_create_link_page(self) -> None:
        self.po.goto(QUICK_COLLECT_CREATE_LINK_PATH)

    def verify_create_link_page_visible(self) -> None:
        assert_page_title(self.page, TITLE_QUICK_COLLECT)
        self.wait_for_element_visible(self.po.lbl_amount_heading)
        self.wait_for_element_visible(self.po.lbl_payers_heading)
        self.wait_for_element_visible(self.po.input_amount)

    # --- amount / notes ---

    def enter_amount(self, amount: str) -> None:
        self.fill(self.po.input_amount, amount)

    def enter_note(self, note: str) -> None:
        self.fill(self.po.input_note, note)

    def verify_amount_range_hint_visible(self) -> None:
        """The 2–200000 helper text is static — a page-loaded signal, not a validation error."""
        assert_element_visible(self.po.lbl_amount_range_hint)

    # --- notifications ---

    def suppress_payer_notifications(self) -> None:
        """Tick "Do not send payment link to payers".

        Automation always does this: the dev members list holds a real phone
        number, and the payment order is created either way. Ticking it also
        relabels the CTA from "Send" to "Create" — see verify_cta_label_*.
        """
        self.click(self.po.chk_suppress_notifications)

    def verify_cta_is_send(self) -> None:
        assert_element_visible(self.po.btn_send)

    def verify_cta_is_create(self) -> None:
        assert_element_visible(self.po.btn_create)

    # --- payers ---

    def search_payer(self, payer_name: str) -> None:
        self.fill(self.po.input_search_payer, payer_name)

    def select_payer(self, payer_name: str) -> None:
        """Select a payer by clicking their row — the row is the reliable target."""
        row = self.po.loc_payer_row_by_name(payer_name)
        self.wait_for_element_visible(row)
        self.click(row)

    def verify_payer_listed(self, payer_name: str) -> None:
        assert_element_visible(self.po.loc_payer_row_by_name(payer_name))

    def verify_payer_not_listed(self, payer_name: str) -> None:
        assert_element_hidden(self.po.loc_payer_row_by_name(payer_name))

    # --- submit ---

    def is_create_cta_enabled(self) -> bool:
        """Whether the suppressed-mode CTA can be actioned."""
        return self.po.btn_create.is_enabled()

    def submit_suppressed(self) -> None:
        self.click(self.po.btn_create)

    def verify_confirm_dialog_visible(self) -> None:
        assert_element_visible(self.po.lbl_confirm_dialog)

    def confirm_submission(self) -> None:
        self.click(self.po.btn_confirm)

    def cancel_submission(self) -> None:
        self.click(self.po.btn_cancel)

    def verify_confirm_dialog_hidden(self) -> None:
        assert_element_hidden(self.po.lbl_confirm_dialog)

    # --- success screen ---

    def verify_link_created_successfully(self) -> None:
        expect(self.po.lbl_success_text).to_have_text(MSG_QUICK_COLLECT_LINK_CREATED)

    def verify_success_shows_amount(self, amount: str) -> None:
        """The success copy echoes the requested amount: "... for ₹<amount> request"."""
        assert_element_visible(self.po.lbl_success_body)
        expect(self.po.lbl_success_body).to_contain_text(amount)

    def click_create_new_link(self) -> None:
        self.click(self.po.btn_create_new_link)

    def click_go_to_home(self) -> None:
        self.click(self.po.btn_go_to_home)
