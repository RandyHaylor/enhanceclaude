# Tooltips & Links

- `tooltip: "text"` — hover text shown on mouseover in SVG output
- `link: https://...` — clickable link on the node in SVG output
- Nodes with tooltips show an indicator icon

```d2
server: API Server {
  tooltip: "Handles all REST endpoints\nPort 8080"
  link: https://github.com/org/api-server
}

database: PostgreSQL {
  tooltip: "Primary read/write database"
}

server -> database
```
