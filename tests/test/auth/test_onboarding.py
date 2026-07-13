"""End-to-end new-user onboarding tests.

NOTE: Both flows start from a fresh login, so they need the same
FEATURE_LOGIN_MOBILE_NUMBER / FEATURE_LOGIN_OTP as test_login.py, pointed at a
mobile number with zero existing organizations (so the app redirects to
AUTH.SELECT_ACCOUNT instead of the dashboard). The organization flow
additionally needs real KYC/bank verification test data
(FEATURE_ONBOARDING_PAN, FEATURE_ONBOARDING_DOCUMENT_PATH,
FEATURE_ONBOARDING_BANK_ACCOUNT_NUMBER, FEATURE_ONBOARDING_BANK_IFSC).
Tests stay @pytest.mark.ignore (via dataprovider marks) until that data is
configured for an environment that accepts it — remove the marker there once verified.
"""

import allure
import pytest

from dataprovider.dp_onboarding import (
    get_individual_onboarding_test_data,
    get_organization_onboarding_test_data,
)
from src.constants.routes import DASHBOARD_PATH
from src.core.assert_helper import assert_url_contains
from src.core.settings import get_settings
from src.steps.document_upload_steps import user_completes_document_upload
from src.steps.login_steps import user_logs_in_with_mobile_and_otp, user_navigates_to_login_page
from src.steps.onboarding_steps import (
    user_completes_individual_onboarding,
    user_completes_organization_onboarding,
    user_verifies_account_selection_page_is_displayed,
)
from src.steps.payment_selection_steps import user_completes_payment_selection
from tests.parallel_groups import PARALLEL_GROUP_ONBOARDING

pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_ONBOARDING)


def _login_new_user(page) -> None:
    # Referral-code screen is currently unreachable: useReferralCode's
    # `referralStatus` defaults to true and nothing in the app ever flips it
    # false, so AccountSelection always renders its main form directly.
    # Confirmed against the live dev app — remove the skip-referral steps
    # entirely once that hook is either wired up or removed upstream.
    settings = get_settings()
    user_navigates_to_login_page(page)
    user_logs_in_with_mobile_and_otp(page, settings.login_mobile_number, settings.login_otp)
    user_verifies_account_selection_page_is_displayed(page)


@allure.epic("Authentication")
@allure.suite("Onboarding")
@allure.feature("Onboarding")
class TestOnboarding:
    """New-user onboarding flow end-to-end tests."""

    @pytest.mark.e2e
    @pytest.mark.onboarding
    @pytest.mark.p0
    @allure.story("Individual onboarding")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("profile_name,business_name", get_individual_onboarding_test_data())
    def test_individual_onboarding(self, page, profile_name, business_name):
        """A brand-new individual user completes onboarding and reaches the dashboard."""
        allure.dynamic.title(f"Individual onboarding: {profile_name}")

        _login_new_user(page)
        user_completes_individual_onboarding(page, profile_name, business_name)

        assert_url_contains(page, DASHBOARD_PATH)
        allure.attach(
            page.url, name="post-onboarding-url", attachment_type=allure.attachment_type.TEXT
        )

    @pytest.mark.e2e
    @pytest.mark.onboarding
    @pytest.mark.p0
    @allure.story("Organization onboarding")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize(
        "profile_name,organization_name,certificate_type,business_license_type",
        get_organization_onboarding_test_data(),
    )
    def test_organization_onboarding(
        self, page, profile_name, organization_name, certificate_type, business_license_type
    ):
        """A brand-new organization user completes onboarding and reaches the dashboard."""
        allure.dynamic.title(f"Organization onboarding: {organization_name}")

        settings = get_settings()

        _login_new_user(page)
        user_completes_organization_onboarding(page, profile_name, organization_name)

        card_number = (
            settings.feature_onboarding_pan
            if certificate_type == "pan"
            else settings.feature_onboarding_gstin
        )
        user_completes_document_upload(
            page,
            certificate_type=certificate_type,
            card_number=card_number,
            certificate_file_path=settings.feature_onboarding_document_path,
            business_license_type=business_license_type,
            business_license_file_path=settings.feature_onboarding_document_path,
        )
        user_completes_payment_selection(
            page,
            settings.feature_onboarding_bank_account_number,
            settings.feature_onboarding_bank_ifsc,
        )

        assert_url_contains(page, DASHBOARD_PATH)
        allure.attach(
            page.url, name="post-onboarding-url", attachment_type=allure.attachment_type.TEXT
        )
