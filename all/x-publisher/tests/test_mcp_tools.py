from __future__ import annotations

import unittest

from x_publisher_mcp.backend import RecordingBackend, XApiBackend
from x_publisher_mcp.registry import list_tool_names
from x_publisher_mcp import tools


EXPECTED_TOOLS = {
    "draft_post",
    "validate_post",
    "create_composer_url",
    "create_post",
    "create_thread",
    "delete_post",
    "get_account_context",
    "lookup_user",
    "lookup_post",
    "search_recent_posts",
    "get_user_posts",
    "summarize_recent_posts",
    "like_post",
    "unlike_post",
    "repost_post",
    "unrepost_post",
    "follow_user",
    "unfollow_user",
    "mute_user",
    "unmute_user",
    "block_user",
    "unblock_user",
    "create_list",
    "update_list",
    "delete_list",
    "add_list_member",
    "remove_list_member",
    "create_bookmark",
    "delete_bookmark",
    "preview_x_operation",
    "execute_x_operation",
}


class McpToolTests(unittest.TestCase):
    def setUp(self) -> None:
        tools.configure_backend(RecordingBackend())

    def tearDown(self) -> None:
        from x_publisher_mcp.backend import DryRunBackend

        tools.configure_backend(DryRunBackend())

    def test_tool_registry_contains_expected_surface(self) -> None:
        self.assertEqual(set(list_tool_names()), EXPECTED_TOOLS)

    def test_create_post_requires_confirmation(self) -> None:
        response = tools.create_post("Testing v2")
        self.assertEqual(response["status"], "confirmation_required")
        self.assertEqual(response["required_confirmation"], "create_post text=Testing v2")

    def test_create_post_executes_with_confirmation(self) -> None:
        response = tools.create_post("Testing v2", confirmation="create_post text=Testing v2")
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["plan"]["operation_id"], "createPosts")
        self.assertEqual(response["plan"]["payload"]["text"], "Testing v2")

    def test_create_post_rejects_invalid_text_before_confirmation(self) -> None:
        response = tools.create_post("a" * 281)
        self.assertEqual(response["status"], "invalid_post")
        self.assertFalse(response["validation"]["valid"])

    def test_create_thread_returns_confirmed_operation_plan(self) -> None:
        text = " ".join(["thread planning keeps risky posting controlled"] * 25)
        first = tools.create_thread(text)
        self.assertEqual(first["status"], "confirmation_required")
        response = tools.create_thread(text, confirmation=first["required_confirmation"])
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["plan"]["operation_id"], "createPosts")
        self.assertGreater(len(response["plan"]["payload"]["thread"]), 1)

    def test_dry_run_backend_previews_mutating_operations(self) -> None:
        from x_publisher_mcp.backend import DryRunBackend

        tools.configure_backend(DryRunBackend())
        first = tools.delete_post("123")
        self.assertEqual(first["status"], "confirmation_required")
        response = tools.delete_post("123", confirmation=first["required_confirmation"])
        self.assertEqual(response["status"], "dry_run")
        self.assertEqual(response["plan"]["operation_id"], "deletePosts")

    def test_read_tool_without_backend_is_actionable(self) -> None:
        from x_publisher_mcp.backend import DryRunBackend

        tools.configure_backend(DryRunBackend())
        response = tools.search_recent_posts("x publisher")
        self.assertEqual(response["status"], "backend_not_configured")
        self.assertIn("X_PUBLISHER_XMCP_URL", response["message"])

    def test_engagement_tools_map_to_operations(self) -> None:
        cases = [
            (tools.like_post, ("me", "p1"), "likePost"),
            (tools.unlike_post, ("me", "p1"), "unlikePost"),
            (tools.repost_post, ("me", "p1"), "repostPost"),
            (tools.unrepost_post, ("me", "p1"), "unrepostPost"),
            (tools.follow_user, ("me", "u2"), "followUser"),
            (tools.unfollow_user, ("me", "u2"), "unfollowUser"),
            (tools.mute_user, ("me", "u2"), "muteUser"),
            (tools.unmute_user, ("me", "u2"), "unmuteUser"),
            (tools.block_user, ("me", "u2"), "blockUsersDms"),
            (tools.unblock_user, ("me", "u2"), "unblockUsersDms"),
        ]
        for func, args, operation_id in cases:
            first = func(*args)
            response = func(*args, confirmation=first["required_confirmation"])
            self.assertEqual(response["status"], "ok")
            self.assertEqual(response["plan"]["operation_id"], operation_id)

    def test_list_and_bookmark_tools_map_to_operations(self) -> None:
        cases = [
            (tools.create_list, ("Builders",), "createLists"),
            (tools.update_list, ("list1",), "updateLists"),
            (tools.delete_list, ("list1",), "deleteLists"),
            (tools.add_list_member, ("list1", "u2"), "addListsMember"),
            (tools.remove_list_member, ("list1", "u2"), "removeListsMemberByUserId"),
            (tools.create_bookmark, ("me", "p1"), "createUsersBookmark"),
            (tools.delete_bookmark, ("me", "p1"), "deleteUsersBookmark"),
        ]
        for func, args, operation_id in cases:
            first = func(*args)
            response = func(*args, confirmation=first["required_confirmation"])
            self.assertEqual(response["status"], "ok")
            self.assertEqual(response["plan"]["operation_id"], operation_id)

    def test_raw_operation_preview_and_execute(self) -> None:
        preview = tools.preview_x_operation("getUsersByUsername", {"username": "XDevelopers"}, mutating=False)
        self.assertEqual(preview["status"], "preview")
        self.assertFalse(preview["plan"]["mutating"])

        blocked = tools.execute_x_operation("followUser", {"id": "me", "target_user_id": "u2"})
        self.assertEqual(blocked["status"], "confirmation_required")

        executed = tools.execute_x_operation(
            "followUser",
            {"id": "me", "target_user_id": "u2"},
            confirmation=blocked["required_confirmation"],
        )
        self.assertEqual(executed["status"], "ok")
        self.assertEqual(executed["plan"]["operation_id"], "followUser")

    def test_x_api_backend_creates_post_with_user_token(self) -> None:
        calls = []

        def transport(method, url, body, headers):
            calls.append((method, url, body, headers))
            return {"data": {"id": "post-1", "text": body["text"]}}

        tools.configure_backend(XApiBackend("user-token", "https://api.x.test", transport=transport))
        response = tools.create_post("Testing live post", confirmation="create_post text=Testing live post")

        self.assertEqual(response["status"], "ok")
        self.assertEqual(calls[0][0], "POST")
        self.assertEqual(calls[0][1], "https://api.x.test/2/tweets")
        self.assertEqual(calls[0][2], {"text": "Testing live post"})
        self.assertEqual(calls[0][3]["Authorization"], "Bearer user-token")
        self.assertEqual(response["result"]["data"]["id"], "post-1")

    def test_x_api_backend_creates_thread_by_reply_chaining(self) -> None:
        calls = []

        def transport(method, url, body, headers):
            calls.append((method, url, body, headers))
            return {"data": {"id": f"post-{len(calls)}", "text": body["text"]}}

        tools.configure_backend(XApiBackend("user-token", "https://api.x.test", transport=transport))
        text = " ".join(["thread planning keeps risky posting controlled"] * 25)
        first = tools.create_thread(text)
        response = tools.create_thread(text, confirmation=first["required_confirmation"])

        self.assertEqual(response["status"], "ok")
        self.assertGreater(len(calls), 1)
        self.assertNotIn("reply", calls[0][2])
        self.assertEqual(calls[1][2]["reply"]["in_reply_to_tweet_id"], "post-1")

    def test_x_api_backend_reports_unsupported_operations(self) -> None:
        tools.configure_backend(XApiBackend("user-token", "https://api.x.test", transport=lambda *_args: {}))
        first = tools.follow_user("me", "target")
        response = tools.follow_user("me", "target", confirmation=first["required_confirmation"])

        self.assertEqual(response["status"], "unsupported_operation")
        self.assertIn("X_PUBLISHER_BACKEND=xmcp", response["message"])


if __name__ == "__main__":
    unittest.main()
