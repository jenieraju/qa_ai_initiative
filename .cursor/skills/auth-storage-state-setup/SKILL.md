---
name: auth-storage-state-setup
description: >-
  Captures and manages Playwright storage state files in .auth/ for role-based
  test profiles. Use when setting up login bypass, new user roles, or refreshing
  expired auth sessions.
---

# Auth Storage State Setup

Uses `@pytest.mark.auth_profile("name")` → loads `.auth/{name}.json`. See [AGENTS.md](../../AGENTS.md).

## When to use storage state

| Use storage state | Use UI login steps |
|-------------------|-------------------|
| Most tests skip login | Login flow is the test subject |
| Stable session, same role | Testing OTP/MFA/session expiry |
| Faster suite execution | First-time capture |

## Capture script pattern

Create a one-off script or pytest session to save state:

```python
# scripts/capture_auth.py (run manually, never commit secrets)
from playwright.sync_api import sync_playwright
from src.core.settings import get_settings

PROFILE = "org_admin"
settings = get_settings()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{settings.base_url}/login")
    # --- perform login manually or via steps ---
    input("Complete login in browser, then press Enter...")
    context.storage_state(path=f".auth/{PROFILE}.json")
    browser.close()
```

## Profile naming

```
.auth/
  org_admin.json
  branch_admin.json
  viewer.json
  default.json
```

Match names to `@pytest.mark.auth_profile("org_admin")`.

## Test usage

```python
@pytest.mark.auth_profile("org_admin")
@pytest.mark.e2e
def test_dashboard_loads(self, page):
    page.goto("/dashboard")
    ...
```

## Refresh policy

Re-capture when:
- Tokens expire mid-suite
- Login flow changes
- Role permissions updated

Add `.auth/*.json` to `.gitignore` (already excluded) — store capture instructions in README, not the files themselves.

## CI option

- Generate storage state in CI setup job via API login + save artifact
- Or use test mobile/OTP with env-configured credentials in a setup step

## Session state integration

After login, update framework session tracking:

```python
from src.core.session_state import session_state
session_state.set_active_profile("org_admin", user_email=email, org_id=org_id)
```
