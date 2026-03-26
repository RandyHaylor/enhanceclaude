# Testing

See also: [graph.md](graph.md) — Graph utilities and model-based test generation from official docs

Pattern: **Arrange** (create machine + actor) → **Act** (send events) → **Assert** (check state/context)

## Basic: State Transitions and Context

```ts
import { setup, createActor, assign } from 'xstate';

test('actor transitions correctly', () => {
  const toggleMachine = setup({}).createMachine({
    initial: 'inactive',
    context: { count: 0 },
    states: {
      inactive: {
        on: {
          activate: {
            target: 'active',
            actions: assign({ count: ({ context }) => context.count + 1 })
          }
        }
      },
      active: { on: { deactivate: 'inactive' } }
    }
  });

  const actor = createActor(toggleMachine);
  actor.start();

  expect(actor.getSnapshot().value).toBe('inactive');
  actor.send({ type: 'activate' });
  expect(actor.getSnapshot().value).toBe('active');
  expect(actor.getSnapshot().context.count).toBe(1);
});
```

## Mocking Side Effects

```ts
test('mocking actions', () => {
  const mockLogger = vi.fn();

  const machine = setup({
    actions: { logMessage: mockLogger }
  }).createMachine({
    initial: 'idle',
    states: {
      idle: {
        on: {
          start: {
            target: 'running',
            actions: { type: 'logMessage', params: { message: 'Started!' } }
          }
        }
      },
      running: {}
    }
  });

  const actor = createActor(machine);
  actor.start();
  actor.send({ type: 'start' });

  expect(mockLogger).toHaveBeenCalled();
});
```

## Override Implementations with provide()

```ts
const testMachine = machine.provide({
  actors: { fetchData: fromPromise(async () => mockData) },
  actions: { notify: vi.fn() },
  guards: { isValid: () => true },
});
const actor = createActor(testMachine);
actor.start();
```

## Async: waitFor()

```ts
import { waitFor } from 'xstate';

await waitFor(actor, (snap) => snap.value === 'done');
expect(actor.getSnapshot().context.result).toBeDefined();
```

## Eventless Transitions

States entered/exited via `always` transitions in the same step are **not observable** via `subscribe()` or `waitFor()`. Use the Inspection API:

```ts
const actor = createActor(machine, {
  inspect: (event) => {
    // @xstate.microstep events show intermediate states
    console.log(event);
  }
});
```

Or use zero-delay transitions instead: `after: { 0: 'nextState' }`

## Model-Based Testing

`@xstate/test` utilities are now in `xstate/graph` — enables automatic test case generation from state machines for path coverage.

Ref: https://stately.ai/docs/testing
