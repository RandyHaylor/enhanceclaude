# Timeout and Polling Strategies

Guide to timing, waiting, and detecting command completion in tmux sessions.

## When to Use Different Sleep Durations

**Core Value:** Match wait times to command initialization characteristics.

### Instant Commands (0-50ms)

Commands that provide immediate feedback.

```bash
# Fast shell built-ins
tmux new-session -d -s quick bash
tmux send-keys -t quick 'echo hello' Enter
# No sleep needed for simple commands
tmux capture-pane -t quick -p
```

**Examples:**
- `echo`, `printf`
- Shell variable assignment
- `cd`, `pwd`
- Simple arithmetic

### Fast Interactive Tools (100-200ms)

Lightweight interactive programs.

```bash
# Python REPL
tmux new-session -d -s python python3
sleep 0.1  # Wait for Python prompt
tmux capture-pane -t python -p
```

**Examples:**
- Python REPL
- Node.js REPL
- bc calculator
- SQLite shell

### Medium Startup Tools (300-500ms)

Programs with configuration loading or initialization.

```bash
# Vim editor
tmux new-session -d -s vim vim file.txt
sleep 0.3  # Wait for vim to render
tmux send-keys -t vim 'i' 'content' Escape ':wq' Enter
```

**Examples:**
- Vim, Neovim
- Git interactive rebase
- Less pager
- Nano editor

### Heavy Applications (500ms-2s)

Programs with extensive startup routines.

```bash
# Emacs editor
tmux new-session -d -s emacs emacs -nw file.txt
sleep 1.5  # Wait for Emacs initialization
tmux send-keys -t emacs 'Hello World' C-x C-s C-x C-c
```

**Examples:**
- Emacs
- Database clients (psql, mysql)
- Docker container shells
- Language servers

### Network-Dependent Commands (variable)

Operations requiring network I/O.

```bash
# SSH connection
tmux new-session -d -s remote ssh user@host
sleep 2  # Wait for connection + authentication
tmux capture-pane -t remote -p
```

**Examples:**
- SSH connections
- Remote database connections
- API requests via curl
- Git fetch/pull operations

## Polling for Expected Output

**Core Value:** Wait for specific output before proceeding, not arbitrary time.

### Basic Output Polling

```bash
# Wait for specific prompt or output
wait_for_output() {
    local session="$1"
    local pattern="$2"
    local timeout="${3:-10}"  # Default 10 seconds
    local interval="${4:-0.1}"  # Check every 100ms

    local elapsed=0

    while (( $(echo "$elapsed < $timeout" | bc -l) )); do
        if tmux capture-pane -t "$session" -p | grep -q "$pattern"; then
            return 0
        fi
        sleep "$interval"
        elapsed=$(echo "$elapsed + $interval" | bc -l)
    done

    return 1  # Timeout
}

# Example: Wait for Python REPL prompt
tmux new-session -d -s python python3
if wait_for_output python ">>>" 5; then
    echo "Python ready"
    tmux send-keys -t python 'import sys' Enter
else
    echo "Timeout waiting for Python" >&2
    exit 1
fi
```

### Polling for Command Completion

```bash
# Wait for command to finish (prompt returns)
wait_for_prompt() {
    local session="$1"
    local prompt_pattern="${2:-\$}"  # Default: shell prompt
    local timeout="${3:-30}"

    local start=$(date +%s)

    while true; do
        local output=$(tmux capture-pane -t "$session" -p)
        local last_line=$(echo "$output" | tail -n 1)

        # Check if last line matches prompt pattern
        if echo "$last_line" | grep -q "$prompt_pattern"; then
            return 0
        fi

        # Check timeout
        local now=$(date +%s)
        if (( now - start >= timeout )); then
            return 1
        fi

        sleep 0.2
    done
}

# Example: Run command and wait for completion
tmux new-session -d -s work bash
sleep 0.2
tmux send-keys -t work 'sleep 3 && echo done' Enter
if wait_for_prompt work '\$' 10; then
    echo "Command completed"
    tmux capture-pane -t work -p | tail -n 5
fi
```

### Polling with Output Change Detection

