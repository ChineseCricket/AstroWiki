#!/usr/bin/env python3
"""Install AstroWiki into another project directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKIP = {".git", "__pycache__", ".pytest_cache"}


def copy_tree(src: Path, dst: Path, force: bool) -> None:
    for item in sorted(src.rglob("*")):
        if any(part in SKIP for part in item.parts):
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file without --force: {target}")
        shutil.copy2(item, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    src = Path(__file__).resolve().parents[1]
    dst = Path(args.target).expanduser().resolve()
    dst.mkdir(parents=True, exist_ok=True)
    copy_tree(src, dst, args.force)
    print(f"Installed AstroWiki into {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
