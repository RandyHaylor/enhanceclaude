# Error Handling in tmux Sessions

Robust error handling patterns for tmux-based interactive command automation.

## Check if Session Exists

**Core Pattern:** Verify session existence before operations.

```bash
# Safe session check (suppresses error output)
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session $SESSION_NAME exists"
else
  echo "Session $SESSION_NAME not found"
fi
```

**Why `2>/dev/null`?**
- `tmux has-session` returns exit code 0 if session exists, 1 if not
- Without `2>/dev/null`, error message "session not found" prints to stderr
- Redirect stderr to suppress noise in scripted contexts

**Common Use Cases:**
```bash
# Avoid creating duplicate sessions
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux new-session -d -s $SESSION_NAME
fi

# Safe cleanup before recreating
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux kill-session -t $SESSION_NAME
fi
tmux new-session -d -s $SESSION_NAME

# Conditional operations
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux send-keys -t $SESSION_NAME 'command' Enter
else
  echo "Error: Session does not exist" >&2
  exit 1
fi
```

## Graceful Cleanup with trap

**Core Pattern:** Always clean up sessions on script exit, even on errors.

```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="work_session"

# Cleanup function
cleanup() {
  if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    tmux kill-session -t $SESSION_NAME
    echo "Cleaned up session: $SESSION_NAME"
  fi
}

# Register cleanup on exit (normal or error)
trap cleanup EXIT

# Main script logic
tmux new-session -d -s $SESSION_NAME vim file.txt
sleep 0.3
tmux send-keys -t $SESSION_NAME 'i' 'content' Escape ':wq' Enter

# Session auto-cleaned on exit
```

**Why trap is Essential:**
- Script crashes (Ctrl+C, errors) leave orphaned sessions
- `trap cleanup EXIT` runs on normal exit OR error
- `trap cleanup INT TERM` handles specific signals
- Prevents accumulation of zombie sessions

**Advanced trap Pattern:**
```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="deploy_session"
CLEANUP_DONE=0

cleanup() {
  if [ $CLEANUP_DONE -eq 0 ]; then
    CLEANUP_DONE=1
    if tmux has-session -t $SESSION_NAME 2>/dev/null; then
      # Capture final state before killing
      echo "=== Final Session State ===" >&2
      tmux capture-pane -t $SESSION_NAME -p >&2
      tmux kill-session -t $SESSION_NAME
    fi
  fi
}

trap cleanup EXIT INT TERM

# Script operations...
tmux new-session -d -s $SESSION_NAME
# ... work ...
```

**Key Features:**
- `CLEANUP_DONE` flag prevents double-cleanup
- Captures final pane state for debugging
- Handles multiple signal types (EXIT, INT, TERM)

## Handling Failed Commands in Sessions

**Problem:** Commands in tmux sessions fail silently - no automatic error detection.

**Solution:** Capture exit codes and validate output.

### Pattern 1: Explicit Exit Code Check

```bash
SESSION_NAME="test_session"

tmux new-session -d -s $SESSION_NAME
tmux send-keys -t $SESSION_NAME 'command-that-might-fail' Enter
sleep 0.5

# Check last exit code
tmux send-keys -t $SESSION_NAME 'echo "EXIT_CODE:$?"' Enter
sleep 0.2
OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)

if echo "$OUTPUT" | grep -q "EXIT_CODE:0"; then
  echo "Command succeeded"
else
  echo "Command failed" >&2
  tmux capture-pane -t $SESSION_NAME -p >&2
  exit 1
fi
```

### Pattern 2: Output Validation

```bash
SESSION_NAME="build_session"

tmux new-session -d -s $SESSION_NAME npm run build
sleep 2

# Capture and validate output
OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)

if echo "$OUTPUT" | grep -qi "error\|failed\|fatal"; then
  echo "Build failed - errors detected:" >&2
  echo "$OUTPUT" >&2
  tmux kill-session -t $SESSION_NAME
  exit 1
fi

echo "Build succeeded"
```

### Pattern 3: Command Chaining with Markers

```bash
SESSION_NAME="chain_session"

tmux new-session -d -s $SESSION_NAME

# Use unique markers to detect success
tmux send-keys -t $SESSION_NAME 'make clean && make all && echo "BUILD_SUCCESS_MARKER"' Enter
sleep 5

OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)

if echo "$OUTPUT" | grep -q "BUILD_SUCCESS_MARKER"; then
  echo "All steps completed successfully"
else
  echo "Build chain failed somewhere" >&2
  echo "$OUTPUT" >&2
  exit 1
fi
```

### Pattern 4: Real-time Error Detection with Polling

```bash
SESSION_NAME="monitor_session"

tmux new-session -d -s $SESSION_NAME long-running-command
MAX_WAIT=60
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)

  # Check for error indicators
  if echo "$OUTPUT" | grep -qi "error\|exception\|fatal"; then
    echo "Error detected in output:" >&2
    echo "$OUTPUT" >&2
    tmux kill-session -t $SESSION_NAME
    exit 1
  fi

  # Check for success marker
  if echo "$OUTPUT" | grep -q "COMPLETE"; then
    echo "Command completed successfully"
    break
  fi

  sleep 2
  ELAPSED=$((ELAPSED + 2))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
  echo "Command timed out after ${MAX_WAIT}s" >&2
  exit 1
fi
```

