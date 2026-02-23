# Dimensions & Grid

```d2
# Fixed size
node.width: 200
node.height: 80

# Grid layout (on a container)
dashboard: {
  grid-rows: 3
  grid-columns: 4

  header: { grid-column-span: 4 }   # spans all 4 cols
  sidebar: { grid-row-span: 2 }     # spans 2 rows
  main: { grid-column-span: 2 }
}
```

- Grid fills cells top-left to bottom-right in declaration order
- `grid-column-span` / `grid-row-span` merge cells
- Works great for UI layout maps, dashboards, component grids
