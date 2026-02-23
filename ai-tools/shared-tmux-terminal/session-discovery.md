# Session Discovery

Guide to finding, identifying, and managing tmux sessions programmatically.

## Listing Active Sessions

**Core Value:** Query existing sessions before creating new ones to avoid conflicts.

```bash
# List all sessions (human-readable)
tmux list-sessions

# List sessions with custom format
tmux list-sessions -F "#{session_name}"

# List sessions with additional details
tmux list-sessions -F "#{session_name}: #{session_windows} windows (created #{session_created})"
```

**Common Format Variables:**
- `#{session_name}` - Session name
- `#{session_windows}` - Number of windows
- `#{session_attached}` - Number of attached clients
- `#{session_created}` - Unix timestamp of creation
- `#{session_activity}` - Unix timestamp of last activity
- `#{session_id}` - Unique session ID

**Exit Codes:**
- `0` - Sessions exist
- `1` - No sessions found

## Preventing Duplicate Session Names

**Core Value:** Avoid creating duplicate sessions that conflict with existing ones.

### Check Before Creating

```bash
# Check if session exists (exit 0 if yes, 1 if no)
if tmux has-session -t my_session 2>/dev/null; then
    echo "Session already exists"
else
    tmux new-session -d -s my_session
fi
```

### Fail-Safe Creation Pattern

```bash
# Only create if session doesn't exist
SESSION="dev_session"

tmux has-session -t "$SESSION" 2>/dev/null || \
    tmux new-session -d -s "$SESSION"
```

### Kill and Recreate Pattern

```bash
# Ensure clean slate by killing if exists
SESSION="temp_session"

tmux kill-session -t "$SESSION" 2>/dev/null
tmux new-session -d -s "$SESSION" vim file.txt
```

## Finding Sessions by Pattern

**Core Value:** Locate sessions matching specific criteria programmatically.

### By Name Pattern

```bash
# Find sessions starting with "dev_"
tmux list-sessions -F "#{session_name}" | grep '^dev_'

# Find sessions containing "python"
tmux list-sessions -F "#{session_name}" | grep python

# Count matching sessions
COUNT=$(tmux list-sessions -F "#{session_name}" | grep -c '^test_')
```

### By Activity

```bash
# Find idle sessions (no activity in 1 hour)
NOW=$(date +%s)
THRESHOLD=3600  # 1 hour in seconds

tmux list-sessions -F "#{session_name} #{session_activity}" | while read name activity; do
    if (( NOW - activity > THRESHOLD )); then
        echo "$name is idle"
    fi
done
```

### By Attachment Status

```bash
# List detached sessions
tmux list-sessions -F "#{session_name} #{session_attached}" | \
    awk '$2 == 0 {print $1}'

# List attached sessions
tmux list-sessions -F "#{session_name} #{session_attached}" | \
    awk '$2 > 0 {print $1}'
```

## Session Naming Conventions

**Core Value:** Consistent naming enables reliable programmatic discovery.

### Recommended Patterns

```bash
# Unique per-task sessions
SESSION="edit_$(date +%s)"          # Timestamp-based uniqueness
SESSION="rebase_$$"                 # Process ID uniqueness
SESSION="vim_$RANDOM"               # Random number uniqueness

# Purpose-based naming
SESSION="python_repl"               # Functional name
SESSION="git_interactive"           # Task-specific name
SESSION="dev_server"                # Service-based name

# Hierarchical naming
SESSION="project_backend_tests"    # Nested categories
SESSION="env_staging_deploy"       # Environment prefix
```

### Anti-Patterns

```bash
# Avoid generic names that conflict
SESSION="session"                   # Too generic
SESSION="temp"                      # Likely to conflict
SESSION="test"                      # Common test name collision

# Avoid special characters that complicate scripting
SESSION="my-session:1"              # Colons conflict with window syntax
SESSION="session with spaces"       # Requires quoting everywhere
```

## Programmatic Session Discovery Patterns

**Core Value:** Robust scripts that handle session lifecycle reliably.

### Idempotent Session Creation

```bash
# Get or create session (safe to run multiple times)
get_or_create_session() {
    local session_name="$1"
    local command="${2:-bash}"

    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        tmux new-session -d -s "$session_name" "$command"
    fi
}

get_or_create_session "python_repl" "python3"
```

### Session Cleanup by Age

```bash
# Kill sessions older than N seconds
cleanup_old_sessions() {
    local max_age="$1"  # In seconds
    local now=$(date +%s)

    tmux list-sessions -F "#{session_name} #{session_created}" 2>/dev/null | \
    while read name created; do
        if (( now - created > max_age )); then
            echo "Killing old session: $name"
            tmux kill-session -t "$name"
        fi
    done
}

# Kill sessions older than 1 hour
cleanup_old_sessions 3600
```

