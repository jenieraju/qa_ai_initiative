"""Ad Sources page object (/lead-management/sources/ad-sources). Locators from LMS.pdf visible text."""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdSourcesPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (text/role sourced from LMS.pdf visible text - no data-testid confirmed) ---
        self.top_volume_label = self.page.get_by_text("Top Volume")
        self.highest_conversion_label = self.page.get_by_text("Highest Conversion")
        self.highest_revenue_label = self.page.get_by_text("Highest Revenue")
        self.distribution_by_ad_heading = self.page.get_by_text("Distribution by Ad")
        self.search_input = self.page.get_by_role("searchbox")
        self.no_data_to_show_message = self.page.get_by_text("No data to show!")

    def goto_ad_sources(self) -> None:
        self.goto("lead-management/sources/ad-sources")

    def search_ad_sources(self, term: str) -> None:
        self.search_input.fill(term)
