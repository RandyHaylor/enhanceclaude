# Classes (Reusable Styles)

- Define in a `classes` block at the top level
- Apply to a node with `node.class: classname`
- Multiple classes: `node.class: [one; two]`

```d2
classes: {
  highlight: {
    style.fill: "#fff3e0"
    style.stroke: "#e65100"
    style.bold: true
  }
  muted: {
    style.opacity: 0.5
  }
}

server: API Server {
  class: highlight
}
old_server: Legacy {
  class: muted
}
```
