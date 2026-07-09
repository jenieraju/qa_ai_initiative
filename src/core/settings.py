"""Pydantic-based application settings with environment resolution."""

from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]

# Maps CLI aliases (e.g. uat1) to canonical env file names (e.g. uat01).
ENV_NAME_ALIASES: dict[str, str] = {
    "dev": "dev",
    "stg": "stg",
    "staging": "stg",
    "uat": "uat",
    "uat1": "uat01",
    "uat01": "uat01",
    "prod": "prod",
    "production": "prod",
}

# Derive URLs from resolved env name — never hardcode hosts elsewhere.
ENV_URL_MAP: dict[str, dict[str, str]] = {
    "dev": {
        "base_url": "https://dev.example.com",
        "api_base_url": "https://api-dev.example.com",
        "admin_portal_url": "https://admin-dev.example.com",
    },
    "stg": {
        "base_url": "https://stg.example.com",
        "api_base_url": "https://api-stg.example.com",
        "admin_portal_url": "https://admin-stg.example.com",
    },
    "uat01": {
        "base_url": "https://uat01.example.com",
        "api_base_url": "https://api-uat01.example.com",
        "admin_portal_url": "https://admin-uat01.example.com",
    },
    "prod": {
        "base_url": "https://www.example.com",
        "api_base_url": "https://api.example.com",
        "admin_portal_url": "https://admin.example.com",
    },
}


def resolve_env_name(raw_env: str | None = None) -> str:
    """Resolve CLI/env alias to a canonical environment name."""
    env = (raw_env or "dev").strip().lower()
    return ENV_NAME_ALIASES.get(env, env)


def load_environment_files(env_name: str) -> None:
    """Load .env then environment-specific overrides."""
    load_dotenv(REPO_ROOT / ".env", override=False)
    env_file = REPO_ROOT / f".env.{env_name}"
    if env_file.exists():
        load_dotenv(env_file, override=True)
    properties_file = REPO_ROOT / "environment" / f"{env_name}.properties"
    if properties_file.exists():
        load_dotenv(properties_file, override=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="dev", alias="APP_ENV")
    app_name: str = Field(default="APP_NAME", alias="APP_NAME")

    base_url: str = Field(default="", alias="BASE_URL")
    api_base_url: str = Field(default="", alias="API_BASE_URL")
    admin_portal_url: str = Field(default="", alias="ADMIN_PORTAL_URL")

    default_timeout_ms: int = Field(default=30_000, alias="DEFAULT_TIMEOUT_MS")
    navigation_timeout_ms: int = Field(default=60_000, alias="NAVIGATION_TIMEOUT_MS")

    credentials_encryption_key: str = Field(default="", alias="CREDENTIALS_ENCRYPTION_KEY")

    # Login is mobile number + OTP (src/features/authentication/pages/login).
    # Optional FEATURE_* vars with fallback chain for shared mobile/OTP reuse.
    feature_login_mobile_number: str = Field(default="", alias="FEATURE_LOGIN_MOBILE_NUMBER")
    feature_login_otp: str = Field(default="", alias="FEATURE_LOGIN_OTP")

    # Fallback to a shared suite when feature-specific vars are absent.
    shared_mobile_number: str = Field(default="", alias="SHARED_MOBILE_NUMBER")
    shared_otp: str = Field(default="", alias="SHARED_OTP")

    # Onboarding — organization path KYC/bank verification (see AUTH.DOCUMENT_UPLOAD,
    # AUTH.SELECT_PAYMENT in the app repo's routes.tsx). No shared fallback: these are
    # onboarding-specific test data, not reused by other features.
    feature_onboarding_pan: str = Field(default="", alias="FEATURE_ONBOARDING_PAN")
    feature_onboarding_gstin: str = Field(default="", alias="FEATURE_ONBOARDING_GSTIN")
    feature_onboarding_document_path: str = Field(
        default="", alias="FEATURE_ONBOARDING_DOCUMENT_PATH"
    )
    feature_onboarding_bank_account_number: str = Field(
        default="", alias="FEATURE_ONBOARDING_BANK_ACCOUNT_NUMBER"
    )
    feature_onboarding_bank_ifsc: str = Field(default="", alias="FEATURE_ONBOARDING_BANK_IFSC")

    target_browser: str = Field(default="chromium", alias="TARGET_BROWSER")
    headless: bool = Field(default=True, alias="HEADLESS")
    record_video: bool = Field(default=False, alias="RECORD_VIDEO")

    @field_validator("headless", "record_video", mode="before")
    @classmethod
    def parse_bool(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    @property
    def login_mobile_number(self) -> str:
        return self.feature_login_mobile_number or self.shared_mobile_number

    @property
    def login_otp(self) -> str:
        return self.feature_login_otp or self.shared_otp


def _apply_url_map(settings: Settings, env_name: str) -> Settings:
    """Fill URL fields from ENV_URL_MAP when not explicitly set in env files."""
    url_defaults = ENV_URL_MAP.get(env_name, {})
    updates: dict[str, str] = {}
    if not settings.base_url and url_defaults.get("base_url"):
        updates["base_url"] = url_defaults["base_url"]
    if not settings.api_base_url and url_defaults.get("api_base_url"):
        updates["api_base_url"] = url_defaults["api_base_url"]
    if not settings.admin_portal_url and url_defaults.get("admin_portal_url"):
        updates["admin_portal_url"] = url_defaults["admin_portal_url"]
    if updates:
        return settings.model_copy(update=updates)
    return settings


def _validate_required(settings: Settings) -> None:
    """Fail fast at import/collection time when required vars are missing."""
    missing: list[str] = []
    if not settings.base_url:
        missing.append("BASE_URL")
    if not settings.api_base_url:
        missing.append("API_BASE_URL")
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Set them in .env / .env.<env> or update ENV_URL_MAP in settings.py."
        )


@lru_cache
def get_settings(env_override: str | None = None) -> Settings:
    """Return cached settings; never instantiate Settings directly elsewhere."""
    env_name = resolve_env_name(env_override or None)
    load_environment_files(env_name)
    settings = Settings(app_env=env_name)
    settings = _apply_url_map(settings, env_name)
    _validate_required(settings)
    return settings
