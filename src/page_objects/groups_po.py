"""Groups list page object — locators only."""

from playwright.sync_api import Locator

from src.core.base_page import BasePage


class GroupsPage(BasePage):
    """Page object for the /groups list screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        self.btn_new_group = self.get_by_button("New Group")

    def loc_group_by_name(self, group_name: str) -> Locator:
        return self.get_by_text(group_name, exact=True)
