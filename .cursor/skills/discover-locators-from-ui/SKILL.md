---
name: discover-locators-from-ui
description: >-
  Finds stable Playwright locators from live UI or frontend source before writing
  page objects. Use when starting a new page, fixing broken tests, or before
  scaffold-feature-automation.
---

# Discover Locators from UI

**Rule:** All `page.locator()` / `page.get_by_*()` calls live in `*_po.py` only. See [AGENTS.md](../../AGENTS.md).

## Priority order

1. `data-testid` / `data-test-id` (check frontend `testId` constants if available)
2. `get_by_role("button", name="...")` with accessible name
3. `get_by_label("...")` for form fields
4. `get_by_text("...", exact=True)` for static copy
5. CSS/XPath — last resort; document why

## Workflow

### Option A — Live app (Playwright codegen or manual inspect)

1. Open target page in browser DevTools
2. For each interactive element, note: tag, role, label, test id, visible text
3. Prefer stable attributes over positional selectors (no `nth(3)` unless unavoidable)

### Option B — Frontend source

1. Find the React/Vue component for the page
2. Search for `data-testid`, `testId`, `aria-label`
3. Map component props to locator strategy

## PO naming (required prefixes)

| Element | Prefix | Example |
|---------|--------|---------|
| Button | `btn_` | `btn_submit` |
| Text input | `input_` | `input_email` |
| Checkbox | `chk_` | `chk_terms` |
| Dropdown | `ddl_` | `ddl_branch` |
| Error message | `msg_` | `msg_login_error` |
| Table | `tbl_` | `tbl_orders` |
| Link | `lnk_` | `lnk_forgot_password` |

## Dynamic elements

Use `_loc_*()` helpers in the PO:

```python
def _loc_row_by_name(self, name: str) -> Locator:
    return self.tbl_items.filter(has_text=name)
```

## Output template

Deliver a locator map before coding:

| UI element | Strategy | PO attribute | Value |
|------------|----------|--------------|-------|
| Login button | testid | `btn_login` | `login-submit` |
| Email field | label | `input_email` | `get_by_label("Email")` |

## Do not

- Invent selectors without seeing the UI or source
- Put locators in actions, steps, or tests
- Use brittle selectors: `.css-abc123`, absolute XPath, index-only
