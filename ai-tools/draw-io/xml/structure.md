```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="unique-id">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" page="0"
      guides="1" connect="1" fold="1" math="0" shadow="0"
      defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- vertices and edges here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

| Attribute | Required | Default |
|-----------|----------|---------|
| `defaultFontFamily` | yes | `Noto Sans JP` |
| `page` | yes | `0` (transparent) |
| `dx` | yes | `1200` |
| `dy` | yes | `800` |

- `id="0"` and `id="1" parent="0"` root cells are always required
- Z-order: elements drawn in XML order (first = back, last = front)
