#!/usr/bin/env python3
"""Tiny JSON-RPC-ish AstroWiki knowledge service.

This intentionally stays dependency-free. It supports line-delimited JSON on
stdin so it can be adapted by MCP wrappers, and a simple CLI smoke mode.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from astrowiki_common import PAGE_DIRS, parse_frontmatter, project_root, read_text, wiki_pages, write_text


def page_record(root: Path, path: Path) -> dict:
    text = read_text(path)
    fm, body = parse_frontmatter(text)
    return {
        "slug": path.stem,
        "path": str(path.relative_to(root)),
        "title": fm.get("title", path.stem),
        "type": fm.get("type"),
        "provenance": fm.get("provenance"),
        "text": text,
        "body": body,
    }


def search(root: Path, query: str, limit: int = 5) -> list[dict]:
    terms = [t.lower() for t in re.findall(r"\w+", query)]
    results: list[dict] = []
    for path in wiki_pages(root):
        rec = page_record(root, path)
        hay = (rec["title"] + "\n" + rec["body"]).lower()
        score = sum(hay.count(t) for t in terms) if terms else 0
        if score:
            summary = " ".join(rec["body"].strip().split())[:300]
            results.append({k: rec[k] for k in ["slug", "path", "title", "type", "provenance"]} | {"score": score, "summary": summary})
    return sorted(results, key=lambda r: (-r["score"], r["path"]))[:limit]


def get(root: Path, slug_or_path: str) -> dict | None:
    for path in wiki_pages(root):
        if path.stem == slug_or_path or str(path.relative_to(root)) == slug_or_path:
            rec = page_record(root, path)
            return {k: rec[k] for k in ["slug", "path", "title", "type", "provenance", "text"]}
    return None


def list_concepts(root: Path) -> list[dict]:
    concepts = []
    for path in sorted((root / "wiki" / "concepts").glob("*.md")):
        rec = page_record(root, path)
        concepts.append({k: rec[k] for k in ["slug", "path", "title", "provenance"]})
    return concepts


def graph_neighbors(root: Path, slug: str) -> dict:
    target = get(root, slug)
    if not target:
        return {"slug": slug, "neighbors": []}
    neighbors = set(re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", target["text"]))
    inbound = []
    for path in wiki_pages(root):
        if path.stem == slug:
            continue
        text = read_text(path)
        if re.search(rf"\[\[{re.escape(slug)}(?:\|[^\]]+)?\]\]", text):
            inbound.append(path.stem)
    return {"slug": slug, "outbound": sorted(neighbors), "inbound": sorted(inbound)}


def submit_feedback(root: Path, payload: dict) -> dict:
    out = root / "outputs" / "queries" / "feedback.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return {"status": "recorded", "path": str(out.relative_to(root))}


def dispatch(root: Path, request: dict) -> dict:
    method = request.get("method")
    params = request.get("params") or {}
    if method == "search":
        result = search(root, params.get("query", ""), int(params.get("limit", 5)))
    elif method == "get":
        result = get(root, params.get("path") or params.get("slug") or "")
    elif method == "list_concepts":
        result = list_concepts(root)
    elif method == "graph_neighbors":
        result = graph_neighbors(root, params.get("slug", ""))
    elif method == "submit_feedback":
        result = submit_feedback(root, params)
    else:
        return {"error": f"unknown method: {method}", "id": request.get("id")}
    return {"result": result, "id": request.get("id")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("port", nargs="?", default="3849")
    parser.add_argument("wiki", nargs="?", default="wiki")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    root = project_root()
    if args.smoke:
        print(json.dumps(dispatch(root, {"method": "search", "params": {"query": "astro", "limit": 3}}), indent=2))
        return 0
    print(f"AstroWiki service ready on logical port {args.port}; root={root}", file=sys.stderr)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            print(json.dumps(dispatch(root, request), ensure_ascii=False), flush=True)
        except Exception as exc:
            print(json.dumps({"error": str(exc)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
