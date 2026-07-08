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
