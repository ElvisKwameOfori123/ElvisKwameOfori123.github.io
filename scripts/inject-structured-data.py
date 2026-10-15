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
AUTHOR_ID = AUTHOR_URL + "#main-author"


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
            "@id": AUTHOR_ID,
            "@type": "Person",
            "name": author,
            "url": AUTHOR_URL,
            "sameAs": [ORCID_URL],
        },
        "publisher": {"@id": AUTHOR_ID},
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

# Help search engines connect the publication name and its author profile to
# the same Person entity used in article markup.
home = ROOT / "index.html"
if home.exists():
    text = home.read_text(encoding="utf-8", errors="replace")
    if 'id="eko-website-jsonld"' not in text and "</head>" in text:
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "EKO Perspectives",
            "url": "https://kwameofori123.com/",
            "description": "Research, evidence and ideas on policy, agriculture, land use, economics, science, technology and development.",
            "publisher": {"@id": AUTHOR_ID},
        }
        block = (
            '\n<script id="eko-website-jsonld" type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "\n</script>\n"
        )
        home.write_text(text.replace("</head>", block + "</head>", 1), encoding="utf-8")
        print("Injected WebSite JSON-LD into homepage.")

about = ROOT / "about.html"
if about.exists():
    text = about.read_text(encoding="utf-8", errors="replace")
    if 'id="eko-profile-jsonld"' not in text and "</head>" in text:
        data = {
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "url": AUTHOR_URL,
            "mainEntity": {
                "@id": AUTHOR_ID,
                "@type": "Person",
                "name": "Elvis Kwame Ofori",
                "url": AUTHOR_URL,
                "image": "https://kwameofori123.com/assets/profile.jpg",
                "jobTitle": "PhD Researcher and Research Assistant in Plant & AgriBiosciences",
                "affiliation": {
                    "@type": "Organization",
                    "name": "University of Galway",
                    "url": "https://www.universityofgalway.ie/",
                },
                "sameAs": [
                    ORCID_URL,
                    "https://github.com/ElvisKwameOfori123",
                    "https://scholar.google.com/citations?user=cf5X1eAAAAAJ&hl=en",
                    "https://www.linkedin.com/in/elvis-ofori-12139b71/",
                ],
            },
        }
        block = (
            '\n<script id="eko-profile-jsonld" type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "\n</script>\n"
        )
        about.write_text(text.replace("</head>", block + "</head>", 1), encoding="utf-8")
        print("Injected ProfilePage JSON-LD into About page.")


# Women Behind the Science: generate original visual cards and add ProfilePage
# structured data. These cards are editorial graphics, not likenesses. They
# provide a rights-safe visual until a portrait with clear reuse terms exists.
PROFILE_SOURCE = Path("people") / "women" / "profiles"
PROFILE_OUTPUT = ROOT / "people" / "women" / "profiles"
WOMEN_ARCHIVE = ROOT / "people" / "women" / "index.html"
WOMEN_SCHEMA_ID = "eko-women-profile-jsonld"
WOMEN_COLLECTION_SCHEMA_ID = "eko-women-collection-jsonld"


def source_frontmatter(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8", errors="replace")
    if not raw.startswith("---"):
        return {}
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}
    out: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r'^([A-Za-z0-9_-]+):\s*"(.*)"\s*$', line)
        if match:
            out[match.group(1)] = match.group(2)
    return out


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def initials(name: str) -> str:
    bits = [part for part in re.split(r"\s+", name.strip()) if part]
    if not bits:
        return "W"
    return "".join(part[0].upper() for part in bits[:2])


def wrap_words(value: str, limit: int, max_lines: int) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if len(trial) <= limit or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
            if len(lines) >= max_lines:
                break
    if len(lines) < max_lines and current:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = lines[-1].rstrip(" .") + "…"
    return lines[:max_lines]


def svg_text_lines(lines: list[str], x: int, y: int, size: int, step: int, family: str, weight: int = 400, fill: str = "#111111") -> str:
    spans = []
    for idx, line in enumerate(lines):
        dy = "0" if idx == 0 else str(step)
        spans.append(f'<tspan x="{x}" dy="{dy}">{xml_escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">' + "".join(spans) + "</text>"
    )


def social_svg(name: str, field: str, question: str) -> str:
    question_lines = wrap_words(question, 42, 3)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(name)} | Women Behind the Science</title>
