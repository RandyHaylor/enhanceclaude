# Multi-Pane Operations in tmux

This document covers advanced multi-pane operations in tmux, enabling parallel workflows, multi-server management, and sophisticated pane control.

## Table of Contents

1. [Creating Multiple Panes](#creating-multiple-panes)
2. [Pane Targeting](#pane-targeting)
3. [Pane Synchronization](#pane-synchronization)
4. [Selecting Panes Programmatically](#selecting-panes-programmatically)
5. [Practical Examples](#practical-examples)

## Creating Multiple Panes

### Basic Pane Creation

Split a window into multiple panes using `split-window`:

```bash
# Split horizontally (top/bottom)
tmux split-window -t session_name

# Split vertically (left/right)
tmux split-window -h -t session_name

# Split and run a command
tmux split-window -t session_name "tail -f /var/log/app.log"
```

### Advanced Splitting

```bash
# Split with specific size (percentage)
tmux split-window -h -p 30 -t session_name  # 30% width

# Split with specific size (lines/columns)
tmux split-window -v -l 10 -t session_name  # 10 lines tall

# Split from specific pane
tmux split-window -h -t session_name:0.1    # Split pane 1
```

### Creating Complex Layouts

```bash
# Create a 4-pane layout
SESSION="dev"

# Start with first pane
tmux new-session -d -s "$SESSION" -n editor

# Split horizontally (top 70%, bottom 30%)
tmux split-window -v -p 30 -t "$SESSION"

# Split bottom pane vertically (left/right)
tmux split-window -h -t "$SESSION:0.1"

# Split top pane vertically
tmux select-pane -t "$SESSION:0.0"
tmux split-window -h -p 50 -t "$SESSION"

# Result: 4 panes
# +--------+--------+
# |   0    |   1    |
# +--------+--------+
# |   2    |   3    |
# +--------+--------+
```

### Predefined Layouts

```bash
# Apply built-in layouts
tmux select-layout -t session_name even-horizontal
tmux select-layout -t session_name even-vertical
tmux select-layout -t session_name main-horizontal
tmux select-layout -t session_name main-vertical
tmux select-layout -t session_name tiled
```

## Pane Targeting

### Target Specification Format

Tmux uses the format `session:window.pane` to identify panes:

```
session_name:0.1
│            │ │
│            │ └─ Pane index (0-based)
│            └─── Window index (0-based)
└──────────────── Session name
```

### Targeting Examples

```bash
# Target by session and pane
tmux send-keys -t dev:0.0 "echo 'pane 0'" Enter
tmux send-keys -t dev:0.1 "echo 'pane 1'" Enter

# Target current window's pane
tmux send-keys -t dev:.2 "echo 'pane 2 in current window'" Enter

# Target by direction from current pane
tmux select-pane -t dev -L  # Left
tmux select-pane -t dev -R  # Right
tmux select-pane -t dev -U  # Up
tmux select-pane -t dev -D  # Down

# Target by special markers
tmux select-pane -t dev -l  # Last (previously selected) pane
tmux select-pane -t dev:.+  # Next pane
tmux select-pane -t dev:.-  # Previous pane
```

### Listing and Inspecting Panes

```bash
# List all panes in a session
tmux list-panes -t session_name

# List panes with format
tmux list-panes -t session_name -F "#{pane_index}: #{pane_current_command} [#{pane_width}x#{pane_height}]"

# Get specific pane info
tmux display-message -t session_name:0.1 -p "#{pane_id} #{pane_current_path}"
```

## Pane Synchronization

Pane synchronization sends the same input to multiple panes simultaneously — essential for multi-server operations.

### Enabling Synchronization

```bash
# Enable for all panes in current window
tmux set-window-option -t session_name:0 synchronize-panes on

# Disable synchronization
tmux set-window-option -t session_name:0 synchronize-panes off

# Toggle synchronization
tmux set-window-option -t session_name:0 synchronize-panes
```

### Synchronized Operations Workflow

```bash
SESSION="multi-server"

# Create session with multiple panes for different servers
tmux new-session -d -s "$SESSION" -n servers

# Create panes for each server
tmux send-keys -t "$SESSION" "ssh server1" Enter
tmux split-window -h -t "$SESSION"
tmux send-keys -t "$SESSION" "ssh server2" Enter
tmux split-window -h -t "$SESSION"
tmux send-keys -t "$SESSION" "ssh server3" Enter

# Enable synchronization
tmux set-window-option -t "$SESSION:0" synchronize-panes on

# Now commands sent to any pane go to all panes
tmux send-keys -t "$SESSION" "sudo systemctl restart nginx" Enter
tmux send-keys -t "$SESSION" "sudo systemctl status nginx" Enter

# Disable when done
tmux set-window-option -t "$SESSION:0" synchronize-panes off
```

### Visual Indicators

```bash
# Check if synchronization is enabled
tmux show-window-options -t session_name:0 | grep synchronize-panes

# Display status in status bar (add to .tmux.conf)
set -g status-right "#{?pane_synchronized,#[bg=red]SYNC ON,}"
```

## Selecting Panes Programmatically

### Sequential Selection

```bash
SESSION="worker"

# Create 4 panes
tmux new-session -d -s "$SESSION"
tmux split-window -h -t "$SESSION"
tmux split-window -v -t "$SESSION:0.0"
tmux split-window -v -t "$SESSION:0.1"

# Send different commands to each pane
for pane in 0 1 2 3; do
    tmux send-keys -t "$SESSION:0.$pane" "echo 'Pane $pane processing...'" Enter
done
```

### Conditional Selection

```bash
# Select panes by criteria
tmux list-panes -t session_name -F "#{pane_index} #{pane_current_command}" | \
while read pane_index command; do
    if [[ "$command" == "bash" ]]; then
        tmux send-keys -t "session_name:0.$pane_index" "echo 'Found idle shell'" Enter
    fi
done
```

### Dynamic Pane Discovery

```bash
# Get pane count
PANE_COUNT=$(tmux list-panes -t session_name | wc -l)

# Get active pane
ACTIVE_PANE=$(tmux display-message -t session_name -p "#{pane_index}")

# Get pane dimensions
PANE_WIDTH=$(tmux display-message -t session_name:0.0 -p "#{pane_width}")
PANE_HEIGHT=$(tmux display-message -t session_name:0.0 -p "#{pane_height}")
```

## Practical Examples

### Example 1: Parallel Test Execution

```bash
SESSION="parallel-tests"
TEST_SUITES=("unit" "integration" "e2e" "performance")

# Create session
tmux new-session -d -s "$SESSION" -n tests

# Create pane for each test suite
for i in "${!TEST_SUITES[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -h -t "$SESSION"
        tmux select-layout -t "$SESSION" tiled
    fi
    tmux send-keys -t "$SESSION:0.$i" "npm run test:${TEST_SUITES[$i]}" Enter
done

# Attach to view all tests running
tmux attach -t "$SESSION"
```

### Example 2: Multi-Environment Deployment Monitor

```bash
SESSION="deploy-monitor"
ENVIRONMENTS=("dev" "staging" "production")

# Create session with 3 panes
tmux new-session -d -s "$SESSION" -n environments

for i in "${!ENVIRONMENTS[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -v -t "$SESSION"
    fi

    ENV="${ENVIRONMENTS[$i]}"
    tmux send-keys -t "$SESSION:0.$i" "# Monitoring $ENV" Enter
    tmux send-keys -t "$SESSION:0.$i" "watch -n 5 'kubectl get pods -n $ENV'" Enter
done

tmux select-layout -t "$SESSION" even-vertical
```

### Example 3: Database Migration Across Shards

```bash
SESSION="db-migrate"
SHARDS=("shard1" "shard2" "shard3" "shard4")

tmux new-session -d -s "$SESSION" -n migration

# Create 2x2 grid
for i in "${!SHARDS[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -h -t "$SESSION"
        if [ $i -eq 2 ]; then
            tmux select-layout -t "$SESSION" tiled
        fi
    fi
done

# Connect each pane to a shard
for i in "${!SHARDS[@]}"; do
    SHARD="${SHARDS[$i]}"
    tmux send-keys -t "$SESSION:0.$i" "mysql -h $SHARD-db -u admin -p" Enter
    sleep 1
    tmux send-keys -t "$SESSION:0.$i" "password123" Enter
done

# Enable synchronization to run migration on all shards
tmux set-window-option -t "$SESSION:0" synchronize-panes on
tmux send-keys -t "$SESSION:0.0" "SOURCE /migrations/v2.sql;" Enter

# Wait and disable sync
sleep 5
tmux set-window-option -t "$SESSION:0" synchronize-panes off
```

### Example 4: Log Tailing and Analysis

```bash
SESSION="log-analysis"
LOG_FILES=(
    "/var/log/nginx/access.log"
    "/var/log/nginx/error.log"
    "/var/log/app/application.log"
    "/var/log/app/errors.log"
)

tmux new-session -d -s "$SESSION" -n logs

# Create 4 panes in 2x2 layout
for i in "${!LOG_FILES[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -h -t "$SESSION"
        if [ $i -eq 2 ]; then
            tmux select-layout -t "$SESSION" tiled
        fi
    fi

    LOG="${LOG_FILES[$i]}"
    BASENAME=$(basename "$LOG")
    tmux send-keys -t "$SESSION:0.$i" "echo '=== $BASENAME ==='" Enter
    tmux send-keys -t "$SESSION:0.$i" "tail -f $LOG | grep --color=auto 'ERROR\\|WARN'" Enter
done
```

### Example 5: Interactive Multi-Server Command Execution

```bash
SESSION="multi-exec"
SERVERS=("web1.example.com" "web2.example.com" "web3.example.com")

# Create session
tmux new-session -d -s "$SESSION" -n servers

# SSH to each server in separate pane
for i in "${!SERVERS[@]}"; do
    if [ $i -gt 0 ]; then
        tmux split-window -v -t "$SESSION"
    fi

    SERVER="${SERVERS[$i]}"
    tmux send-keys -t "$SESSION:0.$i" "ssh $SERVER" Enter

    # Wait for connection
    sleep 2

    # Set pane title
    tmux select-pane -t "$SESSION:0.$i" -T "$SERVER"
done

tmux select-layout -t "$SESSION" even-vertical

# Function to send command to all servers
send_to_all() {
    tmux set-window-option -t "$SESSION:0" synchronize-panes on
    tmux send-keys -t "$SESSION:0.0" "$1" Enter
    sleep 1
    tmux set-window-option -t "$SESSION:0" synchronize-panes off
}

# Example usage
send_to_all "uptime"
send_to_all "df -h"
```

### Example 6: Build and Test Pipeline

```bash
SESSION="pipeline"

tmux new-session -d -s "$SESSION" -n build-test

# Create 3 panes: build (top 60%), test-output (bottom-left 40%), logs (bottom-right 40%)
tmux split-window -v -p 40 -t "$SESSION"
tmux split-window -h -t "$SESSION:0.1"

# Pane 0: Build process
tmux send-keys -t "$SESSION:0.0" "npm run build:watch" Enter

# Pane 1: Test runner
tmux send-keys -t "$SESSION:0.1" "npm run test:watch" Enter

# Pane 2: Application logs
tmux send-keys -t "$SESSION:0.2" "tail -f logs/app.log" Enter

# Select top pane as active
tmux select-pane -t "$SESSION:0.0"
```

## Best Practices

### 1. Always Specify Targets

```bash
# Good - explicit target
tmux send-keys -t session_name:0.1 "command" Enter

# Risky - relies on current context
tmux send-keys "command" Enter
```

### 2. Verify Pane Existence

```bash
# Check if pane exists before sending commands
if tmux list-panes -t session_name:0.1 &>/dev/null; then
    tmux send-keys -t session_name:0.1 "command" Enter
else
    echo "Pane does not exist"
fi
```

### 3. Cleanup After Synchronization

```bash
# Always disable sync when done to avoid accidental commands
tmux set-window-option -t session_name:0 synchronize-panes on
# ... synchronized operations ...
tmux set-window-option -t session_name:0 synchronize-panes off
```

### 4. Use Layout Reapplication

```bash
# After creating/destroying panes, reapply layout for consistency
tmux select-layout -t session_name tiled
```

### 5. Label Panes for Clarity

```bash
# Set pane titles (requires tmux 2.6+)
tmux select-pane -t session_name:0.0 -T "Build"
tmux select-pane -t session_name:0.1 -T "Tests"
tmux select-pane -t session_name:0.2 -T "Logs"
```

## Troubleshooting

### Pane Index Confusion

```bash
# Always verify current pane layout
tmux list-panes -t session_name -F "Pane #{pane_index}: #{pane_current_command}"
```

### Synchronization Not Working

```bash
# Check current sync status
tmux show-window-options -t session_name:0 | grep synchronize-panes

# Ensure you're targeting the correct window
tmux set-window-option -t session_name:window_index synchronize-panes on
```

### Commands Not Reaching Panes

```bash
# Verify pane is responsive
tmux send-keys -t session_name:0.1 "" # Send empty command
tmux display-message -t session_name:0.1 -p "Pane alive: #{pane_id}"
```

## Further Reading

- [Session Persistence](session-persistence.md) - Managing session lifecycle
- [Buffer Operations](buffer-operations.md) - Capturing pane output
- [Error Handling](error-handling.md) - Robust tmux scripting
