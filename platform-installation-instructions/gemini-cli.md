# Gemini CLI: Custom Agents, Skills, and Extensions Setup Guide

Gemini CLI is Google's open-source AI agent that brings the Gemini model directly into your terminal. It supports project-level and global customization through instruction files (GEMINI.md), custom agents (subagents), Agent Skills, extensions, and custom commands.

---

## Table of Contents

1. [Installation](#installation)
2. [Project Instructions with GEMINI.md](#project-instructions-with-geminimd)
3. [Global Configuration (settings.json)](#global-configuration-settingsjson)
4. [Custom Agents (Subagents)](#custom-agents-subagents)
5. [Agent Skills](#agent-skills)
6. [Extensions](#extensions)
7. [Custom Commands](#custom-commands)
8. [Platform-Specific Notes](#platform-specific-notes)

---

## Installation

### Requirements

- **Node.js** 20.0.0 or higher
- **Operating System:** macOS 15+, Windows 11 24H2+, or Ubuntu 20.04+
- **RAM:** 4GB+ for casual use, 16GB+ for large codebases
- Internet connection

### Install via npm (all platforms)

```bash
npm install -g @google/gemini-cli
```

### Install via Homebrew (macOS / Linux)

```bash
brew install gemini-cli
```

### Install via MacPorts (macOS)

```bash
sudo port install gemini-cli
```

### Run without installing

```bash
npx @google/gemini-cli
```

### Launch

After installation, start Gemini CLI by running:

```bash
gemini
```

On first launch, you will be guided through authentication setup.

---

## Project Instructions with GEMINI.md

GEMINI.md files provide persistent instructions, coding standards, and context to the Gemini model. Instead of repeating instructions in every prompt, define them once in a context file.

### How the hierarchy works

Gemini CLI loads context files in three tiers:

1. **Global** -- `~/.gemini/GEMINI.md` -- applies to all your projects
2. **Workspace / Project** -- `GEMINI.md` at your project root or in ancestor directories -- applies to that project
3. **Just-in-Time (JIT)** -- GEMINI.md files in subdirectories -- automatically discovered when tools access files in those directories

More specific files supplement or override more general ones.

### Create a global GEMINI.md

This file applies to every Gemini CLI session on your machine.

**Mac / Linux:**

```bash
mkdir -p ~/.gemini
cat > ~/.gemini/GEMINI.md << 'EOF'
# Global Instructions

- Always use TypeScript with strict mode enabled.
- Follow the Google Style Guide for all languages.
- Write concise commit messages in imperative mood.
EOF
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini"
@"
# Global Instructions

- Always use TypeScript with strict mode enabled.
- Follow the Google Style Guide for all languages.
- Write concise commit messages in imperative mood.
"@ | Set-Content "$env:USERPROFILE\.gemini\GEMINI.md"
```

### Create a project-level GEMINI.md

Place this file at the root of your project. It applies only when you run `gemini` from within that project.

```bash
cat > ./GEMINI.md << 'EOF'
# Project: My Web App

## Tech Stack
- Next.js 15 with App Router
- Tailwind CSS
- PostgreSQL with Prisma ORM

## Coding Standards
- Use server components by default; only use "use client" when necessary.
- All API routes must validate input with Zod.
- Write tests for all new utilities.
EOF
```

You can also use `/init` inside Gemini CLI to auto-generate a starting GEMINI.md for your project.

### Subdirectory context (JIT)

Place a GEMINI.md inside any subdirectory to provide component-specific instructions:

```
my-project/
├── GEMINI.md                  # Project-wide instructions
├── src/
│   ├── api/
│   │   └── GEMINI.md          # API-specific patterns and conventions
│   └── components/
│       └── GEMINI.md          # UI component guidelines
```

### File imports

Use `@filename.md` syntax inside any GEMINI.md to modularize large instruction sets:

```markdown
# Project Instructions

@coding-standards.md
@api-conventions.md
```

### Custom context file names

If you prefer a different filename (e.g., AGENTS.md), configure it in your settings.json:

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

### Useful commands

| Command | Description |
|---------|-------------|
| `/memory show` | Display all loaded context |
| `/memory refresh` | Reload all GEMINI.md files |
| `/memory add <text>` | Append text to your global GEMINI.md |

---

## Global Configuration (settings.json)

The settings.json file controls Gemini CLI behavior. There are two levels:

- **User settings:** `~/.gemini/settings.json` -- applies to all sessions
- **Project settings:** `.gemini/settings.json` -- applies only to that project (higher precedence)

### Configuration precedence (lowest to highest)

1. Default values
2. System defaults (`/etc/gemini-cli/settings.json`)
3. User settings (`~/.gemini/settings.json`)
4. Project settings (`.gemini/settings.json`)
5. Environment variables
6. Command-line arguments

### Example settings.json

```json
{
  "theme": "dark",
  "experimental": {
    "enableAgents": true,
    "skills": true
  },
  "sandbox": true
}
```

### Environment variables

Create a `.env` file for API keys and sensitive values:

- **Global:** `~/.gemini/.env`
- **Project:** `.gemini/.env`

```env
GOOGLE_API_KEY=your-api-key-here
GOOGLE_CLOUD_PROJECT=your-project-id
```

Settings values can also reference environment variables using `$VAR_NAME` or `${VAR_NAME}` syntax.

### In-app settings

Use the `/settings` command inside Gemini CLI to browse and modify settings interactively. Categories include:

- **General:** Approval mode, auto-update, notifications
- **Output & UI:** Theme, footer visibility, inline thinking
- **Model Behavior:** Max session turns, compression threshold
- **Context Management:** Memory discovery, file filtering
- **Tools:** Shell preferences, output truncation
- **Security:** YOLO mode, extension source validation, folder trust
- **Skills & Hooks:** Agent Skills toggle, hooks system

---

## Custom Agents (Subagents)

Subagents are specialized agents that operate within your main Gemini CLI session. They handle specific tasks -- like code review, documentation lookup, or security auditing -- with their own context window and system prompt.

### Enable subagents

Add this to your `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

### Where to place agent files

- **Project-level (shared with team):** `.gemini/agents/*.md`
- **User-level (personal):** `~/.gemini/agents/*.md`

### Agent file format

Each agent is a Markdown file with YAML frontmatter:

```markdown
---
name: code-reviewer
description: Expert at reviewing code for bugs, style issues, and best practices. Use when the user asks to review or critique code changes.
kind: local
tools:
  - read_file
  - search_files
  - web_search
model: gemini-2.5-pro
temperature: 0.2
max_turns: 10
---

# Code Reviewer

You are a senior software engineer performing a code review.

## Review Process

1. Read through all changed files carefully.
2. Check for bugs, logic errors, and edge cases.
3. Verify coding style matches the project conventions.
4. Look for security vulnerabilities (OWASP Top 10).
5. Suggest improvements with specific code examples.

## Output Format

For each finding, provide:
- **File and line number**
- **Severity** (critical / warning / suggestion)
- **Description** of the issue
- **Suggested fix** with code snippet
```

### Frontmatter fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier (lowercase, hyphens/underscores only) |
| `description` | string | Yes | Explains what the agent does and when to use it |
| `kind` | string | No | `local` (default) or `remote` (A2A protocol) |
| `tools` | array | No | List of allowed tool names |
| `model` | string | No | Specific model to use; defaults to main session model |
| `temperature` | number | No | Creativity (0.0 to 2.0) |
| `max_turns` | number | No | Max conversation turns (default: 15) |
| `timeout_mins` | number | No | Execution time limit in minutes (default: 5) |

### How subagents work

The main Gemini agent sees your custom agents as available tools. When it detects a task matching an agent's description, it delegates the work to that specialist. Each subagent maintains its own separate context window.

### Built-in subagents

Gemini CLI includes these built-in agents:

- **codebase_investigator** -- Analyzes codebases and reverse-engineers dependencies
- **cli_help** -- Expert knowledge about Gemini CLI commands and configuration
- **generalist_agent** -- Routes tasks to appropriate specialized subagents

### Step-by-step: Create your first custom agent

1. Enable agents in settings:
   ```bash
   # Mac / Linux
   mkdir -p ~/.gemini
   echo '{ "experimental": { "enableAgents": true } }' > ~/.gemini/settings.json
   ```

   ```powershell
   # Windows (PowerShell)
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini"
   '{ "experimental": { "enableAgents": true } }' | Set-Content "$env:USERPROFILE\.gemini\settings.json"
   ```

2. Create the agents directory:
   ```bash
   # Project-level
   mkdir -p .gemini/agents

   # Or user-level (global)
   mkdir -p ~/.gemini/agents
   ```

3. Create an agent file (e.g., `.gemini/agents/test-writer.md`):
   ```markdown
   ---
   name: test-writer
   description: Writes comprehensive unit tests. Use when the user asks to add tests, improve coverage, or create test files.
   tools:
     - read_file
     - write_file
     - run_shell_command
   max_turns: 15
   ---

   # Test Writer

   You write thorough unit tests following best practices.

   ## Guidelines
   - Use the project's existing test framework.
   - Cover happy paths, edge cases, and error conditions.
   - Use descriptive test names that explain the expected behavior.
   - Mock external dependencies.
   ```

4. Start Gemini CLI and test it:
   ```
   gemini
   > Write tests for the user authentication module
   ```

---

## Agent Skills

Agent Skills are self-contained packages of specialized expertise. Unlike GEMINI.md (always-on context), skills activate on demand when Gemini detects a matching task, which saves tokens.

### Enable skills

Add this to your settings.json:

```json
{
  "experimental": {
    "skills": true
  }
}
```

### Where to place skills

Skills are discovered in three tiers (workspace takes precedence):

1. **Workspace (project-level):** `.gemini/skills/` or `.agents/skills/`
2. **User (global):** `~/.gemini/skills/` or `~/.agents/skills/`
3. **Extension:** Bundled within installed extensions

The `.agents/skills/` alias takes priority within each tier.

### Skill directory structure

```
.gemini/skills/my-skill/
├── SKILL.md           # Required: skill definition
├── scripts/           # Optional: executable scripts
├── references/        # Optional: documentation and reference materials
└── assets/            # Optional: templates and resource files
```

### SKILL.md format

```markdown
---
name: api-auditor
description: Expertise in auditing and testing API endpoints. Use when the user asks to "check", "test", or "audit" a URL or API.
---

# API Auditor

You are an expert at testing and auditing API endpoints.

## Audit Process

1. Send requests to the target endpoint using the bundled audit script.
2. Check response status codes, headers, and body structure.
3. Verify authentication and authorization requirements.
4. Test for common API vulnerabilities.
5. Generate a structured report of findings.

## Output Format

Provide results as a markdown table with columns: Endpoint, Method, Status, Issue, Severity.
```

### How skills activate

1. Gemini loads skill names and descriptions into the system prompt (lightweight).
2. When your request matches a skill's description, Gemini calls `activate_skill`.
3. You see a consent prompt showing the skill's purpose and file access.
4. After you approve, the full SKILL.md and directory contents are injected into the conversation.
5. The model executes using the specialized guidance from the skill.

### Step-by-step: Create your first skill

1. Enable skills in settings:
   ```json
   {
     "experimental": {
       "skills": true
     }
   }
   ```

2. Create the skill directory:
   ```bash
   mkdir -p .gemini/skills/code-documenter
   ```

3. Create `.gemini/skills/code-documenter/SKILL.md`:
   ```markdown
   ---
   name: code-documenter
   description: Generates comprehensive documentation for code. Use when the user asks to "document", "add docs", or "explain" a module or function.
   ---

   # Code Documenter

   You generate clear, thorough documentation for code.

   ## Process
   1. Read the target code files.
   2. Identify public APIs, classes, and functions.
   3. Generate JSDoc/docstring comments for each.
   4. Create a README section summarizing the module's purpose and usage.
   ```

4. Optionally add supporting resources:
   ```bash
   mkdir -p .gemini/skills/code-documenter/references
   mkdir -p .gemini/skills/code-documenter/assets
   ```

5. Verify the skill is detected:
   ```
   gemini
   > /skills list
   ```

6. Test by triggering the skill:
   ```
   > Document the authentication module
   ```

### Managing skills

**Inside Gemini CLI:**

| Command | Description |
|---------|-------------|
| `/skills list` | View all available skills |
| `/skills enable <name>` | Enable a specific skill |
| `/skills disable <name>` | Disable a specific skill |
| `/skills link <path>` | Symlink an external skill directory |

**From the terminal:**

```bash
gemini skills install <git-repo-url>    # Install from Git repo
gemini skills install <local-path>       # Install from local path
gemini skills uninstall <name>           # Remove a skill
gemini skills link <path>                # Symlink a skill collection
```

### Tip: Use the skill-creator skill

The fastest way to create a new skill is to ask Gemini itself:

```
gemini
> Create a new skill called "security-scanner"
```

Gemini will generate the directory structure, SKILL.md, and standard resource folders automatically.

---

## Extensions

Extensions are packages that add tools, commands, skills, and context to Gemini CLI using the Model Context Protocol (MCP).

### Extension directory structure

```
my-extension/
├── gemini-extension.json    # Required: manifest file
├── GEMINI.md                # Optional: persistent context/instructions
├── package.json             # Dependencies (for Node.js-based tools)
├── example.js               # MCP server implementation
├── commands/                # Optional: custom commands
│   └── deploy.toml
└── skills/                  # Optional: bundled skills
    └── audit/
        └── SKILL.md
```

### Manifest file (gemini-extension.json)

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A short description of what the extension does",
  "contextFileName": "GEMINI.md",
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${extensionPath}${/}dist${/}server.js"],
      "cwd": "${extensionPath}"
    }
  },
  "excludeTools": []
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Lowercase identifier with dashes (must match directory name) |
| `version` | Semantic version |
| `description` | Short summary |
| `mcpServers` | Map of MCP server configurations |
| `contextFileName` | Context file name (default: `GEMINI.md`); can be an array |
| `excludeTools` | Tool names to block from the model |
| `settings` | User-configurable settings (stored in keychain if `sensitive: true`) |

**Variable substitution in paths:**

| Variable | Meaning |
|----------|---------|
| `${extensionPath}` | Absolute path to the extension directory |
| `${workspacePath}` | Absolute path to the current workspace |
| `${/}` | Platform-specific path separator |

### Where to place extensions

- **Project-level:** `.gemini/extensions/my-extension/`
- **User-level (global):** `~/.gemini/extensions/my-extension/`

### Creating an extension step by step

1. Generate a template:
   ```bash
   gemini extensions new my-extension mcp-server
   ```

2. Navigate to the extension and install dependencies:
   ```bash
   cd .gemini/extensions/my-extension
   npm install
   ```

3. Edit `example.js` to define your tools using the MCP SDK:
   ```javascript
   import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
   import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
   import { z } from 'zod';

   const server = new McpServer({
     name: 'my-tools',
     version: '1.0.0',
   });

   server.registerTool('hello_world', {
     description: 'Returns a greeting message.',
     inputSchema: z.object({
       name: z.string().describe('Name to greet'),
     }).shape,
   }, async ({ name }) => ({
     content: [{ type: 'text', text: `Hello, ${name}!` }],
   }));

   const transport = new StdioServerTransport();
   await server.connect(transport);
   ```

4. Link the extension for local development:
   ```bash
   gemini extensions link .
   ```

5. Test in Gemini CLI:
   ```
   gemini
   > Say hello to Claude
   ```

### Managing extensions

```bash
gemini extensions list                  # List installed extensions
gemini extensions link <path>           # Link a local extension
gemini extensions config <name>         # Update extension settings
gemini extensions new <name> <template> # Generate from template
```

---

## Custom Commands

Custom commands are shortcuts that expand into full prompts. They are defined as TOML files.

### Where to place commands

- **Global:** `~/.gemini/commands/`
- **Project-level:** `.gemini/commands/`
- **Inside extensions:** `<extension>/commands/`

### Command file format

Create a TOML file (e.g., `~/.gemini/commands/review.toml`):

```toml
prompt = """Review the following code for bugs, style issues, and performance problems.
Focus on:
- Logic errors and edge cases
- Security vulnerabilities
- Performance bottlenecks

Files to review: {{args}}"""
```

Use it in Gemini CLI with:

```
/review src/auth.ts
```

### Nested commands (namespacing)

Directory structure determines command names:

```
commands/
├── review.toml            # /review
├── git/
│   ├── squash.toml        # /git:squash
│   └── changelog.toml     # /git:changelog
└── test/
    └── coverage.toml      # /test:coverage
```

### Shell command integration

Commands can embed shell output:

```toml
prompt = """Summarize the git changes:
!{git diff --stat}

Detailed diff:
!{git diff}"""
```

The `!{...}` syntax runs a shell command and injects its output into the prompt.

---

## Platform-Specific Notes

### Mac

- Install with Homebrew (`brew install gemini-cli`) or npm.
- Config directory: `~/.gemini/`
- Uses Bash or Zsh shell.
- MacPorts also available: `sudo port install gemini-cli`

### Linux

- Install with Homebrew or npm.
- Config directory: `~/.gemini/`
- Requires Node.js 20+ (install via your package manager or nvm).
- Ubuntu 20.04+ recommended.

### Windows

- Install with npm: `npm install -g @google/gemini-cli`
- Config directory: `%USERPROFILE%\.gemini\` (e.g., `C:\Users\YourName\.gemini\`)
- Use PowerShell or Windows Terminal.
- Windows 11 24H2+ required.
- All path examples using `~/.gemini/` translate to `%USERPROFILE%\.gemini\` on Windows.

### Quick reference: File locations

| Item | Mac / Linux | Windows |
|------|-------------|---------|
| Global config | `~/.gemini/settings.json` | `%USERPROFILE%\.gemini\settings.json` |
| Global context | `~/.gemini/GEMINI.md` | `%USERPROFILE%\.gemini\GEMINI.md` |
| Global agents | `~/.gemini/agents/*.md` | `%USERPROFILE%\.gemini\agents\*.md` |
| Global skills | `~/.gemini/skills/` | `%USERPROFILE%\.gemini\skills\` |
| Global commands | `~/.gemini/commands/` | `%USERPROFILE%\.gemini\commands\` |
| Global extensions | `~/.gemini/extensions/` | `%USERPROFILE%\.gemini\extensions\` |
| Global env vars | `~/.gemini/.env` | `%USERPROFILE%\.gemini\.env` |
| Project config | `.gemini/settings.json` | `.gemini\settings.json` |
| Project context | `GEMINI.md` (project root) | `GEMINI.md` (project root) |
| Project agents | `.gemini/agents/*.md` | `.gemini\agents\*.md` |
| Project skills | `.gemini/skills/` | `.gemini\skills\` |
| Project commands | `.gemini/commands/` | `.gemini\commands\` |
| Project extensions | `.gemini/extensions/` | `.gemini\extensions\` |
| Project env vars | `.gemini/.env` | `.gemini\.env` |
