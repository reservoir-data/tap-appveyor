"""Pytest configuration for tests in this directory."""

from __future__ import annotations

import pytest

XFAIL_EMPTY = pytest.mark.xfail(reason="No records returned")

MAYBE_EMPTY = [
    "test_tap_stream_returns_record[collaborators]",
    "test_tap_stream_returns_record[projects]",
]


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests that require a live API key."""
    test_name = item.name.split("::")[-1]

    if test_name in MAYBE_EMPTY:
        item.add_marker(XFAIL_EMPTY)
