---
name: create-dataprovider
description: >-
  Creates tests/dataprovider/dp_*.py files with pytest.param rows for data-driven
  E2E tests. Use when parametrizing scenarios, negative cases, or role matrices.
---

# Create Dataprovider

Rules from [AGENTS.md](../../AGENTS.md):

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
pytest.param(..., marks=[pytest.mark.p0, pytest.mark.smoke])
pytest.param(..., marks=pytest.mark.ignore)  # WIP — excluded from default runs
```

## Credentials pattern

```python
# BAD — secret in dataprovider
pytest.param("user@test.com", "password123", id="valid_user")

# GOOD — scenario key only; test reads settings
pytest.param("valid_admin", id="valid_admin")

# In test:
settings = get_settings()
user_logs_in(page, settings.login_user_email, settings.login_user_password)
```

## Runtime data pattern

```python
# In test body, not dataprovider:
from datetime import datetime
title = f"Auto Group {datetime.now().strftime('%Y%m%d%H%M%S')}"
```

## Negative / permission matrix

```python
@pytest.param("org_admin", True, id="org_admin_can_create")
@pytest.param("viewer", False, id="viewer_cannot_create")
# Test asserts UI visible or forbidden message based on bool
```
