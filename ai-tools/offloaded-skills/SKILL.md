---
name: offloaded-skills
description: >
  Registry of extended skills stored in ~/.claude/offloaded-skills/ to save
  context window space. Consult ~/.claude/offloaded-skills/index.md to discover
  available skills and load them on demand. Also documents how to offload and
  restore skills.
user-invocable: false
---

## Offloaded Skills Library

There is a library of extended skills at `~/.claude/offloaded-skills/index.md`.
When a user request matches an offloaded skill's description, read the skill's
SKILL.md to load its full instructions.

## How to load an offloaded skill

1. Read `~/.claude/offloaded-skills/index.md` to find a matching skill.
2. Read `~/.claude/offloaded-skills/<skill-name>/SKILL.md` to get full instructions.
3. Follow those instructions as if the skill were installed normally.

## How to offload a skill

To move an installed skill out of the active set and into the offloaded library:

1. Move the skill folder: `mv ~/.claude/skills/<skill-name> ~/.claude/offloaded-skills/`
2. Rebuild the index: `python3 ~/.claude/skills/offloaded-skills/rebuild-index.py`

## How to restore an offloaded skill

To bring an offloaded skill back into the active set:

1. Move the skill folder: `mv ~/.claude/offloaded-skills/<skill-name> ~/.claude/skills/`
2. Rebuild the index: `python3 ~/.claude/skills/offloaded-skills/rebuild-index.py`

## Rebuilding the index

Run `python3 ~/.claude/skills/offloaded-skills/rebuild-index.py` any time skills
are added to or removed from the offloaded-skills folder.
