#!/usr/bin/env python3
"""Prepare and inspect the human-in-the-loop Morning Editorial Pipeline.

This script checks files and explicit editorial signals. It does not generate
article prose, score Insight Shift semantics, commit, push, or publish.
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD_BRIEF_ROOT = Path.home() / "Workspace" / "world-brief"


@dataclass
class PipelineState:
    today: str
    world_brief: Path | None
    daily_editorial: Path
    source_verification: str
    article: Path | None
    article_text: str
    editorial_review: str
    insight_shift: str
    take_one_thing: str
    editorial_readiness: str
    build: str
    publish_readiness: str


def latest_world_brief() -> Path | None:
    briefs = WORLD_BRIEF_ROOT / "briefs"
    if not briefs.is_dir():
        return None
    candidates = sorted(briefs.glob("*.md"), reverse=True)
    return candidates[0] if candidates else None


def prepare_daily_editorial(today: str) -> Path:
    destination = ROOT / "docs" / f"DAILY_EDITORIAL_{today}.md"
    if destination.exists():
        return destination
    template = ROOT / "DAILY_EDITORIAL.md"
    if not template.exists():
        raise SystemExit("DAILY_EDITORIAL.md is required to prepare a daily work file.")
    destination.parent.mkdir(exist_ok=True)
    shutil.copyfile(template, destination)
    return destination


def source_verification_status(article_stem: str) -> str:
    docs = ROOT / "docs"
    candidates = sorted(docs.glob("*SOURCE_VERIFICATION*.md"), reverse=True)
    # Prefer a B/fallback verification for the matching pilot when present.
    matching = [p for p in candidates if article_stem.split("_")[-1] in p.name.lower()]
    candidates = matching or candidates
    candidates.sort(key=lambda path: ("b_source_verification" not in path.name.lower(), path.name))
    for candidate in candidates:
        text = candidate.read_text(encoding="utf-8")
        if re.search(r"(?:判定|Article Decision)[^\n]*\bA\b|PASS_A", text, re.I):
            return "PASS_A"
        if re.search(r"(?:判定|Article Decision)[^\n]*\bB\b|PASS_B", text, re.I):
            return "PASS_B"
        if re.search(r"(?:判定|Article Decision)[^\n]*\bC\b|HOLD_C", text, re.I):
            return "HOLD_C"
    return "NOT_STARTED"


def find_article(today: str) -> Path | None:
    for article in sorted((ROOT / "articles").glob("*.md")):
        if re.search(rf"^\*\*Date:\*\*\s*{re.escape(today)}\s*$", article.read_text(encoding="utf-8"), re.M):
            return article
    return None


def section_present(text: str, title: str) -> bool:
    return bool(re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.M))


def evaluate_quality(text: str) -> tuple[str, str]:
    insight = "NOT_RECORDED"
    take = "NOT_RECORDED"
    if re.search(r"\*\*Insight Shift:\*\*\s*PASS", text, re.I) and section_present(text, "Insight Shift"):
        # The PASS signal is an editorial/self-review record, not an automatic semantic score.
        insight = "A"
    elif section_present(text, "Insight Shift"):
        insight = "NEEDS_HUMAN_REVIEW"
    if re.search(r"\*\*Take One Thing:\*\*\s*PASS", text, re.I) and section_present(text, "Take One Thing"):
        take = "PASS"
    elif section_present(text, "Take One Thing"):
        take = "NEEDS_WORK"
    return insight, take


def editorial_review_status(text: str) -> str:
    if "## 最終自己評価" in text and re.search(r"Is it true\?\*\*\s*PASS", text, re.I) and re.search(r"Is it fair\?\*\*\s*PASS", text, re.I) and re.search(r"Is it useful\?\*\*\s*PASS", text, re.I):
        return "COMPLETE"
    return "NOT_RECORDED"


def inspect(today: str, prepare: bool = True) -> PipelineState:
    brief = latest_world_brief()
    daily = prepare_daily_editorial(today) if prepare else ROOT / "docs" / f"DAILY_EDITORIAL_{today}.md"
    daily_text = daily.read_text(encoding="utf-8") if daily.exists() else ""
    article = find_article(today)
    article_text = article.read_text(encoding="utf-8") if article else ""
    insight, take = evaluate_quality(article_text)
    build_ready = all((ROOT / path).exists() for path in ("index.html", "archive.html")) and article is not None and (ROOT / "archive" / f"{today}.html").exists()
    source = source_verification_status(article.stem if article else "")
    required_sections = ("Today's Question", "Quick Choices", "Human Context", "Decision Space", "Insight Shift", "Take One Thing")
    candidate_selected = bool(re.search(r"採用テーマ\s*[:：]\s*\S+", daily_text))
    seeds_present = "Insight Shift Seed" in daily_text and "Take One Thing Seed" in daily_text
    editorial_ready = bool(candidate_selected and seeds_present and article and all(section_present(article_text, section) for section in required_sections) and source in {"PASS_A", "PASS_B"})
    publish_ready = bool(editorial_ready and editorial_review_status(article_text) == "COMPLETE" and insight in {"A", "B"} and take == "PASS" and build_ready)
    return PipelineState(
        today=today,
        world_brief=brief,
        daily_editorial=daily,
        source_verification=source,
        article=article,
        article_text=article_text,
        editorial_review=editorial_review_status(article_text),
        insight_shift=insight,
        take_one_thing=take,
        editorial_readiness="READY" if editorial_ready else "NOT_READY",
        build="READY" if build_ready else "NOT_READY",
        publish_readiness="MANUAL_CHECK_REQUIRED" if publish_ready else "NOT_READY",
    )


def print_state(state: PipelineState) -> None:
    def found(path: Path | None) -> str:
        return "FOUND" if path and path.exists() else "MISSING"

    print("World Insight Morning Editorial Pipeline")
    print(f"\nDate: {state.today}")
    print(f"World Brief: {found(state.world_brief)}" + (f" ({state.world_brief.name})" if state.world_brief else ""))
    print(f"Daily Editorial: {found(state.daily_editorial)}")
    print(f"Source Verification: {state.source_verification}")
    print(f"Article Draft: {found(state.article)}")
    print(f"Editorial Review: {state.editorial_review}")
    print(f"Insight Shift: {state.insight_shift}")
    print(f"Take One Thing: {state.take_one_thing}")
    print(f"Editorial Readiness: {state.editorial_readiness}")
    print(f"Build: {state.build}")
    print(f"Publish Readiness: {state.publish_readiness}")
    print("Publish: MANUAL APPROVAL REQUIRED")
    print("\nHuman decisions are required for topic selection, source gates, quality gates, review, and publication.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect World Insight's human-in-the-loop morning pipeline.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Pipeline date (YYYY-MM-DD).")
    parser.add_argument("--no-prepare", action="store_true", help="Do not create a missing daily editorial work file.")
    args = parser.parse_args()
    if args.no_prepare and not (ROOT / "docs" / f"DAILY_EDITORIAL_{args.date}.md").exists():
        raise SystemExit(f"Daily Editorial is missing: {ROOT / 'docs' / f'DAILY_EDITORIAL_{args.date}.md'}")
    print_state(inspect(args.date, prepare=not args.no_prepare))


if __name__ == "__main__":
    main()
