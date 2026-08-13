"""Sources page object (/lead-management/sources). Locators from LMS.pdf visible text."""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class SourcesPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (text/role sourced from LMS.pdf - no data-testid confirmed) ---
        self.top_volume_label = self.page.get_by_text("Top Volume")
        self.highest_conversion_label = self.page.get_by_text("Highest Conversion")
        self.highest_revenue_label = self.page.get_by_text("Highest Revenue")
        self.distribution_by_source_heading = self.page.get_by_text(
            "Distribution by source"
        )
        self.view_ad_sources_link = self.page.get_by_role(
            "link", name="View Ad Sources"
        )
        self.no_lead_sources_message = self.page.get_by_text("No lead sources found")
        self.no_data_to_show_message = self.page.get_by_text("No data to show!")

    def goto_sources(self) -> None:
        self.goto("lead-management/sources")
