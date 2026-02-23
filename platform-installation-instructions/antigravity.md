# Google Antigravity: Custom Agents and Skills Setup Guide

Google Antigravity is Google's agent-first IDE, launched in November 2025 alongside Gemini 3. It is a VSCode fork that treats the AI agent as the primary developer rather than a passive assistant. Antigravity uses a three-surface architecture: an Editor for synchronous coding, a Manager for autonomous agent orchestration, and browser integration for automated testing.

> **Note:** Antigravity is a Google product (not Shopify). It is currently in public preview and free for users with personal Gmail accounts. Workspace/enterprise Google accounts are not yet supported.

---

## Table of Contents

1. [Installation](#installation)
2. [First Launch and Authentication](#first-launch-and-authentication)
3. [Agent Modes](#agent-modes)
4. [Customization Overview](#customization-overview)
5. [Rules (Project and Global Instructions)](#rules-project-and-global-instructions)
6. [Workflows (Saved Prompt Sequences)](#workflows-saved-prompt-sequences)
7. [Skills (On-Demand Agent Extensions)](#skills-on-demand-agent-extensions)
8. [Complete Directory Reference](#complete-directory-reference)
9. [Tips and Best Practices](#tips-and-best-practices)

---

## Installation

### macOS

**Option A: Direct Download**

1. Visit [antigravity.google/download](https://antigravity.google/download).
2. Click **Download for Apple Silicon** (M1/M2/M3/M4) or **Download for Intel**.
3. Open the downloaded `.dmg` file.
4. Drag the Antigravity icon to your **Applications** folder.
5. Launch Antigravity from Applications. If macOS displays a security warning, click **Open** to proceed.

**Option B: Homebrew**

```bash
brew tap google/antigravity
brew install --cask antigravity
```

### Windows

**Option A: Direct Download**

1. Visit [antigravity.google/download](https://antigravity.google/download).
2. Select **Download for x64** (most common) or **Download for ARM64**.
3. Double-click the downloaded `.exe` file.
4. If Windows Defender SmartScreen displays a warning, click **More info** then **Run anyway**.
5. Follow the installer prompts. Default install path: `C:\Program Files\Google\Antigravity`.

**Option B: Winget**

```powershell
winget install Google.Antigravity
```

### Linux

**Debian / Ubuntu:**

```bash
sudo apt update
sudo apt install antigravity
```

**Fedora / RHEL:**

```bash
sudo dnf makecache
sudo dnf install antigravity
```

**Arch Linux:**

```bash
yay -S antigravity-bin
```

**Manual .deb / .rpm:**

Download from [antigravity.google/download](https://antigravity.google/download), then:

```bash
# Debian/Ubuntu
sudo dpkg -i antigravity_*.deb

# Fedora/RHEL
sudo rpm -i antigravity_*.rpm
```

### System Requirements

| Requirement | Minimum          | Recommended      |
|-------------|------------------|------------------|
| OS          | macOS 10.15+, Windows 10/11 (64-bit), Ubuntu 20.04+, Fedora 34+, Arch | Same |
| RAM         | 4 GB             | 8 GB+            |
| Storage     | 500 MB free      | 1 GB+ free       |
| Processor   | Dual-core        | Quad-core+       |
| Internet    | Required for AI features | Required  |

---

## First Launch and Authentication

1. Open Antigravity.
2. Sign in with your **personal Gmail account** (workspace accounts not yet supported).
3. Configure your preferences:
   - Theme (light/dark)
   - Agent mode (see below)
   - Terminal policy (Auto recommended)
4. Antigravity will initialize your workspace (2-3 minutes on first launch).

Antigravity supports importing VS Code extensions, so your existing setup can carry over.

---

## Agent Modes

Antigravity provides three built-in development modes:

| Mode | Description |
|------|-------------|
| **Agent-driven** | "Autopilot." You instruct the AI what to build and it writes code autonomously. |
| **Agent-assisted** | (Recommended) You stay in control, but the AI helps with safe automations. |
| **Review-driven** | The AI asks permission before performing almost any action. |

Additionally, there are two execution approaches:

- **Plan mode** -- The agent generates a detailed plan before executing.
- **Fast mode** -- The agent executes immediately.

---

## Customization Overview

Antigravity has three customization mechanisms, each serving a different purpose:

| Mechanism | Purpose | When Loaded | Scope |
|-----------|---------|-------------|-------|
| **Rules** | Persistent behavioral guidelines ("system instructions") | Always active | Global or Workspace |
| **Workflows** | Saved prompt sequences triggered on demand with `/` | On user trigger | Global or Workspace |
| **Skills** | On-demand capability extensions with assets | When agent determines relevance | Global or Workspace |

All three can be configured at two levels:

- **Global** -- Applies to every project. Stored under `~/.gemini/`.
- **Workspace** -- Applies to a single project. Stored under `<project-root>/.agent/`.

---

## Rules (Project and Global Instructions)

Rules are passive, persistent guidelines that the agent considers before generating any code or plan. They function as "system instructions" for the agent.

### Global Rules

Global rules apply to every project you open in Antigravity.

**File location:**

```
~/.gemini/GEMINI.md
```

On Windows: `C:\Users\<username>\.gemini\GEMINI.md`

**Creating via UI:** Click the three-dot menu (top right) > **Customizations** > **Rules** > **+ Global**.

**Creating manually:** Create or edit `~/.gemini/GEMINI.md` in any text editor.

**Example `~/.gemini/GEMINI.md`:**

```markdown
# Global Rules

* Always use TypeScript instead of JavaScript.
* Follow PEP 8 style guide for Python code.
* Include error handling in all async functions.
* Write unit tests for new functions.
* Use conventional commits format for commit messages.
```

> **Known issue:** Both Antigravity IDE and Gemini CLI use the same `~/.gemini/GEMINI.md` file. If you use both tools, be aware of potential configuration conflicts.

### Workspace (Project-Level) Rules

Workspace rules apply only to the current project.

**Directory:**

```
<project-root>/.agent/rules/
```

Each `.md` file in this directory becomes a separate rule.

**Creating via UI:** Click the three-dot menu > **Customizations** > **Rules** > **+ Workspace**.

**Creating manually:** Create `.md` files inside your project's `.agent/rules/` directory.

**Example `<project-root>/.agent/rules/code-style-guide.md`:**

```markdown
* Main method in main.py serves as entry point.
* Generate distinct functionality in separate files.
* Add example methods to main.py demonstrating new features.
* All code must follow PEP 8 style guide.
* Ensure all code is properly commented.
```

**Example `<project-root>/.agent/rules/project-conventions.md`:**

```markdown
* Use PostgreSQL for the database layer.
* All API endpoints must return JSON.
* Follow REST naming conventions for routes.
* Use environment variables for configuration (never hardcode secrets).
```

### Using AGENTS.md with Antigravity

Antigravity does not natively load `AGENTS.md` or `CLAUDE.md` files. To make Antigravity respect these files, add a global rule in `~/.gemini/GEMINI.md`:

```markdown
# Load AGENTS.md

If an AGENTS.md file exists in the project root or any subdirectory, read and
follow its instructions. Also check for AGENTS.md files in sub-folders — they
contain instructions specific to that part of the codebase.
```

This is a workaround that instructs the agent to look for and follow AGENTS.md files when present.

---

## Workflows (Saved Prompt Sequences)

Workflows are saved prompts that you trigger on demand by typing `/` in the agent chat. Unlike rules (which are always active), workflows run only when you invoke them.

### Global Workflows

**Directory:**

```
~/.gemini/antigravity/global_workflows/
```

On Windows: `C:\Users\<username>\.gemini\antigravity\global_workflows\`

Each `.md` file in this directory becomes a global workflow.

### Workspace Workflows

**Directory:**

```
<project-root>/.agent/workflows/
```

Each `.md` file in this directory becomes a workspace workflow.

### Creating a Workflow

A workflow file is a markdown file with a numbered list of steps. The agent executes them sequentially.

**Example `<project-root>/.agent/workflows/generate-unit-tests.md`:**

```markdown
* Generate unit tests for each file and method.
* Name test files with test_ prefix.
* Use pytest as the testing framework.
* Aim for at least 80% code coverage.
* Run the tests and report results.
```

**Example `~/.gemini/antigravity/global_workflows/code-review.md`:**

```markdown
* Review all staged changes for bugs and code smells.
* Check for security vulnerabilities (SQL injection, XSS, etc.).
* Verify error handling is present.
* Suggest improvements and list them in priority order.
```

### Triggering Workflows

Type `/` in the agent chat interface. Antigravity autocompletes available workflows matching what you type. Select the workflow to execute it.

---

## Skills (On-Demand Agent Extensions)

Skills are the most powerful customization mechanism. A Skill is a directory-based package containing a definition file (`SKILL.md`) and optional supporting assets. Unlike rules (always loaded) or workflows (user-triggered), skills are loaded into the agent's context only when the agent determines they are relevant to the current request.

### Skill Directory Structure

```
skill-name/
  SKILL.md              # Required: metadata and instructions
  scripts/              # Optional: Python, Bash, or Node scripts
  references/           # Optional: documentation, templates, text files
  examples/             # Optional: input/output example pairs
  assets/               # Optional: images, logos
```

### SKILL.md Format

A `SKILL.md` file has two sections:

1. **YAML Frontmatter** -- Metadata the agent uses for routing decisions.
2. **Markdown Body** -- Instructions injected into the agent's context when the skill is activated.

```markdown
---
name: my-skill-name
description: >
  Use this skill when the user asks about [specific scenario].
  Covers [key capabilities].
---

# My Skill Name

## Goal
[What this skill accomplishes]

## Instructions
1. [Step one]
2. [Step two]
3. [Step three]

## Constraints
- [Rule or limitation]
- [Another constraint]
```

The `description` field is critical -- it determines when the agent activates the skill. Write it as a trigger phrase describing the scenarios where the skill applies.

### Global Skills

Available across all projects on your machine.

**Directory:**

```
~/.gemini/antigravity/skills/
```

On Windows: `C:\Users\<username>\.gemini\antigravity\skills\`

### Workspace Skills

Available only within a specific project.

**Directory:**

```
<project-root>/.agent/skills/
```

### Installing Skills

Skills are automatically discovered when placed in the appropriate directory. No install command is needed -- just drop the skill folder into the correct location.

For community skills, you can clone repositories directly into your skills directory:

```bash
# Global install
cd ~/.gemini/antigravity/skills/
git clone https://github.com/example/my-antigravity-skill.git

# Workspace install
cd <project-root>/.agent/skills/
git clone https://github.com/example/my-antigravity-skill.git
```

### Skill Patterns

There are five established patterns for building skills:

#### Pattern 1: Basic Router (Instructions Only)

Contains only a `SKILL.md` with behavioral rules. Good for enforcing standards.

```
git-commit-formatter/
  SKILL.md
```

**Example `SKILL.md`:**

```markdown
---
name: git-commit-formatter
description: >
  Use when the user asks to create a git commit message or format commits.
---

# Git Commit Formatter

Format all commit messages using the Conventional Commits specification:

    <type>[scope]: <description>

Allowed types: feat, fix, docs, style, refactor, test, chore, perf, ci, build.

Rules:
- Subject line must not exceed 72 characters.
- Use imperative mood ("add feature" not "added feature").
- Include scope when the change targets a specific module.
```

#### Pattern 2: Reference Pattern (SKILL.md + References)

Separates heavy static content (templates, docs) into reference files to conserve tokens.

```
license-header-adder/
  SKILL.md
  references/
    HEADER_TEMPLATE.txt
```

The `SKILL.md` instructs the agent to read the template from `references/HEADER_TEMPLATE.txt` and prepend it to new files, converting comment syntax for different languages.

#### Pattern 3: Few-Shot Pattern (SKILL.md + Examples)

Provides input/output pairs so the agent learns the expected coding style and structure.

```
json-to-pydantic/
  SKILL.md
  examples/
    input_data.json
    output_model.py
```

#### Pattern 4: Tool Use Pattern (SKILL.md + Scripts)

Delegates deterministic work to scripts. The agent runs the script and interprets results.

```
database-schema-validator/
  SKILL.md
  scripts/
    validate_schema.py
```

The `SKILL.md` instructs: "Run `python scripts/validate_schema.py <file>`. Exit code 0 = valid, exit code 1 = invalid. Report the output to the user."

#### Pattern 5: Architect Pattern (Full Composition)

Combines all asset types for complex multi-step workflows.

```
adk-tool-scaffolder/
  SKILL.md
  scripts/
    scaffold.py
  references/
    architecture.md
    api-spec.yaml
  examples/
    sample-tool/
  assets/
    logo.png
```

---

## Complete Directory Reference

### Global Configuration (All Projects)

```
~/.gemini/
  GEMINI.md                                    # Global rules (always loaded)
  antigravity/
    skills/                                    # Global skills
      skill-name/
        SKILL.md
        scripts/
        references/
        examples/
    global_workflows/                          # Global workflows
      workflow-name.md
```

**Windows equivalent:** Replace `~/.gemini/` with `C:\Users\<username>\.gemini\`

### Workspace Configuration (Single Project)

```
<project-root>/
  .agent/
    rules/                                     # Workspace rules
      rule-name.md
    workflows/                                 # Workspace workflows
      workflow-name.md
    skills/                                    # Workspace skills
      skill-name/
        SKILL.md
        scripts/
        references/
        examples/
```

### Loading Priority

1. **Rules** (global `GEMINI.md` + workspace `.agent/rules/*.md`) are always injected into the agent's context.
2. **Skills** are indexed by their YAML metadata but only loaded when the agent determines they match the user's request.
3. **Workflows** are listed when the user types `/` and executed on selection.

---

## Tips and Best Practices

- **Start with rules** for simple behavioral guidelines. Only create skills when you need supporting assets (scripts, references, examples).
- **Write clear `description` fields** in SKILL.md frontmatter. This is what the agent uses to decide when to activate a skill.
- **Use workspace scope** for project-specific customizations. Use global scope for universal preferences.
- **Keep rules concise.** Rules are always loaded into context, so verbose rules waste tokens.
- **Use the Reference pattern** for large static content (API docs, templates) to keep your SKILL.md lean.
- **Commit `.agent/` to version control** so your team shares the same workspace rules, workflows, and skills.
- **Do not commit `~/.gemini/`** -- global configuration is personal and may conflict across team members.
- If you use both Antigravity and Gemini CLI, be aware they share `~/.gemini/GEMINI.md`. Consider keeping shared rules there and platform-specific rules in separate files.
