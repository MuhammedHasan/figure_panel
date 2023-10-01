# Figure_Panel

Create figure panel for publications from svg files.

# Installation
### Creating a Python Environment
```bash
conda create -n figure_panel python=3.9 -y
```

### Activate Created Environment
```bash
conda activate figure_panel
```

### figure_panel installation
```bash
pip install git+https://github.com/MuhammedHasan/figure_panel.git
```

### Cairo-SVG installation
```bash
conda install -c conda-forge cairosvg -y
```

# Usage
```bash
figure_panel -f x.svg,y.svg,z.svg -o fig.pdf --width 1200 --fontsize 24
```

`-f` input svg files separated by `,` indicating figure arrange in the same row
`--width` of figure in pixels and height determined based on the aspect ratio. `--fontsize` is relative to width so need adjustment accordingly.

`-o` output format `.svg`, `.png` and `.pdf` is supported.


```bash
figure_panel -f "[x.svg,y.svg],[z.svg, k.svg]" -o fig.pdf
```

`[]` indicates row in the panel. Figures labeled based on the sequence order in the input.


```bash
figure_panel -f "[x.svg, y.svg],[z.svg, [[x.svg, y.svg], [z.svg, k.svg]]]" -o fig.pdf
```

![](examples/example.png)

See [examples](examples/example.ipynb) for further examples and python api.


## TODOS

- [] Add more test-cases
- [] Margin between figures
- [] Padding between figures and labels
- [] pdf input support
