import json
import io
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

from scripts import brief_readiness


JST = ZoneInfo("Asia/Tokyo")
TEST_DATE = "2026-09-15"


def brief_text(
    *,
    date=TEST_DATE,
    marker=True,
    top3=True,
    required_headings=True,
    categories=True,
):
    lines = [f"_Date: {date}_", "", "## Today's Top 3"]
    if top3:
        lines.extend(["", "1. First item", "2. Second item", "3. Third item"])
    else:
        lines.extend(["", "1. First item", "2. Second item"])
    if required_headings:
        lines.extend(["", "## Executive Summary", "Summary", "", "## Why It Matters", "Why", "", "## Big Picture", "Picture", "", "## Tomorrow's Watchlist", "- Watch"])
    if categories:
        lines.extend(["", "## 🌍 世界情勢", "World", "", "## 💹 経済", "Economy", "", "## 🤖 AI・テクノロジー", "AI", "", "## 🔬 科学", "Science", "", "## 🇯🇵 日本への影響", "Japan"])
    if marker:
        lines.extend(["", "*Generated automatically by World Brief.*"])
    return "\n".join(lines) + "\n"


class BriefReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.briefs = self.root / "briefs"
        self.briefs.mkdir()

    def tearDown(self):
        self.temporary.cleanup()

    def write_brief(self, text=brief_text(), filename=TEST_DATE):
        path = self.briefs / f"{filename}.md"
        path.write_text(text, encoding="utf-8")
        timestamp = datetime(2026, 9, 15, 12, 0, tzinfo=JST).timestamp()
        os.utime(path, (timestamp, timestamp))
        return path

    def check(self, requested=TEST_DATE):
        return brief_readiness.check_brief(requested, self.root)

    def test_valid_brief(self):
        self.write_brief()
        result = self.check()
        self.assertTrue(result["ready"])
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["errors"], [])
        self.assertEqual(brief_readiness.exit_code(result), 0)

    def test_missing_brief(self):
        result = self.check()
        self.assertFalse(result["ready"])
        self.assertEqual(result["status"], "BRIEF_NOT_READY")
        self.assertIn("MISSING_BRIEF", result["errors"])

    def test_internal_date_mismatch(self):
        self.write_brief(brief_text(date="2026-09-14"))
        result = self.check()
        self.assertFalse(result["checks"]["internal_date_matches"])
        self.assertIn("MUST_FAILED:internal_date_matches", result["errors"])

    def test_empty_brief(self):
        self.write_brief("")
        result = self.check()
        self.assertFalse(result["checks"]["non_empty"])
        self.assertIn("MUST_FAILED:non_empty", result["errors"])

    def test_missing_generated_marker(self):
        self.write_brief(brief_text(marker=False))
        result = self.check()
        self.assertFalse(result["checks"]["generated_marker_exists"])
        self.assertIn("MUST_FAILED:generated_marker_exists", result["errors"])

    def test_missing_todays_top_three(self):
        self.write_brief(brief_text().replace("## Today's Top 3", "## News"))
        result = self.check()
        self.assertFalse(result["checks"]["top3_heading_exists"])
        self.assertIn("MUST_FAILED:top3_heading_exists", result["errors"])

    def test_top_three_incomplete(self):
        self.write_brief(brief_text(top3=False))
        result = self.check()
        self.assertFalse(result["checks"]["top3_items_complete"])
        self.assertIn("MUST_FAILED:top3_items_complete", result["errors"])

    def test_missing_required_heading(self):
        self.write_brief(brief_text(required_headings=False))
        result = self.check()
        self.assertFalse(result["checks"]["required_headings_exist"])
        self.assertIn("MUST_FAILED:required_headings_exist", result["errors"])

    def test_stale_mtime(self):
        path = self.write_brief()
        timestamp = datetime(2026, 9, 14, 23, 59, tzinfo=JST).timestamp()
        os.utime(path, (timestamp, timestamp))
        result = self.check()
        self.assertFalse(result["checks"]["mtime_matches_requested_date"])
        self.assertIn("MUST_FAILED:mtime_matches_requested_date", result["errors"])

    def test_should_warning_only_keeps_ready(self):
        self.write_brief(brief_text(categories=False))
        result = self.check()
        self.assertTrue(result["ready"])
        self.assertEqual(result["status"], "READY")
        self.assertTrue(result["warnings"])
        self.assertEqual(result["errors"], [])

    def test_requested_date_parsing_error(self):
        with self.assertRaises(brief_readiness.BriefReadinessError):
            brief_readiness.check_brief("2026-9-15", self.root)

    def test_cli_invalid_requested_date_returns_error_without_brief_path(self):
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = brief_readiness.main(["--date", "2026-9-15", "--brief-root", str(self.root)])
        result = json.loads(stdout.getvalue())
        self.assertEqual(code, 2)
        self.assertFalse(result["ready"])
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("INVALID_REQUESTED_DATE", result["errors"])
        self.assertIsNone(result["brief_path"])

    def test_brief_read_failure_returns_error(self):
        self.write_brief()
        with patch.object(Path, "read_text", side_effect=OSError("read failure")):
            result = self.check()
        self.assertFalse(result["ready"])
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("BRIEF_READ_ERROR", result["errors"])
        self.assertEqual(brief_readiness.exit_code(result), 2)

    def test_stat_failure_never_returns_ready(self):
        self.write_brief()
        with patch.object(brief_readiness, "_mtime_is_requested_date", side_effect=OSError("stat failure")):
            result = self.check()
        self.assertFalse(result["ready"])
        self.assertIn("BRIEF_STAT_ERROR", result["errors"])
        self.assertNotEqual(result["status"], "READY")

    def test_top_three_validation_is_limited_to_top_three_section(self):
        text = brief_text() + "\n## Other\n1. 2. 3. in prose\n"
        self.write_brief(text)
        result = self.check()
        self.assertTrue(result["ready"])

    def test_cli_returns_json_without_brief_body(self):
        self.write_brief()
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = brief_readiness.main(["--date", TEST_DATE, "--brief-root", str(self.root)])
        rendered = stdout.getvalue()
        parsed = json.loads(rendered)
        self.assertEqual(code, 0)
        self.assertNotIn("First item", parsed)
        self.assertTrue(parsed["ready"])


if __name__ == "__main__":
    unittest.main()
