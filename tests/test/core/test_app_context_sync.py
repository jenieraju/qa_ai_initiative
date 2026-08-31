"""Unit test asserting APP_CONTEXT.md stays in sync with pytest.ini's feature markers.

Smoke test, not a substitute for actually reading APP_CONTEXT.md: it only
catches the class of bug this repo already had once — a brand-new feature
marker (e.g. "groups") registered in pytest.ini with zero corresponding
section in APP_CONTEXT.md. It cannot judge whether that section's content
is accurate or complete, and it does not check the "Cross-feature
relationships" table — that still needs a human/agent to actually read it.

No browser involved — pure text checks against two repo files.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]

# Framework/mechanics markers — not app features, no APP_CONTEXT.md section expected.
NON_FEATURE_MARKERS = {"e2e", "p0", "p1", "p2", "unit", "ignore", "auth_profile", "xdist_group"}

# Only add an entry here when a marker's real APP_CONTEXT.md section title
# genuinely uses different wording than the marker itself (e.g. login and
# onboarding share one "Authentication & onboarding flow" heading because
# they're the same app route). Do NOT add an entry just to make this test
# pass without a real section existing — that defeats the point of the check.
HEADING_ALIASES = {
    "login": "authentication",
    "onboarding": "onboarding",
    "groups": "groups",
    "members": "members",
    "quick_collect": "quick collect",
}

pytestmark = pytest.mark.unit


def _registered_feature_markers() -> set[str]:
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text(encoding="utf-8")
    markers_block = pytest_ini.split("markers =")[1]
    names = re.findall(r"^\s+(\w+)(?:\(.*?\))?:", markers_block, re.MULTILINE)
    return {name for name in names if name not in NON_FEATURE_MARKERS}


def _app_context_heading_text() -> str:
    app_context = (REPO_ROOT / "APP_CONTEXT.md").read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(.+)$", app_context, re.MULTILINE)
    return " ".join(headings).lower()


class TestAppContextSync:
    """Every feature marker in pytest.ini needs a matching '##' heading in APP_CONTEXT.md."""

    def test_every_feature_marker_has_a_heading(self):
        heading_text = _app_context_heading_text()
        missing = []
        for marker in sorted(_registered_feature_markers()):
            keyword = HEADING_ALIASES.get(marker, marker)
            if keyword.lower() not in heading_text:
                missing.append(marker)

        assert not missing, (
            f"Feature marker(s) {missing} are registered in pytest.ini but have "
            f"no matching '##' section in APP_CONTEXT.md (or HEADING_ALIASES "
            f"entry in this test, if the wording genuinely differs). Add a "
            f"section — see APP_CONTEXT.md -> 'Writing new tests'."
        )
