# Session Persistence in tmux

How tmux sessions persist, can be reattached, and how to handle session lifecycle correctly.

## Core Concept: Detached Sessions

**Key Insight:** tmux sessions run independently of the creating process and persist until explicitly killed.

```bash
# Create detached session
tmux new-session -d -s my_session vim file.txt

# Session is now running in the background
# You can exit the terminal, log out, even reboot (if using tmux-resurrect)
# The session persists

# Later: attach to see it
tmux attach-session -t my_session
```

**What "detached" means:**
- Session runs in background without visible terminal
- Creating process can exit - session continues
- No parent-child relationship with creating shell
- Session lives until explicitly killed or tmux server stops

## Session Persistence Behaviors

### Sessions Survive Terminal Closure

```bash
# Terminal 1: Create session
tmux new-session -d -s persistent vim important.txt
tmux send-keys -t persistent 'i' 'Draft content' Escape

# Close terminal 1 (or SSH disconnect)

# Terminal 2 (later): Session still exists
tmux list-sessions
# Output: persistent: 1 windows (created Mon Feb 12 10:00:00 2026)

tmux capture-pane -t persistent -p
# Output shows: Draft content still in vim
```

**Why this matters:**
- Long-running commands survive network disconnects
- Interactive sessions can be resumed across SSH sessions
- No need to keep terminal window open
- Scripts can create sessions and exit

### Sessions Survive Creating Process Exit

```bash
#!/bin/bash
# script.sh - creates session and exits

tmux new-session -d -s from_script python3 server.py
echo "Session created, script exiting now"
exit 0
```

```bash
# Run the script
./script.sh
# Output: Session created, script exiting now

# Script is done, but session lives on
tmux list-sessions
# Output: from_script: 1 windows (created ...)

tmux capture-pane -t from_script -p
# Server is still running in the session
```

### Sessions Do NOT Survive tmux Server Restart

```bash
# Create session
tmux new-session -d -s temporary

# Restart tmux server (kills ALL sessions)
tmux kill-server

# Session is gone
tmux list-sessions
# Output: no server running on /tmp/tmux-1000/default
```

**When tmux server stops:**
- System reboot (unless using tmux-resurrect plugin)
- Explicit `tmux kill-server`
- Last session is killed
- All sessions terminate

## Reattaching to Existing Sessions

### Basic Attach

```bash
# Create detached session
tmux new-session -d -s work vim code.py

# Later: attach to see and interact with it
tmux attach-session -t work

# Now you're inside the session - vim is visible
# Press Ctrl+B, then D to detach again

# Session continues running in background
```

**Key points:**
- `attach-session` brings session to foreground
- You can interact with it as if you created it normally
- Detaching (`Ctrl+B D`) returns it to background
- Session state is preserved

### Multiple Clients on Same Session

**Core Feature:** Multiple terminals can attach to the same session simultaneously.

```bash
# Terminal 1:
tmux new-session -d -s shared python3 -i
tmux attach-session -t shared

# Terminal 2 (simultaneously):
tmux attach-session -t shared

# Both terminals now see the SAME session
# Actions in one appear in the other in real-time
```

**Use cases:**
- Pair programming: both developers see same screen
- Monitoring: watch a process from multiple locations
- Remote assistance: helper attaches to same session
- Screen mirroring: present terminal to multiple viewers

**Behavior details:**
```bash
# Terminal 1 sends command
tmux send-keys -t shared 'print("hello")' Enter

# Terminal 2 (attached) sees "hello" appear instantly

# Terminal 3 (detached but capturing)
tmux capture-pane -t shared -p
# Also sees "hello" in output
```

**Window size with multiple clients:**
```bash
# If terminals have different sizes, tmux uses smallest dimensions
# Terminal 1: 80x24
# Terminal 2: 120x40

# Both attach to same session -> session size becomes 80x24

# When larger terminal detaches:
tmux detach-client -t terminal2
# Session expands to fit remaining clients
```

### Attach vs. Capture

**Two ways to access session content:**

| Method | Use Case | Visibility | Interaction |
|--------|----------|------------|-------------|
| `attach-session` | Interactive use | Takes over terminal | Full control |
| `capture-pane -p` | Scripted automation | Prints to stdout | Read-only |

