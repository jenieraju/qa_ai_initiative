"""Add Member form actions — interactions."""

from playwright.sync_api import Page

from src.constants.messages import HEADING_ADD_MEMBER
from src.core.assert_helper import assert_element_has_text, assert_element_visible
from src.core.page_actions import PageActions
from src.page_objects.member_create_po import MemberCreatePage


class MemberCreatePageActions(PageActions):
    """Actions for the Add Member form."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = MemberCreatePage(page)

    def verify_create_page_visible(self) -> None:
        self.wait_for_element_visible(self.po.lbl_heading)
        assert_element_has_text(self.po.lbl_heading, HEADING_ADD_MEMBER)
        self.wait_for_element_visible(self.po.input_member_name)

    def enter_member_name(self, member_name: str) -> None:
        self.fill(self.po.input_member_name, member_name)

    def enter_mobile_number(self, mobile_number: str) -> None:
        self.fill(self.po.input_mobile_number, mobile_number)

    def click_save(self) -> None:
        self.click(self.po.btn_save)

    def complete_basic_details(self, member_name: str, mobile_number: str) -> None:
        self.enter_member_name(member_name)
        self.enter_mobile_number(mobile_number)
        self.click_save()

    def verify_member_created_successfully(self) -> None:
        assert_element_visible(self.po.msg_member_created)
