"""Members list page object — locators only.

TODO: placeholder locators, not confirmed against the live app or its
source. Run discover-locators-from-ui against the real Members tab before
removing @pytest.mark.ignore from tests/test/members/test_member_create.py.
"""

from playwright.sync_api import Locator

from src.constants.messages import BTN_ADD_MEMBER
from src.core.base_page import BasePage


class MembersPage(BasePage):
    """Page object for the /members list screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.btn_add_member = self.get_by_button(BTN_ADD_MEMBER)

    def loc_member_by_name(self, member_name: str) -> Locator:
        return self.get_by_text(member_name, exact=True)
