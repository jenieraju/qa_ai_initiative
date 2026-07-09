"""Structured user credential helpers — decrypt at runtime via config key."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    """Represents a test user profile."""

    email: str
    password: str
    org_id: str = ""
    display_name: str = ""


def get_default_login_user() -> UserCredentials:
    """Return login credentials from settings (never hardcode secrets here)."""
    from src.core.settings import get_settings

    settings = get_settings()
    return UserCredentials(
        email=settings.login_user_email,
        password=settings.login_user_password,
        org_id=settings.login_org_id,
    )
