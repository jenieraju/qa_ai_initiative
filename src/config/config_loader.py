"""Single source of truth for environment config. Nothing else reads config.yaml directly."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config" / "config.yaml"

# 1) Load .env (sets COFEE_ENV=dev|stg)
load_dotenv(_PROJECT_ROOT / ".env")

# 2) Load the env-specific file (.env.dev or .env.stg) for USER_PHONE/USER_OTP/etc.
_env_name = os.environ.get("COFEE_ENV", "dev").strip().lower()
load_dotenv(_PROJECT_ROOT / f".env.{_env_name}")


def _load() -> dict:
    with open(_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_env_config(env_name: str | None = None) -> dict:
    """Return {"base_url": ..., "timeout": ...} for the given env (default: COFEE_ENV, else 'dev')."""
    env_name = (env_name or os.environ.get("COFEE_ENV", "dev")).strip().lower()
    envs = _load()["environments"]
    if env_name not in envs:
        raise ValueError(f"Unknown environment '{env_name}'. Must be one of: {list(envs.keys())}")
    return envs[env_name]


def get_viewport(name: str = "desktop") -> dict:
    """Return {"width": ..., "height": ...} for the named viewport."""
    viewports = _load()["viewports"]
    if name not in viewports:
        raise ValueError(f"Unknown viewport '{name}'. Must be one of: {list(viewports.keys())}")
    return viewports[name]
