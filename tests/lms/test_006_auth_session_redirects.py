"""Sl No. 4, 9, 15, 19, 26 - identical shape (unauthenticated -> redirected to /login),
parametrized into one test per ui-test-design's Parametrization guidance.
"""

import allure
import pytest

from src.config.config_loader import get_env_config
from tests.lms.lms_td import AuthSessionRedirectTestData

pytestmark = pytest.mark.regression


@allure.epic("CoFee UI")
@allure.feature("Lead Management")
class TestAuthSessionRedirects:
    @pytest.mark.smoke
    @pytest.mark.sanity
    @pytest.mark.p0
    @pytest.mark.parametrize(
        "target_path", AuthSessionRedirectTestData.UNAUTHENTICATED_REDIRECT_PATHS
    )
    def test_unauthenticated_access_redirects_to_login(
        self, unauthenticated_page, target_path
    ):
        allure.dynamic.title(
            f"Unauthenticated access to /{target_path} redirects to /login"
        )

        base_url = get_env_config()["base_url"].rstrip("/")

        with allure.step(f"Navigate to /{target_path} with no active session"):
            unauthenticated_page.goto(f"{base_url}/{target_path}")

        with allure.step("Assert redirected to /login"):
            unauthenticated_page.wait_for_url("**/login**")
