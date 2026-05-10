"""Tool registry for the x-publisher MCP server."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from . import tools


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    function: Callable
    description: str


TOOL_DEFINITIONS: tuple[ToolDefinition, ...] = (
    ToolDefinition("draft_post", tools.draft_post, "Draft and validate a post without posting."),
    ToolDefinition("validate_post", tools.validate_post_tool, "Validate local weighted post length."),
    ToolDefinition("create_composer_url", tools.create_composer_url, "Create a prefilled X composer URL."),
    ToolDefinition("create_post", tools.create_post, "Create a post through the configured backend after confirmation."),
    ToolDefinition("create_thread", tools.create_thread, "Create a numbered thread plan through the configured backend after confirmation."),
    ToolDefinition("delete_post", tools.delete_post, "Delete a post after confirmation."),
    ToolDefinition("get_account_context", tools.get_account_context, "Get account context through the configured backend."),
    ToolDefinition("lookup_user", tools.lookup_user, "Look up a user through the configured backend."),
    ToolDefinition("lookup_post", tools.lookup_post, "Look up a post through the configured backend."),
    ToolDefinition("search_recent_posts", tools.search_recent_posts, "Search recent posts through the configured backend."),
    ToolDefinition("get_user_posts", tools.get_user_posts, "Get a user's posts through the configured backend."),
    ToolDefinition("summarize_recent_posts", tools.summarize_recent_posts, "Prepare a recent-posts summary request through the configured backend."),
    ToolDefinition("like_post", tools.like_post, "Like a post after confirmation."),
    ToolDefinition("unlike_post", tools.unlike_post, "Unlike a post after confirmation."),
    ToolDefinition("repost_post", tools.repost_post, "Repost a post after confirmation."),
    ToolDefinition("unrepost_post", tools.unrepost_post, "Undo a repost after confirmation."),
    ToolDefinition("follow_user", tools.follow_user, "Follow a user after confirmation."),
    ToolDefinition("unfollow_user", tools.unfollow_user, "Unfollow a user after confirmation."),
    ToolDefinition("mute_user", tools.mute_user, "Mute a user after confirmation."),
    ToolDefinition("unmute_user", tools.unmute_user, "Unmute a user after confirmation."),
    ToolDefinition("block_user", tools.block_user, "Block a user after confirmation."),
    ToolDefinition("unblock_user", tools.unblock_user, "Unblock a user after confirmation."),
    ToolDefinition("create_list", tools.create_list, "Create a list after confirmation."),
    ToolDefinition("update_list", tools.update_list, "Update a list after confirmation."),
    ToolDefinition("delete_list", tools.delete_list, "Delete a list after confirmation."),
    ToolDefinition("add_list_member", tools.add_list_member, "Add a list member after confirmation."),
    ToolDefinition("remove_list_member", tools.remove_list_member, "Remove a list member after confirmation."),
    ToolDefinition("create_bookmark", tools.create_bookmark, "Bookmark a post after confirmation."),
    ToolDefinition("delete_bookmark", tools.delete_bookmark, "Delete a bookmark after confirmation."),
    ToolDefinition("preview_x_operation", tools.preview_x_operation, "Preview a raw X/OpenAPI operation."),
    ToolDefinition("execute_x_operation", tools.execute_x_operation, "Execute a raw X/OpenAPI operation after confirmation if mutating."),
)


def list_tool_names() -> list[str]:
    return [definition.name for definition in TOOL_DEFINITIONS]
