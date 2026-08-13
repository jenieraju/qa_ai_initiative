"""Leads List page object (/lead-management/list) - includes the Analytics tab
(LeadAnalytics component, same route, not a separate page - see context/ui-context.md).

Live-confirmed 2026-08-13 for the .env.dev test account (zero leads org-wide):
IMPORTANT - with zero leads ever added (not just zero matching a filter),
/lead-management/list shows an onboarding screen ("How would you like to
import leads?" - CSV/Excel Upload or Add manually) INSTEAD of the table,
search bar, filter button, or Add Lead button. None of those elements exist
on the page in that state. This is a materially different state from a
"table exists but a search/filter yielded zero rows" empty state - the
matrix's row 6 (populated table) and row 10 (search zero-match) both assume
a table exists, which isn't true for an org with zero leads ever - see
context/ui-test-case-matrix.md for the follow-up needed here.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LeadsListPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- Zero-leads-ever onboarding screen (live-confirmed) ---
        self.import_leads_heading = self.page.get_by_text("How would you like to import leads?")
        self.start_import_btn = self.page.get_by_role("button", name="Start Import")
        self.add_manually_btn = self.page.get_by_role("button", name="Add Manually")

        # --- List tab elements (only present once at least one lead exists - not
        # yet live-confirmed against an account that actually has lead data) ---
        self.list_tab = self.page.get_by_role("tab", name="List")
        self.analytics_tab = self.page.get_by_role("tab", name="Analytics")
        self.search_input = self.page.get_by_role("searchbox")
        self.filter_btn = self.page.get_by_role("button", name="Filter")
        self.add_lead_btn = self.page.get_by_role("button", name="Add Lead")
        self.leads_table = self.page.get_by_role("table")
        self.no_results_message = self.page.get_by_text(
            "No leads found"
        )  # [Assumption] - exact copy unconfirmed, see matrix Open Questions

        # --- Analytics tab elements ---
        self.leads_by_top_locations_heading = self.page.get_by_text(
            "Leads By Top Locations"
        )
        self.leads_by_source_heading = self.page.get_by_text("Leads By Source")
        self.lead_count_revenue_by_status_heading = self.page.get_by_text(
            "Lead Count & Revenue By Status"
        )
        self.leads_distribution_by_agents_heading = self.page.get_by_text(
            "Leads Distribution By Agents"
        )
        self.agents_table_count_toggle = self.page.get_by_role("button", name="Count")
        self.agents_table_revenue_toggle = self.page.get_by_role(
            "button", name="Revenue"
        )
        # Live-confirmed as "No Lead Data Available" (singular "Lead") on the
        # Dashboard's identical-looking empty state - assumed, not directly
        # re-confirmed, to be the same shared component/text here.
        self.no_leads_data_message = self.page.get_by_text("No Lead Data Available")

    def goto_list(self) -> None:
        self.goto("lead-management/list")

    def open_analytics_tab(self) -> None:
        self.analytics_tab.click()

    def search_leads(self, term: str) -> None:
        self.search_input.fill(term)
