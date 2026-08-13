"""Single chokepoint for UI assertions + explicit waits. Never a bare assert or fixed sleep."""

from playwright.sync_api import Locator, expect


def assert_visible(locator: Locator, timeout: int | None = None) -> None:
    expect(locator).to_be_visible(timeout=timeout)


def assert_hidden(locator: Locator, timeout: int | None = None) -> None:
    expect(locator).to_be_hidden(timeout=timeout)


def assert_text(locator: Locator, expected: str, timeout: int | None = None) -> None:
    expect(locator).to_have_text(expected, timeout=timeout)


def assert_contains_text(locator: Locator, expected: str, timeout: int | None = None) -> None:
    expect(locator).to_contain_text(expected, timeout=timeout)


def assert_url(page, expected: str, timeout: int | None = None) -> None:
    expect(page).to_have_url(expected, timeout=timeout)


def assert_enabled(locator: Locator, timeout: int | None = None) -> None:
    expect(locator).to_be_enabled(timeout=timeout)


def assert_disabled(locator: Locator, timeout: int | None = None) -> None:
    expect(locator).to_be_disabled(timeout=timeout)


def wait_for_clickable(locator: Locator, timeout: int | None = None) -> None:
    """Distinct from visibility - use before any .click(), never visibility alone."""
    expect(locator).to_be_visible(timeout=timeout)
    expect(locator).to_be_enabled(timeout=timeout)
