# tmux Buffer Operations

Comprehensive guide to capturing, viewing, and managing tmux buffer content for programmatic output handling.

## Overview

Buffers in tmux are temporary storage areas that hold captured pane content. Unlike the clipboard, buffers are managed entirely within tmux and can be manipulated programmatically, making them ideal for automation and scripting scenarios.

**Core Value:** Extract and process terminal output programmatically without manual copy/paste.

## Capturing Pane Content

### Basic Capture

```bash
# Capture visible pane content to buffer
tmux capture-pane -t <session-name>

# Capture and print to stdout (most common for scripting)
tmux capture-pane -t <session-name> -p

# Capture and save directly to file
tmux capture-pane -t <session-name> -p > output.txt
```

### History Range Options

**`-S` (start line)** and **`-E` (end line)** control which lines to capture from the pane's scrollback history.

```bash
# Capture last 50 lines from scrollback
tmux capture-pane -t session -S -50 -E -1 -p

# Capture from line 10 to line 30
tmux capture-pane -t session -S -30 -E -10 -p

# Capture ALL scrollback history to current position
tmux capture-pane -t session -S - -p

# Capture only visible pane (no scrollback)
tmux capture-pane -t session -p
```

**Line numbering:**
- `0` = current visible line at top of pane
- Negative numbers = lines in scrollback (`-1` = one line up, `-100` = 100 lines up)
- `-` (hyphen) = beginning of all available history

**Use Cases:**
- `-S -` captures entire session history (useful for logging)
- `-S -50 -E -1` captures last 50 lines of scrollback (useful for recent context)
- Default (no -S/-E) captures only visible content

### Line Wrapping and Formatting

**`-J` (join wrapped lines)** merges lines that were wrapped due to terminal width.

```bash
# Without -J: each visual line is separate
tmux capture-pane -t session -p
# Output:
# This is a very long line that got wrapped because of ter
# minal width constraints

# With -J: wrapped lines are joined back together
tmux capture-pane -t session -J -p
# Output:
# This is a very long line that got wrapped because of terminal width constraints
```

**When to use `-J`:**
- Processing structured output (JSON, logs) where line breaks matter
- Parsing command output that shouldn't be split mid-line
- Extracting URLs or file paths that might wrap

**When NOT to use `-J`:**
- Preserving exact visual layout
- Working with columnar data or tables
- Debugging terminal display issues

### Escape Sequences

**`-e` (preserve escape sequences)** keeps ANSI color codes and terminal control sequences in the output.

```bash
# Strip escape sequences (default - clean text)
tmux capture-pane -t session -p

# Preserve escape sequences (keep colors/formatting)
tmux capture-pane -t session -e -p
```

**With escape sequences (`-e`):**
```
^[[32mSUCCESS^[[0m Test passed
^[[31mERROR^[[0m Test failed
```

**Without escape sequences (default):**
```
SUCCESS Test passed
ERROR Test failed
```

**Use Cases:**
- Use `-e` when converting to HTML/rich text (preserve colors)
- Use `-e` when saving raw terminal output for replay
- Default (no `-e`) for parsing logs, extracting data, or text processing

### Target Specification

```bash
# Target session (uses active pane)
tmux capture-pane -t session_name -p

# Target specific window in session
tmux capture-pane -t session_name:2 -p

# Target specific pane in window
tmux capture-pane -t session_name:2.1 -p

# Target by pane ID (from list-panes)
tmux capture-pane -t %15 -p
```

## Viewing Buffer Contents

### Show Current Buffer

```bash
# Display the most recent buffer
tmux show-buffer

# Display specific buffer by name
tmux show-buffer -b buffer0

# Pipe buffer to processing command
tmux show-buffer | grep ERROR
```

### List All Buffers

```bash
# List all buffers with metadata
tmux list-buffers

# Example output:
# buffer0: 1453 bytes: "Session output..."
# buffer1: 892 bytes: "Previous capture..."
# buffer2: 234 bytes: "Older content..."
```

Buffers are automatically named `buffer0`, `buffer1`, etc., with `buffer0` being the most recent.

## Saving Buffers to Files

### Basic Save Operations

```bash
# Save most recent buffer to file
tmux save-buffer output.txt

# Save specific buffer by name
tmux save-buffer -b buffer1 old_output.txt

# Append to existing file instead of overwriting
tmux save-buffer -a log.txt
```

### Programmatic Output Handling

**Pattern 1: Capture and process immediately**
```bash
# Capture, parse, and extract specific information
tmux capture-pane -t build_session -p | grep "ERROR" | wc -l

# Check if command succeeded by looking for success marker
if tmux capture-pane -t test_session -p | grep -q "All tests passed"; then
    echo "Tests successful"
fi
```

