# Claude Code: Custom Agents and Skills Setup Guide

Claude Code supports two types of customizations that extend its capabilities: **agents** (specialized AI sub-assistants) and **skills** (reusable instructions and slash commands). Both can be configured at the project level (for a specific codebase) or the personal/global level (across all your projects).

---

## Custom Agents

Agents are specialized AI sub-assistants that handle specific types of tasks. Each agent runs in its own context with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches an agent's description, it can delegate to that agent automatically.

### What Goes in an Agent File

An agent file is a Markdown file (`.md`) with YAML frontmatter at the top for configuration, followed by the system prompt in Markdown. The system prompt defines the agent's behavior, personality, and workflow.

**Minimal example:**

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use when reviewing code changes or pull requests.
model: inherit
---

You are a senior code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

**Frontmatter fields:**

| Field               | Required | Description                                                              |
|---------------------|----------|--------------------------------------------------------------------------|
| `name`              | Yes      | Unique identifier (lowercase letters and hyphens)                        |
| `description`       | Yes      | When Claude should delegate to this agent                                |
| `tools`             | No       | Tools the agent can use (inherits all if omitted)                        |
| `disallowedTools`   | No       | Tools to deny from the inherited or specified list                       |
| `model`             | No       | Model to use: `sonnet`, `opus`, `haiku`, or `inherit` (default)          |
| `permissionMode`    | No       | Permission mode: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan` |
| `maxTurns`          | No       | Maximum agentic turns before the agent stops                             |
| `skills`            | No       | Skills to preload into the agent's context at startup                    |
| `mcpServers`        | No       | MCP servers available to this agent                                      |
| `hooks`             | No       | Lifecycle hooks scoped to this agent                                     |
| `memory`            | No       | Persistent memory scope: `user`, `project`, or `local`                   |
| `background`        | No       | Set to `true` to always run as a background task (default: `false`)      |
| `color`             | No       | Background color for the agent in the UI                                 |

### Where Agent Files Live

| Scope    | Path                          | Applies to           |
|----------|-------------------------------|----------------------|
| Project  | `.claude/agents/<name>.md`    | This project only    |
| Personal | `~/.claude/agents/<name>.md`  | All your projects    |

When multiple agents share the same name, higher-priority locations win: personal overrides project.

### Platform-Specific Paths

**Project-level agents** (same on all platforms -- relative to your project root):

```
<project-root>/.claude/agents/
```

**Personal/global agents:**

| Platform | Path                                    |
|----------|-----------------------------------------|
| Mac      | `~/.claude/agents/`                     |
| Linux    | `~/.claude/agents/`                     |
| Windows  | `C:\Users\<username>\.claude\agents\`   |

### Step-by-Step Setup

#### Create a Project Agent

1. Open a terminal in your project root.

2. Create the agents directory:

   **Mac / Linux:**
   ```bash
   mkdir -p .claude/agents
   ```

   **Windows (Command Prompt):**
   ```cmd
   mkdir .claude\agents
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Path .claude\agents -Force
   ```

3. Create an agent file. For example, `.claude/agents/code-reviewer.md`:

   ```markdown
   ---
   name: code-reviewer
   description: Reviews code for quality, security, and best practices. Use when reviewing code changes or pull requests.
   tools: Read, Grep, Glob, Bash
   model: inherit
   ---

   You are a senior code reviewer ensuring high standards of code quality.

   When invoked:
   1. Run git diff to see recent changes
   2. Focus on modified files
   3. Review for clarity, security, and correctness

   Provide feedback organized by priority:
   - Critical issues (must fix)
   - Warnings (should fix)
   - Suggestions (consider improving)
   ```

4. Start or restart Claude Code. The agent is now available. Claude will automatically delegate to it when appropriate, or you can ask explicitly:

   ```
   Use the code-reviewer agent to review my recent changes
   ```

#### Create a Personal (Global) Agent

1. Create the personal agents directory:

   **Mac / Linux:**
   ```bash
   mkdir -p ~/.claude/agents
   ```

   **Windows (Command Prompt):**
   ```cmd
   mkdir %USERPROFILE%\.claude\agents
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Path "$env:USERPROFILE\.claude\agents" -Force
   ```

2. Create your agent file in that directory (for example, `~/.claude/agents/debugger.md`).

3. Restart Claude Code. The agent is now available in all your projects.

#### Use the Interactive `/agents` Command

Instead of creating files manually, you can use the built-in `/agents` command inside Claude Code:

1. Run `/agents` in your Claude Code session.
2. Select **Create new agent**.
3. Choose **Project-level** or **User-level** (personal).
4. Either write the agent yourself or select **Generate with Claude** and describe what you want.
5. Select which tools the agent can use.
6. Choose a model.
7. Pick a color for the UI.
8. Save. The agent is available immediately.

### Including Supporting Files with Agents

Agent files can reference other files in the same directory. For example, if your agent needs reference material:

```
.claude/agents/
  my-agent.md
  reference-material/
    guide.txt
    examples.txt
