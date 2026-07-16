"""End-to-end new-user onboarding tests for web.dev.cofee.life.

Live flow (confirmed against https://web.dev.cofee.life/login):

  /login  →  mobile + terms → Continue
  /login  →  Verification Code (OTP) → Continue
  /select-account  →  "Help us get to know you"
      → name + Individual | Organization + business name → Continue
          Individual   → lands on /groups
          Organization → /document-upload → /select-payment → /groups

Each run needs a **fresh** mobile (zero orgs). Reusing a number skips
/select-account and goes straight into the app. OTP comes from settings
(FEATURE_LOGIN_OTP / SHARED_OTP); mobiles are generated per test so suite
runs do not burn a shared credential.

Organization scenarios stay @pytest.mark.ignore until KYC/bank env vars are set
(FEATURE_ONBOARDING_PAN, FEATURE_ONBOARDING_DOCUMENT_PATH,
FEATURE_ONBOARDING_BANK_ACCOUNT_NUMBER, FEATURE_ONBOARDING_BANK_IFSC).

No teardown: the app has no delete API for the org/user this flow creates.
"""

import uuid

import allure
import pytest

from dataprovider.dp_onboarding import (
    get_individual_onboarding_test_data,
    get_organization_onboarding_test_data,
)
from src.constants.routes import (
    DOCUMENT_UPLOAD_PATH,
    GROUPS_PATH,
    SELECT_ACCOUNT_PATH,
    SELECT_PAYMENT_PATH,
)
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


def _fresh_mobile_number() -> str:
    """Return a unique 10-digit sandbox mobile for one onboarding attempt."""
    return f"98{uuid.uuid4().int % 10**8:08d}"


def _login_new_user_to_account_selection(page, mobile_number: str) -> None:
    """Login → OTP → assert /select-account (referral screen is currently unreachable)."""
    settings = get_settings()
    user_navigates_to_login_page(page)
    user_logs_in_with_mobile_and_otp(page, mobile_number, settings.login_otp)
    assert_url_contains(page, SELECT_ACCOUNT_PATH)
    user_verifies_account_selection_page_is_displayed(page)


def _attach_post_flow_url(page, name: str = "post-onboarding-url") -> None:
    allure.attach(page.url, name=name, attachment_type=allure.attachment_type.TEXT)


@allure.epic("Authentication")
@allure.suite("Onboarding")
@allure.feature("Onboarding")
class TestOnboarding:
    """New-user onboarding — Individual and Organization paths from /login."""

    @pytest.mark.e2e
    @pytest.mark.onboarding
    @pytest.mark.p0
    @allure.story("Individual onboarding")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("profile_name,business_name", get_individual_onboarding_test_data())
    def test_individual_onboarding(self, page, profile_name, business_name):
        """New individual user: /select-account → /groups."""
        mobile_number = _fresh_mobile_number()
        allure.dynamic.title(f"Individual onboarding: {profile_name} ({mobile_number})")

        _login_new_user_to_account_selection(page, mobile_number)
        user_completes_individual_onboarding(page, profile_name, business_name)

        assert_url_contains(page, GROUPS_PATH)
        _attach_post_flow_url(page)

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
        """New org user: /select-account → /document-upload → /select-payment → /groups."""
        mobile_number = _fresh_mobile_number()
        allure.dynamic.title(f"Organization onboarding: {organization_name} ({mobile_number})")
        settings = get_settings()

        _login_new_user_to_account_selection(page, mobile_number)
        user_completes_organization_onboarding(page, profile_name, organization_name)
        assert_url_contains(page, DOCUMENT_UPLOAD_PATH)

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
        assert_url_contains(page, SELECT_PAYMENT_PATH)

        user_completes_payment_selection(
            page,
            settings.feature_onboarding_bank_account_number,
            settings.feature_onboarding_bank_ifsc,
        )

        assert_url_contains(page, GROUPS_PATH)
        _attach_post_flow_url(page)
