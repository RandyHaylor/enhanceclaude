#!/usr/bin/env python3
"""afk-ctl: control the project-local afk-mode config in cwd.

Usage:
  afk-ctl status
  afk-ctl enable [--mode MODE]
  afk-ctl disable
  afk-ctl mode MODE
  afk-ctl list-modes

Exits 0 on success, 1 on user error, 2 on I/O error.
"""

import argparse
import json
import sys
from pathlib import Path

CONFIG_PATH = Path.cwd() / ".claude/hooks/auto-deny-settings.json"


def die_missing():
    print(
        "afk-mode not installed in this project. "
        "Run `afk-install` to set it up.",
        file=sys.stderr,
    )
    sys.exit(1)


def load():
    if not CONFIG_PATH.exists():
        die_missing()
    try:
        return json.loads(CONFIG_PATH.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Failed to read {CONFIG_PATH}: {e}", file=sys.stderr)
        sys.exit(2)


def save(config):
    try:
        CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")
    except OSError as e:
        print(f"Failed to write {CONFIG_PATH}: {e}", file=sys.stderr)
        sys.exit(2)


def cmd_status(_args):
    config = load()
    enabled = config.get("enabled", False)
    mode = config.get("mode", "default")
    state = "ENABLED" if enabled else "disabled"
    print(f"afk-mode: {state}, mode={mode}")


def cmd_enable(args):
    config = load()
    config["enabled"] = True
    if args.mode:
        if args.mode not in config.get("messages", {}):
            print(
                f"Warning: mode '{args.mode}' is not defined in messages. "
                f"Agent will receive the 'default' message instead.",
                file=sys.stderr,
            )
        config["mode"] = args.mode
    save(config)
    cmd_status(None)


def cmd_disable(_args):
    config = load()
    config["enabled"] = False
    save(config)
    cmd_status(None)


def cmd_mode(args):
    config = load()
    if args.mode_name not in config.get("messages", {}):
        print(
            f"Warning: mode '{args.mode_name}' is not defined in messages. "
            f"Agent will receive the 'default' message instead.",
            file=sys.stderr,
        )
    config["mode"] = args.mode_name
    save(config)
    cmd_status(None)


def cmd_list_modes(_args):
    config = load()
    modes = list(config.get("messages", {}).keys())
    active = config.get("mode", "default")
    for m in modes:
        marker = " (active)" if m == active else ""
        print(f"{m}{marker}")


def main():
    parser = argparse.ArgumentParser(
        prog="afk-ctl",
        description="Control afk-mode for the current project.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show current afk state and mode.")

    p_en = sub.add_parser("enable", help="Enable afk-mode.")
    p_en.add_argument(
        "--mode",
        help="Also set the mode (e.g. 'away', 'default').",
    )

    sub.add_parser("disable", help="Disable afk-mode (mode preserved).")

    p_mode = sub.add_parser(
        "mode",
        help="Change active mode without toggling enable.",
    )
    p_mode.add_argument("mode_name")

    sub.add_parser("list-modes", help="List modes defined in this config.")

    args = parser.parse_args()

    dispatch = {
        "status": cmd_status,
        "enable": cmd_enable,
        "disable": cmd_disable,
        "mode": cmd_mode,
        "list-modes": cmd_list_modes,
    }
    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
