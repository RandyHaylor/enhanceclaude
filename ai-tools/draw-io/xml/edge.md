```xml
<!-- Basic edge between two vertices -->
<mxCell id="arrow1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;"
  edge="1"
  parent="1"
  source="box1"
  target="box2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Labeled edge -->
<mxCell id="arrow2"
  value="label text"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;"
  edge="1"
  parent="1"
  source="box1"
  target="box2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `edge="1"` marks it as a connector
- `source`/`target` reference vertex ids
- `relative="1"` required on edge geometry
- Add `value` attribute for a label on the edge
