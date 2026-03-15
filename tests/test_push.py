"""Tests for the push command."""
import pytest
from unittest.mock import patch

from bit.commands.push import run


class TestRun:
    def test_calls_git_push(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            run()
            mock_run.assert_called_once_with(["git", "push"], check=True)

    def test_git_not_found_exits(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit) as exc_info:
                run()
            assert exc_info.value.code == 1

    def test_git_push_failure_exits_with_returncode(self):
        import subprocess
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(128, "git push")
            with pytest.raises(SystemExit) as exc_info:
                run()
            assert exc_info.value.code == 128
