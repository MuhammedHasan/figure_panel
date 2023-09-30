import string
import tempfile
from itertools import product
from functools import reduce
from typing import List
from PIL import Image
import svgutils.transform as sg


def import_wand():
    '''Import optional wand package'''
    try:
        from wand.image import Image as WandImage
    except ImportError as exc:
        raise ImportError(
            "You must install wand package to save png, tiff, jpeg. "
            "`conda install -c conda-forge wand`"
        ) from exc
    return WandImage


def import_cairosvg():
    '''Import optional cairosvg package'''
    try:
        import cairosvg
    except ImportError as exc:
        raise ImportError(
            'You must install cairosvg package to save pdf, png, tiff, jpeg.'
            '`conda install -c conda-forge cairosvg`'
        ) from exc
    return cairosvg


def iter_letters():
    """Iterate over letters from a to z and then aa, ab, ac, ..."""
    i = 1
    while True:
        for s in product(string.ascii_lowercase, repeat=i):
            yield ''.join(s)
        i += 1


class Figure:
    '''
    Figure class to create figure panels from svg files.

    Args:
        root (svgutils.transform.SVGFigure): Root svg element
        height (float): Height of the figure
        width (float): Width of the figure
        labels (List[svgutils.transform.TextElement]): List of labels

    Attributes:
        root (svgutils.transform.SVGFigure): Root svg element
        height (float): Height of the figure
        width (float): Width of the figure
        labels (List[svgutils.transform.TextElement]): List of labels
    '''

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
    def from_file(cls, path: str):
        if str(path).endswith('.svg'):
            return cls.from_svg(path)
        elif str(path).endswith('.png'):
            return cls.from_png(path)
        else:
            raise ValueError(
                f"Invalid file type: {path}. Supported types are: .svg, .png")

    @classmethod
    def from_svg(cls, svg_path: str):
        fig = sg.fromfile(svg_path)
        root = fig.getroot()
        height = float(fig.height.replace('pt', ''))
        width = float(fig.width.replace('pt', ''))
        return cls(root, height, width)

    @classmethod
    def from_png(cls, png_path: str):
        img = Image.open(png_path)
        height = float(img.height)
        width = float(img.width)
        root = sg.ImageElement(open(png_path, 'rb'), width, height)
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
            cairosvg = import_cairosvg()
            cairosvg.svg2pdf(
                url=tmp.name, write_to=path, parent_width=self.width, parent_height=self.height)
        return self

    def save_png(self, path):
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            self.save_pdf(tmp.name)
            WandImage = import_wand()
            with WandImage(filename=tmp.name) as img:
                img.format = 'png'
                img.save(filename=path)
        return self

    def save_jpeg(self, path):
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            self.save_pdf(tmp.name)
            WandImage = import_wand()
            with WandImage(filename=tmp.name) as img:
                img.format = 'jpeg'
                img.save(filename=path)
        return self

    def save_tiff(self, path):
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            self.save_pdf(tmp.name)
            WandImage = import_wand()
            with WandImage(filename=tmp.name) as img:
                img.format = 'tiff'
                img.compression = 'lzw'
                img.save(filename=path)
        return self

    def save(self, path):
        if path.endswith('.svg'):
            return self.save_svg(path)
        elif path.endswith('.pdf'):
            return self.save_pdf(path)
        elif path.endswith('.png'):
            return self.save_png(path)
        elif path.endswith('.jpeg'):
            return self.save_png(path)
        elif path.endswith('.tiff'):
            return self.save_tiff(path)
        else:
            raise ValueError(
                f'Unsupported format file for: {path}'
                'Supported formats are: .svg, .jpeg, .pdf, .png, .tiff'
            )


def read_figure(self, path):
    '''
    Read svg file and return Figure object
    '''
    return Figure.from_file(path)


def create_panel(figures: List[List[str]], width=1000,
                 margin=0, fontsize=24, letters=None, label_pad=0):
    '''
    Create figure panel from svg files

    Args:
        figures (List[List[str]]): List of svg files
        width (int): Width of the panel
        margin (int): Margin between figures
        fontsize (int): Fontsize of the labels
        letters (Iterator[str]): Iterator over letters
        label_pad (int): Padding of the labels
    '''
    return _create_panel(figures, margin=margin,
                         fontsize=fontsize, letters=letters,
                         label_pad=label_pad)[0].scale_width(width)


def _create_panel(figures: List[List[str]], margin=0, fontsize=24, letters=None, label_pad=0):
    '''
    '''
    letters = letters or iter_letters()
    kwargs = dict(margin=margin, fontsize=fontsize, letters=letters)

    if isinstance(figures, str):
        return [
            Figure
            .from_file(figures)
            .add_label(next(letters), fontsize=fontsize, pad=label_pad)
        ]
    elif isinstance(figures, Figure):
        return [figures]
    elif isinstance(figures, list):
        if len(figures) == 0:
            raise ValueError(
                "Invalid input: row is empty and it must have at least one element")
        elif len(figures) == 1:
            if isinstance(figures[0], str):
                return _create_panel(figures[0], **kwargs)
            else:
                return figures
        else:
            def _reduce(x, y):
                _x = _create_panel(x, **kwargs)[0]
                _y = _create_panel(y, **kwargs)[0]

                if isinstance(x, list) and isinstance(y, list):
                    return [_x.margin_bottom(margin) / _y]
                else:
                    return _x.margin_right(margin) + _y

            panel = reduce(_reduce, figures)
            return [panel] if not isinstance(panel, list) else panel
    else:
        raise ValueError(
            f"figures={figures} must be a list but found type={type(figures)}")
