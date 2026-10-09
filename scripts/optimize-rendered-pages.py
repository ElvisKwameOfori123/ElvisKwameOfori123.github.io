#!/usr/bin/env python3
"""Serve right-sized images and make the category row keyboard-reachable.

Measured before this step (phone, 390 px): the Writing page downloaded 4.0 MB
of images for cards about 360 px wide, the homepage 1.7 MB, and How I got here
2.0 MB, because every page used the full 1,280-1,600 px originals.

1. Responsive images. For each local JPEG or PNG wider than 1,000 px that a
   page shows, write 480, 960 and 1200 px copies (where smaller than the
   original) beside the original in _site, and add srcset/sizes so phones
   and card thumbnails pick a smaller file.
   Originals and their URLs are unchanged, so og:image, social cards and
   structured data still use full-size images. Source files are never edited.
2. Lazy loading. Content images after the first on a page get
   loading="lazy" and decoding="async" unless they already set loading.
3. Category row. Quarto's listing category list scrolls sideways on phones
   but contains no focusable element, so keyboard users cannot reach it. It
   gets tabindex="0", role="group" and an aria-label.

If Pillow is not installed, step 1 is skipped with a message and the site is
otherwise unaffected.
"""
from __future__ import annotations

import html
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
WIDTHS = (480, 960, 1200)
MIN_WIDTH = 1000
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
ATTR_RE = r'\b{name}\s*=\s*(["\'])(.*?)\1'
MAIN_SPLIT = 'id="quarto-document-content"'

try:
    from PIL import Image
except ImportError:  # pragma: no cover - depends on the build machine
    Image = None


def attr(tag: str, name: str) -> str | None:
    match = re.search(ATTR_RE.format(name=name), tag, re.I | re.S)
    return html.unescape(match.group(2)) if match else None


def set_attr(tag: str, name: str, value: str) -> str:
    safe = html.escape(value, quote=True)
    if attr(tag, name) is not None:
        return re.sub(ATTR_RE.format(name=name), f'{name}="{safe}"', tag, count=1, flags=re.I | re.S)
    return tag[:-1].rstrip().rstrip("/") + f' {name}="{safe}">'


def sizes_for(tag: str) -> str:
    cls = attr(tag, "class") or ""
    if "thumbnail-image" in cls:
        return "(max-width: 767px) 100vw, 360px"
    return "(max-width: 767px) 100vw, 760px"


variants_cache: dict[Path, list[tuple[str, int]] | None] = {}


def variants(original: Path) -> list[tuple[str, int]] | None:
    """Create resized copies once per image; return (filename, width) pairs."""
    if original in variants_cache:
        return variants_cache[original]
    result = None
    if Image is not None and original.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        with Image.open(original) as im:
            width, height = im.size
            if width > MIN_WIDTH:
                result = []
                for target in (w for w in WIDTHS if w < width * 0.9):
                    name = f"{original.stem}-w{target}{original.suffix.lower()}"
                    out = original.with_name(name)
                    if not out.exists():
                        resized = im.resize((target, round(height * target / width)), Image.LANCZOS)
                        if out.suffix in {".jpg", ".jpeg"}:
                            resized.convert("RGB").save(out, quality=80, optimize=True, progressive=True)
                        else:
                            resized.save(out, optimize=True)
                    result.append((name, target))
                result.append((original.name, width))
    variants_cache[original] = result
    return result


if not ROOT.exists():
    raise SystemExit(f"Rendered site directory not found: {ROOT}")
if Image is None:
    print("Pillow not installed: responsive image copies skipped.")

stats = {"srcset": 0, "lazy": 0, "category": 0, "files": 0}
for page in sorted(ROOT.rglob("*.html")):
    if "site_libs" in page.parts:
        continue
    text = page.read_text(encoding="utf-8", errors="replace")
    if MAIN_SPLIT not in text:
        continue
    head, _, body = text.partition(MAIN_SPLIT)
    seen_images = 0

    def fix(match: re.Match[str]) -> str:
        global seen_images
        tag = match.group(0)
        src = attr(tag, "src") or ""
        parts = urlsplit(src)
        local = not parts.scheme and not parts.netloc and not src.startswith("data:")
        if local and src and attr(tag, "srcset") is None:
            target = (page.parent / unquote(parts.path)).resolve()
            if target.is_file() and ROOT.resolve() in target.parents:
                found = variants(target)
                if found:
                    base = src[: len(src) - len(Path(parts.path).name)] if "/" in src else ""
                    srcset = ", ".join(f"{base}{name} {w}w" for name, w in found)
                    tag = set_attr(tag, "srcset", srcset)
                    tag = set_attr(tag, "sizes", sizes_for(tag))
                    stats["srcset"] += 1
        seen_images += 1
        if seen_images > 1 and attr(tag, "loading") is None:
            tag = set_attr(tag, "loading", "lazy")
            if attr(tag, "decoding") is None:
                tag = set_attr(tag, "decoding", "async")
            stats["lazy"] += 1
        return tag

    seen_images = 0
    updated = head + MAIN_SPLIT + IMG_RE.sub(fix, body)
    # The category list lives in the margin sidebar, outside the main column.
    updated, n = re.subn(
        r'<div class="quarto-listing-category(?P<rest>[^"]*)">',
        r'<div class="quarto-listing-category\g<rest>" tabindex="0" role="group" aria-label="Categories">',
        updated,
    )
    stats["category"] += n
    if updated != text:
        page.write_text(updated, encoding="utf-8")
        stats["files"] += 1

made = sum(len(v) - 1 for v in variants_cache.values() if v)
print(
    f"Optimized {stats['files']} page(s): srcset on {stats['srcset']} image(s) using {made} resized cop(ies), "
    f"lazy loading on {stats['lazy']}, keyboard access on {stats['category']} category row(s)."
)
