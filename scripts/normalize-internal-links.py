#!/usr/bin/env python3
"""Rewrite rendered internal links away from explicit /index.html URLs.

Quarto's source navigation may render directory pages as relative index.html
links even when rel=canonical uses the cleaner trailing-slash URL. This pass
keeps visible/internal links aligned with the canonical and sitemap URL form.
Standalone pages such as /about.html are not changed.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path("_site")
SITE_HOST = "kwameofori123.com"
HREF_RE = re.compile(r'(?P<prefix>\bhref\s*=\s*)(?P<quote>["\'])(?P<url>.*?)(?P=quote)', re.I)


def normalize_href(value: str) -> str:
    raw = html.unescape(value)
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return value

    parts = urlsplit(raw)

    # Only rewrite relative links or absolute links to this site.
    if parts.scheme and parts.scheme not in {"http", "https"}:
        return value
    if parts.netloc and parts.hostname != SITE_HOST:
        return value

    path = parts.path
    if path == "index.html":
        new_path = "./"
    elif path == "/index.html":
        new_path = "/"
    elif path.endswith("/index.html"):
        new_path = path[: -len("index.html")]
    else:
        return value

    normalized = urlunsplit((parts.scheme, parts.netloc, new_path, parts.query, parts.fragment))
    # href attributes are already HTML; escape only characters that matter in attributes.
    return html.escape(normalized, quote=True)


if not ROOT.exists():
    raise SystemExit("Rendered site directory _site/ does not exist. Run quarto render first.")

files_changed = 0
links_changed = 0

for path in sorted(ROOT.rglob("*.html")):
    text = path.read_text(encoding="utf-8", errors="replace")

    def repl(match: re.Match[str]) -> str:
        old = match.group("url")
        new = normalize_href(old)
        global links_changed
        if new != old:
            links_changed += 1
        return f'{match.group("prefix")}{match.group("quote")}{new}{match.group("quote")}'

    updated = HREF_RE.sub(repl, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        files_changed += 1

print(f"Normalized {links_changed} internal index.html link(s) across {files_changed} HTML file(s).")
