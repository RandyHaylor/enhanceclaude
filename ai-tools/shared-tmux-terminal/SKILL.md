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

---

## Open

```bash
SESSION="shared-$(date +%s)"
gnome-terminal -- bash -c "tmux new-session -s '$SESSION' -d; tmux attach -t '$SESSION'" &
disown %1
echo "Session: $SESSION"
```

Save `$SESSION` — needed for all subsequent commands. **macOS:** `osascript -e "tell app \"Terminal\" to do script \"tmux new-session -s '$SESSION'\""`. If `gnome-terminal` unavailable, detect first:
```bash
which gnome-terminal konsole xfce4-terminal lxterminal alacritty kitty 2>/dev/null | head -1
```

---

## Drive

Send commands to the window (user sees them); read output directly (never ask user to report it).

```bash
tmux send-keys -t "$SESSION" 'your command here' Enter
sleep 1 && tmux capture-pane -t "$SESSION" -p | tail -20  # read output
tmux send-keys -t "$SESSION" C-c                           # interrupt
```

---

## Sudo

Send the sudo command to the window; user sees the prompt and types their password. Claude waits, then reads result.

```bash
tmux send-keys -t "$SESSION" 'sudo apt install -y some-package' Enter
sleep 3 && tmux capture-pane -t "$SESSION" -p | tail -20
```

---

## Check alive

```bash
tmux has-session -t "$SESSION" 2>/dev/null && echo "alive" || echo "gone"
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
