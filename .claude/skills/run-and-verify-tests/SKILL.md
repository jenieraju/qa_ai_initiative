---
name: run-and-verify-tests
description: >-
  Runs pytest after scaffold or fixes and decides whether the work is actually
  done; green means done, red routes to a diagnosis skill. Use when scaffold or
  a fix is complete. Do NOT use before test files exist, for collect-only on
  runnable tests, or to diagnose a failure yourself — route it instead.
---

# Run and Verify Tests

```bash
invoke lint
pytest --collect-only --env dev tests/test/<area>/test_<feature>.py
invoke test-files --env dev --args="tests/test/<area>/test_<feature>.py -vv"
```

Run the single file first, then the area. Whole-suite runs come last — a
collection error in one file otherwise hides the result you care about.

## Reading the result

| Outcome | Do |
|---|---|
| Green, and you saw it go red first | Set `Status: automated` in the context doc |
| Green on the **first** run of new code | Suspect it. Flip an expected value and confirm it goes red — a test that cannot fail is not passing |
| Red | Do not edit yet — go to `diagnose-test-failure` |
| Passed here, fails under `--parallel N` | `debug-flaky-e2e-test` |
| Collected 0 items | Wrong path or the whole file is `@pytest.mark.ignore`d — say which |

**Never route a red test straight to `debug-flaky-e2e-test`.** That skill owns
*intermittent* failures only; a test that fails every run, or has never passed,
belongs to `diagnose-test-failure`, which classifies it first.

## Before calling it done

Fixed a flake? Confirm stability, don't infer it:

```bash
invoke test-files --env dev --args="tests/test/<area>/test_<feature>.py --parallel 4 -vv"
```

Failure artifacts land in `output/` (`src/core/failure_artifacts.py`); open a
trace with `playwright show-trace output/traces/<trace>.zip`.

## Done when

- [ ] `invoke lint` clean
- [ ] Executed (unless whole file `@ignore`d); Status matches the real result
- [ ] New tests were seen to fail for the right reason before passing
- [ ] Any red was routed to `diagnose-test-failure`, not patched in place
- [ ] User told pass/fail, with the count and any skips named

## Self-check

Triggers: "run the group-create tests", "is the members suite green", "verify
the scaffold works".
Does not trigger: "why does this test fail after the release"
(`diagnose-test-failure`), "this fails only under 4 workers"
(`debug-flaky-e2e-test`).
