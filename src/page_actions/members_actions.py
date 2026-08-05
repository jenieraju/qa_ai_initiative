"""Members list page actions — business logic and interactions."""

from playwright.sync_api import Page

from src.constants.messages import TITLE_MEMBERS
from src.constants.routes import MEMBERS_PATH
from src.core.assert_helper import assert_element_visible, assert_page_title
from src.core.page_actions import PageActions
from src.page_objects.members_po import MembersPage


class MembersPageActions(PageActions):
    """Actions for the members list screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = MembersPage(page)

    def navigate_to_members_page(self) -> None:
        self.po.goto(MEMBERS_PATH)

    def verify_members_page_visible(self) -> None:
        assert_page_title(self.page, TITLE_MEMBERS)
        self.wait_for_element_visible(self.po.btn_add_member)

    def click_add_member(self) -> None:
        self.click(self.po.btn_add_member)

    def verify_member_listed(self, member_name: str) -> None:
        assert_element_visible(self.po.loc_member_by_name(member_name))
