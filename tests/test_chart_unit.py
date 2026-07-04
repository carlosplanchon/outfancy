"""Unit tests for the deterministic pieces of ``outfancy.chart.LineChart``.

These do not render, so they need no terminal size.
"""

from math import nan

import pytest

from outfancy.chart import LineChart


class TestCheckDataIntegrity:
    def test_non_list_is_invalid(self):
        integrity, reason = LineChart().check_data_integrity("nope")
        assert integrity is False
        assert reason == "The input is not a list."

    def test_empty_list_is_invalid(self):
        integrity, reason = LineChart().check_data_integrity([])
        assert integrity is False
        assert reason == "The dataset have not elements."

    def test_pair_of_wrong_length_is_invalid(self):
        integrity, reason = LineChart().check_data_integrity([(1, 2, 3)])
        assert integrity is False
        assert reason == "An element is not an ordered pair."

    def test_non_numeric_element_is_invalid(self):
        integrity, reason = LineChart().check_data_integrity([(1, "a")])
        assert integrity is False

    def test_none_element_is_allowed(self):
        integrity, reason = LineChart().check_data_integrity([(1, None)])
        assert integrity is True
        assert reason is None

    def test_valid_dataset(self):
        integrity, reason = LineChart().check_data_integrity([(1, 2), (3, 4)])
        assert integrity is True
        assert reason is None


class TestGetCharSlope:
    def test_nan_returns_vertical_bar(self):
        assert LineChart().get_char_slope(nan, color=False, color_number=33) == "|"

    @pytest.mark.parametrize("slope", [3, -3, 2.1, -2.1])
    def test_steep_slope_is_vertical_bar(self, slope):
        assert LineChart().get_char_slope(slope, False, 33) == "|"

    def test_positive_slope_is_forward_slash(self):
        assert LineChart().get_char_slope(1, False, 33) == "/"

    def test_negative_slope_is_backslash(self):
        assert LineChart().get_char_slope(-1, False, 33) == "\\"

    def test_flat_slope_is_dash(self):
        assert LineChart().get_char_slope(0, False, 33) == "—"

    def test_color_wraps_character(self):
        assert (
            LineChart().get_char_slope(1, color=True, color_number=33)
            == "\x1b[1;33m/\x1b[0;99m"
        )


class TestGetListOfElements:
    def test_splits_pairs(self):
        xs, ys = LineChart().get_list_of_elements([(1, 10), (2, 20)])
        assert xs == [1, 2]
        assert ys == [10, 20]


class TestPlotAndClear:
    def test_plot_updates_maxima(self):
        c = LineChart()
        c.plot([(1, 10), (5, 20)])
        assert c.x_max == 5
        assert c.y_max == 20
        assert len(c.dataset_space) == 1

    def test_minima_default_to_zero_for_positive_data(self):
        # Documents a quirk: min tracking starts at 0 and only lowers.
        c = LineChart()
        c.plot([(1, 10), (5, 20)])
        assert c.x_min == 0
        assert c.y_min == 0

    def test_negative_values_lower_the_minima(self):
        c = LineChart()
        c.plot([(-3, -5)])
        assert c.x_min == -3
        assert c.y_min == -5

    def test_plot_with_invalid_data_returns_error_message(self):
        message = LineChart().plot("bad")
        assert "Input data is invalid" in message

    def test_clear_resets_dataset_space(self):
        c = LineChart()
        c.plot([(1, 2)])
        c.clear()
        assert c.dataset_space == []
