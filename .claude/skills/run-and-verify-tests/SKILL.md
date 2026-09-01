---
name: run-and-verify-tests
description: >-
  Runs pytest after scaffold or fixes; done only when tests pass. Use when scaffold
  or a fix is complete. Do NOT use before test files exist or for collect-only on
  runnable tests.
---

# Run and Verify Tests

```bash
invoke lint
pytest --collect-only --env dev tests/test/<area>/test_<feature>.py
invoke test-files --env dev --args="tests/test/<area>/test_<feature>.py -vv"
```

Pass → set `Status: automated` in context doc. Fail → do not; use `debug-flaky-e2e-test`.

## Done when

- [ ] Executed (unless whole file `@ignore`); Status matches; user told pass/fail