```bash
SESSION=demo

# Attach: for humans
tmux attach-session -t $SESSION
# Now inside session, can type, see updates, Ctrl+C programs, etc.
# Ctrl+B D to detach

# Capture: for scripts
OUTPUT=$(tmux capture-pane -t $SESSION -p)
echo "$OUTPUT"
# Session continues running, not affected by capture
# You remain in your original shell
```

**When to use each:**
```bash
# Debugging: want to see and interact
tmux attach-session -t debug_session

# Automation: just need the output
tmux capture-pane -t debug_session -p | grep "ERROR"

# Monitoring: periodic checks without disrupting session
while true; do
  tmux capture-pane -t monitor_session -p > snapshot.txt
  sleep 10
done
```

## Checking if Session Exists Before Creating

**Problem:** Creating duplicate sessions causes errors or unexpected behavior.

**Solution:** Always check first with `has-session`.

### Basic Pattern

```bash
SESSION_NAME="my_work"

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session $SESSION_NAME already exists"
else
  echo "Creating new session $SESSION_NAME"
  tmux new-session -d -s $SESSION_NAME
fi
```

**Why `2>/dev/null`?**
```bash
# Without stderr redirect:
tmux has-session -t nonexistent
# Prints: "can't find session: nonexistent"
# Exit code: 1

# With stderr redirect:
tmux has-session -t nonexistent 2>/dev/null
# Prints: (nothing)
# Exit code: 1

# The exit code is what we check, error message is noise
```

### Idempotent Session Creation

**Goal:** Running script multiple times safely creates session only once.

```bash
#!/bin/bash
SESSION_NAME="persistent_worker"

# Idempotent: safe to run multiple times
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux new-session -d -s $SESSION_NAME python3 worker.py
  echo "Created session $SESSION_NAME"
else
  echo "Session $SESSION_NAME already running"
fi

# Now we can safely send commands knowing session exists
tmux send-keys -t $SESSION_NAME 'process_job()' Enter
```

### Clean Restart Pattern

**Use case:** Want to start fresh, killing old session if it exists.

```bash
SESSION_NAME="fresh_start"

# Kill if exists, then create new
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Killing existing session"
  tmux kill-session -t $SESSION_NAME
fi

echo "Creating fresh session"
tmux new-session -d -s $SESSION_NAME
```

**Alternative: single-line version**
```bash
SESSION_NAME="fresh_start"

# Kill existing session (ignore error if not exists), then create
tmux kill-session -t $SESSION_NAME 2>/dev/null || true
tmux new-session -d -s $SESSION_NAME
```

### Attach or Create Pattern

**Use case:** Attach to session if exists, otherwise create it first.

```bash
#!/bin/bash
SESSION_NAME="work"

attach_or_create() {
  local session=$1
  shift  # Remaining args are the command to run if creating

  if ! tmux has-session -t $session 2>/dev/null; then
    echo "Session $session doesn't exist, creating..."
    tmux new-session -d -s $session "$@"
    sleep 0.3  # Let it initialize
  fi

  echo "Attaching to $session"
  tmux attach-session -t $session
}

# Usage
attach_or_create work vim project.txt
```

### Conditional Operations Based on Session Existence

```bash
SESSION_NAME="optional_session"

# Only send commands if session actually exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux send-keys -t $SESSION_NAME 'status' Enter
  tmux capture-pane -t $SESSION_NAME -p
else
  echo "Warning: Session $SESSION_NAME not running, skipping status check"
fi
```

```bash
# Count active sessions
ACTIVE_COUNT=$(tmux list-sessions 2>/dev/null | wc -l)
echo "Currently $ACTIVE_COUNT active sessions"

if [ $ACTIVE_COUNT -eq 0 ]; then
  echo "No sessions running, starting default"
  tmux new-session -d -s default
fi
```

## Error Handling Patterns for Session Existence

### Defensive Session Operations

**Pattern:** Verify session exists before every operation that requires it.

```bash
safe_send_keys() {
  local session=$1
  shift

  if ! tmux has-session -t $session 2>/dev/null; then
    echo "Error: Session $session does not exist" >&2
    return 1
  fi

  tmux send-keys -t $session "$@"
  return 0
}

safe_capture() {
  local session=$1

  if ! tmux has-session -t $session 2>/dev/null; then
    echo "Error: Session $session does not exist" >&2
    return 1
  fi

  tmux capture-pane -t $session -p
  return 0
}

# Usage with error handling
if safe_send_keys work_session 'make test' Enter; then
  sleep 2
  OUTPUT=$(safe_capture work_session)
  echo "$OUTPUT"
else
  echo "Failed to interact with session"
  exit 1
fi
```

