"""Unit tests for the test-data teardown registry (src/core/teardown.py).

No browser involved — these test the registry's own logic in isolation.
"""

import pytest

from src.core.teardown import TeardownRegistry

pytestmark = pytest.mark.unit


class TestTeardownRegistry:
    """Verifies cleanup ordering, failure isolation, and emptiness reporting."""

    def test_runs_callbacks_in_reverse_creation_order(self):
        executed: list[str] = []
        registry = TeardownRegistry()
        registry.register(lambda: executed.append("created_first"), label="created_first")
        registry.register(lambda: executed.append("created_second"), label="created_second")

        registry.run_all()

        assert executed == ["created_second", "created_first"]

    def test_a_failing_cleanup_does_not_block_the_rest(self):
        executed: list[str] = []
        registry = TeardownRegistry()

        def failing_cleanup():
            raise RuntimeError("boom")

        registry.register(failing_cleanup, label="failing")
        registry.register(lambda: executed.append("still_runs"), label="still_runs")

        registry.run_all()  # must not raise

        assert executed == ["still_runs"]

    def test_run_all_empties_the_registry(self):
        registry = TeardownRegistry()
        registry.register(lambda: None)
        assert not registry.is_empty()

        registry.run_all()

        assert registry.is_empty()

    def test_clear_drops_pending_callbacks_without_running_them(self):
        executed: list[str] = []
        registry = TeardownRegistry()
        registry.register(lambda: executed.append("should_not_run"))

        registry.clear()

        assert registry.is_empty()
        assert executed == []
