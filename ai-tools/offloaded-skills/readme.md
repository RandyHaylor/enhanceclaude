# Offloaded Skills Manager

**Type:** skill | **Version:** 1.0.0 | **OS:** any

Registry and manager for extended skills stored in ~/.claude/offloaded-skills/ to save context window space. Includes a Python script to rebuild the index from SKILL.md frontmatter.

## Tags
skills, context-management, indexing, offloading, workflow

## Overview
This skill acts as a gateway to a library of extended skills that are stored outside the active ~/.claude/skills/ folder to reduce context window usage. It teaches Claude how to discover offloaded skills via an index file, load them on demand, and move skills between active and offloaded states. A Python script (rebuild-index.py) scans all SKILL.md files in the offloaded-skills folder and regenerates the index with names, descriptions, and paths.

## Try These Prompts
- What offloaded skills are available?
- Offload the draw-io skill to save context space.
- Restore the pdf skill back to active skills.
- Rebuild the offloaded skills index.

## Use Cases
- Reducing context window usage by moving infrequently used skills out of the active set
- Discovering and loading extended skills on demand
- Managing a large library of Claude Code skills efficiently
- Keeping an up-to-date index of all available offloaded skills

## Additional Requirements
Requires Python 3 for the rebuild-index.py script. Skills must have a SKILL.md with YAML frontmatter containing name and description fields.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
