# Claude Code - AFK Mode

**Type:** skill | **Version:** 1.0.0 | **OS:** linux, macos, windows

Toggle afk mode by simply typing /afk - progress blocking elevation prompts will be auto-denied and agent will be told to continue! User-invocable skill + PermissionRequest auto-deny hook for Claude Code. Lets the user flip a project into an 'away' state so tool calls that would normally stall on a permission dialog get auto-denied with a directive message instead — the agent continues what it can without silently hanging.

## Tags
claude-code, hook, permission-request, away-mode, automation, agent-workflow

## Overview
A self-contained skill folder that installs globally at ~/.claude/skills/afk-mode/. A PermissionRequest hook script auto-denies tool calls that would trigger a user-facing permission dialog, but only in projects that have opted in via a local config file. When a call is denied, the agent receives a structured message telling it to continue within existing permissions, not mark steps blocked/done, not invent new work, and summarize when stuck. Includes `/afk-mode` toggle semantics (auto-installs and enables on first use), per-project scope (no accidental cross-project blocking), cross-platform invocation (no symlinks or PATH munging), and idempotent hook install/uninstall scripts that edit ~/.claude/settings.json safely. The hook honors merged permissions.allow rules from user/project/local settings so approved operations still pass through.

## Try These Prompts
- /afk-mode
- Set my status to away — I'm stepping out for a meeting.
- I'm back — disable afk on this project.
- Install the afk-mode hook globally so it works in every project.
- Remove afk-mode from this project entirely.
- Add a new 'presenting' mode with a message telling the agent I'm screen-sharing.

## Use Cases
- Preventing agents from silently stalling on permission dialogs when the user is AFK
- Long-running autonomous runs where the user can't respond to elevation prompts
- Focus/deep-work sessions where dialog interruptions are unwanted
- Screen-sharing or presentation scenarios where surprise dialogs are disruptive
- Debugging sessions where the user wants every elevation surfaced as a structured agent message instead of a modal

## Additional Requirements
Requires Claude Code CLI (not the desktop/web app) — uses PermissionRequest hooks registered via ~/.claude/settings.json.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
