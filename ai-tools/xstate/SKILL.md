# XState v5 Quick Reference

## How to Look Up API Details

For complete function signatures, types, and interfaces, **grep `api-reference.md`** — do NOT read it in full (12k+ lines). Example:

```
Grep pattern="createActor" path="~/.claude/skills/xstate/api-reference.md" output_mode="content" -C 5
```

Then use `Read` with `offset`/`limit` to get the full section. This is the primary way to get precise technical info when the quick reference below isn't enough.

## Design Workflow

Recommended approach for designing a state machine before writing code:

1. **List the events** — what can happen? (user actions, API responses, timers, errors)
2. **List the states** — what modes can the system be in? (idle, loading, error, etc.)
3. **Model visually** — draw the statechart (draw.io, Stately Studio, or paper). Map transitions: for each state, which events cause a transition to which other state?
4. **Identify actions** — what side effects fire on entry/exit/transition? (API calls, file writes, logging)
5. **Identify guards** — what conditions gate transitions? (threshold checks, retry limits, permissions)
6. **User-story-driven validation (TDD for the design)** — before writing any code, write concrete user stories and walk each one through the state machine design step-by-step. Each story traces a path through states and transitions. If a story can't complete, hits an undefined state, or requires a transition that doesn't exist, the machine design is broken — fix the machine, not the story. User stories are the tests, the statechart is the implementation, and the walkthrough is the test run. No code until every story passes against the design.
7. **Implement with TDD** — test each transition in isolation using `createActor` + `send` + `getSnapshot`

## Core Concept

A state machine is **pure structure** (string references) with **implementations wired in separately** at creation time. This separation keeps machines serializable, testable, and portable.

## Machine Definition

```js
import { setup } from 'xstate';

const machine = setup({
  actions: { onEnterIdle: () => {}, notifyUser: () => {} },
  guards: { isValid: () => true },
  actors: { fetchData: fromPromise(async ({ input }) => { /* async work */ }) },
}).createMachine({
  id: 'example',
  context: { count: 0, data: null },       // reactive data
  initial: 'idle',
  states: {
    idle: {
      entry: 'onEnterIdle',                // action on state enter
      exit: 'cleanUp',                     // action on state exit
      on: {
        SUBMIT: {
          target: 'loading',
          guard: 'isValid',                 // transition only if guard returns true
          actions: 'notifyUser',            // action fired during transition
        },
      },
    },
    loading: {
      invoke: {
        src: 'fetchData',                  // async actor (service)
        input: ({ context }) => context,
        onDone: { target: 'idle', actions: assign({ data: ({ event }) => event.output }) },
        onError: 'error',
      },
    },
    error: { on: { RETRY: 'loading' } },
  },
});
```

## Key Primitives

| Concept | Purpose | Defined via |
|---------|---------|-------------|
| **States** | Finite modes the system can be in | `states: {}` |
| **Events** | Triggers that cause transitions | `on: { EVENT_NAME: ... }` |
| **Context** | Extended (infinite) data carried by the machine | `context: {}`, mutated with `assign()` |
| **Actions** | Fire-and-forget side effects (entry/exit/transition) | `entry`, `exit`, `actions` |
| **Actors** | Async work: promises, observables, other machines | `invoke: { src: '...' }` |
| **Guards** | Boolean conditions gating transitions | `guard: 'guardName'` |

## Action vs Actor (Service)

- **Action**: synchronous, fire-and-forget. Use for: logging, assigning context, sending events.
- **Actor (service)**: async, has lifecycle (start/complete/error). Use for: API calls, subscriptions, spawned child machines.

Rule of thumb: if you need `onDone`/`onError`, it is an actor.

## Callback Actors (Long-Running Listeners)

Use `fromCallback` for ongoing subscriptions (e.g. Firestore onSnapshot) that send events back to the machine. The listener starts when the state is entered and is automatically cleaned up when the state exits.

