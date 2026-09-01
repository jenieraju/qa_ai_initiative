---
name: get-context
description: >-
  Gathers feature context from APP_CONTEXT.md and context_docs/ before
  automating a flow. Use when starting automation for a new feature or the
  next step of an already-automated flow, or when asked to "get context for
  X". Do NOT use to write test cases (see generate-test-cases).
---

# Get Context

**Single owner** for creating and updating `APP_CONTEXT.md` index entries and
`context_docs/<slug>.md`. Other skills (`generate-test-cases`,
`scaffold-feature-automation`, `extend-feature-automation`) **read** these files
— they do not recreate context inline.

Second step of the new-feature pipeline (after `create-feature-branch`, before
`generate-test-cases`). No Figma or Jira MCP is configured — those artifacts
arrive as pasted text, a link, or an uploaded screenshot. Two browser MCPs
are configured in `.mcp.json` — use `playwright` (`browser_navigate` +
`browser_snapshot`) to see the live screen, `chrome-devtools`
(`list_network_requests`) to capture the API calls a flow really makes. Read
[AGENTS.md](../../../AGENTS.md) and `APP_CONTEXT.md`'s "Writing new tests" first.

## Long-run model (two tiers)

| Source | Job | When written |
|--------|-----|--------------|
| `APP_CONTEXT.md` | Always-on **index**: domain, Features table, cross-feature links, short `##` sketch | Every turn agents may read it — keep it lean |
| `context_docs/<slug>.md` | Living **feature record**: flow, AC gaps, coverage, locators, quirks | Created at **get-context**; enriched after automation; updated on every later step |

Do **not** wait until automation exists to create the context doc — test-case
design needs it. Do **not** dump locator essays into `APP_CONTEXT.md`.

Never invent facts. Label gaps `[Assumption]` or
`[Unknown — needs confirmation]`. Reuse the `create-feature-branch` slug
(`feature/<slug>`) for the `APP_CONTEXT.md` heading, `Detail:` link, and
`context_docs/<slug>.md` filename.

## 1. Read APP_CONTEXT.md first

Use related high-level data (Features table, domain, cross-feature table,
existing `##` section). Do not re-derive what is already written.

## 2. Match context_docs/<slug>.md

Aliases: `login` / `onboarding` → `authentication-onboarding`.

**New flow** (no file yet):
1. Ask only for artifacts not already in chat: PRD/doc, Figma (link or
   screenshot), Jira AC, manual cases.
2. Infer from `src/page_objects/`, `src/steps/`, `tests/`, and
   `APP_CONTEXT.md`. Interview only gaps that block test design.
3. Add/extend a **short** `## <Feature Name>` in `APP_CONTEXT.md` (one
   paragraph + route sketch + `Detail: context_docs/<slug>.md`). Update the
   cross-feature table if a listed entity is mutated.
4. **Create** `context_docs/<slug>.md` with `Status: discovery` using the
   template below.

**Existing flow** (file exists — next step or re-run):
1. Read `APP_CONTEXT.md`, follow `Detail:` into the context doc.
2. Use that file as source of truth; only fill gaps for the *new* step.
3. After the new step is designed/automated, **update the same file** —
   never a second doc for the same slug.

## 3. Cross-checks (both branches)

- Grep `src/page_objects/`, `src/steps/`, `tests/test/` for coverage.
- If this feature creates/edits/deletes a cross-feature entity (member,
  group, branch, payment link, team role), record it under **Cross-feature
  impact** in the context doc and in `APP_CONTEXT.md`'s table — later test
  cases must cover cascade/block/orphan.

## 4. Enrich after automation

When four layers exist and `run-and-verify-tests` passes (see that skill):
- Set `Status:` to `partially-automated` or `automated` in the context doc
- Fill **Coverage** (PO/test paths) and confirmed session/teardown notes
- Keep `APP_CONTEXT.md` high-level; detail stays in the context doc only

Do not set `Status: automated` from scaffold alone — only after a green verify run.

## Template — context_docs/<slug>.md

Keep this lean. Do not copy a 300-line discovery dump.

```markdown
# {Feature Name}

Status: discovery | partially-automated | automated

## Summary
{What it does — sourced from PRD/Jira/Figma/app, never invented.}

## Flow
{ASCII routes if multi-step.}

## Coverage
- Already automated: {paths, or "none yet"}
- Not yet covered: {known gaps}

## Cross-feature impact
{Entities touched + cascade/block/orphan unknowns, or "none"}

## Confirmed locators

{Empty at discovery — fill via discover-locators-from-ui before scaffold.
Table format: | UI element | Strategy | PO attribute | Value |}

## Notes
- {Confirmed quirks}
- {Unconfirmed — "[Assumption]" / "[Unknown — needs confirmation]"}
```

## Done when

- [ ] `APP_CONTEXT.md` read; high-level reused, not re-derived
- [ ] `context_docs/` checked for `<slug>.md`
- [ ] New flow: short `APP_CONTEXT.md` section + **new** context doc
      (`Status: discovery`) + `Detail:` link
- [ ] Existing flow: matching context doc read and used
- [ ] After automation: same context doc enriched; Status updated
- [ ] Cross-feature table/section updated if needed
- [ ] Every unconfirmed fact labeled
- [ ] New context doc includes empty `## Confirmed locators` placeholder
- [ ] Reported: "Context: `APP_CONTEXT.md` → '<Feature>' +
      `context_docs/<slug>.md` (Status: …). Next: generate-test-cases."

## Self-check

Triggers: "get context for custom user role", "automate the next groups
wizard step", "here's the PRD for payment-link, get context".
Does not trigger: "write test cases for login" (`generate-test-cases`),
"why is this test flaky" (`debug-flaky-e2e-test`), "this test broke after the
release" (`diagnose-test-failure`, which triages then routes to
`discover-locators-from-ui` for UI/locator drift).
