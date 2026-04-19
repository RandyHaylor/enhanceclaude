#!/usr/bin/env python3
"""afk-install: create or remove the project-local afk-mode config.

Usage:
  afk-install           # create config in cwd (disabled by default)
  afk-install --force   # overwrite existing config
  afk-install remove    # delete the config from cwd
"""

import argparse
import json
import sys
from pathlib import Path

CONFIG_DIR = Path.cwd() / ".claude/hooks"
CONFIG_PATH = CONFIG_DIR / "auto-deny-settings.json"

DEFAULT_CONFIG = {
    "enabled": False,
    "mode": "away",
    "messages": {
        "away": (
            "AUTO-DENIED: the user is away right now and cannot respond "
            "to permission dialogs. This is not a safety block — it is "
            "the user's configured away-mode. The tool call ({tool_name}) "
            "required a permission elevation that only the user can "
            "approve.\n\n"
            "How to proceed:\n"
            "- Continue working on as much of the user's last request "
            "as you CAN complete without tools that require elevation.\n"
            "- Do NOT mark any step as blocked, done, or skipped — the "
            "user will review progress on return.\n"
            "- Do NOT invent new work, scope, or subtasks the user did "
            "not ask for.\n"
            "- Do NOT retry the same elevation — it will be denied again.\n"
            "- When you have done everything you can without elevated "
            "permissions, stop and write a short summary of: (1) what "
            "you completed, (2) what specifically you could not do and "
            "why (i.e., which tool call was auto-denied and what it was "
            "trying to achieve), (3) which permission rule would need "
            "to be added if the user wants this to run next time."
        ),
        "default": (
            "AUTO-DENIED by the user's PermissionRequest hook. The tool "
            "call ({tool_name}) triggered a permission dialog, which "
            "means it does not match the user's allow rules. This is "
            "the user's configuration choice, not a safety block. "
            "Retrying will not help — either change approach or tell "
            "the user which rule they'd need to add."
        ),
    },
}


def cmd_create(args):
    if CONFIG_PATH.exists() and not args.force:
        print(
            f"Config already exists at {CONFIG_PATH}. "
            f"Use --force to overwrite, or `afk-ctl status` to inspect.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n")
    except OSError as e:
        print(f"Failed to create config: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"Created {CONFIG_PATH}")
    print("afk-mode is installed but DISABLED in this project.")
    print("Run `afk-ctl enable` to activate.")


def cmd_remove(_args):
    if not CONFIG_PATH.exists():
        print(
            "No afk-mode config in this project; nothing to remove.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        CONFIG_PATH.unlink()
    except OSError as e:
        print(f"Failed to remove config: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"Removed {CONFIG_PATH}")
    print("afk-mode is no longer active in this project.")


def main():
    parser = argparse.ArgumentParser(
        prog="afk-install",
        description="Install or remove afk-mode config in the current project.",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser(
        "create",
        help="Create project-local config (default action).",
    )
    p_create.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing config.",
    )

    sub.add_parser("remove", help="Delete the project-local config.")

    args = parser.parse_args()

    if args.cmd is None:
        args.cmd = "create"
        args.force = False

    dispatch = {
        "create": cmd_create,
        "remove": cmd_remove,
    }
    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
