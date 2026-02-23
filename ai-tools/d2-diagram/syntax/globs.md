# Globs (Bulk Selectors)

Apply styles or properties to multiple nodes/edges at once using `*`, `**`, and `***`.

## Single glob `*` — direct children only

```d2
# Style all top-level nodes
*.style.fill: "#e3f2fd"
*.style.font-size: 16

x
y
z
```

## Double glob `**` — recursive (all descendants)

```d2
# Style every node at every nesting level
**.style.font-size: 16
**.style.border-radius: 8

x: {
  y: {
    z
  }
}
```

## Triple glob `***` — global (includes layers and imports)

```d2
# Applies across layers and imported files too
***.style.fill: "#fff3e0"
```

## Scoped globs — inside a container

Globs inside a container only affect that container's children.

```d2
outer: {
  # Only applies to nodes inside outer
  *.style.fill: "#c8e6c9"

  a
  b
}

# c is unaffected
c
```

## Prefix matching — target nodes by name pattern

```d2
# All nodes whose ID starts with "api"
api*.style.fill: "#bbdefb"

api_users
api_orders
database
```

## Glob connections — bulk wiring

```d2
# Connect all a-prefixed to all b-prefixed nodes
a* -> b*

a1
a2
b1
b2
```

## Glob on edges — style all connections

```d2
# Style every edge
(* -> *)[*].style.stroke: "#666"
(* -> *)[*].style.stroke-dash: 3
```

## Common use: global font size

`style.font-size` on a container only sets that container's label. Use `**` to cascade:

```d2
# This DOES NOT cascade to children:
style.font-size: 16

# This DOES cascade to all nested nodes:
**.style.font-size: 16
```

> **v0.7.1 caveat:** `**.style.font-size` causes compile error (`"style" needs a value`). Fallback: add `style.font-size` explicitly to each node that needs it.
