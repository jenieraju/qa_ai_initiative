---
name: api-test-setup-teardown
description: >-
  Uses httpx and API_BASE_URL to seed or clean test data before UI steps. Use
  when UI setup is slow, flaky, or when testing read/display flows only.
---

# API Test Setup / Teardown

Use **UI steps** for flows under test; use **API** for precondition data only.

Config: `get_settings().api_base_url` — never hardcode hosts ([AGENTS.md](../../AGENTS.md)).

## When to prefer API setup

| API setup | UI setup |
|-----------|----------|
| Create 50 test records | Test the create form itself |
| Reset org to known state | Test onboarding wizard |
| Poll async job completion | Test job trigger button |

## Basic pattern

```python
import httpx
import pytest
from src.core.settings import get_settings

@pytest.fixture
def api_client():
    settings = get_settings()
    with httpx.Client(
        base_url=settings.api_base_url,
        timeout=30.0,
        headers={"Authorization": f"Bearer {settings.api_token}"},
    ) as client:
        yield client

@pytest.fixture
def seeded_group(api_client):
    resp = api_client.post("/v1/groups", json={"name": "Setup Group"})
    resp.raise_for_status()
    group_id = resp.json()["id"]
    yield group_id
    api_client.delete(f"/v1/groups/{group_id}")
```

## Auth for API calls

1. Read token from env (`API_TOKEN`, `FEATURE_*` vars)
2. Or login via API once in session fixture, cache token
3. Never commit tokens — same rules as UI credentials

## Polling async jobs

```python
import time

def wait_for_job(client, job_id: str, timeout: int = 60) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = client.get(f"/v1/job/{job_id}")
        data = resp.json()
        if data["status"] in ("completed", "failed"):
            return data
        time.sleep(2)
    raise TimeoutError(f"Job {job_id} not finished")
```

Prefer explicit waits over fixed sleep in UI; polling API status is acceptable.

## Teardown

- Always clean up created entities in fixture `yield` teardown
- Use try/except Exception on delete — don't fail test on cleanup errors
- Log cleanup failures to Allure attach for investigation

## Layer rule

API helpers live in `src/core/` or `tests/fixtures/` — **not** in page actions or steps unless wrapped as a test fixture used before steps run.
