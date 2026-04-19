# afk-mode setup and reference

Full installation, configuration, and troubleshooting reference for the
afk-mode system. This document is the canonical source. The `afk-mode`
skill is the user-facing interface; this file is what the skill consults
when the user asks setup or troubleshooting questions.

## What afk-mode is

A PermissionRequest hook that auto-denies any tool call which would
trigger a user-facing permission dialog in Claude Code — but only in
projects that have opted in by creating a local config file.

Projects without a local config are unaffected; the hook exits silently
in those projects and permission dialogs behave normally.

When the hook denies, the agent receives a message explaining why and
what it should do (continue within its existing permissions, don't mark
steps done/blocked, don't invent new work, summarize when done).

## File layout

- `~/.claude/hooks/auto-deny-elevations.py` — hook script (global).
- `~/.claude/hooks/afk-ctl.py`, `afk-install.py` — CLI scripts.
- `~/.local/bin/afk-ctl`, `afk-install` — symlinks for PATH access.
- `~/.claude/settings.json` — registers the hook.
- `<project>/.claude/hooks/auto-deny-settings.json` — per-project config.

## Opt-in flow for a project

From the project root:

    afk-install
    afk-ctl enable --mode away      # when you want it active

## Modes

The `mode` field in the config selects which message the agent receives
on denial. Messages are defined in the `messages` object; keys are mode
names, values are templates. `{tool_name}` is substituted at runtime.

Ships with two modes:

- `away` — Verbose, directive. Tells the agent to continue what it can,
  not mark steps done/blocked, not invent work, and summarize when done.
- `default` — Terser. Explains the denial is a user config choice,
  retries won't help, either change approach or surface the missing
  permission rule.

Add new modes by editing `auto-deny-settings.json` directly — the CLI
scripts don't create new modes, only switch between existing ones. Agent
should ask the user what directive message to use and then add the entry.

## Permission-rule awareness

The hook reads `permissions.allow` arrays from user, project, and local
settings files and does not deny tool calls that match an allow rule.
This prevents over-blocking of operations the user has already approved
in their normal permission configuration.

The matcher is a heuristic port of Claude Code's real rule engine —
handles bare tool names, `Tool(specifier)`, `Tool(prefix *)`, and
`Tool(domain:...)` patterns. Edge cases in wildcard syntax, sandbox
interactions, and managed-settings precedence may cause ~5% divergence
from Claude Code's actual permission decisions.

## Disabling vs uninstalling in a project

- **Disable** (`afk-ctl disable`) — keeps the config file, sets
  `enabled: false`. Hook no-ops in this project but state is preserved
  for quick re-enable.
- **Uninstall** (`afk-install remove`) — deletes the config file. Hook
  no-ops (same as a project that never had it installed).

## Applying changes

The script reads the config on every hook fire, so edits take effect on
the next tool call. No Claude Code restart needed for config changes.
Restart IS needed for changes to `~/.claude/settings.json` or
`auto-deny-elevations.py`.

## Troubleshooting

**Agent reports seeing a denial but no explanatory text.**
Different Claude Code versions use `message` vs `reason` as the field
name inside `decision`. Edit `auto-deny-elevations.py` and swap
`"message"` to `"reason"` in the JSON output. Current SDK reference
uses `message`.

**Hook isn't firing.**
Run `/hooks` inside Claude Code and confirm the handler is listed under
PermissionRequest. If missing, check `~/.claude/settings.json` syntax
and restart Claude Code.

**`afk-ctl: command not found`.**
The symlink to `~/.local/bin/afk-ctl` is missing or `~/.local/bin` is
not on PATH. Run the symlink commands from the setup steps, then check
`echo $PATH`.

**Config changes aren't picked up.**
The script re-reads config on every fire, so changes should take effect
on the next tool call. If not, verify the JSON is valid — malformed
JSON makes the script no-op silently. Test with
`python3 -m json.tool .claude/hooks/auto-deny-settings.json`.

**Hook blocking operations you meant to approve.**
Add the rule to your `permissions.allow` in `~/.claude/settings.json`
or project settings. The hook honors allow rules and passes those calls
through.

**Multiple PermissionRequest hooks registered.**
Deny takes precedence over ask over allow. This hook's deny will win
regardless of other handlers.

## Hook output caps and limitations

- Hook output (message/additionalContext) is capped at 10,000 characters.
  Current messages are well under this limit.
- This hook only controls PermissionRequest dialogs. It does not override
  `permissions.deny` rules (those block before the hook fires) or
  interact with sandbox policy.
- The hook denies each elevation individually. If the LLM tries a
  different approach that also triggers an elevation, it gets denied
  again with the same message. If you want "one-deny-then-stop"
  semantics, state-tracking would need to be added to the script.
