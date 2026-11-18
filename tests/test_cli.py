"""Tests for the Typer CLI in ``outfancy.cli``."""

import re

from typer.testing import CliRunner

from outfancy.cli import _parse_csv, _parse_json, _parse_order, app
from outfancy.widgets import remove_colors

runner = CliRunner()


def plain(result):
    return remove_colors(result.output)


def plain_lines(result):
    return [line.rstrip() for line in plain(result).rstrip("\n").split("\n")]


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        # "outfancy <version>" for any version format (0.11, 0.10.1, 1.0rc1...).
        match = re.fullmatch(r"outfancy (\S+)", result.output.strip())
        assert match is not None
        assert any(ch.isdigit() for ch in match.group(1))


class TestTableCommand:
    def test_csv_with_headers(self):
        result = runner.invoke(
            app, ["table", "--has-headers"], input="id,name\n1,foo\n2,bar"
        )
        assert result.exit_code == 0
        out = plain(result)
        assert "foo" in out
        assert "bar" in out

    def test_no_labels_hides_header(self):
        result = runner.invoke(
            app, ["table", "--no-labels"], input="1,foo\n2,bar"
        )
        assert result.exit_code == 0

    def test_json_input(self):
        result = runner.invoke(
            app, ["table", "--json"], input='[{"a":1,"b":2},{"a":3,"b":4}]'
        )
        assert result.exit_code == 0
        assert "1" in plain(result)

    def test_empty_input_errors(self):
        result = runner.invoke(app, ["table"], input="")
        assert result.exit_code == 1
        assert "No data" in result.output

    def test_json_object_input_is_handled_gracefully(self):
        # Regression: a top-level JSON object used to crash with KeyError.
        result = runner.invoke(app, ["table", "--json"], input='{"a": 1}')
        assert result.exit_code == 1
        assert "No data" in result.output


class TestRowsOfDifferentLength:
    # The table is as wide as its widest row; missing cells are left empty.

    def test_short_row_is_padded(self, fixed_terminal):
        # Regression: a row shorter than the first one used to crash with
        # IndexError.
        result = runner.invoke(
            app, ["table", "--no-labels"], input="a1,b1,c1\na2,b2\na3"
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" a1 b1 c1", " a2 b2", " a3"]

    def test_long_row_widens_the_table(self, fixed_terminal):
        # Cells beyond the length of the first row used to be left out.
        result = runner.invoke(
            app, ["table", "--no-labels"], input="a1\na2,b2\na3,b3,c3"
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" a1", " a2 b2", " a3 b3 c3"]

    def test_row_longer_than_the_headers(self, fixed_terminal):
        result = runner.invoke(
            app, ["table", "--has-headers"], input="x,y\na1,b1,c1\na2,b2"
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" x  y", " a1 b1 c1", " a2 b2"]

    def test_row_shorter_than_the_headers(self, fixed_terminal):
        result = runner.invoke(
            app, ["table", "--has-headers"], input="x,y,z\na1,b1\na2,b2,c2"
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" x  y  z", " a1 b1", " a2 b2 c2"]

    def test_json_arrays(self, fixed_terminal):
        result = runner.invoke(
            app, ["table", "--json", "--no-labels"], input="[[1, 2, 3], [4, 5]]"
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" 1 2 3", " 4 5"]

    def test_json_object_without_a_key(self, fixed_terminal):
        # The value stays under its own key, not under the first column.
        result = runner.invoke(
            app, ["table", "--json"],
            input='[{"x": "a1", "y": "b1"}, {"y": "b2"}]',
        )
        assert result.exit_code == 0
        assert plain_lines(result) == [" x  y", " a1 b1", "    b2"]


