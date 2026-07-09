"""Login test data provider."""

import pytest

from src.constants.messages import MSG_INVALID_MOBILE_NUMBER


def get_login_test_data() -> list:
    """Return parametrized login scenarios.

    Mobile number and OTP are read from settings at test runtime — never
    embedded here. The "valid" scenario needs a mobile number + OTP pair that
    the target environment actually accepts (e.g. a fixed sandbox OTP) —
    ignored until FEATURE_LOGIN_MOBILE_NUMBER / FEATURE_LOGIN_OTP are configured.
    """
    return [
        pytest.param(
            "valid",
            None,
            id="valid_login_placeholder",
            marks=pytest.mark.ignore,
        ),
        pytest.param(
            "invalid_mobile_number",
            MSG_INVALID_MOBILE_NUMBER,
            id="invalid_mobile_number",
            marks=pytest.mark.ignore,
        ),
    ]
