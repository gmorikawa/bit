"""Tests for the CLI entry point."""
import sys
import pytest

from bit.cli import main, COMMANDS, USAGE


def test_known_commands_are_registered():
    assert set(COMMANDS.keys()) == {"genkey", "clone", "push", "dev"}


def test_no_args_prints_usage_and_exits(capsys):
    sys.argv = ["bit"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "usage:" in captured.out


def test_unknown_command_exits_with_error(capsys):
    sys.argv = ["bit", "notacommand"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "unknown command" in captured.err
