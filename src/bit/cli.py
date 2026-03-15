"""CLI entry point for bit."""
import sys

from bit.commands.genkey import run as genkey_run
from bit.commands.clone import run as clone_run
from bit.commands.push import run as push_run
from bit.commands.dev import run as dev_run

COMMANDS = {
    "genkey": genkey_run,
    "clone": clone_run,
    "push": push_run,
    "dev": dev_run,
}

USAGE = """\
usage: bit <command>

Available commands:
  genkey    Create a new SSH key
  clone     Clone a git remote repository
  push      Push commits to the repository
  dev       Change git credentials for the local (or global) repository
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE, end="")
        sys.exit(1)

    command = sys.argv[1]

    if command not in COMMANDS:
        print(f"bit: unknown command '{command}'", file=sys.stderr)
        print(USAGE, end="", file=sys.stderr)
        sys.exit(1)

    COMMANDS[command]()
