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
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD_BRIEF_ROOT = Path.home() / "Workspace" / "world-brief"


@dataclass
class PipelineState:
    today: str
    world_brief: Path | None
    world_brief_status: str
    daily_editorial: Path
    source_verification: str
    source_verification_link: str
    source_verification_file: Path | None
    source_verification_signal: str
    article: Path | None
    article_text: str
    editorial_review: str
    review_decision: str
    required_fixes: str
    insight_shift: str
    insight_shift_review: str
    take_one_thing: str
    editorial_readiness: str
    build: str
    human_read: str
    technical_validation: str
    local_preview: str
    safari: str
    chrome: str
    git_diff_review: str
    final_approval: str
    daily_result: str
    fallback_attempts: int
    no_publish_confirmation: str
    publish_readiness: str
    next_action: str


def latest_world_brief(on_or_before: str | None = None) -> Path | None:
    briefs = WORLD_BRIEF_ROOT / "briefs"
    if not briefs.is_dir():
        return None
    cutoff = date.fromisoformat(on_or_before) if on_or_before else None
    candidates = []
    for path in briefs.glob("*.md"):
        try:
            issue_date = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if cutoff is None or issue_date <= cutoff:
            candidates.append(path)
    candidates.sort(key=lambda path: path.stem, reverse=True)
    return candidates[0] if candidates else None


def world_brief_for_date(today: str) -> Path | None:
    path = WORLD_BRIEF_ROOT / "briefs" / f"{today}.md"
    return path if path.exists() else None


def world_brief_state(today: str, selected: Path | None = None) -> str:
    """Distinguish today's brief from an older available issue."""
    if world_brief_for_date(today):
        return "FOUND"
    return "STALE" if selected or latest_world_brief(today) else "MISSING"


def selected_topic_value(text: str) -> str | None:
    """Return a concrete topic recorded in the Selected Topic section."""
    section = re.search(
        r"^##\s+Step\s+(?:2|3)\s+[—-]\s+Selected Topic\s*$([\s\S]*?)(?=^##\s|\Z)",
        text,
        re.I | re.M,
    )
    if not section:
        return None
    match = re.search(
        r"^[ \t]*-[ \t]*(?:\*\*)?(?:採用テーマ|Selected Topic)[ \t]*[:：](?:\*\*)?[ \t]*([^\n]*)$",
        section.group(1),
        re.I | re.M,
    )
    if not match:
        return None
    value = re.sub(r"^[`*_\s]+|[`*_\s]+$", "", match.group(1)).strip()
    normalized = re.sub(r"[\s._-]+", "", value).casefold()
    invalid = {
        "", "—", "-", "tbd", "todo", "未定", "未選択", "placeholder",
        "採用テーマ", "selected topic", "テーマ", "説明文", "見出し",
    }
    if normalized in {re.sub(r"[\s._-]+", "", item).casefold() for item in invalid}:
        return None
    # Template examples and labels are not editorial decisions.
    if re.fullmatch(r"candidate\s*\d+(?:\s*[（(].*[）)])?", value, re.I):
        return None
    return value


def selected_topic_present(text: str) -> bool:
    """Recognize a concrete topic recorded in the Selected Topic section."""
    return selected_topic_value(text) is not None


def metadata_value(text: str, label: str) -> str | None:
    """Read an explicit one-line Markdown metadata value."""
    match = re.search(
        rf"^[ \t]*-[ \t]*(?:\*\*)?{re.escape(label)}[ \t]*[:：](?:\*\*)?[ \t]*([^\n]+)$",
        text,
        re.I | re.M,
    )
    if not match:
        return None
    value = re.sub(r"^[`*_\s]+|[`*_\s]+$", "", match.group(1)).strip()
    return value or None


def topics_correspond(daily_topic: str, verification_topic: str) -> bool:
    """Require strong literal overlap between two explicit topic labels."""
    normalize = lambda value: re.sub(r"[^0-9a-z一-龠ぁ-んァ-ヶ]+", "", value.casefold())
    daily = normalize(daily_topic)
    verification = normalize(verification_topic)
    if not daily or not verification:
        return False
    if daily == verification or daily in verification or verification in daily:
        return True
    shorter = min(len(daily), len(verification))
    common = SequenceMatcher(None, daily, verification).find_longest_match().size
    return common >= 12 and common / shorter >= 0.7


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


