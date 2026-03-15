"""clone command: clone a git remote repository.

When using multiple SSH accounts the remote URL sometimes needs to be
rewritten so that the correct Host alias defined in ~/.ssh/config is used.
This command asks for the repository URL and an optional SSH host alias,
rewrites the URL if necessary, and then runs `git clone`.
"""
import re
import subprocess
import sys


# Matches the host part of an SSH git URL, e.g.:
#   git@github.com:owner/repo.git  -> host = "github.com"
_SSH_URL_RE = re.compile(r"^git@(?P<host>[^:]+):(?P<path>.+)$")


def _rewrite_url(url: str, host_alias: str) -> str:
    """Replace the host in an SSH git URL with *host_alias*."""
    match = _SSH_URL_RE.match(url)
    if match:
        return f"git@{host_alias}:{match.group('path')}"
    return url


def run():
    """Clone a remote git repository, optionally rewriting the SSH host."""
    repo_url = input("Enter the repository URL: ").strip()
    if not repo_url:
        print("error: repository URL is required.", file=sys.stderr)
        sys.exit(1)

    host_alias = input(
        "Enter SSH host alias to use (leave blank to keep the original host): "
    ).strip()

    clone_url = _rewrite_url(repo_url, host_alias) if host_alias else repo_url

    if clone_url != repo_url:
        print(f"Rewriting URL: {repo_url} -> {clone_url}")

    try:
        subprocess.run(["git", "clone", clone_url], check=True)
    except FileNotFoundError:
        print("error: git not found. Please install Git.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
