"""End-to-end login tests.

NOTE: Tests are marked @pytest.mark.ignore until real app URLs, credentials,
and login selectors are configured. Remove the ignore marker once verified.
"""

import allure
import pytest

from dataprovider.dp_login import get_login_test_data
from src.constants.routes import DASHBOARD_PATH
from src.core.assert_helper import assert_url_contains
from src.core.settings import get_settings
from src.steps.login_steps import (
    user_logs_in_with_credentials,
    user_navigates_to_login_page,
    user_verifies_login_error_message,
    user_verifies_login_page_is_displayed,
)
from tests.parallel_groups import PARALLEL_GROUP_LOGIN

pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_LOGIN)


@allure.epic("Authentication")
@allure.suite("Login")
@allure.feature("Login")
class TestLogin:
    """Login flow end-to-end tests."""

    @pytest.mark.e2e
    @pytest.mark.login
    @pytest.mark.p0
    @allure.story("Valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("scenario,expected_message", get_login_test_data())
    @pytest.mark.ignore
    def test_login_scenarios(self, page, scenario, expected_message):
        """Verify login behaviour for valid and invalid credential scenarios."""
        allure.dynamic.title(f"Login scenario: {scenario}")
        allure.dynamic.description(
            "Placeholder test — update selectors, credentials, and assertions "
            "once the real login flow is provided."
        )

        settings = get_settings()

        user_navigates_to_login_page(page)
        user_verifies_login_page_is_displayed(page)

        if scenario == "valid":
            user_logs_in_with_credentials(
                page,
                settings.login_user_email,
                settings.login_user_password,
            )
            assert_url_contains(page, DASHBOARD_PATH)
            allure.attach(
                page.url, name="post-login-url", attachment_type=allure.attachment_type.TEXT
            )
        else:
            user_logs_in_with_credentials(page, "invalid@example.com", "wrong-password")
            user_verifies_login_error_message(page, expected_message)
