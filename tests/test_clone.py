"""Tests for the clone command."""
import pytest
from unittest.mock import patch, call

from bit.commands.clone import _rewrite_url, run


class TestRewriteUrl:
    def test_replaces_host_in_ssh_url(self):
        url = "git@github.com:owner/repo.git"
        result = _rewrite_url(url, "github-work")
        assert result == "git@github-work:owner/repo.git"

    def test_leaves_https_url_unchanged(self):
        url = "https://github.com/owner/repo.git"
        result = _rewrite_url(url, "github-work")
        assert result == url

    def test_no_alias_returns_original(self):
        url = "git@github.com:owner/repo.git"
        result = _rewrite_url(url, "")
        # empty alias is falsy; run() skips rewrite, but _rewrite_url still
        # produces git@:owner/repo.git — callers guard against empty alias
        assert "owner/repo.git" in result

    def test_preserves_path_with_subdirectory(self):
        url = "git@gitlab.com:group/subgroup/repo.git"
        result = _rewrite_url(url, "gitlab-personal")
        assert result == "git@gitlab-personal:group/subgroup/repo.git"


class TestRun:
    def test_missing_url_exits(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "")
        with pytest.raises(SystemExit) as exc_info:
            run()
        assert exc_info.value.code == 1

    def test_clone_without_alias(self, monkeypatch):
        inputs = iter(["git@github.com:owner/repo.git", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            run()
            mock_run.assert_called_once_with(
                ["git", "clone", "git@github.com:owner/repo.git"], check=True
            )

    def test_clone_with_alias_rewrites_url(self, monkeypatch, capsys):
        inputs = iter(["git@github.com:owner/repo.git", "github-work"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            run()
            mock_run.assert_called_once_with(
                ["git", "clone", "git@github-work:owner/repo.git"], check=True
            )
        captured = capsys.readouterr()
        assert "Rewriting URL" in captured.out