```bash
# Wait until output stops changing
wait_for_stable_output() {
    local session="$1"
    local stable_duration="${2:-1}"  # Seconds of no change
    local timeout="${3:-30}"

    local prev_output=""
    local stable_since=$(date +%s)
    local start=$(date +%s)

    while true; do
        local current_output=$(tmux capture-pane -t "$session" -p)
        local now=$(date +%s)

        if [[ "$current_output" == "$prev_output" ]]; then
            # Output unchanged
            if (( now - stable_since >= stable_duration )); then
                return 0  # Stable for required duration
            fi
        else
            # Output changed, reset stability timer
            stable_since=$now
            prev_output="$current_output"
        fi

        # Check timeout
        if (( now - start >= timeout )); then
            return 1
        fi

        sleep 0.2
    done
}

# Example: Wait for long-running build output to stabilize
tmux new-session -d -s build bash
tmux send-keys -t build 'npm run build' Enter
if wait_for_stable_output build 2 120; then
    echo "Build completed (output stable for 2 seconds)"
fi
```

## Detecting Command Completion

**Core Value:** Reliably determine when interactive commands finish.

### Exit Code Detection

```bash
# Capture exit code of last command
get_exit_code() {
    local session="$1"

    tmux send-keys -t "$session" 'echo EXIT_CODE:$?' Enter
    sleep 0.1
    local output=$(tmux capture-pane -t "$session" -p)
    echo "$output" | grep -oP 'EXIT_CODE:\K\d+'
}

# Example: Run command and check success
tmux new-session -d -s test bash
tmux send-keys -t test 'test -f /nonexistent' Enter
sleep 0.2
exit_code=$(get_exit_code test)
if [[ "$exit_code" -eq 0 ]]; then
    echo "Command succeeded"
else
    echo "Command failed with exit code $exit_code"
fi
```

### Process Completion Detection

```bash
# Check if foreground process is still running
is_command_running() {
    local session="$1"

    # Send Ctrl+Z to suspend (if running) and check output
    tmux send-keys -t "$session" C-z
    sleep 0.1
    local output=$(tmux capture-pane -t "$session" -p | tail -n 3)

    if echo "$output" | grep -q "Stopped"; then
        # Command was running, resume it
        tmux send-keys -t "$session" 'fg' Enter
        return 0  # Was running
    else
        # No job to suspend, command finished
        return 1
    fi
}
```

### Prompt-Based Completion

```bash
# Wait for shell prompt indicating readiness
wait_for_ready_prompt() {
    local session="$1"
    local max_wait="${2:-10}"

    local start=$(date +%s)

    while true; do
        # Get last line of output
        local last_line=$(tmux capture-pane -t "$session" -p | tail -n 1)

        # Check for common prompt indicators
        if [[ "$last_line" =~ (\$|#|>)\ *$ ]] || \
           [[ "$last_line" =~ ^.*:~.*\$ ]]; then
            return 0
        fi

        local now=$(date +%s)
        if (( now - start >= max_wait )); then
            return 1
        fi

        sleep 0.1
    done
}

# Example: Wait for shell to be ready
tmux new-session -d -s shell bash
if wait_for_ready_prompt shell 5; then
    echo "Shell is ready for input"
fi
```

## Handling Variable Initialization Times

**Core Value:** Adapt to different system loads and command startup speeds.

### Adaptive Polling

```bash
# Start with short delays, increase if command not ready
adaptive_wait() {
    local session="$1"
    local pattern="$2"
    local max_timeout="${3:-10}"

    local delays=(0.1 0.2 0.5 1.0 2.0)
    local total_wait=0

    for delay in "${delays[@]}"; do
        sleep "$delay"
        total_wait=$(echo "$total_wait + $delay" | bc -l)

        if tmux capture-pane -t "$session" -p | grep -q "$pattern"; then
            return 0
        fi

        if (( $(echo "$total_wait >= $max_timeout" | bc -l) )); then
            return 1
        fi
    done

    return 1
}

# Example: Wait for SSH with adaptive delays
tmux new-session -d -s ssh ssh user@host
if adaptive_wait ssh "Last login:" 20; then
    echo "SSH connected"
fi
```

### Resource-Aware Timing

```bash
# Adjust wait time based on system load
get_load_adjusted_sleep() {
    local base_sleep="$1"

    # Get 1-minute load average
    local load=$(uptime | grep -oP 'load average: \K[0-9.]+')
    local cores=$(nproc)

    # If load > cores, increase wait time
    local multiplier=$(echo "1 + ($load / $cores - 1) * 0.5" | bc -l)
    echo "$base_sleep * $multiplier" | bc -l
}

# Example: Adjust vim startup wait based on system load
adjusted_sleep=$(get_load_adjusted_sleep 0.3)
tmux new-session -d -s vim vim file.txt
sleep "$adjusted_sleep"
tmux send-keys -t vim 'i' 'content' Escape ':wq' Enter
```

## Timeout Strategies for Different Command Types

**Core Value:** Match timeout strategy to command characteristics.

### Fast-Fail Commands

Commands that should complete quickly or fail.

