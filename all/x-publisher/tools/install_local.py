#!/usr/bin/env python3
"""Install the runtime x-publisher skill files into the local Codex skills folder."""

from __future__ import annotations

import shutil
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = Path.home() / ".codex" / "skills" / "x-publisher"
RUNTIME_FILES = [
    "SKILL.md",
    "requirements.txt",
    "agents/openai.yaml",
    "scripts/list_mcp_tools.py",
    "scripts/start_mcp.py",
    "scripts/x_publish.py",
    "references/mcp-usage.md",
    "references/posting-workflow.md",
    "references/x-api-mcp-v2.md",
]
RUNTIME_DIRS = [
    "x_publisher_mcp",
]


def main() -> int:
    if SOURCE_ROOT.name != "x-publisher":
        raise SystemExit(f"Unexpected source root: {SOURCE_ROOT}")
    if TARGET_ROOT.name != "x-publisher":
        raise SystemExit(f"Unexpected target root: {TARGET_ROOT}")

    if TARGET_ROOT.exists():
        shutil.rmtree(TARGET_ROOT)
    TARGET_ROOT.mkdir(parents=True)

    for relative in RUNTIME_FILES:
        source = SOURCE_ROOT / relative
        target = TARGET_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    for relative in RUNTIME_DIRS:
        source = SOURCE_ROOT / relative
        target = TARGET_ROOT / relative
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    print(f"Installed x-publisher skill to {TARGET_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
