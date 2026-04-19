#!/usr/bin/env python3
"""PermissionRequest hook: auto-deny tool calls that would trigger a user
permission dialog, but only in projects that have a local config at
.claude/hooks/auto-deny-settings.json in cwd. Projects without a local
config are unaffected — the hook no-ops."""

import json
import sys
from pathlib import Path

AFK_SETTINGS = Path.cwd() / ".claude/hooks/auto-deny-settings.json"

SETTINGS_FILES = [
    Path.home() / ".claude/settings.json",
    Path.cwd() / ".claude/settings.json",
    Path.cwd() / ".claude/settings.local.json",
]

FALLBACK_MESSAGE = (
    "AUTO-DENIED by the user's PermissionRequest hook. The tool call "
    "({tool_name}) triggered a permission dialog. This is the user's "
    "configuration, not a safety block. Retrying will not help."
)


def load_afk_config():
    try:
        return json.loads(AFK_SETTINGS.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def load_permission_rules():
    allow = []
    for f in SETTINGS_FILES:
        try:
            data = json.loads(f.read_text())
            allow += data.get("permissions", {}).get("allow", [])
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            continue
    return allow


def matches_allow_rule(tool_name, tool_input, rule):
    if rule == tool_name:
        return True
    if not rule.startswith(f"{tool_name}(") or not rule.endswith(")"):
        return False

    specifier = rule[len(tool_name) + 1 : -1]

    if specifier.startswith("domain:"):
        domain = specifier.split(":", 1)[1]
        url = tool_input.get("url", "") or ""
        return domain in url

    target = (
        tool_input.get("command")
        or tool_input.get("file_path")
        or tool_input.get("path")
        or ""
    )

    if "*" in specifier:
        prefix = specifier.split("*", 1)[0]
        return target.startswith(prefix)

    return target == specifier


def is_allowed(tool_name, tool_input, rules):
    return any(
        matches_allow_rule(tool_name, tool_input, r) for r in rules
    )


def resolve_message(config, tool_name):
    mode = config.get("mode", "default")
    messages = config.get("messages", {})
    template = (
        messages.get(mode)
        or messages.get("default")
        or FALLBACK_MESSAGE
    )
    return template.format(tool_name=tool_name)


def main():
    payload = json.load(sys.stdin)
    tool_name = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input", {}) or {}

    config = load_afk_config()

    if config is None:
        sys.exit(0)

    if not config.get("enabled", True):
        sys.exit(0)

    allow_rules = load_permission_rules()
    if is_allowed(tool_name, tool_input, allow_rules):
        sys.exit(0)

    json.dump(
        {"hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "deny",
                "message": resolve_message(config, tool_name),
            },
        }},
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
