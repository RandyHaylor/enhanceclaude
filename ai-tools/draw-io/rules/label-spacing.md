- Arrow labels must be positioned at least 20px away from the arrow line to avoid overlap.
- Use the label's `mxGeometry` Y coordinate relative to the arrow's Y to maintain clearance.

```xml
<mxPoint y="200" as="sourcePoint"/>  <!-- arrow at Y=200 -->
<mxGeometry y="170" />              <!-- label 30px above: OK -->
```
