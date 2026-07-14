---
name: test-data-teardown
description: >-
  Registers a cleanup for data a test creates (via API or UI) with
  teardown_registry, so it's automatically removed after the test, pass or
  fail. Use whenever a step/action creates a group, member, event, invite,
  or any other persistent entity. Do NOT use for pre-seeded precondition
  data set up in a fixture before UI steps run — that's
  api-test-setup-teardown's job (yield + delete in the same fixture). Do NOT
  use for data the app itself has no delete API for (e.g. onboarding's
  org/user — see APP_CONTEXT.md).
---

# Test Data Teardown

Read [AGENTS.md](../../AGENTS.md) → "Teardown" first — this skill is the
worked example, not a replacement for that convention.

## When this applies vs. `api-test-setup-teardown`

| Scenario | Skill |
|---|---|
| Seed 50 records via API *before* the UI flow under test runs | `api-test-setup-teardown` (fixture `yield` + delete) |
| The **flow under test itself** creates data (e.g. testing the "create group" form) — the entity's id isn't known until the UI action completes | `test-data-teardown` (this skill) |

Both end the same way: something gets deleted after the test. The
difference is *when* you know what to delete. `test-data-teardown` is for
the "I only find out the id mid-test" case that a `yield`-fixture can't
express.

## Pattern

1. Import the singleton — same pattern as `session_state`, no fixture
   threading needed:
   ```python
   from src.core.teardown import teardown_registry
   ```
2. The instant a page action / step creates something and gets its id back,
   register the cleanup **immediately** — don't wait until "later in the
   test," it may never get there if a later step fails:
   ```python
   def create_group(self, name: str) -> str:
       group_id = self.click_create_and_capture_id(name)  # however this PO/action returns it
       teardown_registry.register(
           lambda: self.api_client.delete(f"/v1/groups/{group_id}"),
           label=f"delete group {group_id}",
       )
       return group_id
   ```
3. Nothing else to do. `tests/conftest.py`'s autouse `_run_data_teardown`
   fixture calls `teardown_registry.run_all()` after every test automatically
   — LIFO order, runs regardless of pass/fail, one failing cleanup doesn't
   block the rest (each failure is attached to Allure instead of raising).

## Where the register call lives

- Page Actions layer, right next to the create call — mirrors AGENTS.md's
  Page Actions rule ("business logic and interactions").
- Never in Page Objects (locators only) or Tests (orchestrate Steps only).

## Combining with API setup

If you're already using `api_client` from `api-test-setup-teardown` for
setup, reuse the same client for the delete call in `register()` — don't
create a second HTTP client.

## Before you assume there's nothing to clean up

Check whether the app actually exposes a delete/cleanup endpoint for the
entity before deciding "not applicable." If it doesn't (confirmed, not
assumed), document the gap in `APP_CONTEXT.md` next to that flow — same as
the existing onboarding note — rather than silently skipping teardown.
