---
name: generate-test-cases
description: >-
  Generates structured manual/E2E test cases from requirements, user stories, or
  acceptance criteria before writing automation code. Use when planning coverage,
  reviewing a feature spec, or asked to write test cases.
---

# Generate Test Cases

Produces **test case documents** first — automation comes later via `map-test-cases-to-automation`.

## Inputs

- Feature name and description
- Acceptance criteria, user story, or spec (paste or file path)
- User roles / personas (if RBAC)
- Environments (dev, staging, etc.)

## Step 0 — required, not optional: sync APP_CONTEXT.md

Before producing any test case, check whether the feature already has a
section in [APP_CONTEXT.md](../../../APP_CONTEXT.md).

- **Missing or incomplete?** Add/extend its section in the same turn you
  generate test cases — don't ask the user whether to do this, don't defer
  it to a follow-up, don't just note the gap. Domain facts come from the
  PRD/spec and the app's real source only; anything not confirmed yet gets
  flagged explicitly in the file (see "Members" there for the pattern),
  never stated as settled fact.
- **Already documented?** Read it, don't re-derive it.

This is what keeps `APP_CONTEXT.md` a live reference instead of drifting
behind automation — it only works if it happens automatically, every time,
not as an occasional manual cleanup.

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

## Next step

Hand off automatable cases to `map-test-cases-to-automation` for layer mapping.
