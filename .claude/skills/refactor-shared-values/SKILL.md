---
name: refactor-shared-values
description: >-
  Changes a value shared across the suite — a constant in messages.py or
  routes.py, a Settings field, or a dataprovider id — by finding every consumer
  first and updating them atomically. Use when app copy changed, a route moved,
  a setting is renamed, or a constant needs a new value. Do NOT use to add a
  brand-new constant that has no consumers yet, and do NOT use a blind
  find-and-replace across the repo.
---

# Refactor Shared Values

Constants are imported *and* — despite the rule — sometimes copied. Changing the
definition updates the importers and silently strands the copies. Find both
before editing anything.

## Step 1 — Find every consumer

Search the **symbol and the literal value**. The symbol search finds the
importers; the value search finds the hardcoded copies that will not follow.

```bash
grep -rn "MSG_INVALID_OTP" --include="*.py" src tests        # importers
grep -rn "Invalid OTP" --include="*.py" --include="*.md" .   # copies + docs
```

Skipping the second search is how this goes wrong. A test that inlined the
string keeps asserting the old copy and passes against an app that no longer
shows it.

## Step 2 — Categorize each hit

| Consumer | Check | Action |
|---|---|---|
| `from src.constants... import X` | Nothing — follows automatically | Leave |
| Literal copy in a test or PO | Violates the import rule | Replace with the import |
| `context_docs/<slug>.md`, `APP_CONTEXT.md` | Records confirmed app behaviour | Update, note it changed |
| `.claude/skills/*/SKILL.md` | May cite the value in an example | Update — `test_skills_sync.py` checks symbols, not values |
| `.env.*.example` | Key must match `Settings` exactly | Update every env file |
| Dataprovider `id=` | Traceability link to a TC ID | Renaming breaks `-k` selection and report history |

## Step 3 — Change atomically

Definition and every consumer in **one commit**. A commit where `routes.py` has
moved and the POs have not is a broken tree that fails for a reason unrelated
to the change.

## Step 4 — Verify

```bash
invoke lint
grep -rn "<old value>" --include="*.py" src tests    # must return nothing
invoke test-files --env dev --args="tests/test/<area> -vv"
```

A `Settings` field rename additionally needs every `.env.*.example` updated and
`get_settings()` exercised, or the failure surfaces later as a missing-env skip
that looks like an unrelated config problem.

## Values confirmed from the app

Copy in `messages.py` and paths in `routes.py` mirror the running app. When
changing one because the app changed, **re-confirm against the app**, do not
retype from a ticket — use the `playwright` MCP (`browser_navigate` +
`browser_snapshot`) or `discover-locators-from-ui` -> Option C. `routes.py`
already carries provenance comments naming the bundle a path came from; keep
that habit.

## Do not

- Run a single global find-and-replace — it hits comments, docs, and unrelated
  substrings, and misses case variants
- Change a value to make a failing test pass before `diagnose-test-failure`
  has established whether the app or the test is wrong
- Leave `.env.*.example` behind on a `Settings` rename
- Split the change across commits

## Done when

- [ ] Both searches run — symbol and literal value
- [ ] Every hit categorized; hardcoded copies replaced with imports
- [ ] Docs, context docs, and skill files updated alongside code
- [ ] `.env.*.example` updated for any `Settings` change
- [ ] Grep for the old value returns nothing
- [ ] One commit; affected tests green

## Self-check

Triggers: "the OTP error copy changed, update it", "we renamed the groups
route", "rename FEATURE_GROUPS_NAME in settings".
Does not trigger: "add a constant for the new banner text" (just add it),
"this test is flaky" (`debug-flaky-e2e-test`).
