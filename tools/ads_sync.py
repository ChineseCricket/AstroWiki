#!/usr/bin/env python3
"""Stage NASA ADS records into raw/ads."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from astrowiki_common import dump_json, load_json, project_root, slugify, write_text


ADS_API = "https://api.adsabs.harvard.edu/v1/search/query"
FIELDS = "bibcode,title,author,year,pub,doi,identifier,abstract,citation_count,reference,citation"


def ads_request(query: str, rows: int) -> dict:
    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        raise RuntimeError("ADS_API_TOKEN is not set")
    params = urllib.parse.urlencode({"q": query, "fl": FIELDS, "rows": rows})
    req = urllib.request.Request(f"{ADS_API}?{params}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def citekey(doc: dict) -> str:
    authors = doc.get("author") or ["unknown"]
    first = authors[0].split(",")[0].split()[-1] if authors else "unknown"
    year = str(doc.get("year") or "undated")
    title = (doc.get("title") or ["untitled"])[0] if isinstance(doc.get("title"), list) else doc.get("title", "untitled")
    words = "-".join(slugify(title).split("-")[:4])
    return slugify(f"{first}{year}-{words}")


def markdown_for(doc: dict) -> str:
    key = citekey(doc)
    title = (doc.get("title") or ["Untitled"])[0] if isinstance(doc.get("title"), list) else doc.get("title", "Untitled")
    authors = doc.get("author") or []
    identifiers = doc.get("identifier") or []
    doi = (doc.get("doi") or [""])[0] if isinstance(doc.get("doi"), list) else doc.get("doi", "")
    arxiv = next((x for x in identifiers if str(x).lower().startswith("arxiv:")), "")
    abstract = doc.get("abstract") or ""
    refs = doc.get("reference") or []
    cites = doc.get("citation") or []
    return f"""---
source_type: ads
citekey: {key}
title: "{title.replace('"', "'")}"
authors: {json.dumps(authors, ensure_ascii=False)}
year: {doc.get("year", "")}
venue: "{str(doc.get("pub", "")).replace('"', "'")}"
ads_bibcode: "{doc.get("bibcode", "")}"
doi: "{doi}"
arxiv: "{arxiv}"
citation_count: {doc.get("citation_count", 0)}
synced: {date.today().isoformat()}
---

# {title}

## Abstract

{abstract}

## ADS Metadata

- Bibcode: `{doc.get("bibcode", "")}`
- DOI: `{doi}`
- arXiv: `{arxiv}`
- Citation count: {doc.get("citation_count", 0)}

## References

{chr(10).join(f"- `{r}`" for r in refs[:50]) if refs else "- Not fetched or unavailable."}

## Citations

{chr(10).join(f"- `{c}`" for c in cites[:50]) if cites else "- Not fetched or unavailable."}
"""


def docs_from_response(data: dict) -> list[dict]:
    return data.get("response", {}).get("docs", [])


def command_search(args: argparse.Namespace) -> int:
    root = project_root()
    try:
        docs = docs_from_response(ads_request(args.query, args.limit))
    except Exception as exc:
        if not args.dry_run:
            print(f"ADS request failed: {exc}", file=sys.stderr)
            return 1
        docs = [
            {
                "bibcode": "2026AstroWiki....1E",
                "title": [f"Dry-run placeholder for {args.query}"],
                "author": ["Example, A."],
                "year": 2026,
                "pub": "AstroWiki Dry Run",
                "abstract": "Set ADS_API_TOKEN to fetch live ADS records.",
                "citation_count": 0,
            }
        ]
    for doc in docs:
        key = citekey(doc)
        if args.dry_run:
            print(f"{key}: {doc.get('bibcode', '')} — {(doc.get('title') or ['Untitled'])[0]}")
        else:
            path = root / "raw" / "ads" / f"{key}.md"
            write_text(path, markdown_for(doc))
            state = load_json(root / ".kb" / "sync_state.json", {"ads": {}})
            state.setdefault("ads", {})[key] = {"bibcode": doc.get("bibcode"), "synced": date.today().isoformat()}
            dump_json(root / ".kb" / "sync_state.json", state)
            print(f"wrote {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--dry-run", action="store_true")
    bib = sub.add_parser("bibcode")
    bib.add_argument("bibcode")
    bib.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "bibcode":
        args.query = f"bibcode:{args.bibcode}"
        args.limit = 1
    return command_search(args)


if __name__ == "__main__":
    raise SystemExit(main())
