#!/usr/bin/env python3
"""Keep every rendered URL a visitor or crawler can follow in the clean form.

Quarto renders directory pages as .../index.html, while this site's canonical
URLs use the trailing-slash form (/blog/posts/x/). This post-render pass makes
the generated output agree with the canonicals:

  1. href attributes in rendered HTML: index.html -> ./, a/index.html -> a/;
  2. search.json, so site-search results open clean URLs;
  3. alias (redirect) pages: clean destination, plus a canonical link, an
     instant meta refresh and a plain link, so the redirect works and is
     understood without JavaScript;
  4. og:url, added from rel=canonical where Quarto does not emit it;
  5. the homepage's hidden Quarto title block, so the masthead is the only H1.

Standalone pages such as /about.html are not changed. listings.json is left
alone on purpose: quarto.js matches its /index.html entries internally to
highlight categories, and nothing in it is a link.
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SITE_HOST = "kwameofori123.com"
SITE_URL = f"https://{SITE_HOST}/"
HREF_RE = re.compile(r'(?P<prefix>\bhref\s*=\s*)(?P<quote>["\'])(?P<url>.*?)(?P=quote)', re.I)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
CANONICAL_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
REDIRECT_MAP_RE = re.compile(r"var redirects = (\{.*?\});", re.S)


def clean_path(path: str) -> str | None:
    """Return the clean form of an index.html path, or None if unchanged."""
    if path == "index.html":
        return "./"
    if path.endswith("/index.html"):
        return path[: -len("index.html")]
    return None


def normalize_url(value: str) -> str:
    raw = html.unescape(value)
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return value
    parts = urlsplit(raw)
    if parts.scheme and parts.scheme not in {"http", "https"}:
        return value
    if parts.netloc and parts.hostname != SITE_HOST:
        return value
    new_path = clean_path(parts.path)
    if new_path is None:
        return value
    if new_path == "./" and parts.netloc:
        new_path = "/"
    return urlunsplit((parts.scheme, parts.netloc, new_path, parts.query, parts.fragment))


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE_URL
    if rel.endswith("/index.html"):
        return SITE_URL + rel[: -len("index.html")]
    return SITE_URL + rel


if not ROOT.exists():
    raise SystemExit(f"Rendered site directory not found: {ROOT}. Run quarto render first.")

counts = {"links": 0, "files": 0, "search": 0, "aliases": 0, "og_url": 0, "home_title": 0}

# 3. Alias pages first, so their rewritten destinations are not touched twice.
alias_pages: set[Path] = set()
for path in sorted(ROOT.rglob("*.html")):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = REDIRECT_MAP_RE.search(text)
    if "<title>Redirect</title>" not in text or not match:
        continue
    redirects = json.loads(match.group(1))
    target_rel = redirects.get("") or "/"
    target_abs = normalize_url(urljoin(page_url(path), target_rel))
    if not target_abs.startswith(SITE_URL):
        raise SystemExit(f"Alias {path} points outside the site: {target_abs}")
    target_local = "/" + target_abs[len(SITE_URL):]
    redirects = {k: normalize_url(urljoin(page_url(path), v))[len(SITE_URL) - 1:] for k, v in redirects.items()}
    safe = html.escape(target_abs, quote=True)
    text = text.replace(match.group(1), json.dumps(redirects))
    head_extra = (
        f'  <link rel="canonical" href="{safe}">\n'
        f'  <meta http-equiv="refresh" content="0; url={html.escape(target_local, quote=True)}">\n'
    )
    if 'rel="canonical"' not in text:
        text = text.replace("<head>", "<head>\n" + head_extra, 1)
    if "<p>This page has moved" not in text:
        text = text.replace(
            "<body>",
            f'<body>\n<p>This page has moved to <a href="{html.escape(target_local, quote=True)}">{safe}</a>.</p>',
            1,
        )
    path.write_text(text, encoding="utf-8")
    alias_pages.add(path)
    counts["aliases"] += 1

# 1, 4 and 5. Ordinary rendered pages.
for path in sorted(ROOT.rglob("*.html")):
    if path in alias_pages or "site_libs" in path.parts:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    def repl(match: re.Match[str]) -> str:
        old = match.group("url")
        new = normalize_url(old)
        if new != old:
            counts["links"] += 1
            new = html.escape(new, quote=True)
        return f'{match.group("prefix")}{match.group("quote")}{new}{match.group("quote")}'

    text = HREF_RE.sub(repl, text)

    canonical_tag = CANONICAL_RE.search(text)
    if canonical_tag and 'property="og:url"' not in text:
        href = CANONICAL_HREF_RE.search(canonical_tag.group(0))
        if href:
            tag = f'<meta property="og:url" content="{href.group(1)}">'
            text = text.replace(canonical_tag.group(0), canonical_tag.group(0) + "\n" + tag, 1)
            counts["og_url"] += 1

    if path == ROOT / "index.html" and 'class="publication-masthead"' in text:
        text, n = re.subn(
            r'<header id="title-block-header"[^>]*>.*?</header>', "", text, count=1, flags=re.S
        )
        counts["home_title"] += n

    if text != original:
        path.write_text(text, encoding="utf-8")
        counts["files"] += 1

# 2. Site search index.
search = ROOT / "search.json"
if search.exists():
    entries = json.loads(search.read_text(encoding="utf-8"))
    for entry in entries:
        href = entry.get("href")
        if isinstance(href, str):
            new = normalize_url(href)
            if new != href:
                entry["href"] = new
                counts["search"] += 1
    search.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

print(
    f"Normalized {counts['links']} internal index.html link(s) across {counts['files']} HTML file(s); "
    f"{counts['search']} search entr(ies); {counts['aliases']} alias page(s); "
    f"added og:url to {counts['og_url']} page(s); removed {counts['home_title']} hidden homepage title block(s)."
)
