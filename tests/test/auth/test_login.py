"""End-to-end login tests.

NOTE: Tests are marked @pytest.mark.ignore until a mobile number + OTP pair
accepted by the target environment is configured (FEATURE_LOGIN_MOBILE_NUMBER /
FEATURE_LOGIN_OTP — e.g. a fixed sandbox OTP). Remove the ignore marker once verified.
"""

import allure
import pytest

from dataprovider.dp_login import get_login_test_data
from src.constants.routes import DASHBOARD_PATH
from src.core.assert_helper import assert_url_contains
from src.core.settings import get_settings
from src.steps.login_steps import (
    user_logs_in_with_mobile_and_otp,
    user_navigates_to_login_page,
    user_submits_mobile_number,
    user_verifies_invalid_mobile_number_error,
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
    @allure.story("Mobile number + OTP")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("scenario,expected_message", get_login_test_data())
    def test_login_scenarios(self, page, scenario, expected_message):
        """Verify login behaviour for valid and invalid mobile number scenarios."""
        allure.dynamic.title(f"Login scenario: {scenario}")

        settings = get_settings()

        user_navigates_to_login_page(page)
        user_verifies_login_page_is_displayed(page)

        if scenario == "valid":
            user_logs_in_with_mobile_and_otp(
                page,
                settings.login_mobile_number,
                settings.login_otp,
            )
            assert_url_contains(page, DASHBOARD_PATH)
            allure.attach(
                page.url, name="post-login-url", attachment_type=allure.attachment_type.TEXT
            )
        else:
            user_submits_mobile_number(page, "9999999999")
            user_verifies_invalid_mobile_number_error(page, expected_message)