```

Reference these from the agent's system prompt using relative paths:

```markdown
## Reference Material
See `.claude/agents/reference-material/guide.txt` for the full guide.
```

---

## Custom Skills

Skills are reusable sets of instructions that extend what Claude can do. Each skill has a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant to the conversation, or you can invoke one directly with `/skill-name` as a slash command.

### What Goes in a SKILL.md File

A `SKILL.md` file has two parts: YAML frontmatter for configuration, and Markdown content with the instructions Claude follows when the skill is invoked.

**Minimal example:**

```yaml
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?
```

**Frontmatter fields:**

| Field                      | Required    | Description                                                                   |
|----------------------------|-------------|-------------------------------------------------------------------------------|
| `name`                     | No          | Display name (also becomes the `/slash-command`). Defaults to directory name.  |
| `description`              | Recommended | What the skill does and when to use it. Claude uses this to decide when to load it automatically. |
| `argument-hint`            | No          | Hint shown during autocomplete (e.g., `[issue-number]` or `[filename] [format]`). |
| `disable-model-invocation` | No          | Set to `true` to prevent Claude from loading this skill automatically. Only you can invoke it with `/name`. Default: `false`. |
| `user-invocable`           | No          | Set to `false` to hide from the `/` menu. Only Claude can invoke it. Default: `true`. |
| `allowed-tools`            | No          | Tools Claude can use without permission when this skill is active.            |
| `model`                    | No          | Model to use when this skill is active.                                       |
| `context`                  | No          | Set to `fork` to run in a forked subagent context.                            |
| `agent`                    | No          | Which agent type to use when `context: fork` is set.                          |
| `hooks`                    | No          | Hooks scoped to this skill's lifecycle.                                       |

### Where Skills Live

Each skill is a directory containing a `SKILL.md` file (required) and optional supporting files:

```
my-skill/
  SKILL.md           # Main instructions (required)
  reference.md       # Detailed docs (optional, loaded when needed)
  examples/          # Example output (optional)
  scripts/           # Scripts Claude can execute (optional)
```

**Scope and path:**

| Scope    | Path                                              | Applies to           |
|----------|---------------------------------------------------|----------------------|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md`          | All your projects    |
| Project  | `.claude/skills/<skill-name>/SKILL.md`            | This project only    |

When skills share the same name across levels, higher-priority locations win: personal overrides project.

### Platform-Specific Paths

**Project-level skills** (same on all platforms -- relative to your project root):

```
<project-root>/.claude/skills/<skill-name>/SKILL.md
```

**Personal/global skills:**

| Platform | Path                                                    |
|----------|---------------------------------------------------------|
| Mac      | `~/.claude/skills/<skill-name>/SKILL.md`                |
| Linux    | `~/.claude/skills/<skill-name>/SKILL.md`                |
| Windows  | `C:\Users\<username>\.claude\skills\<skill-name>\SKILL.md` |

### Step-by-Step Setup

#### Create a Project Skill

1. Open a terminal in your project root.

2. Create the skill directory:

   **Mac / Linux:**
   ```bash
   mkdir -p .claude/skills/my-skill
   ```

   **Windows (Command Prompt):**
   ```cmd
   mkdir .claude\skills\my-skill
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Path .claude\skills\my-skill -Force
   ```

3. Create the `SKILL.md` file inside that directory. For example, `.claude/skills/my-skill/SKILL.md`:

   ```yaml
   ---
   name: my-skill
   description: Does something useful. Use when the user asks to do X or Y.
   ---

   Instructions for Claude go here. This content tells Claude exactly
   what to do when the skill is invoked.
   ```

4. Start or restart Claude Code. The skill is now available:
   - Claude will load it automatically when your request matches the description.
   - You can invoke it directly by typing `/my-skill` in the chat.

#### Create a Personal (Global) Skill

