"""Unit tests for ``outfancy.window.Window`` (deterministic, no terminal I/O)."""

from outfancy.window import Window


def test_empty_window_render():
    win = Window(width=3, height=2, fill=".")
    assert win.render() == "...\n..."


def test_insert_full_matrix():
    win = Window(width=2, height=2, fill=".")
    win.insert([["a", "b"], ["c", "d"]], 0, 0)
    assert win.render() == "ab\ncd"


def test_insert_clips_matrix_larger_than_window():
    win = Window(width=3, height=2, fill=".")
    big = [
        ["a", "b", "c", "d"],
        ["e", "f", "g", "h"],
        ["i", "j", "k", "l"],
    ]
    win.insert(big, 0, 0)
    # Only the top-left 3x2 region fits.
    assert win.render() == "abc\nefg"


def test_insert_at_offset():
    win = Window(width=3, height=2, fill=".")
    win.insert([["x"]], x_vertex=1, y_vertex=1)
    assert win.render() == "...\n.x."


def test_insert_point_in_bounds():
    win = Window(width=2, height=2, fill=".")
    win.insert_point("#", x_coord=1, y_coord=0)
    assert win.render() == ".#\n.."


def test_insert_point_out_of_bounds_is_ignored():
    win = Window(width=2, height=2, fill=".")
    win.insert_point("#", x_coord=5, y_coord=5)
    win.insert_point("#", x_coord=-1, y_coord=0)
    # Nothing changed, no exception raised.
    assert win.render() == "..\n.."
