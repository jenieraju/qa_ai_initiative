"""End-to-end member creation tests.

Assumed flow (NOT yet confirmed against the live app — see TODOs below):

  Authenticated session -> /members -> Add Member -> name + mobile number
      -> Save -> "Member added successfully"
      -> member appears on /members

Session reuse: same pattern as Groups — prefer cookies from
.auth/default.json via @pytest.mark.auth_profile("default"); falls back to
a real UI login via user_ensures_logged_in() if that file is missing/expired.

TODO before removing @pytest.mark.ignore:
  - Confirm MEMBERS_PATH and every locator in members_po.py /
    member_create_po.py against the live app (discover-locators-from-ui).
  - Confirm whether Add Member is a modal or a separate route.
  - Confirm the required field set (name/mobile assumed; email/role/group
    assignment unconfirmed).
  - Confirm whether a delete-member API exists — if so, wire
    teardown_registry (see AGENTS.md -> "Teardown" and
    .claude/skills/test-data-teardown/SKILL.md) instead of leaving this
    without cleanup.
"""

import allure
import pytest

from dataprovider.dp_member_create import get_member_create_test_data
from src.core.auth_storage import DEFAULT_AUTH_PROFILE
from src.steps.login_steps import user_ensures_logged_in
from src.steps.member_create_steps import (
    user_completes_member_basic_details,
    user_verifies_member_create_page_is_displayed,
    user_verifies_member_created_successfully,
)
from src.steps.members_steps import (
    user_clicks_add_member,
    user_navigates_to_members_page,
    user_verifies_member_is_listed,
    user_verifies_members_page_is_displayed,
)
from tests.parallel_groups import PARALLEL_GROUP_MEMBERS

pytestmark = [
    pytest.mark.xdist_group(PARALLEL_GROUP_MEMBERS),
    pytest.mark.auth_profile(DEFAULT_AUTH_PROFILE),
]


@allure.epic("Members")
@allure.suite("Member management")
@allure.feature("Member creation")
class TestMemberCreate:
    """Create a member from the members list — basic details."""

    @pytest.mark.e2e
    @pytest.mark.members
    @pytest.mark.p1
    @pytest.mark.ignore  # placeholder selectors — remove once real Members/Add Member locators are confirmed
    @allure.story("Create member — basic details")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("member_name,mobile_number", get_member_create_test_data())
    def test_create_member_basic_details(self, page, member_name, mobile_number):
        """Logged-in user creates a member and sees it on the members list."""
        allure.dynamic.title(f"Create member: {member_name}")

        user_ensures_logged_in(page, DEFAULT_AUTH_PROFILE)
        user_navigates_to_members_page(page)
        user_verifies_members_page_is_displayed(page)
        user_clicks_add_member(page)
        user_verifies_member_create_page_is_displayed(page)

        user_completes_member_basic_details(page, member_name, mobile_number)
        user_verifies_member_created_successfully(page)

        user_navigates_to_members_page(page)
        user_verifies_members_page_is_displayed(page)
        user_verifies_member_is_listed(page, member_name)

        allure.attach(page.url, name="post-create-url", attachment_type=allure.attachment_type.TEXT)
