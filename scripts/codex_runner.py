"""Safe, non-interactive transport wrapper for the Codex CLI.

This module deliberately contains no Daily Run, workflow, or post-Gate-1
operations.  It only builds a constrained command and returns process results.
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence


DEFAULT_CODEX_EXECUTABLE = "/opt/homebrew/bin/codex"
RUNNER_STATUSES = frozenset(
    {
        "SUCCESS",
        "CODEX_NONZERO_EXIT",
        "TIMEOUT",
        "EXECUTABLE_NOT_FOUND",
        "INVALID_CONFIGURATION",
        "RUNNER_ERROR",
    }
)


class RunnerConfigurationError(ValueError):
    """Raised internally when the execution contract is invalid."""


@dataclass(frozen=True)
class CodexCommand:
    """Prompt-free command representation suitable for review and logging."""

    argv: tuple[str, ...]

    def as_list(self) -> list[str]:
        return list(self.argv)


@dataclass(frozen=True)
class CodexResult:
    status: str
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    elapsed_seconds: float
    command: tuple[str, ...]
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible result without prompt text or secrets."""

        return {
            "status": self.status,
            "success": self.success,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "elapsed_seconds": self.elapsed_seconds,
            "command": list(self.command),
            "error": self.error,
        }


def _validate_configuration(
    executable: str | Path,
    working_directory: str | Path,
    model: str | None,
    timeout_seconds: float,
) -> tuple[Path, Path, str | None, float]:
    executable_path = Path(executable) if str(executable) else None
    working_directory_path = Path(working_directory) if str(working_directory) else None

    if executable_path is None or not str(executable_path):
        raise RunnerConfigurationError("executable is required")
    if working_directory_path is None or not working_directory_path.is_dir():
        raise RunnerConfigurationError("working directory must be an existing directory")
    if model is not None and (not isinstance(model, str) or not model.strip()):
        raise RunnerConfigurationError("model is required")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
        raise RunnerConfigurationError("timeout must be a positive number")
    if timeout_seconds <= 0:
        raise RunnerConfigurationError("timeout must be a positive number")

    return executable_path, working_directory_path, model, float(timeout_seconds)


def build_command(
    executable: str | Path,
    working_directory: str | Path,
    model: str | None = None,
) -> CodexCommand:
    """Build the constrained command; None uses the CLI/account model default."""

    executable_path, working_directory_path, model, _ = _validate_configuration(
        executable, working_directory, model, 1
    )
    command = [
        str(executable_path),
        "exec",
        "-C",
        str(working_directory_path),
        "-s",
        "read-only",
    ]
    if model is not None:
        command.extend(("-m", model))
    command.append("--ephemeral")
    return CodexCommand(tuple(command))


def _text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _result(
    status: str,
    command: Sequence[str],
    started: float,
    *,
    exit_code: int | None = None,
    stdout: str | bytes | None = "",
    stderr: str | bytes | None = "",
    error: str | None = None,
) -> CodexResult:
    return CodexResult(
        status=status,
        success=status == "SUCCESS",
        exit_code=exit_code,
        stdout=_text(stdout),
        stderr=_text(stderr),
        elapsed_seconds=max(0.0, time.monotonic() - started),
        command=tuple(command),
        error=error,
    )


def run_codex(
    prompt: str,
    *,
    executable: str | Path = DEFAULT_CODEX_EXECUTABLE,
    working_directory: str | Path,
    timeout_seconds: float,
    model: str | None = None,
    subprocess_run: Callable[..., Any] = subprocess.run,
) -> CodexResult:
    """Run Codex through stdin and return a machine-readable transport result."""

    started = time.monotonic()
    try:
        executable_path, working_directory_path, model, timeout = _validate_configuration(
            executable, working_directory, model, timeout_seconds
        )
        command = build_command(executable_path, working_directory_path, model)
    except (RunnerConfigurationError, TypeError, ValueError):
        return _result("INVALID_CONFIGURATION", (), started, error="INVALID_CONFIGURATION")

    try:
        completed = subprocess_run(
            command.as_list(),
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            cwd=str(working_directory_path),
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return _result(
            "TIMEOUT",
            command.argv,
            started,
            stdout=getattr(exc, "stdout", None),
            stderr=getattr(exc, "stderr", None),
            error="TIMEOUT",
        )
    except FileNotFoundError:
        return _result("EXECUTABLE_NOT_FOUND", command.argv, started, error="EXECUTABLE_NOT_FOUND")
    except Exception:
        return _result("RUNNER_ERROR", command.argv, started, error="RUNNER_ERROR")

    status = "SUCCESS" if completed.returncode == 0 else "CODEX_NONZERO_EXIT"
    return _result(
        status,
        command.argv,
        started,
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
