# Update Installation Instructions — Team Plan

## Overview

Populate and maintain `installation-instructions.json` with accurate, concise installation paths for AI coding platforms. Each platform entry conforms to `installation-instructions-schema.json`.

## Schema

Each platform is an object with `platform` (string) and `installations` (array). Each installation entry has:
- `type` — what you're installing (skill, agent, rule, mcp, command, config, etc.)
- `scope` — where it goes (global, project)
- `path` — Mac/Linux path
- `windowsPath` — Windows path (only if different from `path`)
- `files` — minimum required files
- `example` — minimal file content (3-5 lines max)

## Phase 1: Extraction

1. Create a team with one agent per platform
2. Each agent reads official docs for their platform and writes a platform-specific JSON file
3. Agent instructions: "Extract ONLY installation paths, required files, and minimal examples. Keep it brief. No lengthy explanations."
4. Combine individual JSON files into single `installation-instructions.json`
5. Delete individual files

## Phase 2: Validation Round 1 — Accuracy Check

1. Create a team with one validator per platform
2. Each validator independently checks their platform's entries against official documentation
3. Agent instructions: "Check each entry against official docs. Report what's CORRECT, what's WRONG, what's MISSING. Be specific about corrections."
4. Apply any corrections found
5. Commit and push

## Phase 3: Validation Round 2 — Would It Work?

1. Create a team with one checker per platform
2. Strict instructions to prevent nitpicking:
   > "Your ONLY question is: if an average user follows this instruction, will they succeed? If YES → PASS. If the path is wrong and files would go to the wrong place → FAIL. If a UI label is slightly different but findable → PASS. If something is deprecated but still works → PASS. Do NOT invent issues. ONLY report genuine blockers."
3. Each checker replies with entry number + PASS/FAIL only
4. Success criteria: all entries PASS with zero failures
5. If any FAIL, fix and re-run this round until clean

## Key Lessons

- **First-pass agents over-document.** Explicitly tell them to be brief — "paths and examples only, no tutorials."
- **First validation round catches real errors** (wrong paths, wrong file locations). Worth doing.
- **Second validation round catches picky non-issues** if not constrained. Must explicitly say: "only flag things that would prevent a user from succeeding."
- **Third round with strict pass/fail criteria** produces a clean result. The "would it work" framing eliminates invented issues.
- **Two validation rounds is the sweet spot**: one for accuracy, one for pass/fail confirmation. A third round is only needed if round two finds real issues.

## Adding a New Platform

1. Add one agent to Phase 1 team for the new platform
2. Agent reads official docs, writes JSON conforming to schema
3. Merge into `installation-instructions.json`
4. Run one validation round with strict pass/fail criteria
5. Commit and push

## Updating Existing Platforms

1. Assign one agent to check the platform's entries against current official docs
2. Use strict pass/fail criteria — only flag entries that would no longer work
3. Apply fixes if any
4. One confirmation round if fixes were made
