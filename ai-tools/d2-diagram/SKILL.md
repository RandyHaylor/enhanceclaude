---
name: d2-diagram
description: Generate D2 diagram files (.d2) for technical reference — flowcharts, architecture diagrams, sequence diagrams, state machines, database schemas, and class diagrams. Use whenever the user wants to create, document, or visualize any system, flow, architecture, API, database, or process. Trigger on "make a diagram", "draw a flowchart", "document this architecture", "visualize this flow", "create a sequence diagram", "map this system", or any request to illustrate how something works.
---

# D2 Diagram Skill

Generates `.d2` files for VS Code (requires [D2 extension](https://marketplace.visualstudio.com/items?itemName=terrastruct.d2)).

---

## Workflow → `guides/workflow.md`
- How to greet user, offer templates, generate file, give preview instructions

## Templates → `templates/`
- `flowchart.d2` — process flows, decision trees, request handling
- `architecture.d2` — microservices, layered system architecture
- `sequence.d2` — API calls, auth flows, request/response chains
- `state-machine.d2` — order lifecycle, connection states, workflow stages
- `sql-schema.d2` — database tables with relationships
- `class-diagram.d2` — OOP class hierarchies, interfaces, SDKs
- `infra-cloud.d2` — cloud/VPC/subnet topology (AWS-style)
- `grid-dashboard.d2` — UI layouts, component maps, dashboards

## Syntax Quick-Reference → `syntax/`
- `nodes.md` — declaring nodes, labels, IDs
- `connections.md` — arrows, labels, chaining, bidirectional
- `containers.md` — grouping nodes, nested references, `_` parent
- `shapes.md` — full shape list with when to use each
- `styles.md` — fill, stroke, dash, bold, shadow, opacity
- `dimensions.md` — width, height, grid-rows, grid-columns
- `layout.md` — direction, layout engines (dagre/elk/tala)
- `globs.md` — `*`, `**`, `***` bulk selectors for global styles and connections
- `vars.md` — variables, substitution (`${var}`), `d2-config` block
- `classes.md` — reusable style definitions applied to multiple nodes
- `icons.md` — built-in and URL-based icons on nodes
- `near.md` — positioning labels/nodes relative to constants (`top-left`, etc.)
- `null.md` — removing/hiding nodes with `null`
- `comments.md` — `#` comments and block comments
- `gotchas.md` — naming rules, cross-container refs, common errors

## Advanced Features → `advanced/`
- `layers.md` — multiple diagram layers for step-by-step views
- `scenarios.md` — scenario variations branching from a base diagram
- `imports.md` — importing from other `.d2` files
- `tooltips-links.md` — interactive hover text and clickable links
- `themes.md` — built-in theme IDs, dark themes, sketch mode

## Special Diagram Types → `special/`
- `sequence.md` — sequence_diagram syntax, actors, self-messages
- `sql-table.md` — sql_table shape, constraints, FK relationships
- `class.md` — class shape, visibility (+/-/#), inheritance lines
- `markdown-code.md` — embedding md/code blocks inside nodes

---

## Validation — ALWAYS

```bash
d2 path/to/file.d2 /dev/null  # errors → stdout
```
Validate before starting + after each logical round of changes (not after every single line). VS Code diagnostics API misses D2 errors; CLI only.
