- Font MUST be set in TWO places: `defaultFontFamily` on `mxGraphModel` AND `fontFamily=` in every element's style string. The model default alone does NOT propagate to PNG export.
- If any element is missing `fontFamily=`, that element renders in a fallback serif font in exported PNGs.

```xml
<!-- BAD: font only on model -->
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
  <mxCell style="text;html=1;fontSize=18;" ... />

<!-- GOOD: font on model AND element -->
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
  <mxCell style="text;html=1;fontSize=18;fontFamily=Noto Sans JP;" ... />
```