**Pattern 2: Capture to buffer, process later**
```bash
# Capture to buffer
tmux capture-pane -t session

# Later: extract from buffer
tmux show-buffer | awk '/^Total:/ {print $2}'

# Save for archival
tmux save-buffer -a session_log_$(date +%Y%m%d).txt
```

**Pattern 3: Continuous monitoring**
```bash
# Monitor build output in loop
while tmux has-session -t build 2>/dev/null; do
    tmux capture-pane -t build -p | tail -5
    sleep 2
done
```

## Buffer Management

### Creating Named Buffers

```bash
# Capture to specifically named buffer
tmux set-buffer -b my_output "$(tmux capture-pane -t session -p)"

# Or capture directly with custom name (requires buffer management)
tmux capture-pane -t session -b custom_name
```

### Deleting Buffers

```bash
# Delete most recent buffer
tmux delete-buffer

# Delete specific buffer
tmux delete-buffer -b buffer1

# Delete all buffers
tmux list-buffers | cut -d: -f1 | xargs -I {} tmux delete-buffer -b {}
```

**Memory Management:**
- Buffers persist until deleted or tmux server restarts
- Each capture creates a new buffer (buffer0 becomes buffer1, etc.)
- Delete old buffers to prevent memory accumulation in long-running sessions

### Setting Buffer Content

```bash
# Manually set buffer content
tmux set-buffer "Custom content here"

# Load file into buffer
tmux load-buffer file.txt

# Set named buffer from file
tmux load-buffer -b my_data file.txt
```

## Practical Examples for Claude Code

### Example 1: Verify Command Success

```bash
#!/bin/bash
# Run npm install and verify success

tmux new-session -d -s npm_install npm install
sleep 2  # Wait for npm to start

# Monitor until complete
while tmux capture-pane -t npm_install -p | tail -1 | grep -q "npm"; do
    sleep 1
done

# Check final output for errors
if tmux capture-pane -t npm_install -S - -p | grep -q "ERR!"; then
    echo "Installation failed"
    tmux capture-pane -t npm_install -S - -p | grep "ERR!"
    exit 1
else
    echo "Installation successful"
fi

tmux kill-session -t npm_install
```

### Example 2: Extract Test Results

```bash
#!/bin/bash
# Run tests and extract statistics

tmux new-session -d -s pytest pytest --verbose
sleep 1

# Wait for tests to complete (prompt returns)
while tmux capture-pane -t pytest -p | tail -1 | grep -qv "^$"; do
    sleep 0.5
done

# Extract results from entire session history
tmux capture-pane -t pytest -S - -J -p > test_results.txt

# Parse summary line
SUMMARY=$(grep "passed\|failed" test_results.txt | tail -1)
echo "Test Summary: $SUMMARY"

# Save full output
tmux save-buffer -b buffer0 "test_run_$(date +%Y%m%d_%H%M%S).log"

tmux kill-session -t pytest
```

### Example 3: Interactive Debugging Session Capture

```bash
#!/bin/bash
# Run interactive debugger and capture specific points

tmux new-session -d -s debug python -m pdb script.py
sleep 0.5

# Send debug commands
tmux send-keys -t debug 'break 45' Enter
sleep 0.2
tmux send-keys -t debug 'continue' Enter
sleep 1

# Capture debugger state at breakpoint
tmux capture-pane -t debug -S -30 -J -p > debug_snapshot.txt

# Check variable values visible on screen
if tmux capture-pane -t debug -p | grep -q "user_count.*=.*0"; then
    echo "WARNING: user_count is zero at breakpoint"
fi

# Continue debugging
tmux send-keys -t debug 'next' Enter
sleep 0.5

# Capture again
tmux capture-pane -t debug -S -20 -p > debug_after_step.txt

tmux kill-session -t debug
```

### Example 4: Long-Running Process Logging

```bash
#!/bin/bash
# Monitor long-running build with periodic snapshots

SESSION="long_build"
LOG_DIR="build_logs"
mkdir -p "$LOG_DIR"

tmux new-session -d -s "$SESSION" make -j4
sleep 1

# Capture snapshots every 30 seconds
for i in {1..100}; do
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
        break
    fi

    # Capture last 50 lines to snapshot
    tmux capture-pane -t "$SESSION" -S -50 -J -p > "$LOG_DIR/snapshot_$i.txt"

    # Check for errors
    if grep -q "error:" "$LOG_DIR/snapshot_$i.txt"; then
        echo "Build error detected at snapshot $i"
        # Capture full history
        tmux capture-pane -t "$SESSION" -S - -p > "$LOG_DIR/full_error_log.txt"
        tmux kill-session -t "$SESSION"
        exit 1
    fi

    sleep 30
done

# Final capture
tmux capture-pane -t "$SESSION" -S - -p > "$LOG_DIR/final_output.txt"
tmux kill-session -t "$SESSION"
```

### Example 5: REPL Session History Export

