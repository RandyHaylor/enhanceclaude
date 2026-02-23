- Elements render in XML declaration order (first = bottom layer). All `edge="1"` elements (arrows) MUST appear BEFORE `vertex="1"` elements (boxes) in the XML, or arrows render in front of boxes.
- Use comments to enforce the ordering convention:

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- === EDGES (arrows) === -->
  <mxCell id="arrow1" edge="1" ... />
  <mxCell id="arrow2" edge="1" ... />
  <!-- === VERTICES (boxes) === -->
  <mxCell id="box1" vertex="1" ... />
  <mxCell id="box2" vertex="1" ... />
</root>
```
