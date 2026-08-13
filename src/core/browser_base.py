"""Single chokepoint for browser/context launch. Every test goes through here, never a one-off launch."""

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.config.config_loader import get_env_config, get_viewport


def launch_browser(browser_name: str = "chromium", headless: bool = True) -> tuple:
    """Returns (playwright, browser) - caller owns lifecycle (stop playwright, close browser)."""
    playwright = sync_playwright().start()
    browser: Browser = getattr(playwright, browser_name).launch(headless=headless)
    return playwright, browser


def new_context(browser: Browser, env_name: str | None = None, viewport_name: str = "desktop",
                 storage_state: str | None = None) -> BrowserContext:
    """New browser context, pre-configured with viewport + base URL awareness (via env config)."""
    env = get_env_config(env_name)
    viewport = get_viewport(viewport_name)
    context = browser.new_context(
        viewport=viewport,
        storage_state=storage_state,
    )
    context.set_default_timeout(env["timeout"])
    return context


def new_page(context: BrowserContext) -> Page:
    return context.new_page()
