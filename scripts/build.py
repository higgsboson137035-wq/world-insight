#!/usr/bin/env python3
"""Build the World Insight static site from every article Markdown source."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

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
ARTICLE_DIR = ROOT / "articles"


@dataclass(frozen=True)
class Article:
    source: Path
    text: str
    front: dict[str, str]
    question: str
    summary: str

    @property
    def date(self) -> str:
        return self.front.get("Date", "")

    @property
    def title(self) -> str:
        return self.front.get("Title", "World Insight")

    @property
    def url(self) -> str:
        return f"archive/{self.date}.html"

    @property
    def reading_time(self) -> str:
        return self.front.get("Estimated Reading Time") or "10〜12分"


def parse_front(text: str) -> dict[str, str]:
    front: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", line)
        if match:
            front[match.group(1).strip()] = match.group(2).strip()
    return front


def section_blocks(text: str) -> list[tuple[str, str]]:
    """Return (H2 title, markdown body) blocks in source order."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    blocks: list[tuple[str, str]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        title = re.sub(r"^##\s+", "", lines[start]).strip()
        blocks.append((title, "\n".join(lines[start:end]).strip()))
    return blocks


def clean_public_text(text: str) -> str:
    """Remove editorial-only metadata while keeping Markdown as the source of truth."""
    public = text.split("## Editor Notes", 1)[0]
    public = public.split("## 最終自己評価", 1)[0]
    public = re.sub(r"^#\s+World Insight Pilot.*?$", "", public, flags=re.M)
    public = re.sub(
        r"^\*\*(Title|Date|Insight ID|Category|Thinking Skill|Estimated Reading Time|Reflection Status|Draft Status):\*\*.*?$",
        "",
        public,
        flags=re.M,
    )
    # The hero presents the question; the body starts at Quick Choices.
    blocks = section_blocks(public)
    kept = [body for title, body in blocks if title not in {"Thinking Journey", "Today's Question"}]
    return "\n\n".join(kept).strip()


def extract_section(text: str, title: str) -> str:
    for section_title, body in section_blocks(text):
        if section_title == title:
            return body
    return ""


def extract_question(text: str) -> str:
    block = extract_section(text, "Today's Question")
    match = re.search(r"^>\s*(.+)$", block, flags=re.M)
    question = match.group(1).strip() if match else ""
    return re.sub(r"\*\*|__", "", question)


def extract_summary(text: str) -> str:
    block = extract_section(text, "30-Second Brief")
    block = re.sub(r"^##\s+30-Second Brief\s*$", "", block, flags=re.M)
    block = re.sub(r"^###\s+.*?$", "", block, flags=re.M)
    block = re.sub(r"^[-*]\s+", "", block, flags=re.M)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
    return markdown_to_plain_text(paragraphs[0]) if paragraphs else ""


def load_articles() -> list[Article]:
    articles: list[Article] = []
    for source in sorted(ARTICLE_DIR.glob("*.md")):
        text = source.read_text(encoding="utf-8")
        front = parse_front(text)
        if not front.get("Date"):
            continue
        articles.append(Article(source, text, front, extract_question(text), extract_summary(text)))
    return sorted(articles, key=lambda article: (article.date, article.source.name), reverse=True)


def md_to_html(value: str) -> str:
    return markdown.markdown(value, extensions=["extra", "sane_lists"], output_format="html5")