1. Create the skill directory:

   **Mac / Linux:**
   ```bash
   mkdir -p ~/.claude/skills/my-skill
   ```

   **Windows (Command Prompt):**
   ```cmd
   mkdir %USERPROFILE%\.claude\skills\my-skill
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Path "$env:USERPROFILE\.claude\skills\my-skill" -Force
   ```

2. Create `SKILL.md` inside that directory with your frontmatter and instructions.

3. Restart Claude Code. The skill is now available in all your projects.

### How Skills Are Invoked

Skills can be triggered in three ways:

1. **Automatic**: Claude reads the `description` of all available skills and decides when one is relevant to your conversation. The full skill content loads only when invoked.

2. **Slash command**: Type `/skill-name` in the chat to invoke a skill directly. You can also pass arguments:
   ```
   /fix-issue 123
   /migrate-component SearchBar React Vue
   ```

3. **Explicit request**: Ask Claude to use a specific skill:
   ```
   Use the explain-code skill on src/auth/login.ts
   ```

### Using Arguments in Skills

Skills support arguments via the `$ARGUMENTS` placeholder. When you invoke `/fix-issue 123`, the `$ARGUMENTS` variable gets replaced with `123`.

```yaml
---
name: fix-issue
description: Fix a GitHub issue
argument-hint: [issue-number]
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Implement the fix
3. Write tests
4. Create a commit
```

You can also access individual arguments by position:
- `$ARGUMENTS[0]` or `$0` for the first argument
- `$ARGUMENTS[1]` or `$1` for the second argument

### Adding Supporting Files

Keep `SKILL.md` focused on the essentials. Move detailed reference material, examples, and scripts into separate files:

```
my-skill/
  SKILL.md              # Overview and navigation (required)
  reference.md          # Detailed API docs (loaded when needed)
  examples.md           # Usage examples (loaded when needed)
  scripts/
    helper.py           # Utility script (executed, not loaded)
```

Reference supporting files from your `SKILL.md` so Claude knows what they contain:

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

### Controlling Invocation Behavior

| Frontmatter Setting                 | You can invoke | Claude can invoke | Use case                                   |
|-------------------------------------|----------------|-------------------|--------------------------------------------|
| (default)                           | Yes            | Yes               | General-purpose skills                     |
| `disable-model-invocation: true`    | Yes            | No                | Deployment, destructive actions            |
| `user-invocable: false`             | No             | Yes               | Background knowledge, domain context       |

---

## Legacy: Custom Commands

Claude Code also supports custom commands in `.claude/commands/` (project) or `~/.claude/commands/` (personal). These are single Markdown files (not directories) that create `/slash-commands`:

```
.claude/commands/review.md     -->  /review
~/.claude/commands/deploy.md   -->  /deploy
```

Custom commands use the same frontmatter as skills. Skills are the recommended approach since they support directories with additional supporting files. If a skill and a command share the same name, the skill takes precedence.

---

## Quick Reference

### Directory Structure Summary

```
# Project-level (checked into version control)
<project-root>/
  .claude/
    agents/
      my-agent.md                    # Project agent
    skills/
      my-skill/
        SKILL.md                     # Project skill
        reference.md                 # Optional supporting files
        scripts/
          helper.py
    commands/
      my-command.md                  # Legacy slash command (still works)

# Personal/global (available in all projects)
~/.claude/                           # Mac/Linux: ~/.claude/
  agents/                            # Windows: C:\Users\<username>\.claude\
    my-agent.md                      #   Personal agent
  skills/
    my-skill/
      SKILL.md                       #   Personal skill
  commands/
    my-command.md                     #   Personal slash command
```

### Key Differences: Agents vs Skills

| Feature        | Agents                                          | Skills                                              |
|----------------|-------------------------------------------------|-----------------------------------------------------|
| What they are  | Specialized AI sub-assistants                   | Reusable instructions and workflows                 |
| Context        | Run in their own isolated context               | Run inline in your current conversation (unless `context: fork`) |
| File format    | Single `.md` file with frontmatter              | `SKILL.md` inside a named directory                 |
| Invocation     | Claude delegates automatically or you ask       | Slash command (`/name`), automatic, or explicit request |
| Tool access    | Configurable per agent                          | Configurable per skill                              |
| Model          | Can use a different model                       | Can use a different model                           |
| Best for       | Complex, isolated tasks (review, debug, research) | Reusable workflows, reference knowledge, slash commands |
