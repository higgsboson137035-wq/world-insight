#!/usr/bin/env python3
"""Thin Phase 1 Manual Runner entry point.

This module owns only the Human-facing presentation step after Phase 1.  The
orchestrator remains responsible for readiness, execution, validation, and
runtime artifact persistence.  No later editorial workflow is invoked here.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, TextIO

# Make direct execution (`python3 scripts/manual_runner.py`) resolve the
# repository's `scripts` package in the same way as module execution.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.brief_readiness import DEFAULT_BRIEF_ROOT, local_today
from scripts.daily_orchestrator import (
    DEFAULT_CODEX_EXECUTABLE,
    DEFAULT_PROMPT_PATH,
    DEFAULT_RUNTIME_ROOT,
    OrchestratorResult,
    run_phase1,
)


class ManualRunnerError(RuntimeError):
    """Raised when the validated Gate 1 artifact cannot be presented safely."""


def _gate1_text(result: OrchestratorResult) -> str:
    """Read only the validated Gate 1 artifact, failing closed otherwise."""

    if result.execution_status != "GATE1_READY":
        raise ManualRunnerError(
            f"execution_status is {result.execution_status!r}; expected 'GATE1_READY'"
        )
    if not result.run_directory:
        raise ManualRunnerError("run_directory is unavailable")

    artifact = Path(result.run_directory) / "gate1.md"
    if not artifact.is_file():
        raise ManualRunnerError(f"gate1.md is missing: {artifact}")
    try:
        return artifact.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ManualRunnerError(f"gate1.md is not valid UTF-8: {artifact}") from exc
    except OSError as exc:
        raise ManualRunnerError(f"gate1.md could not be read: {artifact}") from exc


def run_and_display(
    requested_date: str,
    *,
    brief_root: Path = DEFAULT_BRIEF_ROOT,
    runtime_root: Path = DEFAULT_RUNTIME_ROOT,
    prompt_path: Path = DEFAULT_PROMPT_PATH,
    executable: str | Path = DEFAULT_CODEX_EXECUTABLE,
    working_directory: Path | str = ROOT,
    model: str | None = None,
    timeout_seconds: float = 900,
    human_approved_rerun: bool = False,
    phase1_runner: Callable[..., OrchestratorResult] = run_phase1,
    output: TextIO | None = None,
) -> int:
    """Run Phase 1 once, display validated ``gate1.md``, and stop."""

    result = phase1_runner(
        requested_date,
        brief_root=brief_root,
        runtime_root=runtime_root,
        prompt_path=prompt_path,
        executable=executable,
        working_directory=working_directory,
        model=model,
        timeout_seconds=timeout_seconds,
        human_approved_rerun=human_approved_rerun,
    )
    gate1_text = _gate1_text(result)
    (output or sys.stdout).write(gate1_text)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run World Insight Phase 1 once and display the validated Gate 1 package."
    )
    parser.add_argument("--date", default=local_today().isoformat(), help="Run date (YYYY-MM-DD).")
    parser.add_argument("--brief-root", type=Path, default=DEFAULT_BRIEF_ROOT)
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME_ROOT)
    parser.add_argument("--prompt-path", type=Path, default=DEFAULT_PROMPT_PATH)
    parser.add_argument("--executable", default=DEFAULT_CODEX_EXECUTABLE)
    parser.add_argument("--working-directory", type=Path, default=ROOT)
    parser.add_argument("--model", default=None)
    parser.add_argument("--timeout-seconds", type=float, default=900)
    parser.add_argument(
        "--human-approved-rerun",
        action="store_true",
        help="Allow a new run after a prior terminal result; requires explicit human approval.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        return run_and_display(
            args.date,
            brief_root=args.brief_root,
            runtime_root=args.runtime_root,
            prompt_path=args.prompt_path,
            executable=args.executable,
            working_directory=args.working_directory,
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            human_approved_rerun=args.human_approved_rerun,
        )
    except ManualRunnerError as exc:
        print(f"manual_runner: ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"manual_runner: ERROR: Phase 1 runner failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