```js
import { setup, fromCallback } from 'xstate';

const machine = setup({
  actors: {
    watchPlayers: fromCallback(({ input, sendBack }) => {
      // Start listener — sendBack pushes events to the parent machine
      const unsub = onSnapshot(collection(input.db, 'players'), (snap) => {
        snap.docChanges().forEach((change) => {
          if (change.type === 'added') {
            sendBack({ type: 'PLAYER_JOINED', id: change.doc.id, data: change.doc.data() });
          }
        });
      });
      // Return cleanup function — called automatically when state exits
      return () => unsub();
    }),
  },
}).createMachine({
  states: {
    lobby: {
      invoke: {
        src: 'watchPlayers',
        input: ({ context }) => ({ db: context.db }),
      },
      on: {
        PLAYER_JOINED: { actions: 'addPlayer' },
      },
    },
  },
});
```

Key points:
- `sendBack(event)` sends events to the parent machine
- `receive(handler)` listens for events FROM the parent (optional)
- Return a cleanup function to unsubscribe/clear timers
- Cleanup runs automatically when the machine leaves the invoking state

## File Organization Convention

```
machines/
  game/
    machine.js      # createMachine definition (pure structure, string refs only)
    actions.js      # { onEnterIdle: () => {...}, notifyUser: () => {...} }
    actors.js       # { fetchData: fromPromise(...) }
    guards.js       # { isValid: ({ context }) => context.value > 0 }
    index.js        # wires implementations into machine, exports actor
```

### index.js (wiring)

```js
import { createActor } from 'xstate';
import { machine } from './machine.js';
// machine already has implementations from setup() — or override:
const actor = createActor(machine, { input: { /* initial input */ } });
actor.start();
```

The machine definition references actions/guards/actors **by string name**. Implementations are provided in `setup()`. This means the machine structure is pure data; swap implementations for testing or different environments.

## TypeScript Typing

```ts
const machine = setup({
  types: {} as {
    context: { count: number; user: User | null };
    events: { type: 'FETCH'; id: string } | { type: 'RESET' };
    input: { initialId: string };
  },
  // ...
}).createMachine({ /* ... */ });
```

The `{} as Type` pattern is intentional — runtime value is ignored, types are inferred.

## Testing

```ts
// Override implementations for tests
const testMachine = machine.provide({
  actors: { fetchData: fromPromise(async () => mockData) },
});
const actor = createActor(testMachine);
actor.start();
actor.send({ type: 'FETCH', id: '1' });
expect(actor.getSnapshot().value).toBe('loaded');

// Async: wait for state
import { waitFor } from 'xstate';
await waitFor(actor, (snap) => snap.value === 'done');
```

## v4 → v5 Renames

| v4 | v5 |
|----|-----|
| `cond` | `guard` |
| `services` | `actors` |
| `event.data` | `event.output` |
| `.withConfig()` | `.provide()` |
| `send()` | `raise()` (self) / `sendTo()` (other) |

## Anti-Patterns

- Don't put side effects in `assign()` — only context updates
- Don't use `context: { isLoading: true }` — use actual state nodes
- Always name actions/guards/actors in `setup()` — enables `provide()` for testing

## Detailed References

- [machines-overview.md](machines-overview.md) — **Start here**: Creating machines, actors, setup, provide, type-bound helpers, transitions, modularizing states (from official docs)
- [states.md](states.md) — Atomic, compound, parallel, final, history states
- [actions.md](actions.md) — assign, raise, sendTo, log, enqueueActions, entry/exit
- [guards.md](guards.md) — Basic, parameterized, combinators (and/or/not)
- [actors.md](actors.md) — fromPromise, fromCallback, fromObservable, fromTransition, invoke, spawnChild
- [transitions.md](transitions.md) — Guarded, delayed, eventless, wildcard, self-transitions
- [context.md](context.md) — Static, factory, input-based initialization
- [testing.md](testing.md) — Arrange/Act/Assert, mocking, provide(), waitFor(), microsteps
- [graph.md](graph.md) — Graph utilities, path generation, model-based testing (from official docs)
- [api-reference.md](api-reference.md) — Full API reference from jsdocs.io (functions, classes, interfaces, types)

## Links

- [XState docs](https://stately.ai/docs/xstate)
- [Quick start](https://stately.ai/docs/quick-start)
- [Action vs service decision](https://dev.to/mattpocockuk/xstate-should-this-be-an-action-or-a-service-2cp0)
- [Guidelines for state machines](https://kyleshevlin.com/guidelines-for-state-machines-and-xstate/)
