"""Unit tests asserting .claude/skills/ stays honest.

Smoke tests, not a substitute for reading a skill: they catch the classes of
bug this repo already had once — a skill referencing a `get_settings()` field
that doesn't exist (`settings.api_token`), a `name:` that doesn't match its
folder, a relative AGENTS.md link that resolves to the wrong directory, and a
skill missing from the catalog table in the skills README.

They cannot judge whether a skill's steps are *correct* — that still needs a
human/agent to read the repo — but they do now check that every framework
symbol a skill names actually exists, which is how a skill came to recommend
`wait_for_spinner_to_disappear` months after it was deleted.

No browser involved — pure text checks against repo files.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"

# create-skill's own rule, relaxed for template-heavy skills: this bar exists to
# catch a skill that has started restating AGENTS.md, not to police code templates
# (scaffold-feature-automation legitimately carries five of them).
MAX_SKILL_LINES = 220

# The per-skill cap alone lets the catalog grow without limit; this bounds the sum.
MAX_CATALOG_LINES = 1_800

# Names skills use in illustrative snippets that are deliberately *not* real
# framework helpers — the reader is meant to substitute their own. Keep this
# list short: every entry is a place a skill shows code that cannot be run.
ILLUSTRATIVE_NAMES = {
    "click_create_and_capture_id",  # test-data-teardown: "however your action returns the id"
    "create_and_return_id",  # same
    "wait_for_job",  # api-test-setup-teardown: pre-poll_until example
}

# Legitimate instance attributes on framework base classes, not callables.
FRAMEWORK_ATTRIBUTES = {"po", "page", "settings"}

# Locators are per-feature page-object attributes, never framework symbols, so a
# skill's example locator must not be mistaken for a missing helper. Prefixes are
# the ones discover-locators-from-ui mandates.
LOCATOR_PREFIXES = ("btn_", "input_", "chk_", "ddl_", "msg_", "lbl_", "tbl_", "lnk_", "loc_")

pytestmark = pytest.mark.unit


def _skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def _frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "SKILL.md must open with a --- frontmatter block"
    return match.group(1)


def _declared_name(text: str) -> str:
    match = re.search(r"^name:\s*(\S+)\s*$", _frontmatter(text), re.MULTILINE)
    assert match, "frontmatter must declare 'name:'"
    return match.group(1)


def _code_blocks(text: str) -> list[str]:
    return re.findall(r"^```[a-z]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE)


def _settings_fields() -> set[str]:
    """Field names and @property names on the Settings class."""
    source = (REPO_ROOT / "src" / "core" / "settings.py").read_text(encoding="utf-8")
    fields = set(re.findall(r"^\s{4}(\w+):\s*\w[\w\[\], |]*\s*=\s*Field\(", source, re.MULTILINE))
    fields |= set(re.findall(r"^\s{4}def (\w+)\(self\)", source, re.MULTILINE))
    return fields


def _pytest_ini_addopts() -> set[str]:
    """Flags actually present in pytest.ini's addopts block.

    One flag per line in this repo, so take the leading token and drop any
    `=value` — a path like output/junit-results.xml is not a flag.
    """
    source = (REPO_ROOT / "pytest.ini").read_text(encoding="utf-8")
    block = re.search(r"^addopts =\n((?:[ \t]+\S.*\n)+)", source, re.MULTILINE)
    if not block:
        return set()
    flags = set()
    for line in block.group(1).splitlines():
        token = line.strip().split("=", 1)[0]
        if token.startswith("-"):
            flags.add(token)
    return flags


def _src_symbols() -> set[str]:
    """Every class, function and method name defined anywhere under src/."""
    import ast

    symbols: set[str] = set()
    for path in (REPO_ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                symbols.add(node.name)
    return symbols


class TestSkillsSync:
    """Structural invariants across every skill in .claude/skills/."""

    def test_at_least_one_skill_exists(self):
        assert _skill_files(), f"No SKILL.md files found under {SKILLS_DIR}"

    def test_cursor_skills_is_a_symlink_to_claude_skills(self):
        cursor_skills = REPO_ROOT / ".cursor" / "skills"
        assert cursor_skills.is_symlink(), (
            ".cursor/skills must be a symlink to ../.claude/skills so Cursor and "
            "Claude Code share one copy of every skill"
        )
        assert cursor_skills.resolve() == SKILLS_DIR.resolve()

    def test_name_matches_folder(self):
        for skill in _skill_files():
            text = skill.read_text(encoding="utf-8")
            assert (
                _declared_name(text) == skill.parent.name
            ), f"{skill.parent.name}: frontmatter name is '{_declared_name(text)}'"

    def test_description_states_when_to_use_and_when_not_to(self):
        for skill in _skill_files():
            frontmatter = _frontmatter(skill.read_text(encoding="utf-8"))
            assert "description:" in frontmatter, f"{skill.parent.name}: no description"
            lowered = " ".join(frontmatter.lower().split())
            assert "use when" in lowered, f"{skill.parent.name}: description lacks 'Use when'"
            assert "do not use" in lowered, (
                f"{skill.parent.name}: description lacks a 'Do NOT use for ...' clause — "
                "that clause is what stops the skill mis-triggering"
            )

    def test_settings_attributes_referenced_actually_exist(self):
        """Catches snippets like `settings.api_token` when Settings has no such field."""
        known = _settings_fields()
        for skill in _skill_files():
            text = skill.read_text(encoding="utf-8")
            referenced = set(re.findall(r"(?:get_settings\(\)|settings)\.(?!py\b)(\w+)", text))
            unknown = {attr for attr in referenced if attr not in known}
            assert not unknown, (
                f"{skill.parent.name}: references non-existent Settings attribute(s) "
                f"{sorted(unknown)} — add the field to src/core/settings.py or fix the skill"
            )

    def test_relative_doc_links_resolve(self):
        for skill in _skill_files():
            text = skill.read_text(encoding="utf-8")
            for target in re.findall(r"\]\((\.\.[^)]+)\)", text):
                resolved = (skill.parent / target).resolve()
                assert resolved.exists(), (
                    f"{skill.parent.name}: link '{target}' resolves to {resolved}, "
                    "which does not exist"
                )

    def test_every_skill_is_listed_in_the_readme_catalog(self):
        readme = (SKILLS_DIR / "README.md").read_text(encoding="utf-8")
        for skill in _skill_files():
            assert f"`{skill.parent.name}/`" in readme, (
                f"{skill.parent.name}: missing from the catalog table in "
                ".claude/skills/README.md"
            )

    def test_skills_stay_short_enough_to_not_duplicate_agents_md(self):
        for skill in _skill_files():
            lines = len(skill.read_text(encoding="utf-8").splitlines())
            assert lines <= MAX_SKILL_LINES, (
                f"{skill.parent.name}: {lines} lines (max {MAX_SKILL_LINES}) — "
                "likely restating AGENTS.md; link instead"
            )

    def test_no_stale_pytest_invocations(self):
        """This repo has no pytest-repeat, and headed runs use --headless false.

        Only code blocks are checked — prose may legitimately warn against a flag.
        """
        for skill in _skill_files():
            text = "\n".join(_code_blocks(skill.read_text(encoding="utf-8")))
            assert "--count=" not in text, (
                f"{skill.parent.name}: uses --count (pytest-repeat), which is not "
                "in requirements.txt"
            )
            assert "--headed" not in text, (
                f"{skill.parent.name}: uses --headed; this repo defines "
                "--headless true|false in tests/conftest.py"
            )

    def test_no_skill_recommends_a_helper_base_page_lacks(self):
        """`get_by_label` is the recurring one: no such helper on BasePage.

        `test_framework_symbols_referenced_actually_exist` only sees `self.foo(`
        calls, so a bare mention in a prose table slips past it — which is how a
        skill came to forbid `get_by_label` in one section and recommend it in
        another.
        """
        base_page = (REPO_ROOT / "src" / "core" / "base_page.py").read_text(encoding="utf-8")
        helpers = set(re.findall(r"^\s{4}def (get_by_\w+)\(", base_page, re.MULTILINE))
        offenders: list[str] = []
        for skill in _skill_files():
            for line in skill.read_text(encoding="utf-8").splitlines():
                for name in re.findall(r"\bget_by_\w+", line):
                    # A skill may name a missing helper only to warn against it.
                    if name in helpers or "no `" + name + "`" in line or "none use" in line:
                        continue
                    offenders.append(f"{skill.parent.name}: {name} — {line.strip()}")

        assert not offenders, (
            "These skills reference a get_by_* helper that BasePage does not "
            f"define (it has: {', '.join(sorted(helpers))}). Use a real helper, "
            "or phrase the mention as an explicit warning:\n  " + "\n  ".join(sorted(offenders))
        )

    def test_markers_shown_in_skills_are_registered(self):
        """addopts carries --strict-markers, so an unregistered marker is a hard error.

        A skill showing `pytest.mark.smoke` hands the reader a snippet that fails
        at collection time with "not found in markers configuration".
        """
        ini = (REPO_ROOT / "pytest.ini").read_text(encoding="utf-8")
        registered = set(re.findall(r"^\s{4}(\w+)", ini.split("markers =")[1], re.MULTILINE))
        builtin = {"parametrize", "skip", "skipif", "xfail", "usefixtures", "filterwarnings"}
        offenders: list[str] = []
        for skill in _skill_files():
            for marker in set(
                re.findall(r"pytest\.mark\.(\w+)", skill.read_text(encoding="utf-8"))
            ):
                if marker not in registered and marker not in builtin:
                    offenders.append(f"{skill.parent.name}: pytest.mark.{marker}")

        assert not offenders, (
            "These skills show a marker that pytest.ini does not register; with "
            "--strict-markers the snippet fails at collection. Register it or use "
            f"a registered one ({', '.join(sorted(registered))}):\n  "
            + "\n  ".join(sorted(offenders))
        )

    def test_quoted_pytest_ini_flags_match_reality(self):
        """A skill claiming a flag is "already in pytest.ini addopts" must be right.

        The false claim this catches cost a debugging session: the skill said `-s`
        was in addopts, so nobody passed it and nobody saw the print output.
        """
        addopts = _pytest_ini_addopts()
        offenders: list[str] = []
        for skill in _skill_files():
            text = skill.read_text(encoding="utf-8")
            for flag, gap in re.findall(r"`(-{1,2}[\w-]+)`([^\n]{0,60}?)in `?pytest\.ini", text):
                # "-s is NOT in pytest.ini" is a correct statement, not a claim.
                if re.search(r"\bnot\b", gap) or flag in addopts:
                    continue
                offenders.append(f"{skill.parent.name}: claims {flag} is in pytest.ini addopts")

        assert (
            not offenders
        ), f"pytest.ini addopts is: {' '.join(sorted(addopts))}\n  " + "\n  ".join(
            sorted(offenders)
        )

    def test_parallel_group_lists_match_the_module(self):
        """A skill enumerating the xdist groups goes stale the next time one is added."""
        source = (REPO_ROOT / "tests" / "parallel_groups.py").read_text(encoding="utf-8")
        real = {
            m.removeprefix("PARALLEL_GROUP_")
            for m in re.findall(r"^(PARALLEL_GROUP_\w+)", source, re.MULTILINE)
        }
        offenders: list[str] = []
        for skill in _skill_files():
            for line in skill.read_text(encoding="utf-8").splitlines():
                listed = set(re.findall(r"`([A-Z_]{3,})`", line)) & real
                # One name mentioned in passing isn't an enumeration; two or more is a list,
                # and a list that omits a real group has gone stale.
                if len(listed) >= 2 and real - listed:
                    offenders.append(
                        f"{skill.parent.name}: lists {sorted(listed)}, "
                        f"missing {sorted(real - listed)}"
                    )

        assert not offenders, (
            "These skills enumerate parallel groups and have drifted from "
            "tests/parallel_groups.py. Point at the module instead of listing "
            "the constants:\n  " + "\n  ".join(sorted(offenders))
        )

    def test_framework_symbols_referenced_actually_exist(self):
        """A skill must not recommend a helper or attribute the framework lacks.

        Catches the real failure mode: a helper is deleted as dead code and the
        skill that recommended it silently becomes a dead end for whoever
        follows it next.
        """
        symbols = _src_symbols() | ILLUSTRATIVE_NAMES | FRAMEWORK_ATTRIBUTES
        stale: list[str] = []
        for skill in _skill_files():
            text = skill.read_text(encoding="utf-8")
            # self.foo(...) claims a method; self.foo.bar(...) claims an attribute.
            referenced = set(re.findall(r"self\.(\w+)\s*\(", text))
            referenced |= set(re.findall(r"self\.(\w+)\.", text))
            for name in sorted(referenced - symbols):
                if name.startswith(LOCATOR_PREFIXES):
                    continue
                stale.append(f"{skill.parent.name}: self.{name}")

        assert not stale, (
            "These skills name a framework symbol that does not exist in src/. "
            "Either restore it or fix the skill — a skill pointing at a deleted "
            "helper sends the next reader down a dead end. If the name is "
            "deliberately illustrative, add it to ILLUSTRATIVE_NAMES with a "
            "comment saying why:\n  " + "\n  ".join(stale)
        )

    def test_catalog_total_stays_within_budget(self):
        """The per-skill cap doesn't stop the catalog outgrowing anyone's attention."""
        per_skill = {
            s.parent.name: len(s.read_text(encoding="utf-8").splitlines()) for s in _skill_files()
        }
        total = sum(per_skill.values())
        assert total <= MAX_CATALOG_LINES, (
            f"Skills catalog is {total} lines (max {MAX_CATALOG_LINES}) across "
            f"{len(per_skill)} skills. Every one competes for the same attention — "
            f"trim or merge rather than raising this. Largest: "
            f"{sorted(per_skill.items(), key=lambda kv: -kv[1])[:3]}"
        )
