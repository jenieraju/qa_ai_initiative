---
name: debug-flaky-e2e-test
description: >-
  Diagnoses and fixes intermittent E2E test failures using a structured checklist
  covering waits, locators, shared state, environment, and parallel execution.
  Use when a test passes locally but fails in CI, or fails randomly.
---

# Debug Flaky E2E Test

Do not fix flakiness with longer arbitrary sleeps. Follow this order.

## Diagnostic checklist

```
1. [ ] Re-run failed test 5x locally: pytest -k "test_name" --count=5 (or loop)
2. [ ] Read Allure: screenshot, steps, which assertion failed
3. [ ] Check if failure is timing, locator, data, or environment
4. [ ] Check parallel group — shared org/state collision?
5. [ ] Apply targeted fix; re-run 10x before closing
```

## Common causes → fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Element not found | Locator changed or not yet rendered | Update PO; add `wait_for_element_visible()` |
| Timeout on navigation | Slow env | Increase `NAVIGATION_TIMEOUT_MS` in env config |
| Stale element | DOM re-render | Re-query locator after action |
| Wrong data shown | Shared state / parallel race | Add `xdist_group`; unique runtime test data |
| Passes headed, fails headless | Viewport or animation | Set viewport in conftest; wait for spinner gone |
| Passes alone, fails in suite | Test order dependency | Remove shared mutable state; isolate fixtures |
| Random 401/redirect | Expired storage state | Re-capture `.auth/{profile}.json` |

## Wait hierarchy (prefer top)

1. `wait_for_element_visible(locator)`
2. `wait_for_spinner_to_disappear(spinner)`
3. `expect(locator).to_have_text(...)`
4. `page.wait_for_url(...)` / `assert_url_contains`
5. Fixed `time.sleep()` — **avoid**; document if truly unavoidable

## Parallel debugging

```bash
pytest -n 4 --dist loadgroup -k "test_name" --env dev
```

If only fails under `-n 4`: assign or fix `pytestmark = pytest.mark.xdist_group(...)`.

## Locator debugging

Run headed with slow motion:

```bash
pytest -k "test_name" --headed --env dev -s
```

Use Playwright trace on failure (add to conftest if not present):

```python
context.tracing.start(screenshots=True, snapshots=True)
# on failure: tracing.stop(path="trace.zip")
```

## Data debugging

- Attach `page.url`, visible text, API response to Allure
- Verify test uses runtime-generated unique names (not colliding with prior run)

## When to mark `ignore`

If root cause is external (3rd-party downtime, no test OTP hook) — mark `@pytest.mark.ignore` with ticket link, don't leave flaky in default suite.