def topic_verification_matches(today: str, daily_text: str, candidates: list[Path]) -> list[tuple[Path, str]]:
    """Find records explicitly matching the daily date and selected topic."""
    daily_topic = selected_topic_value(daily_text)
    if daily_topic is None:
        return []
    matches = []
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        verification_date = metadata_value(text, "Date")
        verification_topic = metadata_value(text, "Selected Topic")
        if (verification_date == today and verification_topic
                and topics_correspond(daily_topic, verification_topic)):
            matches.append((path, verdict(text)))
    return matches


def source_verification_status(today: str, daily_text: str, article: Path | None) -> tuple[str, str, Path | None, str]:
    """Return verdict, link state, linked file, and unlinked candidate signal."""
    candidates = sorted((ROOT / "docs").glob("*SOURCE_VERIFICATION*.md"), reverse=True)
    if article is None:
        topic_linked = topic_verification_matches(today, daily_text, candidates)
        if len(topic_linked) == 1:
            path, result = topic_linked[0]
            return result, "TOPIC_VERIFIED", path, result
        if len(topic_linked) > 1:
            return "UNRESOLVED", "UNRESOLVED", None, "AMBIGUOUS"
        return "NOT_STARTED", "UNRESOLVED", None, "NOT_STARTED"
    linked = [(path, verdict(path.read_text(encoding="utf-8")))
              for path in candidates if explicit_article_link(path.read_text(encoding="utf-8"), article)]
    if len(linked) == 1:
        path, result = linked[0]
        return result, "VERIFIED", path, result
    if len(linked) > 1:
        # Multiple explicit records need a human to resolve which one governs.
        return "UNRESOLVED", "UNRESOLVED", None, "AMBIGUOUS"
    topic_linked = topic_verification_matches(today, daily_text, candidates)
    if len(topic_linked) == 1:
        path, result = topic_linked[0]
        # Once an article exists, topic metadata identifies the one candidate
        # record but cannot replace the required explicit Article link.
        return "UNRESOLVED", "UNRESOLVED", path, result
    if len(topic_linked) > 1:
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


def evaluate_quality(text: str, review_quality: dict[str, str] | None = None) -> tuple[str, str]:
    """Prefer a completed independent review, then fall back to article signals."""
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
    review_quality = review_quality or {}
    if review_quality.get("Insight Shift") in {"A", "B", "C"}:
        insight = review_quality["Insight Shift"]
    if review_quality.get("Take One Thing") in {"PASS", "NEEDS_WORK", "FAIL"}:
        take = review_quality["Take One Thing"]
    return insight, take


def insight_shift_gate_passed(insight_shift: str, insight_shift_review: str) -> bool:
    """Pass A directly and B only after an explicit human approval."""
    return insight_shift == "A" or (
        insight_shift == "B" and insight_shift_review == "APPROVED"
    )


def review_field_value(text: str, label: str) -> str | None:
    """Read an explicit review field in metadata or Markdown-list form."""
    match = re.search(
        rf"^[ \t]*(?:-[ \t]*)?(?:\*\*)?{re.escape(label)}(?:\*\*)?[ \t]*[:：](?:\*\*)?[ \t]*([^\n]+)$",
        text,
        re.I | re.M,
    )
    if not match:
        return None
    value = re.sub(r"^[`*_\s]+|[`*_\s]+$", "", match.group(1)).strip()
    return value or None


def final_decision_value(text: str) -> str | None:
    value = review_field_value(text, "Final Decision")
    if not value:
        return None
    match = re.match(r"([ABC])(?:\b|\s|[—-])", value.strip(), re.I)
    return match.group(1).upper() if match else None


def required_fixes_value(text: str) -> str:
    value = review_field_value(text, "Required Fixes Status")
    if value:
        normalized = re.sub(r"[\s-]+", "_", value).upper()
        if normalized in {"NONE", "RESOLVED", "OPEN"}:
            return normalized
    if re.search(r"^##\s+Required Fixes\s+[—-]\s+Resolved\s*$", text, re.I | re.M):
        return "RESOLVED"
    return "NOT_RECORDED"


