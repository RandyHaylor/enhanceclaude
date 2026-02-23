# Sequence Diagrams

- Wrap everything in a container with `shape: sequence_diagram`
- Declare actors in the order they should appear left-to-right (first use = order)
- Self-message: `actor -> actor: label`

```d2
flow: {
  shape: sequence_diagram

  browser: Browser
  api: API
  db: Database

  browser -> api: POST /login
  api -> db: SELECT user
  db -> api: row
  api -> api: bcrypt.compare()
  api -> browser: 200 {token}
}
```
