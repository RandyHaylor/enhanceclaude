---
name: vscode-agent-teams
description: Workaround for agent teams in VS Code extension where TeamCreate teammates cannot execute tools. Uses an echo-back-and-resume pattern where agents return tool requests instead of executing them directly.
---

# VS Code Agent Teams

TeamCreate teammates broken in VS Code — spawn but never execute tools. Use Task subagents with echo-back pattern instead.

## Workarounds

### Echo-Back Pattern
- Use `Task` subagents (NOT TeamCreate)
- Agent returns JSON action request, lead executes, lead resumes agent with result
- Repeat until `{"action": "done"}`

### Agent Prompt Template

```
You are a worker agent. Do your thinking and planning internally.

WHEN YOU NEED TO USE A TOOL (Write, Read, Bash, etc.):
- Do NOT call the tool yourself
- Instead, return a JSON block describing what you need:

{"action": "write", "path": "/path/to/file.txt", "content": "file contents here"}
{"action": "read", "path": "/path/to/file.txt"}
{"action": "bash", "command": "ls -la"}
{"action": "web_search", "query": "search terms"}
{"action": "relay", "to": "agent-name", "message": "message text"}
{"action": "plan", "steps": ["step 1", "step 2"]}
{"action": "done", "summary": "what you accomplished"}

Return ONLY the JSON block, nothing else. One request per return.
After the team lead executes it, you'll be resumed with the result.

YOUR TASK: [task description here]
```

### Relay Pattern (peer communication)
- Agent returns `{"action": "relay", "to": "agent-name", "message": "..."}`
- Lead resumes target agent with message, brings back response

### Broadcast Pattern
- Lead sends same resume message to all active agents in parallel

## Tested Features

- **Multi-step tool execution** — bash, read, write, web_search via echo-back loop
- **Context preservation** — agents remember task and prior results across resumes
- **Plan approval** — agent returns plan JSON, lead approves/rejects, agent continues
- **Plan correction** — lead can redirect off-plan agents mid-execution
- **Peer communication** — relay through lead as intermediary
- **Shared state via file** — multiple agents read/write same file through lead
- **Broadcast** — lead fans out identical message to all agents in parallel
