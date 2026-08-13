"""One-time login -> cached storageState, per context/ui-auth.md's reuse recommendation."""

import os
from pathlib import Path

from playwright.sync_api import BrowserContext

from src.config.config_loader import get_env_config
from src.pages.login_page import LoginPage

_STORAGE_STATE_PATH = Path(__file__).resolve().parent.parent.parent / "auth" / "storage_state.json"


def ensure_logged_in_storage_state(context: BrowserContext) -> str:
    """Return the storage_state file path, performing a real login first if it doesn't exist yet."""
    if _STORAGE_STATE_PATH.exists():
        return str(_STORAGE_STATE_PATH)

    env = get_env_config()
    page = context.new_page()
    login = LoginPage(page, env["base_url"])
    login.goto_login()
    login.fill_mobile_and_continue(os.environ["USER_PHONE"])
    login.fill_otp_and_continue(os.environ["USER_OTP"])  # raises NotImplementedError today
    context.storage_state(path=str(_STORAGE_STATE_PATH))
    page.close()
    return str(_STORAGE_STATE_PATH)
