"""LMS Dashboard page object (/lead-management/dashboard).

Locators live-confirmed 2026-08-13 via real DOM inspection (get_page_text +
read_page against https://web.dev.cofee.life), not just LMS.pdf text - two
corrections made versus the PDF-derived first draft: "Lost Leads" was
missing entirely, and the empty-state message is "No Lead Data Available"
(singular "Lead"), not "No Leads Data Available".
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LeadManagementDashboardPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Elements (live-confirmed text/role - no data-testid found) ---
        self.this_month_btn = self.page.get_by_role("button", name="This Month")
        self.last_month_btn = self.page.get_by_role("button", name="Last Month")
        self.custom_range_btn = self.page.get_by_role("button", name="Custom")
        self.stuck_leads_card = self.page.get_by_text("Stuck Leads")
        self.lost_leads_card = self.page.get_by_text("Lost Leads")
        self.overdue_leads_card = self.page.get_by_text("Overdue Leads")
        self.new_leads_card = self.page.get_by_text("New Leads")
        self.unassigned_leads_card = self.page.get_by_text("Unassigned Leads")
        self.conversion_funnel_heading = self.page.get_by_text("Conversion Funnel")
        self.conversion_rate_label = self.page.get_by_text("Conversion Rate")
        self.avg_time_to_close_label = self.page.get_by_text("Avg Time to Close")
        self.expected_revenue_label = self.page.get_by_text("Expected Revenue")
        self.no_leads_data_message = self.page.get_by_text("No Lead Data Available")

    def goto_dashboard(self) -> None:
        self.goto("lead-management/dashboard")
