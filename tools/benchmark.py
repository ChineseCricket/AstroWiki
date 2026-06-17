#!/usr/bin/env python3
"""Run lightweight AstroWiki benchmark fixtures."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from common import dump_json, load_json, parse_frontmatter, project_root, read_text, write_text


LEGACY_PAGE_DIRS = {
    "papers": "source",
    "concepts": "concept",
    "methods": "method",
    "data_sources": "dataset",
}
ASTROWIKI_PAGE_DIRS = {
    "sources": "source",
    "concepts": "concept",
    "methods": "method",
    "objects": "object",
    "datasets": "dataset",
    "instruments": "instrument",
    "synthesis": "synthesis",
    "notes": "note",
}
LINT_BLOCKING_CHECKS = {"frontmatter", "type", "provenance", "claims", "synthesis", "query-derived", "manifest"}
DEFAULT_SPECS: dict[str, dict[str, Any]] = {
    "s2fitting-noria": {
        "description": "N132D/RGS AstroWiki regression fixture.",
        "profile": "astrowiki",
        "expected_min_score": 0.8,
        "checks": ["structure", "provenance", "retrieval", "comparison"],
        "min_pages": 20,
        "required_pages": [
            "n132d",
            "suzuki2020-n132d-xmm-rgs",
            "gu2025-xrism-n132d-charge-exchange",
            "xmm-newton-rgs",
        ],
        "required_searches": [
            "N132D charge exchange XRISM",
            "XMM Newton RGS plasma diagnostics",
        ],
        "required_terms": [
            "charge exchange",
            "XMM-Newton RGS",
            "plasma diagnostics",
        ],
    },
    "final-project-scaling": {
        "description": "Legacy galaxy-cluster scaling wiki migration fixture.",
        "profile": "legacy-wiki",
        "expected_min_score": 0.8,
        "checks": ["structure", "provenance", "retrieval", "content_quality", "migration"],
        "min_pages": 20,
        "required_pages": [
            "mantz_2016",
            "scaling_relations",
            "self_similar_model",
            "spectral_fitting",
            "clash_survey",
        ],
        "required_searches": [
            "core excised LX M scatter",
            "self similar scaling relation",
            "weak lensing mass calibration",
        ],
        "required_terms": [
            "Core-excised",
            "self-similar",
            "weak lensing",
        ],
    },
}


@dataclass
class Page:
    slug: str
    path: str
    title: str
    type: str
    provenance: str | None
    text: str
    body: str


def normalize_path(root: Path, value: str | None) -> Path:
    if not value:
        return root
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def h1_title(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", slug) if part) or slug


def load_astrowiki_pages(kb_root: Path) -> list[Page]:
    pages: list[Page] = []
    base = kb_root / "wiki"
    for dirname, page_type in ASTROWIKI_PAGE_DIRS.items():
        for path in sorted((base / dirname).glob("*.md")):
            text = read_text(path)
            fm, body = parse_frontmatter(text)
            pages.append(
                Page(
                    slug=path.stem,
                    path=str(path.relative_to(kb_root)),
                    title=str(fm.get("title") or h1_title(body) or title_from_slug(path.stem)),
                    type=str(fm.get("type") or page_type),
                    provenance=fm.get("provenance"),
                    text=text,
                    body=body,
                )
            )
    return pages


def load_legacy_pages(kb_root: Path) -> tuple[list[Page], list[str]]:
    pages: list[Page] = []
    notes: list[str] = []
    base = kb_root / "wiki"
    for dirname, page_type in LEGACY_PAGE_DIRS.items():
        directory = base / dirname
        if not directory.exists():
            notes.append(f"missing legacy directory: wiki/{dirname}")
            continue
        for path in sorted(directory.glob("*.md")):
            text = read_text(path)
            fm, body = parse_frontmatter(text)
            title = fm.get("title") or fm.get("name") or h1_title(body) or title_from_slug(path.stem)
            pages.append(
                Page(
                    slug=path.stem,
                    path=str(path.relative_to(kb_root)),
                    title=str(title),
                    type=page_type,
                    provenance=fm.get("provenance"),
                    text=text,
                    body=body,
                )
            )
    return pages, notes


def run_lint(tool_root: Path, kb_root: Path) -> tuple[list[dict[str, Any]], str]:
    proc = subprocess.run(
        [sys.executable, str(tool_root / "tools" / "lint.py"), "--json"],
        cwd=kb_root,
        text=True,
        capture_output=True,
    )
    if proc.stdout.strip().startswith("["):
        return json.loads(proc.stdout), proc.stderr
    return [{"level": "FAIL", "check": "lint", "file": "", "msg": proc.stderr or proc.stdout or "lint failed"}], proc.stderr


def search_pages(pages: list[Page], query: str, limit: int = 5) -> list[dict[str, Any]]:
    terms = [t.lower() for t in re.findall(r"\w+", query)]
    hits: list[dict[str, Any]] = []
    for page in pages:
        hay = f"{page.slug}\n{page.title}\n{page.body}".lower()
        score = sum(hay.count(term) for term in terms) if terms else 0
        if score:
            hits.append(
                {
                    "slug": page.slug,
                    "path": page.path,
                    "title": page.title,
                    "type": page.type,
                    "score": score,
                }
            )
    return sorted(hits, key=lambda row: (-row["score"], row["path"]))[:limit]


def required_search_specs(meta: dict[str, Any]) -> list[dict[str, Any]]:
    specs = []
    for item in meta.get("required_searches", []):
        if isinstance(item, str):
            specs.append({"query": item})
        elif isinstance(item, dict) and item.get("query"):
            specs.append(item)
    return specs


def match_required_pages(pages: list[Page], required: list[str]) -> tuple[bool, list[str]]:
    slugs = {page.slug for page in pages}
    missing = [slug for slug in required if slug not in slugs]
    return not missing, missing


def match_required_terms(pages: list[Page], required: list[str]) -> tuple[bool, list[str]]:
    corpus = "\n".join(f"{page.title}\n{page.body}" for page in pages).lower()
    missing = [term for term in required if term.lower() not in corpus]
    return not missing, missing


def evaluate_searches(pages: list[Page], specs: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
    rows = []
    all_passed = True
    for spec in specs:
        query = str(spec["query"])
        hits = search_pages(pages, query, int(spec.get("limit", 5)))
        expected = spec.get("expected")
        if isinstance(expected, str):
            passed = any(hit["slug"] == expected for hit in hits)
        elif isinstance(expected, list):
            found = {hit["slug"] for hit in hits}
            passed = all(slug in found for slug in expected)
        else:
            passed = bool(hits)
        all_passed = all_passed and passed
        rows.append({"query": query, "passed": passed, "hits": hits})
    return all_passed, rows


def score_row(check: str, passed: bool, notes: str, details: Any | None = None) -> dict[str, Any]:
    row: dict[str, Any] = {"check": check, "score": 2 if passed else 0, "notes": notes}
    if details is not None:
        row["details"] = details
    return row


def load_pages_for_profile(kb_root: Path, profile: str) -> tuple[list[Page], list[str]]:
    if profile == "astrowiki":
        return load_astrowiki_pages(kb_root), []
    if profile == "legacy-wiki":
        return load_legacy_pages(kb_root)
    raise SystemExit(f"Unknown benchmark profile: {profile}")


def score_benchmark(tool_root: Path, meta: dict[str, Any]) -> dict[str, Any]:
    profile = meta.get("profile", "astrowiki")
    kb_root = normalize_path(tool_root, meta.get("kb_root"))
    expected_min_score = float(meta.get("expected_min_score", 0.8))
    checks = list(meta.get("checks") or ["structure", "provenance", "retrieval", "content_quality"])

    pages, migration_notes = load_pages_for_profile(kb_root, profile)
    required_pages = [str(item) for item in meta.get("required_pages", [])]
    required_terms = [str(item) for item in meta.get("required_terms", [])]
    required_searches = required_search_specs(meta)
    lint_issues: list[dict[str, Any]] = []
    raw_lint_fail = False

    if profile == "astrowiki":
        lint_issues, _ = run_lint(tool_root, kb_root)
        raw_lint_fail = any(issue.get("level") == "FAIL" for issue in lint_issues)
    elif profile == "legacy-wiki":
        lint_issues, _ = run_lint(tool_root, kb_root)
        raw_lint_fail = any(issue.get("level") == "FAIL" for issue in lint_issues)

    blocking_lint_fail = any(
        issue.get("level") == "FAIL" and issue.get("check") in LINT_BLOCKING_CHECKS for issue in lint_issues
    )
    required_pages_passed, missing_pages = match_required_pages(pages, required_pages)
    required_terms_passed, missing_terms = match_required_terms(pages, required_terms)
    searches_passed, search_results = evaluate_searches(pages, required_searches)

    results = []
    for check in checks:
        if check == "structure":
            min_pages = int(meta.get("min_pages", 1))
            passed = len(pages) >= min_pages
            notes = f"{len(pages)} normalized pages found"
            if min_pages > 1:
                notes += f"; minimum is {min_pages}"
            results.append(score_row(check, passed, notes))
        elif check == "provenance":
            missing = [page.path for page in pages if not page.provenance]
            if profile == "astrowiki":
                passed = not blocking_lint_fail and not missing
                notes = "lint-backed provenance checks"
            else:
                passed = not missing
                notes = "legacy frontmatter normalized in memory"
            results.append(score_row(check, passed, notes, {"missing_provenance": missing[:20]} if missing else None))
        elif check == "retrieval":
            details = {"searches": search_results}
            results.append(score_row(check, searches_passed, f"{len(search_results)} required searches evaluated", details))
        elif check in {"comparison", "content_quality"}:
            passed = required_pages_passed and required_terms_passed
            details = {"missing_pages": missing_pages, "missing_terms": missing_terms}
            notes = f"{len(required_pages)} pages and {len(required_terms)} terms checked"
            results.append(score_row(check, passed, notes, details))
        elif check == "migration":
            if profile == "legacy-wiki":
                passed = bool(pages) and required_pages_passed
                notes = "raw lint findings recorded; legacy pages normalized without writing"
                details = {"migration_notes": migration_notes, "raw_lint_fail": raw_lint_fail}
            else:
                passed = not raw_lint_fail
                notes = "lint-backed migration check"
                details = {"raw_lint_fail": raw_lint_fail}
            results.append(score_row(check, passed, notes, details))
        else:
            results.append(score_row(check, False, "unknown check"))

    max_score = 2 * len(results) if results else 2
    score = sum(row["score"] for row in results) / max_score
    return {
        "fixture": meta.get("name", kb_root.name),
        "description": meta.get("description", ""),
        "profile": profile,
        "kb_root": str(kb_root),
        "score": score,
        "expected_min_score": expected_min_score,
        "page_count": len(pages),
        "results": results,
        "lint_fail": raw_lint_fail if profile == "astrowiki" else False,
        "raw_lint_fail": raw_lint_fail,
        "raw_lint_issues": lint_issues,
    }


def meta_from_args(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    if args.fixture:
        fixture = normalize_path(root, args.fixture)
        if not (fixture / "fixture.json").exists():
            raise SystemExit(
                "Benchmark fixture not found. Real fixtures are intentionally private; "
                "pass a local fixture directory containing fixture.json."
            )
        meta = load_json(fixture / "fixture.json", {})
        meta.setdefault("name", fixture.name)
        return DEFAULT_SPECS.get(str(meta["name"]), {}) | meta
    if not args.kb_root:
        raise SystemExit("Pass either --fixture or --kb-root.")
    name = args.name or Path(args.kb_root).expanduser().name
    default = DEFAULT_SPECS.get(name, {})
    meta = {
        "name": args.name or Path(args.kb_root).expanduser().name,
        "kb_root": args.kb_root,
        "profile": args.profile,
        "expected_min_score": args.expected_min_score,
        "checks": args.checks,
    }
    if name in DEFAULT_SPECS:
        meta = default | {"name": name, "kb_root": args.kb_root}
    return meta


def write_report(root: Path, result: dict[str, Any]) -> tuple[Path, Path]:
    out_dir = root / "outputs" / "benchmark"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{date.today().isoformat()}-{result['fixture']}-scores.json"
    md_path = out_dir / f"{date.today().isoformat()}-{result['fixture']}-report.md"
    dump_json(json_path, result)
    lines = [
        f"# Benchmark: {result['fixture']}",
        "",
        f"Profile: `{result['profile']}`",
        f"Knowledge base: `{result['kb_root']}`",
        f"Score: {result['score']:.2%}",
        f"Pages: {result['page_count']}",
        "",
    ]
    for row in result["results"]:
        lines.append(f"- {row['check']}: {row['score']}/2 - {row['notes']}")
    if result.get("raw_lint_fail") and result["profile"] == "legacy-wiki":
        lines.extend(["", "## Migration Findings", ""])
        for issue in result.get("raw_lint_issues", [])[:20]:
            lines.append(f"- {issue.get('level')} {issue.get('check')}: {issue.get('file')} - {issue.get('msg')}")
    write_text(md_path, "\n".join(lines) + "\n")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture")
    parser.add_argument("--kb-root")
    parser.add_argument("--profile", choices=["astrowiki", "legacy-wiki"], default="astrowiki")
    parser.add_argument("--name")
    parser.add_argument("--expected-min-score", type=float, default=0.8)
    parser.add_argument(
        "--checks",
        nargs="+",
        default=["structure", "provenance", "retrieval", "content_quality"],
    )
    args = parser.parse_args()

    root = project_root()
    meta = meta_from_args(root, args)
    result = score_benchmark(root, meta)
    json_path, md_path = write_report(root, result)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0 if result["score"] >= result["expected_min_score"] and not result["lint_fail"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
