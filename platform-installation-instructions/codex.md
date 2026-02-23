# OpenAI Codex CLI -- Custom Agents and Skills Setup Guide

OpenAI Codex CLI is a terminal-based AI coding agent that runs in your terminal. It can read your repository, edit files, and run commands in a conversational workflow. Codex is included with ChatGPT Plus, Pro, Business, Edu, and Enterprise plans.

This guide covers how to install Codex CLI, configure it, and set up project-level and global custom agents and skills.

---

## Table of Contents

1. [Installation](#installation)
2. [Authentication](#authentication)
3. [Global Configuration](#global-configuration)
4. [Project-Level Instructions with AGENTS.md](#project-level-instructions-with-agentsmd)
5. [Custom Agent Skills](#custom-agent-skills)
6. [MCP Server Integration](#mcp-server-integration)
7. [Profiles](#profiles)
8. [Useful Slash Commands](#useful-slash-commands)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- **Node.js 18 or later** is required for the npm installation method.
- A **ChatGPT Plus, Pro, Business, Edu, or Enterprise** account, or OpenAI API credits.

### Mac

**Option A -- Homebrew (recommended):**

```bash
brew install codex
```

**Option B -- npm:**

```bash
npm install -g @openai/codex
```

**Option C -- Desktop App:**

Download the Codex desktop app for Apple Silicon Macs from [openai.com/codex](https://openai.com/codex/).

### Linux

```bash
npm install -g @openai/codex
```

### Windows

Windows support is experimental. The recommended approach is to use WSL (Windows Subsystem for Linux).

**Step 1 -- Install WSL:**

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

Restart your computer if prompted, then open WSL:

```powershell
wsl
```

**Step 2 -- Install Node.js inside WSL:**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc
nvm install 22
```

**Step 3 -- Install Codex CLI:**

```bash
npm install -g @openai/codex
```

**Windows tips:**
- Store your repositories in the Linux home directory (`~/code/`) rather than `/mnt/c/` for better performance.
- Access WSL files from Windows Explorer at `\\wsl$\Ubuntu\home\<your-username>`.

### Verify Installation

```bash
codex --version
```

---

## Authentication

The first time you run `codex`, you will be prompted to sign in.

**Option A -- ChatGPT account (recommended):**

```bash
codex
```

Select "Sign in with ChatGPT" and follow the browser flow.

**Option B -- API key:**

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."
```

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to persist it.

---

## Global Configuration

Codex stores its configuration in `~/.codex/`. The main configuration file is `~/.codex/config.toml`.

### Config File Location

| Level | Path | Purpose |
|-------|------|---------|
| User (global) | `~/.codex/config.toml` | Your personal defaults |
| Project | `.codex/config.toml` | Project-specific overrides |
| System | `/etc/codex/config.toml` | System-wide defaults (Unix) |

### Configuration Precedence

Settings are resolved from highest to lowest priority:

1. CLI flags (e.g., `--model gpt-5.2`)
2. Profile values (via `--profile <name>`)
3. Project config (`.codex/config.toml`)
4. User config (`~/.codex/config.toml`)
5. System config
6. Built-in defaults

### Create Your Global Config

Create or edit `~/.codex/config.toml`:

```toml
#:schema https://developers.openai.com/codex/config-schema.json

# Default model
model = "gpt-5.3-codex"

# Approval policy: "untrusted", "on-request", or "never"
approval_policy = "on-request"

# Sandbox mode: "read-only", "workspace-write", or "danger-full-access"
sandbox_mode = "workspace-write"

# Reasoning effort: "minimal", "low", "medium", "high", or "xhigh"
model_reasoning_effort = "high"

# Communication style: "friendly", "pragmatic", or "none"
personality = "friendly"

# Web search: "disabled", "cached", or "live"
web_search = "cached"
```

### Common Config Options

| Key | Values | Default | Description |
|-----|--------|---------|-------------|
| `model` | Model ID string | `gpt-5.3-codex` | Which model to use |
| `approval_policy` | `untrusted`, `on-request`, `never` | `on-request` | When to ask for approval |
| `sandbox_mode` | `read-only`, `workspace-write`, `danger-full-access` | `workspace-write` | Filesystem/network access |
| `model_reasoning_effort` | `minimal` to `xhigh` | `high` | How much reasoning to apply |
| `personality` | `friendly`, `pragmatic`, `none` | `friendly` | Communication style |
| `web_search` | `disabled`, `cached`, `live` | `cached` | Web search behavior |

### Enable Experimental Features

```toml
[features]
multi_agent = true
web_search = true
shell_snapshot = true
```

---

## Project-Level Instructions with AGENTS.md

AGENTS.md files are the primary way to give Codex project-specific and global instructions. Codex reads these files at the start of every session.

### How It Works

Codex builds an instruction chain by looking for AGENTS.md files in two scopes:

1. **Global scope** (`~/.codex/`): Applies to all projects.
2. **Project scope**: Walks from the Git root down to your current working directory, checking each directory level.

### Discovery Order

At each directory level, Codex checks for files in this order:

1. `AGENTS.override.md` (takes priority)
2. `AGENTS.md` (standard instructions)
3. Fallback filenames (if configured)

Only the first non-empty file found at each level is used.

### Setting Up Global Instructions

Create `~/.codex/AGENTS.md` with instructions that apply to all your projects:

```markdown
# Global Instructions

## Code Style
- Use 2-space indentation for JavaScript/TypeScript.
- Prefer functional programming patterns where appropriate.
- Always add error handling for async operations.

## Git Practices
- Write conventional commit messages (feat:, fix:, docs:, etc.).
- Never force-push to main.

## Testing
- Write tests for all new functions.
- Use descriptive test names.
```

### Setting Up Project-Level Instructions

Create `AGENTS.md` in your project root:

```markdown
# Project Instructions

## Stack
This is a Next.js 14 project with TypeScript, Tailwind CSS, and Prisma ORM.

## Conventions
- Components go in `src/components/`.
- API routes go in `src/app/api/`.
- Use server components by default.

## Database
- Run `npx prisma generate` after schema changes.
- Never modify migrations directly.

## Testing
- Use Vitest for unit tests.
- Run `npm test` before committing.
```

### Using Override Files

Create `AGENTS.override.md` to temporarily override instructions without modifying the main file. This is useful for experimental workflows or temporary team guidelines:

```markdown
# Temporary Override

## Current Sprint Focus
- Prioritize performance optimization.
- All new components must include loading states.
```

### Subdirectory Instructions

You can place additional AGENTS.md files in subdirectories for team-specific or module-specific guidance:

```
project-root/
  AGENTS.md              # Project-wide instructions
  backend/
    AGENTS.md            # Backend-specific instructions
  frontend/
    AGENTS.md            # Frontend-specific instructions
```

### Configuring Fallback Filenames

If your team uses a different filename convention, configure fallbacks in `~/.codex/config.toml`:

```toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md", "CODEX.md"]
project_doc_max_bytes = 65536
```

With this configuration, Codex checks each directory for: `AGENTS.override.md`, then `AGENTS.md`, then `TEAM_GUIDE.md`, then `.agents.md`, then `CODEX.md`.

### Scaffolding AGENTS.md

Codex can generate a starter AGENTS.md for your project:

```bash
codex
```

Then inside the TUI, run:

```
/init
```

This creates a scaffolded `AGENTS.md` based on your project structure.

### Verify Your Instructions

Test that Codex is picking up your instructions:

```bash
codex --ask-for-approval never "Summarize current instructions."
```

Or inside the TUI, run `/debug-config` to inspect which configuration files are loaded.

---

## Custom Agent Skills

Agent skills extend Codex with task-specific capabilities. They package instructions, optional scripts, and reference materials into reusable units.

### Skill Structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
my-skill/
  SKILL.md           # Required -- instructions with name and description
  scripts/           # Optional -- executable scripts
  references/        # Optional -- documentation files
  assets/            # Optional -- templates and resources
  agents/
    openai.yaml      # Optional -- metadata for UI and dependencies
```

### SKILL.md Format

```markdown
---
name: deploy-checker
description: Validates deployment readiness by checking test status, linting, and build health before allowing deploys.
---

# Deploy Checker

## When to Activate
Use this skill when the user asks about deployment readiness or before any deploy command.

## Steps
1. Run the test suite: `npm test`
2. Run the linter: `npm run lint`
3. Verify the build: `npm run build`
4. Check for uncommitted changes: `git status`
5. Report a summary of all checks.
```

### Skill Locations

Skills can be placed at different scopes:

| Scope | Path | Purpose |
|-------|------|---------|
| Repository (local) | `.agents/skills/` | Skills for the current directory |
| Repository (root) | `<repo-root>/.agents/skills/` | Organization-wide repo skills |
| User (global) | `~/.agents/skills/` | Personal cross-project skills |
| Admin | `/etc/codex/skills/` | System-wide defaults |

### Creating a Skill Automatically

Codex includes a built-in skill creator. In the TUI, type:

```
$skill-creator
```

It will prompt you about the skill's purpose, when it should trigger, and whether to include scripts.

### Creating a Skill Manually

**Step 1 -- Create the directory:**

```bash
mkdir -p ~/.agents/skills/code-reviewer
```

**Step 2 -- Create SKILL.md:**

Create `~/.agents/skills/code-reviewer/SKILL.md`:

```markdown
---
name: code-reviewer
description: Reviews code changes for best practices, security issues, and performance concerns.
---

# Code Reviewer

## When to Activate
Activate when the user asks for a code review or uses the $code-reviewer command.

## Review Checklist
1. Check for security vulnerabilities (injection, XSS, auth issues).
2. Verify error handling is present for all external calls.
3. Look for performance issues (N+1 queries, unnecessary re-renders).
4. Confirm tests exist for new functionality.
5. Check naming conventions match project standards.

## Output Format
Provide findings grouped by severity: Critical, Warning, Info.
```

### Installing Additional Skills

Use the built-in skill installer in the TUI:

```
$skill-installer
```

### Disabling a Skill

To disable a skill without deleting it, add to `~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

### Optional Metadata (openai.yaml)

For advanced skill configuration, create `agents/openai.yaml` inside your skill directory:

```yaml
interface:
  display_name: "Deploy Checker"
  icon_small: "./assets/icon.svg"
  brand_color: "#3B82F6"

policy:
  allow_implicit_invocation: true

dependencies:
  tools:
    - type: "mcp"
      value: "github"
```

### How Skills Activate

Skills can be triggered two ways:

- **Explicitly**: Reference the skill by name with `$skill-name` or browse with `/skills`.
- **Implicitly**: Codex automatically selects skills that match the current task description (if `allow_implicit_invocation` is true).

---

## MCP Server Integration

Codex supports the Model Context Protocol (MCP) for connecting external tools and services.

### Configure MCP Servers

Add MCP server definitions to `~/.codex/config.toml`:

**stdio server (local process):**

```toml
[mcp_servers.my-tool]
command = ["node", "/path/to/mcp-server.js"]
enabled_tools = ["tool-a", "tool-b"]
required = false
```

**HTTP server (remote):**

```toml
[mcp_servers.remote-tool]
url = "https://my-mcp-server.example.com/sse"
enabled_tools = ["search", "fetch"]
required = false
```

### List Available MCP Tools

In the TUI, run:

```
/mcp
```

---

## Profiles

Profiles let you switch between different configuration sets without editing your config file.

### Define Profiles

Add named profiles to `~/.codex/config.toml`:

```toml
[profiles.work]
model = "gpt-5.3-codex"
approval_policy = "on-request"
personality = "pragmatic"

[profiles.personal]
model = "gpt-5.3-codex"
approval_policy = "never"
personality = "friendly"

[profiles.review]
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
personality = "pragmatic"
```

### Use a Profile

```bash
codex --profile work
codex --profile review
```

---

## Useful Slash Commands

These commands are available inside the Codex TUI:

| Command | Description |
|---------|-------------|
| `/model` | Switch models or adjust reasoning effort |
| `/permissions` | Change approval mode (Auto, Read Only, Full Access) |
| `/personality` | Set communication style |
| `/status` | Show session configuration and token usage |
| `/debug-config` | Inspect loaded configuration layers |
| `/init` | Generate an AGENTS.md scaffold for your project |
| `/plan` | Switch to plan mode |
| `/new` | Start a fresh conversation |
| `/resume` | Resume a saved conversation |
| `/fork` | Branch the current conversation |
| `/compact` | Summarize conversation to save tokens |
| `/diff` | Show current Git diff |
| `/review` | Request a code review of working tree changes |
| `/mention` | Attach specific files to the conversation |
| `/mcp` | List available MCP tools |
| `/experimental` | Enable optional features like multi-agent |
| `/quit` | Exit the CLI |

---

## Troubleshooting

### "codex" command not found

Verify Node.js is installed (`node --version`) and reinstall:

```bash
npm install -g @openai/codex
```

Check that the npm global bin directory is in your PATH:

```bash
npm bin -g
```

### AGENTS.md not being loaded

- Run `/debug-config` in the TUI to see which files are loaded.
- Verify the file is in the correct location (project root or `~/.codex/`).
- Check that the file is not empty.
- Restart Codex after making changes to config files.

### Slow performance on Windows (WSL)

- Move your code from `/mnt/c/` to the WSL home directory (`~/`).
- Update WSL: `wsl --update` from PowerShell.

### Authentication issues

- Run `/logout` in the TUI, then restart and re-authenticate.
- For API key auth, verify your `OPENAI_API_KEY` is set: `echo $OPENAI_API_KEY`.

### Check logs

Codex logs are stored at `~/.codex/log/`. Inspect them for detailed error information.

---

## Quick Reference

| What | Where |
|------|-------|
| Global config | `~/.codex/config.toml` |
| Project config | `.codex/config.toml` |
| Global instructions | `~/.codex/AGENTS.md` |
| Project instructions | `<project-root>/AGENTS.md` |
| Global skills | `~/.agents/skills/` |
| Project skills | `.agents/skills/` |
| Logs | `~/.codex/log/` |
| Override instructions | `AGENTS.override.md` (at any level) |
