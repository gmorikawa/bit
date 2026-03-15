"""Tests for the genkey command."""
import os
import pytest
from unittest.mock import patch, mock_open

from bit.commands.genkey import run


class TestRun:
    def test_ssh_keygen_called_with_correct_args(self, monkeypatch, tmp_path, capsys):
        key_path = str(tmp_path / "id_ed25519")
        pub_key_path = key_path + ".pub"

        inputs = iter([key_path, "test@example.com"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        def fake_run(cmd, check):
            # Simulate ssh-keygen by creating the public key file
            with open(pub_key_path, "w") as fh:
                fh.write("ssh-ed25519 AAAA... test@example.com\n")

        with patch("subprocess.run", side_effect=fake_run):
            run()

        captured = capsys.readouterr()
        assert "SSH key created" in captured.out
        assert key_path in captured.out

    def test_uses_default_path_when_blank(self, monkeypatch, capsys):
        inputs = iter(["", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with patch("subprocess.run") as mock_run, \
             patch("os.makedirs"), \
             patch("os.path.exists", return_value=False):
            mock_run.return_value.returncode = 0
            run()
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "ssh-keygen"
            assert "id_ed25519" in cmd[cmd.index("-f") + 1]

    def test_ssh_keygen_not_found_exits(self, monkeypatch):
        inputs = iter(["/tmp/test_key", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with patch("subprocess.run", side_effect=FileNotFoundError), \
             patch("os.makedirs"):
            with pytest.raises(SystemExit) as exc_info:
                run()
            assert exc_info.value.code == 1
