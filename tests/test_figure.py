from figure_panel import create_panel, read_figure as F


def test_figure():
    pass


def test_create_figure_panel_1():
    create_panel(['tests/figs/a.svg', 'tests/figs/b.svg', 'tests/figs/c.svg'])


def test_create_figure_panel_2():
    create_panel(
        [['tests/figs/a.svg', 'tests/figs/b.svg'], ['tests/figs/c.svg']])


def test_create_figure_panel_3():
    create_panel([
        ['tests/figs/a.svg', 'tests/figs/b.svg'],
        ['tests/figs/c.svg'],
        ['tests/figs/a.svg', 'tests/figs/b.svg'],
    ])


def test_create_figure_panel_4():
    create_panel([
        ['tests/figs/a.svg', 'tests/figs/b.svg'],
        ['tests/figs/c.svg', [['tests/figs/a.svg', 'tests/figs/b.svg'],
                              ['tests/figs/c.svg', 'tests/figs/c.svg']]],
    ])
