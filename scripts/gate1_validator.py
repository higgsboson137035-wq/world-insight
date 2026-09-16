"""Deterministic structural validation for the Phase 1 Gate 1 package.

This module is intentionally standalone.  It does not read or write files,
invoke subprocesses, access the network, or make semantic judgments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any


REQUIRED_METADATA = (
    "Run-Date",
    "Run-Start",
    "Brief-Readiness",
    "Candidate-Count",
    "Daily-Candidate-Outcome",
    "Recommended-Candidate",
    "Source-Verification",
    "Gate-1-Follow-Up",
    "Human-Decision",
    "Prompt-Version",
    "Prompt-SHA256",
)
REQUIRED_SECTIONS = (
    "World Brief Confirmation",
    "Candidate List",
    "Candidate Comparison",
    "Recommended Candidate",
    "Candidate Light Evaluations",
    "Confirmed",
    "Claims",
    "Analysis",
    "Hypothetical",
    "Unknown",
    "Evidence Boundary",
    "Candidate Discovery Convergence Observation",
    "Measurement",
)
REQUIRED_CANDIDATE_FIELDS = (
    "Brief item",
    "Initial Question",
    "Reader Transformation BEFORE",
    "Reader Transformation AFTER",
    "Structural Question",
    "Insight Shift",
    "Take One Thing",
    "Human Context / Responsibility conflict",
    "Decision Space",
    "Evidence feasibility",
    "Overlap / Independence",
    "Provisional evaluation",
)
ALLOWED_OUTCOMES = {"NO_PUBLISH_CANDIDATE", "CANDIDATES_FOR_HUMAN_REVIEW"}
ALLOWED_FOLLOW_UPS = {"NONE", "SOURCE_VERIFICATION_REQUIRED"}
ALLOWED_RECOMMENDATIONS = {"NONE", "Candidate 1", "Candidate 2", "Candidate 3"}
METADATA_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):(?:\s*)(.*?)\s*$")
SECTION_PATTERN = re.compile(r"^## (.+)$")
CANDIDATE_HEADING_PATTERN = re.compile(r"^### Candidate (.+?)\s*$")
FIELD_PATTERN = re.compile(r"^\s*(?:-\s*)?(.+?):(?:\s*)(.*?)\s*$")


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    status: str
    failure_kind: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    extracted_metadata: dict[str, str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "status": self.status,
            "failure_kind": self.failure_kind,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "extracted_metadata": dict(self.extracted_metadata),
        }


def _result(
    *,
    valid: bool,
    failure_kind: str,
    errors: list[str],
    warnings: list[str],
    metadata: dict[str, str],
) -> ValidationResult:
    return ValidationResult(
        valid=valid,
        status="PASS" if valid else "FAIL",
        failure_kind=failure_kind,
        errors=tuple(errors),
        warnings=tuple(warnings),
        extracted_metadata=dict(metadata),
    )


def _metadata(lines: list[str], errors: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    counts: dict[str, int] = {}
    for line in lines:
        match = METADATA_PATTERN.fullmatch(line)
        if not match:
            continue
        key, value = match.groups()
        if key not in REQUIRED_METADATA:
            continue
        counts[key] = counts.get(key, 0) + 1
        if counts[key] == 1:
            values[key] = value
    for key in REQUIRED_METADATA:
        count = counts.get(key, 0)
        if count == 0:
            errors.append(f"MISSING_METADATA:{key}")
        elif count > 1:
            errors.append(f"DUPLICATE_METADATA:{key}")
        elif not values[key]:
            errors.append(f"EMPTY_METADATA:{key}")
    return values


def _section_ranges(lines: list[str]) -> dict[str, list[tuple[int, int]]]:
    headings = [(index, match.group(1)) for index, line in enumerate(lines) if (match := SECTION_PATTERN.fullmatch(line))]
    ranges: dict[str, list[tuple[int, int]]] = {}
    for position, (start, name) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        ranges.setdefault(name, []).append((start + 1, end))
    return ranges


def _check_sections(lines: list[str], errors: list[str]) -> dict[str, list[tuple[int, int]]]:
    ranges = _section_ranges(lines)
    for name in REQUIRED_SECTIONS:
        count = len(ranges.get(name, []))
        if count == 0:
            errors.append(f"MISSING_SECTION:{name}")
        elif count > 1:
            errors.append(f"DUPLICATE_SECTION:{name}")
    return ranges


def _check_candidates(
    lines: list[str],
    ranges: dict[str, list[tuple[int, int]]],
    count: int | None,
    errors: list[str],
) -> set[int]:
    candidate_ranges = ranges.get("Candidate List", [])
    if len(candidate_ranges) != 1 or count is None:
        return set()
    start, end = candidate_ranges[0]
    headings: list[tuple[int, int | None]] = []
    for index, line in enumerate(lines):
        match = CANDIDATE_HEADING_PATTERN.fullmatch(line)
        if match:
            number_text = match.group(1)
            number = int(number_text) if number_text.isdigit() else None
            if not (start <= index < end):
                errors.append("CANDIDATE_BLOCK_OUTSIDE_LIST")
            headings.append((index, number))
    in_list = [(index, number) for index, number in headings if start <= index < end]
    if count == 0 and in_list:
        errors.append("CANDIDATE_BLOCK_COUNT_MISMATCH")
    if count > 0 and len(in_list) != count:
        errors.append("CANDIDATE_BLOCK_COUNT_MISMATCH")
    numbers = [number for _, number in in_list]
    if any(number is None or number < 1 or number > 3 for number in numbers):
        errors.append("INVALID_CANDIDATE_BLOCK_NUMBER")
    if len(numbers) != len(set(numbers)):
        errors.append("DUPLICATE_CANDIDATE_BLOCK")
    if numbers != list(range(1, count + 1)):
        if count == 0 or in_list:
            errors.append("CANDIDATE_BLOCK_NUMBERING_MISMATCH")

    present: set[int] = set()
    for position, (index, number) in enumerate(in_list):
        if number is None:
            continue
        present.add(number)
        block_end = in_list[position + 1][0] if position + 1 < len(in_list) else end
        field_counts: dict[str, int] = {}
        field_values: dict[str, str] = {}
        for line in lines[index + 1 : block_end]:
            match = FIELD_PATTERN.fullmatch(line)
            if not match:
                continue
            label, value = match.groups()
            if label not in REQUIRED_CANDIDATE_FIELDS:
                continue
            field_counts[label] = field_counts.get(label, 0) + 1
            field_values[label] = value
        for field in REQUIRED_CANDIDATE_FIELDS:
            field_count = field_counts.get(field, 0)
            if field_count == 0:
                errors.append(f"MISSING_CANDIDATE_FIELD:Candidate {number}:{field}")
            elif field_count > 1:
                errors.append(f"DUPLICATE_CANDIDATE_FIELD:Candidate {number}:{field}")
            elif not field_values[field]:
                errors.append(f"EMPTY_CANDIDATE_FIELD:Candidate {number}:{field}")
    return present


def _check_metadata(
    metadata: dict[str, str],
    *,
    requested_date: str,
    prompt_version: str,
    prompt_sha256: str,
    brief_readiness: str,
    errors: list[str],
) -> int | None:
    if metadata.get("Run-Date") != requested_date:
        errors.append("RUN_DATE_MISMATCH")
    try:
        datetime.fromisoformat(metadata.get("Run-Start", ""))
    except ValueError:
        errors.append("INVALID_RUN_START")
    if metadata.get("Brief-Readiness") != "READY":
        errors.append("INVALID_BRIEF_READINESS")
    if metadata.get("Brief-Readiness") != brief_readiness:
        errors.append("BRIEF_READINESS_MISMATCH")
    if metadata.get("Source-Verification") != "NOT_STARTED":
        errors.append("INVALID_SOURCE_VERIFICATION")
    if metadata.get("Human-Decision") != "PENDING":
        errors.append("INVALID_HUMAN_DECISION")
    if metadata.get("Prompt-Version") != prompt_version:
        errors.append("PROMPT_VERSION_MISMATCH")
    if metadata.get("Prompt-SHA256") != prompt_sha256:
        errors.append("PROMPT_SHA256_MISMATCH")
    outcome = metadata.get("Daily-Candidate-Outcome")
    if outcome not in ALLOWED_OUTCOMES:
        errors.append("INVALID_DAILY_CANDIDATE_OUTCOME")
    recommendation = metadata.get("Recommended-Candidate")
    if recommendation not in ALLOWED_RECOMMENDATIONS:
        errors.append("INVALID_RECOMMENDED_CANDIDATE")
    follow_up = metadata.get("Gate-1-Follow-Up")
    if follow_up not in ALLOWED_FOLLOW_UPS:
        errors.append("INVALID_GATE1_FOLLOW_UP")
    count_text = metadata.get("Candidate-Count", "")
    if not re.fullmatch(r"[0-3]", count_text):
        errors.append("INVALID_CANDIDATE_COUNT")
        return None
    return int(count_text)


def _check_outcome(metadata: dict[str, str], count: int | None, present: set[int], errors: list[str]) -> None:
    if count is None:
        return
    outcome = metadata.get("Daily-Candidate-Outcome")
    recommendation = metadata.get("Recommended-Candidate")
    follow_up = metadata.get("Gate-1-Follow-Up")
    if count == 0:
        if outcome != "NO_PUBLISH_CANDIDATE":
            errors.append("ZERO_CANDIDATE_OUTCOME_MISMATCH")
        if recommendation != "NONE":
            errors.append("ZERO_CANDIDATE_RECOMMENDATION_MISMATCH")
        if follow_up != "NONE":
            errors.append("ZERO_CANDIDATE_FOLLOW_UP_MISMATCH")
    else:
        if outcome != "CANDIDATES_FOR_HUMAN_REVIEW":
            errors.append("POSITIVE_CANDIDATE_OUTCOME_MISMATCH")
        if follow_up != "SOURCE_VERIFICATION_REQUIRED":
            errors.append("POSITIVE_CANDIDATE_FOLLOW_UP_MISMATCH")
        if recommendation not in {f"Candidate {number}" for number in present}:
            errors.append("RECOMMENDED_CANDIDATE_NOT_PRESENT")


def _check_measurement(ranges: dict[str, list[tuple[int, int]]], lines: list[str], errors: list[str]) -> None:
    measurement_ranges = ranges.get("Measurement", [])
    if len(measurement_ranges) != 1:
        return
    start, end = measurement_ranges[0]
    fields: dict[str, list[str]] = {}
    for line in lines[start:end]:
        match = FIELD_PATTERN.fullmatch(line)
        if match:
            fields.setdefault(match.group(1), []).append(match.group(2))
    if len(fields.get("Machine elapsed", [])) != 1 or not fields["Machine elapsed"][0]:
        errors.append("INVALID_MACHINE_ELAPSED")
    if fields.get("Human active time") != ["UNKNOWN"]:
        errors.append("INVALID_HUMAN_ACTIVE_TIME")
    if fields.get("Rework count") != ["0"]:
        errors.append("INVALID_REWORK_COUNT")


def validate_gate1_output(
    raw_output: str,
    *,
    requested_date: str,
    prompt_version: str,
    prompt_sha256: str,
    brief_readiness: str = "READY",
) -> ValidationResult:
    """Validate Gate 1 structure without interpreting its substantive content."""

    try:
        if not isinstance(raw_output, str) or not raw_output.strip():
            return _result(
                valid=False,
                failure_kind="MALFORMED_GATE1",
                errors=["EMPTY_RAW_OUTPUT"],
                warnings=[],
                metadata={},
            )
        lines = raw_output.splitlines()
        errors: list[str] = []
        metadata = _metadata(lines, errors)
        ranges = _check_sections(lines, errors)
        count = _check_metadata(
            metadata,
            requested_date=requested_date,
            prompt_version=prompt_version,
            prompt_sha256=prompt_sha256,
            brief_readiness=brief_readiness,
            errors=errors,
        )
        present = _check_candidates(lines, ranges, count, errors)
        _check_outcome(metadata, count, present, errors)
        _check_measurement(ranges, lines, errors)
        if "NO_PUBLISH / HUMAN APPROVED" in raw_output:
            errors.append("FORBIDDEN_HUMAN_APPROVED_NO_PUBLISH")
        return _result(
            valid=not errors,
            failure_kind="NONE" if not errors else "MALFORMED_GATE1",
            errors=errors,
            warnings=[],
            metadata=metadata,
        )
    except Exception:
        return ValidationResult(
            valid=False,
            status="ERROR",
            failure_kind="VALIDATOR_ERROR",
            errors=("VALIDATOR_ERROR",),
            warnings=(),
            extracted_metadata={},
        )
