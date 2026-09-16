import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from scripts.manual_runner import ManualRunnerError, run_and_display


class ManualRunnerPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.run_directory = self.root / "runtime" / "runs" / "2026-09-16" / "run-test"
        self.run_directory.mkdir(parents=True)
        self.gate1 = (
            "Run-Date: 2026-09-16\n"
            "Source-Verification: NOT_STARTED\n"
            "Human-Decision: PENDING\n"
            "## Measurement\n"
            "Machine elapsed: 1 second\n"
        )

    def tearDown(self):
        self.temporary.cleanup()

    def result(self, status="GATE1_READY", run_directory=None):
        return SimpleNamespace(
            execution_status=status,
            run_directory=str(run_directory if run_directory is not None else self.run_directory),
        )

    def test_gate1_ready_displays_gate1_verbatim_and_stops(self):
        gate1_path = self.run_directory / "gate1.md"
        gate1_path.write_text(self.gate1, encoding="utf-8")
        (self.run_directory / "raw-output.txt").write_text("must not be displayed", encoding="utf-8")
        runner = Mock(return_value=self.result())
        output = io.StringIO()

        code = run_and_display("2026-09-16", phase1_runner=runner, output=output)

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), self.gate1)
        self.assertIn("Human-Decision: PENDING", output.getvalue())
        self.assertNotIn("must not be displayed", output.getvalue())
        runner.assert_called_once()

    def test_non_gate1_status_does_not_display_body(self):
        (self.run_directory / "gate1.md").write_text("should not be read", encoding="utf-8")
        runner = Mock(return_value=self.result(status="BRIEF_NOT_READY"))
        output = io.StringIO()

        with self.assertRaisesRegex(ManualRunnerError, "GATE1_READY"):
            run_and_display("2026-09-16", phase1_runner=runner, output=output)

        self.assertEqual(output.getvalue(), "")
        runner.assert_called_once()

    def test_missing_gate1_fails_closed(self):
        runner = Mock(return_value=self.result())
        output = io.StringIO()

        with self.assertRaisesRegex(ManualRunnerError, "missing"):
            run_and_display("2026-09-16", phase1_runner=runner, output=output)

        self.assertEqual(output.getvalue(), "")
        runner.assert_called_once()

    def test_invalid_utf8_fails_closed(self):
        (self.run_directory / "gate1.md").write_bytes(b"valid prefix\xff")
        runner = Mock(return_value=self.result())
        output = io.StringIO()

        with self.assertRaisesRegex(ManualRunnerError, "UTF-8"):
            run_and_display("2026-09-16", phase1_runner=runner, output=output)

        self.assertEqual(output.getvalue(), "")
        runner.assert_called_once()

    def test_missing_run_directory_fails_closed(self):
        runner = Mock(return_value=self.result(run_directory=None))
        runner.return_value.run_directory = None
        output = io.StringIO()

        with self.assertRaisesRegex(ManualRunnerError, "run_directory"):
            run_and_display("2026-09-16", phase1_runner=runner, output=output)

        self.assertEqual(output.getvalue(), "")
        runner.assert_called_once()

    def test_direct_cli_help_has_no_scripts_import_error(self):
        script = Path(__file__).parents[1] / "scripts" / "manual_runner.py"
        completed = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=script.parents[1],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("usage:", completed.stdout)
        self.assertNotIn("ModuleNotFoundError: No module named 'scripts'", completed.stderr)


if __name__ == "__main__":
    unittest.main()
