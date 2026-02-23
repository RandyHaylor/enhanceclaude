# Scenarios

- Define with `scenarios: { name: { ...overrides... } }` at the top level
- Each scenario inherits and modifies the base diagram
- Renders as separate pages (like layers)
- Difference from layers: scenarios branch from base; layers are independent additions

```d2
server: Healthy {
  style.fill: "#c8e6c9"
}
server -> database

scenarios: {
  failure: {
    server: Down {
      style.fill: "#ffcdd2"
    }
    server -> database: timeout {
      style.stroke: red
    }
  }
}
```
