---
name: solid-vue-development
description: Core principles for writing clean, disciplined Vue 3 apps. Invoke when reviewing architecture, adding features, or evaluating component design.
---

## State vs. Behavior

- **State** = what something *is* → reactive refs on the owner of that concern
- **Behavior** = what something *does* → named functions (`signIn()`, `getTemplate()`)
- Never model a process as state. If you're naming refs after verbs (`isLoading`, `hasFetched`, `shouldRefresh`), the process has escaped into the wrong layer.

## Component Boundaries

- Components call functions. They don't own logic that belongs to a manager or service.
- Auth, sync, Drive, encryption — these have dedicated owners. Components receive state and call methods; they don't implement.

## Manager Pattern

- Encapsulate a domain's state AND behavior in a single manager (e.g. `GoogleDriveConnectionManager`).
- The manager exposes reactive state for the UI to read and named functions for the UI to call.
- No Drive logic in components. No auth logic in composables that belong in a manager.

## Reactive Chains: Use Them Right

- `computed` = derived values from state. Not side effects, not process orchestration.
- `watch` = react to state changes for necessary side effects only.
- Don't build process logic out of watcher chains. Write a function.

## Naming

- Functions: verb phrases describing what they do in isolation — `encryptUserData()`, `fetchTopicTemplate()`
- State/types: nouns — `encryptionSalt`, `StorageProvider`, `UserEntry`
- CSS variables: `--target-trigger-property-attribute`
- Long and explicit beats short and ambiguous. Always.

## Scope Discipline

- Don't add what wasn't asked for.
- Don't abstract for hypothetical reuse.
- Three similar lines of code is better than a premature abstraction.
- A bug fix is not an invitation to refactor surrounding code.
