"""Tests for the CLI"""

from pathlib import Path

from PIL import Image

from png2svg.cli import build_parser, main


def create_png(tmp_path: Path) -> Path:
    """Create a small PNG image for CLI tests"""
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    png_path = tmp_path / "input.png"
    img.save(png_path)
    return png_path


def test_parser_defaults(tmp_path: Path) -> None:
    """Check the default parser values"""
    png_path = create_png(tmp_path)
    args = build_parser().parse_args([str(png_path)])

    assert args.size == 10
    assert args.step == 1
    assert args.scale == 1
    assert args.output is None


def test_default_output_name(tmp_path: Path) -> None:
    """Check default output uses input filename"""
    png_path = create_png(tmp_path)

    res = main([str(png_path)])

    # Check CLI returns 0 (successful execution)
    assert res == 0

    # Check SVG file with same name was created
    assert png_path.with_suffix(".svg").is_file()


def test_custom_options(tmp_path: Path) -> None:
    """Check custom output, size and scale option"""
    png_path = create_png(tmp_path)
    output_path = tmp_path / "custom.svg"

    # Run CLI with cutsom output, size, scale
    res = main(
        [
            str(png_path),
            "-o",
            str(output_path),
            "--size",
            "5",
            "--scale",
            "2",
        ]
    )

    assert res == 0
    assert output_path.is_file()


def test_missing_input_file(tmp_path: Path) -> None:
    """Check that a missing input returns exit code 1"""
    missing_path = tmp_path / "missing.png"

    res = main([str(missing_path)])

    # Check CLI returns 1 (input file not found)
    assert res == 1


def test_zero_size(tmp_path: Path) -> None:
    """Check that a size 0 returns exit code 2"""
    png_path = create_png(tmp_path)

    res = main([str(png_path), "--size", "0"])

    assert res == 2
