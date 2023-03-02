import itertools
import string
import tempfile
from itertools import product
from functools import reduce
from typing import List
import svgutils.transform as sg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import cairosvg


def iter_letters():
    i = 1
    while True:
        for s in product(string.ascii_lowercase, repeat=i):
            yield ''.join(s)
        i += 1


class Figure:

    def __init__(self, root, height, width, labels=None):
        self.root = root
        self.height = height
        self.width = width
        self.labels = labels or list()

    def scale_height(self, height):
        '''
        Scale heigh to given value
        '''
        scale = height / self.height
        self.height = height
        self.width = self.width * scale
        return self.scale(scale)

    def scale_width(self, width):
        '''
        Scale width to given value
        '''
        scale = width / self.width
        self.width = width
        self.height = self.height * scale
        return self.scale(scale)

    def scale(self, scale):
        self.root.scale(scale)

        for label in self.labels:
            fontsize = float(label.root.attrib['font-size']) / scale
            label.root.attrib['font-size'] = str(fontsize)
            label.pad = label.pad / scale
            label.root.attrib['x'] = str(label.pad)
            label.root.attrib['y'] = str(label.pad + fontsize)
        return self

    def move_to(self, x, y):
        self.root.moveto(x, y)
        return self

    def margin_right(self, margin):
        self.width += margin
        self.move_to(margin, 0)
        return self

    def margin_bottom(self, margin):
        self.height += margin
        self.move_to(0, margin)
        return self

    def add_label(self, label, fontsize=48, pad=10):
        fig = sg.SVGFigure()
        label_el = sg.TextElement(pad, pad + fontsize, label,
                                  size=fontsize, weight="bold")
        label_el.pad = pad
        fig.append([
            self.root,
            label_el
        ])
        return Figure(fig.getroot(), self.height, self.width, labels=[label_el, *self.labels])

    @classmethod
    def from_file(cls, svg_path: str):
        fig = sg.fromfile(svg_path)
        root = fig.getroot()
        height = float(fig.height.replace('pt', ''))
        width = float(fig.width.replace('pt', ''))
        return cls(root, height, width)

    def __add__(self, other):
        fig = sg.SVGFigure()
        fig.append([
            self.root,
            other.scale_height(self.height)
                 .move_to(self.width, 0)
                 .root
        ])
        return Figure(fig.getroot(), self.height, self.width + other.width, labels=[*self.labels, *other.labels])

    def __truediv__(self, other):
        fig = sg.SVGFigure()
        fig.append([
            self.root,
            other.scale_width(self.width)
                 .move_to(0, self.height)
                 .root
        ])
        return Figure(fig.getroot(), self.height + other.height, self.width, labels=[*self.labels, *other.labels])

    def save_svg(self, path):
        fig = sg.SVGFigure(self.width, self.height)
        fig.append([self.root])
        fig.save(path)
        return self

    def save_pdf(self, path):
        with tempfile.NamedTemporaryFile(suffix='.svg') as tmp:
            self.save_svg(tmp.name)
            cairosvg.svg2pdf(
                url=tmp.name, write_to=path, parent_width=self.width, parent_height=self.height)
        return self

    def save_png(self, path):
        with tempfile.NamedTemporaryFile(suffix='.svg') as tmp:
            self.save_svg(tmp.name)
            cairosvg.svg2png(
                url=tmp.name, write_to=path, parent_width=self.width, parent_height=self.height)
        return self

    def save(self, path):
        if path.endswith('.svg'):
            return self.save_svg(path)
        elif path.endswith('.pdf'):
            return self.save_pdf(path)
        elif path.endswith('.png'):
            return self.save_png(path)


def read_figure(self, path):
    '''
    '''
    return Figure.from_file(path)


def create_panel(figures: List[List[str]], width=1000, margin=0, fontsize=24, letters=None, label_pad=0):
    '''
    '''
    letters = letters or iter_letters()
    kwargs = dict(width=width, margin=margin,
                  fontsize=fontsize, letters=letters)

    if isinstance(figures, str):
        return Figure.from_file(figures).add_label(next(letters), fontsize=fontsize, pad=label_pad)
    elif isinstance(figures, list):
        if len(figures) == 1:
            return create_panel(figures[0], **kwargs)
        elif len(figures) == 0:
            raise ValueError(
                "Invalid input: row is empty and it must have at least one element")

        def _reduce(x, y):
            if isinstance(x, list) and isinstance(y, list):
                return create_panel(x, **kwargs).margin_bottom(margin) / create_panel(y, **kwargs)
            else:
                return create_panel(x, **kwargs).margin_right(margin) + create_panel(y, **kwargs)
        return reduce(_reduce, figures)
    elif isinstance(figures, Figure):
        return figures
    else:
        raise ValueError(
            f"figures={figures} must be a list or str but found type={type(figures)}")