class TestOrderOption:
    def test_valid_order_is_accepted(self):
        result = runner.invoke(
            app, ["table", "--order", " 1 , 0 "], input="1,foo\n2,bar"
        )
        assert result.exit_code == 0

    def test_out_of_range_column_is_reported(self):
        # Regression: used to crash with IndexError.
        result = runner.invoke(
            app, ["table", "--order", "0,9"], input="1,foo\n2,bar"
        )
        assert result.exit_code == 1
        assert "Invalid --order: column 9 does not exist" in result.output

    def test_negative_column_is_reported(self):
        result = runner.invoke(
            app, ["table", "--order", "-1"], input="1,foo\n2,bar"
        )
        assert result.exit_code == 1
        assert "Invalid --order: column -1 does not exist" in result.output

    def test_text_that_is_not_a_number_is_reported(self):
        # Regression: used to crash with ValueError.
        result = runner.invoke(
            app, ["table", "--order", "0,x"], input="1,foo\n2,bar"
        )
        assert result.exit_code == 1
        assert "Invalid --order: 'x' is not a column index" in result.output

    def test_parse_order_returns_the_indices(self):
        assert _parse_order(" 1 , 0 ", columns=2) == [1, 0]


class TestChartCommand:
    def test_valid_pairs(self):
        result = runner.invoke(app, ["chart"], input="1,10\n2,25\n3,15")
        assert result.exit_code == 0
        assert "·" in result.output

    def test_no_valid_pairs_errors(self):
        result = runner.invoke(app, ["chart"], input="notanumber")
        assert result.exit_code == 1
        assert "No valid x,y pairs" in result.output


class TestParsers:
    def test_parse_csv_with_headers(self):
        headers, rows = _parse_csv("a,b\n1,2", has_headers=True)
        assert headers == ["a", "b"]
        assert rows == [("1", "2")]

    def test_parse_csv_without_headers(self):
        headers, rows = _parse_csv("1,2\n3,4")
        assert headers is None
        assert rows == [("1", "2"), ("3", "4")]

    def test_parse_json_array_of_dicts(self):
        labels, rows = _parse_json('[{"x":1},{"x":9}]')
        assert labels == ["x"]
        assert rows == [("1",), ("9",)]

    def test_parse_json_array_of_arrays(self):
        labels, rows = _parse_json("[[1,2]]")
        assert labels is None
        assert rows == [("1", "2")]

    def test_parse_json_empty(self):
        labels, rows = _parse_json("[]")
        assert labels is None
        assert rows == []


class TestParseJsonRobustness:
    def test_top_level_object_returns_no_rows(self):
        # A JSON object is not a supported table shape: handled, no crash.
        labels, rows = _parse_json('{"a": 1}')
        assert labels is None
        assert rows == []

    def test_top_level_scalar_returns_no_rows(self):
        labels, rows = _parse_json("5")
        assert labels is None
        assert rows == []

    def test_array_of_scalars_becomes_single_column(self):
        labels, rows = _parse_json("[1, 2, 3]")
        assert labels is None
        assert rows == [("1",), ("2",), ("3",)]


class TestParseJsonObjects:
    def test_values_are_placed_by_key(self):
        labels, rows = _parse_json('[{"a": 1, "b": 2}, {"b": 3, "a": 4}]')
        assert labels == ["a", "b"]
        assert rows == [("1", "2"), ("4", "3")]

    def test_missing_key_leaves_an_empty_cell(self):
        labels, rows = _parse_json('[{"a": 1, "b": 2}, {"b": 3}]')
        assert labels == ["a", "b"]
        assert rows == [("1", "2"), ("", "3")]

    def test_new_key_adds_a_column(self):
        labels, rows = _parse_json('[{"a": 1}, {"a": 2, "b": 3}]')
        assert labels == ["a", "b"]
        assert rows == [("1", ""), ("2", "3")]

    def test_element_that_is_not_an_object_does_not_crash(self):
        # Regression: a scalar among the objects used to raise AttributeError.
        labels, rows = _parse_json('[{"a": 1, "b": 2}, 5, [6, 7]]')
        assert labels == ["a", "b"]
        assert rows == [("1", "2"), ("5",), ("6", "7")]
