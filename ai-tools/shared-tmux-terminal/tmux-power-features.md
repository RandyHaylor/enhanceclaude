# tmux Power Features

Comprehensive guide to advanced tmux capabilities beyond basic session management.

## Session Persistence & Detachment

**Core Value:** Sessions persist independently of terminal connection state.

- Detach from sessions without terminating processes (`Ctrl+b d`)
- Reattach to existing sessions from any terminal (`tmux attach -t <name>`)
- Sessions survive SSH disconnections, system sleep, terminal crashes
- Multiple clients can attach to same session simultaneously (pair programming)

**Use Cases:**
- Long-running processes (builds, downloads, monitoring)
- Remote development that survives network drops
- Shared debugging sessions with teammates

## Pane Synchronization

**Core Value:** Execute identical commands across multiple panes simultaneously.

```bash
# Enable synchronization for current window
tmux setw synchronize-panes on

# Disable when done
tmux setw synchronize-panes off

# Toggle via keybinding (add to .tmux.conf)
bind-key S setw synchronize-panes
```

**Use Cases:**
- Deploying to multiple servers simultaneously
- Running identical commands across dev/staging/prod environments
- Parallel testing across different configurations
- Database migrations on sharded systems

**Limitations:**
- All panes receive input (can't selectively exclude)
- Works per-window (all panes in window, not across windows)
- Use `select-pane` to choose target when sync is enabled

## Layouts & Window Management

**Core Value:** Organize workspace with predefined or custom layouts.

**Built-in Layouts:**
```bash
# Cycle through layouts
Ctrl+b Space

# Select specific layout
tmux select-layout even-horizontal  # Equal width columns
tmux select-layout even-vertical    # Equal height rows
tmux select-layout main-horizontal  # One large top, small bottom panes
tmux select-layout main-vertical    # One large left, small right panes
tmux select-layout tiled            # Grid layout
```

**Custom Layouts:**
```bash
# Capture current layout
tmux list-windows -F "#{window_layout}"

# Restore saved layout
tmux select-layout "layout-string"
```

**Dynamic Resizing:**
```bash
# Resize pane incrementally
Ctrl+b Ctrl+Arrow    # Resize by 1 cell
Ctrl+b Alt+Arrow     # Resize by 5 cells

# Swap panes
Ctrl+b {             # Swap with previous
Ctrl+b }             # Swap with next

# Break pane into new window
Ctrl+b !

# Join pane from another window
tmux join-pane -s <source-window>:<pane-number>
```

## Copy Mode & Buffer Management

**Core Value:** Search, navigate, and copy terminal output without mouse.

```bash
# Enter copy mode
Ctrl+b [

# In copy mode (vi mode):
Space        # Start selection
Enter        # Copy selection
q            # Exit copy mode
/            # Search forward
?            # Search backward
n            # Next search result
N            # Previous search result

# Paste buffer
Ctrl+b ]

# List all buffers
tmux list-buffers

# Paste specific buffer
tmux paste-buffer -b <buffer-name>

# Save buffer to file
tmux save-buffer -b <buffer-name> file.txt
```

**System Clipboard Integration:**
```bash
# Install xclip (Ubuntu/Debian)
sudo apt install xclip

# Add to .tmux.conf for clipboard integration
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

## Scripting & Automation

**Core Value:** Automate complex workspace setups with scripts.

**Session Creation Script:**
```bash
#!/bin/bash
# dev-session.sh - Create development environment

SESSION="dev"

# Create session with first window
tmux new-session -d -s $SESSION -n editor

# Create additional windows
tmux new-window -t $SESSION:1 -n tests
tmux new-window -t $SESSION:2 -n server

# Split panes in editor window
tmux select-window -t $SESSION:0
tmux split-window -h
tmux split-window -v

# Run commands in specific panes
tmux send-keys -t $SESSION:0.0 'vim' C-m
tmux send-keys -t $SESSION:0.1 'git status' C-m
tmux send-keys -t $SESSION:1 'npm test -- --watch' C-m
tmux send-keys -t $SESSION:2 'npm run dev' C-m

# Attach to session
tmux attach-t $SESSION
```

**Command Line Session Management:**
```bash
# Create named session in background
tmux new-session -d -s background_job 'long-running-command'

# Send commands to existing session
tmux send-keys -t background_job 'next command' Enter

# Capture output programmatically
tmux capture-pane -t background_job -p > output.txt

# Kill session when done
tmux kill-session -t background_job
```

## Plugin Ecosystem (TPM)

**Core Value:** Extend tmux with community plugins.

**Setup tmux Plugin Manager:**
```bash
# Clone TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Add to .tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Initialize TPM (keep at bottom of .tmux.conf)
run '~/.tmux/plugins/tpm/tpm'

# Install plugins: Ctrl+b I
```

**Popular Plugins:**
- **tmux-resurrect:** Save/restore tmux environment across reboots
- **tmux-continuum:** Automatic continuous saving of sessions
- **tmux-yank:** Enhanced clipboard integration
- **tmux-copycat:** Advanced search and highlighting
- **tmux-sidebar:** File tree browser in tmux pane
- **tmux-fzf:** Fuzzy finder integration

## Process Management & cgroups (Linux + systemd)

**Core Value:** Advanced process isolation and resource management.

On systemd-based Linux systems, tmux integrates with systemd user manager:
- Each session runs in isolated cgroup scope
- Resource limits (CPU, memory) can be applied per session
- Process lifecycle managed by systemd
- Improved reliability and crash recovery

```bash
# View systemd scope for tmux session
systemctl --user status tmux@<session-name>.scope

# Apply resource limits (requires systemd configuration)
systemctl --user set-property tmux@session.scope MemoryMax=2G CPUQuota=50%
```

## Mouse Mode

**Core Value:** Optional mouse support for pane selection, resizing, scrolling.

```bash
# Enable mouse mode
tmux set -g mouse on

# Disable mouse mode
tmux set -g mouse off
```

**Mouse Capabilities:**
- Click to select pane
- Drag pane borders to resize
- Scroll to enter copy mode and navigate
- Click on window names to switch
- Right-click for context menu (with plugins)

**Trade-offs:**
- Reduces terminal's native mouse support
- Can interfere with text selection (use Shift to bypass tmux)
- Keyboard is usually faster for power users

## Status Bar Customization

**Core Value:** Information-rich status bar with custom content.

```bash
# Status bar positioning
set -g status-position top    # or bottom

# Status bar content (left)
set -g status-left "[#S] #I:#P"

# Status bar content (right)
set -g status-right "%Y-%m-%d %H:%M | CPU: #{cpu_percentage} | MEM: #{mem_percentage}"

# Window status format
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W* "

# Colors
set -g status-style bg=black,fg=white
set -g window-status-current-style bg=blue,fg=white
```

**Dynamic Content:**
- Session name, window index, pane index
- System metrics (with plugins: CPU, memory, battery)
- Git branch (with plugins)
- Custom scripts output

## Nested Sessions

**Core Value:** Use tmux inside tmux (local + remote).

```bash
# Configure nested session keybinding (add to .tmux.conf)
# Outer session uses Ctrl+b
# Inner session uses Ctrl+a
bind-key -n C-a send-prefix

# Or toggle prefix forwarding
bind-key F12 set-option -g prefix None
```

**Use Cases:**
- Local tmux + SSH into remote tmux
- Different keybindings for each level
- Visual indicators for nested sessions

## Sources

- [GitHub - rothgar/awesome-tmux](https://github.com/rothgar/awesome-tmux)
- [Why You Should Finally Learn Tmux (Yes, Even in 2026)](https://medium.com/quick-programming/why-you-should-finally-learn-tmux-yes-even-in-2026-4dc9478bde30)
- [After 5 Years of Using tmux, Here are the Features I Can't Live Without](https://itnext.io/after-5-years-of-using-tmux-here-are-the-features-i-cant-live-without-04b27dba9b27)
- [Advanced tmux Features - Power User Guide](https://tmux.info/docs/advanced)
- [How to synchronize panes in tmux?](https://tmuxai.dev/tmux-synchronize-panes/)
- [Streamlining Your Tmux Workflow by Synchronizing Panes](https://www.fosslinux.com/105799/streamlining-your-tmux-workflow-by-synchronizing-panes.htm)
- [Advanced Guide to tmux: Enhancing Terminal Productivity](https://www.gingertechblog.com/advanced-guide-to-tmux-enhancing-terminal-productivity/)
- [Tmux Cheat Sheet & Quick Reference](https://tmuxcheatsheet.com/)
