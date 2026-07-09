---
name: create-skill
description: >-
  Creates a new .claude/skills/<name>/SKILL.md for this repo, covering exactly
  ONE repeatable task. Use when asked to "create a skill", "write a SKILL.md",
  "add a skill for X", "make this workflow a skill", or "turn this into a
  reusable skill". Do NOT use to perform the workflow itself (e.g. actually
  scaffolding a page object or writing a test — see
  ../../.cursor/skills/scaffold-feature-automation or create-dataprovider), and
  do NOT use for editing AGENTS.md or general framework-rule changes.
---

# Create Skill

Meta-skill: writes other skills. Never writes test code, page objects, or
edits AGENTS.md itself — those belong to the skill being created, or to a
human editing AGENTS.md directly.

## 1. Clarify scope

Confirm the ONE repeatable task the new skill covers. If the request spans
multiple tasks (e.g. "page objects and dataproviders"), ask which one, or
propose splitting into separate skills. A skill that covers two tasks is two
skills.

## 2. Read the repo first — never invent a workflow

- Read `AGENTS.md` at the repo root (this repo has no `CLAUDE.md` — `AGENTS.md`
  is the conventions doc).
- Read `.cursor/skills/README.md` for the level guide and the "don't duplicate
  AGENTS.md" rule that also applies to `.claude/skills`.
- Find and read 2–3 real examples of the task in this repo — actual page
  objects (`src/page_objects/*_po.py`), page actions, steps, test files
  (`tests/test/**/test_*.py`), dataproviders (`tests/dataprovider/dp_*.py`), or
  `tests/conftest.py` — whichever apply to the task. Name every file you read
  in your response.
- If an equivalent skill already exists in `.cursor/skills/`, read it in full —
  it is the closest style reference and may cover the same task already (ask
  whether to port it instead of writing fresh).
- If no real example of the task exists anywhere in the repo, **stop and say
  so**. Do not fall back on generic Playwright/Pytest/invoke knowledge.

## 3. Write the frontmatter

```yaml
---
name: <kebab-case, matches folder .claude/skills/<name>/SKILL.md>
description: >-
  <one task, one sentence of what it does>. Use when <2-4 concrete trigger
  phrases a teammate would actually type>. Do NOT use for <explicit
  non-trigger situations, e.g. performing the workflow manually, or a
  different existing skill's job>.
---
```

Mirror the folded (`>-`) description style and "Use when / do NOT use" shape
from `.cursor/skills/create-dataprovider/SKILL.md` and
`.cursor/skills/debug-flaky-e2e-test/SKILL.md`.

## 4. Write the body as a numbered/checklist procedure, not prose

- Order steps to match the repo's real pipeline for that task. For anything
  touching the four-layer stack, the order is
  `page object → page actions → steps → dataprovider → test file → pytest.ini marker`
  (see `AGENTS.md` "Adding a new feature" and
  `.cursor/skills/scaffold-feature-automation/SKILL.md`) — adjust only if the
  task's real pipeline differs.
- Every file-creating step names the exact path and a real reference file to
  mirror, e.g. "mirror `src/page_objects/login_po.py` for locator naming
  prefixes."
- Inline only the `AGENTS.md` guardrails that bite for *this* task (e.g. no
  `page.locator()` outside page objects; no secrets in dataproviders; markers
  registered in `pytest.ini`/`conftest.py` before use; web-first
  assertions/no hard sleeps). For everything else write "see AGENTS.md" — do
  not restate the whole file.
- Include the actual local run commands from `tasks.py` (`invoke test --env
  dev`, `invoke test --env dev --parallel 2`, `invoke report`) or direct
  `pytest` invocations from `README.md` — never guess flags.

## 5. End with a "Done when" checklist

Binary, verifiable items only — no "should work" language. Example shape:

```
- [ ] File(s) created at the exact path(s) named in the skill
- [ ] invoke lint passes
- [ ] pytest --collect-only --env dev -m "<marker>" collects the new item
- [ ] No rule from AGENTS.md restated verbatim in the skill body
```

## 6. Self-check the trigger

After writing, list 3 example user messages that should trigger the new skill
and 2 that should not. If any fail, rewrite the `description` — this is the
only field that determines invocation.

## 7. Keep it under ~150 lines

If it's longer, some of `AGENTS.md` got duplicated — cut it and link instead.

## Done when (for create-skill itself)

- [ ] New skill exists at `.claude/skills/<name>/SKILL.md` with valid frontmatter
- [ ] `description` contains explicit "Use when" and "do NOT use" phrases
- [ ] Body is a numbered/checklist procedure, not paragraphs
- [ ] Names of the 2–3 real repo files read are stated in the response
- [ ] References `AGENTS.md` (not a fabricated `CLAUDE.md`) for shared rules
- [ ] Refused and stopped if no real example of the task existed in the repo
- [ ] 3 triggering / 2 non-triggering example messages listed and description
      adjusted if any failed
