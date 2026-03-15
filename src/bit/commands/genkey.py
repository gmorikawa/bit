"""genkey command: create a new SSH key."""
import os
import subprocess
import sys


def run():
    """Interactively create a new SSH key pair."""
    key_path = input("Enter path for the new SSH key [~/.ssh/id_ed25519]: ").strip()
    if not key_path:
        key_path = os.path.expanduser("~/.ssh/id_ed25519")
    else:
        key_path = os.path.expanduser(key_path)

    comment = input("Enter a comment/label for the key (e.g. your email): ").strip()

    key_dir = os.path.dirname(key_path)
    os.makedirs(key_dir, exist_ok=True)

    cmd = ["ssh-keygen", "-t", "ed25519", "-f", key_path]
    if comment:
        cmd += ["-C", comment]

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("error: ssh-keygen not found. Please install OpenSSH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"error: ssh-keygen failed (exit code {exc.returncode}).", file=sys.stderr)
        sys.exit(exc.returncode)

    pub_key_path = key_path + ".pub"
    print(f"\nSSH key created: {key_path}")
    print(f"Public key:      {pub_key_path}")

    if os.path.exists(pub_key_path):
        with open(pub_key_path) as fh:
            print(f"\nPublic key content:\n{fh.read()}")
