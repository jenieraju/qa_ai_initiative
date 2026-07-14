# QA UI Test Automation Framework

Pytest + Playwright (sync API) + Allure UI test automation with a strict four-layer Page Object Model.

See [APP_CONTEXT.md](APP_CONTEXT.md) for what the application under test (cofee-web) actually does — domain model, features, flows, and locator conventions — before writing new tests.

## Prerequisites

- Python 3.11+
- Java 8+ (for Allure report generation)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
invoke install
invoke install-precommit
cp .env.example .env
cp .env.dev.example .env.dev
# Edit .env / .env.dev with real values (never commit secrets)
invoke test --env dev
invoke report
```

## Environment configuration

Load order:

1. `.env` — sets `APP_ENV=dev|stg|uat|prod`
2. `.env.{ENV_NAME}` — environment-specific overrides
3. `environment/{env}.properties` — optional additional overrides

CLI override: `pytest --env uat1` (aliases mapped in `src/core/settings.py`, e.g. `uat1 → uat01`).

URLs are derived from `ENV_URL_MAP` in `settings.py`. Override with `BASE_URL`, `API_BASE_URL`, and `ADMIN_PORTAL_URL` in env files. Required vars are validated at collection time.

Copy the `.env.*.example` templates and fill in credentials via config only — never in dataproviders or committed files.

### Feature variable fallback

Use `FEATURE_<SUITE>_*` vars with fallback to `SHARED_*` when suites share the same org/user:

```
FEATURE_LOGIN_USER_EMAIL → SHARED_USER_EMAIL
```

## Architecture (top → bottom, dependency only)

| Layer | Path | Responsibility |
|-------|------|----------------|
| Tests | `tests/test/**/test_*.py` | Assert + orchestrate steps |
| Steps | `src/steps/` | `@allure.step` user actions → page actions |
| Page Actions | `src/page_actions/` | Business logic, interactions |
| Page Objects | `src/page_objects/*_po.py` | Locators only |

**Rule:** Locator construction (`page.locator()`, `page.get_by_*()`) is forbidden outside page objects.

## Running tests

```bash
# Default run (excludes @pytest.mark.ignore)
invoke test --env dev

# Parallel with load groups
invoke test --env stg --parallel 2

# Direct pytest
pytest --env dev -m "e2e and p0 and not ignore"
pytest --env dev -n 2 --dist loadgroup
```

### CLI options

| Flag | Description |
|------|-------------|
| `--env` | Target environment |
| `--target-browser` | `chromium`, `firefox`, or `webkit` |
| `--headless` | `true` / `false` |
| `--record-video` | `true` / `false` |

### Markers

- `@pytest.mark.e2e` — required on all UI tests
- `@pytest.mark.p0|p1|p2` — priority
- `@pytest.mark.<feature>` — feature grouping (e.g. `login`)
- `@pytest.mark.ignore` — excluded from default runs
- `@pytest.mark.auth_profile("name")` — loads `.auth/{name}.json` storage state
- `pytestmark = pytest.mark.xdist_group(...)` — parallel group for shared mutable state

## Project layout

```
src/
  core/           # Framework primitives (settings, base classes, session, asserts)
  page_objects/   # Locators only (*_po.py)
  page_actions/   # Business logic
  steps/          # Allure-decorated user steps
  constants/      # Static strings, routes (no secrets)
data/             # Structured fixtures (users, models)
tests/
  conftest.py     # Path setup, markers, fixtures, failure screenshots
  dataprovider/   # dp_*.py parametrization
  parallel_groups.py
  test/           # Feature-organized tests
tasks.py          # invoke task runner
```

## Auth storage state

Save authenticated sessions to `.auth/{profile}.json`. Tests marked `@pytest.mark.auth_profile("profile")` load the matching file automatically.

## Tooling

```bash
invoke lint        # ruff --fix + black
invoke precommit   # run all pre-commit hooks
invoke clean       # remove artifacts
invoke report      # generate Allure HTML report
```

## Next steps

The Login reference implementation uses **placeholder selectors** (`data-testid` stubs). Provide the real app name, environment URLs, and login flow details to finalize locators and enable the example tests (remove `@pytest.mark.ignore`).

See `AGENTS.md` for full coding conventions.

Optional Cursor Agent Skills (workflows, not duplicate rules) live in `.cursor/skills/` — see the README there for the full catalog by level.
