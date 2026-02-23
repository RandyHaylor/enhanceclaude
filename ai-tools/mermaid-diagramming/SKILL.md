---
name: mermaid-diagramming
description: "Create, edit, and layout Mermaid diagrams (.mmd files) correctly in VS Code using the MermaidChart extension. Use when creating or modifying any Mermaid diagram — flowcharts, sequence diagrams, etc. Covers node shapes, edge types, line breaks in labels, subgraph layout rules (side-by-side vs stacked), and VS Code preview commands. Critical: subgraph direction TB is silently ignored when nodes link across subgraphs."
---

# Mermaid Diagramming

## VS Code: Opening the Preview

Extension: **MermaidChart.vscode-mermaid-chart**

With a `.mmd` file open and focused:
- `Ctrl+Shift+P` → **"MermaidChart: Preview Diagram"**
- Preview is live — updates on save
- Pan/zoom, theme switcher, SVG/PNG export available in preview panel

## Line Breaks in Node Labels

Use `<br/>` — `\n` renders as literal text:
```
A["First line<br/>Second line"]   %% correct
A["First line\nSecond line"]      %% WRONG — shows \n literally
```

## Node Shapes

```
A["text"]      %% rectangle (process)
A("text")      %% rounded
A(["text"])    %% stadium / terminal
A{"text"}      %% diamond / decision
A[("text")]    %% cylinder / database
A(("text"))    %% circle
```

## Edge Types

```
A --> B              %% arrow
A --- B              %% open line
A -.-> B             %% dotted arrow
A ==> B              %% thick arrow
A -->|label| B       %% labeled arrow
A ~~~ B              %% invisible (forces layout without visible connection)
```

## Directions

```
flowchart TD    %% top-down
flowchart LR    %% left-right
flowchart BT    %% bottom-top
flowchart RL    %% right-left
```

## CRITICAL: Subgraph Layout Rules

### The Rule That Breaks Everything

> **"If any node links externally between subgraphs, `direction TB` inside the subgraph is ignored and the parent direction is inherited."**

This means: if you use `flowchart LR` and connect nodes across subgraphs, all `direction TB` declarations inside subgraphs are silently ignored. Internal nodes flow LR.

### Layout Decision Table

| Goal | Method |
|------|--------|
| Side-by-side, internal flow top-down | `flowchart LR` + `direction TB` inside each subgraph + no node-to-node cross-subgraph links |
| Stacked vertically | `flowchart TD` + node-to-node cross-subgraph edge |
| Side-by-side, internal flow left-right | `flowchart LR` only |

**Critical:** Any node-to-node link crossing between subgraphs silently overrides `direction TB` — internal nodes inherit the outer direction instead.

## Init Configuration

```
%%{init: {
  "flowchart": {
    "nodeSpacing": 50,
    "rankSpacing": 50,
    "subGraphTitleMargin": {"top": 15, "bottom": 0},
    "wrappingWidth": 200,
    "curve": "basis"
  },
  "themeVariables": {
    "clusterBkg": "#1a202c",
    "clusterBorder": "#4a5568",
    "edgeLabelBackground": "#2d3748",
    "primaryColor": "#1a365d",
    "primaryTextColor": "#bee3f8",
    "fontFamily": "monospace",
    "fontSize": "14px"
  }
}}%%
```

**Note:** `subGraphTitleMargin` requires capital G. Hex colors only — color names not recognized.

## Styling

```
classDef myStyle fill:#2d3748,stroke:#4a5568,color:#e2e8f0
class nodeA,nodeB myStyle

%% Inline:
style nodeA fill:#f9f,stroke:#333,stroke-width:2px

%% Edge styling (by index):
linkStyle 0 stroke:#ff0000,stroke-width:2px
```

## Subgraph Title Padding Workaround

`subGraphTitleMargin` often has no effect. Use an invisible spacer node instead:

```
subgraph FOO["Title"]
    direction TB
    PAD[ ]:::spacer ~~~ A["First real node"]
    A --> B
end

classDef spacer fill:none,stroke:none,color:none
```

## Comments

```
%% This is a comment
```
