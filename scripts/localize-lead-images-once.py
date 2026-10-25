#!/usr/bin/env python3
"""One-time migration of three credited public-domain editorial photographs.
Runs on an isolated review branch; fails rather than silently substituting images.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from PIL import Image
import io
import time

ITEMS = [
    ("blog/posts/2026-10-22-cop17-biodiversity-connectivity/index.qmd",
     "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/NAIP%20image.png",
     "usgs-naip-river-floodplain.png"),
    ("blog/posts/2026-10-21-american-farmers-livelihoods/index.qmd",
     "https://commons.wikimedia.org/wiki/Special:FilePath/20201017-FPAC-Harvest0050_TONED.jpg?width=1600",
     "usda-maryland-soybean-harvest.jpg"),
    ("blog/posts/2026-10-21-why-american-farmers-work-off-farm/index.qmd",
     "https://commons.wikimedia.org/wiki/Special:FilePath/20220518-FPAC-PJK-0912_TONED.jpg?width=1600",
     "usda-new-york-tractor-refuelling.jpg"),
]

def get(url):
    for attempt in range(4):
        try:
            req = Request(url, headers={
                "User-Agent": "EKO-Perspectives-Editorial/1.0 (locally archiving attributed public-domain images)",
                "Accept": "image/avif,image/webp,image/png,image/jpeg,image/*;q=0.8",
            })
            with urlopen(req, timeout=35) as r:
                data = r.read(18_000_001)
                if len(data) > 18_000_000:
                    raise ValueError("Image exceeds 18 MB limit")
                return data
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == 3:
                raise
            print(f"Download attempt {attempt + 1} failed: {error}", flush=True)
            time.sleep((attempt + 1) * 3)

for rel, source, filename in ITEMS:
    page = Path(rel)
    content = page.read_text(encoding="utf-8")
    target = page.parent / filename
    if source not in content:
        if target.exists() and filename in content:
            print(f"Already migrated {filename}")
            continue
        raise RuntimeError(f"Expected external image URL missing in {rel}")
    data = get(source)
    with Image.open(io.BytesIO(data)) as img:
        img.verify()
    with Image.open(io.BytesIO(data)) as img:
        expected = "PNG" if filename.endswith(".png") else "JPEG"
        if img.format != expected or img.width < 700 or img.height < 300:
            raise ValueError(f"Unexpected file type or dimensions: {img.format}, {img.size}")
        print(f"{filename}: {img.size[0]}x{img.size[1]}, {len(data)} bytes")
    target.write_bytes(data)
    page.write_text(content.replace(source, filename), encoding="utf-8")
print("All three locally hosted images validated and source references updated.")
