from figure_panel.main import parse_structure


def test_parse_structure():
    assert parse_structure('abc.svg, d.svg, c2.svg') == [
        'abc.svg', 'd.svg', 'c2.svg']

    assert parse_structure('abc.svg, [bd.svg, c2.svg], [d1.svg, [ee.svg, fa.svg], gd.svg]') == [
        'abc.svg',
        ['bd.svg', 'c2.svg'],
        ['d1.svg', ['ee.svg', 'fa.svg'], 'gd.svg']
    ]

    assert parse_structure('[x.svg,y.svg],[z.svg, k.svg]') == [
        ['x.svg', 'y.svg'],
        ['z.svg', 'k.svg']
    ]

    assert parse_structure('[x.svg,y.svg],[z.svg, k.svg],[a.svg,b.svg]') == [
        ['x.svg', 'y.svg'],
        ['z.svg', 'k.svg'],
        ['a.svg', 'b.svg']
    ]

    assert parse_structure('[x.svg,y.svg],[z.svg]') == [
        ['x.svg', 'y.svg'],
        ['z.svg']
    ]
