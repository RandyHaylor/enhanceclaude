# Guards

## Basic
```ts
on: {
  submit: { guard: 'isValid', target: 'next' }
}
// in setup():
guards: { isValid: ({ context }) => context.value.length > 0 }
```

## Parameterized
```ts
on: {
  submit: {
    guard: { type: 'isOlderThan', params: { age: 18 } },
    target: 'allowed'
  }
}
guards: {
  isOlderThan: ({ context }, params) => context.age > params.age
}
```

## Combinators
```ts
import { and, or, not } from 'xstate';

guard: and(['isValid', 'isAuthorized'])
guard: or(['isAdmin', 'isGuest'])
guard: not('isBlocked')
guard: and(['isValid', or(['isAuthorized', 'isGuest'])])  // nested
```

## Multiple Guarded Transitions (first match wins)
```ts
on: {
  submit: [
    { guard: 'sentimentGood', target: 'thanks' },
    { guard: 'sentimentBad', target: 'form' },
    { target: 'form' }  // default fallback
  ]
}
```

Ref: https://stately.ai/docs/guards
