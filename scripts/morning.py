#!/usr/bin/env python3
"""Short daily entry point for the human-in-the-loop editorial pipeline."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from editorial_pipeline import (  # noqa: E402
    PipelineState,
    inspect,
    insight_shift_gate_passed,
    prepare_daily_editorial,
    selected_topic_present,
)


def selected_topic(state: PipelineState) -> bool:
    if not state.daily_editorial.exists():
        return False
    text = state.daily_editorial.read_text(encoding="utf-8")
    return selected_topic_present(text)


def next_action(state: PipelineState, has_topic: bool) -> str:
    if state.daily_result == "NO_PUBLISH":
        if state.no_publish_confirmation == "CONFIRMED":
            return "None — editorial day completed without publication."
        return "Confirm the NO_PUBLISH editorial decision."
    if state.daily_result == "PUBLISHED":
        return "None — publication is already recorded."
    if state.world_brief_status == "MISSING":
        return "Generate or confirm today's World Brief."
    if not state.daily_editorial.exists():
        return "Create today's Daily Editorial workspace."
    if state.world_brief_status == "STALE":
        return "Confirm whether the latest World Brief may be used for today."
    if not has_topic:
        return "Complete Candidate Topics and Scorecard."
    if state.source_verification == "HOLD_C" or state.source_verification_signal == "HOLD_C":
        if state.fallback_attempts >= 1:
            return "Record and confirm NO_PUBLISH; the fallback limit is reached."
        return "Select the single allowed fallback candidate."
    if not state.article and state.source_verification == "NOT_STARTED":
        return "Start Source Verification for the selected topic."
    if state.article and (
        state.source_verification == "NOT_STARTED" or (
        state.source_verification == "UNRESOLVED"
        and state.source_verification_signal == "NOT_STARTED"
        )
    ):
        return "Start or resolve Source Verification."
    if state.source_verification_signal == "AMBIGUOUS":
        return "Resolve multiple Source Verification records."
    if not state.article and (
        state.source_verification in {"PASS_A", "PASS_B"}
        or state.source_verification_signal in {"PASS_A", "PASS_B"}
    ):
        return "Draft the article."
    if state.article and state.source_verification_link != "VERIFIED" and (
        state.source_verification in {"PASS_A", "PASS_B"}
        or state.source_verification_signal in {"PASS_A", "PASS_B"}
    ):
        return "Link the article to its Source Verification record."
    if state.editorial_review == "NEEDS_FIX":
        return "Apply only the required editorial fixes, then re-review."
    if state.editorial_review == "HOLD":
        return "Record and confirm NO_PUBLISH after Editorial Review C."
    if state.editorial_review in {"UNRESOLVED", "PENDING"}:
        return "Complete independent Editorial Review."
    if not insight_shift_gate_passed(state.insight_shift, state.insight_shift_review):
        if state.insight_shift_review == "INVALID":
            return "Resolve the invalid Insight Shift Review record."
        if state.insight_shift == "C":
            return "Revise Insight Shift before continuing."
        return "Review Insight Shift before publication."
    if state.take_one_thing == "NEEDS_WORK":
        return "Revise Take One Thing."
    if state.take_one_thing == "FAIL":
        return "Resolve the failed Take One Thing gate."
    if state.human_read != "COMPLETE":
        return "Complete the human meaning and reading-quality review."
    if state.build != "READY":
        return "Run: python3 scripts/build.py"
    if state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        return "Complete Safari / Chrome Local Preview."
    if state.technical_validation != "PASS":
        return "Complete Technical Validation."
    if state.git_diff_review != "COMPLETE":
        return "Complete Git Diff Review."
    if state.final_approval == "PENDING":
        return "Request Final Approval."
    if state.publish_readiness == "READY_TO_PUBLISH":
        return "Manual publish may proceed."
    return state.next_action


def remaining_gates(state: PipelineState) -> list[str]:
    if state.daily_result in {"NO_PUBLISH", "PUBLISHED"}:
        return [] if state.daily_result == "PUBLISHED" or state.no_publish_confirmation == "CONFIRMED" else ["NO_PUBLISH confirmation"]
    gates = []
    if state.source_verification_link != "VERIFIED":
        gates.append("Source Verification link")
    if state.editorial_review != "PASS":
        gates.append("Editorial Review")
    if not insight_shift_gate_passed(state.insight_shift, state.insight_shift_review):
        gates.append("Insight Shift")
    if state.take_one_thing != "PASS":
        gates.append("Take One Thing")
    if state.build != "READY":
        gates.append("Build")
    if state.human_read != "COMPLETE":
        gates.append("Human Read")
    if state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        gates.append("Local Preview")
    if state.technical_validation != "PASS":
        gates.append("Technical Validation")
    if state.git_diff_review != "COMPLETE":
        gates.append("Git Diff Review")
    if state.final_approval != "APPROVED":
        gates.append("Final Approval")
    return gates


def print_morning(state: PipelineState) -> None:
    topic = selected_topic(state)
    brief_label = state.world_brief_status
    print("World Insight Morning")
    print(f"\nDate: {state.today}")
    print(f"World Brief: {brief_label}")
    if state.world_brief:
        print(f"World Brief Path: {state.world_brief}")
    print(f"Daily Editorial: {'FOUND' if state.daily_editorial.exists() else 'MISSING'}")
    print(f"Selected Topic: {'FOUND' if topic else 'MISSING'}")
    print(f"Daily Result: {state.daily_result}")
    print(f"Fallback Attempts: {state.fallback_attempts}")
    print(f"Source Verification: {state.source_verification}")
    print(f"Article Draft: {'FOUND' if state.article else 'MISSING'}")
    print(f"Editorial Review: {state.editorial_review}")
    print(f"Review Decision: {state.review_decision}")
    print(f"Insight Shift: {state.insight_shift}")
    print(f"Insight Shift Review: {state.insight_shift_review}")
    print(f"Take One Thing: {state.take_one_thing}")
    print(f"Human Read: {state.human_read}")
    print(f"Technical Validation: {state.technical_validation}")
    build_label = state.build if state.build == "READY" else "NEEDED"
    print(f"Build: {build_label}")
    print(f"Publish Readiness: {state.publish_readiness}")
    print(f"\nNext Action:\n{next_action(state, topic)}")
    gates = remaining_gates(state)
    if gates:
        print("\nRemaining Gates: " + ", ".join(gates))
    if state.daily_result == "NO_PUBLISH" and state.no_publish_confirmation == "CONFIRMED":
        publish_label = "NO_PUBLISH"
    elif state.publish_readiness == "READY_TO_PUBLISH":
        publish_label = "READY"
    elif state.publish_readiness == "PUBLISHED":
        publish_label = "PUBLISHED"
    else:
        publish_label = "HOLD"
    print(f"\nPublish: {publish_label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="World Insight's daily editorial entry point.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Pipeline date (YYYY-MM-DD).")
    parser.add_argument("--prepare", action="store_true", help="Create a missing dated Daily Editorial from the blank template.")
    args = parser.parse_args()
    if args.prepare:
        prepare_daily_editorial(args.date)
    state = inspect(args.date, prepare=False)
    print_morning(state)


if __name__ == "__main__":
    main()
