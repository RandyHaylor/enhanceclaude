# Imports

- `...@path/to/file.d2` spreads all content from the target file
- Can scope imports inside a container
- Paths are relative to the importing file

```d2
# Import entire file into current scope
...@./shared/common.d2

# Import into a container
vpc: {
  ...@./shared/services.d2
}

vpc -> external_api
```
