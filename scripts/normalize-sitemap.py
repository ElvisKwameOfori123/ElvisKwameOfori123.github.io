#!/usr/bin/env python3
"""Make the Quarto sitemap agree with the site's canonical URLs and real edit dates.

1. URLs. Quarto renders directory pages as .../index.html. The HTML pages emit
   clean canonical URLs, so <loc> entries are rewritten to match:
     /index.html       -> /
     /path/index.html  -> /path/
   Standalone pages such as /about.html are left unchanged.

2. lastmod. Quarto writes the build time into every <lastmod>, so each deploy
   claims that all pages changed. Search engines learn to ignore lastmod on
   sites that do this. Each <lastmod> is instead taken from the last git commit
   that touched the page's source (for a folder page such as a post, any file in
   its folder, so a replaced image counts). Listing pages also take the newest
   date of the pages they list. If git history is unavailable or shallow, the
   lastmod elements are removed rather than left wrong.
"""
from __future__ import annotations

import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SITE_HOST = "kwameofori123.com"
OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SITEMAP = OUTPUT_DIR / "sitemap.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SOURCE_SUFFIXES = (".qmd", ".md", ".ipynb", ".Rmd")
# Listing pages and the folders whose posts they list.
LISTINGS = {"/": ["blog/posts"], "/blog/": ["blog/posts"]}


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


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


@lru_cache(maxsize=None)
def last_commit(path: str) -> str:
    return git("log", "-1", "--format=%cI", "--", path)


def source_for(path: str) -> str | None:
    """Return the source file or folder that produces a site path."""
    rel = path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        folder = rel.rstrip("/")
        for suffix in SOURCE_SUFFIXES:
            candidate = Path(folder or ".") / f"index{suffix}"
            if candidate.exists():
                return folder or candidate.as_posix()
        return None
    stem = rel[: -len(".html")] if rel.endswith(".html") else rel
    for suffix in SOURCE_SUFFIXES:
        candidate = Path(stem + suffix)
        if candidate.exists():
            return candidate.as_posix()
    return None


def lastmod_for(path: str) -> str:
    dates = []
    source = source_for(path)
    if source:
        dates.append(last_commit(source))
    for folder in LISTINGS.get(path, []):
        dates.append(last_commit(folder))
    dates = [d for d in dates if d]
    return max(dates, key=as_utc) if dates else ""


def as_utc(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(timezone.utc)


if not SITEMAP.exists():
    raise SystemExit(f"Expected generated sitemap not found: {SITEMAP}")

history_ok = git("rev-parse", "--is-shallow-repository") == "false"

ET.register_namespace("", NS)
tree = ET.parse(SITEMAP)
root = tree.getroot()

seen: set[str] = set()
duplicates: list[ET.Element] = []
changed = dated = undated = 0

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
        continue
    seen.add(new)

    lastmod = url_el.find(f"{{{NS}}}lastmod")
    value = lastmod_for(urlsplit(new).path) if history_ok else ""
    if value:
        if lastmod is None:
            lastmod = ET.SubElement(url_el, f"{{{NS}}}lastmod")
        lastmod.text = value
        dated += 1
    elif lastmod is not None:
        url_el.remove(lastmod)
        undated += 1

for url_el in duplicates:
    root.remove(url_el)

tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)
note = "" if history_ok else " (git history unavailable or shallow, so lastmod was removed)"
print(
    f"Normalized sitemap: {changed} URL(s) changed, {len(duplicates)} duplicate(s) removed, "
    f"{len(seen)} URL(s) retained; lastmod from git for {dated}, removed for {undated}{note}."
)
