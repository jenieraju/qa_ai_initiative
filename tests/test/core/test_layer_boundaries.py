"""Unit tests enforcing the four-layer architecture AGENTS.md mandates.

    Tests → Steps → Actions → Page Objects

The rule was documentation-only until now, which meant a violation was caught
only if a reviewer happened to notice it. These are static text checks over the
source tree — no browser, no imports of the modules under test.

Deliberately narrow: they catch the boundary crossings that actually happen
(a raw locator outside a page object, a layer reaching two levels down). They
cannot judge whether a step is a sensible user workflow — that still needs review.
"""

import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
PAGE_OBJECTS_DIR = REPO_ROOT / "src" / "page_objects"
PAGE_ACTIONS_DIR = REPO_ROOT / "src" / "page_actions"
STEPS_DIR = REPO_ROOT / "src" / "steps"
TESTS_DIR = REPO_ROOT / "tests" / "test"
CORE_DIR = REPO_ROOT / "src" / "core"

# page.locator(...) / page.get_by_role(...) and friends — locator construction.
LOCATOR_CALL = re.compile(r"\bpage\.(locator|get_by_\w+|frame_locator)\s*\(")

# BasePage is the sanctioned wrapper page objects build their locators from —
# it is the one place outside src/page_objects/ allowed to touch the Page API.
LOCATOR_EXEMPT = {CORE_DIR / "base_page.py", Path(__file__).resolve()}

# api_client.poll_until is the one sanctioned sleep: an async server-side job
# exposes no browser signal to wait on. Everywhere else must use a real wait.
SLEEP_EXEMPT = {CORE_DIR / "api_client.py", Path(__file__).resolve()}

pytestmark = pytest.mark.unit


def _python_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*.py") if path.name != "__init__.py")


def _imported_modules(path: Path) -> set[str]:
    """Dotted module names imported by a file (`from a.b import c` → `a.b`)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


class TestLocatorsStayInPageObjects:
    """`page.locator()` / `page.get_by_*()` may only appear in src/page_objects/."""

    def test_no_locator_construction_outside_page_objects(self):
        offenders: list[str] = []
        for directory in (PAGE_ACTIONS_DIR, STEPS_DIR, TESTS_DIR, CORE_DIR):
            for path in _python_files(directory):
                if path.resolve() in LOCATOR_EXEMPT:
                    continue
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if LOCATOR_CALL.search(line):
                        offenders.append(f"{_relative(path)}:{number}: {line.strip()}")

        assert not offenders, (
            "Locator construction is only allowed in src/page_objects/*_po.py "
            "(AGENTS.md → Architecture). Move these into the page object and "
            "expose them as named attributes:\n  " + "\n  ".join(offenders)
        )


class TestLayersOnlyCallTheLayerBelow:
    """Each layer imports the layer directly below it — never one further down."""

    def test_steps_do_not_import_page_objects(self):
        offenders = [
            f"{_relative(path)} imports {module}"
            for path in _python_files(STEPS_DIR)
            for module in _imported_modules(path)
            if module.startswith("src.page_objects")
        ]
        assert not offenders, (
            "Steps must go through Page Actions, never straight to a Page Object "
            "(AGENTS.md → Architecture):\n  " + "\n  ".join(offenders)
        )

    def test_tests_do_not_import_actions_or_page_objects(self):
        offenders = [
            f"{_relative(path)} imports {module}"
            for path in _python_files(TESTS_DIR)
            for module in _imported_modules(path)
            if module.startswith(("src.page_actions", "src.page_objects"))
        ]
        assert not offenders, (
            "Tests call Steps only — not Page Actions or Page Objects "
            "(AGENTS.md → Architecture):\n  " + "\n  ".join(offenders)
        )

    def test_page_objects_do_not_import_actions_or_steps(self):
        offenders = [
            f"{_relative(path)} imports {module}"
            for path in _python_files(PAGE_OBJECTS_DIR)
            for module in _imported_modules(path)
            if module.startswith(("src.page_actions", "src.steps"))
        ]
        assert not offenders, (
            "Page Objects are the bottom layer — locators only, no upward imports "
            "(AGENTS.md → Architecture):\n  " + "\n  ".join(offenders)
        )


class TestNoSleeps:
    """Explicit waits only — `sleep()` hides a missing wait and slows every run."""

    def test_no_time_sleep_or_page_wait_for_timeout(self):
        pattern = re.compile(r"\b(time\.sleep|wait_for_timeout)\s*\(")
        offenders = [
            f"{_relative(path)}:{number}: {line.strip()}"
            for directory in (PAGE_OBJECTS_DIR, PAGE_ACTIONS_DIR, STEPS_DIR, TESTS_DIR, CORE_DIR)
            for path in _python_files(directory)
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if pattern.search(line) and path.resolve() not in SLEEP_EXEMPT
        ]
        assert not offenders, (
            "Use an explicit wait or a web-first assertion instead of sleeping "
            "(AGENTS.md → Always-on rules):\n  " + "\n  ".join(offenders)
        )
