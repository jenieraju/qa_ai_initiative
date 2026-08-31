"""Quick Collect test data provider.

Amount bounds (2–200000) are the app's own, read off the create-link screen's
validation copy — see context_docs/quick-collect.md. The payer's name is org
data and comes from settings (FEATURE_QUICK_COLLECT_PAYER_NAME), never from here.
"""

import pytest

from src.constants.messages import QUICK_COLLECT_AMOUNT_MAX, QUICK_COLLECT_AMOUNT_MIN


def get_quick_collect_create_test_data() -> list:
    """Happy-path amounts for creating a payment link (TC-QC-001/002)."""
    return [
        pytest.param(
            "100",
            id="TC-QC-001_create_link_for_single_payer",
        ),
    ]


def get_quick_collect_invalid_amount_test_data() -> list:
    """Amounts the form must reject (TC-QC-004/005)."""
    return [
        pytest.param(
            str(QUICK_COLLECT_AMOUNT_MIN - 1),
            id="TC-QC-004_amount_below_minimum",
        ),
        pytest.param(
            str(QUICK_COLLECT_AMOUNT_MAX + 1),
            id="TC-QC-005_amount_above_maximum",
        ),
    ]


def get_quick_collect_boundary_amount_test_data() -> list:
    """Amounts at the inclusive bounds, which must be accepted (TC-QC-006)."""
    return [
        pytest.param(
            str(QUICK_COLLECT_AMOUNT_MIN),
            id="TC-QC-006_amount_at_minimum",
        ),
        pytest.param(
            str(QUICK_COLLECT_AMOUNT_MAX),
            id="TC-QC-006_amount_at_maximum",
        ),
    ]