def editorial_review_record(article: Path | None) -> tuple[str, str, str, dict[str, str]]:
    """Return status and explicit quality values from one linked review record."""
    if article is None:
        return "UNRESOLVED", "NOT_RECORDED", "NOT_RECORDED", {}
    records: list[tuple[str, str]] = []
    for path in sorted((ROOT / "docs").glob("*REVIEW*.md"), reverse=True):
        text = path.read_text(encoding="utf-8")
        if not explicit_article_link(text, article):
            continue
        status = review_field_value(text, "Review Status") or review_field_value(text, "Editorial Review")
        if status and status.upper() in {"COMPLETE", "PENDING", "UNRESOLVED"}:
            records.append((status.upper(), text))
    if len(records) != 1:
        return "UNRESOLVED", "NOT_RECORDED", "NOT_RECORDED", {}
    status, text = records[0]
    decision = final_decision_value(text)
    fixes = required_fixes_value(text)
    if status != "COMPLETE":
        return status, decision or "NOT_RECORDED", fixes, {}

    allowed = {
        "Insight Shift": {"A", "B", "C"},
        "Thinking Trap": {"PASS", "NEEDS_WORK", "FAIL"},
        "Take One Thing": {"PASS", "NEEDS_WORK", "FAIL"},
        "A/B/C Fairness": {"PASS", "NEEDS_WORK", "FAIL"},
        "Is it true?": {"PASS", "NEEDS_WORK", "FAIL"},
        "Is it fair?": {"PASS", "NEEDS_WORK", "FAIL"},
        "Is it useful?": {"PASS", "NEEDS_WORK", "FAIL"},
    }
    quality: dict[str, str] = {}
    for label, accepted in allowed.items():
        value = review_field_value(text, label)
        if value:
            normalized = re.sub(r"[\s-]+", "_", value).upper()
            if normalized in accepted:
                quality[label] = normalized
    quality_needs_work = any(value in {"NEEDS_WORK", "FAIL"} for value in quality.values())
    if decision == "C":
        review_state = "HOLD"
    elif decision == "B" or fixes == "OPEN" or quality_needs_work:
        review_state = "NEEDS_FIX"
    elif decision == "A":
        review_state = "PASS"
    else:
        # Backward compatibility: old COMPLETE records without Final Decision
        # retain their historic completion semantics.
        review_state = "PASS"
    return review_state, decision or "LEGACY_COMPLETE", fixes, quality


def editorial_review_status(article: Path | None) -> str:
    """Only one independent, explicitly linked review determines status."""
    return editorial_review_record(article)[0]


def daily_metadata(daily_text: str) -> tuple[str, int, str]:
    result = (metadata_value(daily_text, "Daily Result") or "IN_PROGRESS").upper()
    if result not in {"IN_PROGRESS", "NO_PUBLISH", "READY_TO_PUBLISH", "PUBLISHED"}:
        result = "IN_PROGRESS"
    attempts_record = metadata_value(daily_text, "Fallback Attempts")
    attempts_value = attempts_record or ("1" if "Fallback Candidate Selection" in daily_text else "0")
    try:
        attempts = max(0, int(attempts_value))
    except ValueError:
        attempts = 0
    confirmation = (metadata_value(daily_text, "NO_PUBLISH Confirmation") or "PENDING").upper()
    return result, attempts, confirmation


def build_is_fresh(article: Path | None) -> bool:
    """Require generated files to be at least as new as every relevant input."""
    if article is None:
        return False
    date_match = re.search(r"^\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})\s*$", article.read_text(encoding="utf-8"), re.M)
    if not date_match:
        return False
    article_html = ROOT / "archive" / f"{date_match.group(1)}.html"
    index_html = ROOT / "index.html"
    archive_html = ROOT / "archive.html"
    outputs = (article_html, index_html, archive_html)
    if not all(path.exists() for path in outputs):
        return False

    build_script = ROOT / "scripts" / "build.py"
    article_inputs = (article, build_script, ROOT / "templates" / "insight.html")
    all_articles = tuple((ROOT / "articles").glob("*.md"))
    index_inputs = all_articles + (build_script, ROOT / "templates" / "index.html")
    archive_inputs = all_articles + (build_script, ROOT / "templates" / "archive.html")
    groups = (
        (article_html, article_inputs),
        (index_html, index_inputs),
        (archive_html, archive_inputs),
    )
    for output, inputs in groups:
        if not inputs or not all(path.exists() for path in inputs):
            return False
        if output.stat().st_mtime_ns < max(path.stat().st_mtime_ns for path in inputs):
            return False
    return True