<desc id="desc">Original EKO Perspectives research card for {xml_escape(name)}, {xml_escape(field)}.</desc>
<rect width="1600" height="900" fill="#fcfaf6"/>
<circle cx="1370" cy="145" r="285" fill="none" stroke="#d9d3c9" stroke-width="3"/>
<circle cx="210" cy="790" r="210" fill="none" stroke="#d9d3c9" stroke-width="3"/>
<text x="120" y="120" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700" letter-spacing="2" fill="#2c5f7c">WOMEN BEHIND THE SCIENCE</text>
<text x="120" y="300" font-family="Georgia, 'Times New Roman', serif" font-size="112" font-weight="600" fill="#111111">{xml_escape(name)}</text>
<text x="120" y="372" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="600" fill="#5d5a55">{xml_escape(field)}</text>
{svg_text_lines(question_lines, 120, 510, 50, 64, "Georgia, 'Times New Roman', serif", 500, "#111111")}
<text x="120" y="820" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="700" letter-spacing="2" fill="#2c5f7c">EKO PERSPECTIVES</text>
</svg>'''


def portrait_svg(name: str, field: str, question: str) -> str:
    question_lines = wrap_words(question, 30, 4)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1200" viewBox="0 0 960 1200" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(name)} | research card</title>
<desc id="desc">Original typographic research card for {xml_escape(name)}, used where portrait reuse rights are not yet clear.</desc>
<rect width="960" height="1200" fill="#fcfaf6"/>
<circle cx="800" cy="160" r="250" fill="none" stroke="#d9d3c9" stroke-width="3"/>
<circle cx="110" cy="1100" r="190" fill="none" stroke="#d9d3c9" stroke-width="3"/>
<text x="72" y="88" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" letter-spacing="2" fill="#2c5f7c">WOMEN BEHIND THE SCIENCE</text>
<text x="72" y="390" font-family="Georgia, 'Times New Roman', serif" font-size="210" font-weight="500" letter-spacing="-8" fill="#111111">{xml_escape(initials(name))}</text>
{svg_text_lines(wrap_words(name, 22, 2), 72, 560, 58, 66, "Georgia, 'Times New Roman', serif", 600, "#111111")}
<text x="72" y="708" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="600" fill="#5d5a55">{xml_escape(field)}</text>
{svg_text_lines(question_lines, 72, 805, 31, 42, "Georgia, 'Times New Roman', serif", 500, "#111111")}
<text x="72" y="1130" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="700" letter-spacing="2" fill="#2c5f7c">EKO PERSPECTIVES</text>
</svg>'''


def replace_meta_content(text: str, attr: str, key: str, new_value: str) -> str:
    pattern1 = re.compile(
        rf'(<meta[^>]+{attr}=["\']{re.escape(key)}["\'][^>]+content=["\'])([^"\']*)(["\'][^>]*>)',
        flags=re.I,
    )
    pattern2 = re.compile(
        rf'(<meta[^>]+content=["\'])([^"\']*)(["\'][^>]+{attr}=["\']{re.escape(key)}["\'][^>]*>)',
        flags=re.I,
    )
    if pattern1.search(text):
        return pattern1.sub(lambda m: m.group(1) + html.escape(new_value, quote=True) + m.group(3), text, count=1)
    if pattern2.search(text):
        return pattern2.sub(lambda m: m.group(1) + html.escape(new_value, quote=True) + m.group(3), text, count=1)
    return text


