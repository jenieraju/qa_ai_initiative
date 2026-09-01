"""Unit test: every pytest feature marker has a matching context_docs/<slug>.md file.

Smoke test — catches markers registered without a living feature record.
Alias map mirrors context_docs/README.md (login/onboarding share one doc).
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTEXT_DOCS_DIR = REPO_ROOT / "context_docs"

NON_FEATURE_MARKERS = {"e2e", "p0", "p1", "p2", "unit", "ignore", "auth_profile", "xdist_group"}

# marker → context_docs filename (when not {marker}.md)
MARKER_TO_CONTEXT_DOC: dict[str, str] = {
    "login": "authentication-onboarding.md",
    "onboarding": "authentication-onboarding.md",
    "quick_collect": "quick-collect.md",
}

pytestmark = pytest.mark.unit


def _registered_feature_markers() -> set[str]:
    pytest_ini = (REPO_ROOT / "pytest.ini").read_text(encoding="utf-8")
    markers_block = pytest_ini.split("markers =")[1]
    names = re.findall(r"^\s+(\w+)(?:\(.*?\))?:", markers_block, re.MULTILINE)
    return {name for name in names if name not in NON_FEATURE_MARKERS}


def _expected_context_doc(marker: str) -> Path:
    filename = MARKER_TO_CONTEXT_DOC.get(marker, f"{marker}.md")
    return CONTEXT_DOCS_DIR / filename


class TestContextDocsSync:
    """Every feature marker needs a context_docs file."""

    def test_every_feature_marker_has_context_doc(self):
        missing = []
        for marker in sorted(_registered_feature_markers()):
            path = _expected_context_doc(marker)
            if not path.is_file():
                missing.append(f"{marker} → {path.name}")

        assert not missing, (
            f"No context_docs file for: {missing}. "
            "Run get-context and add Detail: link in APP_CONTEXT.md."
        )
