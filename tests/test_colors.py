"""Smoke tests for the ANSI constants in ``outfancy.colors``."""

from outfancy import colors


def _color_constants():
    return {
        name: value
        for name, value in vars(colors).items()
        if not name.startswith("_") and isinstance(value, str)
    }


def test_there_are_many_color_constants():
    # Guards against the module being accidentally emptied.
    assert len(_color_constants()) > 50


def test_every_constant_is_a_well_formed_ansi_escape():
    for name, value in _color_constants().items():
        assert value.startswith("\x1b["), name
        assert value.endswith("m"), name


def test_constants_are_unique():
    values = list(_color_constants().values())
    assert len(values) == len(set(values))
