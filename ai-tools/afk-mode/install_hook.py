#!/usr/bin/env python3
"""install_hook: idempotently register the afk-mode PermissionRequest
hook in the user's Claude Code settings.json.

Adds an entry under hooks.PermissionRequest whose command invokes
auto-deny-elevations.py sitting next to this script. Safe to run
multiple times — existing entries pointing at the same script are
detected and left alone.

Usage:
  python3 install_hook.py
  python3 install_hook.py --settings /path/to/settings.json   # override

Exits 0 on success / already-installed, 1 on user error, 2 on I/O error.
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
HOOK_SCRIPT = SCRIPT_DIR / "auto-deny-elevations.py"
HOOK_MARKER = "auto-deny-elevations.py"  # substring used to detect our hook
DEFAULT_SETTINGS = Path.home() / ".claude" / "settings.json"


def build_hook_entry():
    """Return the JSON structure for our matcher entry."""
    # Use $HOME for portability on Linux/macOS; Windows shell will need
    # %USERPROFILE% if it doesn't expand $HOME, but Claude Code's hook
    # runner on Windows tolerates $HOME in practice.
    command = f'python3 "$HOME"/.claude/skills/afk-mode/auto-deny-elevations.py'
    return {
        "matcher": "*",
        "hooks": [
            {
                "type": "command",
                "command": command,
            }
        ],
    }


def matcher_points_at_our_hook(matcher_entry):
    for h in matcher_entry.get("hooks", []):
        cmd = h.get("command", "")
        if HOOK_MARKER in cmd:
            return True
    return False


def install(settings_path):
    if not HOOK_SCRIPT.exists():
        print(
            f"Hook script missing at {HOOK_SCRIPT}. Aborting install.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if settings_path.exists():
            data = json.loads(settings_path.read_text())
        else:
            data = {}
    except (json.JSONDecodeError, OSError) as e:
        print(f"Failed to read {settings_path}: {e}", file=sys.stderr)
        sys.exit(2)

    hooks = data.setdefault("hooks", {})
    permission_request_list = hooks.setdefault("PermissionRequest", [])

    for entry in permission_request_list:
        if matcher_points_at_our_hook(entry):
            print(
                f"afk-mode PermissionRequest hook already registered in "
                f"{settings_path}. No changes made."
            )
            return

    permission_request_list.append(build_hook_entry())

    try:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(data, indent=2) + "\n")
    except OSError as e:
        print(f"Failed to write {settings_path}: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"Registered afk-mode PermissionRequest hook in {settings_path}.")
    print("Restart Claude Code for the hook to take effect.")


def main():
    parser = argparse.ArgumentParser(
        prog="install_hook",
        description="Register the afk-mode PermissionRequest hook.",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        default=DEFAULT_SETTINGS,
        help=f"Path to settings.json (default: {DEFAULT_SETTINGS}).",
    )
    args = parser.parse_args()
    install(args.settings)


if __name__ == "__main__":
    main()
