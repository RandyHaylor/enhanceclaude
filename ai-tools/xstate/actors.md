# Actors

## fromPromise — one-shot async
```ts
import { fromPromise } from 'xstate';

const fetcher = fromPromise(async ({ input }: { input: { userId: string } }) => {
  const res = await fetch(`/api/users/${input.userId}`);
  return res.json();
});
```

## fromCallback — long-running, bidirectional
```ts
import { fromCallback } from 'xstate';

const watcher = fromCallback(({ sendBack, receive, input }) => {
  const ws = new WebSocket(input.url);
  ws.onmessage = (msg) => sendBack({ type: 'MESSAGE', data: msg.data });
  receive((event) => { if (event.type === 'SEND') ws.send(event.data); });
  return () => ws.close();  // cleanup on state exit
});
```

## fromObservable — streams
```ts
import { fromObservable } from 'xstate';
const timer = fromObservable(() => interval(1000));
```

## fromTransition — reducer-style
```ts
import { fromTransition } from 'xstate';

const counter = fromTransition(
  (state, event) => event.type === 'increment'
    ? { ...state, count: state.count + 1 }
    : state,
  { count: 0 }
);
```

## invoke — state-bound actor lifecycle
```ts
states: {
  loading: {
    invoke: {
      src: 'fetchData',
      id: 'dataFetch',
      input: ({ context }) => ({ userId: context.id }),
      onDone: { target: 'success', actions: assign({ data: ({ event }) => event.output }) },
      onError: { target: 'error', actions: assign({ error: ({ event }) => event.error }) }
    }
  }
}
```

## spawnChild — dynamic, unbounded actors
```ts
import { enqueueActions, spawnChild } from 'xstate';

on: {
  'todo.add': {
    actions: enqueueActions(({ enqueue, event }) => {
      enqueue.spawnChild('todoMachine', { input: event.data, id: event.id });
    })
  }
}
```

Ref: https://stately.ai/docs/actors
