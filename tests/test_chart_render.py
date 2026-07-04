"""Characterization tests for ``LineChart.render`` output.

``render`` reads the real terminal size, so every test here uses the
``fixed_terminal`` fixture (80x24) for reproducibility.
"""

from outfancy.chart import LineChart
from outfancy.widgets import remove_colors


def _plotted():
    c = LineChart()
    c.plot([(1, 10), (2, 25), (3, 15), (4, 30), (5, 20)])
    return c


def test_render_returns_multiline_string(fixed_terminal):
    out = _plotted().render()
    assert isinstance(out, str)
    assert len(out.splitlines()) > 3


def test_render_includes_plot_name(fixed_terminal):
    out = _plotted().render(plot_name="Sales")
    assert "Sales" in out


def test_render_draws_background_points(fixed_terminal):
    out = _plotted().render()
    assert "·" in out


def test_color_adds_ansi_and_matches_plain(fixed_terminal):
    chart = _plotted()
    plain = chart.render(plot_name="T", color=False)
    colored = chart.render(plot_name="T", color=True)
    assert "\x1b[" in colored
    assert "\x1b[" not in plain
    # Stripping the colors must yield the exact plain rendering.
    assert remove_colors(colored) == plain
