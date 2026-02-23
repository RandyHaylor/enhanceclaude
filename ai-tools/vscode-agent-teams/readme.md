# VS Code Agent Teams

**Type:** skill | **Version:** 1.0.0 | **Platform:** Claude Code

Workaround for agent teams in VS Code extension where TeamCreate teammates cannot execute tools. Uses an echo-back-and-resume pattern where agents return tool requests instead of executing them directly.

## Tags
vscode, agent-teams, workaround, collaboration, multi-agent

## Overview
This skill addresses a limitation in the VS Code Claude extension where TeamCreate teammates spawn but cannot execute tools. It replaces TeamCreate with Task subagents that return JSON action requests (read, write, bash, etc.) instead of calling tools directly. The team lead executes each request and resumes the agent with the result, enabling multi-step tool execution, peer communication via relay, broadcast messaging, and plan approval workflows.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
