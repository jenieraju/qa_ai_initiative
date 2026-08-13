"""Sl No. 21, 22, 23, 24, 25, 27 - Sources (/lead-management/sources) and
Ad Sources (/lead-management/sources/ad-sources).
"""

import allure
import pytest

from src.config.config_loader import get_env_config
from src.core.assert_helper import assert_visible
from src.pages.ad_sources_page import AdSourcesPage
from src.pages.sources_page import SourcesPage
from tests.lms.lms_td import AdSourcesTestData

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
@allure.story("Sources")
class TestSources:
    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    def test_sources_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Lead sources render correctly for an org with source data")

        base_url = get_env_config()["base_url"]
        sources = SourcesPage(authenticated_page, base_url)

        with allure.step("Navigate to Sources"):
            sources.goto_sources()

        with allure.step("Assert metric cards and Ad Sources link are visible"):
            assert_visible(sources.top_volume_label)
            assert_visible(sources.highest_conversion_label)
            assert_visible(sources.highest_revenue_label)
            assert_visible(sources.distribution_by_source_heading)
            assert_visible(sources.view_ad_sources_link)

    @pytest.mark.sanity
    @pytest.mark.p0
    def test_sources_navigate_to_ad_sources(self, authenticated_page):
        allure.dynamic.title("The Ad Sources link navigates to the ad-sources view")

        base_url = get_env_config()["base_url"]
        sources = SourcesPage(authenticated_page, base_url)
        sources.goto_sources()

        with allure.step("Click View Ad Sources"):
            sources.view_ad_sources_link.click()

        with allure.step("Assert navigation to the ad-sources route"):
            authenticated_page.wait_for_url("**/lead-management/sources/ad-sources**")

    @pytest.mark.sanity
    @pytest.mark.p0
    def test_ad_sources_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Ad-sources breakdown renders correctly with ad campaign data")

        base_url = get_env_config()["base_url"]
        ad_sources = AdSourcesPage(authenticated_page, base_url)

        with allure.step("Navigate to Ad Sources"):
            ad_sources.goto_ad_sources()

        with allure.step("Assert metric cards and distribution table are visible"):
            assert_visible(ad_sources.top_volume_label)
            assert_visible(ad_sources.highest_conversion_label)
            assert_visible(ad_sources.highest_revenue_label)
            assert_visible(ad_sources.distribution_by_ad_heading)

    @pytest.mark.p1
    def test_sources_empty_state_no_sources(self, authenticated_page):
        allure.dynamic.title("Sources page degrades correctly with no source data")
        # Live-confirmed 2026-08-13: the .env.dev account (zero lead volume,
        # but standard source channels still configured/listed) shows
        # "No data to show!" on the 3 metric cards, NOT "No lead sources
        # found" - that message may need a more extreme zero-sources-
        # configured-at-all account to actually exercise (not available
        # this pass - see context/ui-test-case-matrix.md follow-up).

        base_url = get_env_config()["base_url"]
        sources = SourcesPage(authenticated_page, base_url)

        with allure.step("Navigate to Sources for a zero-lead-volume org"):
            sources.goto_sources()

        with allure.step('Assert "No data to show!" is shown on the metric cards'):
            assert_visible(sources.no_data_to_show_message)

    @pytest.mark.p1
    @pytest.mark.parametrize(
        "search_term", AdSourcesTestData.ZERO_MATCH_SEARCH_TERMS
    )
    def test_ad_sources_search_zero_matches(self, authenticated_page, search_term):
        allure.dynamic.title(
            "An ad-sources search with no matches renders a sensible empty state"
        )

        base_url = get_env_config()["base_url"]
        ad_sources = AdSourcesPage(authenticated_page, base_url)
        ad_sources.goto_ad_sources()

        with allure.step(f"Search ad sources for a non-matching term: {search_term}"):
            ad_sources.search_ad_sources(search_term)

        with allure.step('Assert "No data to show!" is shown'):
            assert_visible(ad_sources.no_data_to_show_message)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="error-display UI unconfirmed for this page - [Assumption] in "
        "context/ui-test-case-matrix.md row 27"
    )
    def test_sources_load_failure_shows_error_state(self, authenticated_page):
        allure.dynamic.title("A failed sources-data load surfaces an error")
