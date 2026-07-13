#!/usr/bin/env python3
"""Shared helpers for the llm-wiki tools (ported from AstroWiki, domain-adapted).

The llm-wiki follows the AstroWiki provenance-first architecture
(`raw -> inbox -> wiki -> outputs`). This module defines the page-type
registry, provenance / claim vocabularies, the YAML-subset frontmatter
parser used by the linter, and the helpers for discovering wiki pages.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


# Page type -> directory. `entity` is added for the FDM/TES domain
# (labs, missions, instruments-as-orgs) following the fdm-wiki convention.
PAGE_DIRS = {
    "source": "sources",
    "concept": "concepts",
    "method": "methods",
    "object": "objects",
    "dataset": "datasets",
    "instrument": "instruments",
    "synthesis": "synthesis",
    "entity": "entities",
    "note": "notes",
}

VALID_TYPES = set(PAGE_DIRS)

VALID_PROVENANCE = {
    "user-verified",
    "source-derived",
    "catalog-derived",
    "llm-derived",
    "web-derived",
    "query-derived",
}
TRUSTED_PROVENANCE = {"user-verified", "source-derived", "catalog-derived"}

VALID_CLAIM_TYPES = {
    "empirical_result",
    "method_claim",
    "physical_insight",
    "definition",
    "comparison",
    "catalog_fact",
    "software_or_pipeline",
}
VALID_CONFIDENCE = {"high", "medium", "low"}


def project_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for path in [cur, *cur.parents]:
        if (path / "wiki" / "schema.md").exists() and (path / ".kb").exists():
            return path
    return cur


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end():]
    return parse_yaml_subset(raw), body


def parse_yaml_subset(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[Any] | None = None
    current_item: dict[str, Any] | None = None

    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2).strip()
            current_key = key
            current_item = None
            if value == "":
                current_list = []
                data[key] = current_list
            else:
                current_list = None
                data[key] = parse_scalar(value)
            continue
        item = re.match(r"^\s*-\s*(.*)$", line)
        if item and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            current_list = data[current_key]
            value = item.group(1).strip()
            if ":" in value and not value.startswith(("'", '"')):
                k, v = value.split(":", 1)
                current_item = {k.strip(): parse_scalar(v.strip())}
                current_list.append(current_item)
            else:
                current_item = None
                current_list.append(parse_scalar(value))
            continue
        nested = re.match(r"^\s+([A-Za-z_][\w-]*):\s*(.*)$", line)
        if nested and current_item is not None:
            current_item[nested.group(1)] = parse_scalar(nested.group(2).strip())
    return data


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in split_csv(inner)]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            pass
    if re.fullmatch(r"-?\d+\.\d+", value):
        try:
            return float(value)
        except ValueError:
            pass
    return value


def split_csv(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    for ch in text:
        if ch in {'"', "'"}:
            quote = None if quote == ch else ch if quote is None else quote
        if ch == "," and quote is None:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return default


def dump_json(path: Path, data: Any) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def wiki_pages(root: Path, include_inbox: bool = False) -> list[Path]:
    paths: list[Path] = []
    bases = [root / "wiki", root / "inbox"] if include_inbox else [root / "wiki"]
    for base in bases:
        for subdir in PAGE_DIRS.values():
            d = base / subdir
            if d.exists():
                paths.extend(sorted(d.glob("*.md")))
    return paths


def page_slug(path: Path) -> str:
    return path.stem
