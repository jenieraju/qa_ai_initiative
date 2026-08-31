---
name: review-automation-pr
description: >-
  Repo-specific scope and checklist for reviewing a pull request in this
  automation framework — what to skip, what to flag, and how to report it.
  Use when asked to "review this PR", "check this diff before I push", or
  when acting as an automated reviewer on a pull request in this repo. Do
  NOT use for a general correctness bug hunt (`code-review`) or a
  reuse/simplify/efficiency pass (`simplify`) — apply this checklist inside
  either, as the domain knowledge those generic passes don't have.
---

# Review Automation PR

This is a **write-time checklist as much as a review-time one**: satisfy it
while writing a page object, action, step, or test, and the diff already
clears review. It extends `AGENTS.md` — read that first — with review scope
and the concrete, repo-specific things to flag; it does not restate its
Architecture table.

## Skip — locators

Never review, in `src/page_objects/*_po.py`:

- Locator strategy, selector strings, XPath/CSS values
- Index-based locators (`.nth(1)`) or multi-match filters
- Whether a locator "looks fragile" — it is correct if it matches the live app

Locators are confirmed against the running app by `discover-locators-from-ui`,
not derived from taste. A page object method that only returns a `Locator` is
never a finding by itself.

## Review by layer

| Layer | Check |
|---|---|
| `src/page_actions/*_actions.py` | Business logic and screen-level `verify_*` assertions via `assert_helper`; delegates to `self.po.*`, never constructs a locator; sibling methods manage UI state consistently (one method shouldn't open a dropdown internally while a sibling expects the caller to) |
| `src/steps/*_steps.py` | Every public function has `@allure.step`; module-level functions, not a class; calls Page Actions only, never a page object or `page.*` directly |
| `tests/test/**/test_*.py` | `@pytest.mark.e2e` + a priority (`p0`/`p1`/`p2`) + the feature marker; class carries `@allure.epic/suite/feature`, methods carry `@allure.story/severity`; test is independent of run order; no hardcoded data outside `tests/dataprovider/dp_*.py` |
| `tests/dataprovider/dp_*.py` | No secrets, no time-relative values, no real org-entity names — see `create-dataprovider` |
| `src/core/` | `base_page.py`, `page_actions.py`, `assert_helper.py`, `settings.py`, `auth_storage.py`, `session_state.py`, `teardown.py`, `api_client.py` — correctness of the shared primitive, not one caller's usage |

## Issues to flag

- **Teardown that could delete more than what the test created.** A
  `teardown_registry.register(...)` callback must delete by the exact id/name
  the test just created (see `test-data-teardown`) — never "the first/most
  recent row" from a shared listing. On a shared dev org that removes someone
  else's data.
- **API setup/cleanup bypassing `ApiClient` for a raw `httpx` call** —
  AGENTS.md bans this; `src/core/api_client.py` is the one implementation.
- Business logic or an `assert_helper` call inside a page object (layer
  violation — Page Objects are locators only).
- Locator construction (`page.locator(...)`, `page.get_by_*(...)`) outside
  `src/page_objects/`. Mechanically enforced by
  `tests/test/core/test_layer_boundaries.py` — a PR that fails it needs no
  human judgment call, just the fix.
- `time.sleep(...)` or `page.wait_for_timeout(...)` anywhere except
  `api_client.py`'s `poll_until` — also enforced by `test_layer_boundaries.py`.
- A one-shot `.is_visible()` / `.text_content()` / `.count()` check on
  async-rendering UI where an `assert_helper` (`expect`-based, auto-retrying)
  call does the same check without a race.
- Hardcoded test data, URLs, or credentials instead of `get_settings()` /
  `tests/dataprovider/`.
- A step missing `@allure.step`, or a test missing its Allure class/method
  annotations.
- A test that depends on another test's execution order or leftover state.
- A bare `except:` (AGENTS.md bans it — use `except Exception` or a specific
  type).
- Imports inside a test method, action, or step instead of the module top.
- Sibling methods that duplicate each other instead of delegating (e.g. a
  `get_first_x()` that could just call the indexed version with `0`).
- A step re-implementing page-action logic, or calling a PO locator directly.
- A vague method-name suffix (`_again`, `_v2`, `_new`) instead of a name that
  describes the actual behavior.
- `Settings()` instantiated directly instead of `get_settings()` — the
  cached-per-env singleton is what makes CLI overrides (`--headless`, env)
  visible to every call site.

## Do not flag

- Ruff/black concerns — `pyproject.toml`'s `[tool.ruff.lint]` already selects
  `F` (unused imports/names) and `E` (including bare `except:`), and the
  `framework-unit-tests` pre-commit hook runs both before a commit lands.
  Flagging them again in review is noise.
- Anything inside `src/page_objects/` per the Skip section above.
- Pre-existing issues outside the diff — comment only on changed lines.

## Reporting findings

- No praise comments — they read as an actionable item to some UIs.
- No informational-only comments; every comment needs a concrete fix.
- One instance of a repeated pattern gets a comment; note "same pattern in
  N other files" instead of repeating it per file.
- Roll findings into one summary with counts by severity and a one-line
  merge verdict, rather than scattering low-value single-line comments.

## Done when

- [ ] Every flagged item is on a changed line, with a concrete fix named
- [ ] No locator/selector content was reviewed
- [ ] No finding duplicates something `ruff`/`black` already catches
- [ ] Layer-boundary and no-sleep findings point at
      `tests/test/core/test_layer_boundaries.py` as the mechanical source of
      truth, not personal judgment
- [ ] Summary comment has counts by severity and one merge verdict; no praise

## Self-check

Triggers: "review this PR", "check my diff before I open the PR", "review
the group-create page actions I just wrote".
Does not trigger: "find correctness bugs in this diff" (`code-review`), "clean
up this diff for reuse/simplification" (`simplify`), "write the test cases"
(`generate-test-cases`).
