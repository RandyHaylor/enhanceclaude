# State Machines Overview

A state machine is a model that describes the behavior of something, for example an actor. Finite state machines describe how the state of an actor transitions to another state when an event occurs.

## Creating a state machine

In XState, a state machine (referred to as a "machine") is created using the `createMachine(config)` function:

```ts
import { createMachine } from 'xstate';

const feedbackMachine = createMachine({
  id: 'feedback',
  initial: 'question',
  states: {
    question: {
      on: {
        'feedback.good': {
          target: 'thanks',
        },
      },
    },
    thanks: {
      // ...
    },
    // ...
  },
});
```

```ts
const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
  console.log(state.value);
});

feedbackActor.start();
// logs 'question'

feedbackActor.send({ type: 'feedback.good' });
// logs 'thanks'
```

## Creating actors from machines

A machine contains the logic of an actor. An actor is a running instance of the machine. Multiple actors can be created from the same machine, and each will be independent with their own states.

```ts
import { createActor } from 'xstate';

const feedbackActor = createActor(feedbackMachine);

feedbackActor.subscribe((state) => {
  console.log(state.value);
});

feedbackActor.start();
// logs 'question'
```

You can also create an actor from other types of logic: functions (`fromTransition`), promises (`fromPromise`), and observables (`fromObservable`).

## Providing implementations

Machine implementations are the language-specific code that is not directly related to the state machine's logic (states and transitions):

* **Actions** — fire-and-forget side-effects
* **Actors** — entities that can communicate with the machine actor
* **Guards** — conditions that determine whether a transition should be taken
* **Delays** — time before a delayed transition is taken

Default implementations are provided in `setup({...})`, then referenced by string/object:

```ts
import { setup } from 'xstate';

const feedbackMachine = setup({
  actions: {
    doSomething: () => {
      console.log('Doing something!');
    },
  },
  actors: { /* ... */ },
  guards: { /* ... */ },
  delays: { /* ... */ },
}).createMachine({
  entry: { type: 'doSomething' },
  // ... rest of machine config
});

const feedbackActor = createActor(feedbackMachine);
feedbackActor.start();
// logs 'Doing something!'
```

Override defaults with `machine.provide(...)` — creates a new machine with the same config but provided implementations:

```ts
const customFeedbackMachine = feedbackMachine.provide({
  actions: {
    doSomething: () => {
      console.log('Doing something else!');
    },
  },
});

const feedbackActor = createActor(customFeedbackMachine);
feedbackActor.start();
// logs 'Doing something else!'
```

## Type-bound action helpers

*Since XState version 5.22.0*

`setup()` provides type-bound action helpers fully typed to context, events, actors, guards, delays, and emitted types:

```ts
import { setup } from 'xstate';

const machineSetup = setup({
  types: {
    context: {} as { count: number; items: string[] },
    events: {} as { type: 'increment' } | { type: 'addItem'; item: string },
    emitted: {} as { type: 'COUNT_CHANGED'; count: number },
  },
});

// Type-bound assign
const incrementCount = machineSetup.assign({
  count: ({ context }) => context.count + 1,
});

const addItem = machineSetup.assign({
  items: ({ context, event }) => [...context.items, event.item],
});

// Type-bound raise
const raiseIncrement = machineSetup.raise({ type: 'increment' });

// Type-bound emit
const emitCountChanged = machineSetup.emit(({ context }) => ({
  type: 'COUNT_CHANGED',
  count: context.count,
}));

// Type-bound sendTo
const sendToLogger = machineSetup.sendTo('logger', ({ context }) => ({
  type: 'LOG',
  message: `Count is ${context.count}`,
}));

// Type-bound log
const logContext = machineSetup.log(
  ({ context }) => `Context: ${JSON.stringify(context)}`,
);

// Type-bound enqueueActions
const batchActions = machineSetup.enqueueActions(({ enqueue, check }) => {
  enqueue(incrementCount);
  enqueue(logContext);
  if (check(() => true)) {
    enqueue(emitCountChanged);
  }
});

const machine = machineSetup.createMachine({
  context: { count: 0, items: [] },
  initial: 'active',
  states: {
    active: {
      entry: [incrementCount, logContext, emitCountChanged],
      on: {
        increment: {
          actions: [incrementCount, batchActions],
        },
        addItem: {
          actions: addItem,
        },
      },
    },
  },
});
```

Available type-bound helpers:
* `setup(…).assign(…)`
* `setup(…).raise(…)`
* `setup(…).emit(…)`
* `setup(…).sendTo(…)`
* `setup(…).log(…)`
* `setup(…).cancel(…)`
* `setup(…).spawnChild(…)`
* `setup(…).stopChild(…)`
* `setup(…).enqueueActions(…)`
* `setup(…).createAction(…)`

## Transitioning state

*Since XState version 5.19.0*

