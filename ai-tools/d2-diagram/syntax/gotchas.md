# Gotchas & Common Errors

- `--` in an ID is parsed as an undirected connection — avoid it in names
- IDs are case-sensitive: `Server` ≠ `server`
- Cross-container: `group1.child -> group2` works; `child -> group2` doesn't (child not in scope)
- `group1 -> group2` connects containers themselves, not their contents
- Redeclaring a node merges — latest explicit label wins
- Quoted IDs: `"my node"` — use when ID has spaces or special chars
- `style.multiple: true` gives a stacked visual; doesn't create multiple nodes
