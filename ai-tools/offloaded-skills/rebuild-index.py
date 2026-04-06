#!/usr/bin/env python3
"""Rebuild ~/.claude/offloaded-skills/index.md from SKILL.md frontmatter."""

import re
from pathlib import Path

OFFLOADED_DIR = Path.home() / ".claude" / "offloaded-skills"
INDEX_PATH = OFFLOADED_DIR / "index.md"


def extract_frontmatter(skill_md: Path) -> dict:
    """Extract name and description from SKILL.md YAML frontmatter."""
    text = skill_md.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    body = match.group(1)

    # Extract name
    name_match = re.search(r"^name:\s*(.+)", body, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else skill_md.parent.name

    # Extract description (handles both single-line and multi-line YAML)
    desc = ""
    desc_match = re.search(
        r"^description:\s*[>|]?\s*\n((?:\s+.+\n?)+)", body, re.MULTILINE
    )
    if desc_match:
        # Multi-line: join indented continuation lines
        lines = desc_match.group(1).strip().splitlines()
        desc = " ".join(line.strip() for line in lines)
    else:
        # Single-line (possibly quoted)
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', body, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()

    return {"name": name, "description": desc}


def main():
    if not OFFLOADED_DIR.is_dir():
        print(f"Directory not found: {OFFLOADED_DIR}")
        return

    skills = []
    for skill_dir in sorted(OFFLOADED_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if skill_dir.is_dir() and skill_md.exists():
            info = extract_frontmatter(skill_md)
            if info:
                skills.append(
                    {
                        "name": info.get("name", skill_dir.name),
                        "description": info.get("description", ""),
                        "path": str(skill_md),
                    }
                )

    lines = [
        "# Offloaded Skills Index",
        "",
        f"_{len(skills)} skills available. Read a skill's SKILL.md to load it._",
        "",
    ]
    for s in skills:
        lines.append(f"- **{s['name']}** (`{s['path']}`)")
        if s["description"]:
            lines.append(f"  {s['description']}")
        lines.append("")

    INDEX_PATH.write_text("\n".join(lines))
    print(f"Wrote {INDEX_PATH} with {len(skills)} skills.")


if __name__ == "__main__":
    main()