### Explicit vs. Silent Failure

**Explicit failure (recommended for critical operations):**
```bash
SESSION_NAME="critical_job"

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "FATAL: Required session $SESSION_NAME not found" >&2
  echo "Start it with: tmux new-session -d -s $SESSION_NAME worker.sh" >&2
  exit 1
fi

# Continue with confidence session exists
tmux send-keys -t $SESSION_NAME 'critical_command' Enter
```

**Silent failure (acceptable for optional operations):**
```bash
SESSION_NAME="optional_monitor"

# Try to capture, but don't fail script if session gone
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux capture-pane -t $SESSION_NAME -p >> monitor.log
fi

# Script continues regardless
echo "Continuing main workflow"
```

### Session Died Mid-Operation

**Problem:** Session exists when you check, but dies before you use it.

**Solution:** Check again after critical operations.

```bash
SESSION_NAME="fragile_process"

# Initial check
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session doesn't exist" >&2
  exit 1
fi

# Send potentially dangerous command
tmux send-keys -t $SESSION_NAME 'risky_operation' Enter
sleep 1

# Verify session survived
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session died during operation" >&2
  echo "Check logs for crash information" >&2
  exit 1
fi

# Safe to continue
OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)
echo "$OUTPUT"
```

### Handling Race Conditions

**Problem:** Multiple scripts might create/kill same session simultaneously.

**Mitigation 1: Unique session names per script instance**
```bash
# Use PID to ensure unique session name
SESSION_NAME="worker_$$"  # $$ is current process ID

tmux new-session -d -s $SESSION_NAME python worker.py
# No risk of collision with other instances

# Cleanup
trap "tmux kill-session -t $SESSION_NAME 2>/dev/null || true" EXIT
```

**Mitigation 2: Lockfile pattern**
```bash
LOCKFILE="/tmp/tmux_session_work.lock"
SESSION_NAME="work"

# Acquire lock
exec 200>"$LOCKFILE"
if ! flock -n 200; then
  echo "Another instance is managing this session" >&2
  exit 1
fi

# Now safe to check/create/kill session
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux new-session -d -s $SESSION_NAME
fi

# Work with session...
tmux send-keys -t $SESSION_NAME 'command' Enter

# Lock released on script exit
```

### Complete Robust Example

```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="robust_session"
COMMAND="python3 -i"

# Cleanup on exit
cleanup() {
  if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Cleaning up session $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
  fi
}
trap cleanup EXIT

# Ensure session exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Found existing session $SESSION_NAME, killing it for fresh start"
  tmux kill-session -t $SESSION_NAME
fi

echo "Creating session $SESSION_NAME"
tmux new-session -d -s $SESSION_NAME $COMMAND

# Verify creation succeeded
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "FATAL: Failed to create session" >&2
  exit 1
fi

sleep 0.3  # Let session initialize

# Perform operations with verification
echo "Sending commands to session"
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "FATAL: Session died before we could use it" >&2
  exit 1
fi

tmux send-keys -t $SESSION_NAME 'import sys' Enter
sleep 0.2

# Verify session still alive after command
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "FATAL: Session died during command execution" >&2
  exit 1
fi

# Capture result
OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)
echo "Session output:"
echo "$OUTPUT"

echo "Script completed successfully"
# Cleanup happens automatically via trap
```

## Best Practices Summary

1. **Check before create:** Use `has-session -t $NAME 2>/dev/null` to avoid duplicates
2. **Detached by default:** Create sessions with `-d` flag for background operation
3. **Persistence is automatic:** Sessions survive creating process exit and terminal closure
4. **Multiple clients OK:** Same session can be attached from multiple terminals simultaneously
5. **Cleanup is manual:** Always kill sessions explicitly or use trap handlers
6. **Verify after risky ops:** Re-check session existence after potentially dangerous commands
7. **Unique names prevent collisions:** Use PID or UUIDs for parallel script instances
8. **Exit code is truth:** `has-session` exit code (0/1) is reliable; stderr is noise
9. **Attach for humans, capture for scripts:** Choose the right access method for your use case
10. **Session death is recoverable:** Implement detection and restart logic for critical workflows
