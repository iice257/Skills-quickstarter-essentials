"""Curated MCP tool implementations."""

from __future__ import annotations

from typing import Any

from .backend import Backend, DryRunBackend, OperationPlan
from .post_text import build_intent_url, make_thread, validate_post


_BACKEND: Backend = DryRunBackend()


def configure_backend(backend: Backend) -> None:
    global _BACKEND
    _BACKEND = backend


def _truncate(value: str, limit: int = 80) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _confirmation_response(plan: OperationPlan, confirmation: str | None) -> dict[str, Any] | None:
    if not plan.mutating:
        return None
    if confirmation == plan.summary:
        return None
    return {
        "status": "confirmation_required",
        "message": "Mutating X operations require exact confirmation before execution.",
        "required_confirmation": plan.summary,
        "plan": plan.to_dict(),
    }


def _invalid_text_response(tool: str, text: str, url: str | None) -> dict[str, Any] | None:
    result = validate_post(text, url)
    if result.valid:
        return None
    return {
        "tool": tool,
        "status": "invalid_post",
        "message": "Post text is too long for X.",
        "validation": result.to_dict(),
    }


def _execute(plan: OperationPlan, confirmation: str | None = None) -> dict[str, Any]:
    blocked = _confirmation_response(plan, confirmation)
    if blocked:
        return blocked
    return _BACKEND.execute(plan)


def _plan(operation_id: str, payload: dict[str, Any], summary: str, *, mutating: bool = True, category: str = "general") -> OperationPlan:
    return OperationPlan(operation_id=operation_id, payload=payload, summary=summary, mutating=mutating, category=category)


def draft_post(text: str, url: str | None = None) -> dict[str, Any]:
    result = validate_post(text, url)
    return {
        "tool": "draft_post",
        "status": "ok" if result.valid else "invalid_post",
        "text": result.text,
        "url": result.url,
        "validation": result.to_dict(),
        "composer_url": build_intent_url(result.text, result.url) if result.valid else None,
    }


def validate_post_tool(text: str, url: str | None = None) -> dict[str, Any]:
    result = validate_post(text, url)
    return {
        "tool": "validate_post",
        "status": "ok" if result.valid else "invalid_post",
        "validation": result.to_dict(),
    }


def create_composer_url(text: str, url: str | None = None) -> dict[str, Any]:
    result = validate_post(text, url)
    if not result.valid:
        return {
            "tool": "create_composer_url",
            "status": "invalid_post",
            "validation": result.to_dict(),
            "composer_url": None,
        }
    return {
        "tool": "create_composer_url",
        "status": "ok",
        "validation": result.to_dict(),
        "composer_url": build_intent_url(result.text, result.url),
    }


def create_post(text: str, url: str | None = None, confirmation: str | None = None) -> dict[str, Any]:
    invalid = _invalid_text_response("create_post", text, url)
    if invalid:
        return invalid
    result = validate_post(text, url)
    final_text = result.text if not result.url else f"{result.text} {result.url}"
    plan = _plan(
        "createPosts",
        {"text": final_text},
        f"create_post text={_truncate(final_text)}",
        category="publish",
    )
    return _execute(plan, confirmation)


def create_thread(text: str, url: str | None = None, confirmation: str | None = None) -> dict[str, Any]:
    chunks = make_thread(text, url)
    operations = []
    for index, chunk in enumerate(chunks, 1):
        final_url = url if index == len(chunks) else None
        final_text = chunk if not final_url else f"{chunk} {final_url}"
        operations.append({"operation_id": "createPosts", "payload": {"text": final_text}})
    plan = _plan(
        "createPosts",
        {"thread": operations, "reply_chaining": "live mode must reply each later post to the previous created post id"},
        f"create_thread posts={len(chunks)} first={_truncate(chunks[0] if chunks else '')}",
        category="publish",
    )
    return _execute(plan, confirmation)


