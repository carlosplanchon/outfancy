"""Shared fixtures for the outfancy test suite.

These tests are *characterization* tests: they pin the current behaviour of a
historical library so future changes have a safety net. They never modify
anything under ``outfancy/``.
"""

import os

import pytest

import outfancy.chart
import outfancy.table
from outfancy.example_dataset import dataset as _dataset
from outfancy.example_dataset import color_dataset as _color_dataset


@pytest.fixture
def sample_dataset():
    """A realistic 8-column dataset shipped with the library."""
    return list(_dataset)


@pytest.fixture
def color_dataset():
    """Same shape as ``sample_dataset`` but with ANSI colors embedded."""
    return list(_color_dataset)


@pytest.fixture
def fixed_terminal(monkeypatch):
    """Force a deterministic 80x24 terminal.

    ``LineChart.render`` and ``LargeTable.render`` read the real terminal size
    via ``shutil.get_terminal_size`` (they take no ``screen_x`` argument), so we
    pin it to make their output reproducible regardless of the environment.
    """
    size = os.terminal_size((80, 24))
    monkeypatch.setattr(
        outfancy.chart.shutil, "get_terminal_size", lambda *a, **k: size
    )
    monkeypatch.setattr(
        outfancy.table.shutil, "get_terminal_size", lambda *a, **k: size
    )
    return size
