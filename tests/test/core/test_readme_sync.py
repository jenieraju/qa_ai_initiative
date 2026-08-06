"""Unit test asserting README.md's "Next steps" section stays in sync with
fully-gated test functions.

Smoke test, not exhaustive: it only catches a test function directly
decorated with @pytest.mark.ignore (an entire feature path gated off) whose
feature marker isn't mentioned anywhere in README.md. It deliberately does
NOT catch ignores applied via a dataprovider's `marks=pytest.mark.ignore`
on a single parametrize row (e.g. login's invalid-mobile scenario, or
organization onboarding) — those are partial/edge-case gates, not a whole
feature path, and still rely on manual review, same as the "unconfirmed"
rows in APP_CONTEXT.md's cross-feature table.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]

NON_FEATURE_MARKERS = {
    "e2e",
    "p0",
    "p1",
    "p2",
    "ignore",
    "unit",
    "auth_profile",
    "xdist_group",
    "parametrize",
}

pytestmark = pytest.mark.unit


def _feature_markers_on_fully_ignored_tests() -> set[str]:
    """Feature markers on a test function directly decorated with @pytest.mark.ignore."""
    markers_found: set[str] = set()
    for test_file in (REPO_ROOT / "tests" / "test").rglob("test_*.py"):
        pending_decorators: list[str] = []
        for raw_line in test_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith("@"):
                pending_decorators.append(line)
                continue
            if line.startswith("def test_"):
                if any(d.startswith("@pytest.mark.ignore") for d in pending_decorators):
                    for decorator in pending_decorators:
                        match = re.match(r"@pytest\.mark\.(\w+)", decorator)
                        if match and match.group(1) not in NON_FEATURE_MARKERS:
                            markers_found.add(match.group(1))
                pending_decorators = []
            else:
                pending_decorators = []
    return markers_found


class TestReadmeSync:
    """Every fully @pytest.mark.ignore'd feature needs a mention in README.md."""

    def test_fully_ignored_features_are_mentioned_in_readme(self):
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8").lower()
        missing = [
            marker
            for marker in sorted(_feature_markers_on_fully_ignored_tests())
            if marker.lower() not in readme_text
        ]
        assert not missing, (
            f"Feature marker(s) {missing} are used on a fully @pytest.mark.ignore'd "
            f"test but aren't mentioned anywhere in README.md. Update README.md -> "
            f"'Next steps' with why it's gated and what confirms it."
        )
