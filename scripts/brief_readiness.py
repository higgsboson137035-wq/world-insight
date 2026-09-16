#!/usr/bin/env python3
"""Read-only readiness checks for the dated World Brief input.

The requested date is interpreted in Asia/Tokyo.  When omitted from the CLI,
the current date is obtained in Asia/Tokyo; the core ``check_brief`` function
always receives an explicit requested date.  This module only reads the Brief
file and never invokes the World Brief generator or inspects its logs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


JST = ZoneInfo("Asia/Tokyo")
DEFAULT_BRIEF_ROOT = Path.home() / "Workspace" / "world-brief"
REQUIRED_HEADINGS = (
    "## Executive Summary",
    "## Why It Matters",
    "## Big Picture",
    "## Tomorrow's Watchlist",
)
SHOULD_HEADINGS = (
    "## 🌍 世界情勢",
    "## 💹 経済",
    "## 🤖 AI・テクノロジー",
    "## 🔬 科学",
    "## 🇯🇵 日本への影響",
)
GENERATED_MARKER = "*Generated automatically by World Brief.*"
DATE_PATTERN = re.compile(r"^_Date:\s*(\d{4}-\d{2}-\d{2})_\s*$")
TOP3_HEADING_PATTERN = re.compile(r"^## Today's Top 3\s*$")
SECTION_HEADING_PATTERN = re.compile(r"^##\s+")
TOP3_ITEM_PATTERN = re.compile(r"^\s*([123])\.\s+\S")


class BriefReadinessError(ValueError):
    """Raised when the requested date cannot be interpreted safely."""


def local_today() -> date:
    """Return today's date in the Phase 1 Japan-timezone assumption."""

    return datetime.now(JST).date()


def parse_requested_date(value: str) -> date:
    """Parse an exact ISO calendar date for deterministic validation."""

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise BriefReadinessError("INVALID_REQUESTED_DATE")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise BriefReadinessError("INVALID_REQUESTED_DATE") from exc


def brief_path(brief_root: Path, requested: date) -> Path:
    """Return only the Brief path for the requested date."""

    return brief_root / "briefs" / f"{requested.isoformat()}.md"


def _section_body(text: str, heading_pattern: re.Pattern[str]) -> str | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if heading_pattern.fullmatch(line):
            body: list[str] = []
            for following in lines[index + 1 :]:
                if SECTION_HEADING_PATTERN.match(following):
                    break
                body.append(following)
            return "\n".join(body)
    return None


def _check_top3(text: str) -> bool:
    body = _section_body(text, TOP3_HEADING_PATTERN)
    if body is None:
        return False
    numbered_items = [
        int(match.group(1))
        for line in body.splitlines()
        if (match := TOP3_ITEM_PATTERN.match(line))
    ]
    return numbered_items == [1, 2, 3]


def _mtime_is_requested_date(path: Path, requested: date) -> bool:
    return datetime.fromtimestamp(path.stat().st_mtime, JST).date() == requested


def _base_checks() -> dict[str, bool]:
    return {
        "file_exists": False,
        "filename_date_matches": False,
        "internal_date_matches": False,
        "non_empty": False,
        "top3_heading_exists": False,
        "top3_items_complete": False,
        "required_headings_exist": False,
        "generated_marker_exists": False,
        "mtime_matches_requested_date": False,
    }


def _result(
    *,
    ready: bool,
    status: str,
    requested: date,
    path: Path,
    warnings: list[str],
    errors: list[str],
    checks: dict[str, bool],
) -> dict[str, Any]:
    return {
        "ready": ready,
        "status": status,
        "requested_date": requested.isoformat(),
        "brief_path": str(path),
        "warnings": warnings,
        "errors": errors,
        "checks": checks,
    }


