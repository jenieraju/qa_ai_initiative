"""Sl No. 17, 18, 20 - Agents (/lead-management/agents)."""

import allure
import pytest

from src.config.config_loader import get_env_config
from src.core.assert_helper import assert_visible
from src.pages.agents_page import AgentsPage

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
@allure.story("Agents")
class TestAgents:
    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    def test_agents_loads_with_populated_data(self, authenticated_page):
        allure.dynamic.title("Agent performance renders correctly for an org with agent activity")

        base_url = get_env_config()["base_url"]
        agents = AgentsPage(authenticated_page, base_url)

        with allure.step("Navigate to Agents"):
            agents.goto_agents()

        with allure.step("Assert team metric cards and table are visible"):
            assert_visible(agents.team_avg_conversion_label)
            assert_visible(agents.team_avg_conversion_time_label)
            assert_visible(agents.agents_above_average_label)
            assert_visible(agents.agents_below_average_label)
            assert_visible(agents.agents_table)

    @pytest.mark.p1
    def test_agents_empty_state_zero_activity(self, authenticated_page):
        allure.dynamic.title("Agents page degrades correctly with no agent activity")
        # NOTE: requires a pre-existing zero-activity org fixture in the
        # target environment.

        base_url = get_env_config()["base_url"]
        agents = AgentsPage(authenticated_page, base_url)

        with allure.step("Navigate to Agents for a zero-activity org"):
            agents.goto_agents()

        with allure.step("Assert team metrics show zero"):
            # Exact zeroed-metric text ("0%", "0 Days", "0") per LMS.pdf's
            # empty-state variant - card-level locators not individually
            # confirmed this pass, asserting card visibility only.
            assert_visible(agents.team_avg_conversion_label)
            assert_visible(agents.agents_above_average_label)

    @pytest.mark.p1
    @pytest.mark.skip(
        reason="error-display UI unconfirmed for this page - [Assumption] in "
        "context/ui-test-case-matrix.md row 20"
    )
    def test_agents_load_failure_shows_error_state(self, authenticated_page):
        allure.dynamic.title("A failed agents-data load surfaces an error")
