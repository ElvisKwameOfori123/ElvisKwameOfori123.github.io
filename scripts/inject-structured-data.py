#!/usr/bin/env python3
"""Inject minimal, accurate BlogPosting JSON-LD into rendered EKO posts.

The source Markdown remains the editorial source of truth. This post-render
step derives structured data only from metadata already present in the
rendered HTML, so the schema cannot invent a different title, date, author,
description, canonical URL or lead image.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path("_site")
POSTS = ROOT / "blog" / "posts"
SCHEMA_ID = "eko-blogposting-jsonld"
AUTHOR_URL = "https://kwameofori123.com/about.html"
ORCID_URL = "https://orcid.org/0000-0001-5404-9078"


def meta(text: str, attr: str, value: str) -> str | None:
    patterns = [
        rf'<meta[^>]+{attr}=["\']{re.escape(value)}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+{attr}=["\']{re.escape(value)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return html.unescape(match.group(1).strip())
    return None


def canonical(text: str) -> str | None:
    patterns = [
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return html.unescape(match.group(1).strip())
    return None


def headline(text: str) -> str | None:
    value = meta(text, "property", "og:title")
    if not value:
        match = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
        value = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip() if match else None
    if value and value.endswith(" – EKO Perspectives"):
        value = value[: -len(" – EKO Perspectives")]
    return value


if not POSTS.exists():
    raise SystemExit("Rendered blog/posts directory not found. Run quarto render first.")

count = 0
for path in sorted(POSTS.rglob("index.html")):
    text = path.read_text(encoding="utf-8", errors="replace")
    if f'id="{SCHEMA_ID}"' in text:
        continue

    url = canonical(text)
    title = headline(text)
    description = meta(text, "name", "description")
    author = meta(text, "name", "author")
    published = meta(text, "name", "dcterms.date")
    image = meta(text, "property", "og:image")

    # Draft/utility output may exist locally. Only inject when the rendered
    # page carries the complete public article metadata.
    if not all([url, title, description, author, published]):
        continue
    if author != "Elvis Kwame Ofori":
        raise SystemExit(f"Unexpected article author in {path}: {author}")

    data: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": published,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {
            "@type": "Person",
            "name": author,
            "url": AUTHOR_URL,
            "sameAs": [ORCID_URL],
        },
        "publisher": {
            "@type": "Person",
            "name": author,
            "url": AUTHOR_URL,
        },
        "isPartOf": {
            "@type": "WebSite",
            "name": "EKO Perspectives",
            "url": "https://kwameofori123.com/",
        },
    }
    if image:
        data["image"] = [image]

    block = (
        f'\n<script id="{SCHEMA_ID}" type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + "\n</script>\n"
    )
    if "</head>" not in text:
        raise SystemExit(f"Could not find </head> in {path}")
    text = text.replace("</head>", block + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    count += 1

print(f"Injected BlogPosting JSON-LD into {count} rendered post(s).")
