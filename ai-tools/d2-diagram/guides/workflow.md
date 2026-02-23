# Workflow Guide

## When the user asks for a diagram

1. If the diagram type is obvious (they said "sequence diagram", "ER diagram", etc.) — pick the matching template and go
2. If the type is ambiguous — briefly list the relevant templates and ask which fits, e.g.:
   > "I can make this as a flowchart, a sequence diagram, or an architecture diagram — which fits best?"
3. Read the matching template from `templates/` before generating
4. Generate the `.d2` file populated with their actual content (nodes, labels, connections)
5. Save as a descriptive filename: `auth-flow.d2`, `user-service-arch.d2`, etc.
6. Tell the user:
   > "Open `filename.d2` in VS Code with the D2 extension for live preview. Or run: `d2 -w filename.d2 out.svg`"

## Loading syntax files

Only load from `syntax/` or `special/` when you need a specific feature:
- Unsure about a shape name → `syntax/shapes.md`
- Need grid layout → `syntax/dimensions.md`
- Building a sequence diagram → `special/sequence.md`
- Need connection styling → `syntax/connections.md`

Don't preload all syntax files — load on demand.

## Iterative Refinement Loop

When the user says **"look at the diagram"** or **"look"** — that means: export to PNG and evaluate. Do not ask; just run the loop.

After generating a diagram, run this loop until the output is acceptable:

1. **Export** — `d2 input.d2 output.png`
2. **Evaluate** — read the PNG and list specific layout/readability issues (too wide, unreadable text, overlapping labels, etc.)
3. **Resolve** — fix the identified issues in the `.d2` file
4. **Repeat** — re-export and re-evaluate until no major issues remain

Common fixes by issue:
- Too wide / horizontal → change `direction: right` to `direction: down`
- Containers in wrong order → reorder top-level container declarations
- Long labels truncated → shorten label text or increase node width
- Arrows too long / hard to trace → restructure container order to match flow direction
- Overcrowded container → split into sub-containers or remove low-value nodes

## Quality checklist before saving

- [ ] All cross-container connections use full dotted path (`container.node`)
- [ ] No `--` in node IDs
- [ ] Complex diagrams use `layout-engine: elk`
- [ ] Start/end nodes use `shape: oval`
- [ ] Decision nodes use `shape: diamond`
- [ ] Dashed lines (`style.stroke-dash: 3`) for async, optional, or passive flows
