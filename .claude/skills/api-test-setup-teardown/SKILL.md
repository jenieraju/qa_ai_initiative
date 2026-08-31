---
name: api-test-setup-teardown
description: >-
  Uses src/core/api_client.ApiClient to seed or clean precondition test data
  in a pytest fixture before UI steps run. Use when UI setup is slow or flaky, when
  seeding many records, or when testing read/display flows only. Do NOT use for
  data the flow under test creates itself (the id is only known mid-test — see
  test-data-teardown), and do NOT use to replace the UI steps of the flow
  actually under test.
---

# API Test Setup / Teardown

Use **UI steps** for flows under test; use **API** for precondition data only.

Config: `get_settings().api_base_url` — never hardcode hosts ([AGENTS.md](../../../AGENTS.md)).

## When to prefer API setup

| API setup | UI setup |
|-----------|----------|
| Create 50 test records | Test the create form itself |
| Reset org to known state | Test onboarding wizard |
| Poll async job completion | Test job trigger button |

## Basic pattern

`src/core/api_client.py` already owns base URL, bearer token, error raising and
Allure attachment. Use it — never hand-roll an `httpx.Client`:

```python
import allure
import pytest

from src.core.api_client import ApiClient, ApiError

@pytest.fixture
def api():
    with ApiClient() as client:
        yield client

@pytest.fixture
def seeded_group(api):
    group = api.post("/v1/groups", json={"name": "Setup Group"})
    group_id = group["id"]
    yield group_id
    try:
        api.delete(f"/v1/groups/{group_id}")
    except ApiError as exc:  # cleanup must not fail the test
        allure.attach(str(exc), "cleanup failed", allure.attachment_type.TEXT)
```

**`/v1/groups` above is a placeholder.** Confirm the real seed and delete
paths before writing a feature fixture — from the app's own bundle
(`discover-locators-from-ui` → Option C finds `` `v1/…` `` literals) or from a
backend engineer. A fixture that seeds against a guessed path fails every test
in the file with a 404 and looks like a broken suite.

`ApiClient` returns the decoded body and raises `ApiError` on a non-2xx, so
there is no `raise_for_status()` or `.json()` to remember.

## Auth for API calls

`ApiClient` sends `Authorization: Bearer <API_TOKEN>` when the token is set.
`get_settings().api_token` (alias `API_TOKEN`) is
**empty by default** — this app's real login is mobile + OTP, not a static
token. Check which of these applies before writing the fixture:

1. **Env issues a static automation token** — set `API_TOKEN` in `.env.<env>`
   and use `get_settings().api_token` as shown above.
2. **No static token** — reuse the session the UI suite already saved.
   `src/core/auth_storage.py` writes `.auth/{profile}.json`; lift the cookies
   out of it rather than logging in a second time:

   ```python
   import json

   from src.core.api_client import ApiClient
   from src.core.auth_storage import auth_state_exists, auth_state_path

   @pytest.fixture(scope="session")
   def api():
       if not auth_state_exists():
           pytest.skip("No .auth/default.json — run a login test first")
       state = json.loads(auth_state_path().read_text())
       cookies = {c["name"]: c["value"] for c in state.get("cookies", [])}
       with ApiClient(cookies=cookies) as client:
           yield client
   ```

Either way: never commit tokens — same rules as UI credentials
([AGENTS.md](../../../AGENTS.md)).

## Polling async jobs

`time.sleep` is banned in UI code and enforced by
`tests/test/core/test_layer_boundaries.py`. API polling is the one legitimate
exception, so it lives in `src/core/api_client.py` (the only module exempt from
that check) — use `ApiClient.poll_until`, don't write a sleep loop in a fixture:

```python
job = api.poll_until(
    f"/v1/job/{job_id}",
    done=lambda data: data["status"] in ("completed", "failed"),
    timeout_seconds=60,
)
```

## Teardown

- Always clean up created entities in fixture `yield` teardown
- Use try/except Exception on delete — don't fail test on cleanup errors
- Log cleanup failures to Allure attach for investigation

## Wiring is proven, endpoints are not

`tests/test/core/test_api_client_teardown_integration.py` exercises this exact seed → register → `run_all()` pattern end-to-end (network mocked at `httpx.Client.request`, so no live API needed) — it proves `ApiClient` and `teardown_registry` compose correctly. It does **not** prove `/v1/groups` or any other feature path is real; no feature suite calls `ApiClient` yet, so treat every endpoint in this skill as unconfirmed until you check it.

## Layer rule

- **The client** lives in `src/core/api_client.py` — one implementation.
- **Precondition fixtures** live in `tests/conftest.py` or a `conftest.py` in
  the feature's test package.
- **Page actions and page objects stay UI-only.** Never call the API from them.
- **Steps may call `ApiClient`** for one specific job: registering cleanup for
  data the UI flow just created, when only a step knows the new id (see
  `test-data-teardown`). That is orchestration, not a UI interaction.

## Done when

- [ ] Fixture uses `ApiClient`, not a hand-rolled `httpx.Client`
- [ ] Auth path chosen from the two options above; no invented settings field
- [ ] Every entity created in the fixture is deleted in its `yield` teardown
- [ ] `invoke lint` passes
- [ ] `pytest --collect-only --env dev -m "<marker>"` still collects the test

## Self-check

Triggers: "seed 50 groups via API before this test", "set up preconditions
over the API instead of the UI wizard", "the UI setup for this read-only test
is too flaky".
Does not trigger: "clean up the group this test just created"
(`test-data-teardown`), "the create-group form is the thing under test"
(UI steps).
