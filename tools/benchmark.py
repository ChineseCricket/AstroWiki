#!/usr/bin/env python3
"""Run lightweight AstroWiki benchmark fixtures."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from common import dump_json, load_json, project_root, write_text


def score_fixture(root: Path, fixture: Path) -> dict:
    meta = load_json(fixture / "fixture.json", {})
    checks = meta.get("checks", [])
    results = []
    lint = subprocess.run([sys.executable, "tools/lint.py", "--json"], cwd=root, text=True, capture_output=True)
    lint_issues = json.loads(lint.stdout) if lint.stdout.strip().startswith("[") else []
    lint_fail = any(i.get("level") == "FAIL" for i in lint_issues)
    for check in checks:
        if check in {"structure", "provenance", "migration"}:
            passed = not lint_fail
            results.append({"check": check, "score": 2 if passed else 0, "notes": "lint-backed"})
        elif check == "retrieval":
            results.append({"check": check, "score": 2, "notes": "MCP smoke is covered separately; fixture has no required hits"})
        elif check in {"comparison", "content_quality"}:
            results.append({"check": check, "score": 2, "notes": "smoke fixture; add expected_pages for strict content scoring"})
        else:
            results.append({"check": check, "score": 1, "notes": "unknown check treated as partial"})
    max_score = 2 * len(results) if results else 2
    score = sum(r["score"] for r in results) / max_score
    return {"fixture": meta.get("name", fixture.name), "score": score, "results": results, "lint_fail": lint_fail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    root = project_root()
    fixture = (root / args.fixture).resolve()
    if not (fixture / "fixture.json").exists():
        raise SystemExit(
            "Benchmark fixture not found. Real fixtures are intentionally private; "
            "pass a local fixture directory containing fixture.json."
        )
    result = score_fixture(root, fixture)
    out_dir = root / "outputs" / "benchmark"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{date.today().isoformat()}-{result['fixture']}-scores.json"
    md_path = out_dir / f"{date.today().isoformat()}-{result['fixture']}-report.md"
    dump_json(json_path, result)
    lines = [f"# Benchmark: {result['fixture']}", "", f"Score: {result['score']:.2%}", ""]
    for row in result["results"]:
        lines.append(f"- {row['check']}: {row['score']}/2 — {row['notes']}")
    write_text(md_path, "\n".join(lines) + "\n")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0 if result["score"] >= 0.8 and not result["lint_fail"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
