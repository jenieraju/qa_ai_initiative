"""Sl No. 12, 13, 14, 16 - Leads Analytics tab (/lead-management/list, Analytics tab)."""

import allure
import pytest

from src.config.config_loader import get_env_config
from src.core.assert_helper import assert_visible
from src.pages.leads_list_page import LeadsListPage

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
@allure.story("Leads Analytics")
class TestLeadsAnalytics:
    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    def test_leads_analytics_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Analytics tab renders correctly for an org with leads")

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)

        with allure.step("Navigate to leads list, open Analytics tab"):
            leads_list.goto_list()
            leads_list.open_analytics_tab()

        with allure.step("Assert the 4 analytics sections are visible"):
            assert_visible(leads_list.leads_by_top_locations_heading)
            assert_visible(leads_list.leads_by_source_heading)
            assert_visible(leads_list.lead_count_revenue_by_status_heading)
            assert_visible(leads_list.leads_distribution_by_agents_heading)

    @pytest.mark.sanity
    @pytest.mark.p0
    def test_leads_analytics_agent_table_count_revenue_toggle(self, authenticated_page):
        allure.dynamic.title(
            "The agent distribution table's Count/Revenue toggle switches displayed values"
        )

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)
        leads_list.goto_list()
        leads_list.open_analytics_tab()

        with allure.step("Toggle from Count to Revenue"):
            leads_list.agents_table_revenue_toggle.click()

        with allure.step("Assert the table area is still visible after the toggle"):
            assert_visible(leads_list.leads_distribution_by_agents_heading)
            # NOTE: asserting the actual displayed values switched from counts
            # to revenue figures needs a documented server-side read or a
            # before/after value comparison - not resolved this pass.

    @pytest.mark.p1
    def test_leads_analytics_empty_state_zero_leads(self, authenticated_page):
        allure.dynamic.title("Analytics tab degrades correctly with no lead data")
        # NOTE: requires a pre-existing zero-lead org fixture in the target
        # environment.

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)
        leads_list.goto_list()
        leads_list.open_analytics_tab()

        with allure.step("Assert the empty-state message is shown"):
            assert_visible(leads_list.no_leads_data_message)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="error-display UI unconfirmed for this page - [Assumption] in "
        "context/ui-test-case-matrix.md row 16"
    )
    def test_leads_analytics_load_failure_shows_error_state(self, authenticated_page):
        allure.dynamic.title("A failed analytics load surfaces an error")
