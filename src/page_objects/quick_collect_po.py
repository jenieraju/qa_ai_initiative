"""Quick Collect page object — locators only.

Covers both routes of the flow, which share one screen sequence:
`/quick-collect/create-link` (form + payer list + confirm dialog) and
`/quick-collect/success`.

The screen has almost no `data-testid` — only the success text and the
file-upload set. Amount / notes / search are placeholder-only and the CTA and
dialog buttons are role+name, per APP_CONTEXT.md -> "Locator strategy notes".
"""

from playwright.sync_api import Locator

from src.constants.messages import (
    BTN_CANCEL,
    BTN_CONFIRM,
    BTN_QUICK_COLLECT_CLEAR,
    BTN_QUICK_COLLECT_CREATE,
    BTN_QUICK_COLLECT_CREATE_NEW_LINK,
    BTN_QUICK_COLLECT_GO_TO_HOME,
    BTN_QUICK_COLLECT_SEND,
    CHK_QUICK_COLLECT_SUPPRESS_NOTIFICATIONS,
    HEADING_QUICK_COLLECT_AMOUNT,
    HEADING_QUICK_COLLECT_PAYERS,
    HINT_QUICK_COLLECT_AMOUNT_RANGE,
    MSG_QUICK_COLLECT_CONFIRM_DIALOG,
    MSG_QUICK_COLLECT_SUCCESS_PREFIX,
    PLACEHOLDER_QUICK_COLLECT_AMOUNT,
    PLACEHOLDER_QUICK_COLLECT_NOTE,
    PLACEHOLDER_QUICK_COLLECT_SEARCH_PAYER,
    TESTID_QUICK_COLLECT_SUCCESS_TEXT,
)
from src.core.base_page import BasePage


class QuickCollectPage(BasePage):
    """Page object for the Quick Collect create-link and success screens."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators: create-link form ---
        self.lbl_amount_heading = self.get_by_text(HEADING_QUICK_COLLECT_AMOUNT, exact=True)
        self.lbl_payers_heading = self.get_by_text(HEADING_QUICK_COLLECT_PAYERS, exact=True)
        self.input_amount = self.get_by_placeholder(PLACEHOLDER_QUICK_COLLECT_AMOUNT)
        self.input_note = self.get_by_placeholder(PLACEHOLDER_QUICK_COLLECT_NOTE)
        self.input_search_payer = self.get_by_placeholder(PLACEHOLDER_QUICK_COLLECT_SEARCH_PAYER)
        self.chk_suppress_notifications = self.get_by_text(
            CHK_QUICK_COLLECT_SUPPRESS_NOTIFICATIONS, exact=True
        )
        self.lbl_amount_range_hint = self.get_by_text(HINT_QUICK_COLLECT_AMOUNT_RANGE, exact=True)

        # --- Locators: primary CTA (label is state-dependent) ---
        # "Send" while payers will be notified, "Create" once suppressed.
        self.btn_send = self.get_by_button(BTN_QUICK_COLLECT_SEND)
        self.btn_create = self.get_by_button(BTN_QUICK_COLLECT_CREATE)
        self.btn_clear = self.get_by_button(BTN_QUICK_COLLECT_CLEAR)

        # --- Locators: confirmation dialog ---
        self.lbl_confirm_dialog = self.get_by_text(MSG_QUICK_COLLECT_CONFIRM_DIALOG, exact=True)
        self.btn_confirm = self.get_by_button(BTN_CONFIRM)
        self.btn_cancel = self.get_by_button(BTN_CANCEL)

        # --- Locators: success screen ---
        self.lbl_success_text = self.get_by_data_test_id(TESTID_QUICK_COLLECT_SUCCESS_TEXT)
        # The success sentence is split across nodes — the prefix is its own
        # <span>, with the ₹ symbol, the amount and "request" as siblings — so
        # scope to the wrapper to assert on the whole sentence including the amount.
        self.lbl_success_body = self.get_by_text(MSG_QUICK_COLLECT_SUCCESS_PREFIX).locator(
            "xpath=.."
        )
        self.btn_create_new_link = self.get_by_button(BTN_QUICK_COLLECT_CREATE_NEW_LINK)
        self.btn_go_to_home = self.get_by_button(BTN_QUICK_COLLECT_GO_TO_HOME)

    def loc_payer_row_by_name(self, payer_name: str) -> Locator:
        """A payer row in the members list — a button whose name is the member's."""
        return self.get_by_button(payer_name)
