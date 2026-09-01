"""Generates the four POM layers + dataprovider + test file for a new feature.

Backs the scaffold-feature-automation skill and the `invoke scaffold-feature`
task. Replaces freehand file authoring: the skill was previously a template
an LLM/human re-typed by hand each time, so naming/prefix/marker-registration
mistakes were easy to make silently. This script stamps out the same
skeleton mechanically and is idempotent — it refuses to overwrite a file that
already exists rather than guessing whether it's safe to replace.

Mirrors the shape of src/page_actions/login_actions.py (the skill's own
reference example): inline goto path, a verify_*_page_visible() screen-level
assertion via assert_helper. Only produces skeletons — locators and the
SECTION_TITLE_* constant are left as TODO placeholders, to be filled in from
discover-locators-from-ui's locator map. This script never invents selectors.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ScaffoldPlan:
    slug: str
    marker: str
    route: str
    area: str
    priority: str

    @property
    def class_prefix(self) -> str:
        return "".join(part.capitalize() for part in self.slug.split("_"))


def _validate_slug(slug: str) -> str:
    normalized = slug.strip().lower().replace("-", "_")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", normalized):
        raise ValueError(
            f"Invalid feature slug {slug!r} — use lowercase snake_case, e.g. 'checkout'."
        )
    return normalized


def _validate_priority(priority: str) -> str:
    priority = priority.strip().lower()
    if priority not in {"p0", "p1", "p2"}:
        raise ValueError(f"Invalid priority {priority!r} — must be p0, p1, or p2.")
    return priority


def build_plan(
    slug: str, route: str, priority: str, marker: str | None, area: str | None
) -> ScaffoldPlan:
    normalized_slug = _validate_slug(slug)
    return ScaffoldPlan(
        slug=normalized_slug,
        marker=_validate_slug(marker or normalized_slug),
        route=route if route.startswith("/") else f"/{route}",
        area=_validate_slug(area or normalized_slug),
        priority=_validate_priority(priority),
    )


def _write_if_absent(path: Path, content: str, created: list[Path], skipped: list[Path]) -> None:
    if path.exists():
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(path)


def _page_object_template(plan: ScaffoldPlan) -> str:
    return f'''"""{plan.class_prefix} page object — locators only."""

from src.core.base_page import BasePage


class {plan.class_prefix}Page(BasePage):
    """Page object for the {plan.route} screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators ---
        # TODO(discover-locators-from-ui): replace with real locators —
        # never invent selectors. Follow the btn_/input_/chk_/ddl_/msg_/lbl_
        # naming convention from AGENTS.md.
        # self.lbl_section_title = self.get_by_data_test_id("...")
'''


def _page_actions_template(plan: ScaffoldPlan) -> str:
    section_title_const = f"SECTION_TITLE_{plan.marker.upper()}"
    return f'''"""{plan.class_prefix} page actions — business logic and interactions."""

from playwright.sync_api import Page

from src.core.page_actions import PageActions
from src.page_objects.{plan.slug}_po import {plan.class_prefix}Page

# TODO(scaffold-feature-automation): add {section_title_const} to
# src/constants/messages.py, then uncomment the import and verify_ body below.
# from src.constants.messages import {section_title_const}
# from src.core.assert_helper import assert_element_has_text


class {plan.class_prefix}PageActions(PageActions):
    """Actions for the {plan.route} screen."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.po = {plan.class_prefix}Page(page)

    def navigate_to_{plan.slug}_page(self) -> None:
        self.po.goto("{plan.route}")

    def verify_{plan.slug}_page_visible(self) -> None:
        # TODO: self.wait_for_element_visible(self.po.lbl_section_title)
        # TODO: assert_element_has_text(self.po.lbl_section_title, {section_title_const})
        raise NotImplementedError("Fill in once locators are confirmed.")
'''


def _steps_template(plan: ScaffoldPlan) -> str:
    return f'''"""Reusable {plan.slug} steps decorated with Allure."""

import allure
from playwright.sync_api import Page

from src.page_actions.{plan.slug}_actions import {plan.class_prefix}PageActions


@allure.step("User navigates to {plan.slug} page")
def user_navigates_to_{plan.slug}_page(page: Page) -> None:
    {plan.class_prefix}PageActions(page).navigate_to_{plan.slug}_page()


@allure.step("User verifies {plan.slug} page is displayed")
def user_verifies_{plan.slug}_page_is_displayed(page: Page) -> None:
    {plan.class_prefix}PageActions(page).verify_{plan.slug}_page_visible()
'''


def _dataprovider_template(plan: ScaffoldPlan) -> str:
    return f'''"""{plan.class_prefix} test data provider."""

import pytest


def get_{plan.slug}_test_data() -> list:
    """Return parametrized {plan.slug} scenarios.

    Scenario keys only — no secrets, no env-entity names (see
    create-dataprovider skill). Read real values from get_settings() at
    runtime inside the test body.
    """
    return [
        pytest.param(
            "TODO_scenario",
            id="TODO_case_id",
        ),
    ]
'''


def _test_template(plan: ScaffoldPlan) -> str:
    return f'''"""End-to-end {plan.slug} tests.

