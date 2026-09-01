---
name: diagnose-test-failure
description: >-
  Triages a failing test to the right owner — locator drift, app bug, or
  flakiness — before anyone edits code. Use when a test fails consistently,
  fails after a release, or has never passed since scaffold. Do NOT use for a
  test that passes locally and fails only under -n workers or randomly across
  runs (debug-flaky-e2e-test owns that), and do NOT use to change an assertion
  so it matches current behaviour before establishing which side is wrong.
---

# Diagnose Test Failure

Entry point for **every** red test. It classifies, then hands off. Fixing a
symptom before classifying is how a real app bug gets absorbed into the suite
as a "fixed" test.

**Never change an assertion to match current behaviour** until you know whether
the app or the test is wrong.

## Step 1 — Read the trace before the code

```bash
invoke test-files --env dev --args="tests/test/<area>/test_<feature>.py -vv"
playwright show-trace output/traces/<trace>.zip
```

The trace answers "what did the page actually look like" faster than reading a
page object will. Screenshots and traces are captured by
`src/core/failure_artifacts.py`.

## Step 2 — Classify

| Symptom | Diagnosis | Route to |
|---|---|---|
| Passed before, now fails every run since a release | **Locator/UI drift** | `discover-locators-from-ui`, then `write-page-object` |
| Never passed since scaffold | **Placeholder locators** | `discover-locators-from-ui`; keep `@pytest.mark.ignore` until green |
| Passes locally, fails under `--parallel` or randomly | **Flakiness** | `debug-flaky-e2e-test` |
| Fails at login / redirects to `/login` | **Auth state** | `auth-storage-state-setup` — check `auth_state_exists` first |
| Locators confirmed correct, app genuinely behaves differently | **App bug or app drift** | Report it. Do not "fix" the test |
| Negative test passes on valid input too | **Static-hint trap** | `discover-locators-from-ui` -> the always-visible trap |
| Fails only after another test ran | **Missing teardown** | `test-data-teardown` |

## Step 3 — Confirm against the live app

Locator drift and app-bug diagnoses must be confirmed against the running app,
not inferred from the diff. Use the browser MCP:

- `playwright` MCP — `browser_navigate`, `browser_snapshot`. The a11y snapshot
  tells you whether the element still exists and under what role/name.
- `chrome-devtools` MCP — `list_network_requests` when the UI renders but the
  data is wrong; the failure is often a 4xx behind an intact screen.

Session auth comes from `.auth/default.json` (see `.mcp.json`). If it has
expired, refresh it via `auth-storage-state-setup` rather than logging in by
hand — the OTP flow cannot be driven unattended.

No MCP connected and no app repo? Fall back to
`discover-locators-from-ui` -> Option C (bundle as source).

## App drift is a valid outcome

If the app changed deliberately and the test encoded the old behaviour, the fix
is not in the test file alone: update the context doc, `routes.py`, and
`messages.py` to match — see `refactor-shared-values` for the cascade — and
record it in `README.md` -> "Next steps" if it stays unautomated.

Live example: individual onboarding now routes to `SELECT_CATEGORY_PATH`, added
app-side after the suite was written. That is drift to absorb deliberately, not
a locator to patch.

## Do not

- Add `time.sleep` or raise a timeout to make red go green — banned, and
  `tests/test/core/test_layer_boundaries.py` catches it
- Loosen an assertion, or `@pytest.mark.ignore` a test, without a comment
  saying which app behaviour it is waiting on
- Fix in the test what belongs in the page object or `messages.py`
- Declare it fixed off one green run — see `run-and-verify-tests`

## Done when

- [ ] Trace read before any file was edited
- [ ] Failure classified against the table, and the owning skill named
- [ ] Diagnosis confirmed against the live app or the bundle, not guessed
- [ ] Fix applied at the layer that owns it
- [ ] App bugs reported rather than absorbed; any skip carries a reason
- [ ] `run-and-verify-tests` green

## Self-check

Triggers: "this test broke after the release", "test_individual_onboarding
fails every run", "the members tests have never passed, what's wrong".
Does not trigger: "this passes locally but fails under 4 workers"
(`debug-flaky-e2e-test`), "find the locators for the Members tab"
(`discover-locators-from-ui`).
