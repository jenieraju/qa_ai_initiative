"""Group creation test data provider."""

import uuid

import pytest


def _random_label(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def get_group_create_test_data() -> list:
    """Return parametrized group-creation scenarios."""
    return [
        pytest.param(
            _random_label("Auto Group"),
            "100",
            id="create_group_monthly_basic",
        ),
    ]
