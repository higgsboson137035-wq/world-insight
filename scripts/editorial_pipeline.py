#!/usr/bin/env python3
"""Inspect the human-in-the-loop Morning Editorial and Publish Gates.

The pipeline reads explicit Markdown records.  It never creates article prose,
assigns editorial quality semantically, commits, pushes, or publishes.
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
    source_verification_link: str
    source_verification_file: Path | None
    source_verification_signal: str
    article: Path | None
    article_text: str
    editorial_review: str
    insight_shift: str
    take_one_thing: str
    editorial_readiness: str
    build: str
    local_preview: str
    safari: str
    chrome: str
    git_diff_review: str
    final_approval: str
    publish_readiness: str
    next_action: str


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


def verdict(text: str) -> str:
    patterns = (
        (r"(?:判定|Article Decision|Source Verification)[^\n]*(?:\bA\b|PASS_A)", "PASS_A"),
        (r"(?:判定|Article Decision|Source Verification)[^\n]*(?:\bB\b|PASS_B)", "PASS_B"),
        (r"(?:判定|Article Decision|Source Verification)[^\n]*(?:\bC\b|HOLD_C)", "HOLD_C"),
    )
    for pattern, result in patterns:
        if re.search(pattern, text, re.I):
            return result
    return "NOT_STARTED"


def explicit_article_link(text: str, article: Path) -> bool:
    relative = article.relative_to(ROOT).as_posix()
    # A source/review record must name the article; date or filename similarity
    # is deliberately insufficient.
    return bool(re.search(rf"(?:\*\*)?(?:Article|記事|対象記事)(?:\*\*)?\s*[:：]\s*(?:\*\*)?\s*`?{re.escape(relative)}`?", text, re.I))


def source_verification_status(article: Path | None) -> tuple[str, str, Path | None, str]:
    """Return verdict, link state, linked file, and unlinked candidate signal."""
    if article is None:
        return "NOT_STARTED", "UNRESOLVED", None, "NOT_STARTED"
    candidates = sorted((ROOT / "docs").glob("*SOURCE_VERIFICATION*.md"), reverse=True)
    linked = [(path, verdict(path.read_text(encoding="utf-8")))
              for path in candidates if explicit_article_link(path.read_text(encoding="utf-8"), article)]
    if len(linked) == 1:
        path, result = linked[0]
        return result, "VERIFIED", path, result
    if len(linked) > 1:
        # Multiple explicit records need a human to resolve which one governs.
        return "UNRESOLVED", "UNRESOLVED", None, "AMBIGUOUS"
    likely = [path for path in candidates if article.stem.lower() in path.name.lower()]
    likely_verdicts = {verdict(path.read_text(encoding="utf-8")) for path in likely}
    # Multiple same-day candidate records (for example HOLD_C and PASS_A)
    # are intentionally reported as ambiguous until a human links one.
    signal = next(iter(likely_verdicts)) if len(likely_verdicts) == 1 else ("AMBIGUOUS" if likely_verdicts else "NOT_STARTED")
    return "UNRESOLVED", "UNRESOLVED", None, signal


def find_article(today: str) -> Path | None:
    for article in sorted((ROOT / "articles").glob("*.md")):
        if re.search(rf"^\*\*Date:\*\*\s*{re.escape(today)}\s*$", article.read_text(encoding="utf-8"), re.M):
            return article
    return None


def section_present(text: str, title: str) -> bool:
    return bool(re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.M))


def evaluate_quality(text: str) -> tuple[str, str]:
    """Read explicit article signals; do not infer semantic quality."""
    insight = "NOT_RECORDED"
    take = "NOT_RECORDED"
    if re.search(r"\*\*Insight Shift:\*\*\s*PASS", text, re.I) and section_present(text, "Insight Shift"):
        insight = "A"
    elif section_present(text, "Insight Shift"):
        insight = "NEEDS_HUMAN_REVIEW"
    if re.search(r"\*\*Take One Thing:\*\*\s*PASS", text, re.I) and section_present(text, "Take One Thing"):
        take = "PASS"
    elif section_present(text, "Take One Thing"):
        take = "NEEDS_WORK"
    return insight, take


def editorial_review_status(article: Path | None) -> str:
    """Only an independent, explicitly linked review can be COMPLETE."""
    if article is None:
        return "UNRESOLVED"
    records = []
    for path in sorted((ROOT / "docs").glob("*REVIEW*.md"), reverse=True):
        text = path.read_text(encoding="utf-8")
        if not explicit_article_link(text, article):
            continue
        match = re.search(r"(?:Editorial Review|Review Status)\s*[:：]\s*(COMPLETE|PENDING|UNRESOLVED)", text, re.I)
        if match:
            records.append(match.group(1).upper())
    if len(records) == 1:
        return records[0]
    return "UNRESOLVED"


def manual_record(today: str, article: Path | None) -> dict[str, str]:
    defaults = {
        "Local Preview": "NOT_CHECKED", "Safari": "NOT_CHECKED", "Chrome": "NOT_CHECKED",
        "Git Diff Review": "NOT_CHECKED", "Final Approval": "PENDING",
    }
    if article is None:
        return defaults
    record = ROOT / "docs" / f"PUBLISH_{today}.md"
    if not record.exists() or not explicit_article_link(record.read_text(encoding="utf-8"), article):
        return defaults
    text = record.read_text(encoding="utf-8")
    for key in defaults:
        match = re.search(rf"^{re.escape(key)}\s*[:：]\s*([^\n]+)", text, re.I | re.M)
        if match:
            defaults[key] = match.group(1).strip().upper()
    return defaults


def publish_readiness(state: PipelineState) -> tuple[str, str]:
    if state.source_verification_link != "VERIFIED" or state.source_verification in {"UNRESOLVED", "HOLD_C", "NOT_STARTED"}:
        return "BLOCKED", "Add an explicit article-to-source link and resolve Source Verification."
    if state.insight_shift == "C" or state.take_one_thing == "FAIL":
        return "BLOCKED", "Resolve the blocked quality gate before publication."
    if state.editorial_review in {"UNRESOLVED", "PENDING"} or state.insight_shift in {"B", "NEEDS_HUMAN_REVIEW"} or state.take_one_thing == "NEEDS_WORK":
        return "NEEDS_REVIEW", "Complete the independent Editorial Review and quality gates."
    if state.build != "READY" or state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        return "NEEDS_PREVIEW", "Complete Build and Safari/Chrome Local Preview checks."
    if state.git_diff_review != "COMPLETE":
        return "NEEDS_GIT_REVIEW", "Complete the human Git Diff Review."
    if state.final_approval == "REJECTED":
        return "BLOCKED", "Final Approval was rejected; resolve the recorded issue."
    if state.final_approval == "PENDING":
        return "WAITING_FOR_APPROVAL", "Record Final Approval after all checks pass."
    return "READY_TO_PUBLISH", "Manual publish may proceed; no git push is performed by this tool."


def inspect(today: str, prepare: bool = True) -> PipelineState:
    brief = latest_world_brief()
    daily = prepare_daily_editorial(today) if prepare else ROOT / "docs" / f"DAILY_EDITORIAL_{today}.md"
    daily_text = daily.read_text(encoding="utf-8") if daily.exists() else ""
    article = find_article(today)
    article_text = article.read_text(encoding="utf-8") if article else ""
    insight, take = evaluate_quality(article_text)
    source, source_link, source_file, source_signal = source_verification_status(article)
    review = editorial_review_status(article)
    manual = manual_record(today, article)
    build_ready = all((ROOT / path).exists() for path in ("index.html", "archive.html")) and article is not None and (ROOT / "archive" / f"{today}.html").exists()
    required_sections = ("Today's Question", "Quick Choices", "Human Context", "Decision Space", "Insight Shift", "Take One Thing")
    candidate_selected = bool(re.search(r"採用テーマ\s*[:：]\s*\S+", daily_text))
    seeds_present = "Insight Shift Seed" in daily_text and "Take One Thing Seed" in daily_text
    editorial_ready = bool(candidate_selected and seeds_present and article and all(section_present(article_text, section) for section in required_sections) and source in {"PASS_A", "PASS_B"} and source_link == "VERIFIED")
    state = PipelineState(today, brief, daily, source, source_link, source_file, source_signal, article, article_text, review, insight, take,
                          "READY" if editorial_ready else "NOT_READY", "READY" if build_ready else "NOT_READY",
                          manual["Local Preview"], manual["Safari"], manual["Chrome"], manual["Git Diff Review"], manual["Final Approval"], "", "")
    state.publish_readiness, state.next_action = publish_readiness(state)
    return state


def print_state(state: PipelineState) -> None:
    def found(path: Path | None) -> str:
        return "FOUND" if path and path.exists() else "MISSING"

    print("World Insight Morning Editorial Pipeline")
    print(f"\nDate: {state.today}")
    print(f"Article: {state.article.relative_to(ROOT) if state.article else 'MISSING'}")
    print(f"World Brief: {found(state.world_brief)}" + (f" ({state.world_brief.name})" if state.world_brief else ""))
    print(f"Daily Editorial: {found(state.daily_editorial)}")
    print(f"Source Verification: {state.source_verification}")
    print(f"Source Verification Link: {state.source_verification_link}")
    if state.source_verification_file:
        print(f"Source Verification File: {state.source_verification_file.relative_to(ROOT)}")
    elif state.source_verification_signal != "NOT_STARTED":
        print(f"Source Verification Signal: {state.source_verification_signal} (unlinked; not a gate pass)")
    print(f"Editorial Review: {state.editorial_review}")
    print(f"Insight Shift: {state.insight_shift}")
    print(f"Take One Thing: {state.take_one_thing}")
    print(f"Editorial Readiness: {state.editorial_readiness}")
    print(f"Build: {state.build}")
    print(f"Local Preview: {state.local_preview}")
    print(f"Safari: {state.safari}")
    print(f"Chrome: {state.chrome}")
    print(f"Git Diff Review: {state.git_diff_review}")
    print(f"Final Approval: {state.final_approval}")
    print(f"Publish Readiness: {state.publish_readiness}")
    print(f"Next Action: {state.next_action}")
    print("Publish: MANUAL APPROVAL REQUIRED")
    print("\nHuman decisions are required for source mapping, review, quality, preview, diff review, and publication.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect World Insight's human-in-the-loop morning and publish gates.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Pipeline date (YYYY-MM-DD).")
    parser.add_argument("--no-prepare", action="store_true", help="Do not create a missing daily editorial work file.")
    args = parser.parse_args()
    if args.no_prepare and not (ROOT / "docs" / f"DAILY_EDITORIAL_{args.date}.md").exists():
        raise SystemExit(f"Daily Editorial is missing: {ROOT / 'docs' / f'DAILY_EDITORIAL_{args.date}.md'}")
    print_state(inspect(args.date, prepare=not args.no_prepare))


if __name__ == "__main__":
    main()
