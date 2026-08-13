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

## Step 0 — required, not optional: sync context

Prefer running `get-context` first — it owns the two-tier model
(`APP_CONTEXT.md` index + living `context_docs/<slug>.md`). If that
already ran, skip to reading those files. If skipped, do the same inline:

1. Read [APP_CONTEXT.md](../../../APP_CONTEXT.md) for high-level data
   (section, Features row, cross-feature table).
2. Read `context_docs/<slug>.md` (via `Detail:` or slug match) — primary
   source for flows, gaps, and cross-feature impact. Don't re-derive it.
3. **Missing both?** Add a short `APP_CONTEXT.md` section **and** create
   `context_docs/<slug>.md` (`Status: discovery`) this turn — same rules
   as `get-context`. Domain facts from PRD/spec/app only; unknowns labeled.

This is what keeps context usable from discovery through later steps.

If any resulting test case is non-automatable or will ship
`@pytest.mark.ignore`d (missing test data, unconfirmed locators, etc.),
add it to `README.md` → "Next steps" too, same turn — same rule.

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

## Approval gate — required, not optional

1. Show the **full draft** of every test case in chat — no partial preview.
2. Wait for explicit user approval ("approved", "looks good", "go ahead" —
   not silence or an unrelated reply).
3. Only after approval are cases considered final. Don't hand anything to
   `map-test-cases-to-automation` before this gate clears.

## Next step

Once approved, hand off automatable cases to `map-test-cases-to-automation`
for layer mapping.
