"""Pydantic-based application settings with environment resolution."""

import os
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
    "uat": "uat01",
    "uat1": "uat01",
    "uat01": "uat01",
    "prod": "prod",
    "production": "prod",
}

# Known environment names. Only envs with confirmed hosts get a URL default;
# the rest must supply BASE_URL / API_BASE_URL from .env.<env> or they fail
# validation — a placeholder default would silently point a run at the wrong host.
KNOWN_ENV_NAMES: frozenset[str] = frozenset({"dev", "stg", "uat01", "prod"})

# Derive URLs from resolved env name — never hardcode hosts elsewhere.
ENV_URL_MAP: dict[str, dict[str, str]] = {
    "dev": {
        "base_url": "https://web.dev.cofee.life",
        "api_base_url": "https://api.dev.cofee.life",
        "admin_portal_url": "",
    },
}


def resolve_env_name(raw_env: str | None = None) -> str:
    """Resolve a CLI value, else APP_ENV from .env, else 'dev' — to a canonical name."""
    if not raw_env:
        # .env is the documented place to pin a default env; read it before falling back.
        load_dotenv(REPO_ROOT / ".env", override=False)
        raw_env = os.environ.get("APP_ENV")
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

    # Bearer token for API-only precondition/cleanup calls against api_base_url.
    # Optional: empty unless the target env issues a static automation token.
    api_token: str = Field(default="", alias="API_TOKEN")

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

    # Quick Collect needs an existing member to act as the payer. The members
    # list is org data, not a fixture, so the name comes from the env file
    # rather than being hardcoded or guessed from "whichever row is first".
    feature_quick_collect_payer_name: str = Field(
        default="", alias="FEATURE_QUICK_COLLECT_PAYER_NAME"
    )

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


def _validate_required(settings: Settings, env_name: str) -> None:
    """Fail fast at import/collection time when required vars are missing."""
    if env_name not in KNOWN_ENV_NAMES:
        raise ValueError(
            f"Unknown environment '{env_name}'. Known environments: "
            f"{', '.join(sorted(KNOWN_ENV_NAMES))} (aliases in ENV_NAME_ALIASES)."
        )
    missing = [
        name
        for name, value in (
            ("BASE_URL", settings.base_url),
            ("API_BASE_URL", settings.api_base_url),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            f"Missing required environment variables for env '{env_name}': "
            f"{', '.join(missing)}. Set them in .env.{env_name} (copy "
            f".env.{env_name}.example) or add the env to ENV_URL_MAP in settings.py."
        )


@lru_cache
def _build_settings(env_name: str) -> Settings:
    """Build and validate settings for one canonical env name (cached per env)."""
    load_environment_files(env_name)
    settings = Settings(app_env=env_name)
    settings = _apply_url_map(settings, env_name)
    _validate_required(settings, env_name)
    return settings


def get_settings(env_override: str | None = None) -> Settings:
    """Return the cached settings for the target env; never instantiate Settings directly.

    Cached on the *resolved* env name, so `get_settings()`, `get_settings("dev")`
    and `get_settings("DEV")` all return the same object. Runtime overrides
    applied in conftest (headless, browser, video) must be visible to every
    call site, which only holds if there is exactly one instance per env.
    """
    return _build_settings(resolve_env_name(env_override or None))
