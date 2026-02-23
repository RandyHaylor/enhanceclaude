# tmux Team Collaboration Pattern

How to use shared tmux sessions for multi-agent collaborative editing with user observation/participation.

## ⚠️ Important Notes

**Status:** Experimental pattern with known limitations. **See [agent-permission-routing.md](agent-permission-routing.md) for the recommended permission routing solution.**

### What Works Well ✓

**Code Review / Mentoring Pattern (Recommended Use Case):**
- **Mentor agent observing programmer agent** - Excellent results in testing
- Mentor watches file changes, provides TDD/SOLID compliance feedback to team lead
- Team lead relays guidance to programmer
- Message-based coordination is smooth and effective
- Clear separation: programmer writes code, mentor reviews, team lead coordinates
- **Example:** Number guessing game test showed mentor successfully providing detailed TDD cycle feedback, identifying good practices, suggesting next steps

**Other Benefits:**
- Asynchronous agent collaboration through shared files and messages
- User can observe work through shared tmux sessions
- Terminal output visibility for all participants
- Clear audit trail of all work

### Known Limitations ⚠️

**Permission Request Flood:**
- Even with `mode: "bypassPermissions"`, agents trigger many permission prompts
- npm install, git commands, folder trust, test runners all need approval
- User must switch between tmux panes to approve each prompt in each agent's window
- **Solution:** Use permission routing pattern (see [agent-permission-routing.md](agent-permission-routing.md))

**Vim Collaborative Editing Issues:**
- Agents can't "see" vim - they need text via Read/cat or capture-pane
- Direct vim editing causes permission prompts for file reading
- Concurrent editing can cause formatting artifacts
- **Better approach:** Agents use Read/Write/Edit tools on files directly, not vim

**Resource Usage:**
- High API usage with multiple concurrent agents
- Each agent is a full Claude instance
- Best for focused, short-duration tasks

### Recommended Pattern

**For code review/mentoring:**
1. Programmer agent writes code using Write/Edit tools
2. Mentor agent reads files, reviews for quality
3. Mentor sends feedback messages to team lead
4. Team lead relays guidance to programmer
5. For bash commands (npm, git, tests), use permission routing pattern

**See Also:**
- **[agent-permission-routing.md](agent-permission-routing.md)** - Route permissions through team lead (solves permission flood)
- Sections below for detailed setup procedures

---

## Concept

Multiple agents edit the same file simultaneously in a shared vim session. User can observe and interact in real-time.

## Setup Procedure

### 1. Create Team
```bash
TeamCreate with team_name and description
```

### 2. Create Template File
```bash
cat > /tmp/shared_file.txt << 'EOF'
# Section markers for each agent

---agent-1 contribution---
(Placeholder for agent 1)
---end agent-1 contribution---

---agent-2 contribution---
(Placeholder for agent 2)
---end agent-2 contribution---

---agent-3 contribution---
(Placeholder for agent 3)
---end agent-3 contribution---
EOF
```

### 3. Create Shared Vim Session
```bash
tmux kill-session -t vim_collab 2>/dev/null
tmux new-session -d -s vim_collab
tmux send-keys -t vim_collab "vim /tmp/shared_file.txt" C-m
```

### 4. Create Tasks for Agents
Each task should include:
- Clear section assignment (agent-1, agent-2, etc.)
- Connection instructions: `TMUX= tmux attach -t vim_collab`
- Editing instructions:
  1. Navigate to assigned section
  2. Delete placeholder
  3. Write content
  4. Save with `:w`
  5. Detach with `Ctrl+b then d`

### 5. Get Initial Bash Pre-Approval from User

**CRITICAL:** Before spawning agents, get user's blanket approval for bash commands.

Tell user:
"The agents will need to run bash commands to interact with the shared vim session (tmux send-keys, etc.). This will require multiple permission approvals. Would you like to grant blanket approval for these commands now?"

If yes, spawn agents with:
```bash
Task tool with:
- subagent_type: general-purpose
- team_name: vim-collab-test
- name: agent-1, agent-2, agent-3
- mode: "bypassPermissions"  # <-- CRITICAL for avoiding constant prompts
- prompt: Instructions to claim and complete their task
```

If no, warn user they'll need to approve each command individually.

### 6. Connect User to Shared Session

**Goal:** Create a new pane to the FAR RIGHT (outside any agent panes) for user's vim view.

```bash
SESSION_NAME=$(cat ~/.claude_tmux_session)

# Split from the main window (not a specific pane) to create rightmost pane
tmux split-window -t "$SESSION_NAME:0" -h -p 33

# Identify the new pane number (should be the highest pane number)
# For standard setup: pane 0=terminal, pane 1=Claude Code, pane 2=new vim pane
tmux send-keys -t "$SESSION_NAME:0.2" "TMUX= tmux attach -t vim_collab" C-m
```

**Layout goal:**
```
[Pane 0: Terminal] [Pane 1: Claude Code] [Pane 2: Shared Vim]
```

