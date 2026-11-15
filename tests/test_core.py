""" "Test functions for png2svg core module"""

import math
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image

from png2svg import convert
from png2svg.core import build_svg, hexagon_points, iter_hex_centers, sample_color


def test_grid_covers_image() -> None:
    # generate hexagon centers for an image of 100 * 80 pixels
    # each hexagon has a size of 10
    centers = list(iter_hex_centers(100, 80, 10))

    # find largest x coordinate
    # add 10 (hexagon size) to check that the grid reaches
    # beyond right edge of image
    assert max(x for x, y in centers) + 10 >= 100

    # find largest y coordinate
    # add 10 (hexagon size) to check that the grid reaches
    # beyond bottom edge of image
    assert max(y for x, y in centers) + 10 >= 80


def test_odd_columns_are_shifted() -> None:
    centers = list(iter_hex_centers(60, 60, 10))

    # extract all y coordinates from first and second column
    first_column = [y for x, y in centers if x == 0]
    second_column = [y for x, y in centers if x == 15]

    # calculate expected vertical shift
    # half vertical distance between 2 hexagon centers
    expected = first_column[0] + math.sqrt(3) * 10 / 2

    # pytest.approx() allows small difference
    assert second_column[0] == pytest.approx(expected)


def test_invalid_size() -> None:
    # check that size 0 raises ValueError
    with pytest.raises(ValueError):
        list(iter_hex_centers(60, 60, 0))


def test_uniform_color() -> None:
    # Create a 40*40 RGB image filled with one colour
    img = Image.new("RGB", (40, 40), (10, 20, 30))

    # Sample colour at the center of image
    res = sample_color(img, 20, 20, 8)

    # every samplex pixel has the same colour
    assert res == (10, 20, 30)


def test_outside_img() -> None:
    img = Image.new("RGB", (10, 10), (200, 100, 50))

    # sample outside the image
    res = sample_color(img, -5, -5, 8)

    # coordinates outside image should be handled safely
    # use nearest valid pixel
    assert res == (200, 100, 50)


def test_average_half() -> None:
    # create 20*20 black RGB image
    img = Image.new("RGB", (20, 20), (0, 0, 0))

    # create white image section
    white_half = Image.new("RGB", (10, 20), (255, 255, 255))
    img.paste(white_half, (10, 0))

    res = sample_color(img, 10, 10, 8)

    # average should be grey : red = green = blue
    assert res[0] == res[1] == res[2]

    # grey colore between 100 and 155
    assert 100 <= res[0] <= 155


def test_hexagon_corners() -> None:
    points = hexagon_points(50, 50, 10)

    # hexagon must have 6 corners
    assert len(points) == 6

    # every corner must be 10 units from the centers
    for x, y in points:
        # straight-line distance
        distance = math.hypot(x - 50, y - 50)
        assert distance == pytest.approx(10)


def test_svg_valid_xml_polygons() -> None:
    img = Image.new("RGB", (60, 40), (255, 0, 0))

    svg = build_svg(img, size=10)

    # parse the svg as XML
    root = ET.fromstring(svg)

    # find all polygon elements in SVG namespace
    namespace = "{http://www.w3.org/2000/svg}"
    polygons = root.findall(f".//{namespace}polygon")

    # check SVG contains more than 10 polygons
    assert len(polygons) > 10

    # check that first polygon is red
    assert polygons[0].get("fill") == "#ff0000"


def test_scale() -> None:
    img = Image.new("RGB", (60, 40), (255, 0, 0))

    svg = build_svg(img, size=10, scale=4)

    root = ET.fromstring(svg)

    # SVG width sclaed from 60 to 240
    assert root.get("width") == "240"

    # check viewBox keeps original image dimensions
    assert root.get("viewBox") == "0 0 60 40"


def test_convert_writes_svg(tmp_path: Path) -> None:
    """Check a small red RGB image"""
    img = Image.new("RGB", (30, 30), (255, 0, 0))

    # save image as png in pytest's temporary directory
    src = tmp_path / "input.png"
    img.save(src)

    # choose output svg path
    out = tmp_path / "output.svg"

    # convert the png to svg
    convert(src, out, size=6)

    # read generated svg file and check its xml declaration
    assert out.read_text(encoding="utf-8").startswith("<?xml")
