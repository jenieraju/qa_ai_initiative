# AGENTS.md — UI Automation Framework Conventions

This file documents enforced conventions for AI assistants and contributors working in this repository. For what the application under test (cofee-web) actually does, see [APP_CONTEXT.md](APP_CONTEXT.md) instead — this file covers the test framework only.

## Stack

- **pytest** + **pytest-playwright** (sync API only — never mix sync/async)
- **pytest-xdist** + **pytest-xdist-worker-stats** with `--dist loadgroup`
- **allure-pytest** for reporting
- **python-dotenv** + **Pydantic settings** for config
- **httpx** for API calls (when needed)
- **ruff** + **black** via pre-commit
- **invoke** (`tasks.py`) as task runner

## Four-layer architecture (strict top-down dependency)

```
Tests → Steps → Page Actions → Page Objects
```

| Layer | May call | Must NOT call |
|-------|----------|---------------|
| Tests (`tests/test/`) | Steps, assert helpers | Page actions, POs directly |
| Steps (`src/steps/`) | Page actions | POs directly |
| Page Actions (`src/page_actions/`) | POs, sibling actions | Steps, tests |
| Page Objects (`src/page_objects/*_po.py`) | BasePage helpers only | Business logic |

## Page Objects

- File suffix: `*_po.py`
- All locators in `__init__` under `# --- Locators ---`
- Methods return `Locator` or plain values — no clicks/fills
- Dynamic locators: `_loc_*()` helpers + format templates in `__init__`
- Naming prefixes: `btn_`, `txt_`, `txa_`, `chk_`, `rdo_`, `dtp_`, `ddl_`, `img_`, `mnu_`, `tbl_`, `msg_`, `lnk_`, `cbo_`, `dlg_`, `frm_`, `fra_`, `lbl_`, `lst_`, `rtf_`, `tab_`, `dgd_`, `pnl_`, `sld_`, `spn_`, `tlb_`, `tre_`, `plh_`, `input_`, `div_`, `icn_`, `opt_`

## Page Actions

- Inherit `PageActions`
- Instantiate corresponding PO in `__init__`
- Verb-phrase methods: `click_filter_option()`, `verify_element_visible()`
- Delegate to sibling methods instead of duplicating logic
- Extract repeated 3+ line sequences shared by two callers

## Steps

- `@allure.step("User ...")` on every public step
- Orchestrate page actions only
- One step decorator per logical user action

## Tests

- `@pytest.mark.e2e` on every UI test
- Priority: `@pytest.mark.p0|p1|p2`
- Feature markers: `@pytest.mark.<feature>`
- `@pytest.mark.ignore` to exclude from default runs
- Allure: epic, suite, feature, severity on class/test; dynamic title/description in body
- Parametrize from `tests/dataprovider/dp_*.py`
- `pytestmark = pytest.mark.xdist_group(...)` when sharing mutable state
- Tests must be independent — no ordering dependencies

## Config

- Always use `get_settings()` — never instantiate `Settings` directly
- Never hardcode hosts — use `ENV_URL_MAP` or env vars
- Required vars validated at import/collection time
- Secrets via env/config only; encrypt stored credentials in `data/`, decrypt with `CREDENTIALS_ENCRYPTION_KEY`
- Never commit `.env` files

## Dataproviders

- Prefix: `dp_`, function: `get_*_test_data()` returning `list[pytest.param(..., id="...")]`
- No secrets in dataproviders
- Time-relative values computed at runtime in tests, not at collection time

## conftest.py

- Inserts repo root + `tests/` on `sys.path`
- Registers all custom markers in `pytest_configure`
- CLI: `--env`, `--target-browser`, `--headless`, `--record-video`
- `browser_context_args`: `@pytest.mark.auth_profile("name")` → `.auth/{name}.json`
- Autouse timeout fixture for slow environments
- `pytest_runtest_makereport`: attach screenshot of most recent page/tab on failure

## Coding standards

- Inline single-use locators — don't assign to a variable used once
- Prefer element waits over fixed `sleep`
- `except Exception:` — never bare `except:`
- All imports at module top
- No `pytest.skip()` in page actions
- One-line module/class docstrings; comments only when non-obvious
- No abstractions beyond what's listed here

## Commands

```bash
invoke install
invoke install-precommit
invoke lint
invoke test --env dev
invoke test --env dev --parallel 2
invoke report
```

## Adding a new feature

1. Create `src/page_objects/{feature}_po.py` with real locators
2. Create `src/page_actions/{feature}_actions.py`
3. Create `src/steps/{feature}_steps.py`
4. Create `tests/dataprovider/dp_{feature}.py`
5. Create `tests/test/{area}/test_{feature}.py`
6. Add feature marker to `pytest.ini` if new
7. Run `invoke lint`