def manual_record(today: str, article: Path | None) -> dict[str, str]:
    defaults = {
        "Insight Shift Review": "PENDING",
        "Human Read": "PENDING", "Technical Validation": "NOT_STARTED",
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
    if defaults["Insight Shift Review"] not in {"PENDING", "APPROVED"}:
        defaults["Insight Shift Review"] = "INVALID"
    # Old Pilot and 2026-08-13 records predate the explicit consolidated fields.
    if defaults["Human Read"] == "PENDING" and defaults["Local Preview"] == "COMPLETE":
        defaults["Human Read"] = "COMPLETE"
    if defaults["Technical Validation"] == "NOT_STARTED" and defaults["Git Diff Review"] == "COMPLETE":
        defaults["Technical Validation"] = "PASS"
    return defaults


def publish_readiness(state: PipelineState) -> tuple[str, str]:
    if state.daily_result == "NO_PUBLISH":
        if state.no_publish_confirmation == "CONFIRMED":
            return "NOT_APPLICABLE", "None — editorial day completed without publication."
        return "NEEDS_NO_PUBLISH_CONFIRMATION", "Confirm the NO_PUBLISH editorial decision."
    if state.daily_result == "PUBLISHED":
        return "PUBLISHED", "None — publication is already recorded."
    if state.source_verification == "HOLD_C":
        if state.fallback_attempts >= 1:
            return "NEEDS_NO_PUBLISH_DECISION", "Record and confirm NO_PUBLISH; the fallback limit is reached."
        return "BLOCKED", "Select the single allowed fallback candidate."
    if state.source_verification == "NOT_STARTED":
        return "BLOCKED", "Start Source Verification for the selected topic."
    if state.article is None and state.source_verification in {"PASS_A", "PASS_B"}:
        return "BLOCKED", "Draft the article."
    if state.source_verification_link != "VERIFIED" or state.source_verification == "UNRESOLVED":
        return "BLOCKED", "Add an explicit article-to-source link and resolve Source Verification."
    if state.editorial_review == "NEEDS_FIX":
        return "NEEDS_REVIEW", "Apply only the required editorial fixes, then re-review."
    if state.editorial_review == "HOLD":
        return "NEEDS_NO_PUBLISH_DECISION", "Record and confirm NO_PUBLISH after Editorial Review C."
    if state.insight_shift == "C" or state.take_one_thing == "FAIL":
        return "BLOCKED", "Resolve the blocked quality gate before publication."
    if state.editorial_review in {"UNRESOLVED", "PENDING"} or not insight_shift_gate_passed(state.insight_shift, state.insight_shift_review) or state.take_one_thing == "NEEDS_WORK":
        return "NEEDS_REVIEW", "Complete the independent Editorial Review and quality gates."
    if state.human_read != "COMPLETE":
        return "NEEDS_HUMAN_READ", "Complete the human meaning and reading-quality review."
    if state.build != "READY" or state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        return "NEEDS_PREVIEW", "Complete Build and Safari/Chrome Local Preview checks."
    if state.technical_validation != "PASS":
        return "NEEDS_TECHNICAL_VALIDATION", "Complete the technical validation record."
    if state.git_diff_review != "COMPLETE":
        return "NEEDS_GIT_REVIEW", "Complete the human Git Diff Review."
    if state.final_approval == "REJECTED":
        return "BLOCKED", "Final Approval was rejected; resolve the recorded issue."
    if state.final_approval == "PENDING":
        return "WAITING_FOR_APPROVAL", "Record Final Approval after all checks pass."
    return "READY_TO_PUBLISH", "Manual publish may proceed; no git push is performed by this tool."


def inspect(today: str, prepare: bool = True) -> PipelineState:
    brief = world_brief_for_date(today) or latest_world_brief(today)
    daily = prepare_daily_editorial(today) if prepare else ROOT / "docs" / f"DAILY_EDITORIAL_{today}.md"
    daily_text = daily.read_text(encoding="utf-8") if daily.exists() else ""
    article = find_article(today)
    article_text = article.read_text(encoding="utf-8") if article else ""
    source, source_link, source_file, source_signal = source_verification_status(today, daily_text, article)
    review, review_decision, required_fixes, review_quality = editorial_review_record(article)
    insight, take = evaluate_quality(article_text, review_quality)
    manual = manual_record(today, article)
    daily_result, fallback_attempts, no_publish_confirmation = daily_metadata(daily_text)
    build_ready = build_is_fresh(article)
    required_sections = ("Today's Question", "Quick Choices", "Human Context", "Decision Space", "Insight Shift", "Take One Thing")
    candidate_selected = selected_topic_present(daily_text)
    seeds_present = "Insight Shift Seed" in daily_text and "Take One Thing Seed" in daily_text
    editorial_ready = bool(candidate_selected and seeds_present and article and all(section_present(article_text, section) for section in required_sections) and source in {"PASS_A", "PASS_B"} and source_link == "VERIFIED")
    state = PipelineState(today, brief, world_brief_state(today, brief), daily, source, source_link, source_file, source_signal, article, article_text, review, review_decision, required_fixes, insight, manual["Insight Shift Review"], take,
                          "READY" if editorial_ready else "NOT_READY", "READY" if build_ready else "NOT_READY",
                          manual["Human Read"], manual["Technical Validation"], manual["Local Preview"], manual["Safari"], manual["Chrome"], manual["Git Diff Review"], manual["Final Approval"], daily_result, fallback_attempts, no_publish_confirmation, "", "")
    state.publish_readiness, state.next_action = publish_readiness(state)
    if state.daily_result == "IN_PROGRESS" and state.publish_readiness == "READY_TO_PUBLISH":
        state.daily_result = "READY_TO_PUBLISH"
    return state


def print_state(state: PipelineState) -> None:
    def found(path: Path | None) -> str:
        return "FOUND" if path and path.exists() else "MISSING"

    print("World Insight Morning Editorial Pipeline")
    print(f"\nDate: {state.today}")
    print(f"Article: {state.article.relative_to(ROOT) if state.article else 'MISSING'}")
    print(f"World Brief: {state.world_brief_status}" + (f" ({state.world_brief.name})" if state.world_brief else ""))
    print(f"Daily Editorial: {found(state.daily_editorial)}")
    print(f"Source Verification: {state.source_verification}")
    print(f"Source Verification Link: {state.source_verification_link}")
    if state.source_verification_file:
        print(f"Source Verification File: {state.source_verification_file.relative_to(ROOT)}")
    elif state.source_verification_signal != "NOT_STARTED":
        print(f"Source Verification Signal: {state.source_verification_signal} (unlinked; not a gate pass)")
    print(f"Editorial Review: {state.editorial_review}")
    print(f"Review Decision: {state.review_decision}")
    print(f"Required Fixes: {state.required_fixes}")
    print(f"Insight Shift: {state.insight_shift}")
    print(f"Insight Shift Review: {state.insight_shift_review}")
    print(f"Take One Thing: {state.take_one_thing}")
    print(f"Editorial Readiness: {state.editorial_readiness}")
    print(f"Build: {state.build}")
    print(f"Human Read: {state.human_read}")
    print(f"Technical Validation: {state.technical_validation}")
    print(f"Local Preview: {state.local_preview}")
    print(f"Safari: {state.safari}")
    print(f"Chrome: {state.chrome}")
    print(f"Git Diff Review: {state.git_diff_review}")
    print(f"Final Approval: {state.final_approval}")
    print(f"Daily Result: {state.daily_result}")
    print(f"Fallback Attempts: {state.fallback_attempts}")
    print(f"Publish Readiness: {state.publish_readiness}")
    print(f"Next Action: {state.next_action}")
    if state.daily_result == "NO_PUBLISH" and state.no_publish_confirmation == "CONFIRMED":
        publish_label = "NO_PUBLISH"
    elif state.publish_readiness == "READY_TO_PUBLISH":
        publish_label = "READY"
    elif state.publish_readiness == "PUBLISHED":
        publish_label = "PUBLISHED"
    else:
        publish_label = "HOLD"
    print(f"Publish: {publish_label}")
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
