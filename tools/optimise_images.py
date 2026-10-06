#!/usr/bin/env python3
"""Resize and recompress oversized JPEG photographs for kwameofori123.com.

Run from the repository root:

    python tools/optimise_images.py            # report and optimise in place
    python tools/optimise_images.py --dry-run  # report only, change nothing

Rules
-----
* Only JPEG files tracked under the content folders are considered.
  Charts and diagrams (PNG/SVG) are left alone.
* A photograph is processed if it is wider than --max-width pixels or
  larger than --max-kb kilobytes.
* Images are scaled down (never up) to --max-width, EXIF orientation is
  applied, the colour profile is kept, and the file is saved as a
  progressive, optimised JPEG at --quality.
* The new file is written only if it is at least --min-saving percent
  smaller than the original, so re-running the script is safe.

Requires Pillow (pip install pillow).
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: pip install pillow")

CONTENT_DIRS = ("blog", "research", "how-i-got-here", "projects", "people", "assets")
JPEG_SUFFIXES = {".jpg", ".jpeg"}


def find_jpegs(root: Path) -> list[Path]:
    files: list[Path] = []
    for folder in CONTENT_DIRS:
        base = root / folder
        if base.is_dir():
            files.extend(
                p for p in base.rglob("*")
                if p.suffix.lower() in JPEG_SUFFIXES and "_site" not in p.parts
            )
    return sorted(files)


def encode(path: Path, max_width: int, quality: int) -> tuple[bytes, tuple[int, int]]:
    with Image.open(path) as src:
        icc = src.info.get("icc_profile")
        img = ImageOps.exif_transpose(src)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        if img.width > max_width:
            height = round(img.height * max_width / img.width)
            img = img.resize((max_width, height), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        save_kwargs = dict(format="JPEG", quality=quality, optimize=True,
                           progressive=True, subsampling="4:2:0")
        if icc:
            save_kwargs["icc_profile"] = icc
        img.save(buf, **save_kwargs)
        return buf.getvalue(), img.size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--max-width", type=int, default=1600)
    parser.add_argument("--max-kb", type=int, default=400)
    parser.add_argument("--quality", type=int, default=82)
    parser.add_argument("--min-saving", type=float, default=15.0,
                        help="minimum percentage reduction required to overwrite")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    total_before = total_after = 0
    changed = 0

    for path in find_jpegs(root):
        size_before = path.stat().st_size
        with Image.open(path) as probe:
            width, height = probe.size
        if width <= args.max_width and size_before <= args.max_kb * 1024:
            continue

        data, new_size = encode(path, args.max_width, args.quality)
        saving = 100 * (1 - len(data) / size_before)
        rel = path.relative_to(root)

        if saving < args.min_saving:
            print(f"skip  {rel}  ({size_before // 1024} KB, saving only {saving:.0f}%)")
            continue

        action = "would" if args.dry_run else "wrote"
        print(f"{action} {rel}  {width}x{height} {size_before // 1024} KB"
              f"  ->  {new_size[0]}x{new_size[1]} {len(data) // 1024} KB  (-{saving:.0f}%)")
        total_before += size_before
        total_after += len(data)
        changed += 1
        if not args.dry_run:
            path.write_bytes(data)

    if changed:
        print(f"\n{changed} image(s): {total_before // 1024} KB -> {total_after // 1024} KB"
              f"  (saved {(total_before - total_after) // 1024} KB)")
    else:
        print("No images needed changing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
