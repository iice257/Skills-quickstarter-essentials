import json
import tempfile
import unittest
from pathlib import Path

from src.main import run


class AutomationStarterTests(unittest.TestCase):
    def test_run_returns_visible_dry_run_output(self):
        result = run("sample input")
        self.assertTrue(result["dry_run"])
        self.assertIn("sample input", result["summary"])
        self.assertIn("workflow", result)

    def test_json_output_shape_is_serializable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run.json"
            payload = run("hello")
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["summary"], "hello")


if __name__ == "__main__":
    unittest.main()
