"""Structured user credential helpers — decrypt at runtime via config key."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    """Represents a test user profile — login is mobile number + OTP."""

    mobile_number: str
    otp: str
    display_name: str = ""


def get_default_login_user() -> UserCredentials:
    """Return login credentials from settings (never hardcode secrets here)."""
    from src.core.settings import get_settings

    settings = get_settings()
    return UserCredentials(
        mobile_number=settings.login_mobile_number,
        otp=settings.login_otp,
    )
