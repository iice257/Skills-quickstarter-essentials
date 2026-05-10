# X Publisher

`x-publisher` is a lightweight Codex skill for drafting X posts, validating local character counts, splitting long drafts into threads, and opening prefilled X composer links.

V1 intentionally avoids direct API posting. V2 adds a dry-run-first MCP server for curated X publishing and account-management workflows.

## Install Locally

From the source repo:

```powershell
python tools/install_local.py
```

This copies the runtime skill files into your Codex skills directory:

```text
%USERPROFILE%\.codex\skills\x-publisher
```

## CLI

```powershell
python scripts/x_publish.py draft --text "Shipped x-publisher v1."
python scripts/x_publish.py validate --text "Shipped x-publisher v1." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher v1." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` to open the generated composer URL in the default browser.

## MCP V2

List tools:

```powershell
python -m x_publisher_mcp.server --list-tools
```

Run the MCP server:

```powershell
python -m pip install -r requirements.txt
python -m x_publisher_mcp.server
```

Default endpoint:

```text
http://127.0.0.1:8765/mcp
```

The MCP server defaults to `dry-run`; mutating tools require an exact confirmation string and do not call X unless live mode is explicitly enabled.

Live mode can use either a separately configured official XMCP backend or the focused direct X API backend for create/delete/read basics:

```powershell
$env:X_PUBLISHER_MODE="live"
$env:X_PUBLISHER_ALLOW_LIVE="1"
$env:X_PUBLISHER_BACKEND="x-api"
$env:X_PUBLISHER_X_USER_ACCESS_TOKEN="<user-context-token>"
python -m x_publisher_mcp.server
```

The direct backend uses X API v2 `POST /2/tweets` for posting. Keep tokens in local environment variables only.

## V2 Direction

X now has an official XMCP server. V2 should build on or wrap that official MCP/OpenAPI surface and add safer agent workflows for posting, account context, search, and management.