def check_brief(requested_date: str, brief_root: Path = DEFAULT_BRIEF_ROOT) -> dict[str, Any]:
    """Check the requested dated Brief without modifying any filesystem data."""

    requested = parse_requested_date(requested_date)
    path = brief_path(brief_root, requested)
    checks = _base_checks()
    errors: list[str] = []
    warnings: list[str] = []

    checks["file_exists"] = path.is_file()
    checks["filename_date_matches"] = path.name == f"{requested.isoformat()}.md"
    if not checks["file_exists"]:
        errors.append("MISSING_BRIEF")
        return _result(
            ready=False,
            status="BRIEF_NOT_READY",
            requested=requested,
            path=path,
            warnings=warnings,
            errors=errors,
            checks=checks,
        )

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append("BRIEF_READ_ERROR")
        return _result(
            ready=False,
            status="ERROR",
            requested=requested,
            path=path,
            warnings=warnings,
            errors=errors,
            checks=checks,
        )

    stripped = text.strip()
    checks["non_empty"] = bool(stripped)

    internal_date = next(
        (match.group(1) for line in text.splitlines() if (match := DATE_PATTERN.fullmatch(line))),
        None,
    )
    checks["internal_date_matches"] = internal_date == requested.isoformat()
    checks["top3_heading_exists"] = _section_body(text, TOP3_HEADING_PATTERN) is not None
    checks["top3_items_complete"] = _check_top3(text)
    checks["required_headings_exist"] = all(heading in text.splitlines() for heading in REQUIRED_HEADINGS)
    checks["generated_marker_exists"] = GENERATED_MARKER in text
    try:
        checks["mtime_matches_requested_date"] = _mtime_is_requested_date(path, requested)
    except OSError:
        errors.append("BRIEF_STAT_ERROR")

    for heading in SHOULD_HEADINGS:
        if heading not in text.splitlines():
            warnings.append(f"MISSING_SHOULD_HEADING:{heading}")
    watchlist = _section_body(text, re.compile(r"^## Tomorrow's Watchlist\s*$"))
    if watchlist is not None and not any(line.lstrip().startswith("-") for line in watchlist.splitlines()):
        warnings.append("WATCHLIST_HAS_NO_BULLET")

    must_checks = (
        "file_exists",
        "filename_date_matches",
        "internal_date_matches",
        "non_empty",
        "top3_heading_exists",
        "top3_items_complete",
        "required_headings_exist",
        "generated_marker_exists",
        "mtime_matches_requested_date",
    )
    for check_name in must_checks:
        if not checks[check_name]:
            errors.append(f"MUST_FAILED:{check_name}")

    ready = not errors
    return _result(
        ready=ready,
        status="READY" if ready else "BRIEF_NOT_READY",
        requested=requested,
        path=path,
        warnings=warnings,
        errors=errors,
        checks=checks,
    )


def exit_code(result: dict[str, Any]) -> int:
    """Return the stable CLI contract: 0 ready, 1 not ready, 2 checker error."""

    if result["status"] == "READY":
        return 0
    if result["status"] == "BRIEF_NOT_READY":
        return 1
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check dated World Brief readiness (read-only).")
    parser.add_argument("--date", default=local_today().isoformat(), help="Requested date (YYYY-MM-DD).")
    parser.add_argument("--brief-root", type=Path, default=DEFAULT_BRIEF_ROOT, help="World Brief repository root.")
    args = parser.parse_args(argv)

    try:
        result = check_brief(args.date, args.brief_root)
    except BriefReadinessError as exc:
        result = {
            "ready": False,
            "status": "ERROR",
            "requested_date": args.date,
            "brief_path": None,
            "warnings": [],
            "errors": [str(exc)],
            "checks": {},
        }
    except (OSError, ValueError) as exc:
        result = {
            "ready": False,
            "status": "ERROR",
            "requested_date": args.date,
            "brief_path": str(args.brief_root),
            "warnings": [],
            "errors": ["CHECKER_RUNTIME_ERROR"],
            "checks": {},
        }

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return exit_code(result)


if __name__ == "__main__":
    sys.exit(main())
