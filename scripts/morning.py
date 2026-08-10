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
    prepare_daily_editorial,
    selected_topic_present,
)


def selected_topic(state: PipelineState) -> bool:
    if not state.daily_editorial.exists():
        return False
    text = state.daily_editorial.read_text(encoding="utf-8")
    return selected_topic_present(text)


def next_action(state: PipelineState, has_topic: bool) -> str:
    if state.world_brief_status == "MISSING":
        return "Generate or confirm today's World Brief."
    if not state.daily_editorial.exists():
        return "Create today's Daily Editorial workspace."
    if state.world_brief_status == "STALE":
        return "Confirm whether the latest World Brief may be used for today."
    if not has_topic:
        return "Complete Candidate Topics and Scorecard."
    if state.source_verification == "HOLD_C" or state.source_verification_signal == "HOLD_C":
        return "Select a fallback candidate."
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
    if state.editorial_review in {"UNRESOLVED", "PENDING"}:
        return "Complete independent Editorial Review."
    if state.insight_shift in {"B", "NEEDS_HUMAN_REVIEW"}:
        return "Review Insight Shift before publication."
    if state.insight_shift == "C":
        return "Revise Insight Shift before continuing."
    if state.take_one_thing == "NEEDS_WORK":
        return "Revise Take One Thing."
    if state.take_one_thing == "FAIL":
        return "Resolve the failed Take One Thing gate."
    if state.build != "READY":
        return "Run: python3 scripts/build.py"
    if state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        return "Complete Safari / Chrome Local Preview."
    if state.git_diff_review != "COMPLETE":
        return "Complete Git Diff Review."
    if state.final_approval == "PENDING":
        return "Request Final Approval."
    if state.publish_readiness == "READY_TO_PUBLISH":
        return "Manual publish may proceed."
    return state.next_action


def remaining_gates(state: PipelineState) -> list[str]:
    gates = []
    if state.source_verification_link != "VERIFIED":
        gates.append("Source Verification link")
    if state.editorial_review != "COMPLETE":
        gates.append("Editorial Review")
    if state.insight_shift not in {"A"}:
        gates.append("Insight Shift")
    if state.take_one_thing != "PASS":
        gates.append("Take One Thing")
    if state.build != "READY":
        gates.append("Build")
    if state.local_preview != "COMPLETE" or state.safari != "PASS" or state.chrome != "PASS":
        gates.append("Local Preview")
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
    print(f"Source Verification: {state.source_verification}")
    print(f"Article Draft: {'FOUND' if state.article else 'MISSING'}")
    print(f"Editorial Review: {state.editorial_review}")
    print(f"Insight Shift: {state.insight_shift}")
    print(f"Take One Thing: {state.take_one_thing}")
    build_label = state.build if state.build == "READY" else "NEEDED"
    print(f"Build: {build_label}")
    print(f"Publish Readiness: {state.publish_readiness}")
    print(f"\nNext Action:\n{next_action(state, topic)}")
    gates = remaining_gates(state)
    if gates:
        print("\nRemaining Gates: " + ", ".join(gates))
    print("\nPublish: HOLD" if state.publish_readiness in {"BLOCKED", "NEEDS_REVIEW", "NEEDS_PREVIEW", "NEEDS_GIT_REVIEW", "WAITING_FOR_APPROVAL"} else "\nPublish: MANUAL APPROVAL REQUIRED")


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
