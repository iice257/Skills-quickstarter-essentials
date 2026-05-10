#!/usr/bin/env python3
"""Start the x-publisher MCP server."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from x_publisher_mcp.server import main


if __name__ == "__main__":
    raise SystemExit(main())
