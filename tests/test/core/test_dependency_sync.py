"""Unit test asserting requirements.txt matches pyproject.toml's dependencies.

The two lists are installed by different entry points (`pip install -r
requirements.txt` locally, the pinned set in CI), so a version bumped in one
and not the other means CI and laptops silently run different stacks.
pyproject.toml is the source of truth; regenerate with `invoke sync-requirements`.
"""

import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]

pytestmark = pytest.mark.unit


def _pyproject_requirements() -> list[str]:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return [*project["dependencies"], *project["optional-dependencies"]["dev"]]


def _requirements_txt() -> list[str]:
    lines = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


class TestDependencySync:
    """requirements.txt is a generated mirror of pyproject.toml."""

    def test_requirements_txt_matches_pyproject(self):
        expected = _pyproject_requirements()
        actual = _requirements_txt()
        assert actual == expected, (
            "requirements.txt has drifted from pyproject.toml. pyproject.toml is "
            "the source of truth — run `invoke sync-requirements` to regenerate.\n"
            f"  only in pyproject.toml: {sorted(set(expected) - set(actual))}\n"
            f"  only in requirements.txt: {sorted(set(actual) - set(expected))}"
        )

    def test_every_dependency_is_pinned(self):
        unpinned = [line for line in _pyproject_requirements() if "==" not in line]
        assert not unpinned, (
            f"Unpinned dependencies make runs irreproducible: {unpinned}. " f"Pin with '=='."
        )