```bash
#!/bin/bash
# Use Python REPL and export complete session

tmux new-session -d -s python_repl python3
sleep 0.3

# Execute commands
tmux send-keys -t python_repl 'import sys' Enter
sleep 0.1
tmux send-keys -t python_repl 'import pandas as pd' Enter
sleep 0.1
tmux send-keys -t python_repl 'df = pd.read_csv("data.csv")' Enter
sleep 0.5
tmux send-keys -t python_repl 'print(df.head())' Enter
sleep 0.2

# Capture entire REPL session with proper line joining
tmux capture-pane -t python_repl -S - -J -p > repl_session.txt

# Also save as buffer for later reference
tmux save-buffer repl_history_$(date +%Y%m%d_%H%M%S).txt

# Extract only output lines (skip >>> prompts) for processing
grep -v "^>>>" repl_session.txt | grep -v "^\.\.\." > output_only.txt

tmux kill-session -t python_repl
```

## Best Practices

### Timing Considerations

```bash
# BAD: Capture too early, might get incomplete output
tmux new-session -d -s sess "long_command"
tmux capture-pane -t sess -p  # Empty or partial!

# GOOD: Wait for command to produce output
tmux new-session -d -s sess "long_command"
sleep 0.5  # Or poll until expected output appears
tmux capture-pane -t sess -p
```

### Choosing Capture Options

| Goal | Options | Example |
|------|---------|---------|
| Parse structured output | `-J -p` | Capture JSON responses |
| Get recent context | `-S -50 -p` | Last 50 lines of logs |
| Full session archive | `-S - -p` | Complete history |
| Preserve colors for display | `-e -p` | Save colored output |
| Clean text for processing | `-p` (default) | Extract data fields |

### Buffer vs. Direct Output

**Use direct output (`-p`) when:**
- Processing immediately with pipes
- One-time extraction
- Don't need to reference later

**Use buffers when:**
- Need to reference same capture multiple times
- Want to compare before/after states
- Archiving session history
- Multiple processing steps on same data

### Memory Management

```bash
# Clean up old buffers in long-running automation
tmux delete-buffer  # Delete newest
tmux list-buffers | head -n -5 | cut -d: -f1 | xargs -I {} tmux delete-buffer -b {}  # Keep last 5
```

## Common Patterns

### Wait-and-Capture Pattern

```bash
# Run command and wait for specific output before capturing
tmux new-session -d -s wait_sess "npm start"

# Poll until ready
until tmux capture-pane -t wait_sess -p | grep -q "Server listening"; do
    sleep 1
done

# Now capture the port number
PORT=$(tmux capture-pane -t wait_sess -p | grep "listening on" | grep -oP '\d+')
echo "Server ready on port $PORT"
```

### Diff Pattern

```bash
# Capture before
tmux capture-pane -t sess -p > before.txt

# Send commands
tmux send-keys -t sess 'some_command' Enter
sleep 1

# Capture after
tmux capture-pane -t sess -p > after.txt

# Compare
diff before.txt after.txt
```

### Stream Processing Pattern

```bash
# Continuously capture and process new output
LAST_LINES=0
while tmux has-session -t monitor 2>/dev/null; do
    CURRENT=$(tmux capture-pane -t monitor -p | wc -l)

    if [ $CURRENT -gt $LAST_LINES ]; then
        # Only process new lines
        NEW_LINES=$((CURRENT - LAST_LINES))
        tmux capture-pane -t monitor -p | tail -n $NEW_LINES | process_output.sh
        LAST_LINES=$CURRENT
    fi

    sleep 1
done
```

## Troubleshooting

### Empty Captures

**Problem:** `capture-pane` returns nothing

**Solutions:**
- Wait longer after session creation
- Check if session actually exists: `tmux has-session -t name`
- Verify target: `tmux list-panes -a` to see all panes
- Check if command already exited

### Truncated History

**Problem:** `-S -` doesn't capture all expected history

**Solution:** tmux has a history limit (default ~2000 lines)
```bash
# Increase history limit when creating session
tmux new-session -d -s sess -x 80 -y 24 'command'
tmux set-option -t sess history-limit 50000
```

### Wrapped Lines Issues

**Problem:** Long lines split across multiple captures incorrectly

**Solution:** Use `-J` flag consistently
```bash
# All captures should use -J if any do
tmux capture-pane -t sess -S -100 -J -p
```

## Sources

- [tmux(1) Manual Page - capture-pane](https://man.openbsd.org/tmux.1#capture-pane)
- [tmux(1) Manual Page - Buffer Commands](https://man.openbsd.org/tmux.1#BUFFERS)
- [GitHub - tmux/tmux Wiki](https://github.com/tmux/tmux/wiki)
- [Thoughtbot - A tmux Crash Course](https://thoughtbot.com/blog/a-tmux-crash-course)
