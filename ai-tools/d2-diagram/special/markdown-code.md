# Markdown & Code in Nodes

- Embed markdown in a node using `|md ... |`
- Embed syntax-highlighted code using `|language ... |`
- Renders inline in the diagram — great for annotating nodes with details

```d2
notes: |md
  ## Auth Flow
  - Validate JWT
  - Check expiry
  - Load user from cache
|

snippet: |go
  func hash(pw string) string {
    b, _ := bcrypt.GenerateFromPassword(
      []byte(pw), 12)
    return string(b)
  }
|
```
