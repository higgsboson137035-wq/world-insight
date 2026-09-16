"""Phase 1 orchestration skeleton.

This module connects readiness, runtime locking, Codex transport, and the
standalone Gate 1 structural validator. It has no later-stage operations.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from scripts.brief_readiness import DEFAULT_BRIEF_ROOT, check_brief
from scripts.codex_runner import DEFAULT_CODEX_EXECUTABLE, CodexResult, run_codex
from scripts.gate1_validator import validate_gate1_output
from scripts.runtime_state import (
    SCHEMA_VERSION,
    acquire_lock,
    atomic_write_json,
    run_directory,
    write_status,
)


PROMPT_HASH_PLACEHOLDER = "INJECTED_BY_ORCHESTRATOR"
DEFAULT_RUNTIME_ROOT = Path.home() / "Library" / "Application Support" / "WorldInsightDaily"
DEFAULT_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "daily_run_phase1.md"


@dataclass(frozen=True)
class OrchestratorResult:
    execution_status: str
    run_id: str
    requested_date: str
    brief_status: str
    codex_status: str
    output_state: str
    human_review_required: bool
    error_reason: str | None
    run_directory: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "execution_status": self.execution_status,
            "run_id": self.run_id,
            "requested_date": self.requested_date,
            "brief_status": self.brief_status,
            "codex_status": self.codex_status,
            "output_state": self.output_state,
            "human_review_required": self.human_review_required,
            "error_reason": self.error_reason,
            "run_directory": self.run_directory,
        }


def _new_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"run-{timestamp}-{uuid.uuid4().hex[:12]}"


def _result(
    *,
    execution_status: str,
    run_id: str,
    requested_date: str,
    brief_status: str,
    codex_status: str,
    output_state: str = "NONE",
    human_review_required: bool = True,
    error_reason: str | None = None,
    run_path: Path | None = None,
) -> OrchestratorResult:
    return OrchestratorResult(
        execution_status=execution_status,
        run_id=run_id,
        requested_date=requested_date,
        brief_status=brief_status,
        codex_status=codex_status,
        output_state=output_state,
        human_review_required=human_review_required,
        error_reason=error_reason,
        run_directory=str(run_path) if run_path else None,
    )


def _write_text_atomically_once(path: Path, content: str) -> None:
    """Create a private text artifact without replacing an existing artifact.

    The completed temporary file is published with an exclusive hard-link
    creation.  Unlike ``os.replace``, the destination can never be replaced
    if it appears after the initial existence check.
    """

    temporary_path: Path | None = None
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, 0o600)
        os.link(temporary_path, path, follow_symlinks=False)
        temporary_path.unlink()
    except BaseException:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
        raise


def _status_record(
    result: OrchestratorResult,
    *,
    prompt_version: str | None = None,
    prompt_sha256: str | None = None,
) -> dict[str, Any]:
    record = result.as_dict()
    record["status"] = result.execution_status
    record["schema_version"] = SCHEMA_VERSION
    if prompt_version is not None:
        record["prompt_version"] = prompt_version
    if prompt_sha256 is not None:
        record["prompt_sha256"] = prompt_sha256
    return record


def _read_prompt(prompt_path: Path) -> tuple[str, str, str]:
    if not prompt_path.is_file():
        raise ValueError("PROMPT_NOT_FOUND")
    try:
        raw = prompt_path.read_bytes()
        prompt_text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("PROMPT_INVALID_UTF8") from exc
    except OSError as exc:
        raise ValueError("PROMPT_READ_ERROR") from exc
    if not raw or not prompt_text.strip():
        raise ValueError("PROMPT_EMPTY")
    count = prompt_text.count(PROMPT_HASH_PLACEHOLDER)
    if count == 0:
        raise ValueError("PROMPT_HASH_PLACEHOLDER_MISSING")
    if count != 1:
        raise ValueError("PROMPT_HASH_PLACEHOLDER_DUPLICATE")
    prompt_sha256 = hashlib.sha256(raw).hexdigest()
    prompt_version = next(
        (
            line.split(":", 1)[1].strip()
            for line in prompt_text.splitlines()
            if line.startswith("Prompt-Version:")
        ),
        "UNKNOWN",
    )
    return prompt_text.replace(PROMPT_HASH_PLACEHOLDER, prompt_sha256), prompt_version, prompt_sha256


def _persist_status(run_path: Path, result: OrchestratorResult, **metadata: str) -> None:
    write_status(run_path / "status.json", _status_record(result, **metadata))


def run_phase1(
    requested_date: str,
    *,
    brief_root: Path = DEFAULT_BRIEF_ROOT,
    runtime_root: Path = DEFAULT_RUNTIME_ROOT,
    prompt_path: Path = DEFAULT_PROMPT_PATH,
    executable: str | Path = DEFAULT_CODEX_EXECUTABLE,
    working_directory: Path | str,
    model: str,
    timeout_seconds: float,
    run_id: str | None = None,
    brief_checker: Callable[..., Mapping[str, Any]] = check_brief,
    lock_acquirer: Callable[..., Any] = acquire_lock,
    codex_runner: Callable[..., CodexResult] = run_codex,
    gate1_validator: Callable[..., Any] = validate_gate1_output,
    human_approved_rerun: bool = False,
) -> OrchestratorResult:
    """Run only through transport output, then stop for Human/Gate 1 review."""

    selected_run_id = run_id or _new_run_id()
    started = time.monotonic()

    try:
        brief_result = dict(brief_checker(requested_date, brief_root))
        brief_status = str(brief_result.get("status", "ERROR"))
        brief_ready = brief_result.get("ready") is True and brief_status == "READY"
    except Exception:
        return _result(
            execution_status="ERROR",
            run_id=selected_run_id,
            requested_date=requested_date,
            brief_status="ERROR",
            codex_status="NOT_STARTED",
            error_reason="BRIEF_CHECKER_ERROR",
        )

    try:
        lock_result, lock = lock_acquirer(
            runtime_root,
            requested_date,
            selected_run_id,
            allow_terminal_result=human_approved_rerun,
        )
    except Exception:
        return _result(
            execution_status="ERROR",
            run_id=selected_run_id,
            requested_date=requested_date,
            brief_status=brief_status,
            codex_status="NOT_STARTED",
            error_reason="LOCK_ERROR",
        )
    if not lock_result.acquired or lock is None:
        return _result(
            execution_status=lock_result.status,
            run_id=selected_run_id,
            requested_date=requested_date,
            brief_status=brief_status,
            codex_status="NOT_STARTED",
            error_reason=lock_result.reason,
        )

    run_path: Path | None = None
    result: OrchestratorResult | None = None
    release_error: str | None = None
    try:
        run_path = run_directory(runtime_root, requested_date, selected_run_id)
        if not brief_ready:
            result = _result(
                execution_status="BRIEF_NOT_READY" if brief_status == "BRIEF_NOT_READY" else "ERROR",
                run_id=selected_run_id,
                requested_date=requested_date,
                brief_status=brief_status,
                codex_status="NOT_STARTED",
                error_reason="BRIEF_NOT_READY" if brief_status == "BRIEF_NOT_READY" else "BRIEF_CHECK_FAILED",
                run_path=run_path,
            )
            _persist_status(run_path, result)
        else:
            result = _result(
                execution_status="RUNNING",
                run_id=selected_run_id,
                requested_date=requested_date,
                brief_status=brief_status,
                codex_status="NOT_STARTED",
                error_reason=None,
                run_path=run_path,
            )
            _persist_status(run_path, result)

            try:
                prompt, prompt_version, prompt_sha256 = _read_prompt(prompt_path)
            except ValueError as exc:
                result = _result(
                    execution_status="ERROR",
                    run_id=selected_run_id,
                    requested_date=requested_date,
                    brief_status=brief_status,
                    codex_status="NOT_STARTED",
                    error_reason=str(exc),
                    run_path=run_path,
                )
                _persist_status(run_path, result)
            else:
                transport = codex_runner(
                    prompt,
                    executable=executable,
                    working_directory=working_directory,
                    model=model,
                    timeout_seconds=timeout_seconds,
                )
                atomic_write_json(run_path / "codex_result.json", transport.as_dict())

                if transport.status != "SUCCESS":
                    result = _result(
                        execution_status="ERROR",
                        run_id=selected_run_id,
                        requested_date=requested_date,
                        brief_status=brief_status,
                        codex_status=transport.status,
                        error_reason=transport.status,
                        run_path=run_path,
                    )
                    _persist_status(run_path, result, prompt_version=prompt_version, prompt_sha256=prompt_sha256)
                else:
                    _write_text_atomically_once(run_path / "raw-output.txt", transport.stdout)
                    try:
                        validation = gate1_validator(
                            transport.stdout,
                            requested_date=requested_date,
                            prompt_version=prompt_version,
                            prompt_sha256=prompt_sha256,
                            brief_readiness=brief_status,
                        )
                        validation_payload = validation.as_dict()
                    except Exception:
                        result = _result(
                            execution_status="ERROR",
                            run_id=selected_run_id,
                            requested_date=requested_date,
                            brief_status=brief_status,
                            codex_status=transport.status,
                            error_reason="VALIDATOR_ERROR",
                            run_path=run_path,
                        )
                        _persist_status(run_path, result, prompt_version=prompt_version, prompt_sha256=prompt_sha256)
                    else:
                        atomic_write_json(run_path / "validation_result.json", validation_payload)
                        is_pass = (
                            validation_payload.get("valid") is True
                            and validation_payload.get("status") == "PASS"
                            and validation_payload.get("failure_kind") == "NONE"
                        )
                        failure_kind = validation_payload.get("failure_kind")
                        is_known_failure = (
                            validation_payload.get("valid") is False
                            and validation_payload.get("status") == "FAIL"
                            and failure_kind in {"MALFORMED_GATE1", "BOUNDARY_VIOLATION"}
                        )
                        is_validator_error = (
                            validation_payload.get("valid") is False
                            and validation_payload.get("status") == "ERROR"
                            and failure_kind == "VALIDATOR_ERROR"
                        )
                        if is_pass:
                            _write_text_atomically_once(run_path / "gate1.md", transport.stdout)
                            result = _result(
                                execution_status="GATE1_READY",
                                run_id=selected_run_id,
                                requested_date=requested_date,
                                brief_status=brief_status,
                                codex_status=transport.status,
                                output_state="VALIDATED_GATE1_OUTPUT",
                                error_reason=None,
                                run_path=run_path,
                            )
                        elif is_known_failure:
                            result = _result(
                                execution_status=failure_kind,
                                run_id=selected_run_id,
                                requested_date=requested_date,
                                brief_status=brief_status,
                                codex_status=transport.status,
                                error_reason=failure_kind,
                                run_path=run_path,
                            )
                        elif is_validator_error:
                            result = _result(
                                execution_status="ERROR",
                                run_id=selected_run_id,
                                requested_date=requested_date,
                                brief_status=brief_status,
                                codex_status=transport.status,
                                error_reason="VALIDATOR_ERROR",
                                run_path=run_path,
                            )
                        else:
                            result = _result(
                                execution_status="ERROR",
                                run_id=selected_run_id,
                                requested_date=requested_date,
                                brief_status=brief_status,
                                codex_status=transport.status,
                                error_reason="VALIDATOR_ERROR",
                                run_path=run_path,
                            )
                        _persist_status(run_path, result, prompt_version=prompt_version, prompt_sha256=prompt_sha256)
    except Exception:
        result = _result(
            execution_status="ERROR",
            run_id=selected_run_id,
            requested_date=requested_date,
            brief_status=brief_status,
            codex_status=(getattr(result, "codex_status", "NOT_STARTED") if result else "NOT_STARTED"),
            error_reason="RUNTIME_WRITE_FAILED",
            run_path=run_path,
        )
        if run_path is not None:
            try:
                _persist_status(run_path, result)
            except Exception:
                pass
    finally:
        try:
            lock.release()
        except Exception:
            release_error = "LOCK_RELEASE_FAILED"
        if release_error is not None:
            result = _result(
                execution_status="ERROR",
                run_id=selected_run_id,
                requested_date=requested_date,
                brief_status=brief_status,
                codex_status=(getattr(result, "codex_status", "NOT_STARTED") if result else "NOT_STARTED"),
                output_state=(getattr(result, "output_state", "NONE") if result else "NONE"),
                error_reason=release_error,
                run_path=run_path,
            )
            if run_path is not None:
                try:
                    _persist_status(run_path, result)
                except Exception:
                    pass
    return result
