"""Backends for curated X operations."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any
from urllib import error, parse, request

from .config import Config


@dataclass(frozen=True)
class OperationPlan:
    operation_id: str
    payload: dict[str, Any]
    summary: str
    mutating: bool = True
    category: str = "general"

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "payload": self.payload,
            "summary": self.summary,
            "mutating": self.mutating,
            "category": self.category,
        }


class Backend:
    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        raise NotImplementedError


class DryRunBackend(Backend):
    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        if not plan.mutating:
            return {
                "status": "backend_not_configured",
                "message": "Read operations need a live official XMCP backend. Set X_PUBLISHER_MODE=live, X_PUBLISHER_ALLOW_LIVE=1, and X_PUBLISHER_XMCP_URL.",
                "plan": plan.to_dict(),
            }
        return {
            "status": "dry_run",
            "message": "Dry-run mode: no request was sent to X.",
            "plan": plan.to_dict(),
        }


class XmcpBackend(Backend):
    def __init__(self, xmcp_url: str):
        self.xmcp_url = xmcp_url

    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        try:
            return asyncio.run(self._execute_async(plan))
        except RuntimeError as exc:
            return {
                "status": "backend_error",
                "message": f"Could not call official XMCP from this runtime: {exc}",
                "plan": plan.to_dict(),
            }

    async def _execute_async(self, plan: OperationPlan) -> dict[str, Any]:
        try:
            from fastmcp import Client
        except ImportError:
            return {
                "status": "backend_not_configured",
                "message": "Install FastMCP dependencies with `python -m pip install -r requirements.txt` before using live XMCP calls.",
                "plan": plan.to_dict(),
            }
        async with Client(self.xmcp_url) as client:
            result = await client.call_tool(plan.operation_id, plan.payload)
        return {
            "status": "ok",
            "message": "Operation executed through official XMCP.",
            "plan": plan.to_dict(),
            "result": _jsonable(result),
        }


class XApiBackend(Backend):
    def __init__(self, access_token: str, base_url: str = "https://api.x.com", transport: Any | None = None):
        self.access_token = access_token
        self.base_url = base_url.rstrip("/")
        self.transport = transport or self._default_transport

    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        try:
            result = self._execute_plan(plan)
            return {
                "status": "ok",
                "message": "Operation executed through X API v2.",
                "plan": plan.to_dict(),
                "result": result,
            }
        except XApiUnsupportedOperation as exc:
            return {
                "status": "unsupported_operation",
                "message": str(exc),
                "plan": plan.to_dict(),
            }
        except XApiError as exc:
            return {
                "status": "backend_error",
                "message": str(exc),
                "plan": plan.to_dict(),
                "response": exc.response,
            }

    def _execute_plan(self, plan: OperationPlan) -> dict[str, Any]:
        if plan.operation_id == "createPosts":
            if isinstance(plan.payload.get("thread"), list):
                return self._create_thread(plan.payload["thread"])
            text = _required_text(plan.payload, "text")
            return self._request("POST", "/2/tweets", {"text": text})

        if plan.operation_id == "deletePosts":
            post_id = _required_text(plan.payload, "id")
            return self._request("DELETE", f"/2/tweets/{parse.quote(post_id)}")

        if plan.operation_id == "getPostsById":
            post_id = _required_text(plan.payload, "id")
            return self._request("GET", f"/2/tweets/{parse.quote(post_id)}")

        if plan.operation_id == "getUsersByUsername":
            username = _required_text(plan.payload, "username")
            return self._request("GET", f"/2/users/by/username/{parse.quote(username)}")

        if plan.operation_id == "getUsersById":
            user_id = _required_text(plan.payload, "id")
            return self._request("GET", f"/2/users/{parse.quote(user_id)}")

        raise XApiUnsupportedOperation(
            f"X API backend does not implement {plan.operation_id}. Use X_PUBLISHER_BACKEND=xmcp for the broader official XMCP surface."
        )

    def _create_thread(self, operations: list[dict[str, Any]]) -> dict[str, Any]:
        created = []
        previous_id = None
        for operation in operations:
            payload = operation.get("payload") if isinstance(operation, dict) else None
            if not isinstance(payload, dict):
                raise XApiUnsupportedOperation("Thread operations must include payload objects.")
            text = _required_text(payload, "text")
            body: dict[str, Any] = {"text": text}
            if previous_id:
                body["reply"] = {"in_reply_to_tweet_id": previous_id}
            result = self._request("POST", "/2/tweets", body)
            created.append(result)
            previous_id = str((result.get("data") or {}).get("id") or "")
            if not previous_id:
                raise XApiError("X API did not return a post id for thread chaining.", result)
        return {"posts": created}

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path
        return self.transport(method, url, body, headers)

    @staticmethod
    def _default_transport(method: str, url: str, body: dict[str, Any] | None, headers: dict[str, str]) -> dict[str, Any]:
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = request.Request(url, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=30) as response:
                return _read_json_response(response.status, response.read().decode("utf-8"))
        except error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            raise XApiError(f"X API returned HTTP {exc.code}.", _safe_json(response_body)) from exc
        except error.URLError as exc:
            raise XApiError(f"Could not reach X API: {exc.reason}", None) from exc


class RecordingBackend(Backend):
    def __init__(self):
        self.calls: list[OperationPlan] = []

    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        self.calls.append(plan)
        return {
            "status": "ok",
            "message": "Recorded operation.",
            "plan": plan.to_dict(),
            "result": {"recorded": True},
        }


def backend_from_config(config: Config) -> Backend:
    if not config.live_enabled:
        return DryRunBackend()
    if config.backend in {"x-api", "rest"}:
        if config.x_user_access_token:
            return XApiBackend(config.x_user_access_token, config.x_api_base_url)
        return DryRunBackend()
    if config.backend == "xmcp" and config.xmcp_url:
        return XmcpBackend(config.xmcp_url)
    if config.backend == "auto" and config.xmcp_url:
        return XmcpBackend(config.xmcp_url)
    if config.backend == "auto" and config.x_user_access_token:
        return XApiBackend(config.x_user_access_token, config.x_api_base_url)
    return DryRunBackend()


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump())
    if hasattr(value, "dict"):
        return _jsonable(value.dict())
    return repr(value)


class XApiUnsupportedOperation(Exception):
    pass


class XApiError(Exception):
    def __init__(self, message: str, response: Any):
        super().__init__(message)
        self.response = response


def _required_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise XApiUnsupportedOperation(f"Missing required string payload field: {key}.")
    return value.strip()


def _read_json_response(status: int, text: str) -> dict[str, Any]:
    body = _safe_json(text)
    if status < 200 or status >= 300:
        raise XApiError(f"X API returned HTTP {status}.", body)
    return body if isinstance(body, dict) else {"data": body}


def _safe_json(text: str) -> Any:
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text[:500]}
