#!/usr/bin/env python3
"""Approval queue for AstroWiki inbox pages."""

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime, timezone
from pathlib import Path

from astrowiki_common import PAGE_DIRS, dump_json, load_json, parse_frontmatter, project_root, read_text, write_text


def inbox_pages(root: Path) -> list[Path]:
    pages: list[Path] = []
    for d in PAGE_DIRS.values():
        path = root / "inbox" / d
        if path.exists():
            pages.extend(sorted(p for p in path.glob("*.md") if p.name != ".gitkeep"))
    return pages


def find_inbox(root: Path, slug: str) -> Path:
    matches = [p for p in inbox_pages(root) if p.stem == slug]
    if not matches:
        raise SystemExit(f"No inbox page found for slug: {slug}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple inbox pages match slug: {slug}")
    return matches[0]


def wiki_target(root: Path, inbox_path: Path) -> Path:
    rel = inbox_path.relative_to(root / "inbox")
    return root / "wiki" / rel


def update_index(root: Path, target: Path) -> None:
    text = read_text(root / "wiki" / "index.md")
    slug = target.stem
    if f"[[{slug}]]" in text:
        return
    section = target.parent.name.replace("_", " ").title()
    lines = text.rstrip().splitlines()
    header = f"## {section}"
    try:
        idx = lines.index(header)
        lines.insert(idx + 1, f"- [[{slug}]]")
    except ValueError:
        lines.extend(["", header, "", f"- [[{slug}]]"])
    write_text(root / "wiki" / "index.md", "\n".join(lines) + "\n")


def approve(root: Path, slug: str) -> None:
    src = find_inbox(root, slug)
    target = wiki_target(root, src)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    src.unlink()
    update_index(root, target)
    manifest = load_json(root / ".kb" / "manifest.json", {"version": 1, "files": {}, "pages": {}})
    manifest.setdefault("pages", {})[slug] = {
        "status": "approved",
        "path": str(target.relative_to(root)),
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    dump_json(root / ".kb" / "manifest.json", manifest)
    with (root / "wiki" / "log.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n[{datetime.now(timezone.utc).isoformat()}] APPROVE {slug} -> {target.relative_to(root)}\n")
    print(f"approved {slug} -> {target.relative_to(root)}")


def reject(root: Path, slug: str, reason: str) -> None:
    src = find_inbox(root, slug)
    out = root / "outputs" / "reviews" / f"rejected-{slug}.md"
    write_text(out, f"# Rejected: {slug}\n\nReason: {reason}\n\nOriginal: `{src.relative_to(root)}`\n")
    src.unlink()
    print(f"rejected {slug}; note written to {out.relative_to(root)}")


def archive(root: Path, slug: str) -> None:
    src = find_inbox(root, slug)
    target = root / "wiki" / "archive" / src.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(target))
    print(f"archived {slug} -> {target.relative_to(root)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    diff = sub.add_parser("diff")
    diff.add_argument("slug")
    app = sub.add_parser("approve")
    app.add_argument("slug")
    rej = sub.add_parser("reject")
    rej.add_argument("slug")
    rej.add_argument("--reason", required=True)
    arc = sub.add_parser("archive")
    arc.add_argument("slug")
    args = parser.parse_args()
    root = project_root()
    if args.cmd == "list":
        for p in inbox_pages(root):
            fm, _ = parse_frontmatter(read_text(p))
            print(f"{p.stem}\t{p.relative_to(root)}\t{fm.get('title', '')}")
    elif args.cmd == "diff":
        src = find_inbox(root, args.slug)
        target = wiki_target(root, src)
        old = read_text(target).splitlines(keepends=True) if target.exists() else []
        new = read_text(src).splitlines(keepends=True)
        print("".join(difflib.unified_diff(old, new, fromfile=str(target), tofile=str(src))))
    elif args.cmd == "approve":
        approve(root, args.slug)
    elif args.cmd == "reject":
        reject(root, args.slug, args.reason)
    elif args.cmd == "archive":
        archive(root, args.slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
