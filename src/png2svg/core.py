"""Core functions for converting images into hexagonal SVGs"""

import math

from PIL import Image


def iter_hex_centers(width: int, height: int, size: float):
    """Generate hexagon centers for a given image"""

    if size <= 0:
        raise ValueError("Size must be strictly positive")

    # horizontal distance between 2 columns
    horizontal_step = 1.5 * size

    # vertical distance between 2 centers in same column
    vertical_step = math.sqrt(3) * size

    # distance to shift every other column
    half_vertical_step = vertical_step / 2

    # start at first column
    x = 0.0
    column_index = 0

    # generate columns until grid reaches beyond right edge
    while x < width + size:
        # odd columns start halfway down
        # even columns start at y=0
        y = half_vertical_step if column_index % 2 else 0.0

        # generate centers vertically within this column
        while y <= height + half_vertical_step:
            # return current hexagon center
            yield (x, y)

            # move down to next hexagon
            y += vertical_step

        # move to next column
        x += horizontal_step
        column_index += 1


def limit(value: int, minimum: int, maximum: int) -> int:
    """keep value within the given boundaries"""
    return max(minimum, min(value, maximum))


def sample_color(
    img: Image.Image, cx: float, cy: float, size: float, step: int = 1
) -> tuple[int, int, int]:
    """ "Sample the average colour inside a hexagon"""
    # cx and cy the hexagon center coordinates
    # step is the distance between sampled pixels; default=1

    # convert image to RGB format
    img = img.convert("RGB")

    width, height = img.size

    # radius of sampling area in the hexagon
    radius = size * math.sqrt(3) / 2
    int_radius = max(1, int(radius))

    # initialization
    red_sum = 0
    green_sum = 0
    blue_sum = 0

    count = 0  # number of sampled pixels

    # loop vertically
    for dy in range(-int_radius, int_radius + 1, step):
        # loop horizontally
        for dx in range(-int_radius, int_radius + 1, step):
            # check whether the point is inside the circle
            if dx * dx + dy * dy <= radius * radius or count == 0:
                # calculate and limit pixel coordinates
                x = limit(int(cx + dx), 0, width - 1)
                y = limit(int(cy + dy), 0, height - 1)

                # read RGB color of current pixel
                pixel = img.getpixel((x, y))

                if isinstance(pixel, tuple) and len(pixel) == 3:
                    red, green, blue = pixel

                    red_sum += red
                    green_sum += green
                    blue_sum += blue

                    count += 1

    return (red_sum // count, green_sum // count, blue_sum // count)


def hexagon_points(cx: float, cy: float, size: float) -> list[tuple[float, float]]:
    """Return the six corner points of a hexagon"""
    # cx, cy position of the center
    # size = distance from the center to each corner

    points = []

    # generate 6 corners, spaced 60 degrees apart
    for i in range(6):
        angle = math.radians(60 * i)

        # corner coordinates
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)

        points.append((x, y))

    return points


def format_color(red: int, green: int, blue: int) -> str:
    """convert RGB values into hexadecimal color"""
    return f"#{red:02x}{green:02x}{blue:02x}"


def build_svg(img: Image.Image, size: float, step: int = 1, scale: int = 1) -> str:
    """Generate SVG image from a Pillow Image"""
    # size = distance from hexagon center to each corner
    # step = distance between sampled pixels when averging colors
    # scale = multiplier for output SVG dimensions

    width, height = img.size

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width * scale}" '
            f'height="{height * scale}" '
            f'viewBox ="0 0 {width} {height}">'
        ),
    ]

    # generate one polygon for each hexagon center
    for cx, cy in iter_hex_centers(width, height, size):
        # sample average color
        red, green, blue = sample_color(img, cx, cy, size, step)

        # format RGB color as hexadecimal string
        color = format_color(red, green, blue)

        # calculate the 6 corner points
        points = hexagon_points(cx, cy, size)

        # format points with 2 decimal places
        points_string = " ".join(f"{x:.2f}, {y:.2f}" for x, y in points)

        # add polygon to SVG
        lines.append(
            f'<polygon points="{points_string}" '
            f'fill="{color}" '
            f'stroke="{color}" '
            f'stroke-width="0.5"/>'
        )

    # close SVG document
    lines.append("</svg>")

    return "\n".join(lines)
