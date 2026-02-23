# Connections

- `a -> b` arrow, `a <- b` reverse, `a <-> b` bidirectional, `a -- b` no arrow
- Label: `a -> b: sends request`
- Chained: `a -> b -> c -> d`
- Multiple on one line: `a -> b; b -> c`

```d2
# Styled connection
a -> b: request {
  style.stroke: "#2196F3"
  style.stroke-dash: 3    # dashed
  style.animated: true    # flowing arrow
}

# Re-style after the fact (0-indexed)
(a -> b)[0].style.stroke: red
```
