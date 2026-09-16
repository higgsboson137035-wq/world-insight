import json
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from scripts.codex_runner import build_command, run_codex


class CodexRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.workdir = Path(self.temp_dir.name)
        self.executable = "/opt/homebrew/bin/codex"
        self.model = "unit-test-model"

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_with(self, runner, prompt="PRIVATE PROMPT SHOULD NOT BE STORED"):
        return run_codex(
            prompt,
            executable=self.executable,
            working_directory=self.workdir,
            model=self.model,
            timeout_seconds=10,
            subprocess_run=runner,
        )

    def test_safe_command_construction(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertEqual(
            command,
            [
                self.executable,
                "exec",
                "-C",
                str(self.workdir),
                "-s",
                "read-only",
                "-m",
                self.model,
                "--ephemeral",
            ],
        )

    def test_prompt_is_sent_through_stdin(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "out", ""))
        prompt = "PROMPT_SENT_ONLY_AS_INPUT"
        self.run_with(runner, prompt)
        self.assertEqual(runner.call_args.kwargs["input"], prompt)

    def test_shell_is_false(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "", ""))
        self.run_with(runner)
        self.assertIs(runner.call_args.kwargs["shell"], False)

    def test_working_directory_validation(self):
        runner = Mock()
        result = run_codex(
            "prompt",
            executable=self.executable,
            working_directory=self.workdir / "missing",
            model=self.model,
            timeout_seconds=10,
            subprocess_run=runner,
        )
        self.assertEqual(result.status, "INVALID_CONFIGURATION")
        runner.assert_not_called()

    def test_invalid_timeout_is_rejected_before_execution(self):
        runner = Mock()
        result = run_codex(
            "prompt",
            executable=self.executable,
            working_directory=self.workdir,
            model=self.model,
            timeout_seconds=0,
            subprocess_run=runner,
        )
        self.assertEqual(result.status, "INVALID_CONFIGURATION")
        runner.assert_not_called()

    def test_zero_exit_is_success(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "out", ""))
        result = self.run_with(runner)
        self.assertEqual((result.status, result.success, result.exit_code), ("SUCCESS", True, 0))

    def test_nonzero_exit_is_failure(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 7, "out", "err"))
        result = self.run_with(runner)
        self.assertEqual((result.status, result.success, result.exit_code), ("CODEX_NONZERO_EXIT", False, 7))

    def test_stderr_alone_does_not_fail(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "out", "diagnostic"))
        result = self.run_with(runner)
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.stderr, "diagnostic")

    def test_timeout_preserves_partial_streams(self):
        runner = Mock(
            side_effect=subprocess.TimeoutExpired(
                [self.executable, "exec"], 10, output="partial out", stderr="partial err"
            )
        )
        result = self.run_with(runner)
        self.assertEqual(result.status, "TIMEOUT")
        self.assertIsNone(result.exit_code)
        self.assertEqual((result.stdout, result.stderr), ("partial out", "partial err"))

    def test_missing_executable(self):
        result = run_codex(
            "prompt",
            executable=str(self.workdir / "does-not-exist"),
            working_directory=self.workdir,
            model=self.model,
            timeout_seconds=10,
        )
        self.assertEqual(result.status, "EXECUTABLE_NOT_FOUND")
        self.assertFalse(result.success)

    def test_unexpected_exception_is_sanitized(self):
        runner = Mock(side_effect=RuntimeError("secret-token-must-not-leak"))
        result = self.run_with(runner)
        serialized = json.dumps(result.as_dict())
        self.assertEqual(result.status, "RUNNER_ERROR")
        self.assertNotIn("secret-token", serialized)

    def test_stdout_and_stderr_remain_separate(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "STDOUT", "STDERR"))
        result = self.run_with(runner)
        self.assertEqual(result.stdout, "STDOUT")
        self.assertEqual(result.stderr, "STDERR")

    def test_result_does_not_contain_prompt(self):
        prompt = "UNIQUE_PROMPT_VALUE"
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "output", ""))
        result = self.run_with(runner, prompt)
        serialized = json.dumps(result.as_dict())
        self.assertNotIn("prompt", result.as_dict())
        self.assertNotIn(prompt, serialized)

    def test_command_representation_does_not_contain_prompt(self):
        prompt = "UNIQUE_COMMAND_PROMPT"
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertNotIn(prompt, command)

    def test_explicit_model_is_included(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertEqual(command[command.index("-m") + 1], self.model)

    def test_missing_model_uses_cli_account_default(self):
        command = build_command(self.executable, self.workdir).as_list()
        self.assertNotIn("-m", command)
        self.assertNotIn("gpt-5", command)

    def test_missing_model_is_passed_to_runner_without_model_override(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "out", ""))
        result = run_codex(
            "prompt",
            executable=self.executable,
            working_directory=self.workdir,
            timeout_seconds=10,
            subprocess_run=runner,
        )
        self.assertEqual(result.status, "SUCCESS")
        self.assertNotIn("-m", runner.call_args.args[0])

    def test_read_only_sandbox_is_included(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertEqual(command[command.index("-s") + 1], "read-only")

    def test_obsolete_approval_argument_is_not_included(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertNotIn("-a", command)
        self.assertNotIn("--ask-for-approval", command)
        self.assertNotIn("--approve-for-me", command)

    def test_ephemeral_is_included(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertIn("--ephemeral", command)

    def test_web_search_option_is_not_added(self):
        command = build_command(self.executable, self.workdir, self.model).as_list()
        self.assertNotIn("--search", command)

    def test_tests_inject_subprocess_and_do_not_invoke_codex(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "", ""))
        result = self.run_with(runner)
        runner.assert_called_once()
        self.assertEqual(result.status, "SUCCESS")

    def test_machine_readable_result(self):
        runner = Mock(return_value=subprocess.CompletedProcess([], 0, "", ""))
        result = self.run_with(runner)
        payload = result.as_dict()
        json.dumps(payload)
        self.assertIn("elapsed_seconds", payload)


if __name__ == "__main__":
    unittest.main()