### Find Session Running Specific Command

```bash
# Find session by command pattern
find_session_by_command() {
    local pattern="$1"

    for session in $(tmux list-sessions -F "#{session_name}" 2>/dev/null); do
        # Capture pane content and search for pattern
        if tmux capture-pane -t "$session" -p | grep -q "$pattern"; then
            echo "$session"
            return 0
        fi
    done

    return 1
}

# Example: Find session running vim
if vim_session=$(find_session_by_command "^vim "); then
    echo "Found vim session: $vim_session"
fi
```

### Bulk Session Operations

```bash
# Kill all sessions matching pattern
kill_sessions_matching() {
    local pattern="$1"

    tmux list-sessions -F "#{session_name}" 2>/dev/null | \
    grep "$pattern" | \
    xargs -I {} tmux kill-session -t {}
}

# Kill all test sessions
kill_sessions_matching "^test_"

# Kill all sessions (nuclear option)
tmux kill-server 2>/dev/null
```

## Error Handling

**Core Value:** Gracefully handle missing sessions without script failure.

### Safe Session Queries

```bash
# Check session exists before operating
if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux send-keys -t "$SESSION" 'command' Enter
else
    echo "Error: Session $SESSION not found" >&2
    exit 1
fi
```

### Defensive Session Access

```bash
# Wrapper that validates session exists
safe_send_keys() {
    local session="$1"
    shift

    if ! tmux has-session -t "$session" 2>/dev/null; then
        echo "Error: Session '$session' does not exist" >&2
        return 1
    fi

    tmux send-keys -t "$session" "$@"
}

safe_send_keys "my_session" 'echo hello' Enter
```

### Capture with Fallback

```bash
# Capture session output or return default
capture_or_default() {
    local session="$1"
    local default="${2:-<session not found>}"

    if tmux has-session -t "$session" 2>/dev/null; then
        tmux capture-pane -t "$session" -p
    else
        echo "$default"
    fi
}

OUTPUT=$(capture_or_default "my_session" "Session unavailable")
```

## Integration Examples

### Wrapper Script with Discovery

```bash
#!/bin/bash
# tmux-ensure-session.sh - Get existing or create new session

SESSION_NAME="${1:?Session name required}"
COMMAND="${2:-bash}"

# Check if session exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Reusing existing session: $SESSION_NAME"
else
    echo "Creating new session: $SESSION_NAME"
    tmux new-session -d -s "$SESSION_NAME" "$COMMAND"
    sleep 0.3  # Wait for initialization
fi

# Return session name for use in scripts
echo "$SESSION_NAME"
```

### Session Status Reporter

```bash
#!/bin/bash
# tmux-status.sh - Report on all tmux sessions

if ! tmux list-sessions &>/dev/null; then
    echo "No tmux sessions running"
    exit 0
fi

echo "Active tmux sessions:"
echo "===================="

tmux list-sessions -F "#{session_name}|#{session_windows}|#{session_attached}|#{session_created}" | \
while IFS='|' read name windows attached created; do
    age=$(($(date +%s) - created))
    status="detached"
    [[ $attached -gt 0 ]] && status="attached ($attached clients)"

    printf "%-20s %d windows  %-25s  %ds old\n" \
        "$name" "$windows" "$status" "$age"
done
```

## Best Practices

1. **Always check session existence** before operating on it
2. **Use unique session names** with timestamps or PIDs for temporary sessions
3. **Avoid hardcoding session names** in scripts; use parameters or environment variables
4. **Clean up sessions** after use to prevent accumulation
5. **Use descriptive names** that indicate purpose (e.g., `python_repl_debugging` not `temp1`)
6. **Document session lifecycle** in comments when sessions persist across script runs
7. **Handle the no-sessions case** gracefully (exit code 1 from `list-sessions`)

## Common Patterns Summary

| Task | Command Pattern |
|------|----------------|
| Check if exists | `tmux has-session -t "$NAME" 2>/dev/null` |
| Create if missing | `tmux has-session -t "$NAME" 2>/dev/null \|\| tmux new-session -d -s "$NAME"` |
| List all sessions | `tmux list-sessions -F "#{session_name}"` |
| Find by pattern | `tmux list-sessions -F "#{session_name}" \| grep "pattern"` |
| Kill by pattern | `tmux list-sessions -F "#{session_name}" \| grep "pattern" \| xargs -I {} tmux kill-session -t {}` |
| Count sessions | `tmux list-sessions 2>/dev/null \| wc -l` |
