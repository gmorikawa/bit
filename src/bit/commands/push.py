"""push command: push commits to the remote repository."""
import subprocess
import sys


def run():
    """Push commits on the current branch to its upstream remote."""
    try:
        subprocess.run(["git", "push"], check=True)
    except FileNotFoundError:
        print("error: git not found. Please install Git.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
