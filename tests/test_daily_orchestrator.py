import hashlib
import json
import os
import stat
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import scripts.daily_orchestrator as orchestrator_module
from scripts.codex_runner import CodexResult
from scripts.daily_orchestrator import (
    PROMPT_HASH_PLACEHOLDER,
    RUNTIME_DATE_PLACEHOLDER,
    _write_text_atomically_once,
    run_phase1,
)
from scripts.gate1_validator import ValidationResult
from scripts.runtime_state import acquire_lock, run_directory, write_status


DATE = "2026-09-15"


class FakeLock:
    def __init__(self, release_error=None):
        self.released = False
        self.release_error = release_error

    def release(self):
        if self.release_error:
            raise RuntimeError(self.release_error)
        self.released = True


class DailyOrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime = self.root / "runtime"
        self.brief = self.root / "brief"
        self.prompt = self.root / "prompt.md"
        self.prompt.write_text(
            "Prompt-Version: phase1-0.2\n"
            "Run target: INJECTED_RUN_DATE_BY_ORCHESTRATOR\n"
            "Prompt-SHA256: INJECTED_BY_ORCHESTRATOR\n"
            "Prompt body.\n",
            encoding="utf-8",
        )
        self.fake_runner = Mock(
            return_value=CodexResult(
                "SUCCESS", True, 0, "candidate output", "diagnostic", 0.1, ("fake",)
            )
        )
        self.fake_validator = Mock(
            return_value=ValidationResult(True, "PASS", "NONE", (), (), {})
        )

    def tearDown(self):
        self.temp.cleanup()

    def ready_checker(self, requested_date, brief_root):
        return {"ready": True, "status": "READY", "warnings": ["warning"]}

    def not_ready_checker(self, requested_date, brief_root):
        return {"ready": False, "status": "BRIEF_NOT_READY", "errors": ["MISSING_BRIEF"]}

    def execute(self, **kwargs):
        options = {
            "requested_date": DATE,
            "brief_root": self.brief,
            "runtime_root": self.runtime,
            "prompt_path": self.prompt,
            "executable": "/fake/codex",
            "working_directory": self.root,
            "model": "fake-model",
            "timeout_seconds": 10,
            "run_id": "run-test-001",
            "brief_checker": self.ready_checker,
            "codex_runner": self.fake_runner,
            "gate1_validator": self.fake_validator,
            "human_approved_rerun": False,
        }
        options.update(kwargs)
        return run_phase1(**options)

    def test_ready_brief_lock_and_success_output(self):
        result = self.execute()
        self.assertEqual(result.codex_status, "SUCCESS")
        self.assertEqual(result.output_state, "VALIDATED_GATE1_OUTPUT")
        self.assertEqual(result.execution_status, "GATE1_READY")
        self.assertTrue(result.human_review_required)

    def test_success_never_becomes_gate1_ready(self):
        self.assertEqual(self.execute().execution_status, "GATE1_READY")

    def test_success_output_is_validated(self):
        result = self.execute()
        self.assertIsNone(result.error_reason)

    def test_raw_output_saved_and_gate1_matches(self):
        result = self.execute()
        run_path = Path(result.run_directory)
        self.assertEqual((run_path / "raw-output.txt").read_text(), "candidate output")
        self.assertEqual((run_path / "gate1.md").read_text(), (run_path / "raw-output.txt").read_text())

    def test_validation_result_is_saved_and_human_decision_stays_pending(self):
        result = self.execute()
        run_path = Path(result.run_directory)
        validation = json.loads((run_path / "validation_result.json").read_text())
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(json.loads((run_path / "status.json").read_text())["human_review_required"], True)

    def test_prompt_runtime_values_are_injected_and_source_unchanged(self):
        original = self.prompt.read_bytes()
        captured = {}
        requested_date = "2026-09-18"

        def runner(prompt, **kwargs):
            captured["prompt"] = prompt
            return self.fake_runner.return_value

        self.execute(codex_runner=runner, requested_date=requested_date)
        self.assertEqual(self.prompt.read_bytes(), original)
        self.assertEqual(captured["prompt"].count(PROMPT_HASH_PLACEHOLDER), 0)
        self.assertEqual(captured["prompt"].count(RUNTIME_DATE_PLACEHOLDER), 0)
        self.assertIn("Prompt-SHA256: ", captured["prompt"])
        self.assertIn(f"Run target: {requested_date}", captured["prompt"])

    def test_prompt_missing_fails_closed(self):
        result = self.execute(prompt_path=self.root / "missing.md")
        self.assertEqual(result.error_reason, "PROMPT_NOT_FOUND")
        self.assertEqual(result.requested_date, DATE)
        self.assertNotEqual(result.requested_date, result.run_id)
        status = json.loads((Path(result.run_directory) / "status.json").read_text())
        self.assertEqual(status["requested_date"], DATE)
        self.assertNotEqual(status["requested_date"], status["run_id"])
        self.fake_runner.assert_not_called()

    def test_prompt_empty_fails_closed(self):
        path = self.root / "empty.md"
        path.write_text("\n", encoding="utf-8")
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_EMPTY")
        self.fake_runner.assert_not_called()

    def test_prompt_invalid_utf8_fails_closed(self):
        path = self.root / "invalid.md"
        path.write_bytes(b"\xff")
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_INVALID_UTF8")
        self.fake_runner.assert_not_called()

    def test_prompt_placeholder_missing_fails_closed(self):
        path = self.root / "missing-placeholder.md"
        path.write_text("Prompt-Version: phase1-0.1\n", encoding="utf-8")
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_HASH_PLACEHOLDER_MISSING")
        self.fake_runner.assert_not_called()

    def test_prompt_placeholder_duplicate_fails_closed(self):
        path = self.root / "duplicate-placeholder.md"
        path.write_text(
            f"{RUNTIME_DATE_PLACEHOLDER}\n{PROMPT_HASH_PLACEHOLDER}\n{PROMPT_HASH_PLACEHOLDER}\n",
            encoding="utf-8",
        )
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_HASH_PLACEHOLDER_DUPLICATE")
        self.fake_runner.assert_not_called()

    def test_date_placeholder_missing_fails_closed(self):
        path = self.root / "missing-date-placeholder.md"
        path.write_text(f"Prompt-SHA256: {PROMPT_HASH_PLACEHOLDER}\n", encoding="utf-8")
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_DATE_PLACEHOLDER_MISSING")
        self.fake_runner.assert_not_called()

    def test_date_placeholder_duplicate_fails_closed(self):
        path = self.root / "duplicate-date-placeholder.md"
        path.write_text(
            f"Prompt-SHA256: {PROMPT_HASH_PLACEHOLDER}\n"
            f"Run target: {RUNTIME_DATE_PLACEHOLDER}\n"
            f"Run target duplicate: {RUNTIME_DATE_PLACEHOLDER}\n",
            encoding="utf-8",
        )
        result = self.execute(prompt_path=path)
        self.assertEqual(result.error_reason, "PROMPT_DATE_PLACEHOLDER_DUPLICATE")
        self.fake_runner.assert_not_called()

    def test_brief_not_ready_does_not_call_codex(self):
        result = self.execute(brief_checker=self.not_ready_checker)
        self.assertEqual(result.execution_status, "BRIEF_NOT_READY")
        self.fake_runner.assert_not_called()

    def test_human_approved_rerun_default_is_false(self):
        first = self.execute()
        second = self.execute(run_id="run-test-002")
        self.assertEqual(first.execution_status, "GATE1_READY")
        self.assertEqual(second.execution_status, "DUPLICATE_SUPPRESSED")
        self.assertEqual(self.fake_runner.call_count, 1)

    def test_human_approved_rerun_starts_new_run_without_touching_previous(self):
        first = self.execute()
        first_path = Path(first.run_directory)
        first_status = (first_path / "status.json").read_bytes()
        second = self.execute(run_id="run-test-002", human_approved_rerun=True)
        self.assertEqual(second.execution_status, "GATE1_READY")
        self.assertNotEqual(first.run_id, second.run_id)
        self.assertEqual((first_path / "status.json").read_bytes(), first_status)
        self.assertTrue(Path(second.run_directory).exists())
        self.assertEqual(self.fake_runner.call_count, 2)

    def test_human_approved_rerun_reused_run_id_fails(self):
        first = self.execute()
        result = self.execute(run_id=first.run_id, human_approved_rerun=True)
        self.assertEqual(result.execution_status, "ERROR")
        self.assertEqual(result.error_reason, "RUNTIME_WRITE_FAILED")
        self.assertEqual(self.fake_runner.call_count, 1)

    def test_human_approved_rerun_active_lock_does_not_call_codex(self):
        _, lock = acquire_lock(self.runtime, DATE, "active", pid=os.getpid())
        try:
            result = self.execute(run_id="run-test-002", human_approved_rerun=True)
        finally:
            lock.release()
        self.assertEqual(result.error_reason, "ACTIVE_LOCK")
        self.fake_runner.assert_not_called()

    def test_human_approved_rerun_stale_lock_does_not_call_codex(self):
        _, lock = acquire_lock(self.runtime, DATE, "stale", pid=999999)
        lock_path = self.runtime / "runs" / DATE / ".run.lock"
        result = self.execute(run_id="run-test-002", human_approved_rerun=True)
        self.assertEqual(result.error_reason, "STALE_LOCK_REQUIRES_HUMAN_REVIEW")
        self.assertTrue(lock_path.exists())
        self.fake_runner.assert_not_called()
        lock.release()

    def test_human_approved_rerun_malformed_state_does_not_call_codex(self):
        broken = run_directory(self.runtime, DATE, "broken")
        (broken / "status.json").write_text("{broken", encoding="utf-8")
        result = self.execute(run_id="run-test-002", human_approved_rerun=True)
        self.assertEqual(result.error_reason, "MALFORMED_STATE_REQUIRES_HUMAN_REVIEW")
        self.fake_runner.assert_not_called()

    def test_brief_not_ready_creates_terminal_result_under_own_lock(self):
        result = self.execute(brief_checker=self.not_ready_checker)
        run_path = Path(result.run_directory)
        self.assertEqual(json.loads((run_path / "status.json").read_text())["status"], "BRIEF_NOT_READY")
        self.assertFalse((self.runtime / "runs" / DATE / ".run.lock").exists())
        self.fake_runner.assert_not_called()

    def test_brief_not_ready_second_run_is_suppressed_without_new_directory(self):
        first = self.execute(brief_checker=self.not_ready_checker)
        second = self.execute(brief_checker=self.not_ready_checker, run_id="run-test-002")
        day_dir = self.runtime / "runs" / DATE
        run_dirs = sorted(path.name for path in day_dir.iterdir() if path.is_dir())
        self.assertEqual(second.execution_status, "DUPLICATE_SUPPRESSED")
        self.assertEqual(run_dirs, ["run-test-001"])
        self.assertIsNotNone(first.run_directory)
        self.fake_runner.assert_not_called()

    def test_brief_not_ready_active_lock_is_fail_closed_without_new_directory(self):
        lock_result, lock = acquire_lock(self.runtime, DATE, "active", pid=os.getpid())
        self.assertTrue(lock_result.acquired)
        try:
            result = self.execute(brief_checker=self.not_ready_checker)
        finally:
            lock.release()
        self.assertEqual(result.execution_status, "DUPLICATE_SUPPRESSED")
        self.assertIsNone(result.run_directory)
        self.fake_runner.assert_not_called()

    def test_brief_not_ready_stale_lock_is_preserved_without_new_directory(self):
        lock_result, lock = acquire_lock(self.runtime, DATE, "stale", pid=999999)
        self.assertTrue(lock_result.acquired)
        lock_path = lock_result.lock_path
        result = self.execute(brief_checker=self.not_ready_checker)
        self.assertEqual(result.error_reason, "STALE_LOCK_REQUIRES_HUMAN_REVIEW")
        self.assertTrue(lock_path.exists())
        self.assertEqual([path.name for path in (self.runtime / "runs" / DATE).iterdir() if path.is_dir()], [".run.lock"])
        self.fake_runner.assert_not_called()
        lock.release()

    def test_duplicate_active_lock_does_not_call_codex(self):
        first, lock = acquire_lock(self.runtime, DATE, "existing", pid=os.getpid())
        self.assertTrue(first.acquired)
        try:
            result = self.execute()
        finally:
            lock.release()
        self.assertEqual(result.error_reason, "ACTIVE_LOCK")
        self.fake_runner.assert_not_called()

    def test_stale_lock_does_not_call_codex(self):
        first, lock = acquire_lock(self.runtime, DATE, "stale", pid=999999)
        self.assertTrue(first.acquired)
        lock_path = first.lock_path
        result = self.execute()
        self.assertEqual(result.error_reason, "STALE_LOCK_REQUIRES_HUMAN_REVIEW")
        self.assertTrue(lock_path.exists())
        self.fake_runner.assert_not_called()
        lock.release()

    def test_malformed_state_does_not_call_codex(self):
        run_path = run_directory(self.runtime, DATE, "broken")
        (run_path / "status.json").write_text("{broken", encoding="utf-8")
        result = self.execute()
        self.assertEqual(result.error_reason, "MALFORMED_STATE_REQUIRES_HUMAN_REVIEW")
        self.fake_runner.assert_not_called()
        self.assertEqual((run_path / "status.json").read_text(), "{broken")

    def test_nonzero_timeout_missing_and_runner_error_map_to_error(self):
        for transport_status in ("CODEX_NONZERO_EXIT", "TIMEOUT", "EXECUTABLE_NOT_FOUND", "RUNNER_ERROR"):
            with self.subTest(transport_status=transport_status):
                self.runtime = self.root / f"runtime-{transport_status}"
                runner = Mock(return_value=CodexResult(transport_status, False, None, "out", "err", 0.1, ("fake",)))
                result = self.execute(codex_runner=runner, run_id=f"run-{transport_status}")
                self.assertEqual(result.execution_status, "ERROR")
                self.assertEqual(result.codex_status, transport_status)
                self.assertEqual(result.output_state, "NONE")

    def test_runner_called_once_and_streams_preserved(self):
        result = self.execute()
        self.fake_runner.assert_called_once()
        payload = json.loads((Path(result.run_directory) / "codex_result.json").read_text())
        self.assertEqual((payload["stdout"], payload["stderr"]), ("candidate output", "diagnostic"))

    def test_validator_receives_runtime_metadata(self):
        captured = {}

        def runner(prompt, **kwargs):
            captured["prompt"] = prompt
            return self.fake_runner.return_value

        result = self.execute(codex_runner=runner)
        self.assertEqual(result.execution_status, "GATE1_READY")
        kwargs = self.fake_validator.call_args.kwargs
        self.assertEqual(kwargs["requested_date"], DATE)
        self.assertIn(f"Run target: {kwargs['requested_date']}", captured["prompt"])
        self.assertEqual(kwargs["prompt_version"], "phase1-0.2")
        self.assertEqual(kwargs["brief_readiness"], "READY")
        self.assertEqual(len(kwargs["prompt_sha256"]), 64)

    def test_malformed_validator_result_preserves_raw_without_gate1(self):
        validator = Mock(
            return_value=ValidationResult(False, "FAIL", "MALFORMED_GATE1", ("bad",), (), {})
        )
        result = self.execute(gate1_validator=validator)
        run_path = Path(result.run_directory)
        self.assertEqual(result.execution_status, "MALFORMED_GATE1")
        self.assertTrue((run_path / "raw-output.txt").exists())
        self.assertTrue((run_path / "validation_result.json").exists())
        self.assertFalse((run_path / "gate1.md").exists())

    def test_boundary_validator_result_preserves_raw_without_gate1(self):
        validator = Mock(
            return_value=ValidationResult(False, "FAIL", "BOUNDARY_VIOLATION", ("boundary",), (), {})
        )
        result = self.execute(gate1_validator=validator)
        self.assertEqual(result.execution_status, "BOUNDARY_VIOLATION")
        self.assertFalse((Path(result.run_directory) / "gate1.md").exists())

    def test_validator_error_maps_to_error_without_gate1(self):
        validator = Mock(
            return_value=ValidationResult(False, "ERROR", "VALIDATOR_ERROR", ("error",), (), {})
        )
        result = self.execute(gate1_validator=validator)
        self.assertEqual(result.execution_status, "ERROR")
        self.assertEqual(result.error_reason, "VALIDATOR_ERROR")
        self.assertFalse((Path(result.run_directory) / "gate1.md").exists())

    def test_existing_gate1_is_not_overwritten(self):
        original_writer = orchestrator_module._write_text_atomically_once

        def create_existing_then_write(path, content):
            if path.name == "gate1.md":
                path.write_text("existing gate1", encoding="utf-8")
            return original_writer(path, content)

        with patch.object(orchestrator_module, "_write_text_atomically_once", side_effect=create_existing_then_write):
            result = self.execute()
        run_path = Path(result.run_directory)
        self.assertEqual(result.execution_status, "ERROR")
        self.assertEqual((run_path / "gate1.md").read_text(), "existing gate1")

    def test_gate1_symlink_is_not_replaced(self):
        original_writer = orchestrator_module._write_text_atomically_once
        target = self.root / "gate1-target.txt"
        target.write_text("symlink target", encoding="utf-8")

        def create_symlink_then_write(path, content):
            if path.name == "gate1.md":
                path.symlink_to(target)
            return original_writer(path, content)

        with patch.object(orchestrator_module, "_write_text_atomically_once", side_effect=create_symlink_then_write):
            result = self.execute()
        run_path = Path(result.run_directory)
        self.assertEqual(result.execution_status, "ERROR")
        self.assertTrue((run_path / "gate1.md").is_symlink())
        self.assertEqual(target.read_text(), "symlink target")

    def test_validation_result_write_failure_does_not_create_gate1(self):
        original_atomic_json = orchestrator_module.atomic_write_json

        def fail_validation_result(path, value):
            if path.name == "validation_result.json":
                raise OSError("validation result write failed")
            return original_atomic_json(path, value)

        with patch.object(orchestrator_module, "atomic_write_json", side_effect=fail_validation_result):
            result = self.execute()
        self.assertEqual(result.execution_status, "ERROR")
        self.assertFalse((Path(result.run_directory) / "gate1.md").exists())

    def test_artifact_permissions(self):
        result = self.execute()
        run_path = Path(result.run_directory)
        self.assertEqual(stat.S_IMODE(run_path.stat().st_mode), 0o700)
        for name in ("status.json", "codex_result.json", "validation_result.json", "raw-output.txt", "gate1.md"):
            self.assertEqual(stat.S_IMODE((run_path / name).stat().st_mode), 0o600)

    def test_existing_artifact_is_not_overwritten(self):
        first = self.execute()
        second = self.execute(run_id="run-test-001")
        self.assertEqual(second.error_reason, "TERMINAL_RESULT_EXISTS")
        self.assertEqual((Path(first.run_directory) / "raw-output.txt").read_text(), "candidate output")

    def test_own_lock_is_released(self):
        result = self.execute()
        self.assertFalse((self.runtime / "runs" / DATE / ".run.lock").exists())
        self.assertIsNotNone(result.run_directory)

    def test_foreign_lock_is_not_removed(self):
        lock_result, lock = acquire_lock(self.runtime, DATE, "foreign", pid=999999)
        self.assertTrue(lock_result.acquired)
        lock_path = lock_result.lock_path
        result = self.execute()
        self.assertEqual(result.execution_status, "ERROR")
        self.assertTrue(lock_path.exists())
        lock.release()

    def test_lock_release_failure_is_fail_closed(self):
        fake_lock = FakeLock(release_error="do not remove foreign lock")

        def lock_acquirer(*args, **kwargs):
            return Mock(acquired=True), fake_lock

        result = self.execute(lock_acquirer=lock_acquirer)
        self.assertEqual(result.execution_status, "ERROR")
        self.assertEqual(result.error_reason, "LOCK_RELEASE_FAILED")
        self.assertFalse(fake_lock.released)

    def test_prompt_not_saved_in_codex_result(self):
        result = self.execute()
        payload = json.loads((Path(result.run_directory) / "codex_result.json").read_text())
        self.assertNotIn("prompt", payload)
        self.assertNotIn("Prompt body", json.dumps(payload))

    def test_tests_do_not_modify_real_runtime_root(self):
        real_runtime = Path.home() / "Library" / "Application Support" / "WorldInsightDaily"

        def inventory(path):
            if not path.exists():
                return None
            entries = []
            for item in [path, *sorted(path.rglob("*"))]:
                relative = "." if item == path else str(item.relative_to(path))
                mode = stat.S_IMODE(item.stat().st_mode)
                digest = hashlib.sha256(item.read_bytes()).hexdigest() if item.is_file() else None
                entries.append((relative, item.is_dir(), mode, item.stat().st_size, item.stat().st_mtime_ns, digest))
            return tuple(entries)

        before = inventory(real_runtime)
        result = self.execute()
        after = inventory(real_runtime)

        self.assertEqual(before, after)
        self.assertTrue(str(result.run_directory).startswith(str(self.runtime)))
        self.assertNotIn(str(real_runtime), str(result.run_directory))

    def test_raw_output_preexisting_content_is_not_overwritten(self):
        path = self.root / "raw-output.txt"
        path.write_text("original", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            _write_text_atomically_once(path, "replacement")
        self.assertEqual(path.read_text(encoding="utf-8"), "original")

    def test_raw_output_overwrite_attempt_failure_preserves_existing_content(self):
        path = self.root / "raw-output.txt"
        path.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            _write_text_atomically_once(path, "do not write")
        self.assertEqual(path.read_text(encoding="utf-8"), "keep")

    def test_raw_output_normal_creation_is_private(self):
        path = self.root / "new-raw-output.txt"
        _write_text_atomically_once(path, "created")
        self.assertEqual(path.read_text(encoding="utf-8"), "created")
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
