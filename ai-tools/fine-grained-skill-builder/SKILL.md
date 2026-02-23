---
name: fine-grained-skill-builder
description: Guide for building fine-grained Claude Code skills where content is split into many small files to minimize tokens loaded per invocation. Use when creating or restructuring a skill to be token-efficient with section-based progressive disclosure.
---

# Fine-Grained Skill Building Approach

## Goal

Minimize tokens loaded per invocation by breaking content into small, purpose-specific files loaded only when needed.

## Structure

```
skill-name/
├── SKILL.md           ← frontmatter + TOC only (links to section indexes)
├── section-a/
│   ├── index.md       ← section TOC (links to content files)
│   ├── topic-1.md     ← 1 table, 1 snippet, or ≤4 bullets
│   └── topic-2.md
├── section-b/
│   ├── index.md
│   └── ...
└── templates/
    └── example.xml    ← raw assets, no markdown wrapper
```

## Rules

- `SKILL.md` body: section list only — no content
- Section `index.md`: file list with one-line descriptions — no content
- Content files: one concept each, as small as possible
- Assets (XML, scripts): raw files, not wrapped in markdown code blocks

## Building with an Agent Team

1. Identify sections (non-overlapping, independently writable)
2. Create empty folder + `index.md` stub per section upfront
3. Write `SKILL.md` pointing to stubs
4. Spawn one agent per section in a single parallel call — each agent gets: its folder path, file list to create, and source material to extract from
5. Agents complete concurrently; shut each down as it reports done
6. Delete old source files

**Key constraint for agent prompts:** give each agent an explicit file list and source files. Vague scope causes overlap or gaps.
