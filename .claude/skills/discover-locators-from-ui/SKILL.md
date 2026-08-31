---
name: discover-locators-from-ui
description: >-
  Finds stable Playwright locators from the live UI or the app's frontend source
  and maps them to BasePage helpers before writing a page object. Use when
  starting a page object for a new screen, confirming placeholder selectors, or
  fixing a locator that broke after UI churn. Do NOT use to write the page
  object's actions or steps (see scaffold-feature-automation), and do NOT use
  to invent selectors when neither the live app nor its source is available —
  stop and say so instead.
---

# Discover Locators from UI

**Rule:** All `page.locator()` / `page.get_by_*()` calls live in `*_po.py` only. See [AGENTS.md](../../../AGENTS.md).

## Priority order — use the `BasePage` helpers only

Every locator must come from a helper on `src/core/base_page.py`. There is
**no `get_by_label` helper** — don't reach for it.

| # | Helper | Use for |
|---|--------|---------|
| 1 | `self.get_by_data_test_id("...")` | anything with a `data-testid` (values live in the app's `src/constants/testId.ts`) |
| 2 | `self.get_by_button("Continue")` | buttons — the shared `Button` renders `label` as accessible text, so role+name beats a testid here |
| 3 | `self.get_by_placeholder("...")` | text inputs — often the **only** stable signal on this app's `Input` |
| 4 | `self.get_by_text(MSG_CONST)` | static copy; import the string from `src/constants/messages.py`, don't inline it |
| 5 | `self.get_by_locator("css")` | last resort; comment why |

**Read [APP_CONTEXT.md](../../../APP_CONTEXT.md) → "Locator strategy notes"
before you start.** It records the per-component signals already discovered
(`Dropdown`, `RadioGroup`, `FileUpload`, `AuthSection`, `Checkbox`) — this
skill deliberately does not restate them.

## Workflow

### Option A — Live app (Playwright codegen or manual inspect)

1. Open target page in browser DevTools
2. For each interactive element, note: tag, role, label, test id, visible text
3. Prefer stable attributes over positional selectors (no `nth(3)` unless unavoidable)

### Option B — Frontend source

1. Find the React/Vue component for the page
2. Search for `data-testid`, `testId`, `aria-label`
3. Map component props to locator strategy

### Option C — The deployed JS bundle (when you have neither)

No app repo checked out, and no browser MCP connected? The **deployed bundle is source**.
This is how Quick Collect was mapped with no PRD, no Figma and no app repo.

`BASE_URL` is the app host for the target env (`get_settings().base_url` /
`.env.<env>`) — don't paste a literal host into the skill or a test:

```bash
curl -s "$BASE_URL/login" -o index.html
grep -oE 'src="/static/js/[^"]+"' index.html          # main bundle
curl -s "$BASE_URL/static/js/main.<hash>.js" -o main.js
```

What `main.js` reliably yields:

| Grep for | You get |
|---|---|
| `CREATE_LINK:"/…"` / route-constant objects | the **real route map** — beats guessing a path |
| `testId`-style nested objects | the full `data-testid` catalogue for the feature |
| `` `v1/…` `` template literals | API paths for setup/teardown and payload field names |
| `permissions:[…]` on nav entries | the permission that gates the screen |
| `label:"…"` / `placeholder:"…"` | exact button and input copy, for `messages.py` |

**Page components are usually in a lazy chunk, not `main.js`.** Follow the
route's dynamic import to the chunk id, resolve its hash from the chunk map,
then fetch just that chunk:

```bash
# main.js: {path:a.bf.CREATE_LINK, element:jsx(o)} where o = lazy(() => n.e(6049)…)
# then find 6049:"2b791fec" in the chunk map
curl -s "$BASE_URL/static/js/6049.2b791fec.chunk.js" -o page.js
```

Treat everything found this way as **confirmed for locators and routes**, but
still verify *behaviour* against the running app (Option A) — the bundle tells
you a string exists, not when it renders. See the trap below.

## PO naming (required prefixes)

| Element | Prefix | Example |
|---------|--------|---------|
| Button | `btn_` | `btn_submit` |
| Text input | `input_` | `input_email` |
| Checkbox | `chk_` | `chk_terms` |
| Dropdown | `ddl_` | `ddl_branch` |
| Error message | `msg_` | `msg_login_error` |
| Static label / title | `lbl_` | `lbl_section_title` |
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
| Email field | placeholder | `input_email` | `get_by_placeholder("Email")` |

## Trap: a locator that is always visible proves nothing

Before asserting "error X appears", confirm the element **actually changes
state**. Probe it both ways against the live app:

```python
for value in ["<invalid>", "<valid>"]:
    field.fill(value)
    print(value, error.is_visible(), cta.is_enabled())
```

If the "error" is visible for the valid value too, it is static helper text and
your negative test will pass on every input — including a broken app. Real
example: Quick Collect's "Allowed amount is between 2 and 200000" is permanent
`text-grey60` hint text that never turns red, and an `amountInput_error_message`
testid exists in the bundle but never renders. The only real signal is the
**CTA staying disabled**. Two negative tests passed for the wrong reason until
the boundary cases exposed it.

Corollary: when a form signals invalidity by gating its submit button, assert
enabled/disabled — and write the positive case too, or "always disabled" also
passes.

## Do not

- Invent selectors without seeing the UI or source — **stop and say so** if
  you have neither. Unconfirmed guesses ship `@pytest.mark.ignore`d and go in
  `README.md` → "Next steps" (see the Members example there).
- Put locators in actions, steps, or tests
- Use brittle selectors: `.css-abc123`, absolute XPath, index-only
- Call `page.get_by_*` directly — go through the `BasePage` helper

## Done when

- [ ] Locator map table delivered before any code was written
- [ ] Every locator uses a `BasePage` helper; none use `get_by_label`
- [ ] Names carry the right prefix (`btn_`/`input_`/`chk_`/`ddl_`/`msg_`/`tbl_`/`lnk_`/`lbl_`)
- [ ] Static copy comes from `src/constants/messages.py`
- [ ] Anything unconfirmed is labeled as such, not silently guessed
- [ ] New confirmed component-level signals added to `APP_CONTEXT.md` →
      "Locator strategy notes" so the next person doesn't rediscover them
- [ ] Any "error" locator probed with **valid** input too, so a static hint
      can't masquerade as a validation message

## Self-check

Triggers: "find the locators for the Members tab", "the group-create selectors
are guesses, confirm them against the live app", "this button locator broke
after the redesign".
Does not trigger: "write the group-create page object and steps"
(`scaffold-feature-automation`), "this test is flaky under 4 workers"
(`debug-flaky-e2e-test`).
