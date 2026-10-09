#!/usr/bin/env python3
"""Normalize Quarto's generated sitemap to the site's canonical URL form.

Quarto writes directory index pages as .../index.html in sitemap.xml even when
the rendered pages declare clean trailing-slash canonicals. Google recommends
that sitemap URLs and rel=canonical agree. This script changes only sitemap
<loc> values ending in /index.html; real standalone .html pages are untouched.
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

SITE = "https://kwameofori123.com"
OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SITEMAP = OUTPUT_DIR / "sitemap.xml"

if not SITEMAP.exists():
    raise SystemExit(f"Expected generated sitemap not found: {SITEMAP}")

ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse(SITEMAP)
root = tree.getroot()
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

changed = 0
for loc in root.findall(".//sm:loc", ns):
    if not loc.text:
        continue
    url = loc.text.strip()
    parts = urlsplit(url)
    if parts.path == "/index.html":
        new_path = "/"
    elif parts.path.endswith("/index.html"):
        new_path = parts.path[: -len("index.html")]
    else:
        continue
    loc.text = urlunsplit((parts.scheme, parts.netloc, new_path, parts.query, parts.fragment))
    changed += 1

tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)
print(f"Normalized {changed} sitemap URL(s) to clean canonical directory URLs.")
