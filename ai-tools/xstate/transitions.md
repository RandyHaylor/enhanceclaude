# Transitions

## Guarded
```ts
on: { submit: { guard: 'isValid', target: 'next' } }
```

## Delayed (after)
```ts
states: {
  active: {
    after: {
      5000: { target: 'timeout' },
      // with guard:
      10000: [
        { guard: 'shouldTimeout', target: 'timeout' },
        { target: 'active' }
      ]
    }
  }
}
```

## Eventless (always) — runs immediately when condition met
```ts
states: {
  check: {
    always: [
      { guard: 'hasErrors', target: 'form' },
      { guard: 'isApproved', target: 'submitted' },
      { target: 'review' }
    ]
  }
}
```

## Wildcard
```ts
on: { '*': { target: 'error' } }           // catch all events
on: { 'feedback.*': { target: 'processing' } }  // prefix match
```

## Self-Transitions
```ts
// Targetless: preserves child states, no re-entry
on: { log: { actions: log('updated') } }

// Targeted: resets child states
on: { reset: { target: 'active', actions: assign({ count: 0 }) } }

// Forced re-entry
on: { restart: { target: 'active', reenter: true } }
```

Ref: https://stately.ai/docs/transitions
