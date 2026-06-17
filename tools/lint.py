#!/usr/bin/env python3
"""Deterministic AstroWiki health checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from common import (
    PAGE_DIRS,
    TRUSTED_PROVENANCE,
    VALID_CLAIM_TYPES,
    VALID_CONFIDENCE,
    VALID_PROVENANCE,
    VALID_TYPES,
    load_json,
    page_slug,
    parse_frontmatter,
    project_root,
    read_text,
    wiki_pages,
)


@dataclass
class Issue:
    level: str
    check: str
    file: str
    msg: str

    def __str__(self) -> str:
        prefix = f"[{self.level}] {self.check}"
        return f"{prefix}: {self.file} — {self.msg}" if self.file else f"{prefix}: {self.msg}"


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def all_slugs(root: Path, include_inbox: bool) -> set[str]:
    return {page_slug(p) for p in wiki_pages(root, include_inbox)}


def check_pages(root: Path, include_inbox: bool) -> list[Issue]:
    issues: list[Issue] = []
    pages = wiki_pages(root, include_inbox)
    slugs = all_slugs(root, include_inbox)
    index_text = read_text(root / "wiki" / "index.md") if (root / "wiki" / "index.md").exists() else ""

    for path in pages:
        text = read_text(path)
        fm, body = parse_frontmatter(text)
        rp = rel(root, path)
        if not fm:
            issues.append(Issue("FAIL", "frontmatter", rp, "missing YAML frontmatter"))
            continue
        page_type = fm.get("type")
        provenance = fm.get("provenance")
        if not fm.get("title"):
            issues.append(Issue("FAIL", "frontmatter", rp, "missing title"))
        if page_type not in VALID_TYPES:
            issues.append(Issue("FAIL", "type", rp, f"invalid or missing type: {page_type}"))
        if provenance not in VALID_PROVENANCE:
            issues.append(Issue("FAIL", "provenance", rp, f"invalid or missing provenance: {provenance}"))
        if provenance == "query-derived" and "/wiki/" in f"/{rp}":
            issues.append(Issue("FAIL", "query-derived", rp, "query-derived content must not live in wiki/"))

        if page_type == "source":
            claims = fm.get("claims")
            if not isinstance(claims, list) or len(claims) < 3:
                issues.append(Issue("FAIL", "claims", rp, "source pages require at least 3 claims"))
            elif len(claims) > 8:
                issues.append(Issue("WARN", "claims", rp, "source pages should keep claims to 3-8"))
            if isinstance(claims, list):
                for idx, claim in enumerate(claims, 1):
                    if not isinstance(claim, dict):
                        issues.append(Issue("FAIL", "claims", rp, f"claim {idx} is not a mapping"))
                        continue
                    for key in ["text", "citekey", "locator", "type", "confidence"]:
                        if not claim.get(key):
                            issues.append(Issue("FAIL", "claims", rp, f"claim {idx} missing {key}"))
                    if claim.get("type") and claim["type"] not in VALID_CLAIM_TYPES:
                        issues.append(Issue("FAIL", "claims", rp, f"claim {idx} invalid type {claim['type']}"))
                    if claim.get("confidence") and claim["confidence"] not in VALID_CONFIDENCE:
                        issues.append(Issue("FAIL", "claims", rp, f"claim {idx} invalid confidence {claim['confidence']}"))

        if page_type == "synthesis":
            if "## Thesis" not in body:
                issues.append(Issue("FAIL", "synthesis", rp, "synthesis page missing ## Thesis"))
            sources = fm.get("sources")
            if not isinstance(sources, list) or len(sources) < 2:
                issues.append(Issue("FAIL", "synthesis", rp, "synthesis pages require at least two sources"))
            if provenance != "llm-derived":
                issues.append(Issue("FAIL", "synthesis", rp, "synthesis pages must be llm-derived"))

        for link in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text):
            if link.strip() not in slugs:
                issues.append(Issue("FAIL", "wikilinks", rp, f"broken link [[{link.strip()}]]"))

        if path.parts[-2] in PAGE_DIRS.values() and path.parts[-3] == "wiki":
            if f"[[{path.stem}]]" not in index_text and path.stem not in {".gitkeep"}:
                issues.append(Issue("WARN", "index", rp, "not referenced in wiki/index.md"))

    if not issues:
        issues.append(Issue("PASS", "all", "", f"{len(pages)} pages passed deterministic checks"))
    return issues


def check_manifest(root: Path) -> list[Issue]:
    manifest = load_json(root / ".kb" / "manifest.json", {})
    issues: list[Issue] = []
    if manifest.get("version") != 1:
        issues.append(Issue("FAIL", "manifest", ".kb/manifest.json", "missing version: 1"))
    if not isinstance(manifest.get("files", {}), dict):
        issues.append(Issue("FAIL", "manifest", ".kb/manifest.json", "files must be an object"))
    if not isinstance(manifest.get("pages", {}), dict):
        issues.append(Issue("FAIL", "manifest", ".kb/manifest.json", "pages must be an object"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--include-inbox", action="store_true")
    args = parser.parse_args()

    root = project_root()
    issues = check_manifest(root) + check_pages(root, args.include_inbox)
    fails = sum(i.level == "FAIL" for i in issues)
    warns = sum(i.level == "WARN" for i in issues)

    if args.json:
        print(json.dumps([asdict(i) for i in issues], indent=2, ensure_ascii=False))
    else:
        for issue in issues:
            if args.quiet and issue.level == "PASS":
                continue
            print(issue)
        print(f"\nTotal: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
