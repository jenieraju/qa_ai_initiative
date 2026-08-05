"""Add Member form page object — locators only.

TODO: placeholder locators, not confirmed against the live app or its
source — including whether Add Member is a modal or a separate route.
Run discover-locators-from-ui before removing @pytest.mark.ignore from
tests/test/members/test_member_create.py.
"""

from src.constants.messages import (
    BTN_SAVE_MEMBER,
    HEADING_ADD_MEMBER,
    MSG_MEMBER_CREATED,
    PLACEHOLDER_MEMBER_MOBILE_NUMBER,
    PLACEHOLDER_MEMBER_NAME,
)
from src.core.base_page import BasePage


class MemberCreatePage(BasePage):
    """Page object for the Add Member form (modal or route — TBD)."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.lbl_heading = self.get_by_text(HEADING_ADD_MEMBER, exact=True)
        self.input_member_name = self.get_by_placeholder(PLACEHOLDER_MEMBER_NAME)
        self.input_mobile_number = self.get_by_placeholder(PLACEHOLDER_MEMBER_MOBILE_NUMBER)
        self.btn_save = self.get_by_button(BTN_SAVE_MEMBER)
        self.btn_cancel = self.get_by_button("Cancel")
        self.msg_member_created = self.get_by_text(MSG_MEMBER_CREATED, exact=True)
