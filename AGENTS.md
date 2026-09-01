# AGENTS.md

Always-on conventions for this repo. Keep this file short — it loads every turn.
App under test: [APP_CONTEXT.md](APP_CONTEXT.md) (always-on index) and
[context_docs/](context_docs/) (living per-feature records from discovery on).
How-to workflows: [.claude/skills/](.claude/skills/) (progressive disclosure — do not paste skill steps here; `.cursor/skills` is a symlink to it).
Before doing a repo workflow manually (scaffolding, extending automation, adding a dataprovider, verifying tests, reviewing a PR, etc.), check `.claude/skills/` for a matching skill and invoke it — even if the user didn't name it.

## Architecture (mandatory every change)

```
Tests → Steps → Actions → Page Objects
```

Never skip layers.

| Layer | Does | Calls |
|-------|------|-------|
| Tests | markers, Allure metadata, flow-level asserts (URL, cross-screen outcome); independent | Steps only |
| Steps | user workflows; `@allure.step`; exposes actions' checks as `user_verifies_*` | Actions only |
| Actions | UI interactions **and** screen-level assertions via `assert_helper` (`verify_*`) | Page Objects only |
| Page Objects | locators only | no business logic, no Playwright actions |

**Where an assertion goes:** is it about one screen (element visible, text,
field state)? → an Action `verify_*`, surfaced as a Step. Is it about the flow
(landed on the right route, data survived a navigation)? → the Test.

Enforced by `tests/test/core/test_layer_boundaries.py` — it fails the build on a
raw locator outside a page object, a layer skipped, or a `sleep`.

## Always-on rules

- New feature from a PRD? `get-context`: short section in `APP_CONTEXT.md` + create/update `context_docs/<slug>.md` (see that file's "Writing new tests"). Extending a flow? Follow `Detail:` into the same context doc. After automation, enrich that doc (`Status:`). If a test ships `@pytest.mark.ignore`d, also add it to `README.md` → "Next steps".
- **Never invent locators.** Run `discover-locators-from-ui` against the live app or frontend source; record results in `context_docs/<slug>.md` → `## Confirmed locators` before `scaffold-feature-automation`. Placeholder POs without that step must stay `@pytest.mark.ignore`.
- Use `get_settings()` for config — never hardcode URLs, secrets, or credentials.
- Parametrize from `tests/dataprovider/dp_*.py`.
- On create of persistent data, register cleanup with `teardown_registry` (see **Teardown** below and `test-data-teardown` skill).
- **Done means green.** After scaffold or fixes, run `run-and-verify-tests` — do not mark `Status: automated` until non-ignored tests pass.
- Prefer explicit waits over `sleep`. No bare `except`.
- Never assert a specific post-login landing route — it varies by account and role. Assert that `/login` was left behind.
- Before asserting an "error" appears, check it isn't always-visible helper text (see `discover-locators-from-ui` → "Trap").
- API setup/cleanup goes through `src/core/api_client.py` — never a raw `httpx` call.
- Keep code simple; no duplicate logic or extra abstractions.
- Do not restate discoverable facts (stack, folder layout, pytest flags) — read the codebase.

## Teardown

Register cleanup with `teardown_registry` when a test **creates** persistent
data and a delete API exists. `tests/conftest.py` runs registered cleanups
after every test (pass or fail). Exception: irreversible flows with no delete
API (onboarding org/user) — document in `APP_CONTEXT.md`; no registry call.
Details: `test-data-teardown` skill.

## New-feature pipeline

See [.cursor/skills/README.md](.cursor/skills/README.md). New feature:
`get-context` → `generate-test-cases` → `map-test-cases-to-automation` →
`discover-locators-from-ui` → `scaffold-feature-automation` →
`run-and-verify-tests`. Extend existing: swap scaffold for
`extend-feature-automation`. Maintenance: `discover-locators-from-ui` (single locator), `debug-flaky-e2e-test` (multi-test drift).

Unit tests in `tests/test/core/` enforce context sync and layer imports.

## Commands

```bash
invoke install
invoke unit          # fast no-browser gate: layers, doc sync, deps
invoke lint
invoke test --env dev
invoke test-files --env dev --args="--headless false -vv"
invoke onboarding --env dev --headless false
invoke report
invoke report-files
```
