"""Unit test: context_docs Status: automated must match runnable E2E tests.

Smoke test — Status: automated requires at least one non-@ignore E2E test
with that feature marker. Status: discovery allows all tests ignored.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTEXT_DOCS_DIR = REPO_ROOT / "context_docs"
TEST_ROOT = REPO_ROOT / "tests" / "test"

# context_docs filename → pytest feature marker(s) covered by that doc
CONTEXT_DOC_TO_MARKERS: dict[str, list[str]] = {
    "authentication-onboarding.md": ["login", "onboarding"],
    "groups.md": ["groups"],
    "members.md": ["members"],
    "quick-collect.md": ["quick_collect"],
}

pytestmark = pytest.mark.unit


def _parse_status(text: str) -> str | None:
    match = re.search(r"^Status:\s*(\S+)", text, re.MULTILINE)
    return match.group(1).lower() if match else None


def _marker_has_runnable_e2e_test(marker: str) -> bool:
    """True if at least one test function with this marker is not @pytest.mark.ignore."""
    marker_pattern = re.compile(rf"@pytest\.mark\.{re.escape(marker)}\b")
    ignore_pattern = re.compile(r"@pytest\.mark\.ignore\b")

    for test_file in TEST_ROOT.rglob("test_*.py"):
        if "core" in test_file.parts:
            continue
        pending: list[str] = []
        for raw_line in test_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith("@"):
                pending.append(line)
                continue
            if line.startswith("def test_"):
                has_marker = any(marker_pattern.search(d) for d in pending)
                is_ignored = any(ignore_pattern.search(d) for d in pending)
                if has_marker and not is_ignored:
                    return True
                pending = []
            else:
                pending = []
    return False


class TestContextDocStatus:
    """Status: automated in context_docs must reflect runnable tests."""

    def test_automated_status_has_non_ignored_e2e_tests(self):
        mismatches: list[str] = []
        for doc_path in CONTEXT_DOCS_DIR.glob("*.md"):
            if doc_path.name.lower() == "readme.md":
                continue
            status = _parse_status(doc_path.read_text(encoding="utf-8"))
            if status != "automated":
                continue
            markers = CONTEXT_DOC_TO_MARKERS.get(doc_path.name, [])
            if not markers:
                continue
            if not any(_marker_has_runnable_e2e_test(m) for m in markers):
                mismatches.append(
                    f"{doc_path.name} is Status: automated but no runnable "
                    f"@pytest.mark.e2e test for marker(s) {markers}"
                )

        assert not mismatches, "\n".join(mismatches)
