"""Assertion utilities wrapped in Allure steps."""

import re

import allure
from playwright.sync_api import Locator, expect


@allure.step("Assert equals: {label}")
def assert_equals(actual, expected, label: str = "value") -> None:
    assert actual == expected, f"{label}: expected '{expected}', got '{actual}'"


@allure.step("Assert contains: {label}")
def assert_contains(container, item, label: str = "container") -> None:
    assert item in container, f"{label}: expected '{item}' in '{container}'"


@allure.step("Assert element visible")
def assert_element_visible(locator: Locator, *, timeout: int | None = None) -> None:
    expect(locator).to_be_visible(timeout=timeout)


@allure.step("Assert element hidden")
def assert_element_hidden(locator: Locator, *, timeout: int | None = None) -> None:
    expect(locator).to_be_hidden(timeout=timeout)


@allure.step("Assert element enabled")
def assert_element_enabled(locator: Locator, *, timeout: int | None = None) -> None:
    expect(locator).to_be_enabled(timeout=timeout)


@allure.step("Assert element has text: {expected_text}")
def assert_element_has_text(
    locator: Locator, expected_text: str, *, timeout: int | None = None
) -> None:
    expect(locator).to_have_text(expected_text, timeout=timeout)


@allure.step("Assert URL contains: {expected_fragment}")
def assert_url_contains(page, expected_fragment: str, *, timeout: int | None = None) -> None:
    """Web-first: waits/retries for navigation instead of checking page.url once."""
    expect(page).to_have_url(re.compile(re.escape(expected_fragment)), timeout=timeout)


@allure.step("Assert page title: {expected_title}")
def assert_page_title(page, expected_title: str, *, timeout: int | None = None) -> None:
    expect(page).to_have_title(expected_title, timeout=timeout)


@allure.step("Assert true: {label}")
def assert_true(condition: bool, label: str = "condition") -> None:
    assert condition, f"{label} was expected to be True"
