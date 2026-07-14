"""Onboarding test data provider.

Business/profile/org names are not secrets and are embedded directly.
PAN/GSTIN, bank details, and document file paths are credential-like test
data — those are read from settings inside the test, never here.
"""

import uuid

import pytest

from src.page_objects.document_upload_po import CERTIFICATE_TYPE_PAN


def _random_label(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def get_individual_onboarding_test_data() -> list:
    """Return parametrized individual-onboarding scenarios."""
    return [
        pytest.param(
            _random_label("Auto User"),
            _random_label("Auto Biz"),
            id="individual_onboarding",
        ),
    ]


def get_organization_onboarding_test_data() -> list:
    """Return parametrized organization-onboarding scenarios.

    Ignored until real KYC/bank verification test data
    (FEATURE_ONBOARDING_PAN, FEATURE_ONBOARDING_DOCUMENT_PATH,
    FEATURE_ONBOARDING_BANK_ACCOUNT_NUMBER, FEATURE_ONBOARDING_BANK_IFSC)
    are configured for an environment that accepts them.
    """
    return [
        pytest.param(
            _random_label("Auto Org Owner"),
            _random_label("Auto Org Biz"),
            CERTIFICATE_TYPE_PAN,
            "incorporation_certificate",
            id="organization_onboarding_pan",
            marks=pytest.mark.ignore,
        ),
    ]
