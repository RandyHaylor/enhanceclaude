# VS Code Agent Teams

**Type:** skill | **Version:** 1.0.0 | **OS:** any

Workaround for agent teams in VS Code extension where TeamCreate teammates cannot execute tools. Uses an echo-back-and-resume pattern.

## Tags
vscode, agent-teams, workaround, collaboration, multi-agent

## Overview
This skill addresses a limitation in the VS Code Claude extension where TeamCreate teammates spawn but cannot execute tools. It replaces TeamCreate with Task subagents that return JSON action requests instead of calling tools directly. The team lead executes each request and resumes the agent with the result, enabling multi-step tool execution, peer communication via relay, and broadcast messaging.

## Try These Prompts
- I'm in VS Code and my TeamCreate agents spawn but never run tools. Set up an echo-back agent team to work around this.
- Create a two-agent team using the VS Code workaround pattern — one researcher, one writer — that communicate through you as relay.
- My Task subagent needs to read a file and write another. Walk me through the echo-back loop to execute those steps.
- Set up a broadcast to all active agents telling them the shared state file has been updated.

## Use Cases
- Multi-agent workflows in VS Code
- Echo-back tool execution relay
- Peer agent communication via lead
- Parallel agent task coordination
- Plan approval and correction flows

## Additional Requirements
Only needed when using Claude Code via the VS Code extension. Not needed for CLI usage.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
