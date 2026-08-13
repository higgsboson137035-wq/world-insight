import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import editorial_pipeline as pipeline
from scripts import morning


ARTICLE_TEXT = """# World Insight — Draft
**Title:** Test
**Date:** 2026-08-14
## Today's Question
> Question
## Quick Choices
## Human Context
## Decision Space
## Insight Shift
## Take One Thing
"""


class PipelinePhaseOneTests(unittest.TestCase):
    def make_root(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for directory in ("articles", "archive", "docs", "scripts", "templates"):
            (root / directory).mkdir()
        article = root / "articles" / "2026-08-14-test.md"
        article.write_text(ARTICLE_TEXT, encoding="utf-8")
        (root / "scripts" / "build.py").write_text("# builder\n", encoding="utf-8")
        for name in ("insight.html", "index.html", "archive.html"):
            (root / "templates" / name).write_text(name, encoding="utf-8")
        return temporary, root, article

    def write_review(self, root, article, decision, fixes="NONE"):
        review = root / "docs" / "EDITORIAL_REVIEW_2026-08-14.md"
        review.write_text(
            f"""Article: articles/{article.name}
Review Status: COMPLETE
Final Decision: {decision}
Required Fixes Status: {fixes}
- Is it true?: PASS
- Is it fair?: PASS
- Is it useful?: PASS
- Insight Shift: A
- Take One Thing: PASS
""",
            encoding="utf-8",
        )

    def test_review_a_passes(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_review(root, article, "A")
        with patch.object(pipeline, "ROOT", root):
            state, decision, fixes, _ = pipeline.editorial_review_record(article)
        self.assertEqual((state, decision, fixes), ("PASS", "A", "NONE"))
        daily = root / "daily.md"
        daily.write_text("daily", encoding="utf-8")
        workflow = self.base_state(editorial_review=state, build="NOT_READY", daily_editorial=daily)
        self.assertEqual(pipeline.publish_readiness(workflow)[0], "NEEDS_PREVIEW")
        self.assertEqual(morning.next_action(workflow, True), "Run: python3 scripts/build.py")

    def test_review_b_needs_fix_and_stops_build(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_review(root, article, "B", "OPEN")
        with patch.object(pipeline, "ROOT", root):
            state, decision, fixes, _ = pipeline.editorial_review_record(article)
        self.assertEqual((state, decision, fixes), ("NEEDS_FIX", "B", "OPEN"))
        workflow = self.base_state(editorial_review=state)
        self.assertEqual(pipeline.publish_readiness(workflow)[0], "NEEDS_REVIEW")

    def test_review_c_holds_for_no_publish_decision(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_review(root, article, "C")
        with patch.object(pipeline, "ROOT", root):
            state, _, _, _ = pipeline.editorial_review_record(article)
        workflow = self.base_state(editorial_review=state)
        self.assertEqual(pipeline.publish_readiness(workflow)[0], "NEEDS_NO_PUBLISH_DECISION")

    def test_open_fix_overrides_decision_a(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_review(root, article, "A", "OPEN")
        with patch.object(pipeline, "ROOT", root):
            state, _, _, _ = pipeline.editorial_review_record(article)
        self.assertEqual(state, "NEEDS_FIX")

    def test_failed_three_test_overrides_decision_a(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        self.write_review(root, article, "A")
        review = root / "docs" / "EDITORIAL_REVIEW_2026-08-14.md"
        review.write_text(review.read_text(encoding="utf-8").replace("Is it fair?: PASS", "Is it fair?: NEEDS_WORK"), encoding="utf-8")
        with patch.object(pipeline, "ROOT", root):
            state, _, _, _ = pipeline.editorial_review_record(article)
        self.assertEqual(state, "NEEDS_FIX")

    def test_no_publish_is_normal_completion(self):
        state = self.base_state(
            article=None,
            daily_result="NO_PUBLISH",
            no_publish_confirmation="CONFIRMED",
            build="NOT_READY",
        )
        readiness, action = pipeline.publish_readiness(state)
        self.assertEqual(readiness, "NOT_APPLICABLE")
        self.assertEqual(action, "None — editorial day completed without publication.")
        output = io.StringIO()
        with patch.object(morning, "selected_topic", return_value=False):
            state.publish_readiness, state.next_action = readiness, action
            with contextlib.redirect_stdout(output):
                morning.print_morning(state)
        self.assertIn("Daily Result: NO_PUBLISH", output.getvalue())
        self.assertIn("Publish Readiness: NOT_APPLICABLE", output.getvalue())
        self.assertIn("Publish: NO_PUBLISH", output.getvalue())

    def test_fallback_attempts_zero_and_one(self):
        daily = "- Daily Result: IN_PROGRESS\n- Fallback Attempts: 0\n"
        self.assertEqual(pipeline.daily_metadata(daily)[1], 0)
        daily = "- Daily Result: IN_PROGRESS\n- Fallback Attempts: 1\n"
        self.assertEqual(pipeline.daily_metadata(daily)[1], 1)
        state = self.base_state(source_verification="HOLD_C", fallback_attempts=1)
        readiness, _ = pipeline.publish_readiness(state)
        self.assertEqual(readiness, "NEEDS_NO_PUBLISH_DECISION")

    def test_build_freshness_detects_old_and_new_html(self):
        temporary, root, article = self.make_root()
        self.addCleanup(temporary.cleanup)
        outputs = (root / "archive" / "2026-08-14.html", root / "index.html", root / "archive.html")
        for output in outputs:
            output.write_text("generated", encoding="utf-8")
        inputs = [article, root / "scripts" / "build.py"] + list((root / "templates").glob("*.html"))
        for path in inputs:
            os.utime(path, ns=(1_000_000_000, 1_000_000_000))
        for output in outputs:
            os.utime(output, ns=(2_000_000_000, 2_000_000_000))
        with patch.object(pipeline, "ROOT", root):
            self.assertTrue(pipeline.build_is_fresh(article))
            os.utime(article, ns=(3_000_000_000, 3_000_000_000))
            self.assertFalse(pipeline.build_is_fresh(article))

    def test_final_approval_is_ready_and_morning_prints_ready(self):
        state = self.base_state(final_approval="APPROVED")
        state.publish_readiness, state.next_action = pipeline.publish_readiness(state)
        self.assertEqual(state.publish_readiness, "READY_TO_PUBLISH")
        with patch.object(morning, "selected_topic", return_value=True):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                morning.print_morning(state)
        self.assertIn("Publish: READY", output.getvalue())

    def test_old_daily_review_records_remain_compatible(self):
        root = Path(__file__).resolve().parents[1]
        article = root / "articles" / "2026-08-13-policy-tool-fit.md"
        state, decision, fixes, _ = pipeline.editorial_review_record(article)
        self.assertEqual((state, decision, fixes), ("PASS", "A", "RESOLVED"))
        pilot = root / "articles" / "pilot_002.md"
        state, decision, _, _ = pipeline.editorial_review_record(pilot)
        self.assertEqual((state, decision), ("PASS", "A"))
        daily = (root / "docs" / "DAILY_EDITORIAL_2026-08-13.md").read_text(encoding="utf-8")
        self.assertEqual(pipeline.daily_metadata(daily)[1], 1)

    @staticmethod
    def base_state(**changes):
        root = Path("/tmp/world-insight-test")
        values = dict(
            today="2026-08-14", world_brief=root / "brief.md", world_brief_status="FOUND",
            daily_editorial=root / "daily.md", source_verification="PASS_A",
            source_verification_link="VERIFIED", source_verification_file=root / "source.md",
            source_verification_signal="PASS_A", article=root / "article.md", article_text="",
            editorial_review="PASS", review_decision="A", required_fixes="NONE",
            insight_shift="A", take_one_thing="PASS", editorial_readiness="READY", build="READY",
            human_read="COMPLETE", technical_validation="PASS", local_preview="COMPLETE",
            safari="PASS", chrome="PASS", git_diff_review="COMPLETE", final_approval="PENDING",
            daily_result="IN_PROGRESS", fallback_attempts=0, no_publish_confirmation="PENDING",
            publish_readiness="", next_action="",
        )
        values.update(changes)
        return pipeline.PipelineState(**values)


if __name__ == "__main__":
    unittest.main()
