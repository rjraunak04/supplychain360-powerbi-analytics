#!/usr/bin/env python3
"""Create a source-control release bundle for SupplyChain360.

The bundle intentionally excludes PBIX/PBIT binaries, local Power BI caches,
Git metadata and secrets. It is suitable for portfolio handoff or CI artifacts.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = [
    ".github",
    "deployment",
    "docs",
    "powerbi",
    "scripts",
    "sql",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".gitignore",
]
EXCLUDED_SUFFIXES = {".pbix", ".pbit", ".abf"}
EXCLUDED_PARTS = {".git", ".pbi", "__pycache__", ".pytest_cache"}


def allowed(path: Path) -> bool:
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if path.name.startswith(".env"):
        return False
    return True


def add_path(zf: zipfile.ZipFile, path: Path) -> None:
    if not path.exists():
        return
    if path.is_file():
        if allowed(path):
            zf.write(path, path.relative_to(ROOT))
        return
    for file in sorted(path.rglob("*")):
        if file.is_file() and allowed(file):
            zf.write(file, file.relative_to(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dist/SupplyChain360-source.zip")
    args = parser.parse_args()

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            add_path(zf, ROOT / item)

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"Created {output.relative_to(ROOT)} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
