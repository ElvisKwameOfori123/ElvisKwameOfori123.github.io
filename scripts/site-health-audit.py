#!/usr/bin/env python3
"""Audit rendered Quarto output for crawl/indexing hygiene.

Uses only the Python standard library so it can run in GitHub Actions without
extra dependencies. It writes a short Markdown report and exits non-zero only
for issues that should block a merge.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

SITE = "https://kwameofori123.com"
ROOT = Path("_site")
REPORT = Path("site-health-report.md")

errors: list[str] = []
warnings: list[str] = []
facts: list[str] = []


def add_error(msg: str) -> None:
    errors.append(msg)


def add_warning(msg: str) -> None:
    warnings.append(msg)


def canonical_from_html(text: str) -> str | None:
    patterns = [
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.I)
        if m:
            return m.group(1).strip()
    return None


def rendered_file_for_url(url: str) -> Path | None:
    path = urlparse(url).path
    if path == "/":
        candidate = ROOT / "index.html"
    elif path.endswith("/"):
        candidate = ROOT / path.lstrip("/") / "index.html"
    else:
        candidate = ROOT / path.lstrip("/")
    return candidate if candidate.exists() else None


if not ROOT.exists():
    add_error("Rendered site directory _site/ does not exist. Run quarto render first.")

sitemap = ROOT / "sitemap.xml"
sitemap_urls: list[str] = []
if not sitemap.exists():
    add_error("Generated _site/sitemap.xml is missing.")
else:
    try:
        tree = ET.parse(sitemap)
        root = tree.getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_urls = [
            (loc.text or "").strip()
            for loc in root.findall(".//sm:loc", ns)
            if (loc.text or "").strip()
        ]
        facts.append(f"Sitemap URLs: {len(sitemap_urls)}")
        if len(sitemap_urls) != len(set(sitemap_urls)):
            add_error("Sitemap contains duplicate URLs.")
        bad_hosts = [u for u in sitemap_urls if not u.startswith(SITE)]
        if bad_hosts:
            add_error(f"Sitemap contains {len(bad_hosts)} URL(s) outside {SITE}.")
        index_urls = [u for u in sitemap_urls if urlparse(u).path.endswith("/index.html")]
        if index_urls:
            add_error(
                f"Sitemap contains {len(index_urls)} explicit /index.html URL(s); "
                "sitemap URLs should match the clean rel=canonical form."
            )
    except ET.ParseError as exc:
        add_error(f"Sitemap XML could not be parsed: {exc}")

robots = ROOT / "robots.txt"
if not robots.exists():
    add_error("Generated _site/robots.txt is missing.")
else:
    robots_text = robots.read_text(encoding="utf-8", errors="replace")
    if "Sitemap: https://kwameofori123.com/sitemap.xml" not in robots_text:
        add_error("robots.txt does not advertise the canonical sitemap URL.")
    if re.search(r"(?im)^\s*Disallow:\s*/\s*$", robots_text):
        add_error("robots.txt blocks the whole site.")

html_files = sorted(ROOT.rglob("*.html")) if ROOT.exists() else []
facts.append(f"Rendered HTML files present: {len(html_files)}")

missing_canonical: list[str] = []
bad_canonical: list[tuple[str, str]] = []
index_canonical: list[tuple[str, str]] = []
canonical_mismatch: list[tuple[str, str, str]] = []
noindex_pages: list[str] = []

# Check only URLs intentionally published in the sitemap. Draft/utility HTML may
# exist in local render output without being discoverable or deployable content.
for url in sitemap_urls:
    path = rendered_file_for_url(url)
    if path is None:
        add_error(f"Sitemap URL has no matching rendered file: {url}")
        continue

    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(ROOT).as_posix()

    if re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex',
        text,
        re.I,
    ):
        noindex_pages.append(rel)

    canonical = canonical_from_html(text)
    if not canonical:
        missing_canonical.append(rel)
        continue
    if not canonical.startswith(SITE):
        bad_canonical.append((rel, canonical))
    if urlparse(canonical).path.endswith("/index.html"):
        index_canonical.append((rel, canonical))
    if canonical.rstrip("/") != url.rstrip("/"):
        canonical_mismatch.append((rel, url, canonical))

facts.append(f"Sitemap pages checked for canonical: {len(sitemap_urls)}")
facts.append(f"Sitemap pages with noindex: {len(noindex_pages)}")
facts.append(f"Sitemap pages without canonical link: {len(missing_canonical)}")
facts.append(f"Pages with explicit /index.html canonical: {len(index_canonical)}")

if noindex_pages:
    add_error(f"{len(noindex_pages)} sitemap page(s) contain noindex.")
if bad_canonical:
    add_error(f"{len(bad_canonical)} sitemap page(s) have canonicals outside the canonical site URL.")
if index_canonical:
    sample = ", ".join(f"{p} -> {u}" for p, u in index_canonical[:5])
    add_error(f"{len(index_canonical)} page(s) canonicalize to /index.html. Examples: {sample}")
if missing_canonical:
    add_error(
        f"{len(missing_canonical)} sitemap page(s) have no rel=canonical: "
        + ", ".join(missing_canonical[:10])
    )
if canonical_mismatch:
    sample = "; ".join(
        f"{p}: sitemap={u}, canonical={c}" for p, u, c in canonical_mismatch[:5]
    )
    add_error(
        f"{len(canonical_mismatch)} sitemap URL(s) disagree with rel=canonical. "
        f"Examples: {sample}"
    )

# Published posts should carry one valid BlogPosting block derived from their
# visible metadata. Google recommends Article/BlogPosting markup with accurate
# author, date, headline and image information when those properties apply.
structured_ok = 0
structured_errors: list[str] = []
for url in sitemap_urls:
    if "/blog/posts/" not in urlparse(url).path:
        continue
    path = rendered_file_for_url(url)
    if path is None:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r'<script id="eko-blogposting-jsonld" type="application/ld\+json">(.*?)</script>',
        text,
        flags=re.I | re.S,
    )
    if not match:
        structured_errors.append(f"{path.relative_to(ROOT)}: missing BlogPosting JSON-LD")
        continue
    try:
        data = __import__("json").loads(match.group(1))
    except Exception as exc:
        structured_errors.append(f"{path.relative_to(ROOT)}: invalid JSON-LD ({exc})")
        continue
    required = ["headline", "description", "datePublished", "author", "mainEntityOfPage"]
    missing = [key for key in required if not data.get(key)]
    if data.get("@type") != "BlogPosting":
        structured_errors.append(f"{path.relative_to(ROOT)}: @type is not BlogPosting")
    elif missing:
        structured_errors.append(
            f"{path.relative_to(ROOT)}: missing structured-data fields {', '.join(missing)}"
        )
    else:
        structured_ok += 1

facts.append(f"Published posts with valid BlogPosting JSON-LD: {structured_ok}")
if structured_errors:
    add_error(
        f"{len(structured_errors)} published post(s) have structured-data errors. "
        + " | ".join(structured_errors[:5])
    )

# Site identity markup: WebSite on the homepage and ProfilePage on About.
for rel, schema_id, expected_type in [
    ("index.html", "eko-website-jsonld", "WebSite"),
    ("about.html", "eko-profile-jsonld", "ProfilePage"),
]:
    path = ROOT / rel
    if not path.exists():
        add_error(f"Expected rendered page missing for structured data: {rel}")
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        rf'<script id="{schema_id}" type="application/ld\+json">(.*?)</script>',
        text,
        flags=re.I | re.S,
    )
    if not match:
        add_error(f"{rel} is missing {expected_type} JSON-LD.")
        continue
    try:
        data = __import__("json").loads(match.group(1))
    except Exception as exc:
        add_error(f"{rel} has invalid {expected_type} JSON-LD: {exc}")
        continue
    if data.get("@type") != expected_type:
        add_error(f"{rel} structured data is not {expected_type}.")
    elif expected_type == "ProfilePage" and not data.get("mainEntity"):
        add_error("about.html ProfilePage JSON-LD has no mainEntity.")

# Draft source files must not survive into production output as blank/indexable HTML.
front_matter = re.compile(r"\\A---\\s*\\n(.*?)\\n---\\s*\\n", re.S)
draft_true = re.compile(r"(?mi)^\\s*draft\\s*:\\s*true\\s*(?:#.*)?$")
rendered_drafts: list[str] = []
for source in sorted(Path(".").rglob("*.qmd")):
    if ROOT in source.parents:
        continue
    source_text = source.read_text(encoding="utf-8", errors="replace")
    match = front_matter.match(source_text)
    if not match or not draft_true.search(match.group(1)):
        continue
    rel = source.relative_to(Path("."))
    if rel.name == "index.qmd":
        target = ROOT / rel.parent / "index.html"
    else:
        target = ROOT / rel.with_suffix(".html")
    if target.exists():
        rendered_drafts.append(target.relative_to(ROOT).as_posix())

facts.append(f"Rendered draft pages remaining: {len(rendered_drafts)}")
if rendered_drafts:
    add_error(
        f"{len(rendered_drafts)} draft page(s) remain in production output: "
        + ", ".join(rendered_drafts[:10])
    )

# The custom homepage masthead should be the page's only H1.
home = ROOT / "index.html"
if home.exists():
    home_text = home.read_text(encoding="utf-8", errors="replace")
    h1_count = len(re.findall(r"<h1\\b", home_text, flags=re.I))
    facts.append(f"Homepage H1 count: {h1_count}")
    if h1_count != 1:
        add_error(f"Homepage should contain exactly one H1; found {h1_count}.")

# Every public page gets WebSite/Person entity markup from includes/head.html.
site_schema_missing: list[str] = []
for url in sitemap_urls:
    path = rendered_file_for_url(url)
    if path is None:
        continue
    page_text = path.read_text(encoding="utf-8", errors="replace")
    if 'id="eko-site-jsonld"' not in page_text:
        site_schema_missing.append(path.relative_to(ROOT).as_posix())
facts.append(f"Sitemap pages with site-level JSON-LD: {len(sitemap_urls) - len(site_schema_missing)}")
if site_schema_missing:
    add_error(
        f"{len(site_schema_missing)} sitemap page(s) lack site-level JSON-LD: "
        + ", ".join(site_schema_missing[:10])
    )

# Internal links on published pages should point to the same clean URL form as
# the sitemap and rel=canonical. This prevents the site itself from continually
# rediscovering duplicate /index.html variants.
index_internal_links: list[tuple[str, str]] = []
for url in sitemap_urls:
    path = rendered_file_for_url(url)
    if path is None:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(ROOT).as_posix()
    for href in re.findall(r'href=["\\\']([^"\\\']+)["\\\']', text, flags=re.I):
        parsed = urlparse(href)
        if parsed.netloc and parsed.hostname != "kwameofori123.com":
            continue
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            continue
        hpath = parsed.path
        if hpath == "index.html" or hpath == "/index.html" or hpath.endswith("/index.html"):
            index_internal_links.append((rel, href))

facts.append(f"Published internal links using explicit /index.html: {len(index_internal_links)}")
if index_internal_links:
    sample = "; ".join(f"{p} -> {h}" for p, h in index_internal_links[:8])
    add_error(
        f"{len(index_internal_links)} internal link(s) still point to explicit /index.html URLs. "
        f"Examples: {sample}"
    )

# Private editorial claim ledgers should never render.
source_ledgers = list(ROOT.rglob("_sources.html")) if ROOT.exists() else []
if source_ledgers:
    add_error(f"{len(source_ledgers)} private _sources ledger(s) rendered into the public site.")

lines = [
    "# Site health audit",
    "",
    "## Summary",
    "",
    f"- Critical errors: **{len(errors)}**",
    f"- Warnings: **{len(warnings)}**",
]
lines.extend(f"- {fact}" for fact in facts)

if errors:
    lines += ["", "## Critical errors", ""]
    lines.extend(f"- {e}" for e in errors)
if warnings:
    lines += ["", "## Warnings", ""]
    lines.extend(f"- {w}" for w in warnings)

lines += [
    "",
    "## Notes",
    "",
    "- This audit checks rendered output, not Search Console's Google-selected canonical.",
    "- An excluded /index.html variant is not itself a problem when the clean URL is canonical and indexed.",
    "- Search Console URL Inspection remains the authority for the two crawled-but-not-indexed URLs.",
    "",
]
REPORT.write_text("\n".join(lines), encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))

if errors:
    sys.exit(1)
