"""Unit test asserting every context_docs feature file has a Confirmed locators section.

Smoke test: scaffold-feature-automation must not run without
context_docs/<slug>.md → ## Confirmed locators. This catches new context
docs that skip the section entirely — not whether every row is verified.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTEXT_DOCS_DIR = REPO_ROOT / "context_docs"
LOCATORS_HEADING = "## Confirmed locators"

pytestmark = pytest.mark.unit


def _feature_context_docs() -> list[Path]:
    return [path for path in CONTEXT_DOCS_DIR.glob("*.md") if path.name.lower() != "readme.md"]


class TestContextDocsLocatorsSection:
    """Every feature context doc must declare a Confirmed locators section."""

    def test_every_context_doc_has_confirmed_locators_section(self):
        missing = []
        for doc in _feature_context_docs():
            text = doc.read_text(encoding="utf-8")
            if LOCATORS_HEADING not in text:
                missing.append(doc.name)

        assert not missing, (
            f"Missing '{LOCATORS_HEADING}' in: {missing}. "
            "Add the section (see get-context / discover-locators-from-ui skills)."
        )
