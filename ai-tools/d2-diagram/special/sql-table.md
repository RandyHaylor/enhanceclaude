# SQL Tables

- Set `shape: sql_table` on a container
- Column constraints: `primary_key`, `foreign_key`, `unique`
- Draw FK relationships as connections between tables

```d2
users: {
  shape: sql_table
  id: bigint {constraint: primary_key}
  email: varchar {constraint: unique}
  org_id: int {constraint: foreign_key}
  created_at: timestamp
}

orders: {
  shape: sql_table
  id: bigint {constraint: primary_key}
  user_id: bigint {constraint: foreign_key}
  total: decimal
}

users -> orders: 1:N
```
