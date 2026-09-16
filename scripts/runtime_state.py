#!/usr/bin/env python3
"""Repository-independent runtime state and same-day run locking.

This module does not invoke Codex, inspect Git, touch the World Brief
repository, or know anything about later editorial stages.  A caller supplies
the runtime root, which keeps tests isolated and avoids creating the real
runtime directory at import time.
"""

from __future__ import annotations

import json
import os
import socket
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "phase1-0.1"
EXECUTION_STATUSES = frozenset(
    {
        "NOT_RUN",
        "CHECKING_BRIEF",
        "RUNNING",
        "GATE1_READY",
        "BRIEF_NOT_READY",
        "ERROR",
        "MALFORMED_GATE1",
        "BOUNDARY_VIOLATION",
        "DUPLICATE_SUPPRESSED",
    }
)
TERMINAL_STATUSES = frozenset(
    {
        "GATE1_READY",
        "BRIEF_NOT_READY",
        "ERROR",
        "MALFORMED_GATE1",
        "BOUNDARY_VIOLATION",
        "DUPLICATE_SUPPRESSED",
    }
)
FORBIDDEN_EXECUTION_STATUS = "NO_PUBLISH_CANDIDATE"


class RuntimeStateError(ValueError):
    """Raised when runtime state is malformed or uses an unsupported status."""


def _ensure_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise RuntimeStateError("INVALID_RUN_DATE") from exc
    if parsed.isoformat() != value:
        raise RuntimeStateError("INVALID_RUN_DATE")
    return parsed


def _ensure_run_id(run_id: str) -> str:
    if not run_id or run_id in {".", ".."} or "/" in run_id or "\\" in run_id:
        raise RuntimeStateError("INVALID_RUN_ID")
    return run_id


def _ensure_execution_status(status: str) -> str:
    if status == FORBIDDEN_EXECUTION_STATUS:
        raise RuntimeStateError("INVALID_EXECUTION_STATUS:NO_PUBLISH_CANDIDATE")
    if status not in EXECUTION_STATUSES:
        raise RuntimeStateError(f"INVALID_EXECUTION_STATUS:{status}")
    return status


def _set_private_mode(path: Path, mode: int) -> None:
    os.chmod(path, mode)


def ensure_runtime_dirs(runtime_root: Path, requested_date: str) -> Path:
    """Create only the supplied test/runtime tree with private permissions."""

    _ensure_date(requested_date)
    day_dir = runtime_root / "runs" / requested_date
    day_dir.mkdir(parents=True, exist_ok=True)
    _set_private_mode(runtime_root, 0o700)
    _set_private_mode(runtime_root / "runs", 0o700)
    _set_private_mode(day_dir, 0o700)
    return day_dir


def run_directory(runtime_root: Path, requested_date: str, run_id: str) -> Path:
    """Create a unique run directory; never overwrite an existing run."""

    _ensure_date(requested_date)
    _ensure_run_id(run_id)
    day_dir = ensure_runtime_dirs(runtime_root, requested_date)
    path = day_dir / run_id
    path.mkdir(mode=0o700)
    _set_private_mode(path, 0o700)
    return path


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    """Write JSON through a flushed temporary sibling and atomic replacement."""

    path.parent.mkdir(parents=True, exist_ok=True)
    _set_private_mode(path.parent, 0o700)
    temporary_path: Path | None = None
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        _set_private_mode(temporary_path, 0o600)
        os.replace(temporary_path, path)
        _set_private_mode(path, 0o600)
    except BaseException:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
        raise


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object or fail closed with RuntimeStateError."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeStateError("MALFORMED_STATE") from exc
    if not isinstance(value, dict):
        raise RuntimeStateError("MALFORMED_STATE")
    return value


