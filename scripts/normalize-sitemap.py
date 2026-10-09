#!/usr/bin/env python3
"""Normalize Quarto sitemap URLs to the site's canonical public URL form.

Quarto renders directory pages as .../index.html. The HTML pages already emit
clean canonical URLs, so this post-render step makes sitemap <loc> entries agree
with those canonicals:
  /index.html       -> /
  /path/index.html  -> /path/

Ordinary standalone pages such as /about.html are left unchanged.
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

SITE_HOST = "kwameofori123.com"
OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SITEMAP = OUTPUT_DIR / "sitemap.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.hostname != SITE_HOST:
        return url.strip()

    path = parts.path
    if path == "/index.html":
        path = "/"
    elif path.endswith("/index.html"):
        path = path[: -len("index.html")]

    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


if not SITEMAP.exists():
    raise SystemExit(f"Expected generated sitemap not found: {SITEMAP}")

ET.register_namespace("", NS)
tree = ET.parse(SITEMAP)
root = tree.getroot()

seen: set[str] = set()
duplicates: list[ET.Element] = []
changed = 0

for url_el in root.findall(f"{{{NS}}}url"):
    loc = url_el.find(f"{{{NS}}}loc")
    if loc is None or not (loc.text or "").strip():
        continue

    old = (loc.text or "").strip()
    new = normalize_url(old)
    if new != old:
        loc.text = new
        changed += 1

    if new in seen:
        duplicates.append(url_el)
    else:
        seen.add(new)

for url_el in duplicates:
    root.remove(url_el)

tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)
print(
    f"Normalized sitemap: {changed} URL(s) changed, "
    f"{len(duplicates)} duplicate(s) removed, {len(seen)} URL(s) retained."
)
