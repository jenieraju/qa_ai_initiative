"""Login test data provider."""

import pytest

from src.constants.messages import MSG_INVALID_CREDENTIALS


def get_login_test_data() -> list:
    """Return parametrized login scenarios.

    Credentials are read at test runtime via fixtures — never embedded here.
    """
    return [
        pytest.param(
            "valid",
            None,
            id="valid_login_placeholder",
            marks=pytest.mark.ignore,
        ),
        pytest.param(
            "invalid",
            MSG_INVALID_CREDENTIALS,
            id="invalid_credentials",
            marks=pytest.mark.ignore,
        ),
    ]
