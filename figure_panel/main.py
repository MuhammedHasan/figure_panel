import click
from figure_panel.figure import create_panel


def parse_structure(arg):
    stack = [[]]

    current = []
    for i in arg:
        if i == ' ':
            continue
        elif (i == '[') or (i == ']') or (i == ','):
            if current:
                stack[-1].append(''.join(current))
                current = []
            if i == '[':
                stack.append(list())
            elif i == ']':
                stack[-2].append(stack[-1])
                stack.pop()
        else:
            current.append(i)

    if current:
        stack[-1].append(''.join(current))

    return stack[0]


@click.command()
@click.option('--figures', '-f', type=str)
@click.option('--output', '-o', type=str)
@click.option('--width', type=float, default=1200)
@click.option('--fontsize', type=float, default=24)
def cli_figure_panel(figures, output, width, fontsize):
    figures = parse_structure(figures)
    create_panel(figures, width=width, fontsize=fontsize).save(output)

# print(parse_structure('[abc.svg, [bd, c2], [d1, [ee, fa], gd]]'))
# print(parse_structure('abc, d, c2'))
