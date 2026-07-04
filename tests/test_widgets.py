"""Unit tests for the pure helper functions in ``outfancy.widgets``."""

import re

import pytest

from outfancy import widgets


class TestCompressList:
    def test_docstring_example(self):
        # [1, 6, 4] -> [0, 2, 1] (rank while preserving position).
        assert widgets.compress_list([1, 6, 4]) == [0, 2, 1]

    def test_reordered(self):
        assert widgets.compress_list([3, 1, 2]) == [2, 0, 1]

    def test_handles_negative_numbers(self):
        assert widgets.compress_list([-2, 0, -5]) == [1, 2, 0]

    def test_empty(self):
        assert widgets.compress_list([]) == []

    def test_single(self):
        assert widgets.compress_list([42]) == [0]


class TestCreateMatrix:
    def test_dimensions(self):
        matrix = widgets.create_matrix(x=3, y=2, fill=".")
        assert matrix == [[".", ".", "."], [".", ".", "."]]

    def test_default_fill_is_empty_string(self):
        assert widgets.create_matrix(2, 1) == [["", ""]]

    def test_zero_rows(self):
        assert widgets.create_matrix(3, 0) == []


class TestIndexIsInList:
    def test_in_range(self):
        assert widgets.index_is_in_list([1, 2, 3], 0) is True
        assert widgets.index_is_in_list([1, 2, 3], 2) is True

    def test_out_of_range(self):
        assert widgets.index_is_in_list([1, 2, 3], 3) is False

    def test_negative_is_rejected(self):
        assert widgets.index_is_in_list([1, 2, 3], -1) is False

    def test_empty_list(self):
        assert widgets.index_is_in_list([], 0) is False


class TestIsCompleteHour:
    @pytest.mark.parametrize("value", ["12:30:00", "12:30", "00:00:00"])
    def test_valid(self, value):
        assert widgets.is_complete_hour(value) is True

    @pytest.mark.parametrize("value", ["25:00", "12:60", "x", ""])
    def test_invalid(self, value):
        assert widgets.is_complete_hour(value) is False


class TestIsDate:
    @pytest.mark.parametrize(
        "value",
        ["25-12-2020", "2020-12-25", "12/05/2021", "5-3-21"],
    )
    def test_valid_formats(self, value):
        assert widgets.is_date(value) is True

    @pytest.mark.parametrize("value", ["31-02-2020", "hello", "", "99-99-9999"])
    def test_invalid(self, value):
        assert widgets.is_date(value) is False


class TestNormaliseDate:
    def test_replaces_separators(self):
        assert widgets.normalise_date("2020/12/25") == "2020-12-25"
        assert widgets.normalise_date("12:30:00") == "12-30-00"
        assert widgets.normalise_date("a.b@c") == "a-b-c"

    def test_leaves_plain_dashes(self):
        assert widgets.normalise_date("2020-12-25") == "2020-12-25"


class TestRemoveColorsAndLength:
    def test_removes_basic_color(self):
        assert widgets.remove_colors("\x1b[1;33mhi\x1b[0;99m") == "hi"

    def test_removes_256_color(self):
        assert widgets.remove_colors("\x1b[38;5;123mX\x1b[0m") == "X"

    def test_removes_rgb_color(self):
        assert widgets.remove_colors("\x1b[38;2;255;0;0mX\x1b[0m") == "X"

    def test_leaves_plain_text(self):
        assert widgets.remove_colors("plain text") == "plain text"

    def test_printed_length_counts_visible_only(self):
        assert widgets.printed_length("\x1b[1;33mhi\x1b[0;99m") == 2
        assert widgets.printed_length("abc") == 3


class TestActualDateHour:
    def test_actual_date_format(self):
        # dd-mm-yyyy
        assert re.fullmatch(r"\d{2}-\d{2}-\d{4}", widgets.actual_date())

    def test_actual_hour_format(self):
        # hh:mm:ss
        assert re.fullmatch(r"\d{2}:\d{2}:\d{2}", widgets.actual_hour())
