---
name: map-test-cases-to-automation
description: >-
  Maps generated or existing test cases to the four-layer automation structure
  (PO, actions, steps, test, dataprovider) and produces a TC-ID → code
  traceability table. Use when approved test cases need mapping to layers,
  when converting manual cases to pytest, or when asked which layer a case or
  assertion belongs in. Do NOT use to
  write the test cases themselves (generate-test-cases) or to create the files
  (scaffold-feature-automation).
---

# Map Test Cases to Automation

Conventions: [AGENTS.md](../../../AGENTS.md). Use with `scaffold-feature-automation` to implement.

## Mapping table

| Test case part | Automation layer | Example |
|----------------|------------------|---------|
| Page elements | Page object | `btn_save`, `input_name` |
| Single UI interaction | Page action | `click_save_button()` |
| Expected result **on a screen** | Page action, via `assert_helper` | `verify_login_page_visible()` |
| User-facing step | Step | `@allure.step("User saves form")` |
| Screen check, exposed to tests | Step | `user_verifies_login_page_is_displayed()` |
| Expected result **about the flow** | Test | `assert_url_contains(page, GROUPS_PATH)` |
| Full scenario orchestration | Test | `test_save_form_success` |
| Data variations | Dataprovider | `dp_checkout.py` parametrize |

Screen-level vs flow-level is the whole rule — see `AGENTS.md` → Architecture.
Don't assert the same thing at two layers.

## Workflow

1. **Group** test cases by page/feature
2. **Extract** shared steps → reusable step functions
3. **Extract** shared interactions → page actions (delegate, don't duplicate)
4. **Identify** parametrizable data → dataprovider rows
5. **Assign** markers: `@pytest.mark.e2e`, `p0/p1/p2`, feature tag
6. **Flag** parallel group if suites share org/state

## Test case → code traceability

**One convention: the dataprovider `id=` is the canonical link.** It shows up in
the node id, in Allure, in JUnit XML, and it is selectable with `-k`, so a TC ID
can always be found the same way:

```python
pytest.param("100", id="TC-QC-001_create_link_for_single_payer")
```

```bash
pytest -k TC-QC-001        # run exactly that case
```

For a test with no parametrize, name the TCs in the **docstring's first line**.

Do **not** put TC IDs in `allure.story` — story is the human-readable scenario
grouping in the report ("Create payment link — single payer"), and overloading
it with ids makes the report unreadable while duplicating the id in a second
place that can drift.

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
- [ ] Assertions go through `src/core/assert_helper.py`. Screen-level checks
      ("page shows X") live in the **actions** layer as `verify_*` methods
      (see `verify_login_page_visible` in `src/page_actions/login_actions.py`);
      flow-level outcomes (final URL, saved session) may assert in the test.
      Never in a page object.

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

## Done when

- [ ] Every automatable TC ID appears in the mapping table
- [ ] Non-automatable cases marked `@pytest.mark.ignore` with the TC ID in a
      comment, and listed in `README.md` → "Next steps"
- [ ] Layer-violation checklist above passes for the plan
- [ ] Dataprovider ids mirror TC IDs
- [ ] Parallel group named if the suite shares org/branch state

## Self-check

Triggers: "map these approved test cases to the layers", "turn TC-LOGIN-001..
005 into pytest structure", "which layer should this assertion live in".
Does not trigger: "write test cases for the payment flow"
(`generate-test-cases`), "create the page object files"
(`scaffold-feature-automation`).