def validate_status_record(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the minimal machine status contract without editorial logic."""

    status = value.get("status")
    if not isinstance(status, str):
        raise RuntimeStateError("MALFORMED_STATE:status")
    _ensure_execution_status(status)
    return dict(value)


def write_status(path: Path, status_record: Mapping[str, Any]) -> None:
    """Validate and atomically persist a machine status record."""

    atomic_write_json(path, validate_status_record(status_record))


def read_status(path: Path) -> dict[str, Any]:
    """Read and validate a machine status record."""

    return validate_status_record(read_json(path))


def _status_files(day_dir: Path) -> list[Path]:
    if not day_dir.is_dir():
        return []
    return sorted(
        path / "status.json"
        for path in day_dir.iterdir()
        if path.is_dir() and path.name != ".run.lock" and (path / "status.json").is_file()
    )


def has_terminal_result(runtime_root: Path, requested_date: str) -> bool:
    """Return true if any valid run for the date has a terminal result."""

    _ensure_date(requested_date)
    day_dir = runtime_root / "runs" / requested_date
    for status_path in _status_files(day_dir):
        try:
            if read_status(status_path).get("status") in TERMINAL_STATUSES:
                return True
        except RuntimeStateError as exc:
            raise RuntimeStateError("MALFORMED_STATE_REQUIRES_HUMAN_REVIEW") from exc
    return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _pid_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


@dataclass(frozen=True)
class LockResult:
    acquired: bool
    status: str
    reason: str
    lock_path: Path
    metadata: dict[str, Any] | None = None


@dataclass
class RunLock:
    path: Path
    metadata: dict[str, Any]

    def release(self) -> None:
        """Release only the lock owned by this RunLock instance."""

        current = read_json(self.path / "metadata.json")
        owner_fields = ("run_id", "pid", "hostname", "started_at")
        if any(current.get(field) != self.metadata.get(field) for field in owner_fields):
            raise RuntimeStateError("LOCK_OWNER_MISMATCH")
        (self.path / "metadata.json").unlink()
        self.path.rmdir()


def acquire_lock(
    runtime_root: Path,
    requested_date: str,
    run_id: str,
    *,
    schema_version: str = SCHEMA_VERSION,
    pid: int | None = None,
    hostname: str | None = None,
    started_at: str | None = None,
    pid_exists: Any = _pid_exists,
    allow_terminal_result: bool = False,
) -> tuple[LockResult, RunLock | None]:
    """Acquire the date lock or return a fail-closed decision.

    A stale lock is never removed automatically.  PID existence is only a
    signal: PID reuse and process identity limitations mean it cannot prove
    ownership or liveness by itself.
    """

    _ensure_date(requested_date)
    _ensure_run_id(run_id)
    day_dir = ensure_runtime_dirs(runtime_root, requested_date)
    lock_path = day_dir / ".run.lock"

    try:
        terminal_result_exists = has_terminal_result(runtime_root, requested_date)
    except RuntimeStateError as exc:
        return LockResult(False, "ERROR", str(exc), lock_path), None

    if terminal_result_exists and not allow_terminal_result:
        return LockResult(False, "DUPLICATE_SUPPRESSED", "TERMINAL_RESULT_EXISTS", lock_path), None

    try:
        lock_path.mkdir(mode=0o700)
    except FileExistsError:
        metadata_path = lock_path / "metadata.json"
        try:
            metadata = read_json(metadata_path)
        except RuntimeStateError:
            return LockResult(False, "ERROR", "STALE_LOCK_REQUIRES_HUMAN_REVIEW", lock_path), None
        existing_pid = metadata.get("pid")
        if isinstance(existing_pid, int) and pid_exists(existing_pid):
            return LockResult(False, "DUPLICATE_SUPPRESSED", "ACTIVE_LOCK", lock_path, metadata), None
        return LockResult(False, "ERROR", "STALE_LOCK_REQUIRES_HUMAN_REVIEW", lock_path, metadata), None

    metadata = {
        "run_id": run_id,
        "pid": os.getpid() if pid is None else pid,
        "hostname": socket.gethostname() if hostname is None else hostname,
        "started_at": _now_iso() if started_at is None else started_at,
        "schema_version": schema_version,
    }
    try:
        atomic_write_json(lock_path / "metadata.json", metadata)
    except BaseException:
        try:
            lock_path.rmdir()
        except OSError:
            pass
        raise
    lock = RunLock(lock_path, metadata)
    return LockResult(True, "RUNNING", "LOCK_ACQUIRED", lock_path, metadata), lock
