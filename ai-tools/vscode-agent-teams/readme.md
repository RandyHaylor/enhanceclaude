# VS Code Agent Teams

**Type:** skill | **Version:** 1.0.0 | **OS:** any

Workaround for agent teams in VS Code extension where TeamCreate teammates cannot execute tools. Uses an echo-back-and-resume pattern.

## Tags
vscode, agent-teams, workaround, collaboration, multi-agent

## Overview
This skill addresses a limitation in the VS Code Claude extension where TeamCreate teammates spawn but cannot execute tools. It replaces TeamCreate with Task subagents that return JSON action requests instead of calling tools directly. The team lead executes each request and resumes the agent with the result, enabling multi-step tool execution, peer communication via relay, and broadcast messaging.

## Installation
Only needed when using Claude Code via the VS Code extension. Not needed for CLI usage.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
