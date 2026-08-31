---
name: debug-flaky-e2e-test
description: >-
  Diagnoses and fixes intermittent E2E test failures using a structured
  checklist covering waits, locators, shared state, environment, and parallel
  execution. Use when a test passes locally but fails in CI, fails only under
  -n workers, or fails randomly across runs. Do NOT use for a test that fails
  every single time (that is a plain bug or a wrong locator — see
  discover-locators-from-ui), and do NOT use to add sleeps or bump timeouts as
  a first resort.
---

# Debug Flaky E2E Test

Do not fix flakiness with longer arbitrary sleeps. Follow this order.

## Diagnostic checklist

```
1. [ ] Re-run the failing test several times (no pytest-repeat in this repo —
      loop the invoke task):
      for i in 1 2 3 4 5; do invoke test --env dev --args="-k test_name"; done
2. [ ] Read Allure: screenshot, steps, which assertion failed
3. [ ] Check if failure is timing, locator, data, or environment
4. [ ] Check parallel group — shared org/state collision?
5. [ ] Apply targeted fix; re-run 10x before closing
```

## Common causes → fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Element not found | Locator changed or not yet rendered | Update PO; add `wait_for_element_visible()` |
| Timeout on navigation | Slow env | Raise `NAVIGATION_TIMEOUT_MS` in `.env.<env>` or `environment/<env>.properties` (loaded last, wins) — last resort, after ruling out a real wait |
| Stale element | DOM re-render | Re-query locator after action |
| Wrong data shown | Shared state / parallel race | Add `xdist_group`; unique runtime test data |
| Passes headed, fails headless | Viewport or animation | Set viewport in conftest; wait for spinner gone |
| Passes alone, fails in suite | Test order dependency | Remove shared mutable state; isolate fixtures |
| Random 401/redirect | Expired or **missing** storage state (conftest applies it silently only if the file exists) | Re-capture via `auth-storage-state-setup` |

## Start with the trace, not the code

A failing test writes `output/traces/<nodeid>.zip` (and attaches it to Allure).
Open it before reading a single line of the test:

```bash
playwright show-trace output/traces/<nodeid>.zip
```

It replays the run with a DOM snapshot per action, network activity and
per-action screenshots — which usually identifies the flake in under a minute
and saves you guessing from the checklist below. Traces are kept only for
failures, so a green run leaves nothing behind.

## Wait hierarchy (prefer top)

1. `expect(locator).to_have_text(...)` / the `assert_helper` wrappers —
   web-first, retry until the deadline. Prefer these to any manual wait.
2. `self.wait_for_element_visible(locator)` — `src/core/page_actions.py`
3. `assert_url_contains(page, path)` — `src/core/assert_helper.py`
4. Fixed `time.sleep()` — **banned in UI code** and enforced by
   `tests/test/core/test_layer_boundaries.py`. API polling is the one
   exception and belongs in `src/core/api_client.py`.

These are `PageActions` methods, so they are available as `self.*` in the
actions layer — not in steps or tests.

## Parallel debugging

```bash
invoke test --env dev --parallel 4 --args="-k test_name"
```

`--parallel N` adds `-n N --dist loadgroup` (`tasks.py`), so `xdist_group`
markers are respected — plain `-n N` without `--dist loadgroup` would break
them.

If only fails under `-n 4`: assign or fix `pytestmark = pytest.mark.xdist_group(...)`.

## Locator debugging

Run headed (this repo uses `--headless false`, not Playwright's `--headed`;
add `-s` yourself if you want print output — it is not in `pytest.ini`):

```bash
invoke test --env dev --args="--headless false -vv -s -k test_name"
invoke test-files --env dev --args="--headless false -vv"   # per-file reports
```

## Artifacts already captured for you

`pytest_runtest_makereport` in `tests/conftest.py` attaches failure artifacts
via `src/core/failure_artifacts.py` automatically — check `output/` and the
Allure report before adding manual instrumentation.

## Data debugging

- Attach `page.url`, visible text, API response to Allure
- Verify test uses runtime-generated unique names (not colliding with prior run)

## When to mark `ignore`

If root cause is external (3rd-party downtime, no test OTP hook) — mark
`@pytest.mark.ignore` with a ticket link, don't leave flaky in the default
suite. `invoke test` defaults to `-m "not ignore"`. If that leaves the whole
feature ignored, add it to `README.md` → "Next steps" — `tests/test/core/
test_readme_sync.py` fails otherwise.

## Done when

- [ ] Root cause named (timing / locator / data / env / parallel) — not guessed
- [ ] Fix is a targeted wait, locator, or isolation change — no new `time.sleep`
- [ ] Test re-run 10x green via the loop above
- [ ] Ran once with `--parallel 4` if the suite shares org/branch state
- [ ] `invoke lint` passes

## Self-check

Triggers: "this login test passes locally but fails in CI", "test_group_create
is flaky", "only fails when I run with 4 workers".
Does not trigger: "this test has never passed" (real bug / unconfirmed
locators), "add a new test for group deletion" (`scaffold-feature-automation`).
