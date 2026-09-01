"""Unit test enforcing the "no secrets in dataproviders" rule from AGENTS.md
and the create-dataprovider skill: credentials, OTPs, and phone numbers must
come from get_settings() at runtime, never as literals in tests/dataprovider/.

Smoke test, not an exhaustive secret scanner: it only catches the clearest,
most common shapes (email-like literals, phone-number-like literals, and
password/token/otp/secret keyword-value literals) — the same class of bug the
skill's own "BAD" example (`pytest.param("9876543210", "123456", ...)`) shows.
It cannot judge every possible literal, so this does not replace review; it
stops the obvious case from landing quietly.

No browser involved — pure text checks against tests/dataprovider source files.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
DATAPROVIDER_DIR = REPO_ROOT / "tests" / "dataprovider"

EMAIL_PATTERN = re.compile(r"[\"'][A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+[\"']")
PHONE_PATTERN = re.compile(r"[\"']\+?\d{10,}[\"']")
KEYWORD_LITERAL_PATTERN = re.compile(
    r"(?i)(password|secret|api[_-]?key|otp|token)\s*[:=]\s*[\"'][^\"']+[\"']"
)

pytestmark = pytest.mark.unit


def _violations() -> list[str]:
    violations = []
    for path in sorted(DATAPROVIDER_DIR.glob("dp_*.py")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if (
                EMAIL_PATTERN.search(line)
                or PHONE_PATTERN.search(line)
                or KEYWORD_LITERAL_PATTERN.search(line)
            ):
                violations.append(f"{path.relative_to(REPO_ROOT)}:{line_no}: {line.strip()}")
    return violations


class TestDataproviderNoSecrets:
    """dp_*.py files must hold scenario keys only — never real credentials/PII literals."""

    def test_no_secret_like_literals_in_dataproviders(self):
        violations = _violations()
        assert not violations, (
            "Secret-shaped literal(s) found in tests/dataprovider/ — use a "
            'scenario key (e.g. id="valid_admin") and read the real value '
            "from get_settings() inside the test body instead (see "
            "create-dataprovider skill's Credentials pattern):\n"
            + "\n".join(violations)
        )
