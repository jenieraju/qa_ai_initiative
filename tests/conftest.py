"""Pytest configuration, fixtures, and hooks."""

import sys
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
TESTS_ROOT = REPO_ROOT / "tests"
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from src.core.session_state import session_state  # noqa: E402
from src.core.settings import get_settings, resolve_env_name  # noqa: E402

# Track the most recently opened page/tab for failure screenshots.
_active_pages: list[Page] = []


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--env", action="store", default=None, help="Target environment: dev|stg|uat|prod"
    )
    parser.addoption(
        "--target-browser",
        action="store",
        default=None,
        help="Browser engine: chromium|firefox|webkit",
    )
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run headless: true|false",
    )
    parser.addoption(
        "--record-video",
        action="store",
        default=None,
        help="Record video: true|false",
    )


def pytest_configure(config) -> None:
    env_override = config.getoption("--env")
    resolve_env_name(env_override)
    get_settings(env_override)

    target_browser = config.getoption("--target-browser")
    if target_browser:
        config.option.browser = [target_browser]

    markers = [
        ("e2e", "End-to-end UI tests"),
        ("p0", "Priority 0 — critical path"),
        ("p1", "Priority 1 — high importance"),
        ("p2", "Priority 2 — lower priority"),
        ("login", "Login and authentication flows"),
        ("ignore", "Excluded from default test runs"),
        ("auth_profile", "Load Playwright storage state from .auth/{name}.json"),
        ("xdist_group", "Group tests for pytest-xdist loadgroup distribution"),
    ]
    for name, description in markers:
        config.addinivalue_line("markers", f"{name}: {description}")


@pytest.fixture(scope="session", autouse=True)
def _configure_settings(pytestconfig) -> None:
    env_override = pytestconfig.getoption("--env")
    settings = get_settings(env_override)

    browser_override = pytestconfig.getoption("--target-browser")
    if browser_override:
        settings.target_browser = browser_override

    headless_override = pytestconfig.getoption("--headless")
    if headless_override is not None:
        settings.headless = str(headless_override).strip().lower() in {"1", "true", "yes", "on"}

    video_override = pytestconfig.getoption("--record-video")
    if video_override is not None:
        settings.record_video = str(video_override).strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(autouse=True)
def _reset_session_state() -> None:
    session_state.clear()
    yield
    session_state.clear()


@pytest.fixture(autouse=True)
def _track_active_page(page: Page) -> None:
    _register_active_page(page)
    yield


def _register_active_page(page: Page) -> None:
    _active_pages.append(page)

    def on_popup(popup: Page) -> None:
        _register_active_page(popup)

    page.on("popup", on_popup)


@pytest.fixture(autouse=True)
def _apply_timeouts(page: Page) -> None:
    settings = get_settings()
    page.set_default_timeout(settings.default_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    settings = get_settings(pytestconfig.getoption("--env"))
    updated = dict(browser_type_launch_args)
    updated["headless"] = settings.headless
    return updated


@pytest.fixture
def browser_context_args(browser_context_args, request, pytestconfig):
    """Load storage state when @pytest.mark.auth_profile('name') is present."""
    settings = get_settings(pytestconfig.getoption("--env"))
    updated = dict(browser_context_args)

    if settings.record_video:
        updated.setdefault("record_video_dir", str(REPO_ROOT / "test-results" / "videos"))

    auth_marker = request.node.get_closest_marker("auth_profile")
    if auth_marker is None:
        return updated

    profile_name = auth_marker.args[0] if auth_marker.args else auth_marker.kwargs.get("name")
    if not profile_name:
        return updated

    auth_file = REPO_ROOT / ".auth" / f"{profile_name}.json"
    if auth_file.exists():
        updated["storage_state"] = str(auth_file)
    return updated


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    page = _get_most_recent_page()
    if page is None:
        return

    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass


def _get_most_recent_page() -> Page | None:
    for page in reversed(_active_pages):
        try:
            if not page.is_closed():
                return page
        except Exception:
            continue
    return None
