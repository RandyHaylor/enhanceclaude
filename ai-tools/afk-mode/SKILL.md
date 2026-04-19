---
name: afk-mode
description: Manage the user's AFK (away-from-keyboard) status for the PermissionRequest auto-deny hook. Use when the user says they're stepping away, coming back, switching to focus/presenting/debugging mode, or asks to change their Claude Code permission-dialog behavior. Also use when the user asks to set up, configure, or troubleshoot the afk-mode system.
user-invocable: true
allowed-tools: Read, Edit, Bash, Write
---

# afk-mode

This skill manages the auto-deny permission-elevation hook installed at the user scope. All scripts (hook + CLIs + install/uninstall) live inside this skill folder at `~/.claude/skills/afk-mode/`. The hook is registered globally in `~/.claude/settings.json` via `install_hook.py`. Each project that wants afk-mode has its own config at `.claude/hooks/auto-deny-settings.json` — no config means afk-mode is inactive in that project.

## Central install / uninstall of the hook itself

If the hook isn't registered in `~/.claude/settings.json` yet (or was previously at a different path), run:

    python3 ~/.claude/skills/afk-mode/install_hook.py

This is idempotent — safe to run again. It adds a `PermissionRequest` matcher entry pointing at `auto-deny-elevations.py` in this skill folder. Restart Claude Code afterward so the new registration snapshots into the next session.

To unregister:

    python3 ~/.claude/skills/afk-mode/uninstall_hook.py

Removes any `PermissionRequest` entry whose command references `auto-deny-elevations.py`.

If a user asks you to "set up afk-mode globally" / "install the hook" / "the hook isn't running", use `install_hook.py`. If they ask to "remove it entirely" / "unregister the hook", use `uninstall_hook.py`. For per-project install (the config file, not the hook registration), use `afk-install.py` instead — that's a different scope.

## Scope: project-local only

The hook fires in every project globally, but only ACTS in projects with a local config. Projects without a local config behave like afk-mode doesn't exist. There is no global afk status.

This means:
- To change afk status in a project, that project needs a local config.
- If a project has no local config and the user wants afk-mode there, offer to run `afk-install`.
- Each project is fully independent.

## When invoked directly (`/afk-mode`)

Direct invocation via the slash command means the user wants to toggle afk-mode state for the current project with minimal friction. Follow this decision tree:

1. Run `python3 ~/.claude/skills/afk-mode/afk-ctl.py status`.

2. **If it reports "afk-mode not installed in this project":**
   Auto-install and enable in one go: run `python3 ~/.claude/skills/afk-mode/afk-install.py` then `python3 ~/.claude/skills/afk-mode/afk-ctl.py enable --mode away`. Report the final state in one line, noting that the project was auto-installed. No confirmation prompt — the user invoked `/afk-mode` which is an explicit toggle-on intent.

3. **If it reports `afk-mode: disabled, mode=<X>`:**
   Run `python3 ~/.claude/skills/afk-mode/afk-ctl.py enable` (no `--mode` flag — preserve the existing mode). Report the new state.

4. **If it reports `afk-mode: ENABLED, mode=<X>`:**
   Run `python3 ~/.claude/skills/afk-mode/afk-ctl.py disable`. Report the new state.

After running the command, always print a clear user-facing message in your own reply — do not rely on the raw CLI output to speak for itself (the user finds bare `afk-mode: ENABLED, mode=away` confusing).

Use exactly these phrasings:

- **Just enabled (toggled on, or auto-installed-and-enabled):**
  "Your status on this project is now set to AWAY. Actions requiring elevation will automatically be blocked, and the agent will work on what they can without the access."

  If you auto-installed, prepend a short sentence: "afk-mode wasn't installed in this project, so I set it up and enabled it."

- **Just disabled (toggled off):**
  "Your status on this project is now BACK / active. Elevation prompts will behave normally again — the agent will ask you when it needs approval."

- **Mode changed without toggling enable** (from `afk-ctl mode …`, not `/afk-mode`):
  "Your afk-mode on this project is now using the `<mode_name>` mode."

Do not dump JSON, do not lecture about the hook, do not offer to make other changes. The user invoked a toggle; give them the toggle and the plain-language confirmation.

For anything other than a bare `/afk-mode` toggle — changing mode, installing, removing, editing messages — follow the guidance in the next section.

## Primary interface: use the CLI scripts, not JSON edits

The scripts `afk-ctl` and `afk-install` are the canonical way to manipulate afk-mode state. Do not edit `.claude/hooks/auto-deny-settings.json` directly unless the user explicitly asks you to modify message text, add a new mode, or do something the scripts don't cover.

**Status check — always run this first when unsure:**

    python3 ~/.claude/skills/afk-mode/afk-ctl.py status

Exits 0 with a line like `afk-mode: ENABLED, mode=away`, or exits 1 with "afk-mode not installed in this project" if no config exists.

**Platform note for the commands below:** on macOS/Linux use `python3` and `~/.claude/...`. On Windows use `python` and `%USERPROFILE%\.claude\...`. The Python scripts themselves are platform-agnostic; only the invocation differs.

**Common requests and the command to run:**

| User says | Command |
|---|---|
| "Set my status to away" / "Enable afk" | `python3 ~/.claude/skills/afk-mode/afk-ctl.py enable --mode away` |
| "I'm back" / "Disable afk" | `python3 ~/.claude/skills/afk-mode/afk-ctl.py disable` |
| "Switch to focus mode" | `python3 ~/.claude/skills/afk-mode/afk-ctl.py mode focus` |
| "What's my current status?" | `python3 ~/.claude/skills/afk-mode/afk-ctl.py status` |
| "What modes are available?" | `python3 ~/.claude/skills/afk-mode/afk-ctl.py list-modes` |
| "Set up afk-mode in this project" | `python3 ~/.claude/skills/afk-mode/afk-install.py` |
| "Remove afk-mode from this project" | `python3 ~/.claude/skills/afk-mode/afk-install.py remove` |

**If the status command reports "afk-mode not installed":** tell the user and offer to run `python3 ~/.claude/skills/afk-mode/afk-install.py`. The install creates the config with `enabled: false` — enabling is a separate, deliberate step.

**Only edit the config JSON directly if:** the user explicitly asks to modify message text, add a new mode, or make a change the scripts don't cover. Read the JSON first, edit, write back. For normal state changes, always prefer the scripts.

## Applying edits

Config changes take effect on the next tool call — the hook script reads config fresh every time it fires. No Claude Code restart needed.

## When the user asks about setup, configuration, or what any of this does

Read `afk-setup-instructions.md` in this skill directory (`~/.claude/skills/afk-mode/afk-setup-instructions.md`). It contains the canonical installation steps, file contents, mode semantics, and troubleshooting. Do not regenerate that content from memory.

## Note to agents encountering auto-deny in a fresh session

If you are an agent that just hit an auto-denied tool call for the first time this session, the deny message you received is the authoritative explanation. It is not a safety block — it is the user's PermissionRequest hook configured via this skill. Follow the deny message's directives exactly: continue what you can, don't mark steps done/blocked, don't invent new work, summarize when stuck. You do not need to invoke this skill to understand a denial; the skill is only for the user changing their status.

## Constraints

- Do not modify `~/.claude/settings.json` or the hook script (`auto-deny-elevations.py`) from within this skill. Those are installation artifacts.
- Do not invent new modes unprompted. Only add modes the user explicitly requests.
- Do not edit the `away` or `default` message text without explicit user request.
- When installing or removing config, always confirm to the user what you did.
