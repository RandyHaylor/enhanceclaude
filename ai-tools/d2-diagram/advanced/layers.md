# Layers

- Define with `layers: { layer_name: { ... } }` at the top level
- Each layer inherits the base diagram and can add/override nodes
- Layers render as separate pages in SVG output
- Useful for step-by-step or progressive diagrams

```d2
server -> database: queries

layers: {
  with_cache: {
    cache: Redis
    server -> cache: check first
    cache -> database: miss
  }
  with_monitoring: {
    monitor: Prometheus
    server -> monitor: metrics
  }
}
```
