#!/usr/bin/env python3
"""Export AstroWiki content."""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path

from common import parse_frontmatter, project_root, read_text, wiki_pages, write_text


def export_jsonl(root: Path, output: Path) -> None:
    rows = []
    for path in wiki_pages(root):
        text = read_text(path)
        fm, body = parse_frontmatter(text)
        rows.append({"path": str(path.relative_to(root)), "slug": path.stem, "frontmatter": fm, "body": body})
    write_text(output, "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")


def export_bundle(root: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in wiki_pages(root):
            zf.write(path, path.relative_to(root))
        for name in ["wiki/index.md", "wiki/schema.md", "wiki/log.md"]:
            p = root / name
            if p.exists():
                zf.write(p, p.relative_to(root))


def extract_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    block: list[str] = []
    for line in text.splitlines():
        if "|" in line:
            block.append(line)
        else:
            if len(block) >= 2 and re.search(r"\|\s*:?-{3,}:?\s*\|", block[1]):
                tables.append(parse_table(block))
            block = []
    if len(block) >= 2 and re.search(r"\|\s*:?-{3,}:?\s*\|", block[1]):
        tables.append(parse_table(block))
    return tables


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for i, line in enumerate(lines):
        if i == 1:
            continue
        cells = [strip_md(c.strip()) for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def strip_md(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`]", "", text)
    return text


def export_tables(root: Path, source: Path, output: Path) -> None:
    tables = extract_tables(read_text(source))
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".csv":
        for i, table in enumerate(tables or [[]], 1):
            path = output if len(tables) <= 1 else output.with_name(f"{output.stem}_{i}.csv")
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerows(table)
            print(f"wrote {path}")
    else:
        raise SystemExit("Only CSV table export is dependency-free in V1. Use .csv output.")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    j = sub.add_parser("jsonl")
    j.add_argument("--output", default="outputs/exports/wiki.jsonl")
    b = sub.add_parser("bundle")
    b.add_argument("--output", default="outputs/exports/wiki-bundle.zip")
    t = sub.add_parser("tables")
    t.add_argument("source")
    t.add_argument("--output", required=True)
    args = parser.parse_args()
    root = project_root()
    if args.cmd == "jsonl":
        export_jsonl(root, root / args.output)
    elif args.cmd == "bundle":
        export_bundle(root, root / args.output)
    elif args.cmd == "tables":
        export_tables(root, root / args.source, root / args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
