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

Read [AGENTS.md](../../../AGENTS.md) → "Always-on rules" first (the
`teardown_registry` bullet) — this skill is the worked example, not a
replacement for that convention.

## When this applies vs. `api-test-setup-teardown`

| Scenario | Skill |
|---|---|
| Seed 50 records via API *before* the UI flow under test runs | `api-test-setup-teardown` (fixture `yield` + delete) |
| The **flow under test itself** creates data (e.g. testing the "create group" form) — the entity's id isn't known until the UI action completes | `test-data-teardown` (this skill) |

Both end the same way: something gets deleted after the test. The
difference is *when* you know what to delete. `test-data-teardown` is for
the "I only find out the id mid-test" case that a `yield`-fixture can't
express.

## This pattern is proven, but unused

`api-test-setup-teardown` → "Wiring is proven, endpoints are not" names the test that proves `ApiClient` + `teardown_registry` compose correctly. Members is the first real candidate for wiring it into a feature (a confirmed delete endpoint exists — see `APP_CONTEXT.md` → "Members"), but its test is still `@pytest.mark.ignore`d pending confirmed locators, so don't guess `org_id`/`branch_id` to wire it early; wait for `discover-locators-from-ui`.

## Pattern

1. Import the singleton — same pattern as `session_state`, no fixture
   threading needed:
   ```python
   from src.core.teardown import teardown_registry
   ```
2. **Register from the Steps layer**, the instant the id is known — don't wait
   until "later in the test", it may never get there if a later step fails.

   Steps are the right layer: they orchestrate, and they are the first layer
   that both knows the new id and is allowed to talk to `ApiClient`. Page
   actions and page objects stay UI-only per the four-layer rule, so a
   `delete()` call does **not** belong in them.

   ```python
   from src.core.api_client import ApiClient
   from src.core.teardown import teardown_registry

   @allure.step("User creates group '{group_name}'")
   def user_creates_group(page: Page, group_name: str) -> str:
       group_id = GroupCreatePageActions(page).create_and_return_id(group_name)

       def delete_group() -> None:
           with ApiClient() as api:
               api.delete(f"/v1/groups/{group_id}")

       teardown_registry.register(delete_group, label=f"delete group {group_id}")
       return group_id
   ```

   Use `ApiClient` (`src/core/api_client.py`) — it carries `API_BASE_URL` and
   the bearer token from settings, and attaches each request/response to
   Allure. Never a raw `httpx` call.
3. Nothing else to do. `tests/conftest.py`'s autouse `_run_data_teardown`
   fixture calls `teardown_registry.run_all()` after every test automatically
   — LIFO order, runs regardless of pass/fail, one failing cleanup doesn't
   block the rest (each failure is attached to Allure instead of raising).

## Combining with API setup

If the test already has an `api` fixture from `api-test-setup-teardown`,
reuse that client for the delete call in `register()` — don't create a
second HTTP client.

## Before you assume there's nothing to clean up

Check whether the app actually exposes a delete/cleanup endpoint for the
entity before deciding "not applicable." If it doesn't (confirmed, not
assumed), document the gap in `APP_CONTEXT.md` next to that flow — same as
the existing onboarding note, and the group-delete note in
`tests/test/groups/test_group_create.py` — rather than silently skipping
teardown.

## Done when

- [ ] `teardown_registry.register(...)` called in the steps layer, in the
      same function that creates the entity
- [ ] Called immediately after the id is known, not later in the test
- [ ] `label=` describes what gets deleted (it shows up in Allure)
- [ ] No new HTTP client if one already exists for the test
- [ ] Confirmed-missing delete endpoints documented in `APP_CONTEXT.md`
- [ ] `invoke lint` passes and the test still passes end to end

## Self-check

Triggers: "clean up the group this test creates", "register teardown for the
member we just added", "tests are leaving data behind in dev".
Does not trigger: "seed 50 groups before the test runs"
(`api-test-setup-teardown`), "onboarding creates an org we can't delete"
(document the gap in `APP_CONTEXT.md`).
