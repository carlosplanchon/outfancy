"""Characterization tests for ``outfancy.table.Table``.

``Table.render`` accepts explicit ``screen_x`` / ``screen_y``, so we always pass
them to get deterministic output without depending on the real terminal.
"""

from outfancy.table import Table
from outfancy.widgets import remove_colors

DATA = [(1, "Marie"), (2, "Joseph")]


def render(data, **kwargs):
    kwargs.setdefault("screen_x", 80)
    kwargs.setdefault("screen_y", 24)
    return Table().render(data, **kwargs)


def plain_lines(out):
    return [line.rstrip() for line in remove_colors(out).split("\n")]


class TestBasicRendering:
    def test_returns_string(self):
        assert isinstance(render(DATA), str)

    def test_golden_layout(self):
        # Characterization: also documents that the auto label "Id" is
        # truncated to the (narrow) data column width -> "I".
        assert plain_lines(render(DATA)) == [" I Name", " 1 Marie", " 2 Joseph"]

    def test_one_data_row_per_tuple(self):
        body = [ln for ln in plain_lines(render(DATA, label_list=False)) if ln]
        assert len(body) == len(DATA)


class TestEmptyAndNone:
    def test_empty_data_uses_default_empty_string(self):
        assert render([]) == "--- EMPTY ---"

    def test_set_empty_string_is_respected(self):
        t = Table()
        t.set_empty_string("no data")
        assert t.render([], screen_x=80) == "no data"

    def test_none_data_returns_message(self):
        assert "was not provided" in render(None)


class TestLabels:
    def test_label_list_false_hides_header(self):
        out = plain_lines(render(DATA, label_list=False))
        assert "Marie" in "\n".join(out)
        assert "Name" not in "\n".join(out)

    def test_forced_labels_are_shown(self):
        out = "\n".join(plain_lines(render(DATA, label_list=["ID", "Name"])))
        # Header row is present (Name fits the wider column).
        assert "Name" in out


class TestOrder:
    def test_reordering_changes_output(self):
        forward = render(DATA, order=[0, 1])
        reversed_ = render(DATA, order=[1, 0])
        assert forward != reversed_

    def test_selecting_single_column_suppresses_the_other(self):
        out = "\n".join(plain_lines(render(DATA, order=[0])))
        assert "Marie" not in out
        assert "1" in out


class TestConfiguration:
    def test_setters_and_getters_round_trip(self):
        t = Table()
        assert t.show_corrector() == -2
        t.set_corrector(-4)
        assert t.show_corrector() == -4

        assert t.show_show_labels() is True
        t.set_show_labels(False)
        assert t.show_show_labels() is False

        t.set_maximum_number_of_rows(5)
        assert t.show_maximum_number_of_rows() == 5

    def test_empty_string_getter_reflects_setter(self):
        t = Table()
        t.set_empty_string("custom")
        assert t.render([], screen_x=80) == "custom"


class TestColorDataset:
    def test_color_dataset_renders_with_ansi(self, color_dataset):
        out = Table().render(color_dataset, screen_x=120, screen_y=40)
        assert isinstance(out, str)
        assert "\x1b[" in out
        # Every row is still present once colors are stripped.
        plain = remove_colors(out)
        assert "Feisbuk" in plain
