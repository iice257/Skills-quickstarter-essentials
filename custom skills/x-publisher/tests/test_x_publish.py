from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "x_publish.py"
SPEC = importlib.util.spec_from_file_location("x_publish", MODULE_PATH)
assert SPEC and SPEC.loader
x_publish = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = x_publish
SPEC.loader.exec_module(x_publish)


class XPublishTests(unittest.TestCase):
    def test_url_counts_as_tco_length(self) -> None:
        self.assertEqual(x_publish.weighted_length("https://example.com/very/long/path"), 23)
        self.assertEqual(x_publish.weighted_length("Read https://example.com/very/long/path"), 28)

    def test_cjk_and_emoji_count_conservatively(self) -> None:
        self.assertEqual(x_publish.weighted_length("hi"), 2)
        self.assertEqual(x_publish.weighted_length("火"), 2)
        self.assertEqual(x_publish.weighted_length("🚀"), 2)

    def test_validate_detects_over_limit(self) -> None:
        self.assertTrue(x_publish.validate_post("a" * 280).valid)
        self.assertFalse(x_publish.validate_post("a" * 281).valid)

    def test_intent_url_encodes_text_and_url(self) -> None:
        intent_url = x_publish.build_intent_url("hello world", "https://example.com/a?b=c")
        parsed = urlparse(intent_url)
        query = parse_qs(parsed.query)
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "twitter.com")
        self.assertEqual(parsed.path, "/intent/tweet")
        self.assertEqual(query["text"], ["hello world"])
        self.assertEqual(query["url"], ["https://example.com/a?b=c"])

    def test_thread_splits_into_valid_chunks(self) -> None:
        text = " ".join(["shipping reliable local social publishing workflows"] * 30)
        chunks = x_publish.make_thread(text, "https://github.com/iice257/x-publisher")
        self.assertGreater(len(chunks), 1)
        for index, chunk in enumerate(chunks, 1):
            url = "https://github.com/iice257/x-publisher" if index == len(chunks) else None
            self.assertTrue(x_publish.validate_post(chunk, url).valid)
            self.assertTrue(chunk.startswith(f"{index}/{len(chunks)} "))

    def test_thread_command_reads_file(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".md") as handle:
            handle.write(" ".join(["x-publisher makes launch posts easier"] * 20))
            path = handle.name
        try:
            with redirect_stdout(io.StringIO()):
                code = x_publish.main(["thread", "--file", path])
            self.assertEqual(code, 0)
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
