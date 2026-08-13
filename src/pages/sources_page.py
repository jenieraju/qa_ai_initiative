"""Sources page object (/lead-management/sources).

Live-confirmed 2026-08-13 for the .env.dev test account: "Top Volume" /
"Highest Conversion" / "Highest Revenue" / "Distribution by source" /
"No data to show!" all confirmed exactly. IMPORTANT nuance: for this
account, the distribution table still renders one row per standard channel
(Facebook Ads, Website, etc.), all zeroed, rather than showing
"No lead sources found" - that message may only apply to an org with zero
sources *configured* at all (a more extreme state this account doesn't
represent), not to an org with configured sources but zero lead volume.
Kept the locator since it's a real string somewhere in the app, but matrix
row 24 needs a different account/state to actually exercise it - see
context/ui-test-case-matrix.md follow-up.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class SourcesPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (live-confirmed text/role - no data-testid found) ---
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
