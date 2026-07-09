"""Onboarding test data provider.

Business/profile/org names are not secrets and are embedded directly.
PAN/GSTIN, bank details, and document file paths are credential-like test
data — those are read from settings inside the test, never here.
"""

import pytest

from src.page_objects.document_upload_po import CERTIFICATE_TYPE_PAN


def get_individual_onboarding_test_data() -> list:
    """Return parametrized individual-onboarding scenarios.

    Ignored until a mobile number + OTP pair accepted by the target
    environment is configured (FEATURE_LOGIN_MOBILE_NUMBER / FEATURE_LOGIN_OTP).
    """
    return [
        pytest.param(
            "Automation Individual",
            "Automation Individual Business",
            id="individual_onboarding",
            marks=pytest.mark.ignore,
        ),
    ]


def get_organization_onboarding_test_data() -> list:
    """Return parametrized organization-onboarding scenarios.

    Ignored until login OTP plus real KYC/bank verification test data
    (FEATURE_ONBOARDING_PAN, FEATURE_ONBOARDING_DOCUMENT_PATH,
    FEATURE_ONBOARDING_BANK_ACCOUNT_NUMBER, FEATURE_ONBOARDING_BANK_IFSC)
    are configured for an environment that accepts them.
    """
    return [
        pytest.param(
            "Automation Org Owner",
            "Automation Org Business",
            CERTIFICATE_TYPE_PAN,
            "incorporation_certificate",
            id="organization_onboarding_pan",
            marks=pytest.mark.ignore,
        ),
    ]
