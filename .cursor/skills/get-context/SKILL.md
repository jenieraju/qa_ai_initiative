---
name: get-context
description: >-
  Gathers and documents feature context from a PRD/doc, Figma link or
  screenshot, and/or Jira ticket, before any test cases are written. Use when
  starting automation for a new feature, enhancement, or bug fix and
  APP_CONTEXT.md doesn't yet cover it, or when asked to "get context for X".
  Do NOT use to write test cases (see generate-test-cases) or when the
  feature is already fully documented in APP_CONTEXT.md.
---

# Get Context

Second step of the new-feature pipeline (after `create-feature-branch`, before
`generate-test-cases`). No Figma/Jira/Playwright MCP is configured in this
repo — every artifact comes in as pasted text, a link, or an uploaded
screenshot, never a live API call. Read [AGENTS.md](../../AGENTS.md) and
`APP_CONTEXT.md`'s "Writing new tests" section first — that section is the
required output shape and the reason this skill updates `APP_CONTEXT.md`
directly instead of writing a separate context file per feature ("no
separate per-feature context files... single section in *this* file").

## Core rules

1. **Never block on missing artifacts.** No PRD/Figma/Jira? Infer from
   `src/page_objects/`, `src/steps/`, existing `tests/`, and
   `APP_CONTEXT.md`, then interview the user only for the gaps that actually
   block test design.
2. **No hallucination.** Confirmed facts only; unconfirmed ones are labeled
   `[Assumption]`, missing ones `[Unknown — needs confirmation]` — the same
   pattern already used for "Members" in `APP_CONTEXT.md`.
3. **Reuse the slug** from `create-feature-branch` (branch `feature/<slug>`)
   for the new `## <Feature Name>` heading — don't invent a different one.
4. **One section, no new files.** Output is always an addition/edit to
   `APP_CONTEXT.md`, written in the same turn — never a `.context/*.md` file.

## Workflow

1. **Ask what's available**, one question each, only for artifacts not yet
   pasted in chat:
   - PRD / doc (paste text or link)
   - Figma (link, or paste/upload a screenshot — read it directly, no MCP)
   - Jira ticket (paste the description/AC, or a link)
   - Existing manual test cases, if any
2. **Check `APP_CONTEXT.md` first.** If the feature already has a section (or
   a row in "Features"), read it — don't re-derive what's already there; this
   run only fills gaps.
3. **Cross-check code.** Grep `src/page_objects/`, `src/steps/`,
   `tests/test/` for anything already automated for this area; note routes,
   locator patterns (see "Locator strategy notes" in `APP_CONTEXT.md`), and
   existing coverage.
4. **Cross-feature check.** If this feature creates/edits/deletes an entity
   listed in `APP_CONTEXT.md`'s "Cross-feature relationships" table (member,
   group, branch, payment link, team role), flag it explicitly — it must be
   covered in test cases later, not just the happy path.
5. **Gap interview.** Ask only about unknowns that block test design: roles
   or permission gates, exact routes, required fields/validation rules,
   whether the flow is reachable from more than one entry point.
6. **Write the section** into `APP_CONTEXT.md`: what the feature does, real
   flow/routes (ASCII flow like "Authentication & onboarding flow" above),
   any field/locator quirks, and every unresolved item labeled per rule 2.
   If this feature mutates a cross-feature entity, update that table row too
   (step 4).

## Output shape (mirror existing sections)

```markdown
## {Feature Name}

{What it does — one paragraph, sourced from the PRD/Jira/Figma or app source,
never invented.}

{Route/flow, ASCII diagram if multi-step.}

Notes:
- {Field/locator quirks, confirmed facts}
- {Unconfirmed items — "[Assumption]" or "[Unknown — needs confirmation]"}
```

## Done when

- [ ] `APP_CONTEXT.md` has a `## <Feature Name>` section (new or extended),
      written in the same turn
- [ ] Every unconfirmed fact is labeled, none stated as settled without a
      source
- [ ] "Cross-feature relationships" table updated if this feature touches a
      listed entity
- [ ] No separate `.context/*.md` file was created
- [ ] Reported to the user: "Context added to `APP_CONTEXT.md` → '<Feature
      Name>'. Next: generate-test-cases for this feature."

## Self-check

Triggers: "get context for custom user role", "here's the PRD/Figma for the
disable-payment-link feature, get context", "I have a Jira ticket for a new
feature, help me understand it before we write tests".
Does not trigger: "write test cases for login" (skip straight to
`generate-test-cases` if `APP_CONTEXT.md` already covers it), "why is this
test flaky" (`debug-flaky-e2e-test`).
