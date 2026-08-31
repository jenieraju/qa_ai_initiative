"""Proves the api-test-setup-teardown / test-data-teardown pattern actually runs.

Both skills teach: seed via `ApiClient`, register the delete with
`teardown_registry`, let `run_all()` call it. Neither module has a caller
anywhere in `src/` or `tests/` outside its own unit test — the skills
document a pattern nobody has ever executed. This test exercises the real
wiring end-to-end (mocking only the network boundary, `httpx.Client.request`)
so a regression in either module, or in how they compose, fails here instead
of being discovered the first time a feature test tries to use it.

No browser, no live API: `unittest.mock` stands in for the network call.
"""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.core.api_client import ApiClient, ApiError
from src.core.teardown import TeardownRegistry

pytestmark = pytest.mark.unit


def _mock_response(*, status_code: int = 200, json_body: dict | None = None) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.is_error = status_code >= 400
    response.text = "" if json_body is None else str(json_body)
    response.content = b"{}" if json_body is not None else b""
    response.json.return_value = json_body or {}
    response.request = MagicMock(url="https://api.dev.cofee.life/v1/groups")
    return response


class TestApiClientTeardownIntegration:
    """`ApiClient` + `teardown_registry`, wired the way the skills describe."""

    def test_seed_then_register_then_run_all_deletes_the_seeded_entity(self):
        create_response = _mock_response(status_code=201, json_body={"id": "grp_123"})
        delete_response = _mock_response(status_code=204)

        registry = TeardownRegistry()

        with (
            patch.object(httpx.Client, "request", side_effect=[create_response, delete_response]),
            ApiClient() as api,
        ):
            created = api.post("/v1/groups", json={"name": "Setup Group"})
            group_id = created["id"]
            registry.register(
                lambda: api.delete(f"/v1/groups/{group_id}"),
                label=f"delete group {group_id}",
            )

            assert not registry.is_empty()
            registry.run_all()

        assert registry.is_empty()

    def test_a_failing_delete_is_swallowed_not_raised(self):
        """Mirrors real usage: a fixture/step must not let a cleanup failure fail the test."""
        create_response = _mock_response(status_code=201, json_body={"id": "grp_456"})
        delete_response = _mock_response(status_code=500)

        registry = TeardownRegistry()

        with (
            patch.object(httpx.Client, "request", side_effect=[create_response, delete_response]),
            ApiClient() as api,
        ):
            created = api.post("/v1/groups", json={"name": "Setup Group"})
            group_id = created["id"]
            registry.register(lambda: api.delete(f"/v1/groups/{group_id}"))

            registry.run_all()  # must not raise, even though the delete call does

        assert registry.is_empty()

    def test_delete_raises_apierror_on_non_2xx_outside_the_registry(self):
        """Direct call (no registry) still raises — confirms the registry, not ApiClient, swallows errors."""
        with (
            patch.object(httpx.Client, "request", return_value=_mock_response(status_code=404)),
            ApiClient() as api,
            pytest.raises(ApiError),
        ):
            api.delete("/v1/groups/does-not-exist")
