"""Sl No. 6, 7, 8, 10, 11 - Leads List (/lead-management/list, List tab)."""

import allure
import pytest

from src.config.config_loader import get_env_config
from src.core.assert_helper import assert_hidden, assert_visible
from src.pages.leads_list_page import LeadsListPage
from tests.lms.lms_td import LeadsListTestData

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
@allure.story("Leads List")
class TestLeadsList:
    @pytest.mark.p1
    def test_leads_list_zero_leads_ever_shows_import_onboarding(self, authenticated_page):
        allure.dynamic.title(
            "With zero leads ever added, the List route shows an import-onboarding "
            "screen instead of a table"
        )
        # New case discovered live 2026-08-13, not in the original 27-row
        # matrix: for an org with zero leads *ever* (not just zero matching a
        # filter), /lead-management/list shows "How would you like to import
        # leads?" (CSV/Excel Upload or Add manually) - there's no table,
        # search bar, filter, or Add Lead button in this state at all. This
        # is the .env.dev account's actual real-world state - see
        # context/ui-test-case-matrix.md follow-up on whether to add this as
        # its own matrix row.

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)

        with allure.step("Navigate to leads list for a zero-leads-ever org"):
            leads_list.goto_list()

        with allure.step("Assert the import-onboarding screen is shown"):
            assert_visible(leads_list.import_leads_heading)
            assert_visible(leads_list.start_import_btn)
            assert_visible(leads_list.add_manually_btn)

    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    @pytest.mark.skip(
        reason="requires an account with >=1 lead already added - the "
        ".env.dev test account has zero leads ever, which shows a different "
        "onboarding screen instead (see test_leads_list_zero_leads_ever_"
        "shows_import_onboarding)"
    )
    def test_leads_list_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Leads table renders correctly for an org with leads")

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)

        with allure.step("Navigate to leads list"):
            leads_list.goto_list()

        with allure.step("Assert table, search, and filter are visible"):
            assert_visible(leads_list.leads_table)
            assert_visible(leads_list.search_input)
            assert_visible(leads_list.filter_btn)

    @pytest.mark.sanity
    @pytest.mark.p0
    @pytest.mark.skip(
        reason="requires an account with >=1 lead already added - the "
        ".env.dev test account has zero leads ever, so the Add Lead button "
        "isn't even reachable (see test_leads_list_zero_leads_ever_shows_"
        "import_onboarding)"
    )
    def test_add_lead_button_visible_with_permission(self, authenticated_page):
        allure.dynamic.title("A user with lead_create can see and open the Add Lead action")
        # NOTE: requires the authenticated fixture's account to actually hold
        # lead_create - not parametrized by role/permission this pass.

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)
        leads_list.goto_list()

        with allure.step("Assert Add Lead button is visible and enabled"):
            assert_visible(leads_list.add_lead_btn)

        with allure.step("Click Add Lead"):
            leads_list.add_lead_btn.click()

        with allure.step("Assert navigation toward the Add Lead page"):
            authenticated_page.wait_for_url("**/lead-management/add**")

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="requires a pre-existing test account WITH lead_create removed "
        "but WITH >=1 lead already added - this project has no role-fixture "
        "mechanism yet, and the .env.dev account's zero-leads-ever state "
        "would make the button absent for the wrong reason (the onboarding "
        "screen, not the missing permission), producing a false-positive pass"
    )
    def test_add_lead_button_hidden_without_permission(self, authenticated_page):
        allure.dynamic.title("A user without lead_create cannot see/use Add Lead")
        # NOTE: requires a pre-existing test account without lead_create -
        # this project has no role-fixture mechanism yet (see Open Questions).

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)
        leads_list.goto_list()

        with allure.step("Assert Add Lead is hidden or disabled"):
            # Exact treatment (hidden vs disabled) unconfirmed - row 8 Open
            # Question in context/ui-test-case-matrix.md.
            assert_hidden(leads_list.add_lead_btn)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="requires an account with >=1 lead already added - a search "
        "bar doesn't exist at all in the .env.dev account's zero-leads-ever "
        "onboarding state (see test_leads_list_zero_leads_ever_shows_import_"
        "onboarding)"
    )
    @pytest.mark.parametrize(
        "search_term", LeadsListTestData.ZERO_MATCH_SEARCH_TERMS
    )
    def test_leads_list_search_zero_matches(self, authenticated_page, search_term):
        allure.dynamic.title(
            "An empty search result renders a sensible empty state, not a broken table"
        )

        base_url = get_env_config()["base_url"]
        leads_list = LeadsListPage(authenticated_page, base_url)
        leads_list.goto_list()

        with allure.step(f"Search for a non-matching term: {search_term}"):
            leads_list.search_leads(search_term)

        with allure.step("Assert a no-results indication is shown"):
            assert_visible(leads_list.no_results_message)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="error-display UI unconfirmed for this page - [Assumption] in "
        "context/ui-test-case-matrix.md row 11"
    )
    def test_leads_list_load_failure_shows_error_state(self, authenticated_page):
        allure.dynamic.title("A failed table load surfaces an error")