## Recovery Patterns When Sessions Die Unexpectedly

**Problem:** Sessions can terminate due to:
- Command crashes (segfaults, unhandled exceptions)
- System resource exhaustion
- Network disconnections (for remote tmux)
- Explicit user intervention

### Pattern 1: Session Liveness Check Before Operations

```bash
send_to_session() {
  local session=$1
  shift

  if ! tmux has-session -t $session 2>/dev/null; then
    echo "Error: Session $session no longer exists" >&2
    return 1
  fi

  tmux send-keys -t $session "$@"
}

# Usage
if send_to_session work_session 'ls -la' Enter; then
  echo "Command sent successfully"
else
  echo "Session died - initiating recovery"
  # Recovery logic here
fi
```

### Pattern 2: Automatic Session Restart

```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="persistent_session"
COMMAND="python3 server.py"

ensure_session_running() {
  if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Session dead - restarting..."
    tmux new-session -d -s $SESSION_NAME $COMMAND
    sleep 1
    return 1  # Indicate restart occurred
  fi
  return 0  # Session already running
}

# Main loop with recovery
for i in {1..10}; do
  if ! ensure_session_running; then
    echo "Session restarted - skipping iteration $i"
    continue
  fi

  tmux send-keys -t $SESSION_NAME "task $i" Enter
  sleep 5
done
```

### Pattern 3: State Capture Before Risky Operations

```bash
SESSION_NAME="risky_session"

# Capture state before risky operation
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
  BEFORE_STATE=$(tmux capture-pane -t $SESSION_NAME -p)
fi

# Risky operation
tmux send-keys -t $SESSION_NAME 'potentially-crashing-command' Enter
sleep 2

# Verify session survived
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session crashed during command execution" >&2
  echo "=== Last Known State ===" >&2
  echo "$BEFORE_STATE" >&2

  # Recovery actions
  tmux new-session -d -s $SESSION_NAME
  # Restore previous state if possible
  exit 1
fi
```

### Pattern 4: Persistent Session Monitoring

```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="monitored_session"
COMMAND="critical-process"
CHECK_INTERVAL=5

# Initial session creation
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  tmux new-session -d -s $SESSION_NAME $COMMAND
fi

# Monitor and restart loop
while true; do
  if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "[$(date)] Session died - restarting" >&2

    # Optional: log the death event
    echo "[$(date)] Session $SESSION_NAME terminated unexpectedly" >> session_deaths.log

    # Restart with same command
    tmux new-session -d -s $SESSION_NAME $COMMAND
    sleep 1

    # Optional: notify administrator
    # send_alert "Session $SESSION_NAME restarted"
  fi

  sleep $CHECK_INTERVAL
done
```

### Pattern 5: Graceful Degradation

```bash
perform_task_with_fallback() {
  local session=$1
  local command=$2
  local fallback_file=$3

  if tmux has-session -t $session 2>/dev/null; then
    # Try to use existing session
    tmux send-keys -t $session "$command" Enter
    sleep 0.5

    if tmux has-session -t $session 2>/dev/null; then
      tmux capture-pane -t $session -p
      return 0
    fi
  fi

  # Fallback: run without tmux
  echo "Session unavailable - running directly" >&2
  eval "$command" | tee "$fallback_file"
  return 1
}

# Usage
perform_task_with_fallback work_session 'make test' /tmp/test_output.txt
```

## Complete Example: Robust tmux Script

```bash
#!/bin/bash
set -euo pipefail

SESSION_NAME="robust_example"
COMMAND="python3 -i"
MAX_RETRIES=3
RETRY_COUNT=0

# Cleanup handler
cleanup() {
  if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Cleaning up session: $SESSION_NAME"
    tmux capture-pane -t $SESSION_NAME -p > final_state.log
    tmux kill-session -t $SESSION_NAME
  fi
}

trap cleanup EXIT INT TERM

# Session creation with retry
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Cleaning up stale session"
    tmux kill-session -t $SESSION_NAME
  fi

  tmux new-session -d -s $SESSION_NAME $COMMAND
  sleep 0.5

  if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Session created successfully"
    break
  fi

  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "Session creation failed - retry $RETRY_COUNT/$MAX_RETRIES"
  sleep 1
done

if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
  echo "Failed to create session after $MAX_RETRIES attempts" >&2
  exit 1
fi

# Perform operations with error checking
tmux send-keys -t $SESSION_NAME 'import sys' Enter
sleep 0.2

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
  echo "Session died during operation" >&2
  exit 1
fi

OUTPUT=$(tmux capture-pane -t $SESSION_NAME -p)
echo "Session output:"
echo "$OUTPUT"

# Explicit success marker
echo "Script completed successfully"
```

## Best Practices Summary

1. **Always check session existence** before operations with `has-session -t $NAME 2>/dev/null`
2. **Use trap for cleanup** to prevent orphaned sessions (`trap cleanup EXIT`)
3. **Validate command success** via exit codes, output markers, or content inspection
4. **Capture state before risky operations** for debugging and recovery
5. **Implement retry logic** for transient failures
6. **Monitor long-running sessions** with periodic liveness checks
7. **Log failures** for post-mortem analysis
8. **Provide fallback paths** when tmux is unavailable or sessions die
9. **Use unique markers** in output to detect success/failure states
10. **Set timeouts** to prevent infinite waiting on hung sessions
