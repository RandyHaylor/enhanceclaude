# Context

## Static
```ts
const machine = createMachine({
  context: { feedback: '', count: 0 }
});
```

## Factory (fresh per actor instance)
```ts
const machine = createMachine({
  context: () => ({ feedback: '', createdAt: Date.now() })
});
```

## Input-based
```ts
const machine = setup({
  types: {
    context: {} as { feedback: string; rating: number },
    input: {} as { defaultRating: number }
  }
}).createMachine({
  context: ({ input }) => ({ feedback: '', rating: input.defaultRating })
});

const actor = createActor(machine, { input: { defaultRating: 5 } });
```

## Updating with assign()
```ts
import { assign } from 'xstate';

on: {
  increment: { actions: assign({ count: ({ context }) => context.count + 1 }) }
}
```

Ref: https://stately.ai/docs/context
