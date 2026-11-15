"""CLI for png2svg"""

import argparse
from pathlib import Path

from png2svg import convert


def build_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(prog="png2svg")

    # Add required input image path
    # Path converts str into a Pth object
    parser.add_argument("input", type=Path, help="Input image")

    # Add optional output SVG path
    # specified with -o or --output
    parser.add_argument("-o", "--output", type=Path, help="Output SVG file")

    # Add hexagon size option
    # convert value to float and use default = 10
    parser.add_argument("--size", type=float, default=10, help="Hexagon size")

    # Add sampling step option
    # 1 by default
    parser.add_argument("--step", type=int, default=1, help="Sampling step")

    # Add output scale option
    # 1 by default
    parser.add_argument("--scale", type=float, default=1, help="Output scale")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run CLI and return exit code"""

    parser = build_parser()

    # Read and parse the arguments entered by user
    args = parser.parse_args(argv)

    # Check hexagon size > 0
    # Return exit code 2 if value is invalid
    if args.size <= 0:
        print("Error: size must be positive")
        return 2

    # Check that output scale > 0
    if args.scale <= 0:
        print("Error: scale must be positive")
        return 2

        # Check that sampling step > 1
        if args.step < 1:
            print("Error: step must be at least 1")
            return 2

    # Check if input path points to existing file
    # return exit code 1 if file doesn't exist
    if not args.input.is_file():
        print(f"Error: input file not found: {args.input}")
        return 1

    # Choose output path :
    # - use path provide with -o/ --output
    # - or, replace input file extension with .svg

    if args.output is not None:
        output_path = args.output

    else:
        output_path = args.input.with_suffix(".svg")

    # Convert input image into SVG file
    convert(args.input, output_path, size=args.size, step=args.step, scale=args.scale)

    # Display success message with output file path
    print(f"wrote {output_path}")
    return 0


# Run CLI only when file is executed directly
if __name__ == "__main__":
    raise SystemExit(main())
