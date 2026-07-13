#!/usr/bin/env python3
"""Regenerate wiki/index.md and .kb/manifest.json from the actual wiki pages.

Run after bulk-seeding the wiki (e.g. `python tools/reindex.py`). Produces one
section per page type (Sources, Concepts, ...), each listing `- [[slug]] -- Title`,
so the linter's index-reference check passes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from common import PAGE_DIRS, dump_json, load_json, page_slug, parse_frontmatter, project_root, read_text, wiki_pages

SECTION_ORDER = ["sources", "concepts", "methods", "objects", "datasets",
                 "instruments", "entities", "synthesis", "notes"]


def build_index(root: Path) -> str:
    lines = ["# llm-wiki Index", "",
             "> Auto-maintained by `tools/reindex.py` / `tools/queue.py`. "
             "Domain: X-ray TES + FDM readout simulation.", ""]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for subdir in SECTION_ORDER:
        title = subdir.capitalize()
        pages = sorted((root / "wiki" / subdir).glob("*.md"))
        pages = [p for p in pages if p.stem != ".gitkeep"]
        lines.append(f"## {title}")
        if not pages:
            lines.append(f"No approved {subdir} yet.")
        else:
            for p in pages:
                fm, _ = parse_frontmatter(read_text(p))
                t = fm.get("title", page_slug(p))
                lines.append(f"- [[{page_slug(p)}]] — {t}")
        lines.append("")
    lines.append(f"_Last reindexed {now}._")
    return "\n".join(lines) + "\n"


def build_manifest(root: Path) -> dict:
    manifest = load_json(root / ".kb" / "manifest.json",
                         {"version": 1, "files": {}, "pages": {}})
    manifest.setdefault("version", 1)
    manifest.setdefault("files", {})
    pages = manifest.setdefault("pages", {})
    now = datetime.now(timezone.utc).isoformat()
    for path in wiki_pages(root):
        slug = page_slug(path)
        pages[slug] = {
            "status": "approved",
            "path": str(path.relative_to(root)),
            "title": parse_frontmatter(read_text(path))[0].get("title", slug),
            "type": parse_frontmatter(read_text(path))[0].get("type"),
            "approved_at": pages.get(slug, {}).get("approved_at", now),
        }
    return manifest


def main() -> int:
    root = project_root()
    (root / "wiki" / "index.md").write_text(build_index(root), encoding="utf-8")
    dump_json(root / ".kb" / "manifest.json", build_manifest(root))
    pages = wiki_pages(root)
    print(f"reindexed {len(pages)} pages -> wiki/index.md, .kb/manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
