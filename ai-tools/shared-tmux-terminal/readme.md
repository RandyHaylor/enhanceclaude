# Shared Tmux Terminal

**Type:** skill | **Version:** 1.0.0 | **OS:** linux, macos

Open a shared tmux terminal window that both Claude and the user can see and control simultaneously. Claude sends commands and reads output autonomously.

## Tags
terminal, tmux, shared-terminal, sudo, collaboration

## Overview
Shared Tmux Terminal creates a visible tmux session that acts as a collaborative workspace between Claude and the user. Claude can autonomously send commands and read output from the terminal, while the user retains full control to type directly at any time -- including entering sudo passwords or taking over operations. This skill supports session discovery, multi-pane operations, buffer reading, error handling, and persistent session management across platforms.

## Try These Prompts
- Open a shared terminal so I can watch what you're doing
- Set up a shared tmux session and install these packages for me
- I need to run some sudo commands — open a shared terminal so I can enter my password
- Start a visible terminal and walk me through deploying this app step by step

## Use Cases
- Running sudo commands where the user enters their own password
- Live-debugging sessions where both parties can see the terminal
- Guided server setup or configuration with full user visibility
- Multi-step deployments with real-time output monitoring
- Multi-agent collaborative terminal workflows

## Additional Requirements
Requires tmux installed. Linux also needs a terminal emulator (gnome-terminal, konsole, etc.) and optionally xdotool for window title control.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