def delete_post(post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("deletePosts", {"id": post_id}, f"delete_post id={post_id}", category="publish")
    return _execute(plan, confirmation)


def _read(operation_id: str, payload: dict[str, Any], summary: str, category: str) -> dict[str, Any]:
    return _BACKEND.execute(_plan(operation_id, payload, summary, mutating=False, category=category))


def get_account_context(username: str | None = None, user_id: str | None = None) -> dict[str, Any]:
    payload = {"username": username, "id": user_id}
    op = "getUsersByUsername" if username else "getUsersById"
    target = username or user_id or "me"
    return _read(op, payload, f"get_account_context target={target}", "read")


def lookup_user(username: str | None = None, user_id: str | None = None) -> dict[str, Any]:
    payload = {"username": username, "id": user_id}
    op = "getUsersByUsername" if username else "getUsersById"
    target = username or user_id or "missing"
    return _read(op, payload, f"lookup_user target={target}", "read")


def lookup_post(post_id: str) -> dict[str, Any]:
    return _read("getPostsById", {"id": post_id}, f"lookup_post id={post_id}", "read")


def search_recent_posts(query: str, max_results: int = 10) -> dict[str, Any]:
    return _read("searchPostsRecent", {"query": query, "max_results": max_results}, f"search_recent_posts query={_truncate(query)}", "read")


def get_user_posts(user_id: str, max_results: int = 10) -> dict[str, Any]:
    return _read("getUsersPosts", {"id": user_id, "max_results": max_results}, f"get_user_posts user_id={user_id}", "read")


def summarize_recent_posts(username: str | None = None, user_id: str | None = None, max_results: int = 10) -> dict[str, Any]:
    payload = {"username": username, "id": user_id, "max_results": max_results, "summary": True}
    target = username or user_id or "me"
    return _read("getUsersPosts", payload, f"summarize_recent_posts target={target}", "read")


def like_post(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("likePost", {"id": user_id, "tweet_id": post_id}, f"like_post user_id={user_id} post_id={post_id}", category="engagement")
    return _execute(plan, confirmation)


def unlike_post(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("unlikePost", {"id": user_id, "tweet_id": post_id}, f"unlike_post user_id={user_id} post_id={post_id}", category="engagement")
    return _execute(plan, confirmation)


def repost_post(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("repostPost", {"id": user_id, "tweet_id": post_id}, f"repost_post user_id={user_id} post_id={post_id}", category="engagement")
    return _execute(plan, confirmation)


def unrepost_post(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("unrepostPost", {"id": user_id, "source_tweet_id": post_id}, f"unrepost_post user_id={user_id} post_id={post_id}", category="engagement")
    return _execute(plan, confirmation)


def follow_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("followUser", {"id": user_id, "target_user_id": target_user_id}, f"follow_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def unfollow_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("unfollowUser", {"source_user_id": user_id, "target_user_id": target_user_id}, f"unfollow_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def mute_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("muteUser", {"id": user_id, "target_user_id": target_user_id}, f"mute_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def unmute_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("unmuteUser", {"source_user_id": user_id, "target_user_id": target_user_id}, f"unmute_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def block_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("blockUsersDms", {"id": user_id, "target_user_id": target_user_id}, f"block_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def unblock_user(user_id: str, target_user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("unblockUsersDms", {"source_user_id": user_id, "target_user_id": target_user_id}, f"unblock_user user_id={user_id} target_user_id={target_user_id}", category="engagement")
    return _execute(plan, confirmation)


def create_list(name: str, description: str | None = None, private: bool = False, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("createLists", {"name": name, "description": description, "private": private}, f"create_list name={name}", category="lists")
    return _execute(plan, confirmation)


def update_list(list_id: str, name: str | None = None, description: str | None = None, private: bool | None = None, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("updateLists", {"id": list_id, "name": name, "description": description, "private": private}, f"update_list id={list_id}", category="lists")
    return _execute(plan, confirmation)


def delete_list(list_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("deleteLists", {"id": list_id}, f"delete_list id={list_id}", category="lists")
    return _execute(plan, confirmation)


def add_list_member(list_id: str, user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("addListsMember", {"id": list_id, "user_id": user_id}, f"add_list_member list_id={list_id} user_id={user_id}", category="lists")
    return _execute(plan, confirmation)


def remove_list_member(list_id: str, user_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("removeListsMemberByUserId", {"id": list_id, "user_id": user_id}, f"remove_list_member list_id={list_id} user_id={user_id}", category="lists")
    return _execute(plan, confirmation)


def create_bookmark(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("createUsersBookmark", {"id": user_id, "tweet_id": post_id}, f"create_bookmark user_id={user_id} post_id={post_id}", category="bookmarks")
    return _execute(plan, confirmation)


def delete_bookmark(user_id: str, post_id: str, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan("deleteUsersBookmark", {"id": user_id, "tweet_id": post_id}, f"delete_bookmark user_id={user_id} post_id={post_id}", category="bookmarks")
    return _execute(plan, confirmation)


def preview_x_operation(operation_id: str, payload: dict[str, Any], mutating: bool = True) -> dict[str, Any]:
    plan = _plan(operation_id, payload, f"x_operation operation_id={operation_id}", mutating=mutating, category="raw")
    return {"status": "preview", "plan": plan.to_dict()}


def execute_x_operation(operation_id: str, payload: dict[str, Any], mutating: bool = True, confirmation: str | None = None) -> dict[str, Any]:
    plan = _plan(operation_id, payload, f"x_operation operation_id={operation_id}", mutating=mutating, category="raw")
    return _execute(plan, confirmation)
