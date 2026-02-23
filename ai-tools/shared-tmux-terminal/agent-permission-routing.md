# Agent Permission Routing via Team Lead

How to route agent permission requests to the team lead so all approvals happen in one window.

## Problem

When agents run Bash commands (npm, git, test runners, etc.), permission prompts appear in **each agent's own Claude Code window**, even with `mode: "bypassPermissions"`.

**User impact:**
- Must switch between tmux panes to approve each prompt
- Multiple windows require attention
- Disruptive workflow

## Solution

**Team lead executes all Bash commands on behalf of agents** via tmux send-keys.

**Result:**
- All permission prompts appear in team lead's window only
- User approves from one location
- Agents get their commands executed without direct Bash tool usage

## Setup

### 1. Team Lead Creates Dedicated Terminal for Each Agent

```bash
# Create separate terminal session for each agent
tmux new-session -d -s agent1_terminal -c /path/to/workspace
tmux new-session -d -s agent2_terminal -c /path/to/workspace
```

### 2. Spawn Agents with Clear Instructions

```
Task tool with:
- team_name: your-team
- name: agent1, agent2
- prompt: |
    CRITICAL: DO NOT use the Bash tool directly.

    For any commands (npm, git, test runners, etc.), send a message to team-lead:
    "Please run `<command>` in my terminal (agent1_terminal)"

    You CAN use these tools directly:
    - Read/Write/Edit - file operations
    - Glob/Grep - file search

    Working directory: /path/to/workspace
    Your terminal session: agent1_terminal (for team-lead to execute commands)
```

## Workflow

### Agent Needs to Run a Command

**Agent writes:**
```
SendMessage to team-lead:
"Please run `npm install jest` in my terminal (agent1_terminal)"
```

### Team Lead Executes Command

**Team lead receives message, then:**
```bash
tmux send-keys -t agent1_terminal "npm install jest" Enter
```

### Permission Prompt Appears in Team Lead's Window

- User sees prompt in team lead's Claude pane
- User approves once
- Command executes in agent's terminal

### Agent Sees Result

**Agent can check output by:**
- Reading created/modified files (use Read tool)
- Requesting team lead capture terminal output:
  ```
  SendMessage to team-lead:
  "Please capture output from agent1_terminal"
  ```
- Team lead responds with:
  ```bash
  tmux capture-pane -t agent1_terminal -p
  ```

## Command Routing Guide

### Route Through Team Lead (via tmux send-keys)

These trigger permission prompts:
- `npm install`, `npm test`, `yarn add`
- `git commit`, `git push`, `git rebase`
- Test runners: `jest`, `vitest`, `pytest`, `cargo test`
- Interactive programs: `vim`, `nano`, `less`
- System commands: `mkdir`, `cd`, `rm` (when needed)

### Agents Execute Directly (no permission issues)

These don't trigger permission prompts:
- **Read** - read file contents
- **Write** - create/overwrite files
- **Edit** - modify existing files
- **Glob** - find files by pattern
- **Grep** - search file contents

## Example: TDD Workflow

### Agent Needs to Run Test

```
Agent → Team Lead:
"Please run `npm test` in my terminal (programmer_terminal)"
```

### Team Lead Executes

```bash
tmux send-keys -t programmer_terminal "npm test" Enter
```

### Permission Prompt

- Appears in team lead's window
- User approves
- Test runs in programmer's terminal

### Agent Sees Test Failure

Agent reads test output file, or requests:
```
Agent → Team Lead:
"Please capture test output from programmer_terminal"
```

Team lead responds with captured output.

### Agent Writes Code

```
Agent uses Write/Edit tools directly (no permissions needed)
```

### Agent Needs to Run Test Again

```
Agent → Team Lead:
"Please run `npm test` again in programmer_terminal"
```

Cycle continues.

## Benefits

✓ **Single approval point** - all permissions in team lead's window
✓ **No pane switching** - user stays in one window
✓ **Better UX** - async agent work, batch user approvals
✓ **Clear audit trail** - team lead sees all commands before execution
✓ **Persistent sessions** - terminal output available for inspection

## Limitations

- Requires team lead to monitor and relay command requests
- Adds latency (agent → team lead → execute → response)
- Team lead must be active participant, not just observer
- Agents can't see terminal output directly (must request captures)

## Tips

1. **Batch approvals:** If user trusts the workflow, approve multiple commands at once
2. **Standard commands:** Team lead can auto-execute safe commands (like `npm test`)
3. **Terminal naming:** Use descriptive session names (`tdd_terminal`, `build_terminal`)
4. **Capture often:** Team lead can proactively send terminal captures to agents
5. **Clear messages:** Agents should specify exact command and target terminal
