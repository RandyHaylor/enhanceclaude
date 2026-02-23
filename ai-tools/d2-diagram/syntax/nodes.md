# Nodes & Labels

- ID alone = rectangle with ID as label: `server`
- Custom label: `server: API Server`
- Quoted ID (spaces/symbols): `"my server": API Server`
- Redeclare to merge: declare node twice, D2 merges properties

```d2
server: API Server
server.style.fill: "#e3f2fd"

# same as:
server: API Server {
  style.fill: "#e3f2fd"
}
```
