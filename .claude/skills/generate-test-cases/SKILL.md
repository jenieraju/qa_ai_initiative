---
name: generate-test-cases
description: >-
  Generates structured manual/E2E test cases (TC-IDs, priority, steps, expected
  results) from requirements, user stories, or acceptance criteria, then waits
  for approval. Use when planning coverage, reviewing a feature spec, or asked
  to "write test cases" for a feature. Do NOT use to write automation code or
  map cases to layers (map-test-cases-to-automation), and do NOT use to gather
  the feature context itself (get-context).
---

# Generate Test Cases

Produces **test case documents** first — automation comes later via `map-test-cases-to-automation`.

## Inputs

- Feature name and description
- Acceptance criteria, user story, or spec (paste or file path)
- User roles / personas (if RBAC)
- Environments (dev, staging, etc.)

## Step 0 — required, not optional: sync context

1. Read [APP_CONTEXT.md](../../../APP_CONTEXT.md) — section, Features row,
   cross-feature table.
2. Read `context_docs/<slug>.md` (via `Detail:` or slug match) — the primary
   source for flows, gaps and cross-feature impact. Don't re-derive it.
3. **Either file missing?** Run `get-context` — it owns creating them and the
   rules for doing it. Don't reproduce that work here: two copies of the same
   instructions is exactly the drift `.claude/skills/README.md` warns about.

Test-case design without a context doc is guesswork, so this is a gate, not a
suggestion.

## Output format

For each test case:

```markdown
### TC-{FEATURE}-{NNN}: {Short title}

| Field | Value |
|-------|-------|
| Priority | P0 / P1 / P2 |
| Type | Happy path / Negative / Edge / Permission |
| Precondition | Logged in as X, data Y exists |
| Steps | 1. ... 2. ... 3. ... |
| Expected result | ... |
| Test data | Field values (no real secrets) |
| Automatable | Yes / No / Partial — reason |
| Markers | e2e, p0, {feature} |
```

## Coverage checklist

Generate cases across these categories:

```
- [ ] Happy path — primary user journey end-to-end
- [ ] Negative — invalid input, empty fields, wrong credentials
- [ ] Boundary — min/max length, limits, empty lists
- [ ] Permission — role without access sees blocked/hidden UI
- [ ] State — draft vs published, active vs inactive
- [ ] Navigation — deep links, back button, refresh
- [ ] Error handling — API failure, timeout, toast/message text
- [ ] Empty state — no data yet, first-time user
- [ ] Cross-feature impact — if this feature creates/edits/deletes an
      entity in APP_CONTEXT.md's "Cross-feature relationships" table
      (member, group, branch, payment link, team role), write explicit
      cases for what happens to each dependent — cascade, block, or
      orphan. Do not skip this category just because the PRD didn't
      mention it; that silence is exactly what causes production bugs.
```

## Priority guide

| Priority | Criteria |
|----------|----------|
| **P0** | Revenue/critical path, login, payment, data loss risk |
| **P1** | Core feature flows, common user actions |
| **P2** | Edge cases, cosmetic, low-traffic paths |

## Rules

- One logical assertion focus per test case (split compound scenarios)
- Steps written as **user actions** ("User clicks Save") — matches steps layer naming
- Flag **non-automatable** cases (CAPTCHA, 3rd-party SMS OTP without test hook)
- Note **shared mutable state** (same org/branch) for parallel group planning
- Do not embed real passwords or API keys in test data
- Any case that is non-automatable or will ship `@pytest.mark.ignore`d
  (missing test data, unconfirmed locators) goes in `README.md` → "Next
  steps" in the same turn — `tests/test/core/test_readme_sync.py` fails
  otherwise

## Example (abbreviated)

```markdown
### TC-LOGIN-001: Valid mobile + OTP login

| Field | Value |
|-------|-------|
| Priority | P0 |
| Type | Happy path |
| Precondition | Valid test mobile whitelisted in env |
| Steps | 1. Open /login 2. Enter mobile 3. Accept T&C 4. Submit 5. Enter OTP 6. Submit |
| Expected result | Redirect to dashboard; user menu visible |
| Automatable | Yes |
| Markers | e2e, p0, login |
```

## Approval gate — required, not optional

1. Show the **full draft** of every test case in chat — no partial preview.
2. Wait for explicit user approval ("approved", "looks good", "go ahead" —
   not silence or an unrelated reply).
3. Only after approval are cases considered final. Don't hand anything to
   `map-test-cases-to-automation` before this gate clears.

## Next step

Once approved, hand off automatable cases to `map-test-cases-to-automation`
for layer mapping.

## Done when

- [ ] `APP_CONTEXT.md` + `context_docs/<slug>.md` read (or created) first
- [ ] Every coverage-checklist category addressed or explicitly ruled out
- [ ] Cross-feature impact cases written for every entity this feature mutates
- [ ] Each case has a TC ID, priority, `Automatable`, and markers
- [ ] No real credentials or API keys in test data
- [ ] Full draft shown in chat and **explicitly approved** before handoff
- [ ] Non-automatable / to-be-ignored cases added to `README.md` → "Next steps"

## Self-check

Triggers: "write test cases for the payment-link feature", "here's the PRD,
what should we cover", "generate P0 cases for group creation".
Does not trigger: "get context for custom user role" (`get-context`), "turn
these cases into pytest files" (`map-test-cases-to-automation`).
