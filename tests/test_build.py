import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build


def article(reading_time=None, summary="Summary", date="2026-08-14"):
    front = {"Title": "Test", "Date": date}
    if reading_time is not None:
        front["Estimated Reading Time"] = reading_time
    return build.Article(
        Path(f"articles/{date}.md"),
        "## Quick Choices\n\nBody",
        front,
        "Question",
        summary,
    )


class BuilderRegressionTests(unittest.TestCase):
    def make_root(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "templates").mkdir()
        (root / "templates" / "insight.html").write_text(
            "{{ date }} · {{ reading_time }} {{ question }} {{ summary }} {{ body }}",
            encoding="utf-8",
        )
        (root / "templates" / "index.html").write_text(
            "{{ summary }}", encoding="utf-8"
        )
        (root / "templates" / "archive.html").write_text(
            "{{ entries }}", encoding="utf-8"
        )
        return temporary, root

    def test_article_reading_time_uses_each_front_matter_value(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        with patch.object(build, "ROOT", root):
            self.assertIn("7〜9分", build.render_article(article("7〜9分")))
            self.assertIn("8〜10分", build.render_article(article("8〜10分", date="2026-08-13")))

    def test_missing_reading_time_uses_backward_compatible_default(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        with patch.object(build, "ROOT", root):
            self.assertIn("10〜12分", build.render_article(article()))

    def test_real_insight_template_does_not_hardcode_reading_time(self):
        template = (Path(__file__).resolve().parents[1] / "templates" / "insight.html").read_text(encoding="utf-8")
        self.assertIn("{{ reading_time }}", template)
        self.assertNotIn("·　10〜12分", template)

    def test_summary_markdown_becomes_plain_text(self):
        text = """## 30-Second Brief

### Confirmed Facts

- Dose was **61.8%** with [display text](https://example.com) and `code`.
"""
        summary = build.extract_summary(text)
        self.assertEqual(summary, "Dose was 61.8% with display text and code.")
        self.assertNotIn("**", summary)
        self.assertNotIn("https://", summary)

    def test_index_escapes_plain_text_summary(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        with patch.object(build, "ROOT", root):
            rendered = build.render_index(article(summary="5 < 7 & 8"))
        self.assertEqual(rendered, "5 &lt; 7 &amp; 8")

    def test_article_displays_escaped_summary_between_question_and_body(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        with patch.object(build, "ROOT", root):
            rendered = build.render_article(article(summary="5 < 7 > 3 & safe"))
        escaped_summary = "5 &lt; 7 &gt; 3 &amp; safe"
        self.assertIn(escaped_summary, rendered)
        self.assertLess(rendered.index("Question"), rendered.index(escaped_summary))
        self.assertLess(rendered.index(escaped_summary), rendered.index('id="quick-choices"'))

    def test_index_and_article_use_the_same_article_summary(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        insight = article(summary="Shared <summary> & facts")
        with patch.object(build, "ROOT", root):
            index = build.render_index(insight)
            rendered_article = build.render_article(insight)
        escaped_summary = "Shared &lt;summary&gt; &amp; facts"
        self.assertEqual(index, escaped_summary)
        self.assertIn(escaped_summary, rendered_article)

    def test_2026_08_13_summary_no_longer_contains_emphasis_markers(self):
        source = Path(__file__).resolve().parents[1] / "articles" / "2026-08-13-policy-tool-fit.md"
        summary = build.extract_summary(source.read_text(encoding="utf-8"))
        self.assertNotIn("**", summary)
        self.assertIn("0.1%", summary)

    def test_archive_order_and_article_body_rendering_are_unchanged(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        newer = article("7〜9分", date="2026-08-14")
        older = article("8〜10分", date="2026-08-13")
        with patch.object(build, "ROOT", root):
            archive = build.render_archive([newer, older])
            body = build.render_article(newer)
        self.assertLess(archive.index("2026-08-14"), archive.index("2026-08-13"))
        self.assertIn('id="quick-choices"', body)
        self.assertIn("Body", body)

    def test_article_keeps_brief_and_major_sections_after_hero_summary(self):
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        source = """## Quick Choices

Choice

## 30-Second Brief

### Confirmed Facts

- Brief body

## Human Context

Context

## Decision Space

Decision
"""
        insight = build.Article(
            Path("articles/test.md"),
            source,
            {"Title": "Test", "Date": "2026-08-14"},
            "Question",
            build.extract_summary(source),
        )
        with patch.object(build, "ROOT", root):
            rendered = build.render_article(insight)
        summary_position = rendered.index("Brief body")
        self.assertLess(summary_position, rendered.index('id="quick-choices"'))
        for section_id in (
            'id="quick-choices"',
            'id="30-second-brief"',
            'id="human-context"',
            'id="decision-space"',
        ):
            self.assertIn(section_id, rendered)
        self.assertGreater(rendered.rindex("Brief body"), summary_position)

    def test_every_existing_article_has_a_summary(self):
        self.assertEqual(len(build.load_articles()), 7)
        for insight in build.load_articles():
            with self.subTest(source=insight.source.name):
                self.assertTrue(insight.summary)


if __name__ == "__main__":
    unittest.main()
