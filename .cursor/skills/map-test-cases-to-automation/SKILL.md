---
name: map-test-cases-to-automation
description: >-
  Maps generated or existing test cases to the four-layer automation structure
  (PO, actions, steps, test, dataprovider). Use after generate-test-cases or
  when converting manual cases to pytest code.
---

# Map Test Cases to Automation

Conventions: [AGENTS.md](../../AGENTS.md). Use with `scaffold-feature-automation` to implement.

## Mapping table

| Test case part | Automation layer | Example |
|----------------|------------------|---------|
| Page elements | Page object | `btn_save`, `input_name` |
| Single UI interaction | Page action | `click_save_button()` |
| User-facing step | Step | `@allure.step("User saves form")` |
| Full scenario + assert | Test | `test_save_form_success` |
| Data variations | Dataprovider | `dp_checkout.py` parametrize |

## Workflow

1. **Group** test cases by page/feature
2. **Extract** shared steps → reusable step functions
3. **Extract** shared interactions → page actions (delegate, don't duplicate)
4. **Identify** parametrizable data → dataprovider rows
5. **Assign** markers: `@pytest.mark.e2e`, `p0/p1/p2`, feature tag
6. **Flag** parallel group if suites share org/state

## Test case → code traceability

```python
@allure.story("TC-LOGIN-001")  # link to test case ID
@pytest.mark.parametrize("scenario,expected", get_login_test_data())
def test_login_scenarios(self, page, scenario, expected):
    allure.dynamic.title(f"TC-LOGIN: {scenario}")
```

Dataprovider ids should mirror case IDs:

```python
pytest.param("valid_otp", "dashboard", id="TC-LOGIN-001")
pytest.param("invalid_otp", "Invalid OTP", id="TC-LOGIN-002")
```

## One test function per case or parametrize?

| Situation | Approach |
|-----------|----------|
| Same flow, different data | One test + `@pytest.mark.parametrize` |
| Different flows | Separate test functions |
| Different setup cost | Separate tests or fixtures |

## Layer violation check

Before implementing, verify:

- [ ] Test calls steps only (not actions/POs)
- [ ] Steps call actions only
- [ ] Actions use PO locators only
- [ ] Assertions in test or `assert_helper` — not in PO

## Non-automatable cases

Mark in dataprovider or skip file with `@pytest.mark.ignore` and comment:

```python
# TC-PAY-003: Real bank 3DS — manual only (external iframe)
```

## Deliverable

Provide a mapping doc:

| TC ID | Test function | Steps used | New PO locators needed | Dataprovider row |
|-------|---------------|------------|------------------------|------------------|
| TC-LOGIN-001 | `test_login_valid` | `user_logs_in_with_otp` | `input_mobile`, `btn_continue` | `valid_otp` |

Then run `scaffold-feature-automation` for missing files.
