# Positioning with `near`

- Place a node relative to the diagram: `near: top-center`
- Constants: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`
- Useful for titles, legends, annotations
- Can also position relative to another node: `near: other_node`

```d2
title: System Architecture {
  near: top-center
  style.font-size: 24
  style.bold: true
}

legend: "v2.1 — production" {
  near: bottom-right
  style.font-size: 12
}

server
database
server -> database
```
