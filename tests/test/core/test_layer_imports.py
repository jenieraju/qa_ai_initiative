"""Unit test: E2E test files must not import page_actions or page_objects directly.

Smoke test for the Tests → Steps → Actions → Page Objects rule (AGENTS.md).
Steps and conftest may import lower layers; tests/test/**/test_*.py may not.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_ROOT = REPO_ROOT / "tests" / "test"

FORBIDDEN_IMPORT = re.compile(
    r"^\s*(?:from\s+src\.page_(?:actions|objects)|import\s+src\.page_(?:actions|objects))"
)

pytestmark = pytest.mark.unit


class TestLayerImports:
    """E2E test modules call Steps only — not Actions or Page Objects."""

    def test_e2e_tests_do_not_import_page_actions_or_objects(self):
        violations: list[str] = []
        for test_file in TEST_ROOT.rglob("test_*.py"):
            if (test_file.parent / "core").name == "core" or "core" in test_file.parts:
                continue
            for line_no, line in enumerate(
                test_file.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if FORBIDDEN_IMPORT.search(line):
                    rel = test_file.relative_to(REPO_ROOT)
                    violations.append(f"{rel}:{line_no}: {line.strip()}")

        assert (
            not violations
        ), "Tests must call Steps only — move imports to src/steps/:\n" + "\n".join(violations)
