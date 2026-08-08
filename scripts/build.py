#!/usr/bin/env python3
"""Build the minimal static site for GitHub Pages."""
from pathlib import Path
import html
import re

try:
    import markdown
except ImportError as exc:  # pragma: no cover - user-facing setup error
    raise SystemExit(
        "Markdown package is required.\n"
        "Run:\n"
        "source .venv/bin/activate\n"
        "python3 -m pip install -r requirements.txt"
    ) from exc

ROOT = Path(__file__).resolve().parent.parent
ARTICLE = ROOT / "articles" / "pilot_001.md"
DATE = "2026-08-08"


def read_article():
    text = ARTICLE.read_text(encoding="utf-8")
    front = {}
    for line in text.splitlines():
        match = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", line)
        if match:
            front[match.group(1).strip()] = match.group(2).strip()
    return text, front


def body_markdown(text):
    # Keep editorial notes out of the public page while retaining the article as source of truth.
    public = text.split("## Editor Notes", 1)[0]
    public = re.sub(r"^# World Insight Pilot #1.*?$", "", public, flags=re.M)
    public = re.sub(r"^\*\*(Title|Date|Insight ID|Category|Thinking Skill|Estimated Reading Time|Reflection Status|Draft Status):\*\*.*?$", "", public, flags=re.M)
    return public.strip()


def render_article(text, front):
    body = markdown.markdown(
        body_markdown(text),
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    template = (ROOT / "templates" / "insight.html").read_text(encoding="utf-8")
    values = {
        "title": html.escape(front.get("Title", "World Insight")),
        "date": html.escape(front.get("Date", DATE)),
        "question": html.escape("あなたが交渉責任者なら、海峡を開くために何を譲り、何を検証可能な条件として残しますか。"),
        "body": body,
    }
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template.replace("{{ body }}", body)


def render_index(front):
    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    replacements = {
        "{{ date }}": html.escape(front.get("Date", DATE)),
        "{{ title }}": html.escape(front.get("Title", "World Insight")),
        "{{ question }}": html.escape("あなたが交渉責任者なら、海峡を開くために何を譲り、何を検証可能な条件として残しますか。"),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def render_archive(front):
    template = (ROOT / "templates" / "archive.html").read_text(encoding="utf-8")
    replacements = {
        "{{ date }}": html.escape(front.get("Date", DATE)),
        "{{ title }}": html.escape(front.get("Title", "World Insight")),
        "{{ question }}": html.escape("あなたが交渉責任者なら、海峡を開くために何を譲り、何を検証可能な条件として残しますか。"),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def main():
    text, front = read_article()
    article_html = render_article(text, front)
    (ROOT / "archive").mkdir(exist_ok=True)
    (ROOT / "archive" / f"{DATE}.html").write_text(article_html, encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(front), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(front), encoding="utf-8")
    print("Built index.html, archive.html, and archive/%s.html" % DATE)


if __name__ == "__main__":
    main()
