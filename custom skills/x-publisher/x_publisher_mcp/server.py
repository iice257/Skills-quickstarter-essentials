"""Runnable FastMCP server for x-publisher."""

from __future__ import annotations

import argparse
import json
import sys

from .backend import backend_from_config
from .config import Config
from .registry import TOOL_DEFINITIONS, list_tool_names
from .tools import configure_backend


def build_mcp(config: Config | None = None):
    config = config or Config.from_env()
    configure_backend(backend_from_config(config))
    try:
        from fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("FastMCP is not installed. Run `python -m pip install -r requirements.txt`.") from exc

    mcp = FastMCP("X Publisher MCP")
    for definition in TOOL_DEFINITIONS:
        mcp.tool(name=definition.name, description=definition.description)(definition.function)
    return mcp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the x-publisher MCP server.")
    parser.add_argument("--list-tools", action="store_true", help="Print registered tool names and exit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON for --list-tools.")
    parser.add_argument("--host", help="Override X_PUBLISHER_MCP_HOST.")
    parser.add_argument("--port", type=int, help="Override X_PUBLISHER_MCP_PORT.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list_tools:
        names = list_tool_names()
        if args.json:
            print(json.dumps(names, indent=2))
        else:
            for name in names:
                print(name)
        return 0

    try:
        config = Config.from_env()
        if args.host:
            config = Config(
                mode=config.mode,
                host=args.host,
                port=config.port,
                backend=config.backend,
                xmcp_url=config.xmcp_url,
                x_api_base_url=config.x_api_base_url,
                x_user_access_token=config.x_user_access_token,
                allow_live=config.allow_live,
            )
        if args.port:
            config = Config(
                mode=config.mode,
                host=config.host,
                port=args.port,
                backend=config.backend,
                xmcp_url=config.xmcp_url,
                x_api_base_url=config.x_api_base_url,
                x_user_access_token=config.x_user_access_token,
                allow_live=config.allow_live,
            )
        mcp = build_mcp(config)
        mcp.run(transport="http", host=config.host, port=config.port)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