Determine the next state and actions from current state and event using pure `transition()` and `initialTransition()` functions:

```ts
import { createMachine, initialTransition, transition } from 'xstate';

const machine = createMachine({
  initial: 'pending',
  states: {
    pending: {
      on: {
        start: { target: 'started' },
      },
    },
    started: {
      entry: 'doSomething',
    },
  },
});

const [initialState, initialActions] = initialTransition(machine);

console.log(initialState.value);
// logs 'pending'

console.log(initialActions);
// logs []

const [nextState, actions] = transition(machine, initialState, {
  type: 'start',
});

console.log(nextState.value);
// logs 'started'

console.log(actions);
// logs [{ type: 'doSomething', … }]
```

## Determining the next state

Use `getNextSnapshot(…)` to determine the next state outside of the actor:

```ts
import { getNextSnapshot } from 'xstate';
import { feedbackMachine } from './feedbackMachine';

const nextSnapshot = getNextSnapshot(
  feedbackMachine,
  feedbackMachine.resolveState({ value: 'question' }),
  { type: 'feedback.good' },
);

console.log(nextSnapshot.value);
// logs 'thanks'
```

Use `getInitialSnapshot(…)` for the initial state:

```ts
import { getInitialSnapshot } from 'xstate';

const initialSnapshot = getInitialSnapshot(
  feedbackMachine,
  { defaultRating: 3 }, // optional input
);

console.log(initialSnapshot.value);
// logs 'question'
```

> It is recommended to use `initialTransition(…)` and `transition(…)` instead of `getNextSnapshot(…)` and `getInitialSnapshot(…)`, which will be deprecated.

## Next transitions

*Since XState version 5.26.0*

Get all potential next transitions from a given state using `getNextTransitions(state)`:

```ts
import { createMachine, createActor, getNextTransitions } from 'xstate';

const machine = createMachine({
  initial: 'idle',
  states: {
    idle: {
      on: {
        start: { target: 'running' },
        reset: { target: 'idle' },
      },
    },
    running: {
      on: {
        stop: { target: 'idle' },
        pause: { target: 'paused' },
      },
    },
    paused: {
      on: {
        resume: { target: 'running' },
        stop: { target: 'idle' },
      },
    },
  },
});

const actor = createActor(machine).start();

const transitions = getNextTransitions(actor.getSnapshot());

console.log(transitions.map((t) => t.eventType));
// logs ['start', 'reset']
```

Each transition definition has:

* `eventType` - The event type of the transition
* `target` - The state node that the transition targets
* `source` - The state node where the transition originates from
* `actions` - The actions that will be executed during the transition
* `reenter` - Whether the transition is reentrant
* `guard` - The guard that will be evaluated

Useful for: building UIs showing available actions, debugging, testing, generating documentation.

## Modularizing states

*Since XState version 5.21.0*

Use `.createStateConfig(...)` from setup to create modular, reusable state configurations:

```ts
import { setup } from 'xstate';

const lightMachineSetup = setup({ /* ... */ });

const green = lightMachineSetup.createStateConfig({
  entry: { type: 'startTimer' },
  on: {
    TIMER: { target: 'yellow' },
    PEDESTRIAN: { target: 'yellow' },
    EMERGENCY: { target: 'red' },
  },
});

const yellow = lightMachineSetup.createStateConfig({
  entry: { type: 'startTimer' },
  on: {
    TIMER: { target: 'red' },
    EMERGENCY: { target: 'red' },
  },
});

const red = lightMachineSetup.createStateConfig({
  entry: { type: 'startTimer' },
  on: {
    TIMER: { target: 'green' },
    EMERGENCY: { target: 'green' },
  },
});

const trafficLightMachine = lightMachineSetup.createMachine({
  initial: 'green',
  states: { green, yellow, red },
});
```

## Specifying types

Provide TypeScript types via `setup(...)` and `.types`:

```ts
import { setup, fromPromise } from 'xstate';

const feedbackMachine = setup({
  types: {
    context: {} as { count: number },
    events: {} as { type: 'increment' } | { type: 'decrement' },
  },
  actions: { someAction: () => { /* ... */ } },
  guards: { someGuard: ({ context }) => context.count <= 10 },
  actors: { someActor: fromPromise(async () => 42) },
}).createMachine({
  initial: 'counting',
  states: {
    counting: {
      entry: { type: 'someAction' },
      invoke: {
        src: 'someActor',
        onDone: {
          actions: ({ event }) => {
            event.output; // strongly-typed as number
          },
        },
      },
      on: {
        increment: {
          guard: { type: 'someGuard' },
          actions: assign({
            count: ({ context }) => context.count + 1,
          }),
        },
      },
    },
  },
});
```

> XState v5 requires TypeScript version 5.0 or greater.

Ref: https://stately.ai/docs/machines
