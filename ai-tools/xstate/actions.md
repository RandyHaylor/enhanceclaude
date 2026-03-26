# Actions

## assign()
```ts
import { assign } from 'xstate';

// Object syntax
actions: assign({
  count: ({ context }) => context.count + 1,
  feedback: ({ event }) => event.feedback
})

// Function syntax (return full context)
actions: assign(({ context, event }) => ({
  ...context, count: context.count + 1
}))
```

## raise() — send event to self
```ts
import { raise } from 'xstate';

entry: raise({ type: 'check' })
entry: raise({ type: 'check' }, { delay: 1000 })  // delayed
actions: raise(({ context }) => ({ type: 'next', data: context.val }))  // dynamic
```

## sendTo() — send event to another actor
```ts
import { sendTo } from 'xstate';

actions: sendTo('targetActor', { type: 'message' })
actions: sendTo('actor', { type: 'event' }, { delay: 1000, id: 'sendId' })
actions: sendTo(({ context }) => context.actorRef, { type: 'event' })  // dynamic target
```

## log()
```ts
import { log } from 'xstate';
actions: log('User clicked button')
```

## enqueueActions() — conditional action logic (replaces v4 choose)
```ts
import { enqueueActions } from 'xstate';

entry: enqueueActions(({ enqueue, check }) => {
  enqueue.assign({ count: 1 });
  if (check({ type: 'someGuard' })) {
    enqueue.sendTo('actor', { type: 'event' });
  }
  enqueue.raise({ type: 'nextEvent' });
})
```

## Entry / Exit
```ts
states: {
  active: {
    entry: [{ type: 'startTimer' }],
    exit: [{ type: 'stopTimer' }]
  }
}
```

Ref: https://stately.ai/docs/actions
