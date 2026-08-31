"""Groups list page actions — business logic and interactions."""

from playwright.sync_api import Page, expect

from src.constants.messages import TITLE_GROUPS
from src.constants.routes import GROUPS_PATH
from src.core.assert_helper import assert_element_visible, assert_page_title
from src.core.page_actions import PageActions
from src.page_objects.groups_po import GroupsPage


class GroupsPageActions(PageActions):
    """Actions for the groups list screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = GroupsPage(page)

    def navigate_to_groups_page(self) -> None:
        self.po.goto(GROUPS_PATH)

    def verify_groups_page_visible(self) -> None:
        assert_page_title(self.page, TITLE_GROUPS)
        self.wait_for_element_visible(self.po.btn_new_group)

    def click_new_group(self) -> None:
        self.click(self.po.btn_new_group)

    def verify_group_listed(self, group_name: str) -> None:
        assert_element_visible(self.po.loc_group_by_name(group_name))

    def is_groups_page_loaded(self, *, timeout_ms: int = 3_000) -> bool:
        """True when the Groups list chrome is visible — i.e. not a login redirect.

        A probe, not an assertion: callers branch on the result (see
        user_ensures_logged_in), so a missing session must return False
        rather than fail the test.
        """
        try:
            expect(self.po.btn_new_group).to_be_visible(timeout=timeout_ms)
            return True
        except AssertionError:
            return False
