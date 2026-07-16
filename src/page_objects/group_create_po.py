"""Group creation wizard page object — locators only (basic-details step)."""

from src.constants.messages import (
    BTN_SAVE_AND_NEXT,
    HEADING_NEW_GROUP,
    MSG_GROUP_CREATED,
    PAYMENT_COLLECTION_MONTHLY,
    PLACEHOLDER_AMOUNT,
    PLACEHOLDER_GROUP_NAME,
    PLACEHOLDER_PAYMENT_COLLECTION_DAY,
)
from src.core.base_page import BasePage


class GroupCreatePage(BasePage):
    """Page object for /groups/create — basic details step."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.lbl_heading = self.get_by_text(HEADING_NEW_GROUP, exact=True)
        self.input_group_name = self.get_by_placeholder(PLACEHOLDER_GROUP_NAME)
        self.input_payment_collection_day = self.get_by_placeholder(
            PLACEHOLDER_PAYMENT_COLLECTION_DAY
        )
        self.input_amount = self.get_by_placeholder(PLACEHOLDER_AMOUNT)
        self.btn_save_and_next = self.get_by_button(BTN_SAVE_AND_NEXT)
        self.btn_cancel = self.get_by_button("Cancel")
        self.opt_monthly = self.get_by_text(PAYMENT_COLLECTION_MONTHLY, exact=True)
        self.btn_apply = self.get_by_button("Apply")
        self.msg_group_created = self.get_by_text(MSG_GROUP_CREATED, exact=True)
