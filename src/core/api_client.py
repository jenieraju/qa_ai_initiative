"""Thin httpx wrapper for API-based test setup and cleanup.

For seeding preconditions and deleting test data — never for exercising the
flow under test itself, which must go through the UI (see the
api-test-setup-teardown skill). Base URL and auth come from get_settings(),
so no call site hardcodes a host or a token.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

import allure
import httpx

from src.core.settings import get_settings


class ApiError(RuntimeError):
    """An API call used for setup/teardown returned a non-success status."""


class ApiClient:
    """Authenticated httpx client bound to API_BASE_URL.

    Usable as a context manager so the connection is always released:

        with ApiClient() as api:
            group = api.post("/groups", json={"name": name})
    """

    def __init__(
        self,
        *,
        timeout_seconds: float = 30.0,
        cookies: dict[str, str] | None = None,
    ) -> None:
        """Bind to API_BASE_URL.

        `cookies` covers the environments that issue no static automation token:
        lift them out of `.auth/{profile}.json` and reuse the session the UI
        suite already logged in with (see the api-test-setup-teardown skill).
        """
        settings = get_settings()
        if not settings.api_base_url:
            raise ApiError("API_BASE_URL is not configured for this environment.")
        headers = {"Accept": "application/json"}
        if settings.api_token:
            headers["Authorization"] = f"Bearer {settings.api_token}"
        self._client = httpx.Client(
            base_url=settings.api_base_url.rstrip("/"),
            headers=headers,
            timeout=timeout_seconds,
            cookies=cookies or {},
        )

    def __enter__(self) -> ApiClient:
        return self

    def __exit__(self, *_exc_info) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Send a request and return the decoded body; raise ApiError on failure.

        The request/response pair is attached to Allure so a setup failure is
        diagnosable from the report alone.
        """
        response = self._client.request(method, path, **kwargs)
        allure.attach(
            f"{method.upper()} {response.request.url}\n"
            f"Status: {response.status_code}\n\n{response.text[:2000]}",
            name=f"api {method.lower()} {path}",
            attachment_type=allure.attachment_type.TEXT,
        )
        if response.is_error:
            raise ApiError(
                f"{method.upper()} {path} failed with {response.status_code}: {response.text[:500]}"
            )
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)

    def poll_until(
        self,
        path: str,
        *,
        done: Callable[[Any], bool],
        timeout_seconds: float = 60.0,
        interval_seconds: float = 2.0,
        **kwargs: Any,
    ) -> Any:
        """GET `path` until `done(body)` is true, then return the body.

        The one sanctioned sleep in the framework. UI code must wait on the
        browser (web-first assertions, explicit waits) — but an async server-side
        job exposes no such signal, so polling is the only option. Keeping it here
        means `time.sleep` stays banned everywhere else, enforced by
        tests/test/core/test_layer_boundaries.py.
        """
        deadline = time.monotonic() + timeout_seconds
        last_body: Any = None
        while time.monotonic() < deadline:
            last_body = self.get(path, **kwargs)
            if done(last_body):
                return last_body
            time.sleep(interval_seconds)
        raise ApiError(
            f"GET {path} did not reach the expected state within "
            f"{timeout_seconds}s. Last response: {str(last_body)[:300]}"
        )
