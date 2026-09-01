---
name: write-page-object
description: >-
  Structures a src/page_objects/*_po.py file once locators are confirmed —
  section order, feedback locators, dynamic _loc_* helpers, and when to split
  or share a page object. Use when creating a new PO, adding locators to an
  existing one, or deciding whether a screen needs its own PO. Do NOT use to
  find or confirm the locators themselves (discover-locators-from-ui), and do
  NOT use to write actions, steps, or tests (scaffold-feature-automation).
---

# Write Page Object

**Prerequisite:** `discover-locators-from-ui` has delivered a locator map and
filled `## Confirmed locators` in the context doc. Never open this skill with
unconfirmed selectors — a PO of guesses is what `@pytest.mark.ignore` exists to
quarantine, not a starting point.

**Rule:** every `page.locator()` / `page.get_by_*()` call in the repo lives in a
`*_po.py` and reaches the page through a `BasePage` helper. See
[AGENTS.md](../../../AGENTS.md).

## Section order (required)

Mirror `src/page_objects/login_po.py`. A PO is locators only — no waits, no
assertions, no business logic.

```python
class GroupCreatePage(BasePage):
    """Page object for the group-create screen."""

    def __init__(self, page) -> None:
        super().__init__(page)

        # --- Locators: shared chrome ---
        self.lbl_section_title = self.get_by_data_test_id("groupCreate_title")

        # --- Locators: interactive ---
        self.input_group_name = self.get_by_placeholder("Enter group name")
        self.btn_submit = self.get_by_button("Create")

        # --- Locators: feedback ---
        self.msg_name_error = self.get_by_data_test_id("groupName_error_message")
```

| Section | Holds | Comment header |
|---|---|---|
| 1. Shared chrome | Title, description, nav common to the route's states | `# --- Locators: shared chrome ---` |
| 2. Interactive | Inputs, buttons, checkboxes, dropdowns | `# --- Locators: interactive ---` |
| 3. Feedback | Success, error, validation, empty state | `# --- Locators: feedback ---` |

## Feedback locators are not optional

A PO for a form or CRUD screen with **zero feedback locators is incomplete** —
it can only express happy paths, so the negative cases in your approved test
cases have nothing to assert against.

Before finishing, confirm each exists or is recorded as absent-by-design:
success signal, field validation, form-level error, empty state.

**Then probe them.** `discover-locators-from-ui` -> "a locator that is always
visible proves nothing" applies at write time: if a feedback locator is static
hint text, the real signal is usually the **CTA disabled state**. Capture that
instead, and say so in a comment.

## Dynamic elements

Never store a locator that depends on runtime data as an attribute — expose a
`_loc_*()` method so the caller passes the value:

```python
def _loc_row_by_name(self, name: str) -> Locator:
    return self.tbl_members.filter(has_text=name)
```

## One PO per route, not per state

`login_po.py` holds **both** the mobile-entry and OTP states because they share
one route (`LOGIN_PATH`). Split only when the route changes.

| Situation | Do |
|---|---|
| Two states, one route (wizard step, modal over a page) | One PO, separate comment sections per state |
| Two routes | Two POs, even if the screens look alike |
| Chrome repeated across screens (nav, header) | Keep it per-PO; extract only when a third PO needs it |
| Route in `routes.py` with no PO | Create the PO; import the constant, never a literal path |

## Do not

- Add waits, `expect`, or `assert` to a PO — those belong in actions
  (`verify_*`) or the test, via `assert_helper`
- Call `page.get_by_*` directly — go through the `BasePage` helper
- Inline copy — import from `src/constants/messages.py`
- Inline a route string — import from `src/constants/routes.py`
- Reach for it: there is no `get_by_label` helper on `BasePage`

## Done when

- [ ] Sections present and in order, with the comment headers above
- [ ] Feedback locators exist, or their absence is justified in the docstring
- [ ] Every "error" locator probed with valid input too (static-hint trap)
- [ ] Dynamic elements are `_loc_*()` methods, not attributes
- [ ] Prefixes match `discover-locators-from-ui`; copy and routes imported
- [ ] Module docstring names the route(s) and states the PO covers
- [ ] `invoke lint` clean; `tests/test/core/test_layer_boundaries.py` passes

## Self-check

Triggers: "write the page object for group create", "add the OTP locators to
the login PO", "should members list and members add share a page object".
Does not trigger: "find the locators for the Members tab"
(`discover-locators-from-ui`), "write the group-create steps and test"
(`scaffold-feature-automation`).
