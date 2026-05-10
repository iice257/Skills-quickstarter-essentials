#!/usr/bin/env python3
"""Find unresolved Idea Launcher template placeholders."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
DEFAULT_EXCLUDES = {".git", "node_modules", ".next", "dist", "build", "__pycache__"}
DEFAULT_TEMPLATE_SOURCE_EXCLUDES = {
    Path("assets/templates"),
    Path("assets/blueprints"),
}


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def iter_files(root: Path, excludes: set[Path]):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        relative = path.relative_to(root)
        if any(relative == excluded or is_under(relative, excluded) for excluded in excludes):
            continue
        yield path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate that generated project docs have no unresolved placeholders.")
    parser.add_argument("path", nargs="?", default=".", help="Project path to scan.")
    parser.add_argument(
        "--include-template-sources",
        action="store_true",
        help="Also scan this skill's intentional template and blueprint sources.",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    excludes = set()
    if not args.include_template_sources:
        excludes.update(DEFAULT_TEMPLATE_SOURCE_EXCLUDES)
    findings = []
    for path in iter_files(root, excludes):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            matches = PLACEHOLDER.findall(line)
            if matches:
                findings.append((path, line_number, ", ".join(sorted(set(matches)))))

    if findings:
        print("Unresolved placeholders found:")
        for path, line_number, matches in findings:
            print(f"{path}:{line_number}: {matches}")
        raise SystemExit(1)

    print(f"No unresolved placeholders found under {root}")


if __name__ == "__main__":
    main()
