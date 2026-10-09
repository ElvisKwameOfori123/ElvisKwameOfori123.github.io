#!/usr/bin/env python3
"""Remove everything a `draft: true` source publishes, in production builds only.

Quarto leaves small placeholders for draft pages in the output tree, and copies
resources that sit beside the draft (figures, .llms.md companions). None of that
should be deployed while a post waits for editorial approval.

This step only runs for production builds, so local `quarto render` and
`quarto preview` of a draft keep working:
  - GitHub Actions sets CI=true, which counts as production;
  - set EKO_PRODUCTION=1 to force it locally (for example before a manual
    `quarto publish`);
  - set EKO_KEEP_DRAFTS=1 to skip it even in CI.

Removal rules:
  - a draft `index.qmd` whose source folder holds no other published page owns
    its whole output folder, so that folder is deleted;
  - otherwise only that page's own outputs (.html and .llms.md) are deleted.
Shared assets outside a draft's folder are never touched.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

ROOT = Path(".")
OUTPUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SOURCE_SUFFIXES = (".qmd", ".md", ".ipynb", ".Rmd")

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
DRAFT_TRUE = re.compile(r"(?mi)^\s*draft\s*:\s*true\s*(?:#.*)?$")


def production_build() -> bool:
    if os.environ.get("EKO_KEEP_DRAFTS") == "1":
        return False
    return os.environ.get("EKO_PRODUCTION") == "1" or os.environ.get("CI") == "true"


def is_source(path: Path) -> bool:
    if path.suffix not in SOURCE_SUFFIXES:
        return False
    parts = path.relative_to(ROOT).parts
    if parts[0] in {OUTPUT.name, "site_libs", "node_modules"}:
        return False
    # Quarto ignores files and folders starting with _ or . (claim ledgers,
    # includes, editorial notes), and so do we.
    return not any(p.startswith(("_", ".")) for p in parts)


def is_draft(path: Path) -> bool:
    if path.suffix == ".ipynb":
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONT_MATTER.match(text)
    return bool(match and DRAFT_TRUE.search(match.group(1)))


if not production_build():
    print("Draft output kept (not a production build). Set EKO_PRODUCTION=1 to remove it.")
    raise SystemExit(0)

if not OUTPUT.exists():
    raise SystemExit(f"Rendered output directory not found: {OUTPUT}")

sources = [p for p in ROOT.rglob("*") if p.is_file() and is_source(p)]
drafts = {p for p in sources if is_draft(p)}
published = [p for p in sources if p not in drafts]

removed: list[str] = []
for source in sorted(drafts):
    rel = source.relative_to(ROOT)
    out_dir = OUTPUT / rel.parent
    if source.stem == "index" and rel.parent != Path("."):
        owns_folder = not any(rel.parent in p.relative_to(ROOT).parents for p in published)
        if owns_folder and out_dir.exists():
            shutil.rmtree(out_dir)
            removed.append(out_dir.as_posix() + "/")
            continue
    for suffix in (".html", ".llms.md"):
        target = out_dir / f"{source.stem}{suffix}"
        if target.exists():
            target.unlink()
            removed.append(target.as_posix())

print(f"Removed output of {len(drafts)} draft source(s): {len(removed)} path(s).")
for path in removed:
    print(f"  - {path}")