profile_items: list[dict[str, str]] = []
if PROFILE_OUTPUT.exists():
    for profile_html in sorted(PROFILE_OUTPUT.glob("*.html")):
        slug = profile_html.stem
        source = PROFILE_SOURCE / f"{slug}.qmd"
        fm = source_frontmatter(source)
        if not fm:
            continue

        text = profile_html.read_text(encoding="utf-8", errors="replace")
        url = canonical(text)
        description = meta(text, "name", "description") or fm.get("description")
        name = fm.get("name")
        role = fm.get("role")
        institution = fm.get("institution")
        field = fm.get("field")
        focus = fm.get("focus")
        question = fm.get("question")
        if not all([url, description, name, role, institution, field, question]):
            continue

        social_name = f"{slug}-card.svg"
        portrait_name = f"{slug}-research-card.svg"
        (PROFILE_OUTPUT / social_name).write_text(
            social_svg(name, field, question), encoding="utf-8"
        )
        (PROFILE_OUTPUT / portrait_name).write_text(
            portrait_svg(name, field, question), encoding="utf-8"
        )

        folder_url = url.rsplit("/", 1)[0] + "/"
        social_url = folder_url + social_name
        portrait_url = folder_url + portrait_name
        alt = f"Original EKO Perspectives research card for {name}"

        text = replace_meta_content(text, "property", "og:image", social_url)
        text = replace_meta_content(text, "property", "og:image:alt", alt)
        text = replace_meta_content(text, "name", "twitter:image", social_url)
        text = replace_meta_content(text, "name", "twitter:image:alt", alt)

        if 'class="profile-research-visual"' not in text:
            visual = (
                '\n<div class="profile-research-visual" aria-label="Profile overview">'
                f'<img class="profile-research-image" src="{html.escape(portrait_name, quote=True)}" '
                f'alt="{html.escape(alt, quote=True)}" loading="eager">'
                '<div class="profile-research-copy">'
                '<p class="profile-research-label">Research question</p>'
                f'<p class="profile-research-field">{html.escape(field)}</p>'
                f'<p class="profile-research-question">{html.escape(question)}</p>'
                "</div></div>\n"
            )
            title_block = re.search(
                r'(<header[^>]+id=["\']title-block-header["\'][\s\S]*?</header>)',
                text,
                flags=re.I,
            )
            if title_block:
                text = (
                    text[: title_block.end()]
                    + visual
                    + text[title_block.end() :]
                )

        if f'id="{WOMEN_SCHEMA_ID}"' not in text:
            person: dict[str, object] = {
                "@type": "Person",
                "name": name,
                "url": url,
                "jobTitle": role,
                "affiliation": {"@type": "Organization", "name": institution},
                "description": description,
                "knowsAbout": [value for value in [field, focus] if value],
            }
            data = {
                "@context": "https://schema.org",
                "@type": "ProfilePage",
                "name": f"{name} | Women Behind the Science",
                "description": description,
                "url": url,
                "primaryImageOfPage": {"@type": "ImageObject", "url": social_url},
                "mainEntity": person,
                "isPartOf": {
                    "@type": "CollectionPage",
                    "name": "Women Behind the Science",
                    "url": "https://kwameofori123.com/people/women/",
                },
            }
            block = (
                f'\n<script id="{WOMEN_SCHEMA_ID}" type="application/ld+json">\n'
                + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                + "\n</script>\n"
            )
            if "</head>" in text:
                text = text.replace("</head>", block + "</head>", 1)

        profile_html.write_text(text, encoding="utf-8")
        profile_items.append({"name": name, "url": url, "portrait": portrait_name})

# Replace the archive's rights-safe monogram fallback with the generated,
# researcher-specific editorial cards. If a future source template supplies a
# licensed portrait, it can replace these without changing the archive layout.
if WOMEN_ARCHIVE.exists() and profile_items:
    text = WOMEN_ARCHIVE.read_text(encoding="utf-8", errors="replace")
    for item in profile_items:
        name = item["name"]
        portrait = item["portrait"]
        pattern = re.compile(
            rf'(<a href=["\']profiles/{re.escape(Path(portrait).stem.replace("-research-card", ""))}\.html["\'][^>]*>\s*'
            r'<div class="person-image-wrap">)([\s\S]*?)(</div>\s*<div class="person-card-body">)',
            flags=re.I,
        )
        replacement = (
            r'\1'
            + f'<img class="person-research-card" loading="lazy" '
            + f'src="profiles/{html.escape(portrait, quote=True)}" '
            + f'alt="Original EKO Perspectives research card for {html.escape(name, quote=True)}">'
            + r'\3'
        )
        text = pattern.sub(replacement, text, count=1)

    if f'id="{WOMEN_COLLECTION_SCHEMA_ID}"' not in text and "</head>" in text:
        item_list = [
            {
                "@type": "ListItem",
                "position": idx,
                "url": item["url"],
                "name": item["name"],
            }
            for idx, item in enumerate(profile_items, start=1)
        ]
        description = meta(text, "name", "description") or (
            "A growing portrait archive celebrating women whose research and "
            "leadership have shaped land, food, climate and development."
        )
        data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Women Behind the Science",
            "description": description,
            "url": "https://kwameofori123.com/people/women/",
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(item_list),
                "itemListElement": item_list,
            },
            "isPartOf": {
                "@type": "WebSite",
                "name": "EKO Perspectives",
                "url": "https://kwameofori123.com/",
            },
        }
        block = (
            f'\n<script id="{WOMEN_COLLECTION_SCHEMA_ID}" type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "\n</script>\n"
        )
        text = text.replace("</head>", block + "</head>", 1)

    WOMEN_ARCHIVE.write_text(text, encoding="utf-8")
    print(
        f"Enhanced {len(profile_items)} Women Behind the Science profile(s) "
        "with original research-card visuals and ProfilePage JSON-LD."
    )
