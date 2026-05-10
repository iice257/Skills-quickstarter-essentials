"""Configuration for the x-publisher MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    mode: str = "dry-run"
    host: str = "127.0.0.1"
    port: int = 8765
    backend: str = "auto"
    xmcp_url: str | None = None
    x_api_base_url: str = "https://api.x.com"
    x_user_access_token: str | None = None
    allow_live: bool = False

    @property
    def live_enabled(self) -> bool:
        return self.mode == "live" and self.allow_live

    @classmethod
    def from_env(cls) -> "Config":
        raw_mode = os.getenv("X_PUBLISHER_MODE", "dry-run").strip().lower()
        if raw_mode not in {"dry-run", "live"}:
            raise ValueError("X_PUBLISHER_MODE must be dry-run or live")
        raw_backend = os.getenv("X_PUBLISHER_BACKEND", "auto").strip().lower()
        if raw_backend not in {"auto", "xmcp", "x-api", "rest"}:
            raise ValueError("X_PUBLISHER_BACKEND must be auto, xmcp, x-api, or rest")
        raw_port = os.getenv("X_PUBLISHER_MCP_PORT", "8765").strip()
        try:
            port = int(raw_port)
        except ValueError as exc:
            raise ValueError("X_PUBLISHER_MCP_PORT must be an integer") from exc
        return cls(
            mode=raw_mode,
            host=os.getenv("X_PUBLISHER_MCP_HOST", "127.0.0.1").strip() or "127.0.0.1",
            port=port,
            backend=raw_backend,
            xmcp_url=os.getenv("X_PUBLISHER_XMCP_URL", "").strip() or None,
            x_api_base_url=os.getenv("X_PUBLISHER_X_API_BASE_URL", "https://api.x.com").strip().rstrip("/") or "https://api.x.com",
            x_user_access_token=os.getenv("X_PUBLISHER_X_USER_ACCESS_TOKEN", "").strip() or None,
            allow_live=_truthy(os.getenv("X_PUBLISHER_ALLOW_LIVE")),
        )
