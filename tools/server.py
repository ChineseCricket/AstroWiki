#!/usr/bin/env python3
"""Lightweight JSON-RPC-over-stdin search service for the llm-wiki (ported from AstroWiki).

Exposes search / get / list_concepts / graph_neighbors.
Usage:

    printf '{"method":"search","params":{"query":"sixte tes","limit":5}}\n' | python tools/server.py
    printf '{"method":"get","params":{"slug":"dauser2019-sixte"}}\n' | python tools/server.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from common import PAGE_DIRS, page_slug, parse_frontmatter, project_root, read_text, wiki_pages


def search(root: Path, query: str, limit: int = 8) -> list[dict]:
    q = query.lower()
    terms = [t for t in re.split(r"\s+", q) if t]
    hits: list[tuple[int, dict]] = []
    for path in wiki_pages(root):
        text = read_text(path).lower()
        fm, _ = parse_frontmatter(read_text(path))
        score = sum(text.count(t) for t in terms)
        score += 3 * sum(t in (fm.get("title", "") + " " + " ".join(fm.get("tags", []) or [])).lower() for t in terms)
        if score:
            hits.append((score, {"slug": page_slug(path), "path": str(path.relative_to(root)),
                                 "title": fm.get("title", page_slug(path)), "type": fm.get("type"),
                                 "score": score}))
    hits.sort(key=lambda x: x[0], reverse=True)
    return [h[1] for h in hits[:limit]]


def get_page(root: Path, slug: str) -> dict | None:
    for path in wiki_pages(root):
        if page_slug(path) == slug:
            return {"slug": slug, "path": str(path.relative_to(root)), "content": read_text(path)}
    return None


def list_pages(root: Path, ptype: str | None = None) -> list[dict]:
    out: list[dict] = []
    for path in wiki_pages(root):
        fm, _ = parse_frontmatter(read_text(path))
        if ptype and fm.get("type") != ptype:
            continue
        out.append({"slug": page_slug(path), "title": fm.get("title", page_slug(path)), "type": fm.get("type")})
    return out


def neighbors(root: Path, slug: str) -> dict:
    target = get_page(root, slug)
    if not target:
        return {"slug": slug, "incoming": [], "outgoing": []}
    out_links = set(re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", target["content"]))
    incoming = []
    for path in wiki_pages(root):
        text = read_text(path)
        if f"[[{slug}" in text:
            fm, _ = parse_frontmatter(text)
            incoming.append({"slug": page_slug(path), "title": fm.get("title", page_slug(path))})
    return {"slug": slug, "outgoing": sorted(out_links), "incoming": incoming}


def main() -> int:
    root = project_root()
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "no input"}, ensure_ascii=False))
        return 1
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"bad json: {exc}"}, ensure_ascii=False))
        return 1
    method = req.get("method")
    params = req.get("params", {}) or {}
    if method == "search":
        print(json.dumps(search(root, params.get("query", ""), int(params.get("limit", 8))), ensure_ascii=False, indent=2))
    elif method == "get":
        print(json.dumps(get_page(root, params.get("slug", "")) or {"error": "not found"}, ensure_ascii=False, indent=2))
    elif method == "list_concepts":
        print(json.dumps(list_pages(root, "concept"), ensure_ascii=False, indent=2))
    elif method == "graph_neighbors":
        print(json.dumps(neighbors(root, params.get("slug", "")), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": f"unknown method: {method}"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