Not:
```
[Pane 0: Terminal] [Pane 1a: Agent] [Pane 2: Shared Vim]
                   [Pane 1b: Claude]
```

## Key Technical Details

### Nested Sessions
- Use `TMUX=` prefix to allow nested tmux sessions
- Without this, attach will fail with "sessions should be nested with care"

### Pane Management
- User's session has panes: 0 (terminal), 1 (Claude Code), 2 (shared vim)
- Target pane 2 for the shared vim connection
- Verify with: `tmux list-panes -t $SESSION_NAME:0`

### Vim Collaboration
- All users attached to same session see same vim state
- Any edit by any user is immediately visible to all
- Use section markers to coordinate who edits what
- Agents should save (`:w`) but not exit (`:q`)
- Agents detach with `Ctrl+b then d` to leave vim running

### Agent Instructions
Agents need clear instructions to:
1. Connect to the shared session (with TMUX= prefix)
2. Navigate to their section in vim
3. Edit their assigned section only
4. Save changes
5. Detach (not exit) to allow others to continue

## Permission Routing Pattern (Recommended)

**Problem:** Even with `mode: "bypassPermissions"`, agents still trigger permission prompts for npm, git, test runners, folder trust, etc. User must switch between tmux panes to approve each prompt in each agent's window.

**Solution:** Team lead executes all Bash commands on behalf of agents via tmux send-keys. All permission prompts appear in team lead's window only.

### How It Works

1. **Team lead sets up dedicated terminal session for each agent:**
   ```bash
   # For each agent, create their own terminal session
   tmux new-session -d -s agent1_terminal -c /path/to/workspace
   tmux new-session -d -s agent2_terminal -c /path/to/workspace
   ```

2. **Agents are instructed to:**
   - Use Read/Write/Edit/Glob/Grep tools directly (no permission issues)
   - **Never call Bash tool** for commands like npm, git, test runners
   - Instead, send message to team lead requesting command execution

3. **Agent workflow example:**
   ```
   Agent needs: npm install jest

   Agent sends message to team-lead:
   "Please run `npm install jest` in my terminal (agent1_terminal)"
   ```

4. **Team lead executes command via tmux:**
   ```bash
   tmux send-keys -t agent1_terminal "npm install jest" Enter
   ```

5. **Permission prompt appears in team lead's Claude window** (not agent's window)

6. **User approves once in one window** (the team lead's)

### Commands That Need Team Lead Execution

**Route through team lead:**
- npm/yarn commands (`npm install`, `npm test`, etc.)
- git commands (`git commit`, `git push`, etc.)
- Test runners (`jest`, `vitest`, `pytest`, etc.)
- Interactive programs (vim, nano, etc.)
- System commands when necessary (`mkdir`, `cd`, etc.)

**Agents can execute directly:**
- Read tool - read files
- Write tool - create/overwrite files
- Edit tool - modify files
- Glob tool - find files by pattern
- Grep tool - search file contents

### Benefits

- **Single approval point:** All permission prompts in team lead's window
- **No pane switching:** User stays in team lead's Claude pane
- **Better UX:** Agents work async, user approves in batch
- **Clear audit trail:** Team lead sees all commands before execution

### Implementation Notes

- Agents must be instructed NOT to use Bash tool
- Team lead monitors for command requests via SendMessage
- Team lead can batch approvals or provide pre-approval for common commands
- Terminal sessions persist - agents can see output via capture-pane or file reads

## Test Case: Grass Cutting Advice

Setup:
- 3 agents each write 2-3 sentences of grass cutting advice
- Each agent has their own marked section
- User observes all edits in real-time
- **MUST get blanket bash approval first** or user will be spammed with permission prompts

Result (when done correctly):
- All 3 agents can write simultaneously (though vim shows one at a time)
- User can read, navigate, and even edit alongside agents
- File persists with all contributions

Result (without pre-approval):
- User gets constant permission prompts for every tmux send-keys command
- Very disruptive to user experience
- Agents get blocked waiting for approvals

## Limitations

- Only one cursor position visible (last attached user)
- No conflict resolution if agents edit same line
- Agents must coordinate via section markers
- vim must stay running (agents detach, don't exit)
- **Permission prompts:** Without mode: "bypassPermissions", user will be prompted to approve every bash command agents run (very disruptive)

## Cleanup

```bash
# Kill shared session
tmux kill-session -t vim_collab

# Shutdown agents
SendMessage with type: "shutdown_request" to each agent

# Delete team
TeamDelete
```

## Improvements to Test

Ideas for iteration:
1. Add timestamps to each agent's contribution
2. Use git for version control of shared file
3. Add agent coordination via chat before editing
4. Test with larger files and more complex edits
5. Add conflict resolution mechanism
6. Use tmux pane synchronization for multi-window views
7. **Test permission routing pattern:** Set up TDD project where programmer agent requests npm/git commands from team lead instead of running Bash directly