class _PlainTextParser(HTMLParser):
    """Collect visible text from rendered Markdown without preserving markup or URLs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "li", "blockquote", "div"}:
            self.parts.append(" ")


def markdown_to_plain_text(value: str) -> str:
    """Render Markdown, then return normalized visible text for the index card."""
    parser = _PlainTextParser()
    parser.feed(md_to_html(value))
    parser.close()
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def h3_blocks(value: str) -> list[str]:
    lines = value.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^###\s+", line)]
    if not starts:
        return [value]
    blocks: list[str] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        blocks.append("\n".join(lines[start:end]).strip())
    return blocks


def h3_parts(value: str) -> tuple[str, list[str]]:
    """Return text before the first H3 and the H3 blocks that follow."""
    lines = value.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^###\s+", line)]
    if not starts:
        return value, []
    prefix = "\n".join(lines[: starts[0]]).strip()
    return prefix, h3_blocks(value)


def render_card_section(block: str, card_class: str) -> str:
    title, _, body = block.partition("\n")
    rendered = md_to_html(block)
    return f'<div class="{card_class}">{rendered}</div>'


def render_section(block: str, title: str) -> str:
    body = block.split("\n", 1)[1] if "\n" in block else ""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    phase_class = {
        "Quick Choices": "quick-choices-section",
        "30-Second Brief": "brief-section",
        "Decision Materials": "materials-section",
        "Human Context": "human-context-section",
        "Decision Space": "decision-space-section",
        "Virtual Cabinet": "cabinet-section",
        "What If?": "what-if-section",
        "Paradox": "paradox-section",
        "Shared Assumptions": "shared-assumptions-section",
        "Structural Question": "structural-question-section",
        "Insight Shift": "insight-shift-section",
        "Thinking Trap": "thinking-trap-section",
        "Take One Thing": "take-one-thing-section",
        "Final Question": "final-question-section",
        "Reflection": "reflection-section",
        "Sources": "sources-section",
    }.get(title, "")
    classes = f"article-section {slug} {phase_class}".strip()

    if title == "Quick Choices":
        prefix, parts = h3_parts(body)
        if parts:
            cards = "".join(render_card_section(part, "quick-choice-card") for part in parts)
            content = md_to_html(block.split("\n", 1)[0]) + md_to_html(prefix) + f'<div class="quick-choice-cards">{cards}</div>'
        else:
            content = md_to_html(block)
    elif title in {"Decision Materials", "Human Context", "What If?"}:
        prefix, parts = h3_parts(body)
        cards = "".join(render_card_section(part, "material-card" if title == "Decision Materials" else "context-card" if title == "Human Context" else "what-if-card") for part in parts)
        content = md_to_html(block.split("\n", 1)[0]) + md_to_html(prefix) + f'<div class="card-grid">{cards}</div>'
    elif title == "Virtual Cabinet":
        prefix, parts = h3_parts(body)
        cards = "".join(render_card_section(part, "choice-card") for part in parts)
        content = md_to_html(block.split("\n", 1)[0]) + md_to_html(prefix) + f'<div class="choice-grid">{cards}</div>'
    elif title == "30-Second Brief":
        prefix, parts = h3_parts(body)
        cards = "".join(render_card_section(part, "brief-card") for part in parts)
        content = md_to_html(block.split("\n", 1)[0]) + md_to_html(prefix) + f'<div class="brief-grid">{cards}</div>'
    elif title == "Insight Shift":
        steps = []
        for number, part in enumerate(h3_blocks(body), start=1):
            step_class = "shift-new" if number == 3 else ""
            steps.append(f'<div class="shift-step {step_class}"><span>{number}</span><div>{md_to_html(part)}</div></div>')
        content = md_to_html(block.split("\n", 1)[0]) + "".join(steps)
    elif title == "Thinking Trap":
        content = md_to_html(block)
    else:
        content = md_to_html(block)
    return f'<section class="{classes}" id="{slug}">{content}</section>'


def phase_label(title: str) -> tuple[str, str] | None:
    labels = {
        "Quick Choices": ("Phase 1 — Question", "まず仮の判断を持つ"),
        "30-Second Brief": ("Phase 2 — Materials", "判断材料を集める"),
        "Virtual Cabinet": ("Phase 3 — Decision", "選んだ判断を再検討する"),
        "What If?": ("Phase 4 — Challenge", "いったん決めた判断を揺さぶる"),
        "Insight Shift": ("Phase 5 — Insight Shift", "見方を一つ増やす"),
        "Thinking Trap": ("Phase 6 — Transfer", "別の判断へ持ち運ぶ"),
        "Reflection": ("Phase 7 — Reflection", "当時の判断を未来から検証する"),
    }
    return labels.get(title)


def render_article(article: Article) -> str:
    sections = section_blocks(clean_public_text(article.text))
    body_parts: list[str] = []
    rendered_phase: set[str] = set()
    for title, block in sections:
        label = phase_label(title)
        if label and label[0] not in rendered_phase:
            body_parts.append(f'<div class="journey-divider"><span>{html.escape(label[0])}</span><p>{html.escape(label[1])}</p></div>')
            rendered_phase.add(label[0])
        body_parts.append(render_section(block, title))
    template = (ROOT / "templates" / "insight.html").read_text(encoding="utf-8")
    values = {
        "title": html.escape(article.title),
        "date": html.escape(article.date),
        "reading_time": html.escape(article.reading_time),
        "question": html.escape(article.question),
        "summary": html.escape(article.summary),
        "body": "".join(body_parts),
    }
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template


def render_index(latest: Article) -> str:
    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    values = {
        "date": html.escape(latest.date),
        "title": html.escape(latest.title),
        "question": html.escape(latest.question),
        "summary": html.escape(latest.summary),
        "article_url": html.escape(latest.url),
    }
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template


def render_archive(articles: list[Article]) -> str:
    template = (ROOT / "templates" / "archive.html").read_text(encoding="utf-8")
    entries = []
    for article in articles:
        entries.append(
            '<article class="archive-entry">'
            f'<p class="date">{html.escape(article.date)}</p>'
            f'<h2>{html.escape(article.title)}</h2>'
            f'<p>{html.escape(article.question)}</p>'
            f'<a href="{html.escape(article.url)}">記事を読む</a>'
            "</article>"
        )
    return template.replace("{{ entries }}", "\n".join(entries))


def main() -> None:
    articles = load_articles()
    if not articles:
        raise SystemExit("No dated Markdown articles found in articles/.")
    archive_dir = ROOT / "archive"
    archive_dir.mkdir(exist_ok=True)
    for article in articles:
        (archive_dir / f"{article.date}.html").write_text(render_article(article), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(articles[0]), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(articles), encoding="utf-8")
    generated = ", ".join(f"archive/{article.date}.html" for article in articles)
    print(f"Built index.html, archive.html, and {generated}")


if __name__ == "__main__":
    main()
