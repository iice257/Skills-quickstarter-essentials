import unittest

from src.main import summarize


class DataToolStarterTests(unittest.TestCase):
    def test_summary_counts_rows_and_columns(self):
        report = summarize([{"id": "1", "value": "42"}])
        self.assertEqual(report["record_count"], 1)
        self.assertEqual(report["columns"], ["id", "value"])


if __name__ == "__main__":
    unittest.main()
