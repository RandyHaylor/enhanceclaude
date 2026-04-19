#!/usr/bin/env python3
"""uninstall_hook: remove any afk-mode PermissionRequest hook entries
from the user's Claude Code settings.json.

Identifies entries by the substring 'auto-deny-elevations.py' in their
hook command. Removes matching matcher entries; removes the
PermissionRequest list entirely if it becomes empty.

Usage:
  python3 uninstall_hook.py
  python3 uninstall_hook.py --settings /path/to/settings.json
"""

import argparse
import json
import sys
from pathlib import Path

HOOK_MARKER = "auto-deny-elevations.py"
DEFAULT_SETTINGS = Path.home() / ".claude" / "settings.json"


def matcher_points_at_our_hook(matcher_entry):
    for h in matcher_entry.get("hooks", []):
        cmd = h.get("command", "")
        if HOOK_MARKER in cmd:
            return True
    return False


def uninstall(settings_path):
    if not settings_path.exists():
        print(
            f"{settings_path} does not exist. Nothing to uninstall.",
            file=sys.stderr,
        )
        sys.exit(0)

    try:
        data = json.loads(settings_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Failed to read {settings_path}: {e}", file=sys.stderr)
        sys.exit(2)

    hooks = data.get("hooks", {})
    permission_request_list = hooks.get("PermissionRequest", [])

    original_count = len(permission_request_list)
    filtered = [
        entry
        for entry in permission_request_list
        if not matcher_points_at_our_hook(entry)
    ]
    removed = original_count - len(filtered)

    if removed == 0:
        print(
            f"No afk-mode PermissionRequest hook entries found in "
            f"{settings_path}. Nothing to do."
        )
        return

    if filtered:
        hooks["PermissionRequest"] = filtered
    else:
        hooks.pop("PermissionRequest", None)
        if not hooks:
            data.pop("hooks", None)

    try:
        settings_path.write_text(json.dumps(data, indent=2) + "\n")
    except OSError as e:
        print(f"Failed to write {settings_path}: {e}", file=sys.stderr)
        sys.exit(2)

    print(
        f"Removed {removed} afk-mode PermissionRequest hook "
        f"entr{'y' if removed == 1 else 'ies'} from {settings_path}."
    )
    print("Restart Claude Code for the change to take effect.")


def main():
    parser = argparse.ArgumentParser(
        prog="uninstall_hook",
        description="Unregister the afk-mode PermissionRequest hook.",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        default=DEFAULT_SETTINGS,
        help=f"Path to settings.json (default: {DEFAULT_SETTINGS}).",
    )
    args = parser.parse_args()
    uninstall(args.settings)


if __name__ == "__main__":
    main()
