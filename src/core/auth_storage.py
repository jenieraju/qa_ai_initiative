"""Playwright storage-state helpers for reusable authenticated sessions."""

from pathlib import Path

from playwright.sync_api import Page

REPO_ROOT = Path(__file__).resolve().parents[2]
AUTH_DIR = REPO_ROOT / ".auth"
DEFAULT_AUTH_PROFILE = "default"


def auth_state_path(profile_name: str = DEFAULT_AUTH_PROFILE) -> Path:
    return AUTH_DIR / f"{profile_name}.json"


def auth_state_exists(profile_name: str = DEFAULT_AUTH_PROFILE) -> bool:
    return auth_state_path(profile_name).is_file()


def save_auth_storage_state(page: Page, profile_name: str = DEFAULT_AUTH_PROFILE) -> Path:
    """Persist cookies/localStorage from the current browser context."""
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    path = auth_state_path(profile_name)
    page.context.storage_state(path=str(path))
    return path
