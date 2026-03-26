# States

## Atomic
```ts
const machine = createMachine({
  initial: 'idle',
  states: { idle: {}, active: {} }
});
```

## Compound (Nested)
```ts
states: {
  form: {
    initial: 'empty',
    states: {
      empty: {},
      filled: { type: 'final' }
    }
  }
}
// value === { form: 'empty' }
```

## Parallel
```ts
const machine = createMachine({
  type: 'parallel',
  states: {
    monitor: { initial: 'off', states: { off: {}, on: {} } },
    mode: { initial: 'light', states: { light: {}, dark: {} } }
  }
});
// value === { monitor: 'on', mode: 'dark' }
```

## Final
```ts
states: {
  processing: { on: { COMPLETE: 'done' } },
  done: { type: 'final' }
}
// snapshot.status === 'done', snapshot.output available
```

## History
```ts
states: {
  parent: {
    initial: 'a',
    states: {
      a: {},
      b: {},
      hist: { type: 'history' }                    // shallow
      // hist: { type: 'history', history: 'deep' } // deep
      // hist: { type: 'history', target: 'a' }     // with default
    }
  }
}
```

Ref: https://stately.ai/docs/states
