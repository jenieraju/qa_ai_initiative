"""Leads List page object (/lead-management/list) - includes the Analytics tab
(LeadAnalytics component, same route, not a separate page - see context/ui-context.md).
Locators from LMS.pdf visible text and cofee-web route/permission source.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LeadsListPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        # --- List tab elements ---
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
        self.no_leads_data_message = self.page.get_by_text("No Leads Data Available")

    def goto_list(self) -> None:
        self.goto("lead-management/list")

    def open_analytics_tab(self) -> None:
        self.analytics_tab.click()

    def search_leads(self, term: str) -> None:
        self.search_input.fill(term)
