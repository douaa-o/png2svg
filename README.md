# png2svg

Convert images into SVG artwork using a hexagonal grid. Choose the hexagon size and orientation to create your own visual style.


## Example 

The following example shows the original image and the generated SVG.

### Original image 

![Original picture](docs/images/screenshot.jpg)

### Generated SVG

![Generated wallpaper](docs/images/wallpaper.svg)


## Installation

Clone the repository and install the project dependencies using uv: 

```bash
git clone https://github.com/douaa-o/png2svg.git
cd png2svg
uv sync --all-groups
```


## Command-line usage

Convert an image into an SVG:

```bash
uv run png2svg screenshot.png
```

By default, the output file has the same name as the input image, with an .svg extension.

You can customize the conversion:

```bash
uv run png2svg screenshot.png -o wallpaper.svg --size 15 --step 2 --scale 2 --orientation pointy
```

To see all available options : 

```bash
uv run png2svg --help
```

## CLI options 

| Option | Description | Default |
|---|---|---|
| `input` | Path to the input image | Required |
| `-o`, `--output` | Output SVG file path | Input filename with `.svg`extension |
| `--size` | Hexagon size | `10` |
| `--step` | Pixel sampling step | `1` |
| `--scale` | Output scale factor | `1` |
| `--orientation` | Hexagon orientation (`flat`or `pointy`) | `flat` |
| `-help` | Display help information | - | 


## Library usage

You can also use `png2svg`directly from Python:

```python 
from pathlib import Path
from png2svg import convert

input_path = Path("screenshot.png")
output_path = Path("wallpaper.svg")

convert(
    input_path, 
    output_path, 
    size=10, 
    step=1, 
    scale=1, 
    orientation="flat")
```
The `convert()`function reads the input image, generates the SVG, saves it to the specified output path and returns the output path. 


## Interactive notebooks 

The project includes two Marimo notebooks. 

### 1. Hexagonal grid exploration 

Explore the hexagonal grid and its geometry: 

```bash
uv run marimo edit notebooks/png2svg_kata.py
```

### 2. Interactive SVG explorer

Upload an image, adjust the hexagon size and orientation, preview the generated SVG and download it :

```bash
uv run marimo edit notebooks/png2svg_explorer.py
```

To launch the explorer as an application : 

```bash
uv run marimo run notebooks/png2svg_explorer.py
```

## Algorithm 

The conversion process follows four main steps :

1. **Generate hexagon centers** Create a hexagonal grid covering the image. The spacing and offset depend on the selected orientation. 

2. **Sample image colors** For each hexagon center, sample surrounding pixels and calculate their average RGB color. 

3. **Generate hexagons** Calculate the six corner coordinates of each hexagon according to its size and orientation.

4. **Build the SVG** Create an SVG document containing colored polygons and save it to the output file. 

# Project layout 

```text
png2svg/
├── .github/
|   └── workflows/
|       └── tests.yml
├── notebooks/ 
|   ├── png2svg_kata.py
|   └── png2svg_explorer.py
├── src/
|   └── png2svg/
|       ├── __init__.py
|       ├── core.py
|       └── cli.py
├── tests/
|   ├── test_core.py
|   └── test_cli.py
├── docs/ 
|   └──images/ 
|      ├── screenshot.png
|      └── wallpaper.svg
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```