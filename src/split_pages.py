"""
Split scanned double-page book images into separate pages.

Behavior
--------
- Images wider than WIDTH_THRESHOLD are treated as double-page scans
- Images below the threshold are skipped
- Split is vertical with a conservative overlap margin
- Output files:
    original_a.jpg
    original_b.jpg

Usage
-----
uv run split_pages.py scans/

Custom threshold:
uv run split_pages.py scans/ --threshold 6600

Custom overlap margin:
uv run split_pages.py scans/ --margin 50

Install
-------
uv add pillow
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from PIL import Image

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
    ".bmp",
    ".webp",
}

DEFAULT_THRESHOLD = 6600
DEFAULT_MARGIN = 30


def split_image(
    image_path: Path,
    output_dir: Path,
    margin: int,
    threshold: int,
) -> None:
    with Image.open(image_path) as img:
        width, height = img.size

        if width <= threshold:
            if output_dir != image_path.parent:
                destination = output_dir / image_path.name
                shutil.copy2(image_path, destination)

                print(
                    f"Copied {image_path.name} "
                    f"({width}px) -> {destination.name}"
                )
            else:
                print(f"Skipping {image_path.name} ({width}px)")

            return

        midpoint = width // 2

        # Conservative overlap around the center
        left_box = (
            0,
            0,
            min(width, midpoint + margin),
            height,
        )

        right_box = (
            max(0, midpoint - margin),
            0,
            width,
            height,
        )

        left_img = img.crop(left_box)
        right_img = img.crop(right_box)

        stem = image_path.stem
        suffix = image_path.suffix

        left_output = output_dir / f"{stem}_a{suffix}"
        right_output = output_dir / f"{stem}_b{suffix}"

        left_img.save(left_output)
        right_img.save(right_output)

        print(f"Split {image_path.name}")
        print(f"  -> {left_output.name}")
        print(f"  -> {right_output.name}")


def collect_images(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [path]
        raise ValueError(f"Unsupported image format: {path}")

    if path.is_dir():
        return sorted(
            p
            for p in path.iterdir()
            if p.is_file()
            and p.suffix.lower() in SUPPORTED_EXTENSIONS
        )

    raise ValueError(f"Path does not exist: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split scanned double-page images vertically."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input image or directory",
    )

    parser.add_argument(
        "--margin",
        type=int,
        default=DEFAULT_MARGIN,
        help=f"Overlap margin in pixels (default: {DEFAULT_MARGIN})",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=(
            "Minimum width in pixels required to split "
            f"(default: {DEFAULT_THRESHOLD})"
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: same directory as input)",
    )

    args = parser.parse_args()

    images = collect_images(args.input)

    if not images:
        print("No supported images found.")
        return

    output_dir = args.output or (
        args.input
        if args.input.is_dir()
        else args.input.parent
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    for image_path in images:
        try:
            split_image(
                image_path=image_path,
                output_dir=output_dir,
                margin=args.margin,
                threshold=args.threshold,
            )
        except Exception as exc:
            print(f"Failed to process {image_path}: {exc}")


if __name__ == "__main__":
    main()