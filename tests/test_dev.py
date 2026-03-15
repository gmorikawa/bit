"""Tests for the dev command."""
import pytest
from unittest.mock import patch, call

from bit.commands.dev import _is_git_repo, run


class TestIsGitRepo:
    def test_returns_true_inside_repo(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "true\n"
            assert _is_git_repo() is True

    def test_returns_false_outside_repo(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 128
            mock_run.return_value.stdout = ""
            assert _is_git_repo() is False


class TestRun:
    def test_missing_name_exits(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "")
        with pytest.raises(SystemExit) as exc_info:
            run()
        assert exc_info.value.code == 1

    def test_missing_email_exits(self, monkeypatch):
        inputs = iter(["Alice", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with pytest.raises(SystemExit) as exc_info:
            run()
        assert exc_info.value.code == 1

    def test_sets_local_config_inside_repo(self, monkeypatch, capsys):
        inputs = iter(["Alice", "alice@example.com"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with patch("bit.commands.dev._is_git_repo", return_value=True), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            run()
            calls = mock_run.call_args_list
            assert call(["git", "config", "--local", "user.name", "Alice"], check=True) in calls
            assert call(["git", "config", "--local", "user.email", "alice@example.com"], check=True) in calls
        captured = capsys.readouterr()
        assert "local" in captured.out

    def test_sets_global_config_outside_repo(self, monkeypatch, capsys):
        inputs = iter(["Bob", "bob@example.com"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with patch("bit.commands.dev._is_git_repo", return_value=False), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            run()
            calls = mock_run.call_args_list
            assert call(["git", "config", "--global", "user.name", "Bob"], check=True) in calls
            assert call(["git", "config", "--global", "user.email", "bob@example.com"], check=True) in calls
        captured = capsys.readouterr()
        assert "global" in captured.out
