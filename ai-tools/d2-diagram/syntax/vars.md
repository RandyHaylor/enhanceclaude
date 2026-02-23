# Variables & Config

- Define variables in a `vars` block, reference with `${var}`
- `d2-config` is a special nested block for engine/theme/layout settings
- Variables apply to labels and values

```d2
vars: {
  server-name: API Gateway
  color: "#e3f2fd"

  d2-config: {
    layout-engine: elk
    theme: 4
    dark-theme: 200
    sketch: true
    center: true
    pad: 0
  }
}

server: ${server-name} {
  style.fill: ${color}
}
```
