---
name: auth-storage-state-setup
description: >-
  Captures and manages Playwright storage state files in .auth/ via
  src/core/auth_storage.py for role-based test profiles. Use when setting up
  login bypass for a new role, adding an auth_profile marker to a suite, or
  refreshing an expired .auth/{profile}.json. Do NOT use when the login or OTP
  flow is itself the thing under test (write real login steps), and do NOT use
  to store credentials — those stay in .env via get_settings().
---

# Auth Storage State Setup

Uses `@pytest.mark.auth_profile("name")` → loads `.auth/{name}.json`. See [AGENTS.md](../../../AGENTS.md).

## When to use storage state

| Use storage state | Use UI login steps |
|-------------------|-------------------|
| Most tests skip login | Login flow is the test subject |
| Stable session, same role | Testing OTP/MFA/session expiry |
| Faster suite execution | First-time capture |

## Capture — use the framework helper, never raw sync_playwright

`src/core/auth_storage.py` already owns this. Do not write a standalone
`sync_playwright()` script:

| Need | Use |
|---|---|
| Save the current context | `save_auth_storage_state(page, profile_name)` |
| Path for a profile | `auth_state_path(profile_name)` |
| Guard before reuse | `auth_state_exists(profile_name)` |
| Default profile name | `DEFAULT_AUTH_PROFILE` (`"default"`) |

Capture happens **inside a login test**, so the saved state is always produced
by the same steps a user takes. `user_saves_authenticated_session`
(`src/steps/login_steps.py`) is a **separate step you must call yourself** — it
is deliberately not folded into `user_logs_in_with_mobile_and_otp`, so a test
of the login flow can log in without overwriting a good stored session. Two
callers show the pattern: `tests/test/auth/test_login.py` (after asserting the
login succeeded) and `user_ensures_logged_in()` (after a fallback login).

For a **new role**, add a login test for that role and save under its own
profile — no new helper needed:

```python
import pytest

from src.core.settings import get_settings
from src.steps.login_steps import (
    user_logs_in_with_mobile_and_otp,
    user_saves_authenticated_session,
)


class TestCaptureSessions:
    """Login tests whose job is to save a reusable storage state."""

    @pytest.mark.e2e
    @pytest.mark.login
    @pytest.mark.p0
    def test_capture_org_admin_session(self, page):
        settings = get_settings()
        # login_mobile_number / login_otp are fallback properties:
        # FEATURE_LOGIN_* first, then SHARED_* (src/core/settings.py).
        user_logs_in_with_mobile_and_otp(
            page, settings.login_mobile_number, settings.login_otp
        )
        user_saves_authenticated_session(page, "org_admin")
```

`save_auth_storage_state` creates `.auth/` if missing, writes the file, and
`user_saves_authenticated_session` also sets `session_state` and attaches the
path to Allure.

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

`user_saves_authenticated_session` already calls
`session_state.set_active_profile(profile_name)`. Only call it yourself to
record extra identity for reporting:

```python
from src.core.session_state import session_state
session_state.set_active_profile("org_admin", user_email=email, org_id=org_id)
```

`user_email` and `org_id` are keyword-only (`src/core/session_state.py`).

## Gotcha — a missing profile fails silently

`browser_context_args` in `tests/conftest.py` applies `storage_state` **only if
the file exists**; if `.auth/{profile}.json` is absent it returns unchanged, so
the test runs **unauthenticated** and fails later with a confusing redirect
instead of a clear error. When a suite depends on a profile, guard it:

```python
from src.core.auth_storage import auth_state_exists

if not auth_state_exists("org_admin"):
    pytest.skip("Run test_capture_org_admin_session first")
```

## Done when

- [ ] Capture goes through `save_auth_storage_state` — no raw `sync_playwright()`
- [ ] Profile name matches `@pytest.mark.auth_profile("<name>")` exactly
- [ ] `.auth/<profile>.json` exists locally and is gitignored (`.gitignore:21`)
- [ ] Consuming suite guards on `auth_state_exists` or documents the dependency
- [ ] `invoke lint` passes

## Self-check

Triggers: "set up a storage-state profile for the branch admin role", "tests
are getting 401s, refresh the auth state", "make the groups suite skip login".
Does not trigger: "test that an invalid OTP shows an error" (login is the
subject), "where do I put the test mobile number" (`.env` / `get_settings()`).
