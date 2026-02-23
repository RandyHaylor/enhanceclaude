# Removing Nodes with `null`

- `node: null` removes a previously declared or imported node
- Useful to hide glob-matched or imported nodes you don't need
- Connections to a nulled node are also removed

```d2
# Glob styles everything
*.style.fill: "#e3f2fd"

a
b
c

# But hide c
c: null
```
