# AGENTS.md

Always-on conventions for this repo. Keep this file short — it loads every turn.
App under test: [APP_CONTEXT.md](APP_CONTEXT.md). How-to workflows: [.cursor/skills/](.cursor/skills/) (progressive disclosure — do not paste skill steps here).

## Architecture (mandatory every change)

```
Tests → Steps → Actions → Page Objects
```

Never skip layers.

| Layer | Does | Calls |
|-------|------|-------|
| Tests | markers, Allure metadata, asserts; independent | Steps only |
| Steps | user workflows; `@allure.step` | Actions only |
| Actions | UI interactions | Page Objects only |
| Page Objects | locators only | no business logic, no Playwright actions |

## Always-on rules

- Use `get_settings()` for config — never hardcode URLs, secrets, or credentials.
- Parametrize from `tests/dataprovider/dp_*.py`.
- On create of persistent data, register cleanup with `teardown_registry` (see `test-data-teardown` skill).
- Prefer explicit waits over `sleep`. No bare `except`.
- Keep code simple; no duplicate logic or extra abstractions.
- Do not restate discoverable facts (stack, folder layout, pytest flags) — read the codebase.

## Commands

```bash
invoke install
invoke lint
invoke test --env dev
invoke report
```
