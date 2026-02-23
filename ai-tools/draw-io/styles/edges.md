- **Orthogonal:** `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;`
- **Curved:** `edgeStyle=none;curved=1;html=1;`
- **Labeled:** add `value="Label"` on the mxCell + `fontFamily=Noto Sans JP;fontSize=14;` in style
- **Dashed:** append `dashed=1;` to any edge style

**Connection points** (append to edge style):

| Property | 0 | 0.5 | 1 |
|----------|---|-----|---|
| `exitX` / `entryX` | left | center | right |
| `exitY` / `entryY` | top | center | bottom |

Always pair with `exitDx=0;exitDy=0;` and `entryDx=0;entryDy=0;`.
