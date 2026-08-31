---
name: create-dataprovider
description: >-
  Creates tests/dataprovider/dp_*.py files with pytest.param rows for
  data-driven E2E tests. Use when parametrizing scenarios, adding negative
  cases or a role matrix, or when a test needs more data variations. Do NOT use
  to create the test/step/action/page-object files themselves
  (scaffold-feature-automation), and do NOT put secrets, real credentials, or
  values computed at collection time in a dataprovider.
---

# Create Dataprovider

Rules from [AGENTS.md](../../../AGENTS.md):

- File prefix: `dp_`
- Function: `get_{feature}_test_data()` → `list[pytest.param(..., id="...")]`
- **No secrets** — credentials from `get_settings()` at runtime
- **No time-relative values** at collection time

## Template

```python
"""{Feature} test data provider."""

import pytest

def get_{feature}_test_data() -> list:
    return [
        pytest.param(
            "field_a",
            "field_b",
            id="happy_path_short_name",
            marks=pytest.mark.p0,
        ),
        pytest.param(
            "bad_a",
            "bad_b",
            id="invalid_input",
            marks=pytest.mark.p1,
        ),
    ]
```

## Test wiring

Param order must match test function signature exactly:

```python
# dp_checkout.py
pytest.param("visa", "100.00", "success", id="visa_payment")

# test_checkout.py
@pytest.mark.parametrize("card_type,amount,expected_status", get_checkout_test_data())
def test_payment(self, page, card_type, amount, expected_status):
    ...
```

## Id naming

- Use snake_case, descriptive: `empty_email`, `expired_session`
- Mirror test case IDs when available: `TC_LOGIN_001` → `id="TC-LOGIN-001"`

## Marks in dataprovider

```python
pytest.param(..., marks=[pytest.mark.p0, pytest.mark.login])  # both in pytest.ini
pytest.param(..., marks=pytest.mark.ignore)  # WIP — excluded from default runs
```

## Credentials pattern

```python
# BAD — secret in dataprovider
pytest.param("9876543210", "123456", id="valid_user")

# GOOD — scenario key only; test reads settings
pytest.param("valid", id="valid_login")

# In test (login is mobile + OTP; these are fallback properties on Settings):
settings = get_settings()
user_logs_in_with_mobile_and_otp(
    page, settings.login_mobile_number, settings.login_otp
)
```

## Environment entity data is not test data

Secrets aren't the only thing that must stay out of a dataprovider. The **name
or id of an existing record on the target org** belongs in settings too:

```python
# BAD — breaks when the member is renamed, and can't target another env
pytest.param("Abheda", "100", id="quick_collect_link")

# GOOD — a FEATURE_* setting names the entity; the row carries only test values
pytest.param("100", id="TC-QC-001_create_link_for_single_payer")
# in the test:
payer = get_settings().feature_quick_collect_payer_name
```

Add the var to `Settings`, to `.env.example`, and skip the test with a clear
message when it is unset — a `KeyError` deep in a step is not a diagnosis.

Equally, do **not** substitute "whichever row is first" for real config: it
makes the test depend on unrelated org data and it silently passes against the
wrong record.

## Runtime data pattern

```python
# In test body, not dataprovider:
from datetime import datetime
title = f"Auto Group {datetime.now().strftime('%Y%m%d%H%M%S')}"
```

## Negative / permission matrix

```python
pytest.param("org_admin", True, id="org_admin_can_create"),
pytest.param("viewer", False, id="viewer_cannot_create"),
# Test asserts UI visible or forbidden message based on the bool
```

## Import path in the test

Dataproviders are imported as `dataprovider.dp_*`, **not**
`tests.dataprovider.dp_*` — `tests/conftest.py` adds `tests/` to `sys.path`:

```python
from dataprovider.dp_{feature} import get_{feature}_test_data
```

## Done when

- [ ] File at `tests/dataprovider/dp_{feature}.py`, function
      `get_{feature}_test_data()`
- [ ] Param order matches the test signature exactly
- [ ] Every row has an `id=`; ids mirror TC IDs where they exist
- [ ] No secrets, no `datetime.now()` / time-relative values at module level
- [ ] Imported in the test as `from dataprovider.dp_{feature} import ...`
- [ ] `invoke lint` passes; `pytest --collect-only --env dev -m "{feature}"`
      shows one collected item per row

## Self-check

Triggers: "add a dataprovider for the group-create scenarios", "parametrize
this login test over valid and invalid OTP", "add a role permission matrix for
members".
Does not trigger: "create the group-create page object"
(`scaffold-feature-automation`), "write the manual test cases first"
(`generate-test-cases`).