TODO: describe the live flow under test and session-reuse strategy before
removing @pytest.mark.ignore.
"""

import allure
import pytest

from dataprovider.dp_{plan.slug} import get_{plan.slug}_test_data
from src.steps.{plan.slug}_steps import (
    user_navigates_to_{plan.slug}_page,
    user_verifies_{plan.slug}_page_is_displayed,
)

pytestmark = [
    pytest.mark.ignore,  # remove once locators/flow are confirmed
]


@allure.epic("TODO")
@allure.suite("TODO")
@allure.feature("{plan.class_prefix}")
class Test{plan.class_prefix}:
    """TODO: describe this test class."""

    @pytest.mark.e2e
    @pytest.mark.{plan.marker}
    @pytest.mark.{plan.priority}
    @allure.story("TODO-TC-ID")
    @pytest.mark.parametrize("scenario", get_{plan.slug}_test_data())
    def test_{plan.slug}(self, page, scenario):
        allure.dynamic.title(f"{plan.class_prefix}: {{scenario}}")
        user_navigates_to_{plan.slug}_page(page)
        user_verifies_{plan.slug}_page_is_displayed(page)
'''


def _register_marker(plan: ScaffoldPlan) -> bool:
    """Add the feature marker to pytest.ini if it isn't already registered."""
    pytest_ini = REPO_ROOT / "pytest.ini"
    text = pytest_ini.read_text(encoding="utf-8")
    if re.search(rf"^\s+{re.escape(plan.marker)}:", text, re.MULTILINE):
        return False
    marker_line = f"    {plan.marker}: {plan.class_prefix} flows\n"
    updated = text.replace(
        "    xdist_group(name): Group tests for pytest-xdist loadgroup distribution\n",
        f"    xdist_group(name): Group tests for pytest-xdist loadgroup distribution\n{marker_line}",
    )
    pytest_ini.write_text(updated, encoding="utf-8")
    return True


def scaffold_feature(
    slug: str,
    route: str,
    priority: str = "p2",
    marker: str | None = None,
    area: str | None = None,
) -> dict[str, list[Path]]:
    """Create the four-layer skeleton + dataprovider + test for one feature.

    Returns {"created": [...], "skipped": [...]} — skipped files already
    existed and were left untouched.
    """
    plan = build_plan(slug, route, priority, marker, area)
    created: list[Path] = []
    skipped: list[Path] = []

    _write_if_absent(
        REPO_ROOT / "src" / "page_objects" / f"{plan.slug}_po.py",
        _page_object_template(plan),
        created,
        skipped,
    )
    _write_if_absent(
        REPO_ROOT / "src" / "page_actions" / f"{plan.slug}_actions.py",
        _page_actions_template(plan),
        created,
        skipped,
    )
    _write_if_absent(
        REPO_ROOT / "src" / "steps" / f"{plan.slug}_steps.py",
        _steps_template(plan),
        created,
        skipped,
    )
    _write_if_absent(
        REPO_ROOT / "tests" / "dataprovider" / f"dp_{plan.slug}.py",
        _dataprovider_template(plan),
        created,
        skipped,
    )
    _write_if_absent(
        REPO_ROOT / "tests" / "test" / plan.area / f"test_{plan.slug}.py",
        _test_template(plan),
        created,
        skipped,
    )

    if _register_marker(plan):
        created.append(REPO_ROOT / "pytest.ini")

    return {"created": created, "skipped": skipped}
