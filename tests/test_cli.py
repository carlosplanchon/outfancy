"""Tests for the Typer CLI in ``outfancy.cli``."""

import re

from typer.testing import CliRunner

from outfancy.cli import _parse_csv, _parse_json, app
from outfancy.widgets import remove_colors

runner = CliRunner()


def plain(result):
    return remove_colors(result.output)


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
