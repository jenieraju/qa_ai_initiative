# Shared fixtures for all feature tests.
# Auth fixtures (a cached storageState, e.g. auth/storage_state.json) land here once
# get-ui-auth has documented the real login flow in context/ui-auth.md - not invented
# by create-ui-framework-structure.
import pytest

from src.core.browser_base import launch_browser, new_context, new_page


@pytest.fixture(scope="session")
def browser():
    playwright, browser = launch_browser()
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def page(browser):
    context = new_context(browser)
    page = new_page(context)
    yield page
    context.close()
