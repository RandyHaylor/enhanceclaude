# Layout & Direction

```d2
direction: right   # top (default) | right | left | down

vars: {
  d2-config: {
    layout-engine: elk    # dagre (default) | elk | tala
  }
}
```

- `dagre` — default; good for trees, simple flowcharts
- `elk` — better for dense graphs, nested containers, architecture; use this for complex diagrams
- `tala` — best quality; requires paid license
