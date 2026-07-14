"""Test-data teardown registry — register cleanup callables as data is created.

Mirrors session_state.py's pattern: a module-level singleton that any layer
(steps, page actions) can import directly, without threading a fixture
through every call. tests/conftest.py runs and clears it after every test.
"""

from collections.abc import Callable

import allure


class TeardownRegistry:
    """Collects cleanup callables; runs them in reverse (LIFO) creation order."""

    def __init__(self) -> None:
        self._callbacks: list[tuple[str, Callable[[], None]]] = []

    def register(self, cleanup: Callable[[], None], *, label: str = "cleanup") -> None:
        """Register a cleanup to run after the test, regardless of pass/fail.

        Call this immediately after creating data — e.g. right after an API
        or UI action returns the new entity's id.
        """
        self._callbacks.append((label, cleanup))

    def run_all(self) -> None:
        """Run every registered cleanup, most-recently-created first.

        A failing cleanup is attached to Allure and does not stop the rest
        from running — one broken teardown must not leave everything else
        behind uncleaned.
        """
        while self._callbacks:
            label, cleanup = self._callbacks.pop()
            try:
                cleanup()
            except Exception as error:
                allure.attach(
                    f"{label}: {error}",
                    name="teardown-failure",
                    attachment_type=allure.attachment_type.TEXT,
                )

    def is_empty(self) -> bool:
        return not self._callbacks

    def clear(self) -> None:
        """Drop pending callbacks without running them — for test isolation only."""
        self._callbacks.clear()


teardown_registry = TeardownRegistry()
