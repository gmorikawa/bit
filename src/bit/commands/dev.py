"""dev command: change git credentials for the local or global repository.

If the current working directory is inside a git repository, credentials
are written to the *local* git config.  Otherwise they are written to the
*global* git config (~/.gitconfig).
"""
import subprocess
import sys


def _is_git_repo() -> bool:
    """Return True when the current directory is inside a git repository."""
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def _set_git_config(scope: str, name: str, email: str) -> None:
    """Set user.name and user.email in the given git config scope."""
    subprocess.run(["git", "config", scope, "user.name", name], check=True)
    subprocess.run(["git", "config", scope, "user.email", email], check=True)


def run():
    """Interactively set git user.name and user.email."""
    name = input("Enter git user name: ").strip()
    if not name:
        print("error: name is required.", file=sys.stderr)
        sys.exit(1)

    email = input("Enter git user email: ").strip()
    if not email:
        print("error: email is required.", file=sys.stderr)
        sys.exit(1)

    try:
        if _is_git_repo():
            _set_git_config("--local", name, email)
            print(f"Updated local git config: user.name='{name}', user.email='{email}'")
        else:
            _set_git_config("--global", name, email)
            print(f"Updated global git config: user.name='{name}', user.email='{email}'")
    except FileNotFoundError:
        print("error: git not found. Please install Git.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"error: git config failed (exit code {exc.returncode}).", file=sys.stderr)
        sys.exit(exc.returncode)
