#!/usr/bin/env python3
"""Remove rendered HTML for Quarto sources explicitly marked draft: true.

Quarto may leave tiny draft placeholders in the output tree. They are useful
during local authoring but should not be deployed as 200-status, indexable
pages. This script reads only front matter at the start of .qmd files and
removes the matching rendered HTML after a production render.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(".")
OUTPUT = Path("_site")

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
DRAFT_TRUE = re.compile(r"(?mi)^\s*draft\s*:\s*true\s*(?:#.*)?$")


def output_for_source(source: Path) -> Path:
    rel = source.relative_to(ROOT)
    if rel.name == "index.qmd":
        return OUTPUT / rel.parent / "index.html"
    return OUTPUT / rel.with_suffix(".html")


removed: list[str] = []
for source in sorted(ROOT.rglob("*.qmd")):
    if OUTPUT in source.parents:
        continue
    text = source.read_text(encoding="utf-8", errors="replace")
    match = FRONT_MATTER.match(text)
    if not match or not DRAFT_TRUE.search(match.group(1)):
        continue
    target = output_for_source(source)
    if target.exists():
        target.unlink()
        removed.append(target.as_posix())

print(f"Removed {len(removed)} rendered draft page(s).")
for path in removed:
    print(f"  - {path}")
