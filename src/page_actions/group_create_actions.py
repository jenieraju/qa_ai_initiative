"""Group creation wizard actions — basic-details step interactions."""

from playwright.sync_api import Page

from src.constants.messages import HEADING_NEW_GROUP
from src.core.assert_helper import assert_element_has_text, assert_element_visible
from src.core.page_actions import PageActions
from src.page_objects.group_create_po import GroupCreatePage


class GroupCreatePageActions(PageActions):
    """Actions for the /groups/create basic-details step."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = GroupCreatePage(page)

    def verify_create_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_heading)
        assert_element_has_text(self.po.lbl_heading, HEADING_NEW_GROUP)
        self.wait_for_element_visible(self.po.input_group_name)

    def enter_group_name(self, group_name: str) -> None:
        self.fill(self.po.input_group_name, group_name)

    def select_monthly_payment_collection(self) -> None:
        self.click(self.po.input_payment_collection_day)
        self.click(self.po.opt_monthly)
        self.click(self.po.btn_apply)

    def enter_amount(self, amount: str) -> None:
        self.fill(self.po.input_amount, amount)

    def click_save_and_next(self) -> None:
        self.click(self.po.btn_save_and_next)

    def complete_basic_details(self, group_name: str, amount: str) -> None:
        self.enter_group_name(group_name)
        self.select_monthly_payment_collection()
        self.enter_amount(amount)
        self.click_save_and_next()

    def verify_group_created_successfully(self) -> None:
        assert_element_visible(self.po.msg_group_created)
