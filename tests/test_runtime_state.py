import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts import runtime_state


TEST_DATE = "2026-09-15"


class RuntimeStateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def acquire(self, run_id="run-001"):
        return runtime_state.acquire_lock(
            self.root,
            TEST_DATE,
            run_id,
            pid=12345,
            hostname="test-host",
            started_at="2026-09-15T07:00:00+09:00",
            pid_exists=lambda pid: pid == 12345,
        )

    def test_first_run_can_acquire_lock(self):
        result, lock = self.acquire()
        self.assertTrue(result.acquired)
        self.assertEqual(result.status, "RUNNING")
        self.assertIsNotNone(lock)
        self.assertTrue(result.lock_path.is_dir())

    def test_second_simultaneous_run_is_rejected(self):
        _, lock = self.acquire()
        self.assertIsNotNone(lock)
        result, second_lock = self.acquire("run-002")
        self.assertFalse(result.acquired)
        self.assertEqual(result.status, "DUPLICATE_SUPPRESSED")
        self.assertEqual(result.reason, "ACTIVE_LOCK")
        self.assertIsNone(second_lock)
        lock.release()

    def test_lock_metadata_round_trip(self):
        result, lock = self.acquire()
        self.assertIsNotNone(lock)
        metadata = runtime_state.read_json(result.lock_path / "metadata.json")
        self.assertEqual(metadata["run_id"], "run-001")
        self.assertEqual(metadata["pid"], 12345)
        self.assertEqual(metadata["hostname"], "test-host")
        self.assertEqual(metadata["started_at"], "2026-09-15T07:00:00+09:00")
        self.assertEqual(metadata["schema_version"], runtime_state.SCHEMA_VERSION)
        lock.release()

    def test_lock_release(self):
        result, lock = self.acquire()
        self.assertIsNotNone(lock)
        lock.release()
        self.assertFalse(result.lock_path.exists())
        next_result, next_lock = self.acquire("run-002")
        self.assertTrue(next_result.acquired)
        next_lock.release()

    def test_stale_lock_is_detected_but_not_auto_deleted(self):
        lock_path = runtime_state.ensure_runtime_dirs(self.root, TEST_DATE) / ".run.lock"
        lock_path.mkdir(mode=0o700)
        runtime_state.atomic_write_json(
            lock_path / "metadata.json",
            {
                "run_id": "old-run",
                "pid": 99999,
                "hostname": "old-host",
                "started_at": "2026-09-15T06:00:00+09:00",
                "schema_version": runtime_state.SCHEMA_VERSION,
            },
        )
        result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-002", pid_exists=lambda pid: False
        )
        self.assertFalse(result.acquired)
        self.assertEqual(result.status, "ERROR")
        self.assertEqual(result.reason, "STALE_LOCK_REQUIRES_HUMAN_REVIEW")
        self.assertTrue(lock_path.exists())
        self.assertIsNone(lock)

    def test_terminal_result_suppresses_normal_duplicate(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(run_dir / "status.json", {"status": "GATE1_READY", "run_id": "run-001"})
        result, lock = self.acquire("run-002")
        self.assertFalse(result.acquired)
        self.assertEqual(result.status, "DUPLICATE_SUPPRESSED")
        self.assertEqual(result.reason, "TERMINAL_RESULT_EXISTS")
        self.assertIsNone(lock)

    def test_human_approved_rerun_allows_new_run_with_new_id(self):
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(first / "status.json", {"status": "GATE1_READY", "run_id": "run-001"})
        result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-002", allow_terminal_result=True,
            pid_exists=lambda pid: pid == 12345,
        )
        self.assertTrue(result.acquired)
        self.assertIsNotNone(lock)
        lock.release()
        self.assertTrue((first / "status.json").exists())
        self.assertFalse((self.root / "runs" / TEST_DATE / "run-002").exists())

    def test_human_approved_rerun_reused_run_id_fails_at_run_directory(self):
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(first / "status.json", {"status": "GATE1_READY", "run_id": "run-001"})
        result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-001", allow_terminal_result=True
        )
        self.assertTrue(result.acquired)
        with self.assertRaises(FileExistsError):
            runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        lock.release()

    def test_human_approved_rerun_does_not_bypass_active_lock(self):
        _, active = self.acquire("active")
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(first / "status.json", {"status": "GATE1_READY", "run_id": "run-001"})
        result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-002", allow_terminal_result=True,
            pid_exists=lambda pid: pid == 12345,
        )
        self.assertFalse(result.acquired)
        self.assertEqual(result.reason, "ACTIVE_LOCK")
        self.assertIsNone(lock)
        active.release()

    def test_human_approved_rerun_does_not_bypass_stale_lock(self):
        lock_result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "stale", pid=999999
        )
        self.assertTrue(lock_result.acquired)
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(first / "status.json", {"status": "GATE1_READY", "run_id": "run-001"})
        result, new_lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-002", allow_terminal_result=True, pid_exists=lambda pid: False
        )
        self.assertFalse(result.acquired)
        self.assertEqual(result.reason, "STALE_LOCK_REQUIRES_HUMAN_REVIEW")
        self.assertIsNone(new_lock)
        self.assertTrue(lock_result.lock_path.exists())
        lock.release()

    def test_human_approved_rerun_does_not_bypass_malformed_state(self):
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        status_path = first / "status.json"
        status_path.write_text("{broken", encoding="utf-8")
        result, lock = runtime_state.acquire_lock(
            self.root, TEST_DATE, "run-002", allow_terminal_result=True
        )
        self.assertFalse(result.acquired)
        self.assertEqual(result.reason, "MALFORMED_STATE_REQUIRES_HUMAN_REVIEW")
        self.assertIsNone(lock)
        self.assertEqual(status_path.read_text(encoding="utf-8"), "{broken")

    def test_malformed_existing_state_blocks_new_run_without_modification(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        status_path = run_dir / "status.json"
        malformed = "{malformed existing state}\n"
        status_path.write_text(malformed, encoding="utf-8")

        result, lock = self.acquire("run-002")

        self.assertFalse(result.acquired)
        self.assertEqual(result.status, "ERROR")
        self.assertEqual(result.reason, "MALFORMED_STATE_REQUIRES_HUMAN_REVIEW")
        self.assertIsNone(lock)
        self.assertFalse((self.root / "runs" / TEST_DATE / ".run.lock").exists())
        self.assertFalse((self.root / "runs" / TEST_DATE / "run-002").exists())
        self.assertEqual(status_path.read_text(encoding="utf-8"), malformed)

    def test_previous_artifacts_are_not_overwritten(self):
        first = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        artifact = first / "gate1.md"
        artifact.write_text("first", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        second = runtime_state.run_directory(self.root, TEST_DATE, "run-002")
        self.assertEqual(artifact.read_text(encoding="utf-8"), "first")
        self.assertNotEqual(first, second)

    def test_atomic_status_write_read(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        path = run_dir / "status.json"
        runtime_state.write_status(path, {"status": "RUNNING", "run_id": "run-001"})
        self.assertEqual(runtime_state.read_status(path)["status"], "RUNNING")
        self.assertFalse(any(run_dir.glob("*.tmp")))

    def test_malformed_state_fails_closed(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        path = run_dir / "status.json"
        path.write_text("{not-json", encoding="utf-8")
        with self.assertRaises(runtime_state.RuntimeStateError):
            runtime_state.read_status(path)

    def test_temporary_runtime_root_works_with_private_permissions(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        self.assertEqual(os.stat(self.root).st_mode & 0o777, 0o700)
        self.assertEqual(os.stat(run_dir).st_mode & 0o777, 0o700)
        path = run_dir / "status.json"
        runtime_state.write_status(path, {"status": "RUNNING"})
        self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)

    def test_no_publish_candidate_is_not_an_execution_status(self):
        with self.assertRaises(runtime_state.RuntimeStateError):
            runtime_state.validate_status_record({"status": "NO_PUBLISH_CANDIDATE"})

    def test_invalid_execution_status_is_rejected(self):
        with self.assertRaises(runtime_state.RuntimeStateError):
            runtime_state.write_status(self.root / "status.json", {"status": "UNKNOWN"})

    def test_run_id_is_unique_and_path_safe(self):
        with self.assertRaises(runtime_state.RuntimeStateError):
            runtime_state.run_directory(self.root, TEST_DATE, "../unsafe")

    def test_json_status_does_not_include_unrequested_secret_fields(self):
        run_dir = runtime_state.run_directory(self.root, TEST_DATE, "run-001")
        runtime_state.write_status(run_dir / "status.json", {"status": "RUNNING"})
        value = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
        self.assertNotIn("token", value)
        self.assertNotIn("api_key", value)


if __name__ == "__main__":
    unittest.main()
