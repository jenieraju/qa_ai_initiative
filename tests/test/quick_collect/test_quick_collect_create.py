"""End-to-end Quick Collect create-link tests (TC-QC-001).

Live flow (web.dev.cofee.life):

  Authenticated session → /quick-collect/create-link
      → amount + notes → Add from members list → Send → Confirm
      → /quick-collect/success → "Payment link sent successfully!"
"""

import allure
import pytest

from dataprovider.dp_quick_collect import get_quick_collect_create_test_data
from src.constants.routes import QUICK_COLLECT_CREATE_PATH, QUICK_COLLECT_SUCCESS_PATH
from src.core.assert_helper import assert_url_contains
from src.core.auth_storage import DEFAULT_AUTH_PROFILE
from src.steps.login_steps import user_ensures_logged_in
from src.steps.quick_collect_steps import (
    user_completes_quick_collect_form,
    user_generates_quick_collect_link,
    user_navigates_to_quick_collect_page,
    user_verifies_quick_collect_link_created,
    user_verifies_quick_collect_page_is_displayed,
)
from tests.parallel_groups import PARALLEL_GROUP_GROUPS

pytestmark = [
    pytest.mark.xdist_group(PARALLEL_GROUP_GROUPS),
    pytest.mark.auth_profile(DEFAULT_AUTH_PROFILE),
]


@allure.epic("Quick Collect")
@allure.suite("Quick Collect")
@allure.feature("Create payment link")
class TestQuickCollectCreate:
    """Create a one-off Quick Collect payment link — happy path."""

    @pytest.mark.e2e
    @pytest.mark.quick_collect
    @pytest.mark.p0
    @allure.story("TC-QC-001")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "amount,notes,payer_name,phone_number",
        get_quick_collect_create_test_data(),
    )
    def test_create_quick_collect_link_valid_amount(
        self, page, amount, notes, payer_name, phone_number
    ):
        """Logged-in user creates a Quick Collect link with one payer."""
        allure.dynamic.title(f"TC-QC-001: Quick Collect link for {payer_name}")

        user_ensures_logged_in(page, DEFAULT_AUTH_PROFILE)
        user_navigates_to_quick_collect_page(page)
        assert_url_contains(page, QUICK_COLLECT_CREATE_PATH)
        user_verifies_quick_collect_page_is_displayed(page)

        user_completes_quick_collect_form(page, amount, notes, payer_name, phone_number)
        user_generates_quick_collect_link(page)
        user_verifies_quick_collect_link_created(page)

        assert_url_contains(page, QUICK_COLLECT_SUCCESS_PATH)
        allure.attach(page.url, name="post-create-url", attachment_type=allure.attachment_type.TEXT)
