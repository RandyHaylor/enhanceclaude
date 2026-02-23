# Containers

- Nest nodes inside `{}` block — creates a grouped container
- Connect into nested node from outside: `vpc.subnet.server -> db`
- Reference parent from inside: `_` = one level up

```d2
vpc: Production VPC {
  subnet: {
    server
    db
    server -> db
  }
}

# from outside, into nested:
vpc.subnet.server -> internet

# from inside, to grandparent scope:
vpc: {
  _.internet -> server
}
```
