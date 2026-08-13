import pytest

from src.core.browser_base import new_context, new_page
from src.helpers.auth_setup import ensure_logged_in_storage_state


@pytest.fixture
def authenticated_page(browser):
    """Page with a cached, logged-in session (see context/ui-auth.md)."""
    context = new_context(browser)
    storage_state_path = ensure_logged_in_storage_state(context)
    context.close()

    authed_context = new_context(browser, storage_state=storage_state_path)
    page = new_page(authed_context)
    yield page
    authed_context.close()


@pytest.fixture
def unauthenticated_page(browser):
    """Page with no session at all - for auth-session redirect tests."""
    context = new_context(browser)
    page = new_page(context)
    yield page
    context.close()
