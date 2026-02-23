# Shared Tmux Terminal

**Type:** skill | **Version:** 1.0.0 | **OS:** linux, macos

Open a shared tmux terminal window that both Claude and the user can see and control simultaneously. Claude sends commands and reads output autonomously.

## Tags
terminal, tmux, shared-terminal, sudo, collaboration

## Overview
Shared Tmux Terminal creates a visible tmux session that acts as a collaborative workspace between Claude and the user. Claude can autonomously send commands and read output from the terminal, while the user retains full control to type directly at any time -- including entering sudo passwords or taking over operations. This skill supports session discovery, multi-pane operations, buffer reading, error handling, and persistent session management across platforms.

## Installation
Requires tmux installed. Linux also needs a terminal emulator (gnome-terminal, konsole, etc.) and optionally xdotool for window title control.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
