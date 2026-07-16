"""End-to-end group creation tests.

Live flow (web.dev.cofee.life):

  Authenticated session → /groups → New Group → /groups/create
      → name + monthly collection day + amount → Save and next
      → "Group created successfully"
      → group appears on /groups

Session reuse:
  - Prefer cookies from `.auth/default.json` (saved by a prior login test) via
    @pytest.mark.auth_profile("default").
  - If that file is missing/expired, user_ensures_logged_in() UI-logs in with
    FEATURE_LOGIN_MOBILE_NUMBER / FEATURE_LOGIN_OTP and saves a fresh state.

No teardown — confirm delete-group API with the app team before wiring
teardown_registry.
"""

import allure
import pytest

from dataprovider.dp_group_create import get_group_create_test_data
from src.constants.routes import GROUPS_CREATE_PATH, GROUPS_PATH
from src.core.assert_helper import assert_url_contains
from src.core.auth_storage import DEFAULT_AUTH_PROFILE
from src.steps.group_create_steps import (
    user_completes_group_basic_details,
    user_verifies_group_create_page_is_displayed,
    user_verifies_group_created_successfully,
)
from src.steps.groups_steps import (
    user_clicks_new_group,
    user_navigates_to_groups_page,
    user_verifies_group_is_listed,
    user_verifies_groups_page_is_displayed,
)
from src.steps.login_steps import user_ensures_logged_in
from tests.parallel_groups import PARALLEL_GROUP_GROUPS

pytestmark = [
    pytest.mark.xdist_group(PARALLEL_GROUP_GROUPS),
    pytest.mark.auth_profile(DEFAULT_AUTH_PROFILE),
]


@allure.epic("Groups")
@allure.suite("Group management")
@allure.feature("Group creation")
class TestGroupCreate:
    """Create a group from the groups list — basic details step."""

    @pytest.mark.e2e
    @pytest.mark.groups
    @pytest.mark.p1
    @allure.story("Create group — basic details")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("group_name,amount", get_group_create_test_data())
    def test_create_group_basic_details(self, page, group_name, amount):
        """Logged-in user creates a group and sees it on the groups list."""
        allure.dynamic.title(f"Create group: {group_name}")

        user_ensures_logged_in(page, DEFAULT_AUTH_PROFILE)
        user_navigates_to_groups_page(page)
        user_verifies_groups_page_is_displayed(page)
        user_clicks_new_group(page)
        assert_url_contains(page, GROUPS_CREATE_PATH)
        user_verifies_group_create_page_is_displayed(page)

        user_completes_group_basic_details(page, group_name, amount)
        user_verifies_group_created_successfully(page)

        user_navigates_to_groups_page(page)
        user_verifies_groups_page_is_displayed(page)
        user_verifies_group_is_listed(page, group_name)
        assert_url_contains(page, GROUPS_PATH)

        allure.attach(page.url, name="post-create-url", attachment_type=allure.attachment_type.TEXT)