```bash
# Strict timeout for expected-fast operations
run_with_strict_timeout() {
    local session="$1"
    local command="$2"
    local timeout="${3:-5}"

    tmux send-keys -t "$session" "$command" Enter

    local start=$(date +%s)
    while true; do
        sleep 0.1
        local now=$(date +%s)

        if (( now - start >= timeout )); then
            echo "Error: Command timed out after ${timeout}s" >&2
            tmux send-keys -t "$session" C-c  # Kill command
            return 1
        fi

        # Check if prompt returned (command finished)
        if tmux capture-pane -t "$session" -p | tail -n 1 | grep -q '\$'; then
            return 0
        fi
    done
}
```

### Long-Running Commands

Commands expected to take extended time.

```bash
# Patient timeout with progress checking
run_with_progress_check() {
    local session="$1"
    local command="$2"
    local check_interval="${3:-5}"  # Check every N seconds
    local max_wait="${4:-300}"  # Max 5 minutes

    tmux send-keys -t "$session" "$command" Enter

    local start=$(date +%s)
    local last_output=$(tmux capture-pane -t "$session" -p)

    while true; do
        sleep "$check_interval"
        local now=$(date +%s)
        local current_output=$(tmux capture-pane -t "$session" -p)

        # Check if output changed (indicates progress)
        if [[ "$current_output" != "$last_output" ]]; then
            echo "Progress detected..."
            last_output="$current_output"
        fi

        # Check timeout
        if (( now - start >= max_wait )); then
            echo "Warning: Max wait time reached" >&2
            return 1
        fi

        # Check if command completed
        if echo "$current_output" | tail -n 1 | grep -q '\$'; then
            return 0
        fi
    done
}
```

### Interactive Commands

Commands requiring user interaction at unpredictable times.

```bash
# Wait with pattern list (multiple possible outcomes)
wait_for_any_pattern() {
    local session="$1"
    shift
    local patterns=("$@")
    local timeout=30

    local start=$(date +%s)

    while true; do
        local output=$(tmux capture-pane -t "$session" -p)

        # Check each pattern
        for pattern in "${patterns[@]}"; do
            if echo "$output" | grep -q "$pattern"; then
                echo "Matched: $pattern"
                return 0
            fi
        done

        local now=$(date +%s)
        if (( now - start >= timeout )); then
            return 1
        fi

        sleep 0.2
    done
}

# Example: Git rebase might prompt for conflict or complete
tmux new-session -d -s rebase -c /repo git rebase -i HEAD~3
if wait_for_any_pattern rebase "CONFLICT" "Successfully rebased" "^:"; then
    echo "Rebase awaiting input or completed"
fi
```

## Best Practices

1. **Start with minimal waits** and increase only when needed
2. **Poll for expected output** instead of guessing time requirements
3. **Implement timeouts** to prevent infinite waiting
4. **Log intermediate states** when debugging timing issues
5. **Use exponential backoff** for commands with variable startup times
6. **Detect command completion** via prompts, not arbitrary delays
7. **Consider system load** when setting timeouts on resource-intensive commands
8. **Test on slow systems** to ensure timing works across environments

## Common Timing Patterns Summary

| Command Type | Recommended Wait | Detection Method |
|--------------|------------------|------------------|
| Shell built-in | 0ms | Immediate |
| REPL (Python, Node) | 100-200ms | Poll for prompt (`>>>`, `>`) |
| Vim/editor | 300-500ms | Poll for file content or mode line |
| Git interactive | 300-500ms | Poll for editor prompt |
| SSH connection | 1-3s | Poll for login message or prompt |
| Database client | 500-1500ms | Poll for DB prompt |
| Container shell | 1-2s | Poll for shell prompt |
| Network operations | Variable | Poll for output + timeout |
| Build commands | Variable | Output stability detection |

## Anti-Patterns to Avoid

```bash
# DON'T: Arbitrary long sleeps
sleep 5  # Why 5? Too long or too short?

# DO: Poll for expected state
wait_for_output session "Ready" 5

# DON'T: No timeout (infinite wait)
while ! tmux capture-pane -t sess -p | grep -q "done"; do
    sleep 1
done

# DO: Implement timeout
if wait_for_output sess "done" 30; then
    echo "Success"
fi

# DON'T: Assume instant readiness
tmux new-session -d -s vim vim file.txt
tmux send-keys -t vim 'i' 'text' Escape ':wq' Enter  # Too fast!

# DO: Wait for initialization
tmux new-session -d -s vim vim file.txt
wait_for_output vim "file.txt" 1
tmux send-keys -t vim 'i' 'text' Escape ':wq' Enter
```
