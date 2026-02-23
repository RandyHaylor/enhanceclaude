# Cursor IDE: Custom Agents, Rules, and Skills Setup Guide

This guide covers how to set up project-level and global custom agents, rules, and tools in Cursor IDE on Mac, Linux, and Windows.

---

## Table of Contents

1. [Overview](#overview)
2. [Rules (Custom Instructions)](#rules-custom-instructions)
   - [User Rules (Global)](#user-rules-global)
   - [Project Rules (.cursor/rules/)](#project-rules-cursorrules)
   - [AGENTS.md (Cross-Platform Standard)](#agentsmd-cross-platform-standard)
   - [Legacy .cursorrules File](#legacy-cursorrules-file)
3. [Custom Agent Modes](#custom-agent-modes)
4. [MCP Servers (Custom Tools)](#mcp-servers-custom-tools)
   - [Project-Level MCP Config](#project-level-mcp-config)
   - [Global MCP Config](#global-mcp-config)
5. [Platform-Specific Paths](#platform-specific-paths)
6. [Quick-Start Checklist](#quick-start-checklist)

---

## Overview

Cursor provides several layers of customization for AI behavior:

| Layer | Scope | Format | Location |
|-------|-------|--------|----------|
| **User Rules** | All projects (global) | Plain text | Cursor Settings UI |
| **Project Rules** | Single project | `.mdc` files with YAML frontmatter | `.cursor/rules/` directory |
| **AGENTS.md** | Single project | Plain markdown | Project root (or subdirectories) |
| **Custom Modes** | Per project or global | JSON or UI config | `.cursor/modes.json` or Settings UI |
| **MCP Servers** | Per project or global | JSON | `.cursor/mcp.json` or `~/.cursor/mcp.json` |

Rule precedence (highest to lowest): **Team Rules > Project Rules > User Rules**

---

## Rules (Custom Instructions)

### User Rules (Global)

User Rules apply to every project you open in Cursor. They are plain text (no frontmatter or special formatting).

**How to set them up:**

1. Open Cursor Settings:
   - **Mac**: `Cmd + ,` (or Cursor menu > Settings)
   - **Linux / Windows**: `Ctrl + ,` (or File menu > Preferences > Settings)
2. Navigate to **Rules** (or search for "Rules" in the settings search bar)
3. Type your global instructions in plain text

**Example user rules:**

```
Always use TypeScript with strict mode.
Prefer functional components in React.
Use 2-space indentation.
Write concise commit messages in imperative mood.
```

These rules are stored in Cursor's internal settings and are not version-controlled.

---

### Project Rules (.cursor/rules/)

Project Rules are the recommended way to customize AI behavior per project. They live in your repository and can be version-controlled with your team.

**Step 1: Create the rules directory**

```bash
# From your project root
mkdir -p .cursor/rules
```

**Step 2: Create a rule file**

You can create rules via the Command Palette or manually:

**Via Command Palette:**
- **Mac**: `Cmd + Shift + P` then type "New Cursor Rule"
- **Linux / Windows**: `Ctrl + Shift + P` then type "New Cursor Rule"

**Manually:**

Create a file in `.cursor/rules/` with a descriptive name. As of Cursor v2.2+, rule files use a directory structure: `.cursor/rules/[rule-name]/RULE.md`. Earlier versions used `.mdc` files directly in `.cursor/rules/`. Both formats are currently supported.

**Step 3: Write the rule with YAML frontmatter**

Each rule file has two parts: YAML frontmatter (metadata) and the rule body (markdown content).

```markdown
---
description: "Enforce project coding standards for TypeScript files"
globs: ["src/**/*.ts", "src/**/*.tsx"]
alwaysApply: false
---

# TypeScript Coding Standards

- Use strict TypeScript with no `any` types
- All functions must have explicit return types
- Use `interface` over `type` for object shapes
- Prefer `const` over `let`
```

**Frontmatter fields:**

| Field | Type | Description |
|-------|------|-------------|
| `description` | String | Brief summary of what the rule does. Used by the AI to decide when to apply the rule. |
| `globs` | String or Array | File patterns that trigger automatic application (e.g., `"*.py"` or `["src/**/*.ts", "*.tsx"]`) |
| `alwaysApply` | Boolean | If `true`, the rule is included in every chat session regardless of file context |

**Rule application types:**

The combination of frontmatter fields determines how the rule is applied:

| Behavior | Configuration |
|----------|---------------|
| **Always Apply** | `alwaysApply: true` |
| **Auto Attached** (file-based) | `globs` set, `alwaysApply: false` |
| **Agent Requested** (intelligent) | `description` set, no `globs`, `alwaysApply: false` -- the AI decides when to use it based on the description |
| **Manual** | No `globs`, `alwaysApply: false`, no `description` -- user must `@mention` the rule in chat |

**Glob pattern examples:**

```
*.ts              # All TypeScript files
src/**/*.tsx      # React components in src/
*.test.js         # Test files
docs/**/*.md      # Documentation files
```

**Editor tip:** Add this to your Cursor settings.json to prevent UI rendering issues when editing rule files:

```json
{
  "workbench.editorAssociations": {
    "*.mdc": "default"
  }
}
```

---

### AGENTS.md (Cross-Platform Standard)

AGENTS.md is an open standard supported by Cursor, GitHub Copilot, OpenAI Codex, Gemini CLI, and other AI coding tools. It is a simple markdown file -- no special frontmatter required.

**Setup:**

Create an `AGENTS.md` file in your project root:

```markdown
# Project Instructions for AI Agents

## Project Overview
This is a Node.js REST API using Express and TypeScript.

## Build and Test Commands
- Install: `npm install`
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Code Style
- Use ESLint with the Airbnb config
- 2-space indentation, single quotes, trailing commas
- All new code must include unit tests

## Architecture
- Routes in `src/routes/`
- Business logic in `src/services/`
- Database queries in `src/repositories/`
```

You can also place `AGENTS.md` files in subdirectories for more specific instructions. The closest file in the directory tree takes precedence.

---

### Legacy .cursorrules File

The `.cursorrules` file in the project root is the original format. It is **deprecated** but still functional. If you have one, consider migrating to `.cursor/rules/` for better organization.

```bash
# Old format (deprecated)
echo "Use TypeScript strict mode" > .cursorrules

# New format (recommended)
mkdir -p .cursor/rules
# Then create rule files as described above
```

---

## Custom Agent Modes

Custom Agent Modes let you create specialized AI assistants with specific tools, models, and instructions. Each mode can have its own permissions and behavior.

### Creating a Custom Mode via the UI

1. Open the Chat panel in Cursor
2. Click the mode selector dropdown (shows "Agent" by default)
3. Select **"Add custom mode"** (or look for a + icon)
4. Configure the mode:
   - **Name**: A descriptive name (e.g., "Code Reviewer", "Test Writer")
   - **Keybinding**: Optional keyboard shortcut for quick access
   - **Model**: Choose which AI model to use
   - **Tools**: Select which tools the agent can use:
     - Codebase Search
     - Read File
     - Edit File
     - Run Commands (terminal)
     - MCP Servers (custom tools)
   - **Custom Instructions**: Add a system prompt that guides the agent's behavior
   - **Auto-run**: Enable to let the agent execute tools without confirmation

### Creating Modes via modes.json

You can also define custom modes in a `.cursor/modes.json` file in your project root for version-controlled, shareable agent configurations:

```json
[
  {
    "name": "Code Reviewer",
    "tools": ["codebase_search", "read_file"],
    "instructions": "You are a code reviewer. Review code for bugs, security issues, and best practices. Never make edits -- only provide feedback.",
    "model": "claude-sonnet-4-20250514"
  },
  {
    "name": "Test Writer",
    "tools": ["codebase_search", "read_file", "edit_file", "run_commands"],
    "instructions": "You write comprehensive test suites. Always run tests after writing them to verify they pass.",
    "model": "claude-sonnet-4-20250514"
  }
]
```

**Best practices for custom modes:**
- Start with minimal tool permissions and add more as needed
- Write specific, detailed instructions rather than vague guidance
- Test the mode iteratively and refine instructions based on results
- Use the mode's custom instructions as a focused "always apply" rule for that agent

---

## MCP Servers (Custom Tools)

MCP (Model Context Protocol) lets you extend Cursor's AI agent with custom tools -- database access, API integrations, file processors, and more.

### Project-Level MCP Config

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "my-database-tool": {
      "command": "npx",
      "args": ["-y", "@my-org/db-mcp-server"],
      "env": {
        "DATABASE_URL": "postgresql://localhost:5432/mydb"
      }
    },
    "file-search": {
      "command": "python",
      "args": ["-m", "mcp_server_search", "--index-path", "./search-index"]
    }
  }
}
```

### Global MCP Config

Create `~/.cursor/mcp.json` in your home directory for tools available in every project:

**Mac / Linux:**
```bash
mkdir -p ~/.cursor
```

Then create `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Windows:**
```powershell
mkdir "$env:USERPROFILE\.cursor" -Force
```

Then create `%USERPROFILE%\.cursor\mcp.json` with the same JSON structure.

### MCP Configuration Fields

| Field | Description |
|-------|-------------|
| `command` | The executable to run (e.g., `npx`, `python`, `node`). Use absolute paths if not in system PATH. |
| `args` | Array of command-line arguments |
| `env` | Environment variables passed to the server process |

### Transport Types

Cursor supports two MCP transport types:

- **stdio** (default): The server runs locally and communicates via standard input/output. Use the `command` + `args` format shown above.
- **Streamable HTTP**: The server runs as an independent process (local or remote) that handles HTTP connections. Configure with a `url` field instead of `command`.

### Verifying MCP Tools

1. Open Cursor Settings > Developer (or Features > MCP)
2. You should see your configured MCP servers listed
3. A green indicator means the server is running and connected
4. In Agent chat, MCP tools will appear in the available tools list

### Security Note

By default, Cursor prompts you to approve each MCP tool execution. You can enable "Yolo mode" in settings to auto-approve, but this is not recommended for untrusted tools.

---

## Platform-Specific Paths

### Project-Level Files (Same on All Platforms)

All project-level configuration lives in the `.cursor/` directory at your project root:

```
your-project/
  .cursor/
    rules/            # Project rules (.mdc files or rule directories)
    mcp.json          # Project MCP server config
    modes.json        # Custom agent modes
  AGENTS.md           # Cross-platform agent instructions
  .cursorrules        # Legacy rules (deprecated)
```

### Global Configuration Paths

| Item | Mac | Linux | Windows |
|------|-----|-------|---------|
| Global MCP config | `~/.cursor/mcp.json` | `~/.cursor/mcp.json` | `%USERPROFILE%\.cursor\mcp.json` |
| User Rules | Cursor Settings UI | Cursor Settings UI | Cursor Settings UI |
| Cursor settings.json | `~/Library/Application Support/Cursor/User/settings.json` | `~/.config/Cursor/User/settings.json` | `%APPDATA%\Cursor\User\settings.json` |

### Keyboard Shortcuts Reference

| Action | Mac | Linux / Windows |
|--------|-----|-----------------|
| Open Settings | `Cmd + ,` | `Ctrl + ,` |
| Command Palette | `Cmd + Shift + P` | `Ctrl + Shift + P` |
| New Cursor Rule | Command Palette > "New Cursor Rule" | Command Palette > "New Cursor Rule" |
| Open Chat Panel | `Cmd + L` | `Ctrl + L` |

---

## Quick-Start Checklist

Here is the fastest path to getting custom rules, agents, and tools working in Cursor:

### 1. Set Global Preferences (one time)

- [ ] Open Cursor Settings (`Cmd/Ctrl + ,`)
- [ ] Go to **Rules** and add your global coding preferences in plain text

### 2. Set Up Project Rules

```bash
# From your project root
mkdir -p .cursor/rules
```

- [ ] Create your first rule file (use Command Palette > "New Cursor Rule" or create manually)
- [ ] Add YAML frontmatter with `description`, `globs`, and `alwaysApply`
- [ ] Write rule instructions in markdown below the frontmatter

### 3. Add an AGENTS.md (Optional, Cross-Platform)

- [ ] Create `AGENTS.md` in your project root with project overview, build commands, and code style

### 4. Configure MCP Tools (Optional)

```bash
# Project-level
mkdir -p .cursor
# Then create .cursor/mcp.json

# Global
mkdir -p ~/.cursor
# Then create ~/.cursor/mcp.json
```

- [ ] Add MCP server entries to the JSON file
- [ ] Verify servers appear in Cursor Settings > Developer

### 5. Create Custom Agent Modes (Optional)

- [ ] Use the Chat panel mode selector > "Add custom mode"
- [ ] Or create `.cursor/modes.json` for version-controlled mode definitions
- [ ] Configure tools, model, and custom instructions for each mode

### 6. Commit Your Configuration

```bash
git add .cursor/rules/ .cursor/mcp.json .cursor/modes.json AGENTS.md
git commit -m "Add Cursor AI configuration"
```

> **Note:** Be careful not to commit secrets. If your `.cursor/mcp.json` contains API keys, add it to `.gitignore` and document the required keys separately.
