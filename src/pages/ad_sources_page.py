"""Ad Sources page object (/lead-management/sources/ad-sources).

Live-confirmed 2026-08-13. Two corrections versus the PDF-derived first
draft: the heading is "Distribution by ad" (lowercase "ad"), not
"Distribution by Ad". Also, for the .env.dev test account, the distribution
table actually errors ("Something went wrong. Please try again later.")
rather than rendering an empty/zeroed table - this is real, observed
error-display text (resolves the [Assumption] tag on matrix row 27,
at least for this specific failure mode).
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AdSourcesPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (live-confirmed text/role - no data-testid found) ---
        self.top_volume_label = self.page.get_by_text("Top Volume")
        self.highest_conversion_label = self.page.get_by_text("Highest Conversion")
        self.highest_revenue_label = self.page.get_by_text("Highest Revenue")
        self.distribution_by_ad_heading = self.page.get_by_text("Distribution by ad")
        self.search_input = self.page.get_by_role("searchbox")
        self.no_data_to_show_message = self.page.get_by_text("No data to show!")
        self.something_went_wrong_message = self.page.get_by_text("Something went wrong")

    def goto_ad_sources(self) -> None:
        self.goto("lead-management/sources/ad-sources")

    def search_ad_sources(self, term: str) -> None:
        self.search_input.fill(term)
