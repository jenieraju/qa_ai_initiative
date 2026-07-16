"""Pytest configuration, fixtures, and hooks."""

import contextlib
import platform
import sys
import tomllib
from datetime import datetime
from importlib import metadata
from pathlib import Path

import pytest
from playwright.sync_api import Page

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
TESTS_ROOT = REPO_ROOT / "tests"
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from src.core.failure_artifacts import capture_failure_artifacts  # noqa: E402
from src.core.report_urls import print_report_urls  # noqa: E402
from src.core.session_state import session_state  # noqa: E402
from src.core.settings import get_settings, resolve_env_name  # noqa: E402
from src.core.teardown import teardown_registry  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "output"
ALLURE_RESULTS_DIR = OUTPUT_DIR / "allure-results"
LOGS_DIR = OUTPUT_DIR / "logs"


def _resolve_allure_results_dir(config) -> Path:
    """Use pytest's --alluredir when set (per-file runs), else the default."""
    for attr in ("allure_report_dir", "alluredir"):
        value = getattr(config.option, attr, None)
        if value:
            return Path(value)
    with contextlib.suppress(ValueError):
        value = config.getoption("--alluredir")
        if value:
            return Path(value)
    return ALLURE_RESULTS_DIR

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
    parser.addoption(
        "--open-allure",
        action="store",
        default="true",
        help="Open Allure report in browser after the run: true|false (default true)",
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
        ("onboarding", "New user onboarding flow"),
        ("groups", "Group creation and management flows"),
        ("unit", "Fast unit tests for core framework utilities (no browser)"),
        ("ignore", "Excluded from default test runs"),
        ("auth_profile", "Load Playwright storage state from .auth/{name}.json"),
        ("xdist_group", "Group tests for pytest-xdist loadgroup distribution"),
    ]
    for name, description in markers:
        config.addinivalue_line("markers", f"{name}: {description}")


def pytest_sessionstart(session) -> None:
    """Bootstrap report output dirs and write Allure environment metadata.

    Runs after pytest_configure (so --clean-alluredir has already cleaned
    the active allure results dir) and once per process, including each xdist worker.
    """
    allure_dir = _resolve_allure_results_dir(session.config)
    for directory in (OUTPUT_DIR, allure_dir, LOGS_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    _write_allure_environment(allure_dir)


def _write_allure_environment(allure_dir: Path = ALLURE_RESULTS_DIR) -> None:
    settings = get_settings()
    framework_name, framework_version = _read_framework_version()
    properties = {
        "Environment": settings.app_env,
        "Base.URL": settings.base_url,
        "Browser": settings.target_browser,
        "Headless": settings.headless,
        "OS": platform.platform(),
        "Python.Version": platform.python_version(),
        "Playwright.Version": metadata.version("playwright"),
        "Pytest.Version": metadata.version("pytest"),
        "Framework": f"{framework_name} {framework_version}",
        "Execution.Timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    lines = [f"{key}={value}" for key, value in properties.items()]
    (allure_dir / "environment.properties").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def _read_framework_version() -> tuple[str, str]:
    try:
        with (REPO_ROOT / "pyproject.toml").open("rb") as pyproject_file:
            project = tomllib.load(pyproject_file)["project"]
        return project["name"], project["version"]
    except Exception:
        return "unknown", "0.0.0"


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
def _run_data_teardown():
    """Clean up any data a test registered with teardown_registry, pass or fail."""
    teardown_registry.clear()
    yield
    teardown_registry.run_all()


@pytest.fixture(autouse=True)
def _track_active_page(request) -> None:
    # @pytest.mark.unit tests are pure Python (e.g. core utility tests) and
    # must not force a browser launch — skip requesting `page` for them.
    if request.node.get_closest_marker("unit") is None:
        _register_active_page(request.getfixturevalue("page"))
    yield


def _register_active_page(page: Page) -> None:
    _active_pages.append(page)
    page._console_logs = []  # attached here for failure-artifact capture below
    page.on("console", lambda msg: page._console_logs.append(f"[{msg.type}] {msg.text}"))

    def on_popup(popup: Page) -> None:
        _register_active_page(popup)

    page.on("popup", on_popup)


@pytest.fixture(autouse=True)
def _apply_timeouts(request) -> None:
    if request.node.get_closest_marker("unit") is not None:
        return
    page = request.getfixturevalue("page")
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
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or report.passed:
        return

    page = _get_most_recent_page()
    if page is None:
        return

    error_message = str(report.longrepr) if report.longrepr else ""
    allure_dir = _resolve_allure_results_dir(item.config)
    output_dir = allure_dir.parent

    report.extra = getattr(report, "extra", []) + capture_failure_artifacts(
        page,
        output_dir=output_dir,
        nodeid=item.nodeid,
        error_message=error_message,
    )


def _get_most_recent_page() -> Page | None:
    for page in reversed(_active_pages):
        try:
            if not page.is_closed():
                return page
        except Exception:
            continue
    return None


def pytest_sessionfinish(session, exitstatus) -> None:
    """Generate Allure HTML, print report URLs, and optionally open Allure in the browser."""
    # xdist workers finish separately; only the controller/main process should open the report.
    if hasattr(session.config, "workerinput"):
        return

    config = session.config
    allure_dir = _resolve_allure_results_dir(config)

    html_report = getattr(config.option, "htmlpath", None)
    junit_report = getattr(config.option, "xmlpath", None)
    log_file = getattr(config.option, "log_file", None) or config.getini("log_file")

    allure_report = allure_dir.parent / "allure-report"
    if allure_report.name != "allure-report":
        allure_report = OUTPUT_DIR / "allure-report"

    from src.core.report_urls import generate_allure_report, open_allure_report  # noqa: E402

    generated = generate_allure_report(allure_dir, allure_report)

    print_report_urls(
        html_report=Path(html_report) if html_report else OUTPUT_DIR / "report.html",
        junit_report=Path(junit_report) if junit_report else OUTPUT_DIR / "junit-results.xml",
        allure_results=allure_dir,
        allure_report=allure_report if (allure_report / "index.html").exists() else None,
        execution_log=Path(log_file) if log_file else LOGS_DIR / "execution.log",
        title="Test reports",
    )

    open_flag = str(config.getoption("--open-allure")).strip().lower()
    should_open = open_flag in {"1", "true", "yes", "on"}
    if should_open and generated:
        open_allure_report(allure_report)
