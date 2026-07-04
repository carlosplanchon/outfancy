"""Characterization tests for ``Oneline`` and ``LargeTable``."""

from outfancy.table import LargeTable, Oneline
from outfancy.widgets import remove_colors

DATA = [(1, "Marie"), (2, "Joseph")]


class TestOneline:
    def test_returns_string_without_header(self):
        out = Oneline().render(DATA, screen_x=80, screen_y=24)
        plain = remove_colors(out)
        assert "Marie" in plain
        # Oneline forces label_list=False -> no header labels.
        assert "Name" not in plain

    def test_none_data_returns_message(self):
        assert "was not received" in Oneline().render(None)


class TestLargeTable:
    def test_renders_all_rows(self, fixed_terminal):
        rows = [(i, f"User{i}") for i in range(5)]
        plain = remove_colors(LargeTable().render(rows))
        for i in range(5):
            assert f"User{i}" in plain

    def test_empty_data_uses_default_empty_string(self, fixed_terminal):
        assert LargeTable().render([]) == "--- EMPTY ---"

    def test_set_empty_string_is_respected(self, fixed_terminal):
        lt = LargeTable()
        lt.set_empty_string("nothing here")
        assert lt.render([]) == "nothing here"

    def test_none_data_returns_message(self, fixed_terminal):
        assert "was not provided" in LargeTable().render(None)
