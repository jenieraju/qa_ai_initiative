"""Quick Collect cross-feature tests (TC-QC-004).

Verifies Quick Collect link creation does not add a new group on /groups.
"""

import allure
import pytest

from dataprovider.dp_quick_collect import get_quick_collect_groups_impact_test_data
from src.core.auth_storage import DEFAULT_AUTH_PROFILE
from src.steps.groups_steps import user_counts_groups_on_list
from src.steps.login_steps import user_ensures_logged_in
from src.steps.quick_collect_steps import (
    user_creates_quick_collect_link,
    user_navigates_to_quick_collect_page,
    user_verifies_quick_collect_page_is_displayed,
)
from tests.parallel_groups import PARALLEL_GROUP_GROUPS

pytestmark = [
    pytest.mark.xdist_group(PARALLEL_GROUP_GROUPS),
    pytest.mark.auth_profile(DEFAULT_AUTH_PROFILE),
]


@allure.epic("Quick Collect")
@allure.suite("Quick Collect")
@allure.feature("Cross-feature impact")
class TestQuickCollectGroupsImpact:
    """Quick Collect must not create a group."""

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.groups
    @pytest.mark.p0
    @allure.story("TC-QC-004")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "amount,notes,payer_name,phone_number",
        get_quick_collect_groups_impact_test_data(),
    )
    def test_quick_collect_does_not_create_group(
        self, page, amount, notes, payer_name, phone_number
    ):
        """Groups list count is unchanged after a successful Quick Collect."""
        allure.dynamic.title(f"TC-QC-004: no new group after QC for {payer_name}")

        user_ensures_logged_in(page, DEFAULT_AUTH_PROFILE)
        groups_before = user_counts_groups_on_list(page)

        user_navigates_to_quick_collect_page(page)
        user_verifies_quick_collect_page_is_displayed(page)
        user_creates_quick_collect_link(page, amount, notes, payer_name, phone_number)

        groups_after = user_counts_groups_on_list(page)
        assert (
            groups_after == groups_before
        ), f"Expected group count to stay {groups_before}, got {groups_after}"
