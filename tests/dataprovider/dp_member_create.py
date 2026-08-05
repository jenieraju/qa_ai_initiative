"""Member creation test data provider."""

import uuid

import pytest


def _random_label(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def _random_mobile_number() -> str:
    """Unique 10-digit sandbox mobile so runs don't collide on a uniqueness rule."""
    return f"97{uuid.uuid4().int % 10**8:08d}"


def get_member_create_test_data() -> list:
    """Return parametrized member-creation scenarios."""
    return [
        pytest.param(
            _random_label("Auto Member"),
            _random_mobile_number(),
            id="create_member_basic_details",
        ),
    ]
