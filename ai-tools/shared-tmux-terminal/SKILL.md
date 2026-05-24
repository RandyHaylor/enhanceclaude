---
name: shared-tmux-terminal
description: >
  Open a shared tmux terminal window that both Claude and the user can see and
  control simultaneously. Claude sends commands to it and reads the output
  automatically — no need to ask the user what happened. The user can type in
  it directly, including for sudo passwords, or to take over at any time. Use when the user
  wants a visible terminal, needs to run sudo commands, wants Claude to assist
  with terminal operations, or wants shared visibility of what Claude is doing.
triggers:
  - "open a shared terminal"
  - "shared tmux"
  - "visible terminal"
  - "sudo command"
  - "let me see what you're doing"
  - "terminal I can watch"
  - "assist with terminal"
---

# shared-tmux-terminal

Single terminal window shared by Claude and user. Claude drives it (sends commands, reads output autonomously). User can type at any time — including sudo passwords.

**Follow these steps in order. Step 1 is mandatory — you MUST open a visible window before sending any commands.**

---

## Step 1: Open a visible terminal window (REQUIRED FIRST)

Create the tmux session:
```bash
tmux new-session -s shared -d
```

Then open a terminal window attached to it (the user must be able to see it):
```bash
gnome-terminal -- tmux attach -t shared &
```

**macOS:** `osascript -e "tell app \"Terminal\" to do script \"tmux attach -t shared\"""`

If `gnome-terminal` is unavailable, detect the available terminal emulator first:
```bash
which gnome-terminal konsole xfce4-terminal lxterminal alacritty kitty 2>/dev/null
```

---

## Live output streaming

Always pipe pane output to a log file **in the current chat session folder** (not /tmp). This keeps logs scoped to the conversation and avoids cross-session collisions:
```bash
# Use the chat session folder for the log (agents should create this path)
tmux pipe-pane -t shared -o 'cat >> /home/aikenyon/.claude/sessions/<SESSION_ID>/tmux_shared.log'
```

If the session folder is unknown or unavailable, fall back to `/tmp/tmux_shared.log`.

**Default: read log on demand** (low token use). Start with a small tail, expand only if needed:
```bash
tail -3 <LOG_PATH>    # check last few lines first
tail -50 <LOG_PATH>   # expand if more context needed
```

**Optional: Monitor tool** (HIGH TOKEN USE — every line becomes a message). Offer to the user but don't enable by default:
```
Monitor({ description: "tmux output", command: "tail -f <LOG_PATH>", persistent: true })
```

---

## Step 2: Send commands

Send commands to the window (user sees them live):
```bash
tmux send-keys -t shared 'your command here' Enter
```

**ALWAYS verify the command started by reading the log file** (tail the log, not capture-pane):
```bash
tail -3 <LOG_PATH>
```

**Only use `tmux capture-pane -t shared -p` as a last resort** — it captures only visible lines and is lossy. Prefer the piped log file for all output reading.

Interrupt a running command:
```bash
tmux send-keys -t shared C-c
```

---

## Step 3: Sudo (when needed)

Send the sudo command to the window. The user sees the password prompt and types it. Wait, then read the result:
```bash
tmux send-keys -t shared 'sudo apt install -y some-package' Enter
```

---

## Check if session is alive

```bash
tmux has-session -t shared 2>/dev/null
```

---

## Advanced Features

- **[session-persistence.md](session-persistence.md)** — idempotent creation, attach vs capture, multiple clients, cleanup traps, race conditions
- **[error-handling.md](error-handling.md)** — defensive session ops, graceful cleanup, failure detection
- **[buffer-operations.md](buffer-operations.md)** — advanced buffer and history capture
- **[multi-pane-operations.md](multi-pane-operations.md)** — multi-pane control and synchronization
- **[session-discovery.md](session-discovery.md)** — finding and managing existing sessions
- **[timeout-polling.md](timeout-polling.md)** — timing strategies and output polling
- **[tmux-power-features.md](tmux-power-features.md)** — advanced tmux capabilities
- **[agent-permission-routing.md](agent-permission-routing.md)** — route agent permission requests through team lead
- **[tmux-team-collaboration.md](tmux-team-collaboration.md)** — multi-agent collaborative workflows

---

## Set window title (optional, Linux only — uses `xdotool`; Mac: `osascript`; Windows: `AutoHotkey`/`SetConsoleTitle` — untested on non-Linux)

`printf` to PTY won't work from Claude's subprocess. Discover the PTY dynamically:

```bash
WID=$(xdotool search --class "gnome-terminal" | while read w; do
  echo "$w $(xdotool getwindowname $w)"; done | grep -v tmux | head -1 | awk '{print $1}')
TERM_PID=$(xdotool getwindowpid $WID)
for child in $(pgrep -P $TERM_PID); do ls -la /proc/$child/fd/0; done
# identify /dev/pts/N, then:
printf "\033]2;My Title\007" > /dev/pts/N
```
