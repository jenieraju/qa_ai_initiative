"""Agents page object (/lead-management/agents). Locators from LMS.pdf visible text."""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AgentsPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (text/role sourced from LMS.pdf - no data-testid confirmed) ---
        self.team_avg_conversion_label = self.page.get_by_text("Team Average Conversion")
        self.team_avg_conversion_time_label = self.page.get_by_text(
            "Team Avg Conversion Time"
        )
        self.agents_above_average_label = self.page.get_by_text("Agents Above Average")
        self.agents_below_average_label = self.page.get_by_text("Agents Below Average")
        self.search_input = self.page.get_by_role("searchbox")
        self.filter_btn = self.page.get_by_role("button", name="Filter")
        self.agents_table = self.page.get_by_role("table")

    def goto_agents(self) -> None:
        self.goto("lead-management/agents")
