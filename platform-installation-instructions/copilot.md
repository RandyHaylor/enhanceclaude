# GitHub Copilot: Custom Instructions, Agents, and Skills Setup Guide

This guide covers how to set up project-level and global custom instructions, agents, prompt files (skills), and MCP server integrations for GitHub Copilot. Instructions are provided for Mac, Linux, and Windows.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Custom Instructions (Project-Level and Global)](#2-custom-instructions-project-level-and-global)
3. [Custom Agents](#3-custom-agents)
4. [Prompt Files (Reusable Skills / Slash Commands)](#4-prompt-files-reusable-skills--slash-commands)
5. [MCP Server Integration](#5-mcp-server-integration)
6. [Copilot CLI Agents](#6-copilot-cli-agents)
7. [Quick Reference](#7-quick-reference)

---

## 1. Prerequisites

- **GitHub Copilot subscription**: Individual, Pro, Pro+, Business, or Enterprise
- **IDE**: VS Code, JetBrains IDE, Visual Studio, Eclipse, or Xcode
- **GitHub Copilot extension** installed in your IDE
- For CLI features: GitHub Copilot CLI installed (`gh copilot` or standalone `copilot`)

---

## 2. Custom Instructions (Project-Level and Global)

Custom instructions tell Copilot about your project's coding standards, conventions, and preferences. They are automatically included in every chat request.

### Priority Order (Highest to Lowest)

1. Personal instructions (user-level settings)
2. Repository instructions (`.github/copilot-instructions.md` or `AGENTS.md`)
3. Organization instructions

---

### 2a. Repository-Wide Instructions

These apply to everyone working in the repository.

**Step 1**: Create the instructions file at the root of your repository:

```
your-repo/
  .github/
    copilot-instructions.md
```

**Step 2**: Add your instructions in Markdown format:

```markdown
## Coding Standards

- Use TypeScript for all new files
- Follow the Airbnb style guide
- Write unit tests for all public functions
- Use descriptive variable names, no abbreviations
- Prefer functional components with hooks in React
```

**Step 3**: Enable instruction files in your IDE:

| IDE | How to Enable |
|-----|---------------|
| **VS Code** | Settings > search "instruction file" > enable "Code Generation: Use Instruction Files" |
| **Visual Studio** | Tools > Options > search "custom instructions" > check the enable box |
| **JetBrains** | File > Settings > Tools > GitHub Copilot > Customizations |

**Step 4**: Verify it works. In Copilot Chat, ask a question. Check the "References" list in the response -- the instructions file should appear if it was included.

---

### 2b. Path-Specific Instructions

These apply only to files matching a glob pattern.

**Step 1**: Create instruction files in `.github/instructions/`:

```
your-repo/
  .github/
    instructions/
      python-style.instructions.md
      react-components.instructions.md
      api-routes.instructions.md
```

**Step 2**: Add YAML frontmatter with an `applyTo` pattern:

```markdown
---
applyTo: "**/*.py"
---

# Python Standards

- Use type hints on all function signatures
- Follow PEP 8 naming conventions
- Use dataclasses instead of plain dicts for structured data
- Write docstrings in Google style format
```

More `applyTo` examples:

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files recursively |
| `src/**/*.py` | Python files in the `src/` directory |
| `app/models/**/*.rb` | Ruby files in `app/models/` |
| `**/*.test.js` | All JavaScript test files |

---

### 2c. Personal / User-Level Instructions (Global)

These are your personal preferences that apply across all repositories.

#### In VS Code Settings

**Step 1**: Open settings:
- **Mac**: `Cmd + ,`
- **Linux / Windows**: `Ctrl + ,`

**Step 2**: Search for `github.copilot.chat.codeGeneration.instructions`

**Step 3**: Click "Edit in settings.json" and add your instructions:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Always use const instead of let when the variable is not reassigned. Prefer arrow functions. Use early returns to reduce nesting."
    }
  ]
}
```

You can also point to an external file:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": "/absolute/path/to/my-instructions.md"
    }
  ]
}
```

#### Other Instruction Settings

You can customize instructions for specific Copilot features:

| Setting | Purpose |
|---------|---------|
| `github.copilot.chat.codeGeneration.instructions` | Code generation preferences |
| `github.copilot.chat.commitMessageGeneration.instructions` | Commit message style |
| `github.copilot.chat.pullRequestDescriptionGeneration.instructions` | PR description format |
| `github.copilot.chat.reviewSelection.instructions` | Code review behavior |
| `github.copilot.chat.testGeneration.instructions` | Test generation preferences |

Each accepts an array of objects with either a `text` or `file` property.

#### Settings File Locations

| Platform | User Settings Path |
|----------|--------------------|
| **Mac** | `~/Library/Application Support/Code/User/settings.json` |
| **Linux** | `~/.config/Code/User/settings.json` |
| **Windows** | `%APPDATA%\Code\User\settings.json` |

---

### 2d. Organization-Level Instructions

If your GitHub organization has defined custom instructions, enable them in VS Code:

```json
{
  "github.copilot.chat.organizationInstructions.enabled": true
}
```

Organization admins configure these through GitHub organization settings.

---

## 3. Custom Agents

Custom agents are specialized AI personas with defined expertise, tool access, and behavioral instructions. They let you create focused assistants for specific tasks like testing, security review, or documentation.

### 3a. Project-Level Agents (Workspace)

**Step 1**: Create a `.github/agents/` directory in your repository:

```
your-repo/
  .github/
    agents/
      test-writer.agent.md
      security-reviewer.agent.md
      doc-generator.agent.md
```

**Step 2**: Write an agent profile with YAML frontmatter and Markdown instructions.

Example -- `test-writer.agent.md`:

```markdown
---
description: "Writes comprehensive unit and integration tests"
tools:
  - read
  - edit
  - search
  - execute
---

# Test Writer Agent

You are a testing specialist. Your job is to write thorough tests for the codebase.

## Rules

- Always check existing test patterns in the project before writing new tests
- Use the project's existing test framework (detect from package.json, requirements.txt, etc.)
- Write both positive and negative test cases
- Include edge cases and boundary conditions
- Never modify production code -- only create or update test files
```

#### YAML Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Brief explanation of the agent's purpose (shown as placeholder text) |
| `name` | No | Display name (defaults to filename) |
| `tools` | No | List of allowed tools; omit to grant all tools |
| `model` | No | AI model to use (e.g., `claude-opus-4-6`, `gpt-4o`) |
| `agents` | No | List of subagents this agent can invoke |
| `user-invokable` | No | Whether it appears in the agent dropdown (default: `true`) |
| `disable-model-invocation` | No | Prevents automatic selection; must be manually invoked |
| `handoffs` | No | Define sequential workflow transitions to other agents |

#### Available Tool Names

| Tool | Aliases | What It Does |
|------|---------|--------------|
| `execute` | `shell`, `bash`, `powershell` | Run terminal commands |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write` | Modify files |
| `search` | `Grep`, `Glob` | Search files and text |
| `agent` | `custom-agent`, `Task` | Invoke other agents |
| `web` | `WebSearch`, `WebFetch` | Web access |

Use `["*"]` to grant all tools, or `[]` to grant none.

For MCP server tools, use: `mcp-server-name/*` or `mcp-server-name/specific-tool`

**Step 3**: Commit and push the files. Restart your IDE or reload the Copilot Chat window.

**Step 4**: Use the agent. In Copilot Chat, click the agents dropdown at the bottom and select your custom agent.

---

### 3b. User-Level Agents (Global, All Workspaces)

#### In VS Code

**Step 1**: Open the Chat view and select "Configure Custom Agents..." from the agents dropdown.

**Step 2**: Click "Create new custom agent" and choose "User profile" as the location.

This stores the agent in your VS Code user profile's agents folder so it is available across all workspaces.

#### In JetBrains IDEs

Open Copilot Chat > agents dropdown > "Configure Agents..." > select your preferred scope.

---

### 3c. Organization-Level Agents

Organization agents are shared across all repositories in a GitHub organization.

**Step 1**: In your organization's `.github-private` repository (or `.github` repository), create an `agents/` directory.

**Step 2**: Add `.agent.md` files just like project-level agents.

**Step 3**: Enable in VS Code:

```json
{
  "github.copilot.chat.organizationCustomAgents.enabled": true
}
```

These agents appear alongside personal and workspace agents in the dropdown.

---

### 3d. Agent Handoffs (Workflows)

You can chain agents together for multi-step workflows:

```markdown
---
description: "Plans implementation before coding"
tools:
  - read
  - search
handoffs:
  - label: "Start Implementation"
    agent: implementation
    prompt: "Implement the plan outlined above."
    send: false
---

# Planning Agent

Review the codebase and create a detailed implementation plan.
Do not write any code. Only produce the plan.
```

The `send: false` setting shows a button for the user to click, rather than automatically transitioning.

---

## 4. Prompt Files (Reusable Skills / Slash Commands)

Prompt files are reusable prompts you invoke with `/` in chat. They act like saved commands for common tasks.

**Supported IDEs**: VS Code, Visual Studio, JetBrains

### 4a. Project-Level Prompt Files

**Step 1**: Create a `.github/prompts/` directory in your repository:

```
your-repo/
  .github/
    prompts/
      create-component.prompt.md
      review-security.prompt.md
      generate-docs.prompt.md
```

**Step 2**: Write the prompt file with optional YAML frontmatter:

Example -- `create-component.prompt.md`:

```markdown
---
description: "Generate a new React component with tests"
agent: "agent"
model: "gpt-4o"
tools:
  - githubRepo
  - search
---

Create a new React component based on the following requirements.

## Rules
- Use TypeScript with proper type definitions
- Create a corresponding test file
- Follow the project's existing component patterns in ${workspaceFolder}/src/components
- Use the project's CSS approach (detect from existing files)

## Input
Component name and requirements: ${input:componentName:Enter component name and requirements}
```

#### YAML Frontmatter Fields

| Field | Description |
|-------|-------------|
| `description` | Brief explanation shown in the prompt picker |
| `name` | Display name after `/` (defaults to filename) |
| `argument-hint` | Placeholder text shown in the chat input |
| `agent` | Agent mode: `ask`, `agent`, `plan`, or a custom agent name |
| `model` | AI model to use |
| `tools` | List of available tools |

#### Available Variables

| Variable | Description |
|----------|-------------|
| `${workspaceFolder}` | Workspace root path |
| `${file}` | Current file path |
| `${fileBasename}` | Current filename |
| `${fileDirname}` | Current file's directory |
| `${selection}` | Currently selected text |
| `${input:name}` | Prompt user for input |
| `${input:name:hint}` | Prompt with placeholder hint |

**Step 3**: Use the prompt. In Copilot Chat, type `/` followed by the prompt name:

```
/create-component
```

You can also add extra context:

```
/create-component UserProfile with avatar, name, and bio fields
```

---

### 4b. User-Level Prompt Files (Global)

**Step 1**: In VS Code, open the Command Palette:
- **Mac**: `Cmd + Shift + P`
- **Linux / Windows**: `Ctrl + Shift + P`

**Step 2**: Run "Chat: New Prompt File"

**Step 3**: Choose "User profile" as the location.

This saves the prompt in your VS Code profile's `prompts/` folder, making it available in all workspaces.

**Step 4**: To sync across devices, run "Settings Sync: Configure" and enable "Prompts and Instructions".

---

## 5. MCP Server Integration

MCP (Model Context Protocol) servers extend Copilot with external tools and data sources.

### 5a. Installing from the MCP Marketplace (VS Code)

**Step 1**: Open the Extensions panel:
- **Mac**: `Cmd + Shift + X`
- **Linux / Windows**: `Ctrl + Shift + X`

**Step 2**: If this is your first time, follow the prompts to enable the MCP Servers Marketplace.

**Step 3**: Search for the MCP server you want (e.g., "github") and click "Install" on its configuration page.

### 5b. Manual MCP Server Configuration

#### In VS Code (Workspace Level)

Create or edit `.vscode/mcp.json` in your project:

```json
{
  "servers": {
    "my-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": {
        "API_KEY": "${input:apiKey}"
      }
    }
  }
}
```

#### In VS Code (User Level)

Add to your user `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "my-mcp-server": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@my-org/my-mcp-server"]
      }
    }
  }
}
```

#### In Custom Agent Profiles (Organization/Enterprise Level Only)

```yaml
---
description: "Agent with custom MCP tools"
mcp-servers:
  custom-mcp:
    type: "local"
    command: "some-command"
    args: ["--arg1", "--arg2"]
    tools: ["*"]
    env:
      API_KEY: ${{ secrets.MCP_API_KEY }}
---
```

Note: MCP servers in agent profiles are only available at the organization/enterprise level, not in repository-level agent profiles.

### 5c. Authentication for GitHub MCP Server

The GitHub MCP server supports two authentication methods:

- **OAuth** (recommended): Follow the prompts when first connecting
- **Personal Access Token (PAT)**: Configure the token in your MCP server settings

### 5d. Using MCP Tools in Agents and Prompts

Reference MCP tools in your agent or prompt files:

```yaml
tools:
  - my-mcp-server/*           # All tools from this server
  - my-mcp-server/specific-tool  # One specific tool
```

Or reference in Markdown with: `#tool:my-mcp-server/tool-name`

---

## 6. Copilot CLI Agents

GitHub Copilot CLI supports its own custom agents for terminal-based workflows.

### 6a. File Locations

| Scope | Path |
|-------|------|
| **Project** | `.github/agents/` in your repository |
| **User (global)** | See table below |

| Platform | Global Agents Path |
|----------|--------------------|
| **Mac** | `~/.config/copilot/agents/` |
| **Linux** | `~/.config/copilot/agents/` |
| **Windows** | `%USERPROFILE%\.config\copilot\agents\` |

Note: If an agent with the same name exists in both locations, the user-level (home directory) version takes precedence.

### 6b. Creating a CLI Agent

**Option 1 -- Interactive (AI-Assisted)**:

1. Start Copilot CLI in interactive mode
2. Type `/agent`
3. Select "Create new agent"
4. Describe the agent's expertise and Copilot generates the profile

**Option 2 -- Manual**:

Create a file like `~/.config/copilot/agents/security-auditor.agent.md`:

```markdown
---
description: "Reviews code for security vulnerabilities"
tools:
  - read
  - search
---

# Security Auditor

You are a security specialist. Analyze code for common vulnerabilities including:
- SQL injection
- XSS
- Authentication flaws
- Insecure dependencies
- Hardcoded secrets

Report findings with severity levels and remediation steps.
```

After creating the file, restart the CLI to load the new agent.

### 6c. Using CLI Agents

Four ways to invoke:

1. **Slash command**: Type `/agent` in interactive mode, then select the agent
2. **Direct instruction**: "Use the security-auditor agent on all files in /src/app"
3. **Automatic inference**: Copilot selects the agent based on your prompt's context
4. **Command line flag**: `copilot --agent security-auditor --prompt "Check /src/app"`

---

## 7. Quick Reference

### File Structure Overview

```
your-repo/
  .github/
    copilot-instructions.md          # Repository-wide instructions
    instructions/
      python.instructions.md         # Path-specific instructions
      react.instructions.md
    agents/
      test-writer.agent.md           # Custom agents
      security-reviewer.agent.md
    prompts/
      create-component.prompt.md     # Reusable prompt files (slash commands)
      review-security.prompt.md
  .vscode/
    mcp.json                         # MCP server config (VS Code)
```

### User-Level Files

| Feature | Mac / Linux | Windows |
|---------|-------------|---------|
| VS Code settings | `~/.config/Code/User/settings.json` (Linux) or `~/Library/Application Support/Code/User/settings.json` (Mac) | `%APPDATA%\Code\User\settings.json` |
| CLI agents | `~/.config/copilot/agents/` | `%USERPROFILE%\.config\copilot\agents\` |
| VS Code profile agents | Managed through VS Code profile | Managed through VS Code profile |
| VS Code profile prompts | Managed through VS Code profile | Managed through VS Code profile |

### Key VS Code Settings

| Setting | Purpose |
|---------|---------|
| `github.copilot.chat.codeGeneration.instructions` | Personal code generation preferences |
| `github.copilot.chat.organizationInstructions.enabled` | Enable organization instructions |
| `github.copilot.chat.organizationCustomAgents.enabled` | Enable organization agents |
| `chat.includeApplyingInstructions` | Enable path-specific instructions |
| `chat.useAgentsMdFile` | Enable AGENTS.md support |

### Feature Availability by IDE

| Feature | VS Code | JetBrains | Visual Studio | Eclipse | Xcode | GitHub.com | CLI |
|---------|---------|-----------|---------------|---------|-------|------------|-----|
| Repository instructions | Yes | Yes | Yes | Yes | Yes | Yes | -- |
| Path-specific instructions | Yes | Yes | Yes | -- | -- | -- | -- |
| Personal instructions (settings) | Yes | Yes | Yes | -- | -- | -- | -- |
| Custom agents | Yes | Preview | -- | Preview | Preview | Yes | Yes |
| Prompt files | Yes | Yes | Yes | -- | -- | -- | -- |
| MCP servers | Yes | Yes | Yes | Yes | Yes | -- | Yes |

---

## Tips

- Keep instruction files concise. Short, focused statements work better than long paragraphs.
- Include code examples in instructions to show preferred and avoided patterns.
- Explain the "why" behind conventions -- Copilot makes better decisions when it understands the reasoning.
- Test instructions incrementally. Check the References list in chat responses to verify your files are being picked up.
- Use path-specific instructions to avoid cluttering the main instructions file with language-specific rules.
- Custom agents work best when given a focused scope. A "test writer" agent is more effective than a "do everything" agent.
