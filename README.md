# LMS UI Automation (sara-trial-1)

UI test automation for CoFee's Lead Management (LMS) feature, targeting `cofee-web`.

Stack: Python + Playwright (sync API) + pytest + Allure. Matches `cofee-frontend-automation`'s established convention for testing this same app.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

cp .env.example .env  # fill in USER_PHONE / USER_OTP / ORGANISATION_NAME
```

## Running tests

```bash
pytest
pytest --env stg
```

## Structure

```
config/config.yaml          # per-environment base URL, browsers, viewports
src/config/config_loader.py # reads config.yaml
src/core/browser_base.py    # browser/context launch
src/core/assert_helper.py   # UI assertions + wait helpers
src/pages/                  # page objects, one per real page
tests/                      # feature-grouped test folders
auth/                       # cached storageState (gitignored)
```

## Workflow

Built via this project's `.claude/skills/` — see `.claude/skills/README.md` for the full suite and `.claude/agents/ui-automation-agent.md` for the sequence.
