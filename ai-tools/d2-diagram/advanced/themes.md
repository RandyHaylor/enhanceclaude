# Themes & Sketch Mode

- Set via `vars: { d2-config: { theme: ID } }`
- Theme IDs: `0` default, `1` Neutral Grey, `2` Flagship Terrastruct, `3` Cool Classics, `4` Mixed Berry Blue, `5` Grape Soda, `6` Aubergine, `7` Colorblind Clear, `8` Vanilla Nitro Cola
- Dark themes: IDs `200`+ (e.g., `200` Dark Mauve)
- `sketch: true` for hand-drawn look

```d2
vars: {
  d2-config: {
    theme: 4
    dark-theme: 200
    sketch: true
  }
}

server -> database
```
