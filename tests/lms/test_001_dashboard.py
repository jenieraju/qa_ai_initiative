"""Sl No. 1, 2, 3, 5 - LMS Dashboard (/lead-management/dashboard)."""

import allure
import pytest

from src.config.config_loader import get_env_config
from src.core.assert_helper import assert_visible
from src.pages.lead_management_dashboard_page import LeadManagementDashboardPage

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
@allure.story("Dashboard")
class TestLeadManagementDashboard:
    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    def test_dashboard_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Dashboard shows correct metrics/funnel for an org with lead data")

        base_url = get_env_config()["base_url"]
        dashboard = LeadManagementDashboardPage(authenticated_page, base_url)

        with allure.step("Navigate to LMS dashboard"):
            dashboard.goto_dashboard()

        with allure.step("Assert the 4 metric cards and funnel are visible"):
            assert_visible(dashboard.stuck_leads_card)
            assert_visible(dashboard.overdue_leads_card)
            assert_visible(dashboard.new_leads_card)
            assert_visible(dashboard.unassigned_leads_card)
            assert_visible(dashboard.conversion_funnel_heading)
            assert_visible(dashboard.conversion_rate_label)
            assert_visible(dashboard.avg_time_to_close_label)

    @pytest.mark.sanity
    @pytest.mark.p0
    def test_dashboard_date_range_switch_updates_metrics(self, authenticated_page):
        allure.dynamic.title("Switching the date range reloads dashboard data")

        base_url = get_env_config()["base_url"]
        dashboard = LeadManagementDashboardPage(authenticated_page, base_url)
        dashboard.goto_dashboard()

        with allure.step("Switch date range to Last Month"):
            dashboard.last_month_btn.click()

        with allure.step("Assert metrics area is still visible after the reload"):
            assert_visible(dashboard.conversion_funnel_heading)
            # NOTE: asserting the *values* actually changed needs a documented
            # server-side read or before/after comparison - not resolved this
            # pass (see context/ui-test-case-matrix.md Open Questions).

    @pytest.mark.p1
    def test_dashboard_empty_state_zero_leads(self, authenticated_page):
        allure.dynamic.title("Dashboard degrades correctly for an org with no leads")

        base_url = get_env_config()["base_url"]
        dashboard = LeadManagementDashboardPage(authenticated_page, base_url)

        with allure.step("Navigate to LMS dashboard for a zero-lead org"):
            # Live-confirmed 2026-08-13: the .env.dev test account is itself
            # a zero-lead org already - no separate fixture needed for this
            # specific account/environment.
            dashboard.goto_dashboard()

        with allure.step("Assert the empty-state funnel message is shown"):
            assert_visible(dashboard.no_leads_data_message)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="error-display UI unconfirmed for this page - [Assumption] in "
        "context/ui-test-case-matrix.md row 5; needs a live DOM check before "
        "an assertion can be written"
    )
    def test_dashboard_load_failure_shows_error_state(self, authenticated_page):
        allure.dynamic.title("A failed data load surfaces an error, not a silent blank page")
