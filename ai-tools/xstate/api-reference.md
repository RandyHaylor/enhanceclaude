Source: https://www.jsdocs.io/package/xstate

## Variables

### variable [interpret](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L221 "View definition for interpret")
    
    
    const interpret: <TLogic extends AnyActorLogic>(
    
        logic: TLogic,
    
        ...[options]: ConditionalRequired<
    
            [
    
                options?: ActorOptions<TLogic> & {
    
                    [K in RequiredActorOptionsKeys<TLogic>]: unknown;
    
                }
    
            ],
    
            IsNotNever<RequiredActorOptionsKeys<TLogic>>
    
        >
    
    ) => Actor<TLogic>;

  * Creates a new Interpreter instance for the given machine with the provided options, if any.

#### Deprecated

Use `createActor` instead 




### variable [stop](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/stopChild.d.ts#L18 "View definition for stop")
    
    
    const stop: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject
    
    >(
    
        actorRef: ResolvableActorRef<TContext, TExpressionEvent, TParams, TEvent>
    
    ) => StopAction<TContext, TExpressionEvent, TParams, TEvent>;

  * Stops a child actor.

#### Deprecated

Use `stopChild(...)` instead 




## Functions

### function [and](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L88 "View definition for and")
    
    
    and: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TArg extends unknown[]
    
    >(
    
        guards: readonly [
    
            ...{
    
                [K in keyof TArg]: SingleGuardArg<
    
                    TContext,
    
                    TExpressionEvent,
    
                    unknown,
    
                    TArg[K]
    
                >;
    
            }
    
        ]
    
    ) => GuardPredicate<
    
        TContext,
    
        TExpressionEvent,
    
        unknown,
    
        NormalizeGuardArgArray<DoNotInfer<TArg>>
    
    >;

  * Higher-order guard that evaluates to `true` if all `guards` passed to it evaluate to `true`.

Guards

#### Returns

A guard action object

#### Example 1
        
        import { setup, and } from 'xstate';
        
        
        
        
        const machine = setup({
        
          guards: {
        
            someNamedGuard: () => true
        
          }
        
        }).createMachine({
        
          on: {
        
            someEvent: {
        
              guard: and([({ context }) => context.value > 0, 'someNamedGuard']),
        
              actions: () => {
        
                // will be executed if all guards in `and(...)`
        
                // evaluate to true
        
              }
        
            }
        
          }
        
        });




### function [assertEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/assert.d.ts#L25 "View definition for assertEvent")
    
    
    assertEvent: <
    
        TEvent extends EventObject,
    
        TAssertedDescriptor extends EventDescriptor<TEvent>
    
    >(
    
        event: TEvent,
    
        type: TAssertedDescriptor | readonly TAssertedDescriptor[]
    
    ) => asserts event is ExtractEvent<TEvent, TAssertedDescriptor>;

  * Asserts that the given event object is of the specified type or types. Throws an error if the event object is not of the specified types.

#### Example 1
        
        // ...
        
        entry: ({ event }) => {
        
          assertEvent(event, 'doNothing');
        
          // event is { type: 'doNothing' }
        
        },
        
        // ...
        
        exit: ({ event }) => {
        
          assertEvent(event, 'greet');
        
          // event is { type: 'greet'; message: string }
        
        
        
        
          assertEvent(event, ['greet', 'notify']);
        
          // event is { type: 'greet'; message: string }
        
          // or { type: 'notify'; message: string; level: 'info' | 'error' }
        
        },




### function [assign](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts#L44 "View definition for assign")
    
    
    assign: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends AnyEventObject,
    
        TParams extends {},
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    >(
    
        assignment:
    
            | Assigner<LowInfer<TContext>, TExpressionEvent, TParams, TEvent, TActor>
    
            | PropertyAssigner<
    
                  LowInfer<TContext>,
    
                  TExpressionEvent,
    
                  TParams,
    
                  TEvent,
    
                  TActor
    
              >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        TActor,
    
        never,
    
        never,
    
        never,
    
        never
    
    >;

  * Updates the current context of the machine.

#### Parameter assignment

An object that represents the partial context to update, or a function that returns an object that represents the partial context to update.

#### Example 1
        
        import { createMachine, assign } from 'xstate';
        
        
        
        
        const countMachine = createMachine({
        
          context: {
        
            count: 0,
        
            message: ''
        
          },
        
          on: {
        
            inc: {
        
              actions: assign({
        
                count: ({ context }) => context.count + 1
        
              })
        
            },
        
            updateMessage: {
        
              actions: assign(({ context, event }) => {
        
                return {
        
                  message: event.message.trim()
        
                };
        
              })
        
            }
        
          }
        
        });




### function [cancel](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/cancel.d.ts#L38 "View definition for cancel")
    
    
    cancel: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject
    
    >(
    
        sendId: ResolvableSendId<TContext, TExpressionEvent, TParams, TEvent>
    
    ) => CancelAction<TContext, TExpressionEvent, TParams, TEvent>;

  * Cancels a delayed `sendTo(...)` action that is waiting to be executed. The canceled `sendTo(...)` action will not send its event or execute, unless the `delay` has already elapsed before `cancel(...)` is called.

#### Parameter sendId

The `id` of the `sendTo(...)` action to cancel.

#### Example 1
        
        import { createMachine, sendTo, cancel } from 'xstate';
        
        
        
        
        const machine = createMachine({
        
          // ...
        
          on: {
        
            sendEvent: {
        
              actions: sendTo(
        
                'some-actor',
        
                { type: 'someEvent' },
        
                {
        
                  id: 'some-id',
        
                  delay: 1000
        
                }
        
              )
        
            },
        
            cancelEvent: {
        
              actions: cancel('some-id')
        
            }
        
          }
        
        });




### function [createActor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L209 "View definition for createActor")
    
    
    createActor: <TLogic extends AnyActorLogic>(
    
        logic: TLogic,
    
        ...[options]: ConditionalRequired<
    
            [
    
                options?: ActorOptions<TLogic> & {
    
                    [K in RequiredActorOptionsKeys<TLogic>]: unknown;
    
                }
    
            ],
    
            IsNotNever<RequiredActorOptionsKeys<TLogic>>
    
        >
    
    ) => Actor<TLogic>;

  * Creates a new actor instance for the given actor logic with the provided options, if any.

#### Parameter logic

The actor logic to create an actor from. For a state machine actor logic creator, see createMachine. Other actor logic creators include fromCallback, fromEventObservable, fromObservable, fromPromise, and fromTransition.

#### Parameter options

Actor options

#### Remarks

When you create an actor from actor logic via `createActor(logic)`, you implicitly create an actor system where the created actor is the root actor. Any actors spawned from this root actor and its descendants are part of that actor system.

#### Example 1
        
        import { createActor } from 'xstate';
        
        import { someActorLogic } from './someActorLogic.ts';
        
        
        
        
        // Creating the actor, which implicitly creates an actor system with itself as the root actor
        
        const actor = createActor(someActorLogic);
        
        
        
        
        actor.subscribe((snapshot) => {
        
          console.log(snapshot);
        
        });
        
        
        
        
        // Actors must be started by calling `actor.start()`, which will also start the actor system.
        
        actor.start();
        
        
        
        
        // Actors can receive events
        
        actor.send({ type: 'someEvent' });
        
        
        
        
        // You can stop root actors by calling `actor.stop()`, which will also stop the actor system and all actors in that system.
        
        actor.stop();




### function [createEmptyActor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/index.d.ts#L6 "View definition for createEmptyActor")
    
    
    createEmptyActor: () => ActorRef<
    
        Snapshot<undefined>,
    
        AnyEventObject,
    
        AnyEventObject
    
    >;




### function [createMachine](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createMachine.d.ts#L45 "View definition for createMachine")
    
    
    createMachine: <
    
        TContext extends MachineContext,
    
        TEvent extends AnyEventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TTag extends string,
    
        TInput,
    
        TOutput extends {},
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject,
    
        _ = any
    
    >(
    
        config: {
    
            types?: MachineTypes<
    
                TContext,
    
                TEvent,
    
                TActor,
    
                TAction,
    
                TGuard,
    
                TDelay,
    
                TTag,
    
                TInput,
    
                TOutput,
    
                TEmitted,
    
                TMeta
    
            >;
    
            schemas?: unknown;
    
        } & MachineConfig<
    
            TContext,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TTag,
    
            TInput,
    
            TOutput,
    
            TEmitted,
    
            TMeta
    
        >,
    
        implementations?: InternalMachineImplementations<
    
            ResolvedStateMachineTypes<
    
                TContext,
    
                TEvent,
    
                TActor,
    
                TAction,
    
                TGuard,
    
                TDelay,
    
                TTag,
    
                TEmitted
    
            >
    
        >
    
    ) => StateMachine<
    
        TContext,
    
        TEvent,
    
        Cast<ToChildren<TActor>, Record<string, AnyActorRef | undefined>>,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        StateValue,
    
        TTag & string,
    
        TInput,
    
        TOutput,
    
        TEmitted,
    
        TMeta,
    
        TODO
    
    >;

  * Creates a state machine (statechart) with the given configuration.

The state machine represents the pure logic of a state machine actor.

#### Parameter config

The state machine configuration.

#### Parameter options

DEPRECATED: use `setup({ ... })` or `machine.provide({ ... })` to provide machine implementations instead.

#### Example 1
        
        import { createMachine } from 'xstate';
        
        
        
        
        const lightMachine = createMachine({
        
          id: 'light',
        
          initial: 'green',
        
          states: {
        
            green: {
        
              on: {
        
                TIMER: { target: 'yellow' }
        
              }
        
            },
        
            yellow: {
        
              on: {
        
                TIMER: { target: 'red' }
        
              }
        
            },
        
            red: {
        
              on: {
        
                TIMER: { target: 'green' }
        
              }
        
            }
        
          }
        
        });
        
        
        
        
        const lightActor = createActor(lightMachine);
        
        lightActor.start();
        
        
        
        
        lightActor.send({ type: 'TIMER' });




### function [emit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/emit.d.ts#L42 "View definition for emit")
    
    
    emit: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject,
    
        TEmitted extends AnyEventObject
    
    >(
    
        eventOrExpr:
    
            | DoNotInfer<TEmitted>
    
            | SendExpr<TContext, TExpressionEvent, TParams, DoNotInfer<TEmitted>, TEvent>
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        never,
    
        never,
    
        never,
    
        never,
    
        TEmitted
    
    >;

  * Emits an event to event handlers registered on the actor via `actor.on(event, handler)`.

#### Example 1
        
        import { emit } from 'xstate';
        
        
        
        
        const machine = createMachine({
        
          // ...
        
          on: {
        
            something: {
        
              actions: emit({
        
                type: 'emitted',
        
                some: 'data'
        
              })
        
            }
        
          }
        
          // ...
        
        });
        
        
        
        
        const actor = createActor(machine).start();
        
        
        
        
        actor.on('emitted', (event) => {
        
          console.log(event);
        
        });
        
        
        
        
        actor.send({ type: 'something' });
        
        // logs:
        
        // {
        
        //   type: 'emitted',
        
        //   some: 'data'
        
        // }




### function [enqueueActions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/enqueueActions.d.ts#L56 "View definition for enqueueActions")
    
    
    enqueueActions: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject = TExpressionEvent,
    
        TActor extends ProvidedActor = ProvidedActor,
    
        TAction extends ParameterizedObject = ParameterizedObject,
    
        TGuard extends ParameterizedObject = ParameterizedObject,
    
        TDelay extends string = never,
    
        TEmitted extends EventObject = EventObject
    
    >(
    
        collect: CollectActions<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;

  * Creates an action object that will execute actions that are queued by the `enqueue(action)` function.

#### Example 1
        
        import { createMachine, enqueueActions } from 'xstate';
        
        
        
        
        const machine = createMachine({
        
          entry: enqueueActions(({ enqueue, check }) => {
        
            enqueue.assign({ count: 0 });
        
        
        
        
            if (check('someGuard')) {
        
              enqueue.assign({ count: 1 });
        
            }
        
        
        
        
            enqueue('someAction');
        
          })
        
        });




### function [forwardTo](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts#L32 "View definition for forwardTo")
    
    
    forwardTo: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject,
    
        TDelay extends string = never,
    
        TUsedDelay extends TDelay = never
    
    >(
    
        target: SendToActionTarget<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            AnyActorRef,
    
            TEvent
    
        >,
    
        options?: SendToActionOptions<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            TEvent,
    
            TUsedDelay
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        never,
    
        never,
    
        never,
    
        TDelay,
    
        never
    
    >;

  * Forwards (sends) an event to the `target` actor.

#### Parameter target

The target actor to forward the event to.

#### Parameter options

Options to pass into the send action creator.




### function [fromCallback](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts#L131 "View definition for fromCallback")
    
    
    fromCallback: <
    
        TEvent extends EventObject,
    
        TInput = {},
    
        TEmitted extends EventObject = EventObject
    
    >(
    
        callback: CallbackLogicFunction<TEvent, AnyEventObject, TInput, TEmitted>
    
    ) => CallbackActorLogic<TEvent, TInput, TEmitted>;

  * An actor logic creator which returns callback logic as defined by a callback function.

#### Parameter callback

The callback function used to describe the callback logic The callback function is passed an object with the following properties:

\- `receive` \- A function that can send events back to the parent actor; the listener is then called whenever events are received by the callback actor - `sendBack` \- A function that can send events back to the parent actor - `input` \- Data that was provided to the callback actor - `self` \- The parent actor of the callback actor - `system` \- The actor system to which the callback actor belongs The callback function can (optionally) return a cleanup function, which is called when the actor is stopped.

#### Returns

Callback logic

#### Remarks

Useful for subscription-based or other free-form logic that can send events back to the parent actor.

Actors created from callback logic (“callback actors”) can:

\- Receive events via the `receive` function - Send events to the parent actor via the `sendBack` function

Callback actors are a bit different from other actors in that they:

\- Do not work with `onDone` \- Do not produce a snapshot using `.getSnapshot()` \- Do not emit values when used with `.subscribe()` \- Can not be stopped with `.stop()`

#### Example 1
        
        const callbackLogic = fromCallback(({ sendBack, receive }) => {
        
          let lockStatus = 'unlocked';
        
        
        
        
          const handler = (event) => {
        
            if (lockStatus === 'locked') {
        
              return;
        
            }
        
            sendBack(event);
        
          };
        
        
        
        
          receive((event) => {
        
            if (event.type === 'lock') {
        
              lockStatus = 'locked';
        
            } else if (event.type === 'unlock') {
        
              lockStatus = 'unlocked';
        
            }
        
          });
        
        
        
        
          document.body.addEventListener('click', handler);
        
        
        
        
          return () => {
        
            document.body.removeEventListener('click', handler);
        
          };
        
        });

#### See Also

    * CallbackLogicFunction for more information about the callback function and its object argument

    * [Input docs](https://stately.ai/docs/input) for more information about how input is passed




### function [fromEventObservable](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts#L146 "View definition for fromEventObservable")
    
    
    fromEventObservable: <
    
        TEvent extends EventObject,
    
        TInput extends {},
    
        TEmitted extends EventObject = EventObject
    
    >(
    
        lazyObservable: ({
    
            input,
    
            system,
    
            self,
    
            emit,
    
        }: {
    
            input: TInput;
    
            system: AnyActorSystem;
    
            self: ObservableActorRef<TEvent>;
    
            emit: (emitted: TEmitted) => void;
    
        }) => Subscribable<TEvent>
    
    ) => ObservableActorLogic<TEvent, TInput, TEmitted>;

  * Creates event observable logic that listens to an observable that delivers event objects.

Event observable actor logic is described by an observable stream of [event objects](https://stately.ai/docs/transitions#event-objects). Actors created from event observable logic (“event observable actors”) can:

\- Implicitly send events to its parent actor - Emit snapshots of its emitted event objects

Sending events to event observable actors will have no effect.

#### Parameter lazyObservable

A function that creates an observable that delivers event objects. It receives one argument, an object with the following properties:

\- `input` \- Data that was provided to the event observable actor - `self` \- The parent actor - `system` \- The actor system to which the event observable actor belongs.

It should return a Subscribable, which is compatible with an RxJS Observable, although RxJS is not required to create them.

#### Example 1
        
        import {
        
          fromEventObservable,
        
          Subscribable,
        
          EventObject,
        
          createMachine,
        
          createActor
        
        } from 'xstate';
        
        import { fromEvent } from 'rxjs';
        
        
        
        
        const mouseClickLogic = fromEventObservable(
        
          () => fromEvent(document.body, 'click') as Subscribable<EventObject>
        
        );
        
        
        
        
        const canvasMachine = createMachine({
        
          invoke: {
        
            // Will send mouse `click` events to the canvas actor
        
            src: mouseClickLogic
        
          }
        
        });
        
        
        
        
        const canvasActor = createActor(canvasMachine);
        
        canvasActor.start();




### function [fromObservable](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts#L89 "View definition for fromObservable")
    
    
    fromObservable: <
    
        TContext,
    
        TInput extends {},
    
        TEmitted extends EventObject = EventObject
    
    >(
    
        observableCreator: ({
    
            input,
    
            system,
    
            self,
    
        }: {
    
            input: TInput;
    
            system: AnyActorSystem;
    
            self: ObservableActorRef<TContext>;
    
            emit: (emitted: TEmitted) => void;
    
        }) => Subscribable<TContext>
    
    ) => ObservableActorLogic<TContext, TInput, TEmitted>;

  * Observable actor logic is described by an observable stream of values. Actors created from observable logic (“observable actors”) can:

\- Emit snapshots of the observable’s emitted value

The observable’s emitted value is used as its observable actor’s `context`.

Sending events to observable actors will have no effect.

#### Parameter observableCreator

A function that creates an observable. It receives one argument, an object with the following properties:

\- `input` \- Data that was provided to the observable actor - `self` \- The parent actor - `system` \- The actor system to which the observable actor belongs

It should return a Subscribable, which is compatible with an RxJS Observable, although RxJS is not required to create them.

#### Example 1
        
        import { fromObservable, createActor } from 'xstate';
        
        import { interval } from 'rxjs';
        
        
        
        
        const logic = fromObservable((obj) => interval(1000));
        
        
        
        
        const actor = createActor(logic);
        
        
        
        
        actor.subscribe((snapshot) => {
        
          console.log(snapshot.context);
        
        });
        
        
        
        
        actor.start();
        
        // At every second:
        
        // Logs 0
        
        // Logs 1
        
        // Logs 2
        
        // ...

#### See Also

    * <https://rxjs.dev> for documentation on RxJS Observable and observable creators.

    * Subscribable interface in XState, which is based on and compatible with RxJS Observable.




### function [fromPromise](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/promise.d.ts#L95 "View definition for fromPromise")
    
    
    fromPromise: <TOutput, TInput = {}, TEmitted extends EventObject = EventObject>(
    
        promiseCreator: ({
    
            input,
    
            system,
    
            self,
    
            signal,
    
            emit,
    
        }: {
    
            input: TInput;
    
            system: AnyActorSystem;
    
            self: PromiseActorRef<TOutput>;
    
            signal: AbortSignal;
    
            emit: (emitted: TEmitted) => void;
    
        }) => PromiseLike<TOutput>
    
    ) => PromiseActorLogic<TOutput, TInput, TEmitted>;

  * An actor logic creator which returns promise logic as defined by an async process that resolves or rejects after some time.

Actors created from promise actor logic (“promise actors”) can:

\- Emit the resolved value of the promise - Output the resolved value of the promise

Sending events to promise actors will have no effect.

#### Parameter promiseCreator

A function which returns a Promise, and accepts an object with the following properties:

\- `input` \- Data that was provided to the promise actor - `self` \- The parent actor of the promise actor - `system` \- The actor system to which the promise actor belongs

#### Example 1
        
        const promiseLogic = fromPromise(async () => {
        
          const result = await fetch('https://example.com/...').then((data) =>
        
            data.json()
        
          );
        
        
        
        
          return result;
        
        });
        
        
        
        
        const promiseActor = createActor(promiseLogic);
        
        promiseActor.subscribe((snapshot) => {
        
          console.log(snapshot);
        
        });
        
        promiseActor.start();
        
        // => {
        
        //   output: undefined,
        
        //   status: 'active'
        
        //   ...
        
        // }
        
        
        
        
        // After promise resolves
        
        // => {
        
        //   output: { ... },
        
        //   status: 'done',
        
        //   ...
        
        // }

#### See Also

    * [Input docs](https://stately.ai/docs/input) for more information about how input is passed




### function [fromTransition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/transition.d.ts#L140 "View definition for fromTransition")
    
    
    fromTransition: <
    
        TContext,
    
        TEvent extends EventObject,
    
        TSystem extends AnyActorSystem,
    
        TInput extends {},
    
        TEmitted extends EventObject = EventObject
    
    >(
    
        transition: (
    
            snapshot: TContext,
    
            event: TEvent,
    
            actorScope: ActorScope<
    
                TransitionSnapshot<TContext>,
    
                TEvent,
    
                TSystem,
    
                TEmitted
    
            >
    
        ) => TContext,
    
        initialContext:
    
            | TContext
    
            | (({
    
                  input,
    
                  self,
    
              }: {
    
                  input: TInput;
    
                  self: TransitionActorRef<TContext, TEvent>;
    
              }) => TContext)
    
    ) => TransitionActorLogic<TContext, TEvent, TInput, TEmitted>;

  * Returns actor logic given a transition function and its initial state.

A “transition function” is a function that takes the current `state` and received `event` object as arguments, and returns the next state, similar to a reducer.

Actors created from transition logic (“transition actors”) can:

\- Receive events - Emit snapshots of its state

The transition function’s `state` is used as its transition actor’s `context`.

Note that the "state" for a transition function is provided by the initial state argument, and is not the same as the State object of an actor or a state within a machine configuration.

#### Parameter transition

The transition function used to describe the transition logic. It should return the next state given the current state and event. It receives the following arguments:

\- `state` \- the current state. - `event` \- the received event. - `actorScope` \- the actor scope object, with properties like `self` and `system`.

#### Parameter initialContext

The initial state of the transition function, either an object representing the state, or a function which returns a state object. If a function, it will receive as its only argument an object with the following properties:

\- `input` \- the `input` provided to its parent transition actor. - `self` \- a reference to its parent transition actor.

#### Returns

Actor logic

#### Example 1
        
        const transitionLogic = fromTransition(
        
          (state, event) => {
        
            if (event.type === 'increment') {
        
              return {
        
                ...state,
        
                count: state.count + 1
        
              };
        
            }
        
            return state;
        
          },
        
          { count: 0 }
        
        );
        
        
        
        
        const transitionActor = createActor(transitionLogic);
        
        transitionActor.subscribe((snapshot) => {
        
          console.log(snapshot);
        
        });
        
        transitionActor.start();
        
        // => {
        
        //   status: 'active',
        
        //   context: { count: 0 },
        
        //   ...
        
        // }
        
        
        
        
        transitionActor.send({ type: 'increment' });
        
        // => {
        
        //   status: 'active',
        
        //   context: { count: 1 },
        
        //   ...
        
        // }

#### See Also

    * [Input docs](https://stately.ai/docs/input) for more information about how input is passed




### function [getInitialMicrosteps](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts#L31 "View definition for getInitialMicrosteps")
    
    
    getInitialMicrosteps: <T extends AnyStateMachine>(
    
        machine: T,
    
        ...[input]: undefined extends InputFrom<T>
    
            ? [input?: InputFrom<T>]
    
            : [input: InputFrom<T>]
    
    ) => Array<[SnapshotFrom<T>, ExecutableActionsFrom<T>[]]>;

  * Given a state `machine` and optional `input`, returns an array of microsteps from the initial transition, where each microstep is a tuple of `[snapshot, actions]`.

This is a pure function that does not execute `actions`.




### function [getInitialSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/getNextSnapshot.d.ts#L3 "View definition for getInitialSnapshot")
    
    
    getInitialSnapshot: <T extends AnyActorLogic>(
    
        actorLogic: T,
    
        ...[input]: undefined extends InputFrom<T>
    
            ? [input?: InputFrom<T>]
    
            : [input: InputFrom<T>]
    
    ) => SnapshotFrom<T>;

  * #### Deprecated

Use `initialTransition(…)` instead.




### function [getMicrosteps](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts#L23 "View definition for getMicrosteps")
    
    
    getMicrosteps: <T extends AnyStateMachine>(
    
        machine: T,
    
        snapshot: SnapshotFrom<T>,
    
        event: EventFromLogic<T>
    
    ) => Array<[SnapshotFrom<T>, ExecutableActionsFrom<T>[]]>;

  * Given a state `machine`, a `snapshot`, and an `event`, returns an array of microsteps, where each microstep is a tuple of `[snapshot, actions]`.

This is a pure function that does not execute `actions`.




### function [getNextSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/getNextSnapshot.d.ts#L37 "View definition for getNextSnapshot")
    
    
    getNextSnapshot: <T extends AnyActorLogic>(
    
        actorLogic: T,
    
        snapshot: SnapshotFrom<T>,
    
        event: EventFromLogic<T>
    
    ) => SnapshotFrom<T>;

  * Determines the next snapshot for the given `actorLogic` based on the given `snapshot` and `event`.

If the `snapshot` is `undefined`, the initial snapshot of the `actorLogic` is used.

#### Example 1
        
        import { getNextSnapshot } from 'xstate';
        
        import { trafficLightMachine } from './trafficLightMachine.ts';
        
        
        
        
        const nextSnapshot = getNextSnapshot(
        
          trafficLightMachine, // actor logic
        
          undefined, // snapshot (or initial state if undefined)
        
          { type: 'TIMER' }
        
        ); // event object
        
        
        
        
        console.log(nextSnapshot.value);
        
        // => 'yellow'
        
        
        
        
        const nextSnapshot2 = getNextSnapshot(
        
          trafficLightMachine, // actor logic
        
          nextSnapshot, // snapshot
        
          { type: 'TIMER' }
        
        ); // event object
        
        
        
        
        console.log(nextSnapshot2.value);
        
        // =>'red'

#### Deprecated

Use `transition(…)` instead.




### function [getNextTransitions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts#L56 "View definition for getNextTransitions")
    
    
    getNextTransitions: (state: AnyMachineSnapshot) => AnyTransitionDefinition[];

  * Gets all potential next transitions from the current state.

Returns all transitions that are available from the current state, including:

\- All transitions from atomic states (leaf states in the current state configuration) - All transitions from ancestor states (parent states that may handle events) - All guarded transitions (regardless of whether their guards would pass) - Always (eventless) transitions - After (delayed) transitions

The order of transitions is deterministic:

1\. Atomic states are processed in document order 2. For each atomic state, transitions are collected from the state itself first, then its ancestors 3. Within each state node, transitions are in the order they appear in the state definition

#### Parameter state

The current machine snapshot

#### Returns

Array of transition definitions from the current state, in deterministic order




### function [getStateNodes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/stateUtils.d.ts#L34 "View definition for getStateNodes")
    
    
    getStateNodes: (
    
        stateNode: AnyStateNode,
    
        stateValue: StateValue
    
    ) => Array<AnyStateNode>;

  * Returns the state nodes represented by the current state value.

#### Parameter stateValue

The state value or State instance




### function [initialTransition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts#L16 "View definition for initialTransition")
    
    
    initialTransition: <T extends AnyActorLogic>(
    
        logic: T,
    
        ...[input]: undefined extends InputFrom<T>
    
            ? [input?: InputFrom<T>]
    
            : [input: InputFrom<T>]
    
    ) => [SnapshotFrom<T>, ExecutableActionsFrom<T>[]];

  * Given actor `logic` and optional `input`, returns a tuple of the `nextSnapshot` and `actions` to execute from the initial transition (no previous state).

This is a pure function that does not execute `actions`.




### function [isMachineSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/State.d.ts#L7 "View definition for isMachineSnapshot")
    
    
    isMachineSnapshot: (value: unknown) => value is AnyMachineSnapshot;




### function [log](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/log.d.ts#L15 "View definition for log")
    
    
    log: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject
    
    >(
    
        value?: ResolvableLogValue<TContext, TExpressionEvent, TParams, TEvent>,
    
        label?: string
    
    ) => LogAction<TContext, TExpressionEvent, TParams, TEvent>;

  * #### Parameter expr

The expression function to evaluate which will be logged. Takes in 2 arguments:

\- `ctx` \- the current state context - `event` \- the event that caused this action to be executed.

#### Parameter label

The label to give to the logged expression.




### function [matchesState](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/utils.d.ts#L3 "View definition for matchesState")
    
    
    matchesState: (parentStateId: StateValue, childStateId: StateValue) => boolean;




### function [not](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L58 "View definition for not")
    
    
    not: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TArg
    
    >(
    
        guard: SingleGuardArg<TContext, TExpressionEvent, unknown, TArg>
    
    ) => GuardPredicate<
    
        TContext,
    
        TExpressionEvent,
    
        unknown,
    
        NormalizeGuardArg<DoNotInfer<TArg>>
    
    >;

  * Higher-order guard that evaluates to `true` if the `guard` passed to it evaluates to `false`.

Guards

#### Returns

A guard

#### Example 1
        
        import { setup, not } from 'xstate';
        
        
        
        
        const machine = setup({
        
          guards: {
        
            someNamedGuard: () => false
        
          }
        
        }).createMachine({
        
          on: {
        
            someEvent: {
        
              guard: not('someNamedGuard'),
        
              actions: () => {
        
                // will be executed if guard in `not(...)`
        
                // evaluates to `false`
        
              }
        
            }
        
          }
        
        });




### function [or](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L122 "View definition for or")
    
    
    or: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TArg extends unknown[]
    
    >(
    
        guards: readonly [
    
            ...{
    
                [K in keyof TArg]: SingleGuardArg<
    
                    TContext,
    
                    TExpressionEvent,
    
                    unknown,
    
                    TArg[K]
    
                >;
    
            }
    
        ]
    
    ) => GuardPredicate<
    
        TContext,
    
        TExpressionEvent,
    
        unknown,
    
        NormalizeGuardArgArray<DoNotInfer<TArg>>
    
    >;

  * Higher-order guard that evaluates to `true` if any of the `guards` passed to it evaluate to `true`.

Guards

#### Returns

A guard action object

#### Example 1
        
        import { setup, or } from 'xstate';
        
        
        
        
        const machine = setup({
        
          guards: {
        
            someNamedGuard: () => true
        
          }
        
        }).createMachine({
        
          on: {
        
            someEvent: {
        
              guard: or([({ context }) => context.value > 0, 'someNamedGuard']),
        
              actions: () => {
        
                // will be executed if any of the guards in `or(...)`
        
                // evaluate to true
        
              }
        
            }
        
          }
        
        });




### function [pathToStateValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/utils.d.ts#L5 "View definition for pathToStateValue")
    
    
    pathToStateValue: (statePath: string[]) => StateValue;




### function [raise](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/raise.d.ts#L13 "View definition for raise")
    
    
    raise: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TParams extends {},
    
        TDelay extends string = never,
    
        TUsedDelay extends TDelay = never
    
    >(
    
        eventOrExpr:
    
            | DoNotInfer<TEvent>
    
            | SendExpr<TContext, TExpressionEvent, TParams, DoNotInfer<TEvent>, TEvent>,
    
        options?: RaiseActionOptions<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            DoNotInfer<TEvent>,
    
            TUsedDelay
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        never,
    
        never,
    
        never,
    
        TDelay,
    
        never
    
    >;

  * Raises an event. This places the event in the internal event queue, so that the event is immediately consumed by the machine in the current step.

#### Parameter eventType

The event to raise.




### function [sendParent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts#L24 "View definition for sendParent")
    
    
    sendParent: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TSentEvent extends EventObject = AnyEventObject,
    
        TEvent extends EventObject = AnyEventObject,
    
        TDelay extends string = never,
    
        TUsedDelay extends TDelay = never
    
    >(
    
        event:
    
            | TSentEvent
    
            | SendExpr<TContext, TExpressionEvent, TParams, TSentEvent, TEvent>,
    
        options?: SendToActionOptions<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            TEvent,
    
            TUsedDelay
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        never,
    
        never,
    
        never,
    
        TDelay,
    
        never
    
    >;

  * Sends an event to this machine's parent.

#### Parameter event

The event to send to the parent machine.

#### Parameter options

Options to pass into the send event.




### function [sendTo](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts#L17 "View definition for sendTo")
    
    
    sendTo: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TTargetActor extends AnyActorRef,
    
        TEvent extends EventObject,
    
        TDelay extends string = never,
    
        TUsedDelay extends TDelay = never
    
    >(
    
        to: SendToActionTarget<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            TTargetActor,
    
            TEvent
    
        >,
    
        eventOrExpr:
    
            | EventFrom<TTargetActor>
    
            | SendExpr<
    
                  TContext,
    
                  TExpressionEvent,
    
                  TParams,
    
                  InferEvent<Cast<EventFrom<TTargetActor>, EventObject>>,
    
                  TEvent
    
              >,
    
        options?: SendToActionOptions<
    
            TContext,
    
            TExpressionEvent,
    
            TParams,
    
            DoNotInfer<TEvent>,
    
            TUsedDelay
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        never,
    
        never,
    
        never,
    
        TDelay,
    
        never
    
    >;

  * Sends an event to an actor.

#### Parameter actor

The `ActorRef` to send the event to.

#### Parameter event

The event to send, or an expression that evaluates to the event to send

#### Parameter options

Send action options

\- `id` \- The unique send event identifier (used with `cancel()`). - `delay` \- The number of milliseconds to delay the sending of the event.




### function [setup](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/setup.d.ts#L113 "View definition for setup")
    
    
    setup: <
    
        TContext extends MachineContext,
    
        TEvent extends AnyEventObject,
    
        TActors extends Record<string, UnknownActorLogic> = {},
    
        TChildrenMap extends Record<string, string> = {},
    
        TActions extends Record<string, {}> = {},
    
        TGuards extends Record<string, {}> = {},
    
        TDelay extends string = never,
    
        TTag extends string = string,
    
        TInput = {},
    
        TOutput extends {} = {},
    
        TEmitted extends EventObject = EventObject,
    
        TMeta extends MetaObject = MetaObject
    
    >({
    
        schemas,
    
        actors,
    
        actions,
    
        guards,
    
        delays,
    
    }: {
    
        schemas?: unknown;
    
        types?: SetupTypes<
    
            TContext,
    
            TEvent,
    
            TChildrenMap,
    
            TTag,
    
            TInput,
    
            TOutput,
    
            TEmitted,
    
            TMeta
    
        >;
    
        actors?: {
    
            [K in keyof TActors | Values<TChildrenMap>]: K extends keyof TActors
    
                ? TActors[K]
    
                : never;
    
        };
    
        actions?: {
    
            [K in keyof TActions]: ActionFunction<
    
                TContext,
    
                TEvent,
    
                TEvent,
    
                TActions[K],
    
                ToProvidedActor<TChildrenMap, TActors>,
    
                ToParameterizedObject<TActions>,
    
                ToParameterizedObject<TGuards>,
    
                TDelay,
    
                TEmitted
    
            >;
    
        };
    
        guards?: {
    
            [K in keyof TGuards]: GuardPredicate<
    
                TContext,
    
                TEvent,
    
                TGuards[K],
    
                ToParameterizedObject<TGuards>
    
            >;
    
        };
    
        delays?: {
    
            [K in TDelay]: DelayConfig<
    
                TContext,
    
                TEvent,
    
                ToParameterizedObject<TActions>['params'],
    
                TEvent
    
            >;
    
        };
    
    } & { [K in RequiredSetupKeys<TChildrenMap>]: unknown }) => SetupReturn<
    
        TContext,
    
        TEvent,
    
        TActors,
    
        TChildrenMap,
    
        TActions,
    
        TGuards,
    
        TDelay,
    
        TTag,
    
        TInput,
    
        TOutput,
    
        TEmitted,
    
        TMeta
    
    >;




### function [spawnChild](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L33 "View definition for spawnChild")
    
    
    spawnChild: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    >(
    
        ...[src, { id, systemId, input, syncSnapshot }]: SpawnArguments<
    
            TContext,
    
            TExpressionEvent,
    
            TEvent,
    
            TActor
    
        >
    
    ) => ActionFunction<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        TParams,
    
        TActor,
    
        never,
    
        never,
    
        never,
    
        never
    
    >;




### function [stateIn](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L28 "View definition for stateIn")
    
    
    stateIn: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {}
    
    >(
    
        stateValue: StateValue
    
    ) => GuardPredicate<TContext, TExpressionEvent, TParams, any>;




### function [stopChild](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/stopChild.d.ts#L11 "View definition for stopChild")
    
    
    stopChild: <
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends {},
    
        TEvent extends EventObject
    
    >(
    
        actorRef: ResolvableActorRef<TContext, TExpressionEvent, TParams, TEvent>
    
    ) => StopAction<TContext, TExpressionEvent, TParams, TEvent>;

  * Stops a child actor.

#### Parameter actorRef

The actor to stop.




### function [toObserver](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/utils.d.ts#L14 "View definition for toObserver")
    
    
    toObserver: <T>(
    
        nextHandler?: Observer<T> | ((value: T) => void),
    
        errorHandler?: (error: any) => void,
    
        completionHandler?: () => void
    
    ) => Observer<T>;




### function [toPromise](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/toPromise.d.ts#L25 "View definition for toPromise")
    
    
    toPromise: <T extends AnyActorRef>(actor: T) => Promise<OutputFrom<T>>;

  * Returns a promise that resolves to the `output` of the actor when it is done.

#### Example 1
        
        const machine = createMachine({
        
          // ...
        
          output: {
        
            count: 42
        
          }
        
        });
        
        
        
        
        const actor = createActor(machine);
        
        
        
        
        actor.start();
        
        
        
        
        const output = await toPromise(actor);
        
        
        
        
        console.log(output);
        
        // logs { count: 42 }




### function [transition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts#L8 "View definition for transition")
    
    
    transition: <T extends AnyActorLogic>(
    
        logic: T,
    
        snapshot: SnapshotFrom<T>,
    
        event: EventFromLogic<T>
    
    ) => [nextSnapshot: SnapshotFrom<T>, actions: ExecutableActionsFrom<T>[]];

  * Given actor `logic`, a `snapshot`, and an `event`, returns a tuple of the `nextSnapshot` and `actions` to execute.

This is a pure function that does not execute `actions`.




### function [waitFor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/waitFor.d.ts#L34 "View definition for waitFor")
    
    
    waitFor: <TActorRef extends AnyActorRef>(
    
        actorRef: TActorRef,
    
        predicate: (emitted: SnapshotFrom<TActorRef>) => boolean,
    
        options?: Partial<WaitForOptions>
    
    ) => Promise<SnapshotFrom<TActorRef>>;

  * Subscribes to an actor ref and waits for its emitted value to satisfy a predicate, and then resolves with that value. Will throw if the desired state is not reached after an optional timeout. (defaults to Infinity).

#### Parameter actorRef

The actor ref to subscribe to

#### Parameter predicate

Determines if a value matches the condition to wait for

#### Parameter options

#### Returns

A promise that eventually resolves to the emitted value that matches the condition

#### Example 1
        
        const state = await waitFor(someService, (state) => {
        
          return state.hasTag('loaded');
        
        });
        
        
        
        
        state.hasTag('loaded'); // true




## Classes

### class [Actor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L17 "View definition for Actor")
    
    
    class Actor<TLogic extends AnyActorLogic>
    
        implements
    
            ActorRef<
    
                SnapshotFrom<TLogic>,
    
                EventFromLogic<TLogic>,
    
                EmittedFrom<TLogic>
    
            > {}

  * An Actor is a running process that can receive events, send events and change its behavior based on the events it receives, which can cause effects outside of the actor. When you run a state machine, it becomes an actor.




###  [constructor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L50 "View definition for constructor")
    
    
    constructor(
    
        logic: ActorLogic<any, any, any, any, any>,
    
        options?: ActorOptions<TLogic>
    
    );

  * Creates a new actor instance for the given logic with the provided options, if any.

#### Parameter logic

The logic to create an actor from

#### Parameter options

Actor options




### property [clock](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L25 "View definition for clock")
    
    
    clock: Clock;

  * The clock that is responsible for setting and clearing timeouts, such as delayed events and transitions.




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L28 "View definition for id")
    
    
    id: string;

  * The unique identifier for this actor relative to its parent.




### property [logic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L18 "View definition for logic")
    
    
    logic: ActorLogic<any, any, any, any, any>;




### property [options](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L26 "View definition for options")
    
    
    options: Readonly<ActorOptions<TLogic>>;




### property [ref](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L34 "View definition for ref")
    
    
    ref: ActorRef<SnapshotFrom<TLogic>, EventFromLogic<TLogic>, EmittedFrom<TLogic>>;




### property [sessionId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L38 "View definition for sessionId")
    
    
    sessionId: string;

  * The globally unique process ID for this invocation.




### property [src](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L42 "View definition for src")
    
    
    src: string | AnyActorLogic;




### property [system](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L40 "View definition for system")
    
    
    system: AnyActorSystem;

  * The system to which this actor belongs.




### property [systemId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L36 "View definition for systemId")
    
    
    systemId: string;




### method [[symbolObservable]](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L153 "View definition for \[symbolObservable\]")
    
    
    [symbolObservable]: () => InteropSubscribable<SnapshotFrom<TLogic>>;




### method [getPersistedSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L152 "View definition for getPersistedSnapshot")
    
    
    getPersistedSnapshot: () => Snapshot<unknown>;

  * Obtain the internal state of the actor, which can be persisted.

#### Remarks

The internal state can be persisted from any actor, not only machines.

Note that the persisted state is not the same as the snapshot from Actor.getSnapshot. Persisted state represents the internal state of the actor, while snapshots represent the actor's last emitted value.

Can be restored with ActorOptions.state

#### See Also

    * https://stately.ai/docs/persistence




### method [getSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L168 "View definition for getSnapshot")
    
    
    getSnapshot: () => SnapshotFrom<TLogic>;

  * Read an actor’s snapshot synchronously.

#### Remarks

The snapshot represent an actor's last emitted value.

When an actor receives an event, its internal state may change. An actor may emit a snapshot when a state transition occurs.

Note that some actors, such as callback actors generated with `fromCallback`, will not emit snapshots.

#### See Also

    * Actor.subscribe to subscribe to an actor’s snapshot values.

    * Actor.getPersistedSnapshot to persist the internal state of an actor (which is more than just a snapshot).




### method [on](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L115 "View definition for on")
    
    
    on: <TType extends '*' | EmittedFrom<TLogic>['type']>(
    
        type: TType,
    
        handler: (
    
            emitted: EmittedFrom<TLogic> &
    
                (TType extends '*' ? unknown : { type: TType })
    
        ) => void
    
    ) => Subscription;




### method [send](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L133 "View definition for send")
    
    
    send: (event: EventFromLogic<TLogic>) => void;

  * Sends an event to the running Actor to trigger a transition.

#### Parameter event

The event to send




### method [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L119 "View definition for start")
    
    
    start: () => this;

  * Starts the Actor from the initial state




### method [stop](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L123 "View definition for stop")
    
    
    stop: () => this;

  * Stops the Actor and unsubscribe all listeners.




### method [subscribe](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L113 "View definition for subscribe")
    
    
    subscribe: {
    
        (observer: Observer<SnapshotFrom<TLogic>>): Subscription;
    
        (
    
            nextListener?: (snapshot: SnapshotFrom<TLogic>) => void,
    
            errorListener?: (error: any) => void,
    
            completeListener?: () => void
    
        ): Subscription;
    
    };

  * Subscribe an observer to an actor’s snapshot values.

#### Parameter observer

Either a plain function that receives the latest snapshot, or an observer object whose `.next(snapshot)` method receives the latest snapshot

#### Remarks

The observer will receive the actor’s snapshot value when it is emitted. The observer can be:

\- A plain function that receives the latest snapshot, or - An observer object whose `.next(snapshot)` method receives the latest snapshot

#### Example 1
        
        // Observer as a plain function
        
        const subscription = actor.subscribe((snapshot) => {
        
          console.log(snapshot);
        
        });

#### Example 2
        
        // Observer as an object
        
        const subscription = actor.subscribe({
        
          next(snapshot) {
        
            console.log(snapshot);
        
          },
        
          error(err) {
        
            // ...
        
          },
        
          complete() {
        
            // ...
        
          }
        
        });

The return value of `actor.subscribe(observer)` is a subscription object that has an `.unsubscribe()` method. You can call `subscription.unsubscribe()` to unsubscribe the observer:

#### Example 3
        
        const subscription = actor.subscribe((snapshot) => {
        
          // ...
        
        });
        
        
        
        
        // Unsubscribe the observer
        
        subscription.unsubscribe();

When the actor is stopped, all of its observers will automatically be unsubscribed.




### method [toJSON](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L135 "View definition for toJSON")
    
    
    toJSON: () => { xstate$$type: number; id: string };




### class [SimulatedClock](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L7 "View definition for SimulatedClock")
    
    
    class SimulatedClock implements SimulatedClock {}




### method [clearTimeout](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L16 "View definition for clearTimeout")
    
    
    clearTimeout: (id: number) => void;




### method [now](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L13 "View definition for now")
    
    
    now: () => number;




### method [setTimeout](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L15 "View definition for setTimeout")
    
    
    setTimeout: (fn: (...args: any[]) => void, timeout: number) => number;




### class [StateMachine](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L5 "View definition for StateMachine")
    
    
    class StateMachine<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TChildren extends Record<string, AnyActorRef | undefined>,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TStateValue extends StateValue,
    
        TTag extends string,
    
        TInput,
    
        TOutput,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject,
    
        TStateSchema extends StateSchema
    
    > implements
    
            ActorLogic<
    
                MachineSnapshot<
    
                    TContext,
    
                    TEvent,
    
                    TChildren,
    
                    TStateValue,
    
                    TTag,
    
                    TOutput,
    
                    TMeta,
    
                    TStateSchema
    
                >,
    
                TEvent,
    
                TInput,
    
                AnyActorSystem,
    
                TEmitted
    
            > {}




###  [constructor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L19 "View definition for constructor")
    
    
    constructor(
    
        config: Omit<
    
            StateNodeConfig<
    
                DoNotInfer<TContext>,
    
                DoNotInfer<TEvent>,
    
                any,
    
                any,
    
                any,
    
                any,
    
                any,
    
                DoNotInfer<TOutput>,
    
                any,
    
                any
    
            >,
    
            'output'
    
        > & {
    
            version?: string;
    
            output?:
    
                | TOutput
    
                | Mapper<TContext, DoneStateEvent<unknown>, TOutput, TEvent>;
    
        } & (
    
                | { context?: InitialContext<TContext, any, any, TEvent> }
    
                | { context: InitialContext<TContext, any, any, TEvent> }
    
            ) & { schemas?: unknown },
    
        implementations?: MachineImplementationsSimplified<
    
            TContext,
    
            TEvent,
    
            ProvidedActor,
    
            ParameterizedObject,
    
            ParameterizedObject
    
        >
    
    );




### property [config](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L7 "View definition for config")
    
    
    config: Omit<
    
        StateNodeConfig<
    
            DoNotInfer<TContext>,
    
            DoNotInfer<TEvent>,
    
            any,
    
            any,
    
            any,
    
            any,
    
            any,
    
            DoNotInfer<TOutput>,
    
            any,
    
            any
    
        >,
    
        'output'
    
    > & {
    
        version?: string;
    
        output?:
    
            | TOutput
    
            | Mapper<TContext, DoneStateEvent<unknown>, TOutput, TEvent>;
    
    } & (
    
            | { context?: InitialContext<TContext, any, any, TEvent> }
    
            | { context: InitialContext<TContext, any, any, TEvent> }
    
        ) & { schemas?: unknown };

  * The raw config used to create the machine.




### property [definition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L67 "View definition for definition")
    
    
    readonly definition: StateMachineDefinition<TContext, TEvent>;




### property [events](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L18 "View definition for events")
    
    
    events: EventDescriptor<TEvent>[];




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L16 "View definition for id")
    
    
    id: string;




### property [implementations](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L14 "View definition for implementations")
    
    
    implementations: MachineImplementationsSimplified<
    
        TContext,
    
        TEvent,
    
        ProvidedActor,
    
        ParameterizedObject,
    
        ParameterizedObject
    
    >;




### property [root](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L15 "View definition for root")
    
    
    root: StateNode<TContext, TEvent>;




### property [schemas](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L13 "View definition for schemas")
    
    
    schemas: {};




### property [states](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L17 "View definition for states")
    
    
    states: StateNodesConfig<TContext, TEvent>;




### property [version](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L12 "View definition for version")
    
    
    version?: string;

  * The machine's own version.




### method [getInitialSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L64 "View definition for getInitialSnapshot")
    
    
    getInitialSnapshot: (
    
        actorScope: ActorScope<
    
            MachineSnapshot<
    
                TContext,
    
                TEvent,
    
                TChildren,
    
                TStateValue,
    
                TTag,
    
                TOutput,
    
                TMeta,
    
                TStateSchema
    
            >,
    
            TEvent,
    
            AnyActorSystem,
    
            TEmitted
    
        >,
    
        input?: TInput
    
    ) => MachineSnapshot<
    
        TContext,
    
        TEvent,
    
        TChildren,
    
        TStateValue,
    
        TTag,
    
        TOutput,
    
        TMeta,
    
        TStateSchema
    
    >;

  * Returns the initial `State` instance, with reference to `self` as an `ActorRef`.




### method [getPersistedSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L69 "View definition for getPersistedSnapshot")
    
    
    getPersistedSnapshot: (
    
        snapshot: MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >,
    
        options?: unknown
    
    ) => Snapshot<unknown>;




### method [getStateNodeById](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L66 "View definition for getStateNodeById")
    
    
    getStateNodeById: (stateId: string) => StateNode<TContext, TEvent>;




### method [getTransitionData](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L59 "View definition for getTransitionData")
    
    
    getTransitionData: (
    
        snapshot: MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >,
    
        event: TEvent
    
    ) => Array<TransitionDefinition<TContext, TEvent>>;




### method [microstep](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L58 "View definition for microstep")
    
    
    microstep: (
    
        snapshot: MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >,
    
        event: TEvent,
    
        actorScope: AnyActorScope
    
    ) => Array<
    
        MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >
    
    >;

  * Determines the next state given the current `state` and `event`. Calculates a microstep.

#### Parameter state

The current state

#### Parameter event

The received event




### method [provide](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L32 "View definition for provide")
    
    
    provide: (
    
        implementations: InternalMachineImplementations<
    
            ResolvedStateMachineTypes<
    
                TContext,
    
                DoNotInfer<TEvent>,
    
                TActor,
    
                TAction,
    
                TGuard,
    
                TDelay,
    
                TTag,
    
                TEmitted
    
            >
    
        >
    
    ) => StateMachine<
    
        TContext,
    
        TEvent,
    
        TChildren,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TStateValue,
    
        TTag,
    
        TInput,
    
        TOutput,
    
        TEmitted,
    
        TMeta,
    
        TStateSchema
    
    >;

  * Clones this state machine with the provided implementations.

#### Parameter implementations

Options (`actions`, `guards`, `actors`, `delays`) to recursively merge with the existing options.

#### Returns

A new `StateMachine` instance with the provided implementations.




### method [resolveState](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L33 "View definition for resolveState")
    
    
    resolveState: (
    
        config: {
    
            value: StateValue;
    
            context?: TContext;
    
            historyValue?: HistoryValue<TContext, TEvent>;
    
            status?: SnapshotStatus;
    
            output?: TOutput;
    
            error?: unknown;
    
        } & (Equals<TContext, MachineContext> extends false
    
            ? { context: unknown }
    
            : {})
    
    ) => MachineSnapshot<
    
        TContext,
    
        TEvent,
    
        TChildren,
    
        TStateValue,
    
        TTag,
    
        TOutput,
    
        TMeta,
    
        TStateSchema
    
    >;




### method [restoreSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L70 "View definition for restoreSnapshot")
    
    
    restoreSnapshot: (
    
        snapshot: Snapshot<unknown>,
    
        _actorScope: ActorScope<
    
            MachineSnapshot<
    
                TContext,
    
                TEvent,
    
                TChildren,
    
                TStateValue,
    
                TTag,
    
                TOutput,
    
                TMeta,
    
                TStateSchema
    
            >,
    
            TEvent,
    
            AnyActorSystem,
    
            TEmitted
    
        >
    
    ) => MachineSnapshot<
    
        TContext,
    
        TEvent,
    
        TChildren,
    
        TStateValue,
    
        TTag,
    
        TOutput,
    
        TMeta,
    
        TStateSchema
    
    >;




### method [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L65 "View definition for start")
    
    
    start: (
    
        snapshot: MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >
    
    ) => void;




### method [toJSON](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L68 "View definition for toJSON")
    
    
    toJSON: () => StateMachineDefinition<TContext, TEvent>;




### method [transition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts#L50 "View definition for transition")
    
    
    transition: (
    
        snapshot: MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            TChildren,
    
            TStateValue,
    
            TTag,
    
            TOutput,
    
            TMeta,
    
            TStateSchema
    
        >,
    
        event: TEvent,
    
        actorScope: ActorScope<typeof snapshot, TEvent, AnyActorSystem, TEmitted>
    
    ) => MachineSnapshot<
    
        TContext,
    
        TEvent,
    
        TChildren,
    
        TStateValue,
    
        TTag,
    
        TOutput,
    
        TMeta,
    
        TStateSchema
    
    >;

  * Determines the next snapshot given the current `snapshot` and received `event`. Calculates a full macrostep from all microsteps.

#### Parameter snapshot

The current snapshot

#### Parameter event

The received event




### class [StateNode](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L8 "View definition for StateNode")
    
    
    class StateNode<
    
        TContext extends MachineContext = MachineContext,
    
        TEvent extends EventObject = EventObject
    
    > {}




###  [constructor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L84 "View definition for constructor")
    
    
    constructor(
    
        config: StateNodeConfig<
    
            TContext,
    
            TEvent,
    
            any,
    
            any,
    
            any,
    
            any,
    
            any,
    
            any,
    
            any,
    
            any
    
        >,
    
        options: StateNodeOptions<TContext, TEvent>
    
    );




### property [after](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L101 "View definition for after")
    
    
    readonly after: DelayedTransitionDefinition<TContext, TEvent>[];




### property [always](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L83 "View definition for always")
    
    
    always?: TransitionDefinition<TContext, TEvent>[];




### property [config](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L10 "View definition for config")
    
    
    config: StateNodeConfig<
    
        TContext,
    
        TEvent,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any
    
    >;

  * The raw config used to create the machine.




### property [definition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L95 "View definition for definition")
    
    
    readonly definition: StateNodeDefinition<TContext, TEvent>;

  * The well-structured state node definition.




### property [description](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L80 "View definition for description")
    
    
    description?: string;




### property [entry](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L47 "View definition for entry")
    
    
    entry: UnknownAction[];

  * The action(s) to be executed upon entering the state node.




### property [events](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L104 "View definition for events")
    
    
    readonly events: EventDescriptor<TEvent>[];

  * All the event types accepted by this state node and its descendants.




### property [exit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L49 "View definition for exit")
    
    
    exit: UnknownAction[];

  * The action(s) to be executed upon exiting the state node.




### property [history](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L45 "View definition for history")
    
    
    history: false | 'shallow' | 'deep';

  * The type of history on this state node. Can be:

\- `'shallow'` \- recalls only top-level historical state value - `'deep'` \- recalls historical state value at all levels




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L24 "View definition for id")
    
    
    id: string;

  * The unique ID of the state node.




### property [initial](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L102 "View definition for initial")
    
    
    readonly initial: InitialTransitionDefinition<TContext, TEvent>;




### property [invoke](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L97 "View definition for invoke")
    
    
    readonly invoke: InvokeDefinition<
    
        TContext,
    
        TEvent,
    
        ProvidedActor,
    
        ParameterizedObject,
    
        ParameterizedObject,
    
        string,
    
        any,
    
        any
    
    >[];

  * The logic invoked as actors by this state node.




### property [key](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L22 "View definition for key")
    
    
    key: string;

  * The relative key of the state node, which represents its location in the overall state value.




### property [machine](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L53 "View definition for machine")
    
    
    machine: StateMachine<
    
        TContext,
    
        TEvent,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any
    
    >;

  * The root machine node.




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L69 "View definition for meta")
    
    
    meta?: any;

  * The meta data associated with this state node, which will be returned in State instances.




### property [on](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L100 "View definition for on")
    
    
    readonly on: TransitionDefinitionMap<TContext, TEvent>;

  * The mapping of events to transitions.




### property [order](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L79 "View definition for order")
    
    
    order: number;

  * The order this state node appears. Corresponds to the implicit document order.




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L74 "View definition for output")
    
    
    output?: {} | Mapper<MachineContext, EventObject, unknown, EventObject>;

  * The output data sent with the "xstate.done.state._id_" event if this is a final state node.




### property [ownEvents](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L110 "View definition for ownEvents")
    
    
    readonly ownEvents: EventDescriptor<TEvent>[];

  * All the events that have transitions directly from this state node.

Excludes any inert events.




### property [parent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L51 "View definition for parent")
    
    
    parent?: StateNode<TContext, TEvent>;

  * The parent state node.




### property [path](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L36 "View definition for path")
    
    
    path: string[];

  * The string path from the root machine node to this node.




### property [states](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L38 "View definition for states")
    
    
    states: StateNodesConfig<TContext, TEvent>;

  * The child state nodes.




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L81 "View definition for tags")
    
    
    tags: string[];




### property [transitions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L82 "View definition for transitions")
    
    
    transitions: Map<string, TransitionDefinition<TContext, TEvent>[]>;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts#L34 "View definition for type")
    
    
    type: 'history' | 'atomic' | 'compound' | 'parallel' | 'final';

  * The type of this state node:

\- `'atomic'` \- no child state nodes - `'compound'` \- nested child state nodes (XOR) - `'parallel'` \- orthogonal nested child state nodes (AND) - `'history'` \- history state node - `'final'` \- final state node




## Interfaces

### interface [ActionArgs](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L91 "View definition for ActionArgs")
    
    
    interface ActionArgs<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject
    
    > extends UnifiedArg<TContext, TExpressionEvent, TEvent> {}




### interface [ActorLike](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L754 "View definition for ActorLike")
    
    
    interface ActorLike<TCurrent, TEvent extends EventObject>
    
        extends Subscribable<TCurrent> {}




### property [send](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L755 "View definition for send")
    
    
    send: (event: TEvent) => void;




### interface [ActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L826 "View definition for ActorLogic")
    
    
    interface ActorLogic<
    
        in out TSnapshot extends Snapshot<unknown>, // it's invariant because it's also part of `ActorScope["self"]["getSnapshot"]`
    
        in out TEvent extends EventObject, // it's invariant because it's also part of `ActorScope["self"]["send"]`
    
        in TInput = NonReducibleUnknown,
    
        TSystem extends AnyActorSystem = AnyActorSystem,
    
        in out TEmitted extends EventObject = EventObject
    
    > {}

  * Represents logic which can be used by an actor.

TSnapshot - The type of the snapshot.  TEvent - The type of the event object.  TInput - The type of the input.  TSystem - The type of the actor system.




### property [config](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L830 "View definition for config")
    
    
    config?: unknown;

  * The initial setup/configuration used to create the actor logic.




### property [getInitialSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L848 "View definition for getInitialSnapshot")
    
    
    getInitialSnapshot: (
    
        actorScope: ActorScope<TSnapshot, TEvent, TSystem, TEmitted>,
    
        input: TInput
    
    ) => TSnapshot;

  * Called to provide the initial state of the actor.

#### Parameter actorScope

The actor scope.

#### Parameter input

The input for the initial state.

#### Returns

The initial state.




### property [getPersistedSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L873 "View definition for getPersistedSnapshot")
    
    
    getPersistedSnapshot: (
    
        snapshot: TSnapshot,
    
        options?: unknown
    
    ) => Snapshot<unknown>;

  * Obtains the internal state of the actor in a representation which can be be persisted. The persisted state can be restored by `restoreSnapshot`.

#### Parameter snapshot

The current state.

#### Returns

The a representation of the internal state to be persisted.




### property [restoreSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L858 "View definition for restoreSnapshot")
    
    
    restoreSnapshot?: (
    
        persistedState: Snapshot<unknown>,
    
        actorScope: ActorScope<TSnapshot, TEvent, AnyActorSystem, TEmitted>
    
    ) => TSnapshot;

  * Called when Actor is created to restore the internal state of the actor given a persisted state. The persisted state can be created by `getPersistedSnapshot`.

#### Parameter persistedState

The persisted state to restore from.

#### Parameter actorScope

The actor scope.

#### Returns

The restored state.




### property [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L865 "View definition for start")
    
    
    start?: (
    
        snapshot: TSnapshot,
    
        actorScope: ActorScope<TSnapshot, TEvent, AnyActorSystem, TEmitted>
    
    ) => void;

  * Called when the actor is started.

#### Parameter snapshot

The starting state.

#### Parameter actorScope

The actor scope.




### property [transition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L840 "View definition for transition")
    
    
    transition: (
    
        snapshot: TSnapshot,
    
        event: TEvent,
    
        actorScope: ActorScope<TSnapshot, TEvent, TSystem, TEmitted>
    
    ) => TSnapshot;

  * Transition function that processes the current state and an incoming event to produce a new state.

#### Parameter snapshot

The current state.

#### Parameter event

The incoming event.

#### Parameter actorScope

The actor scope.

#### Returns

The new state.




### interface [ActorOptions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L594 "View definition for ActorOptions")
    
    
    interface ActorOptions<TLogic extends AnyActorLogic> {}




### property [clock](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L612 "View definition for clock")
    
    
    clock?: Clock;

  * The clock that is responsible for setting and clearing timeouts, such as delayed events and transitions.

#### Remarks

You can create your own “clock”. The clock interface is an object with two functions/methods:

\- `setTimeout` \- same arguments as `window.setTimeout(fn, timeout)` \- `clearTimeout` \- same arguments as `window.clearTimeout(id)`

By default, the native `setTimeout` and `clearTimeout` functions are used.

For testing, XState provides `SimulatedClock`.

#### See Also

    * Clock

    * SimulatedClock




### property [devTools](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L622 "View definition for devTools")
    
    
    devTools?: never;

  * #### Deprecated

Use `inspect` instead.




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L620 "View definition for id")
    
    
    id?: string;

  * The custom `id` for referencing this service.




### property [input](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L626 "View definition for input")
    
    
    input?: InputFrom<TLogic>;

  * The input data to pass to the actor.




### property [inspect](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L726 "View definition for inspect")
    
    
    inspect?:
    
        | Observer<InspectionEvent>
    
        | ((inspectionEvent: InspectionEvent) => void);

  * A callback function or observer object which can be used to inspect actor system updates.

#### Remarks

If a callback function is provided, it can accept an inspection event argument. The types of inspection events that can be observed include:

\- `@xstate.actor` \- An actor ref has been created in the system - `@xstate.event` \- An event was sent from a source actor ref to a target actor ref in the system - `@xstate.snapshot` \- An actor ref emitted a snapshot due to a received event

#### Example 1
        
        import { createMachine } from 'xstate';
        
        
        
        
        const machine = createMachine({
        
          // ...
        
        });
        
        
        
        
        const actor = createActor(machine, {
        
          inspect: (inspectionEvent) => {
        
            if (inspectionEvent.actorRef === actor) {
        
              // This event is for the root actor
        
            }
        
        
        
        
            if (inspectionEvent.type === '@xstate.actor') {
        
              console.log(inspectionEvent.actorRef);
        
            }
        
        
        
        
            if (inspectionEvent.type === '@xstate.event') {
        
              console.log(inspectionEvent.sourceRef);
        
              console.log(inspectionEvent.actorRef);
        
              console.log(inspectionEvent.event);
        
            }
        
        
        
        
            if (inspectionEvent.type === '@xstate.snapshot') {
        
              console.log(inspectionEvent.actorRef);
        
              console.log(inspectionEvent.event);
        
              console.log(inspectionEvent.snapshot);
        
            }
        
          }
        
        });

Alternately, an observer object (`{ next?, error?, complete? }`) can be provided:

#### Example 2
        
        const actor = createActor(machine, {
        
          inspect: {
        
            next: (inspectionEvent) => {
        
              if (inspectionEvent.actorRef === actor) {
        
                // This event is for the root actor
        
              }
        
        
        
        
              if (inspectionEvent.type === '@xstate.actor') {
        
                console.log(inspectionEvent.actorRef);
        
              }
        
        
        
        
              if (inspectionEvent.type === '@xstate.event') {
        
                console.log(inspectionEvent.sourceRef);
        
                console.log(inspectionEvent.actorRef);
        
                console.log(inspectionEvent.event);
        
              }
        
        
        
        
              if (inspectionEvent.type === '@xstate.snapshot') {
        
                console.log(inspectionEvent.actorRef);
        
                console.log(inspectionEvent.event);
        
                console.log(inspectionEvent.snapshot);
        
              }
        
            }
        
          }
        
        });




### property [logger](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L617 "View definition for logger")
    
    
    logger?: (...args: any[]) => void;

  * Specifies the logger to be used for `log(...)` actions. Defaults to the native `console.log(...)` method.




### property [parent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L618 "View definition for parent")
    
    
    parent?: AnyActorRef;




### property [snapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L640 "View definition for snapshot")
    
    
    snapshot?: Snapshot<unknown>;

  * Initializes actor logic from a specific persisted internal state.

#### Remarks

If the state is compatible with the actor logic, when the actor is started it will be at that persisted state. Actions from machine actors will not be re-executed, because they are assumed to have been already executed. However, invocations will be restarted, and spawned actors will be restored recursively.

Can be generated with Actor.getPersistedSnapshot.

#### See Also

    * https://stately.ai/docs/persistence




### property [src](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L644 "View definition for src")
    
    
    src?: string | AnyActorLogic;

  * The source actor logic.




### property [state](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L642 "View definition for state")
    
    
    state?: Snapshot<unknown>;

  * #### Deprecated

Use `snapshot` instead.




### property [systemId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L624 "View definition for systemId")
    
    
    systemId?: string;

  * The system ID to register this actor under.




### interface [ActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L757 "View definition for ActorRef")
    
    
    interface ActorRef<
    
        TSnapshot extends Snapshot<unknown>,
    
        TEvent extends EventObject,
    
        TEmitted extends EventObject = EventObject
    
    > extends Subscribable<TSnapshot>,
    
            InteropObservable<TSnapshot> {}




### property [getPersistedSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L764 "View definition for getPersistedSnapshot")
    
    
    getPersistedSnapshot: () => Snapshot<unknown>;




### property [getSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L763 "View definition for getSnapshot")
    
    
    getSnapshot: () => TSnapshot;




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L759 "View definition for id")
    
    
    id: string;

  * The unique identifier for this actor relative to its parent.




### property [on](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L770 "View definition for on")
    
    
    on: <TType extends TEmitted['type'] | '*'>(
    
        type: TType,
    
        handler: (
    
            emitted: TEmitted &
    
                (TType extends '*'
    
                    ? unknown
    
                    : {
    
                          type: TType;
    
                      })
    
        ) => void
    
    ) => Subscription;




### property [send](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L761 "View definition for send")
    
    
    send: (event: TEvent) => void;




### property [sessionId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L760 "View definition for sessionId")
    
    
    sessionId: string;




### property [src](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L769 "View definition for src")
    
    
    src: string | AnyActorLogic;




### property [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L762 "View definition for start")
    
    
    start: () => void;




### property [stop](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L765 "View definition for stop")
    
    
    stop: () => void;




### property [system](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L768 "View definition for system")
    
    
    system: AnyActorSystem;




### property [toJSON](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L766 "View definition for toJSON")
    
    
    toJSON?: () => any;




### interface [ActorScope](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L786 "View definition for ActorScope")
    
    
    interface ActorScope<
    
        TSnapshot extends Snapshot<unknown>,
    
        TEvent extends EventObject,
    
        TSystem extends AnyActorSystem = AnyActorSystem,
    
        TEmitted extends EventObject = EventObject
    
    > {}




### property [actionExecutor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L795 "View definition for actionExecutor")
    
    
    actionExecutor: ActionExecutor;




### property [defer](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L791 "View definition for defer")
    
    
    defer: (fn: () => void) => void;




### property [emit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L792 "View definition for emit")
    
    
    emit: (event: TEmitted) => void;




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L788 "View definition for id")
    
    
    id: string;




### property [logger](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L790 "View definition for logger")
    
    
    logger: (...args: any[]) => void;




### property [self](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L787 "View definition for self")
    
    
    self: ActorRef<TSnapshot, TEvent, TEmitted>;




### property [sessionId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L789 "View definition for sessionId")
    
    
    sessionId: string;




### property [stopChild](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L794 "View definition for stopChild")
    
    
    stopChild: (child: AnyActorRef) => void;




### property [system](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L793 "View definition for system")
    
    
    system: TSystem;




### interface [ActorSystem](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L20 "View definition for ActorSystem")
    
    
    interface ActorSystem<T extends ActorSystemInfo> {}




### property [get](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L21 "View definition for get")
    
    
    get: <K extends keyof T['actors']>(key: K) => T['actors'][K] | undefined;




### property [getAll](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L22 "View definition for getAll")
    
    
    getAll: () => Partial<T['actors']>;




### property [getSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L25 "View definition for getSnapshot")
    
    
    getSnapshot: () => {
    
        _scheduledEvents: Record<string, ScheduledEvent>;
    
    };




### property [inspect](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L23 "View definition for inspect")
    
    
    inspect: (
    
        observer:
    
            | Observer<InspectionEvent>
    
            | ((inspectionEvent: InspectionEvent) => void)
    
    ) => Subscription;




### property [scheduler](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L24 "View definition for scheduler")
    
    
    scheduler: Scheduler;




### property [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts#L28 "View definition for start")
    
    
    start: () => void;




### interface [ActorSystemInfo](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L900 "View definition for ActorSystemInfo")
    
    
    interface ActorSystemInfo {}




### property [actors](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L901 "View definition for actors")
    
    
    actors: Record<string, AnyActorRef>;




### interface [AnyEventObject](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L75 "View definition for AnyEventObject")
    
    
    interface AnyEventObject extends EventObject {}




###  [index signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L76 "View definition for index signature")
    
    
    [key: string]: any;




### interface [AssignAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts#L6 "View definition for AssignAction")
    
    
    interface AssignAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts#L7 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [AssignArgs](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts#L3 "View definition for AssignArgs")
    
    
    interface AssignArgs<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > extends ActionArgs<TContext, TExpressionEvent, TEvent> {}




### property [spawn](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts#L4 "View definition for spawn")
    
    
    spawn: Spawner<TActor>;




### interface [AtomicStateNodeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L397 "View definition for AtomicStateNodeConfig")
    
    
    interface AtomicStateNodeConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends StateNodeConfig<
    
            TContext,
    
            TEvent,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO, // emitted
    
            TODO
    
        > {}




### property [initial](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L399 "View definition for initial")
    
    
    initial?: undefined;




### property [onDone](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L402 "View definition for onDone")
    
    
    onDone?: undefined;




### property [parallel](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L400 "View definition for parallel")
    
    
    parallel?: false | undefined;




### property [states](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L401 "View definition for states")
    
    
    states?: undefined;




### interface [BaseActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L751 "View definition for BaseActorRef")
    
    
    interface BaseActorRef<TEvent extends EventObject> {}




### property [send](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L752 "View definition for send")
    
    
    send: (event: TEvent) => void;




### interface [CancelAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/cancel.d.ts#L3 "View definition for CancelAction")
    
    
    interface CancelAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/cancel.d.ts#L4 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [DelayedTransitionDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L576 "View definition for DelayedTransitionDefinition")
    
    
    interface DelayedTransitionDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends TransitionDefinition<TContext, TEvent> {}




### property [delay](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L577 "View definition for delay")
    
    
    delay: number | string | DelayExpr<TContext, TEvent, undefined, TEvent>;




### interface [DoneActorEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L502 "View definition for DoneActorEvent")
    
    
    interface DoneActorEvent<TOutput = unknown, TId extends string = string>
    
        extends EventObject {}




### property [actorId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L505 "View definition for actorId")
    
    
    actorId: TId;




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L504 "View definition for output")
    
    
    output: TOutput;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L503 "View definition for type")
    
    
    type: `xstate.done.actor.${TId}`;




### interface [DoneStateEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L516 "View definition for DoneStateEvent")
    
    
    interface DoneStateEvent<TOutput = unknown> extends EventObject {}




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L518 "View definition for output")
    
    
    output: TOutput;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L517 "View definition for type")
    
    
    type: `xstate.done.state.${string}`;




### interface [EmitAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/emit.d.ts#L2 "View definition for EmitAction")
    
    
    interface EmitAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TEmitted extends EventObject
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/emit.d.ts#L3 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [EnqueueActionsAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/enqueueActions.d.ts#L21 "View definition for EnqueueActionsAction")
    
    
    interface EnqueueActionsAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/enqueueActions.d.ts#L22 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [ErrorActorEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L507 "View definition for ErrorActorEvent")
    
    
    interface ErrorActorEvent<TErrorData = unknown, TId extends string = string>
    
        extends EventObject {}




### property [actorId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L510 "View definition for actorId")
    
    
    actorId: TId;




### property [error](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L509 "View definition for error")
    
    
    error: TErrorData;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L508 "View definition for type")
    
    
    type: `xstate.error.actor.${TId}`;




### interface [ExecutableActionObject](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L985 "View definition for ExecutableActionObject")
    
    
    interface ExecutableActionObject {}




### property [exec](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L989 "View definition for exec")
    
    
    exec: ((info: ActionArgs<any, any, any>, params: unknown) => void) | undefined;




### property [info](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L987 "View definition for info")
    
    
    info: ActionArgs<MachineContext, EventObject, EventObject>;




### property [params](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L988 "View definition for params")
    
    
    params: NonReducibleUnknown;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L986 "View definition for type")
    
    
    type: string;




### interface [ExecutableSpawnAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L996 "View definition for ExecutableSpawnAction")
    
    
    interface ExecutableSpawnAction extends ExecutableActionObject {}




### property [info](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L998 "View definition for info")
    
    
    info: ActionArgs<MachineContext, EventObject, EventObject>;




### property [params](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L999 "View definition for params")
    
    
    params: {
    
        id: string;
    
        actorRef: AnyActorRef | undefined;
    
        src: string | AnyActorLogic;
    
    };




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L997 "View definition for type")
    
    
    type: 'xstate.spawnChild';




### interface [GuardArgs](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L20 "View definition for GuardArgs")
    
    
    interface GuardArgs<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject
    
    > {}




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L21 "View definition for context")
    
    
    context: TContext;




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L22 "View definition for event")
    
    
    event: TExpressionEvent;




### interface [HistoryStateNode](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L491 "View definition for HistoryStateNode")
    
    
    interface HistoryStateNode<TContext extends MachineContext>
    
        extends StateNode<TContext> {}




### property [history](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L492 "View definition for history")
    
    
    history: 'shallow' | 'deep';




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L493 "View definition for target")
    
    
    target: string | undefined;




### interface [HistoryStateNodeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L404 "View definition for HistoryStateNodeConfig")
    
    
    interface HistoryStateNodeConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends AtomicStateNodeConfig<TContext, TEvent> {}




### property [history](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L405 "View definition for history")
    
    
    history: 'shallow' | 'deep' | true;




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L406 "View definition for target")
    
    
    target: string | undefined;




### interface [InitialTransitionConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L143 "View definition for InitialTransitionConfig")
    
    
    interface InitialTransitionConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string
    
    > extends TransitionConfig<
    
            TContext,
    
            TEvent,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TODO, // TEmitted
    
            TODO
    
        > {}




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L145 "View definition for target")
    
    
    target: string;




### interface [InitialTransitionDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L569 "View definition for InitialTransitionDefinition")
    
    
    interface InitialTransitionDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends TransitionDefinition<TContext, TEvent> {}




### property [guard](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L571 "View definition for guard")
    
    
    guard?: never;




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L570 "View definition for target")
    
    
    target: ReadonlyArray<StateNode<TContext, TEvent>>;




### interface [InspectedActionEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L25 "View definition for InspectedActionEvent")
    
    
    interface InspectedActionEvent extends BaseInspectionEventProperties {}




### property [action](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L27 "View definition for action")
    
    
    action: {
    
        type: string;
    
        params: unknown;
    
    };




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L26 "View definition for type")
    
    
    type: '@xstate.action';




### interface [InspectedActorEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L37 "View definition for InspectedActorEvent")
    
    
    interface InspectedActorEvent extends BaseInspectionEventProperties {}




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L38 "View definition for type")
    
    
    type: '@xstate.actor';




### interface [InspectedEventEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L32 "View definition for InspectedEventEvent")
    
    
    interface InspectedEventEvent extends BaseInspectionEventProperties {}




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L35 "View definition for event")
    
    
    event: AnyEventObject;




### property [sourceRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L34 "View definition for sourceRef")
    
    
    sourceRef: ActorRefLike | undefined;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L33 "View definition for type")
    
    
    type: '@xstate.event';




### interface [InspectedMicrostepEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L19 "View definition for InspectedMicrostepEvent")
    
    
    interface InspectedMicrostepEvent extends BaseInspectionEventProperties {}




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L21 "View definition for event")
    
    
    event: AnyEventObject;




### property [snapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L22 "View definition for snapshot")
    
    
    snapshot: Snapshot<unknown>;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L20 "View definition for type")
    
    
    type: '@xstate.microstep';




### interface [InspectedSnapshotEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L14 "View definition for InspectedSnapshotEvent")
    
    
    interface InspectedSnapshotEvent extends BaseInspectionEventProperties {}




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L16 "View definition for event")
    
    
    event: AnyEventObject;




### property [snapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L17 "View definition for snapshot")
    
    
    snapshot: Snapshot<unknown>;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L15 "View definition for type")
    
    
    type: '@xstate.snapshot';




### interface [InteropObservable](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L739 "View definition for InteropObservable")
    
    
    interface InteropObservable<T> {}




### property [[Symbol.observable]](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L740 "View definition for \[Symbol.observable\]")
    
    
    [Symbol.observable]: () => InteropSubscribable<T>;




### interface [InteropSubscribable](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L742 "View definition for InteropSubscribable")
    
    
    interface InteropSubscribable<T> {}




### method [subscribe](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L743 "View definition for subscribe")
    
    
    subscribe: (observer: Observer<T>) => Subscription;




### interface [InvokeDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L156 "View definition for InvokeDefinition")
    
    
    interface InvokeDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > {}




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L157 "View definition for id")
    
    
    id: string;




### property [input](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L161 "View definition for input")
    
    
    input?:
    
        | Mapper<TContext, TEvent, NonReducibleUnknown, TEvent>
    
        | NonReducibleUnknown;




### property [onDone](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L166 "View definition for onDone")
    
    
    onDone?:
    
        | string
    
        | SingleOrArray<
    
              TransitionConfig<
    
                  TContext,
    
                  DoneActorEvent<unknown>,
    
                  TEvent,
    
                  TActor,
    
                  TAction,
    
                  TGuard,
    
                  TDelay,
    
                  TEmitted,
    
                  TMeta
    
              >
    
          >;

  * The transition to take upon the invoked child machine reaching its final top-level state.




### property [onError](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L171 "View definition for onError")
    
    
    onError?:
    
        | string
    
        | SingleOrArray<
    
              TransitionConfig<
    
                  TContext,
    
                  ErrorActorEvent,
    
                  TEvent,
    
                  TActor,
    
                  TAction,
    
                  TGuard,
    
                  TDelay,
    
                  TEmitted,
    
                  TMeta
    
              >
    
          >;

  * The transition to take upon the invoked child machine sending an error event.




### property [onSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L172 "View definition for onSnapshot")
    
    
    onSnapshot?:
    
        | string
    
        | SingleOrArray<
    
              TransitionConfig<
    
                  TContext,
    
                  SnapshotEvent,
    
                  TEvent,
    
                  TActor,
    
                  TAction,
    
                  TGuard,
    
                  TDelay,
    
                  TEmitted,
    
                  TMeta
    
              >
    
          >;




### property [src](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L160 "View definition for src")
    
    
    src: AnyActorLogic | string;

  * The source of the actor logic to be invoked




### property [systemId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L158 "View definition for systemId")
    
    
    systemId: string | undefined;




### property [toJSON](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L173 "View definition for toJSON")
    
    
    toJSON: () => Omit<
    
        InvokeDefinition<
    
            TContext,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted,
    
            TMeta
    
        >,
    
        'onDone' | 'onError' | 'toJSON'
    
    >;




### interface [LogAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/log.d.ts#L3 "View definition for LogAction")
    
    
    interface LogAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/log.d.ts#L4 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [MachineImplementationsSimplified](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L423 "View definition for MachineImplementationsSimplified")
    
    
    interface MachineImplementationsSimplified<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor = ProvidedActor,
    
        TAction extends ParameterizedObject = ParameterizedObject,
    
        TGuard extends ParameterizedObject = ParameterizedObject
    
    > {}

  * 


### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L425 "View definition for actions")
    
    
    actions: ActionFunctionMap<TContext, TEvent, TActor, TAction>;




### property [actors](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L426 "View definition for actors")
    
    
    actors: Record<
    
        string,
    
        | AnyActorLogic
    
        | {
    
              src: AnyActorLogic;
    
              input: Mapper<TContext, TEvent, unknown, TEvent> | NonReducibleUnknown;
    
          }
    
    >;




### property [delays](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L430 "View definition for delays")
    
    
    delays: DelayFunctionMap<TContext, TEvent, TAction>;




### property [guards](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L424 "View definition for guards")
    
    
    guards: GuardMap<TContext, TEvent, TGuard>;




### interface [MachineTypes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L484 "View definition for MachineTypes")
    
    
    interface MachineTypes<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TTag extends string,
    
        TInput,
    
        TOutput,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > extends SetupTypes<
    
            TContext,
    
            TEvent,
    
            never,
    
            TTag,
    
            TInput,
    
            TOutput,
    
            TEmitted,
    
            TMeta
    
        > {}




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L486 "View definition for actions")
    
    
    actions?: TAction;




### property [actors](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L485 "View definition for actors")
    
    
    actors?: TActor;




### property [delays](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L488 "View definition for delays")
    
    
    delays?: TDelay;




### property [guards](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L487 "View definition for guards")
    
    
    guards?: TGuard;




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L489 "View definition for meta")
    
    
    meta?: TMeta;




### interface [ParameterizedObject](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L78 "View definition for ParameterizedObject")
    
    
    interface ParameterizedObject {}




### property [params](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L80 "View definition for params")
    
    
    params?: NonReducibleUnknown;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L79 "View definition for type")
    
    
    type: string;




### interface [ProvidedActor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L469 "View definition for ProvidedActor")
    
    
    interface ProvidedActor {}




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L472 "View definition for id")
    
    
    id?: string | undefined;




### property [logic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L471 "View definition for logic")
    
    
    logic: UnknownActorLogic;




### property [src](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L470 "View definition for src")
    
    
    src: string;




### interface [RaiseAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/raise.d.ts#L2 "View definition for RaiseAction")
    
    
    interface RaiseAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/raise.d.ts#L3 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [RaiseActionOptions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L529 "View definition for RaiseActionOptions")
    
    
    interface RaiseActionOptions<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > {}




### property [delay](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L531 "View definition for delay")
    
    
    delay?: Delay<TDelay> | DelayExpr<TContext, TExpressionEvent, TParams, TEvent>;




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L530 "View definition for id")
    
    
    id?: string;




### interface [RaiseActionParams](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L533 "View definition for RaiseActionParams")
    
    
    interface RaiseActionParams<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > extends RaiseActionOptions<TContext, TExpressionEvent, TParams, TEvent, TDelay> {}




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L534 "View definition for event")
    
    
    event: TEvent | SendExpr<TContext, TExpressionEvent, TParams, TEvent, TEvent>;




### interface [ResolvedStateMachineTypes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L954 "View definition for ResolvedStateMachineTypes")
    
    
    interface ResolvedStateMachineTypes<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TTag extends string,
    
        TEmitted extends EventObject = EventObject
    
    > {}

  * #### Deprecated




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L958 "View definition for actions")
    
    
    actions: TAction;




### property [actors](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L957 "View definition for actors")
    
    
    actors: TActor;




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L955 "View definition for context")
    
    
    context: TContext;




### property [delays](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L960 "View definition for delays")
    
    
    delays: TDelay;




### property [emitted](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L962 "View definition for emitted")
    
    
    emitted: TEmitted;




### property [events](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L956 "View definition for events")
    
    
    events: TEvent;




### property [guards](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L959 "View definition for guards")
    
    
    guards: TGuard;




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L961 "View definition for tags")
    
    
    tags: TTag;




### interface [RouteTransitionConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L346 "View definition for RouteTransitionConfig")
    
    
    interface RouteTransitionConfig<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject
    
    > {}




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L348 "View definition for actions")
    
    
    actions?: Actions<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        undefined,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;




### property [description](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L350 "View definition for description")
    
    
    description?: string;




### property [guard](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L347 "View definition for guard")
    
    
    guard?: Guard<TContext, TExpressionEvent, undefined, TGuard>;




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L349 "View definition for meta")
    
    
    meta?: Record<string, any>;




### interface [SendToAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts#L2 "View definition for SendToAction")
    
    
    interface SendToAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts#L3 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [SendToActionOptions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L527 "View definition for SendToActionOptions")
    
    
    interface SendToActionOptions<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > extends RaiseActionOptions<TContext, TExpressionEvent, TParams, TEvent, TDelay> {}




### interface [SendToActionParams](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L536 "View definition for SendToActionParams")
    
    
    interface SendToActionParams<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TSentEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TDelay extends string
    
    > extends SendToActionOptions<TContext, TExpressionEvent, TParams, TEvent, TDelay> {}




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L537 "View definition for event")
    
    
    event:
    
        | TSentEvent
    
        | SendExpr<TContext, TExpressionEvent, TParams, TSentEvent, TEvent>;




### interface [SetupTypes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L474 "View definition for SetupTypes")
    
    
    interface SetupTypes<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TChildrenMap extends Record<string, string>,
    
        TTag extends string,
    
        TInput,
    
        TOutput,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > {}




### property [children](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L477 "View definition for children")
    
    
    children?: TChildrenMap;




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L475 "View definition for context")
    
    
    context?: TContext;




### property [emitted](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L481 "View definition for emitted")
    
    
    emitted?: TEmitted;




### property [events](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L476 "View definition for events")
    
    
    events?: TEvent;




### property [input](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L479 "View definition for input")
    
    
    input?: TInput;




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L482 "View definition for meta")
    
    
    meta?: TMeta;




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L480 "View definition for output")
    
    
    output?: TOutput;




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L478 "View definition for tags")
    
    
    tags?: TTag;




### interface [SimulatedClock](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L2 "View definition for SimulatedClock")
    
    
    interface SimulatedClock extends Clock {}




### method [increment](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L4 "View definition for increment")
    
    
    increment: (ms: number) => void;




### method [set](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L5 "View definition for set")
    
    
    set: (ms: number) => void;




### method [start](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts#L3 "View definition for start")
    
    
    start: (speed: number) => void;




### interface [SnapshotEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L512 "View definition for SnapshotEvent")
    
    
    interface SnapshotEvent<TSnapshot extends Snapshot<unknown> = Snapshot<unknown>>
    
        extends EventObject {}




### property [snapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L514 "View definition for snapshot")
    
    
    snapshot: TSnapshot;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L513 "View definition for type")
    
    
    type: `xstate.snapshot.${string}`;




### interface [SpawnAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L3 "View definition for SpawnAction")
    
    
    interface SpawnAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L4 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [SpawnActionOptions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L7 "View definition for SpawnActionOptions")
    
    
    interface SpawnActionOptions<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > {}




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L8 "View definition for id")
    
    
    id?: ResolvableActorId<TContext, TExpressionEvent, TEvent, TActor['id']>;




### property [input](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L10 "View definition for input")
    
    
    input?:
    
        | Mapper<TContext, TEvent, InputFrom<TActor['logic']>, TEvent>
    
        | InputFrom<TActor['logic']>;




### property [syncSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L11 "View definition for syncSnapshot")
    
    
    syncSnapshot?: boolean;




### property [systemId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts#L9 "View definition for systemId")
    
    
    systemId?: string;




### interface [StateConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L584 "View definition for StateConfig")
    
    
    interface StateConfig<TContext extends MachineContext, TEvent extends EventObject> {}




### property [children](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L587 "View definition for children")
    
    
    children: Record<string, AnyActorRef>;




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L585 "View definition for context")
    
    
    context: TContext;




### property [error](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L590 "View definition for error")
    
    
    error?: unknown;




### property [historyValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L586 "View definition for historyValue")
    
    
    historyValue?: HistoryValue<TContext, TEvent>;




### property [machine](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L591 "View definition for machine")
    
    
    machine?: StateMachine<
    
        TContext,
    
        TEvent,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any, // TMeta
    
        any
    
    >;




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L589 "View definition for output")
    
    
    output?: any;




### property [status](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L588 "View definition for status")
    
    
    status: SnapshotStatus;




### interface [StateLike](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L579 "View definition for StateLike")
    
    
    interface StateLike<TContext extends MachineContext> {}




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L581 "View definition for context")
    
    
    context: TContext;




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L582 "View definition for event")
    
    
    event: EventObject;




### property [value](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L580 "View definition for value")
    
    
    value: StateValue;




### interface [StateMachineDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L375 "View definition for StateMachineDefinition")
    
    
    interface StateMachineDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends StateNodeDefinition<TContext, TEvent> {}




### interface [StateMachineTypes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L943 "View definition for StateMachineTypes")
    
    
    interface StateMachineTypes {}




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L947 "View definition for actions")
    
    
    actions: ParameterizedObject;




### property [actors](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L946 "View definition for actors")
    
    
    actors: ProvidedActor;




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L944 "View definition for context")
    
    
    context: MachineContext;




### property [delays](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L949 "View definition for delays")
    
    
    delays: string;




### property [emitted](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L951 "View definition for emitted")
    
    
    emitted: EventObject;




### property [events](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L945 "View definition for events")
    
    
    events: EventObject;




### property [guards](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L948 "View definition for guards")
    
    
    guards: ParameterizedObject;




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L950 "View definition for tags")
    
    
    tags: string;




### interface [StateNodeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L258 "View definition for StateNodeConfig")
    
    
    interface StateNodeConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TTag extends string,
    
        _TOutput,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > {}




### property [after](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L305 "View definition for after")
    
    
    after?: DelayedTransitions<TContext, TEvent, TActor, TAction, TGuard, TDelay>;

  * The mapping (or array) of delays (in milliseconds) to their potential transition(s). The delayed transitions are taken after the specified delay in an interpreter.




### property [always](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L310 "View definition for always")
    
    
    always?: TransitionConfigOrTarget<
    
        TContext,
    
        TEvent,
    
        TEvent,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted,
    
        TMeta
    
    >;

  * An eventless transition that is always taken when this state node is active.




### property [description](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L341 "View definition for description")
    
    
    description?: string;

  * A text description of the state node




### property [entry](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L289 "View definition for entry")
    
    
    entry?: Actions<
    
        TContext,
    
        TEvent,
    
        TEvent,
    
        undefined,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;

  * The action(s) to be executed upon entering the state node.




### property [exit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L291 "View definition for exit")
    
    
    exit?: Actions<
    
        TContext,
    
        TEvent,
    
        TEvent,
    
        undefined,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;

  * The action(s) to be executed upon exiting the state node.




### property [history](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L275 "View definition for history")
    
    
    history?: 'shallow' | 'deep' | boolean | undefined;

  * Indicates whether the state node is a history state node, and what type of history: shallow, deep, true (shallow), false (none), undefined (none)




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L329 "View definition for id")
    
    
    id?: string | undefined;

  * The unique ID of the state node, which can be referenced as a transition target via the `#id` syntax.




### property [initial](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L260 "View definition for initial")
    
    
    initial?:
    
        | InitialTransitionConfig<TContext, TEvent, TActor, TAction, TGuard, TDelay>
    
        | string
    
        | undefined;

  * The initial state transition.




### property [invoke](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L285 "View definition for invoke")
    
    
    invoke?: SingleOrArray<
    
        InvokeConfig<
    
            TContext,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted,
    
            TMeta
    
        >
    
    >;

  * The services to invoke upon entering this state node. These services will be stopped upon exiting this state node.




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L316 "View definition for meta")
    
    
    meta?: TMeta;

  * The meta data associated with this state node, which will be returned in State instances.




### property [on](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L287 "View definition for on")
    
    
    on?: TransitionsConfig<
    
        TContext,
    
        TEvent,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted,
    
        TMeta
    
    >;

  * The mapping of event types to their potential transition(s).




### property [onDone](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L299 "View definition for onDone")
    
    
    onDone?:
    
        | string
    
        | SingleOrArray<
    
              TransitionConfig<
    
                  TContext,
    
                  DoneStateEvent,
    
                  TEvent,
    
                  TActor,
    
                  TAction,
    
                  TGuard,
    
                  TDelay,
    
                  TEmitted,
    
                  TMeta
    
              >
    
          >
    
        | undefined;

  * The potential transition(s) to be taken upon reaching a final child state node.

This is equivalent to defining a `[done(id)]` transition on this state node's `on` property.




### property [order](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L334 "View definition for order")
    
    
    order?: number;

  * The order this state node appears. Corresponds to the implicit document order.




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L324 "View definition for output")
    
    
    output?: Mapper<TContext, TEvent, unknown, TEvent> | NonReducibleUnknown;

  * The output data sent with the "xstate.done.state._id_" event if this is a final state node.

The output data will be evaluated with the current `context` and placed on the `.data` property of the event.




### property [parent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L311 "View definition for parent")
    
    
    parent?: StateNode<TContext, TEvent>;




### property [route](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L344 "View definition for route")
    
    
    route?: RouteTransitionConfig<
    
        TContext,
    
        TEvent,
    
        TEvent,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;




### property [states](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L280 "View definition for states")
    
    
    states?:
    
        | StatesConfig<
    
              TContext,
    
              TEvent,
    
              TActor,
    
              TAction,
    
              TGuard,
    
              TDelay,
    
              TTag,
    
              NonReducibleUnknown,
    
              TEmitted,
    
              TMeta
    
          >
    
        | undefined;

  * The mapping of state node keys to their state node configurations (recursive).




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L339 "View definition for tags")
    
    
    tags?: SingleOrArray<TTag>;

  * The tags for this state node, which are accumulated into the `state.tags` property.




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L343 "View definition for target")
    
    
    target?: string | undefined;

  * A default target for a history state




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L270 "View definition for type")
    
    
    type?: 'atomic' | 'compound' | 'parallel' | 'final' | 'history';

  * The type of this state node:

\- `'atomic'` \- no child state nodes - `'compound'` \- nested child state nodes (XOR) - `'parallel'` \- orthogonal nested child state nodes (AND) - `'history'` \- history state node - `'final'` \- final state node




### interface [StateNodeDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L354 "View definition for StateNodeDefinition")
    
    
    interface StateNodeDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > {}




### property [description](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L372 "View definition for description")
    
    
    description?: string;




### property [entry](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L364 "View definition for entry")
    
    
    entry: UnknownAction[];




### property [exit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L365 "View definition for exit")
    
    
    exit: UnknownAction[];




### property [history](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L360 "View definition for history")
    
    
    history: boolean | 'shallow' | 'deep' | undefined;




### property [id](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L355 "View definition for id")
    
    
    id: string;




### property [initial](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L359 "View definition for initial")
    
    
    initial: InitialTransitionDefinition<TContext, TEvent> | undefined;




### property [invoke](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L370 "View definition for invoke")
    
    
    invoke: Array<
    
        InvokeDefinition<
    
            TContext,
    
            TEvent,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO,
    
            TODO, // TEmitted
    
            TODO
    
        >
    
    >;




### property [key](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L357 "View definition for key")
    
    
    key: string;




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L366 "View definition for meta")
    
    
    meta: any;




### property [on](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L362 "View definition for on")
    
    
    on: TransitionDefinitionMap<TContext, TEvent>;




### property [order](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L367 "View definition for order")
    
    
    order: number;




### property [output](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L368 "View definition for output")
    
    
    output?: StateNodeConfig<
    
        TContext,
    
        TEvent,
    
        ProvidedActor,
    
        ParameterizedObject,
    
        ParameterizedObject,
    
        string,
    
        string,
    
        unknown,
    
        EventObject, // TEmitted
    
        any
    
    >['output'];




### property [states](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L361 "View definition for states")
    
    
    states: StatesDefinition<TContext, TEvent>;




### property [tags](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L373 "View definition for tags")
    
    
    tags: string[];




### property [transitions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L363 "View definition for transitions")
    
    
    transitions: Array<TransitionDefinition<TContext, TEvent>>;




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L358 "View definition for type")
    
    
    type: 'atomic' | 'compound' | 'parallel' | 'final' | 'history';




### property [version](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L356 "View definition for version")
    
    
    version?: string | undefined;




### interface [StateValueMap](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L121 "View definition for StateValueMap")
    
    
    interface StateValueMap {}




###  [index signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L122 "View definition for index signature")
    
    
    [key: string]: StateValue | undefined;




### interface [StopAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/stopChild.d.ts#L3 "View definition for StopAction")
    
    
    interface StopAction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > {}




###  [call signature](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/stopChild.d.ts#L4 "View definition for call signature")
    
    
    (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;




### interface [Subscribable](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L745 "View definition for Subscribable")
    
    
    interface Subscribable<T> extends InteropSubscribable<T> {}




### method [subscribe](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L746 "View definition for subscribe")
    
    
    subscribe: {
    
        (observer: Observer<T>): Subscription;
    
        (
    
            next: (value: T) => void,
    
            error?: (error: any) => void,
    
            complete?: () => void
    
        ): Subscription;
    
    };




### interface [Subscription](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L736 "View definition for Subscription")
    
    
    interface Subscription {}




### method [unsubscribe](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L737 "View definition for unsubscribe")
    
    
    unsubscribe: () => void;




### interface [ToExecutableAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L991 "View definition for ToExecutableAction")
    
    
    interface ToExecutableAction<T extends ParameterizedObject>
    
        extends ExecutableActionObject {}




### property [exec](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L994 "View definition for exec")
    
    
    exec: undefined;




### property [params](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L993 "View definition for params")
    
    
    params: T['params'];




### property [type](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L992 "View definition for type")
    
    
    type: T['type'];




### interface [TransitionConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L135 "View definition for TransitionConfig")
    
    
    interface TransitionConfig<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject = EventObject,
    
        TMeta extends MetaObject = MetaObject
    
    > {}




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L137 "View definition for actions")
    
    
    actions?: Actions<
    
        TContext,
    
        TExpressionEvent,
    
        TEvent,
    
        undefined,
    
        TActor,
    
        TAction,
    
        TGuard,
    
        TDelay,
    
        TEmitted
    
    >;




### property [description](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L141 "View definition for description")
    
    
    description?: string;




### property [guard](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L136 "View definition for guard")
    
    
    guard?: Guard<TContext, TExpressionEvent, undefined, TGuard>;




### property [meta](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L140 "View definition for meta")
    
    
    meta?: TMeta;




### property [reenter](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L138 "View definition for reenter")
    
    
    reenter?: boolean;




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L139 "View definition for target")
    
    
    target?: TransitionTarget | undefined;




### interface [TransitionDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L551 "View definition for TransitionDefinition")
    
    
    interface TransitionDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > extends Omit<
    
            TransitionConfig<
    
                TContext,
    
                TEvent,
    
                TEvent,
    
                TODO,
    
                TODO,
    
                TODO,
    
                TODO,
    
                TODO, // TEmitted
    
                TODO
    
            >,
    
            'target' | 'guard'
    
        > {}




### property [actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L555 "View definition for actions")
    
    
    actions: readonly UnknownAction[];




### property [eventType](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L558 "View definition for eventType")
    
    
    eventType: EventDescriptor<TEvent>;




### property [guard](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L557 "View definition for guard")
    
    
    guard?: UnknownGuard;




### property [reenter](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L556 "View definition for reenter")
    
    
    reenter: boolean;




### property [source](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L554 "View definition for source")
    
    
    source: StateNode<TContext, TEvent>;




### property [target](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L553 "View definition for target")
    
    
    target: ReadonlyArray<StateNode<TContext, TEvent>> | undefined;




### property [toJSON](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L559 "View definition for toJSON")
    
    
    toJSON: () => {
    
        target: string[] | undefined;
    
        source: string;
    
        actions: readonly UnknownAction[];
    
        guard?: UnknownGuard;
    
        eventType: EventDescriptor<TEvent>;
    
        meta?: Record<string, any>;
    
    };




### interface [UnifiedArg](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L82 "View definition for UnifiedArg")
    
    
    interface UnifiedArg<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject
    
    > {}




### property [context](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L83 "View definition for context")
    
    
    context: TContext;




### property [event](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L84 "View definition for event")
    
    
    event: TExpressionEvent;




### property [self](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L85 "View definition for self")
    
    
    self: ActorRef<
    
        MachineSnapshot<
    
            TContext,
    
            TEvent,
    
            Record<string, AnyActorRef | undefined>, // TODO: this should be replaced with `TChildren`
    
            StateValue,
    
            string,
    
            unknown,
    
            TODO, // TMeta
    
            TODO
    
        >,
    
        TEvent,
    
        AnyEventObject
    
    >;




### property [system](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L88 "View definition for system")
    
    
    system: AnyActorSystem;




## Enums

### enum [SpecialTargets](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L523 "View definition for SpecialTargets")
    
    
    enum SpecialTargets {
    
        Parent = '#_parent',
    
        Internal = '#_internal',
    
    }




### member [Internal](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L525 "View definition for Internal")
    
    
    Internal = '#_internal'




### member [Parent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L524 "View definition for Parent")
    
    
    Parent = '#_parent'




## Type Aliases

### type [Action](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L117 "View definition for Action")
    
    
    type Action<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject
    
    > =
    
        | NoRequiredParams<TAction>
    
        | WithDynamicParams<TContext, TExpressionEvent, TAction>
    
        | ActionFunction<
    
              TContext,
    
              TExpressionEvent,
    
              TEvent,
    
              TParams,
    
              TActor,
    
              TAction,
    
              TGuard,
    
              TDelay,
    
              TEmitted
    
          >;




### type [ActionExecutor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L1007 "View definition for ActionExecutor")
    
    
    type ActionExecutor = (actionToExecute: ExecutableActionObject) => void;




### type [ActionFunction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L99 "View definition for ActionFunction")
    
    
    type ActionFunction<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject
    
    > = {
    
        (args: ActionArgs<TContext, TExpressionEvent, TEvent>, params: TParams): void;
    
        _out_TEvent?: TEvent;
    
        _out_TActor?: TActor;
    
        _out_TAction?: TAction;
    
        _out_TGuard?: TGuard;
    
        _out_TDelay?: TDelay;
    
        _out_TEmitted?: TEmitted;
    
    };




### type [ActionFunctionMap](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L410 "View definition for ActionFunctionMap")
    
    
    type ActionFunctionMap<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject = ParameterizedObject,
    
        TGuard extends ParameterizedObject = ParameterizedObject,
    
        TDelay extends string = string,
    
        TEmitted extends EventObject = EventObject
    
    > = {
    
        [K in TAction['type']]?: ActionFunction<
    
            TContext,
    
            TEvent,
    
            TEvent,
    
            GetParameterizedParams<
    
                TAction extends {
    
                    type: K;
    
                }
    
                    ? TAction
    
                    : never
    
            >,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted
    
        >;
    
    };




### type [Actions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L119 "View definition for Actions")
    
    
    type Actions<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject
    
    > = SingleOrArray<
    
        Action<
    
            TContext,
    
            TExpressionEvent,
    
            TEvent,
    
            TParams,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted
    
        >
    
    >;




### type [ActorLogicFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L778 "View definition for ActorLogicFrom")
    
    
    type ActorLogicFrom<T> = ReturnTypeOrValue<T> extends infer R
    
        ? R extends StateMachine<
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any,
    
              any, // TMeta
    
              any
    
          >
    
            ? R
    
            : R extends Promise<infer U>
    
            ? PromiseActorLogic<U>
    
            : never
    
        : never;




### type [ActorRefFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L780 "View definition for ActorRefFrom")
    
    
    type ActorRefFrom<T> = ReturnTypeOrValue<T> extends infer R
    
        ? R extends StateMachine<
    
              infer TContext,
    
              infer TEvent,
    
              infer TChildren,
    
              infer _TActor,
    
              infer _TAction,
    
              infer _TGuard,
    
              infer _TDelay,
    
              infer TStateValue,
    
              infer TTag,
    
              infer _TInput,
    
              infer TOutput,
    
              infer TEmitted,
    
              infer TMeta,
    
              infer TStateSchema
    
          >
    
            ? ActorRef<
    
                  MachineSnapshot<
    
                      TContext,
    
                      TEvent,
    
                      TChildren,
    
                      TStateValue,
    
                      TTag,
    
                      TOutput,
    
                      TMeta,
    
                      TStateSchema
    
                  >,
    
                  TEvent,
    
                  TEmitted
    
              >
    
            : R extends Promise<infer U>
    
            ? ActorRefFrom<PromiseActorLogic<U>>
    
            : R extends ActorLogic<
    
                  infer TSnapshot,
    
                  infer TEvent,
    
                  infer _TInput,
    
                  infer _TSystem,
    
                  infer TEmitted
    
              >
    
            ? ActorRef<TSnapshot, TEvent, TEmitted>
    
            : never
    
        : never;




### type [ActorRefFromLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L781 "View definition for ActorRefFromLogic")
    
    
    type ActorRefFromLogic<T extends AnyActorLogic> = ActorRef<
    
        SnapshotFrom<T>,
    
        EventFromLogic<T>,
    
        EmittedFrom<T>
    
    >;




### type [ActorRefLike](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L776 "View definition for ActorRefLike")
    
    
    type ActorRefLike = Pick<AnyActorRef, 'sessionId' | 'send' | 'getSnapshot'>;




### type [AnyActor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L728 "View definition for AnyActor")
    
    
    type AnyActor = Actor<any>;




### type [AnyActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L875 "View definition for AnyActorLogic")
    
    
    type AnyActorLogic = ActorLogic<
    
        any, // snapshot
    
        any, // event
    
        any, // input
    
        any, // system
    
        any
    
    >;




### type [AnyActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L774 "View definition for AnyActorRef")
    
    
    type AnyActorRef = ActorRef<
    
        any,
    
        any, // TODO: shouldn't this be AnyEventObject?
    
        any
    
    >;




### type [AnyActorScope](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L797 "View definition for AnyActorScope")
    
    
    type AnyActorScope = ActorScope<
    
        any, // TSnapshot
    
        any, // TEvent
    
        AnyActorSystem,
    
        any
    
    >;




### type [AnyFunction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L43 "View definition for AnyFunction")
    
    
    type AnyFunction = (...args: any[]) => any;




### type [AnyHistoryValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L499 "View definition for AnyHistoryValue")
    
    
    type AnyHistoryValue = HistoryValue<any, any>;




### type [AnyInterpreter](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L730 "View definition for AnyInterpreter")
    
    
    type AnyInterpreter = AnyActor;

  * #### Deprecated

Use `AnyActor` instead.




### type [AnyInvokeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L257 "View definition for AnyInvokeConfig")
    
    
    type AnyInvokeConfig = InvokeConfig<any, any, any, any, any, any, any, any>;




### type [AnyMachineSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L379 "View definition for AnyMachineSnapshot")
    
    
    type AnyMachineSnapshot = MachineSnapshot<any, any, any, any, any, any, any, any>;




### type [AnyState](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L381 "View definition for AnyState")
    
    
    type AnyState = AnyMachineSnapshot;

  * #### Deprecated

Use `AnyMachineSnapshot` instead




### type [AnyStateConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L396 "View definition for AnyStateConfig")
    
    
    type AnyStateConfig = StateConfig<any, AnyEventObject>;




### type [AnyStateMachine](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L382 "View definition for AnyStateMachine")
    
    
    type AnyStateMachine = StateMachine<
    
        any, // context
    
        any, // event
    
        any, // children
    
        any, // actor
    
        any, // action
    
        any, // guard
    
        any, // delay
    
        any, // state value
    
        any, // tag
    
        any, // input
    
        any, // output
    
        any, // emitted
    
        any, // TMeta
    
        any
    
    >;




### type [AnyStateNode](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L377 "View definition for AnyStateNode")
    
    
    type AnyStateNode = StateNode<any, any>;




### type [AnyStateNodeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L352 "View definition for AnyStateNodeConfig")
    
    
    type AnyStateNodeConfig = StateNodeConfig<
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any,
    
        any, // emitted
    
        any
    
    >;




### type [AnyStateNodeDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L378 "View definition for AnyStateNodeDefinition")
    
    
    type AnyStateNodeDefinition = StateNodeDefinition<any, any>;




### type [AnyTransitionConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L147 "View definition for AnyTransitionConfig")
    
    
    type AnyTransitionConfig = TransitionConfig<
    
        any, // TContext
    
        any, // TExpressionEvent
    
        any, // TEvent
    
        any, // TActor
    
        any, // TAction
    
        any, // TGuard
    
        any, // TDelay
    
        any, // TEmitted
    
        any
    
    >;




### type [AnyTransitionDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L568 "View definition for AnyTransitionDefinition")
    
    
    type AnyTransitionDefinition = TransitionDefinition<any, any>;




### type [Assigner](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L539 "View definition for Assigner")
    
    
    type Assigner<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > = (
    
        args: AssignArgs<TContext, TExpressionEvent, TEvent, TActor>,
    
        params: TParams
    
    ) => Partial<TContext>;




### type [BuiltinActionResolution](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L1008 "View definition for BuiltinActionResolution")
    
    
    type BuiltinActionResolution = [
    
        AnyMachineSnapshot,
    
        NonReducibleUnknown,
    
        // params
    
        UnknownAction[] | undefined
    
    ];




### type [CallbackActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts#L6 "View definition for CallbackActorLogic")
    
    
    type CallbackActorLogic<
    
        TEvent extends EventObject,
    
        TInput = NonReducibleUnknown,
    
        TEmitted extends EventObject = EventObject
    
    > = ActorLogic<CallbackSnapshot<TInput>, TEvent, TInput, AnyActorSystem, TEmitted>;




### type [CallbackActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts#L41 "View definition for CallbackActorRef")
    
    
    type CallbackActorRef<
    
        TEvent extends EventObject,
    
        TInput = NonReducibleUnknown
    
    > = ActorRefFromLogic<CallbackActorLogic<TEvent, TInput>>;

  * Represents an actor created by `fromCallback`.

The type of `self` within the actor's logic.

#### Example 1
        
        import { fromCallback, createActor } from 'xstate';
        
        
        
        
        // The events the actor receives.
        
        type Event = { type: 'someEvent' };
        
        // The actor's input.
        
        type Input = { name: string };
        
        
        
        
        // Actor logic that logs whenever it receives an event of type `someEvent`.
        
        const logic = fromCallback<Event, Input>(({ self, input, receive }) => {
        
          self;
        
          // ^? CallbackActorRef<Event, Input>
        
        
        
        
          receive((event) => {
        
            if (event.type === 'someEvent') {
        
              console.log(`${input.name}: received "someEvent" event`);
        
              // logs 'myActor: received "someEvent" event'
        
            }
        
          });
        
        });
        
        
        
        
        const actor = createActor(logic, { input: { name: 'myActor' } });
        
        //    ^? CallbackActorRef<Event, Input>

#### See Also

    * fromCallback




### type [CallbackLogicFunction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts#L45 "View definition for CallbackLogicFunction")
    
    
    type CallbackLogicFunction<
    
        TEvent extends EventObject = AnyEventObject,
    
        TSentEvent extends EventObject = AnyEventObject,
    
        TInput = NonReducibleUnknown,
    
        TEmitted extends EventObject = EventObject
    
    > = ({
    
        input,
    
        system,
    
        self,
    
        sendBack,
    
        receive,
    
        emit,
    
    }: {
    
        /**
    
         * Data that was provided to the callback actor
    
         *
    
         * @see {@link https://stately.ai/docs/input | Input docs}
    
         */
    
        input: TInput;
    
        /** The actor system to which the callback actor belongs */
    
        system: AnyActorSystem;
    
        /** The parent actor of the callback actor */
    
        self: CallbackActorRef<TEvent>;
    
        /** A function that can send events back to the parent actor */
    
        sendBack: (event: TSentEvent) => void;
    
        /**
    
         * A function that can be called with a listener function argument; the
    
         * listener is then called whenever events are received by the callback actor
    
         */
    
        receive: Receiver<TEvent>;
    
        emit: (emitted: TEmitted) => void;
    
    }) => (() => void) | void;




### type [CallbackSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts#L3 "View definition for CallbackSnapshot")
    
    
    type CallbackSnapshot<TInput> = Snapshot<undefined> & {
    
        input: TInput;
    
    };




### type [Cast](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L62 "View definition for Cast")
    
    
    type Cast<A, B> = A extends B ? A : B;




### type [Compute](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L47 "View definition for Compute")
    
    
    type Compute<A> = {
    
        [K in keyof A]: A[K];
    
    } & unknown;




### type [ConditionalRequired](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L109 "View definition for ConditionalRequired")
    
    
    type ConditionalRequired<T, Condition extends boolean> = Condition extends true
    
        ? Required<T>
    
        : T;




### type [ContextFactory](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L451 "View definition for ContextFactory")
    
    
    type ContextFactory<
    
        TContext extends MachineContext,
    
        TActor extends ProvidedActor,
    
        TInput,
    
        TEvent extends EventObject = EventObject
    
    > = ({
    
        spawn,
    
        input,
    
        self,
    
    }: {
    
        spawn: Spawner<TActor>;
    
        input: TInput;
    
        self: ActorRef<
    
            MachineSnapshot<
    
                TContext,
    
                TEvent,
    
                Record<string, AnyActorRef | undefined>, // TODO: this should be replaced with `TChildren`
    
                StateValue,
    
                string,
    
                unknown,
    
                TODO, // TMeta
    
                TODO
    
            >,
    
            TEvent,
    
            AnyEventObject
    
        >;
    
    }) => TContext;




### type [ContextFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L889 "View definition for ContextFrom")
    
    
    type ContextFrom<T> = ReturnTypeOrValue<T> extends infer R
    
        ? R extends StateMachine<
    
              infer TContext,
    
              infer _TEvent,
    
              infer _TChildren,
    
              infer _TActor,
    
              infer _TAction,
    
              infer _TGuard,
    
              infer _TDelay,
    
              infer _TStateValue,
    
              infer _TTag,
    
              infer _TInput,
    
              infer _TOutput,
    
              infer _TEmitted,
    
              infer _TMeta,
    
              infer _TStateSchema
    
          >
    
            ? TContext
    
            : R extends MachineSnapshot<
    
                  infer TContext,
    
                  infer _TEvent,
    
                  infer _TChildren,
    
                  infer _TStateValue,
    
                  infer _TTag,
    
                  infer _TOutput,
    
                  infer _TMeta,
    
                  infer _TStateSchema
    
              >
    
            ? TContext
    
            : R extends Actor<infer TActorLogic>
    
            ? TActorLogic extends StateMachine<
    
                  infer TContext,
    
                  infer _TEvent,
    
                  infer _TChildren,
    
                  infer _TActor,
    
                  infer _TAction,
    
                  infer _TGuard,
    
                  infer _TDelay,
    
                  infer _TStateValue,
    
                  infer _TTag,
    
                  infer _TInput,
    
                  infer _TOutput,
    
                  infer _TEmitted,
    
                  infer _TMeta,
    
                  infer _TStateSchema
    
              >
    
                ? TContext
    
                : never
    
            : never
    
        : never;




### type [DelayConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L421 "View definition for DelayConfig")
    
    
    type DelayConfig<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > = number | DelayExpr<TContext, TExpressionEvent, TParams, TEvent>;




### type [DelayedTransitions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L176 "View definition for DelayedTransitions")
    
    
    type DelayedTransitions<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string
    
    > = {
    
        [K in Delay<TDelay>]?:
    
            | string
    
            | SingleOrArray<
    
                  TransitionConfig<
    
                      TContext,
    
                      TEvent,
    
                      TEvent,
    
                      TActor,
    
                      TAction,
    
                      TGuard,
    
                      TDelay,
    
                      TODO, // TEmitted
    
                      TODO
    
                  >
    
              >;
    
    };




### type [DelayExpr](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L520 "View definition for DelayExpr")
    
    
    type DelayExpr<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > = (
    
        args: ActionArgs<TContext, TExpressionEvent, TEvent>,
    
        params: TParams
    
    ) => number;




### type [DelayFunctionMap](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L420 "View definition for DelayFunctionMap")
    
    
    type DelayFunctionMap<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TAction extends ParameterizedObject
    
    > = Record<string, DelayConfig<TContext, TEvent, TAction['params'], TEvent>>;




### type [DevToolsAdapter](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L782 "View definition for DevToolsAdapter")
    
    
    type DevToolsAdapter = (service: AnyActor) => void;




### type [DoNotInfer](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L63 "View definition for DoNotInfer")
    
    
    type DoNotInfer<T> = [T][T extends any ? 0 : any];




### type [Elements](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L52 "View definition for Elements")
    
    
    type Elements<T> = T[keyof T & `${number}`];




### type [EmittedFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L886 "View definition for EmittedFrom")
    
    
    type EmittedFrom<TLogic extends AnyActorLogic> = TLogic extends ActorLogic<
    
        infer _TSnapshot,
    
        infer _TEvent,
    
        infer _TInput,
    
        infer _TSystem,
    
        infer TEmitted
    
    >
    
        ? TEmitted
    
        : never;




### type [Equals](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L60 "View definition for Equals")
    
    
    type Equals<A1, A2> = (<A>() => A extends A2 ? true : false) extends <
    
        A
    
    >() => A extends A1 ? true : false
    
        ? true
    
        : false;




### type [EventDescriptor](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L197 "View definition for EventDescriptor")
    
    
    type EventDescriptor<TEvent extends EventObject> =
    
        | TEvent['type']
    
        | PartialEventDescriptor<TEvent['type']>
    
        | '*';




### type [EventFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L888 "View definition for EventFrom")
    
    
    type EventFrom<
    
        T,
    
        K extends Prop<TEvent, 'type'> = never,
    
        TEvent extends EventObject = ResolveEventType<T>
    
    > = IsNever<K> extends true ? TEvent : ExtractEvent<TEvent, K>;




### type [EventFromLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L885 "View definition for EventFromLogic")
    
    
    type EventFromLogic<TLogic extends AnyActorLogic> = TLogic extends ActorLogic<
    
        infer _TSnapshot,
    
        infer TEvent,
    
        infer _TInput,
    
        infer _TEmitted,
    
        infer _TSystem
    
    >
    
        ? TEvent
    
        : never;




### type [EventObject](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L71 "View definition for EventObject")
    
    
    type EventObject = {
    
        /** The type of event that is sent. */
    
        type: string;
    
    };

  * The full definition of an event, with a string `type`.




### type [ExecutableActionsFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L1006 "View definition for ExecutableActionsFrom")
    
    
    type ExecutableActionsFrom<T extends AnyActorLogic> = T extends StateMachine<
    
        infer _TContext,
    
        infer _TEvent,
    
        infer _TChildren,
    
        infer _TActor,
    
        infer TAction,
    
        infer _TGuard,
    
        infer _TDelay,
    
        infer _TStateValue,
    
        infer _TTag,
    
        infer _TInput,
    
        infer _TOutput,
    
        infer _TEmitted,
    
        infer _TMeta,
    
        infer _TStateSchema
    
    >
    
        ?
    
              | SpecialExecutableAction
    
              | (string extends TAction['type'] ? never : ToExecutableAction<TAction>)
    
        : never;




### type [ExtractEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L750 "View definition for ExtractEvent")
    
    
    type ExtractEvent<
    
        TEvent extends EventObject,
    
        TDescriptor extends EventDescriptor<TEvent>
    
    > = string extends TEvent['type']
    
        ? TEvent
    
        : NormalizeDescriptor<TDescriptor> extends infer TNormalizedDescriptor
    
        ? TEvent extends any
    
            ? true extends EventDescriptorMatches<TEvent['type'], TNormalizedDescriptor>
    
                ? TEvent
    
                : never
    
            : never
    
        : never;




### type [GetConcreteByKey](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L964 "View definition for GetConcreteByKey")
    
    
    type GetConcreteByKey<T, TKey extends keyof T, TValue extends T[TKey]> = T &
    
        Record<TKey, TValue>;




### type [GetParameterizedParams](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L25 "View definition for GetParameterizedParams")
    
    
    type GetParameterizedParams<T extends ParameterizedObject | undefined> =
    
        T extends any ? ('params' extends keyof T ? T['params'] : undefined) : never;




### type [GuardPredicate](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts#L16 "View definition for GuardPredicate")
    
    
    type GuardPredicate<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TGuard extends ParameterizedObject
    
    > = {
    
        (args: GuardArgs<TContext, TExpressionEvent>, params: TParams): boolean;
    
        _out_TGuard?: TGuard;
    
    };




### type [HistoryValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L495 "View definition for HistoryValue")
    
    
    type HistoryValue<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > = Record<string, Array<StateNode<TContext, TEvent>>>;




### type [HomomorphicOmit](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L19 "View definition for HomomorphicOmit")
    
    
    type HomomorphicOmit<T, K extends keyof any> = {
    
        [P in keyof T as Exclude<P, K>]: T[P];
    
    };




### type [HomomorphicPick](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L16 "View definition for HomomorphicPick")
    
    
    type HomomorphicPick<T, K extends keyof any> = {
    
        [P in keyof T as P & K]: T[P];
    
    };




### type [Identity](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L13 "View definition for Identity")
    
    
    type Identity<T> = {
    
        [K in keyof T]: T[K];
    
    };




### type [IndexByProp](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L54 "View definition for IndexByProp")
    
    
    type IndexByProp<T extends Record<P, string>, P extends keyof T> = {
    
        [E in T as E[P]]: E;
    
    };




### type [IndexByType](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L57 "View definition for IndexByType")
    
    
    type IndexByType<
    
        T extends {
    
            type: string;
    
        }
    
    > = IndexByProp<T, 'type'>;




### type [InferEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L890 "View definition for InferEvent")
    
    
    type InferEvent<E extends EventObject> = {
    
        [T in E['type']]: {
    
            type: T;
    
        } & Extract<
    
            E,
    
            {
    
                type: T;
    
            }
    
        >;
    
    }[E['type']];




### type [InputFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L93 "View definition for InputFrom")
    
    
    type InputFrom<T> = T extends StateMachine<
    
        infer _TContext,
    
        infer _TEvent,
    
        infer _TChildren,
    
        infer _TActor,
    
        infer _TAction,
    
        infer _TGuard,
    
        infer _TDelay,
    
        infer _TStateValue,
    
        infer _TTag,
    
        infer TInput,
    
        infer _TOutput,
    
        infer _TEmitted,
    
        infer _TMeta,
    
        infer _TStateSchema
    
    >
    
        ? TInput
    
        : T extends ActorLogic<
    
              infer _TSnapshot,
    
              infer _TEvent,
    
              infer TInput,
    
              infer _TSystem,
    
              infer _TEmitted
    
          >
    
        ? TInput
    
        : never;




### type [InspectionEvent](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts#L2 "View definition for InspectionEvent")
    
    
    type InspectionEvent =
    
        | InspectedSnapshotEvent
    
        | InspectedEventEvent
    
        | InspectedActorEvent
    
        | InspectedMicrostepEvent
    
        | InspectedActionEvent;




### type [InternalMachineImplementations](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L444 "View definition for InternalMachineImplementations")
    
    
    type InternalMachineImplementations<TTypes extends StateMachineTypes> = {
    
        actions?: MachineImplementationsActions<TTypes>;
    
        actors?: MachineImplementationsActors<TTypes>;
    
        delays?: MachineImplementationsDelays<TTypes>;
    
        guards?: MachineImplementationsGuards<TTypes>;
    
    };




### type [Interpreter](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L226 "View definition for Interpreter")
    
    
    type Interpreter = typeof Actor;

  * #### Deprecated

Use `Actor` instead. 




### type [InterpreterFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L784 "View definition for InterpreterFrom")
    
    
    type InterpreterFrom<
    
        T extends AnyStateMachine | ((...args: any[]) => AnyStateMachine)
    
    > = ReturnTypeOrValue<T> extends StateMachine<
    
        infer TContext,
    
        infer TEvent,
    
        infer TChildren,
    
        infer _TActor,
    
        infer _TAction,
    
        infer _TGuard,
    
        infer _TDelay,
    
        infer TStateValue,
    
        infer TTag,
    
        infer TInput,
    
        infer TOutput,
    
        infer TEmitted,
    
        infer TMeta,
    
        infer TStateSchema
    
    >
    
        ? Actor<
    
              ActorLogic<
    
                  MachineSnapshot<
    
                      TContext,
    
                      TEvent,
    
                      TChildren,
    
                      TStateValue,
    
                      TTag,
    
                      TOutput,
    
                      TMeta,
    
                      TStateSchema
    
                  >,
    
                  TEvent,
    
                  TInput,
    
                  AnyActorSystem,
    
                  TEmitted
    
              >
    
          >
    
        : never;

  * #### Deprecated

Use `Actor<T>` instead.




### type [Invert](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L22 "View definition for Invert")
    
    
    type Invert<T extends Record<PropertyKey, PropertyKey>> = {
    
        [K in keyof T as T[K]]: K;
    
    };




### type [InvokeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L234 "View definition for InvokeConfig")
    
    
    type InvokeConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > = IsLiteralString<TActor['src']> extends true
    
        ? DistributeActors<
    
              TContext,
    
              TEvent,
    
              TActor,
    
              TAction,
    
              TGuard,
    
              TDelay,
    
              TEmitted,
    
              TMeta,
    
              TActor
    
          >
    
        : {
    
              /**
    
               * The unique identifier for the invoked machine. If not specified, this
    
               * will be the machine's own `id`, or the URL (from `src`).
    
               */
    
              id?: string;
    
              systemId?: string;
    
              /** The source of the machine to be invoked, or the machine itself. */
    
              src: AnyActorLogic | string;
    
              input?:
    
                  | Mapper<TContext, TEvent, NonReducibleUnknown, TEvent>
    
                  | NonReducibleUnknown;
    
              /**
    
               * The transition to take upon the invoked child machine reaching its
    
               * final top-level state.
    
               */
    
              onDone?:
    
                  | string
    
                  | SingleOrArray<
    
                        TransitionConfigOrTarget<
    
                            TContext,
    
                            DoneActorEvent<any>, // TODO: consider replacing with `unknown`
    
                            TEvent,
    
                            TActor,
    
                            TAction,
    
                            TGuard,
    
                            TDelay,
    
                            TEmitted,
    
                            TMeta
    
                        >
    
                    >;
    
              /**
    
               * The transition to take upon the invoked child machine sending an
    
               * error event.
    
               */
    
              onError?:
    
                  | string
    
                  | SingleOrArray<
    
                        TransitionConfigOrTarget<
    
                            TContext,
    
                            ErrorActorEvent,
    
                            TEvent,
    
                            TActor,
    
                            TAction,
    
                            TGuard,
    
                            TDelay,
    
                            TEmitted,
    
                            TMeta
    
                        >
    
                    >;
    
              onSnapshot?:
    
                  | string
    
                  | SingleOrArray<
    
                        TransitionConfigOrTarget<
    
                            TContext,
    
                            SnapshotEvent,
    
                            TEvent,
    
                            TActor,
    
                            TAction,
    
                            TGuard,
    
                            TDelay,
    
                            TEmitted,
    
                            TMeta
    
                        >
    
                    >;
    
          };




### type [IsAny](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L61 "View definition for IsAny")
    
    
    type IsAny<T> = Equals<T, any>;




### type [IsLiteralString](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L199 "View definition for IsLiteralString")
    
    
    type IsLiteralString<T extends string> = string extends T ? false : true;




### type [IsNever](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L45 "View definition for IsNever")
    
    
    type IsNever<T> = [T] extends [never] ? true : false;




### type [IsNotNever](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L46 "View definition for IsNotNever")
    
    
    type IsNotNever<T> = [T] extends [never] ? false : true;




### type [Lazy](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L68 "View definition for Lazy")
    
    
    type Lazy<T> = () => T;




### type [LogExpr](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L521 "View definition for LogExpr")
    
    
    type LogExpr<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject
    
    > = (
    
        args: ActionArgs<TContext, TExpressionEvent, TEvent>,
    
        params: TParams
    
    ) => unknown;




### type [LowInfer](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L66 "View definition for LowInfer")
    
    
    type LowInfer<T> = T & NonNullable<unknown>;




### type [MachineConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L458 "View definition for MachineConfig")
    
    
    type MachineConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor = ProvidedActor,
    
        TAction extends ParameterizedObject = ParameterizedObject,
    
        TGuard extends ParameterizedObject = ParameterizedObject,
    
        TDelay extends string = string,
    
        TTag extends string = string,
    
        TInput = any,
    
        TOutput = unknown,
    
        TEmitted extends EventObject = EventObject,
    
        TMeta extends MetaObject = MetaObject
    
    > = (Omit<
    
        StateNodeConfig<
    
            DoNotInfer<TContext>,
    
            DoNotInfer<TEvent>,
    
            DoNotInfer<TActor>,
    
            DoNotInfer<TAction>,
    
            DoNotInfer<TGuard>,
    
            DoNotInfer<TDelay>,
    
            DoNotInfer<TTag>,
    
            DoNotInfer<TOutput>,
    
            DoNotInfer<TEmitted>,
    
            DoNotInfer<TMeta>
    
        >,
    
        'output'
    
    > & {
    
        /** The initial context (extended state) */
    
        /** The machine's own version. */
    
        version?: string;
    
        output?: Mapper<TContext, DoneStateEvent, TOutput, TEvent> | TOutput;
    
    }) &
    
        (MachineContext extends TContext
    
            ? {
    
                  context?: InitialContext<LowInfer<TContext>, TActor, TInput, TEvent>;
    
              }
    
            : {
    
                  context: InitialContext<LowInfer<TContext>, TActor, TInput, TEvent>;
    
              });




### type [MachineContext](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L90 "View definition for MachineContext")
    
    
    type MachineContext = Record<string, any>;




### type [MachineImplementationsFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L785 "View definition for MachineImplementationsFrom")
    
    
    type MachineImplementationsFrom<
    
        T extends AnyStateMachine | ((...args: any[]) => AnyStateMachine)
    
    > = ReturnTypeOrValue<T> extends StateMachine<
    
        infer TContext,
    
        infer TEvent,
    
        infer _TChildren,
    
        infer TActor,
    
        infer TAction,
    
        infer TGuard,
    
        infer TDelay,
    
        infer _TStateValue,
    
        infer TTag,
    
        infer _TInput,
    
        infer _TOutput,
    
        infer TEmitted,
    
        infer _TMeta,
    
        infer _TStateSchema
    
    >
    
        ? InternalMachineImplementations<
    
              ResolvedStateMachineTypes<
    
                  TContext,
    
                  TEvent,
    
                  TActor,
    
                  TAction,
    
                  TGuard,
    
                  TDelay,
    
                  TTag,
    
                  TEmitted
    
              >
    
          >
    
        : never;




### type [MachineSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/State.d.ts#L91 "View definition for MachineSnapshot")
    
    
    type MachineSnapshot<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TChildren extends Record<string, AnyActorRef | undefined>,
    
        TStateValue extends StateValue,
    
        TTag extends string,
    
        TOutput,
    
        TMeta extends MetaObject,
    
        TStateSchema extends StateSchema
    
    > =
    
        | ActiveMachineSnapshot<
    
              TContext,
    
              TEvent,
    
              TChildren,
    
              TStateValue,
    
              TTag,
    
              TOutput,
    
              TMeta,
    
              TStateSchema
    
          >
    
        | DoneMachineSnapshot<
    
              TContext,
    
              TEvent,
    
              TChildren,
    
              TStateValue,
    
              TTag,
    
              TOutput,
    
              TMeta,
    
              TStateSchema
    
          >
    
        | ErrorMachineSnapshot<
    
              TContext,
    
              TEvent,
    
              TChildren,
    
              TStateValue,
    
              TTag,
    
              TOutput,
    
              TMeta,
    
              TStateSchema
    
          >
    
        | StoppedMachineSnapshot<
    
              TContext,
    
              TEvent,
    
              TChildren,
    
              TStateValue,
    
              TTag,
    
              TOutput,
    
              TMeta,
    
              TStateSchema
    
          >;




### type [Mapper](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L544 "View definition for Mapper")
    
    
    type Mapper<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TResult,
    
        TEvent extends EventObject
    
    > = (args: {
    
        context: TContext;
    
        event: TExpressionEvent;
    
        self: ActorRef<
    
            MachineSnapshot<
    
                TContext,
    
                TEvent,
    
                Record<string, AnyActorRef>, // TODO: this should be replaced with `TChildren`
    
                StateValue,
    
                string,
    
                unknown,
    
                TODO, // TMeta
    
                TODO
    
            >,
    
            TEvent,
    
            AnyEventObject
    
        >;
    
    }) => TResult;




### type [MaybeLazy](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L69 "View definition for MaybeLazy")
    
    
    type MaybeLazy<T> = T | Lazy<T>;




### type [Merge](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L53 "View definition for Merge")
    
    
    type Merge<M, N> = Omit<M, keyof N> & N;




### type [MetaObject](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L67 "View definition for MetaObject")
    
    
    type MetaObject = Record<string, any>;




### type [NoInfer](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L65 "View definition for NoInfer")
    
    
    type NoInfer<T> = DoNotInfer<T>;

  * #### Deprecated

Use the built-in `NoInfer` type instead




### type [NonReducibleUnknown](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L42 "View definition for NonReducibleUnknown")
    
    
    type NonReducibleUnknown = {} | null | undefined;

  * #### Remarks

`T | unknown` reduces to `unknown` and that can be problematic when it comes to contextual typing. It especially is a problem when the union has a function member, like here:
        
        declare function test(
        
          cbOrVal: ((arg: number) => unknown) | unknown
        
        ): void;
        
        test((arg) => {}); // oops, implicit any

This type can be used to avoid this problem. This union represents the same value space as `unknown`.




### type [NoRequiredParams](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L108 "View definition for NoRequiredParams")
    
    
    type NoRequiredParams<T extends ParameterizedObject> = T extends any
    
        ? undefined extends T['params']
    
            ? T['type']
    
            : never
    
        : never;




### type [ObservableActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts#L8 "View definition for ObservableActorLogic")
    
    
    type ObservableActorLogic<
    
        TContext,
    
        TInput extends NonReducibleUnknown,
    
        TEmitted extends EventObject = EventObject
    
    > = ActorLogic<
    
        ObservableSnapshot<TContext, TInput>,
    
        {
    
            type: string;
    
            [k: string]: unknown;
    
        },
    
        TInput,
    
        AnyActorSystem,
    
        TEmitted
    
    >;




### type [ObservableActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts#L44 "View definition for ObservableActorRef")
    
    
    type ObservableActorRef<TContext> = ActorRefFromLogic<
    
        ObservableActorLogic<TContext, any>
    
    >;

  * Represents an actor created by `fromObservable` or `fromEventObservable`.

The type of `self` within the actor's logic.

#### Example 1
        
        import { fromObservable, createActor } from 'xstate';
        
        import { interval } from 'rxjs';
        
        
        
        
        // The type of the value observed by the actor's logic.
        
        type Context = number;
        
        // The actor's input.
        
        type Input = { period?: number };
        
        
        
        
        // Actor logic that observes a number incremented every `input.period`
        
        // milliseconds (default: 1_000).
        
        const logic = fromObservable<Context, Input>(({ input, self }) => {
        
          self;
        
          // ^? ObservableActorRef<Event, Input>
        
        
        
        
          return interval(input.period ?? 1_000);
        
        });
        
        
        
        
        const actor = createActor(logic, { input: { period: 2_000 } });
        
        //    ^? ObservableActorRef<Event, Input>

#### See Also

    * fromObservable

    * fromEventObservable




### type [ObservableSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts#L3 "View definition for ObservableSnapshot")
    
    
    type ObservableSnapshot<
    
        TContext,
    
        TInput extends NonReducibleUnknown
    
    > = Snapshot<undefined> & {
    
        context: TContext | undefined;
    
        input: TInput | undefined;
    
        _subscription: Subscription | undefined;
    
    };




### type [Observer](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L731 "View definition for Observer")
    
    
    type Observer<T> = {
    
        next?: (value: T) => void;
    
        error?: (err: unknown) => void;
    
        complete?: () => void;
    
    };




### type [OutputFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L94 "View definition for OutputFrom")
    
    
    type OutputFrom<T> = T extends ActorLogic<
    
        infer TSnapshot,
    
        infer _TEvent,
    
        infer _TInput,
    
        infer _TSystem,
    
        infer _TEmitted
    
    >
    
        ? (TSnapshot & {
    
              status: 'done';
    
          })['output']
    
        : T extends ActorRef<infer TSnapshot, infer _TEvent, infer _TEmitted>
    
        ? (TSnapshot & {
    
              status: 'done';
    
          })['output']
    
        : never;




### type [PartialAssigner](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L540 "View definition for PartialAssigner")
    
    
    type PartialAssigner<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TKey extends keyof TContext
    
    > = (
    
        args: AssignArgs<TContext, TExpressionEvent, TEvent, TActor>,
    
        params: TParams
    
    ) => TContext[TKey];




### type [PersistedHistoryValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L496 "View definition for PersistedHistoryValue")
    
    
    type PersistedHistoryValue = Record<
    
        string,
    
        Array<{
    
            id: string;
    
        }>
    
    >;




### type [PromiseActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/promise.d.ts#L6 "View definition for PromiseActorLogic")
    
    
    type PromiseActorLogic<
    
        TOutput,
    
        TInput = unknown,
    
        TEmitted extends EventObject = EventObject
    
    > = ActorLogic<
    
        PromiseSnapshot<TOutput, TInput>,
    
        {
    
            type: string;
    
            [k: string]: unknown;
    
        },
    
        TInput, // input
    
        AnyActorSystem,
    
        TEmitted
    
    >;




### type [PromiseActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/promise.d.ts#L44 "View definition for PromiseActorRef")
    
    
    type PromiseActorRef<TOutput> = ActorRefFromLogic<
    
        PromiseActorLogic<TOutput, unknown>
    
    >;

  * Represents an actor created by `fromPromise`.

The type of `self` within the actor's logic.

#### Example 1
        
        import { fromPromise, createActor } from 'xstate';
        
        
        
        
        // The actor's resolved output
        
        type Output = string;
        
        // The actor's input.
        
        type Input = { message: string };
        
        
        
        
        // Actor logic that fetches the url of an image of a cat saying `input.message`.
        
        const logic = fromPromise<Output, Input>(async ({ input, self }) => {
        
          self;
        
          // ^? PromiseActorRef<Output, Input>
        
        
        
        
          const data = await fetch(
        
            `https://cataas.com/cat/says/${input.message}`
        
          );
        
          const url = await data.json();
        
          return url;
        
        });
        
        
        
        
        const actor = createActor(logic, { input: { message: 'hello world' } });
        
        //    ^? PromiseActorRef<Output, Input>

#### See Also

    * fromPromise




### type [PromiseSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/promise.d.ts#L3 "View definition for PromiseSnapshot")
    
    
    type PromiseSnapshot<TOutput, TInput> = Snapshot<TOutput> & {
    
        input: TInput | undefined;
    
    };




### type [Prop](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L50 "View definition for Prop")
    
    
    type Prop<T, K> = K extends keyof T ? T[K] : never;




### type [PropertyAssigner](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L541 "View definition for PropertyAssigner")
    
    
    type PropertyAssigner<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor
    
    > = {
    
        [K in keyof TContext]?:
    
            | PartialAssigner<TContext, TExpressionEvent, TParams, TEvent, TActor, K>
    
            | TContext[K];
    
    };




### type [RequiredActorOptions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L903 "View definition for RequiredActorOptions")
    
    
    type RequiredActorOptions<TActor extends ProvidedActor> =
    
        | (undefined extends TActor['id'] ? never : 'id')
    
        | (undefined extends InputFrom<TActor['logic']> ? never : 'input');




### type [RequiredActorOptionsKeys](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts#L170 "View definition for RequiredActorOptionsKeys")
    
    
    type RequiredActorOptionsKeys<TLogic extends AnyActorLogic> =
    
        undefined extends InputFrom<TLogic> ? never : 'input';




### type [RequiredLogicInput](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L904 "View definition for RequiredLogicInput")
    
    
    type RequiredLogicInput<TLogic extends AnyActorLogic> =
    
        undefined extends InputFrom<TLogic> ? never : 'input';




### type [RoutableStateId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L937 "View definition for RoutableStateId")
    
    
    type RoutableStateId<TSchema extends StateSchema> =
    
        | (TSchema extends {
    
              route: any;
    
              id: string;
    
          }
    
              ? `#${TSchema['id']}`
    
              : never)
    
        | (TSchema['states'] extends Record<string, any>
    
              ? Values<{
    
                    [K in keyof TSchema['states'] & string]: RoutableStateId<
    
                        TSchema['states'][K]
    
                    >;
    
                }>
    
              : never);




### type [SendExpr](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L522 "View definition for SendExpr")
    
    
    type SendExpr<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TParams extends ParameterizedObject['params'] | undefined,
    
        TSentEvent extends EventObject,
    
        TEvent extends EventObject
    
    > = (
    
        args: ActionArgs<TContext, TExpressionEvent, TEvent>,
    
        params: TParams
    
    ) => TSentEvent;




### type [SetupReturn](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/setup.d.ts#L32 "View definition for SetupReturn")
    
    
    type SetupReturn<TContext extends MachineContext, TEvent extends AnyEventObject, TActors extends Record<string, UnknownActorLogic>, TChildrenMap extends Record<string, string>, TActions extends Record<string, ParameterizedObject['params'] | undefined>, TGuards extends Record<string, ParameterizedObject['params'] | undefined>, TDelay extends string, TTag extends string, TInput, TOutput extends NonReducibleUnknown, TEmitted extends EventObject, TMeta extends MetaObject> = {
    
        extend: <TExtendActions extends Record<string, ParameterizedObject['params'] | undefined> = {}, TExtendGuards extends Record<string, ParameterizedObject['params'] | undefined> = {}, TExtendDelays extends string = never>({ actions, guards, delays }: {
    
            actions?: {
    
                [K in keyof TExtendActions]: ActionFunction<TContext, TEvent, TEvent, TExtendActions[K], ToProvidedActor<TChildrenMap, TActors>, ToParameterizedObject<TActions & TExtendActions>, ToParameterizedObject<TGuards & TExtendGuards>, TDelay | TExtendDelays, TEmitted>;
    
            };
    
            guards?: {
    
                [K in keyof TExtendGuards]: GuardPredicate<TContext, TEvent, TExtendGuards[K], ToParameterizedObject<TGuards & TExtendGuards>>;
    
            };
    
            delays?: {
    
                [K in TExtendDelays]: DelayConfig<TContext, TEvent, ToParameterizedObject<TActions & TExtendActions>['params'], TEvent>;
    
            };
    
        }) => SetupReturn<TContext, TEvent, TActors, TChildrenMap, TActions & TExtendActions, TGuards & TExtendGuards, TDelay | TExtendDelays, TTag, TInput, TOutput, TEmitted, TMeta>;
    
        /**
    
         * Creates a state config that is strongly typed. This state config can be
    
         * used to create a machine.
    
         *
    
         * @example
    
         *
    
         * ```ts
    
         * const lightMachineSetup = setup({
    
         *   // ...
    
         * });
    
         *
    
         * const green = lightMachineSetup.createStateConfig({
    
         *   on: {
    
         *     timer: {
    
         *       actions: 'doSomething'
    
         *     }
    
         *   }
    
         * });
    
         *
    
         * const machine = lightMachineSetup.createMachine({
    
         *   initial: 'green',
    
         *   states: {
    
         *     green,
    
         *     yellow,
    
         *     red
    
         *   }
    
         * });
    
         * ```
    
         */
    
        createStateConfig: <TStateConfig extends StateNodeConfig<TContext, TEvent, ToProvidedActor<TChildrenMap, TActors>, ToParameterizedObject<TActions>, ToParameterizedObject<TGuards>, TDelay, TTag, unknown, TEmitted, TMeta>>(config: TStateConfig) => TStateConfig;
    
        /**
    
         * Creates a type-safe action.
    
         *
    
         * @example
    
         *
    
         * ```ts
    
         * const machineSetup = setup({
    
         *   // ...
    
         * });
    
         *
    
         * const action = machineSetup.createAction(({ context, event }) => {
    
         *   console.log(context.count, event.value);
    
         * });
    
         *
    
         * const incrementAction = machineSetup.createAction(
    
         *   assign({ count: ({ context }) => context.count + 1 })
    
         * );
    
         *
    
         * const machine = machineSetup.createMachine({
    
         *   context: { count: 0 },
    
         *   entry: [action, incrementAction]
    
         * });
    
         * ```
    
         */
    
        createAction: (action: ActionFunction<TContext, TEvent, TEvent, unknown, ToProvidedActor<TChildrenMap, TActors>, ToParameterizedObject<TActions>, ToParameterizedObject<TGuards>, TDelay, TEmitted>) => typeof action;
    
        createMachine: <const




### type [SimpleOrStateNodeConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L408 "View definition for SimpleOrStateNodeConfig")
    
    
    type SimpleOrStateNodeConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > =
    
        | AtomicStateNodeConfig<TContext, TEvent>
    
        | StateNodeConfig<
    
              TContext,
    
              TEvent,
    
              TODO,
    
              TODO,
    
              TODO,
    
              TODO,
    
              TODO,
    
              TODO,
    
              TODO, // emitted
    
              TODO
    
          >;




### type [SingleOrArray](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L181 "View definition for SingleOrArray")
    
    
    type SingleOrArray<T> = readonly T[] | T;




### type [Snapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L801 "View definition for Snapshot")
    
    
    type Snapshot<TOutput> =
    
        | {
    
              status: 'active';
    
              output: undefined;
    
              error: undefined;
    
          }
    
        | {
    
              status: 'done';
    
              output: TOutput;
    
              error: undefined;
    
          }
    
        | {
    
              status: 'error';
    
              output: undefined;
    
              error: unknown;
    
          }
    
        | {
    
              status: 'stopped';
    
              output: undefined;
    
              error: undefined;
    
          };




### type [SnapshotFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L884 "View definition for SnapshotFrom")
    
    
    type SnapshotFrom<T> = ReturnTypeOrValue<T> extends infer R
    
        ? R extends ActorRef<infer TSnapshot, infer _, infer __>
    
            ? TSnapshot
    
            : R extends Actor<infer TLogic>
    
            ? SnapshotFrom<TLogic>
    
            : R extends ActorLogic<
    
                  infer _TSnapshot,
    
                  infer _TEvent,
    
                  infer _TInput,
    
                  infer _TEmitted,
    
                  infer _TSystem
    
              >
    
            ? ReturnType<R['transition']>
    
            : R extends ActorScope<
    
                  infer TSnapshot,
    
                  infer _TEvent,
    
                  infer _TEmitted,
    
                  infer _TSystem
    
              >
    
            ? TSnapshot
    
            : never
    
        : never;




### type [SnapshotStatus](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L800 "View definition for SnapshotStatus")
    
    
    type SnapshotStatus = 'active' | 'done' | 'error' | 'stopped';




### type [Spawner](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/spawn.d.ts#L14 "View definition for Spawner")
    
    
    type Spawner<TActor extends ProvidedActor> = IsLiteralString<
    
        TActor['src']
    
    > extends true
    
        ? {
    
              <TSrc extends TActor['src']>(
    
                  logic: TSrc,
    
                  ...[options]: SpawnOptions<TActor, TSrc>
    
              ): ActorRefFromLogic<GetConcreteByKey<TActor, 'src', TSrc>['logic']>;
    
              <TLogic extends AnyActorLogic>(
    
                  src: TLogic,
    
                  ...[options]: ConditionalRequired<
    
                      [
    
                          options?: {
    
                              id?: never;
    
                              systemId?: string;
    
                              input?: InputFrom<TLogic>;
    
                              syncSnapshot?: boolean;
    
                          } & {
    
                              [K in RequiredLogicInput<TLogic>]: unknown;
    
                          }
    
                      ],
    
                      IsNotNever<RequiredLogicInput<TLogic>>
    
                  >
    
              ): ActorRefFromLogic<TLogic>;
    
          }
    
        : <TLogic extends AnyActorLogic | string>(
    
              src: TLogic,
    
              ...[options]: ConditionalRequired<
    
                  [
    
                      options?: {
    
                          id?: string;
    
                          systemId?: string;
    
                          input?: TLogic extends string ? unknown : InputFrom<TLogic>;
    
                          syncSnapshot?: boolean;
    
                      } & (TLogic extends AnyActorLogic
    
                          ? {
    
                                [K in RequiredLogicInput<TLogic>]: unknown;
    
                            }
    
                          : {})
    
                  ],
    
                  IsNotNever<
    
                      TLogic extends AnyActorLogic ? RequiredLogicInput<TLogic> : never
    
                  >
    
              >
    
          ) => TLogic extends AnyActorLogic ? ActorRefFromLogic<TLogic> : AnyActorRef;




### type [SpecialExecutableAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L1005 "View definition for SpecialExecutableAction")
    
    
    type SpecialExecutableAction =
    
        | ExecutableSpawnAction
    
        | ExecutableRaiseAction
    
        | ExecutableSendToAction;




### type [StateFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L500 "View definition for StateFrom")
    
    
    type StateFrom<T extends AnyStateMachine | ((...args: any[]) => AnyStateMachine)> =
    
        T extends AnyStateMachine
    
            ? ReturnType<T['transition']>
    
            : T extends (...args: any[]) => AnyStateMachine
    
            ? ReturnType<ReturnType<T>['transition']>
    
            : never;




### type [StateId](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L932 "View definition for StateId")
    
    
    type StateId<
    
        TSchema extends StateSchema,
    
        TKey extends string = '(machine)',
    
        TParentKey extends string | null = null
    
    > =
    
        | (TSchema extends {
    
              id: string;
    
          }
    
              ? TSchema['id']
    
              : TParentKey extends null
    
              ? TKey
    
              : `${TParentKey}.${TKey}`)
    
        | (TSchema['states'] extends Record<string, any>
    
              ? Values<{
    
                    [K in keyof TSchema['states'] & string]: StateId<
    
                        TSchema['states'][K],
    
                        K,
    
                        TParentKey extends string
    
                            ? `${TParentKey}.${TKey}`
    
                            : TSchema['id'] extends string
    
                            ? TSchema['id']
    
                            : TKey
    
                    >;
    
                }>
    
              : never);




### type [StateKey](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L120 "View definition for StateKey")
    
    
    type StateKey = string | AnyMachineSnapshot;




### type [StateNodesConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L182 "View definition for StateNodesConfig")
    
    
    type StateNodesConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > = {
    
        [K in string]: StateNode<TContext, TEvent>;
    
    };




### type [StateSchema](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L915 "View definition for StateSchema")
    
    
    type StateSchema = {
    
        id?: string;
    
        route?: unknown;
    
        states?: Record<string, StateSchema>;
    
        type?: unknown;
    
        invoke?: unknown;
    
        on?: unknown;
    
        entry?: unknown;
    
        exit?: unknown;
    
        onDone?: unknown;
    
        after?: unknown;
    
        always?: unknown;
    
        meta?: unknown;
    
        output?: unknown;
    
        tags?: unknown;
    
        description?: unknown;
    
    };




### type [StatesConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L185 "View definition for StatesConfig")
    
    
    type StatesConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TTag extends string,
    
        TOutput,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > = {
    
        [K in string]: StateNodeConfig<
    
            TContext,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TTag,
    
            TOutput,
    
            TEmitted,
    
            TMeta
    
        >;
    
    };




### type [StatesDefinition](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L188 "View definition for StatesDefinition")
    
    
    type StatesDefinition<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > = {
    
        [K in string]: StateNodeDefinition<TContext, TEvent>;
    
    };




### type [StateTypes](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L180 "View definition for StateTypes")
    
    
    type StateTypes =
    
        | 'atomic'
    
        | 'compound'
    
        | 'parallel'
    
        | 'final'
    
        | 'history'
    
        | ({} & string);




### type [StateValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L133 "View definition for StateValue")
    
    
    type StateValue = string | StateValueMap;

  * The string or object representing the state value relative to the parent state node.

#### Remarks

\- For a child atomic state node, this is a string, e.g., `"pending"`. - For complex state nodes, this is an object, e.g., `{ success: "someChildState" }`.




### type [StateValueFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L898 "View definition for StateValueFrom")
    
    
    type StateValueFrom<TMachine extends AnyStateMachine> = Parameters<
    
        StateFrom<TMachine>['matches']
    
    >[0];




### type [TagsFrom](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L899 "View definition for TagsFrom")
    
    
    type TagsFrom<TMachine extends AnyStateMachine> = Parameters<
    
        StateFrom<TMachine>['hasTag']
    
    >[0];




### type [ToChildren](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L909 "View definition for ToChildren")
    
    
    type ToChildren<TActor extends ProvidedActor> = string extends TActor['src']
    
        ? Record<string, AnyActorRef>
    
        : Compute<
    
              ToConcreteChildren<TActor> &
    
                  {
    
                      include: {
    
                          [id: string]: TActor extends any
    
                              ? ActorRefFromLogic<TActor['logic']> | undefined
    
                              : never;
    
                      };
    
                      exclude: unknown;
    
                  }[undefined extends TActor['id']
    
                      ? 'include'
    
                      : string extends TActor['id']
    
                      ? 'include'
    
                      : 'exclude']
    
          >;




### type [TODO](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L897 "View definition for TODO")
    
    
    type TODO = any;




### type [ToStateValue](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L974 "View definition for ToStateValue")
    
    
    type ToStateValue<T extends StateSchema> = T extends {
    
        states: Record<infer S, any>;
    
    }
    
        ? IsNever<S> extends true
    
            ? {}
    
            :
    
                  | GroupStateKeys<T, S>['leaf']
    
                  | (IsNever<GroupStateKeys<T, S>['nonLeaf']> extends false
    
                        ? T extends {
    
                              type: 'parallel';
    
                          }
    
                            ? {
    
                                  [K in GroupStateKeys<T, S>['nonLeaf']]: ToStateValue<
    
                                      T['states'][K]
    
                                  >;
    
                              }
    
                            : Compute<
    
                                  Values<{
    
                                      [K in GroupStateKeys<T, S>['nonLeaf']]: {
    
                                          [StateKey in K]: ToStateValue<T['states'][K]>;
    
                                      };
    
                                  }>
    
                              >
    
                        : never)
    
        : {};




### type [TransitionActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/transition.d.ts#L6 "View definition for TransitionActorLogic")
    
    
    type TransitionActorLogic<
    
        TContext,
    
        TEvent extends EventObject,
    
        TInput extends NonReducibleUnknown,
    
        TEmitted extends EventObject = EventObject
    
    > = ActorLogic<
    
        TransitionSnapshot<TContext>,
    
        TEvent,
    
        TInput,
    
        AnyActorSystem,
    
        TEmitted
    
    >;




### type [TransitionActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/transition.d.ts#L65 "View definition for TransitionActorRef")
    
    
    type TransitionActorRef<TContext, TEvent extends EventObject> = ActorRefFromLogic<
    
        TransitionActorLogic<TransitionSnapshot<TContext>, TEvent, unknown>
    
    >;

  * Represents an actor created by `fromTransition`.

The type of `self` within the actor's logic.

#### Example 1
        
        import {
        
          fromTransition,
        
          createActor,
        
          type AnyActorSystem
        
        } from 'xstate';
        
        
        
        
        //* The actor's stored context.
        
        type Context = {
        
          // The current count.
        
          count: number;
        
          // The amount to increase `count` by.
        
          step: number;
        
        };
        
        // The events the actor receives.
        
        type Event = { type: 'increment' };
        
        // The actor's input.
        
        type Input = { step?: number };
        
        
        
        
        // Actor logic that increments `count` by `step` when it receives an event of
        
        // type `increment`.
        
        const logic = fromTransition<Context, Event, AnyActorSystem, Input>(
        
          (state, event, actorScope) => {
        
            actorScope.self;
        
            //         ^? TransitionActorRef<Context, Event>
        
        
        
        
            if (event.type === 'increment') {
        
              return {
        
                ...state,
        
                count: state.count + state.step
        
              };
        
            }
        
            return state;
        
          },
        
          ({ input, self }) => {
        
            self;
        
            // ^? TransitionActorRef<Context, Event>
        
        
        
        
            return {
        
              count: 0,
        
              step: input.step ?? 1
        
            };
        
          }
        
        );
        
        
        
        
        const actor = createActor(logic, { input: { step: 10 } });
        
        //    ^? TransitionActorRef<Context, Event>

#### See Also

    * fromTransition




### type [TransitionConfigOrTarget](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L192 "View definition for TransitionConfigOrTarget")
    
    
    type TransitionConfigOrTarget<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > = SingleOrArray<
    
        | TransitionConfigTarget
    
        | TransitionConfig<
    
              TContext,
    
              TExpressionEvent,
    
              TEvent,
    
              TActor,
    
              TAction,
    
              TGuard,
    
              TDelay,
    
              TEmitted,
    
              TMeta
    
          >
    
    >;




### type [TransitionConfigTarget](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L191 "View definition for TransitionConfigTarget")
    
    
    type TransitionConfigTarget = string | undefined;




### type [TransitionDefinitionMap](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L573 "View definition for TransitionDefinitionMap")
    
    
    type TransitionDefinitionMap<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > = {
    
        [K in EventDescriptor<TEvent>]: Array<
    
            TransitionDefinition<TContext, ExtractEvent<TEvent, K>>
    
        >;
    
    };




### type [Transitions](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L501 "View definition for Transitions")
    
    
    type Transitions<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject
    
    > = Array<TransitionDefinition<TContext, TEvent>>;




### type [TransitionsConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L193 "View definition for TransitionsConfig")
    
    
    type TransitionsConfig<
    
        TContext extends MachineContext,
    
        TEvent extends EventObject,
    
        TActor extends ProvidedActor,
    
        TAction extends ParameterizedObject,
    
        TGuard extends ParameterizedObject,
    
        TDelay extends string,
    
        TEmitted extends EventObject,
    
        TMeta extends MetaObject
    
    > = {
    
        [K in EventDescriptor<TEvent>]?: TransitionConfigOrTarget<
    
            TContext,
    
            ExtractEvent<TEvent, K>,
    
            TEvent,
    
            TActor,
    
            TAction,
    
            TGuard,
    
            TDelay,
    
            TEmitted,
    
            TMeta
    
        >;
    
    };




### type [TransitionSnapshot](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/transition.d.ts#L3 "View definition for TransitionSnapshot")
    
    
    type TransitionSnapshot<TContext> = Snapshot<undefined> & {
    
        context: TContext;
    
    };




### type [TransitionTarget](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L134 "View definition for TransitionTarget")
    
    
    type TransitionTarget = SingleOrArray<string>;




### type [UnknownAction](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L118 "View definition for UnknownAction")
    
    
    type UnknownAction = Action<
    
        MachineContext,
    
        EventObject,
    
        EventObject,
    
        ParameterizedObject['params'] | undefined,
    
        ProvidedActor,
    
        ParameterizedObject,
    
        ParameterizedObject,
    
        string,
    
        EventObject
    
    >;




### type [UnknownActorLogic](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L880 "View definition for UnknownActorLogic")
    
    
    type UnknownActorLogic = ActorLogic<
    
        any, // snapshot
    
        any, // event
    
        any, // input
    
        AnyActorSystem,
    
        any
    
    >;




### type [UnknownActorRef](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L777 "View definition for UnknownActorRef")
    
    
    type UnknownActorRef = ActorRef<Snapshot<unknown>, EventObject>;




### type [UnknownMachineConfig](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L468 "View definition for UnknownMachineConfig")
    
    
    type UnknownMachineConfig = MachineConfig<MachineContext, EventObject>;




### type [Values](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L51 "View definition for Values")
    
    
    type Values<T> = T[keyof T];




### type [WithDynamicParams](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts#L110 "View definition for WithDynamicParams")
    
    
    type WithDynamicParams<
    
        TContext extends MachineContext,
    
        TExpressionEvent extends EventObject,
    
        T extends ParameterizedObject
    
    > = T extends any
    
        ? ConditionalRequired<
    
              {
    
                  type: T['type'];
    
                  params?:
    
                      | T['params']
    
                      | (({
    
                            context,
    
                            event,
    
                        }: {
    
                            context: TContext;
    
                            event: TExpressionEvent;
    
                        }) => T['params']);
    
              },
    
              undefined extends T['params'] ? false : true
    
          >
    
        : never;




## Package Files (34)

  * [dist/declarations/src/SimulatedClock.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/SimulatedClock.d.ts "View file dist/declarations/src/SimulatedClock.d.ts")
  * [dist/declarations/src/State.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/State.d.ts "View file dist/declarations/src/State.d.ts")
  * [dist/declarations/src/StateMachine.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateMachine.d.ts "View file dist/declarations/src/StateMachine.d.ts")
  * [dist/declarations/src/StateNode.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/StateNode.d.ts "View file dist/declarations/src/StateNode.d.ts")
  * [dist/declarations/src/actions/assign.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/assign.d.ts "View file dist/declarations/src/actions/assign.d.ts")
  * [dist/declarations/src/actions/cancel.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/cancel.d.ts "View file dist/declarations/src/actions/cancel.d.ts")
  * [dist/declarations/src/actions/emit.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/emit.d.ts "View file dist/declarations/src/actions/emit.d.ts")
  * [dist/declarations/src/actions/enqueueActions.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/enqueueActions.d.ts "View file dist/declarations/src/actions/enqueueActions.d.ts")
  * [dist/declarations/src/actions/log.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/log.d.ts "View file dist/declarations/src/actions/log.d.ts")
  * [dist/declarations/src/actions/raise.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/raise.d.ts "View file dist/declarations/src/actions/raise.d.ts")
  * [dist/declarations/src/actions/send.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/send.d.ts "View file dist/declarations/src/actions/send.d.ts")
  * [dist/declarations/src/actions/spawnChild.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/spawnChild.d.ts "View file dist/declarations/src/actions/spawnChild.d.ts")
  * [dist/declarations/src/actions/stopChild.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actions/stopChild.d.ts "View file dist/declarations/src/actions/stopChild.d.ts")
  * [dist/declarations/src/actors/callback.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/callback.d.ts "View file dist/declarations/src/actors/callback.d.ts")
  * [dist/declarations/src/actors/index.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/index.d.ts "View file dist/declarations/src/actors/index.d.ts")
  * [dist/declarations/src/actors/observable.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/observable.d.ts "View file dist/declarations/src/actors/observable.d.ts")
  * [dist/declarations/src/actors/promise.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/promise.d.ts "View file dist/declarations/src/actors/promise.d.ts")
  * [dist/declarations/src/actors/transition.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/actors/transition.d.ts "View file dist/declarations/src/actors/transition.d.ts")
  * [dist/declarations/src/assert.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/assert.d.ts "View file dist/declarations/src/assert.d.ts")
  * [dist/declarations/src/createActor.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createActor.d.ts "View file dist/declarations/src/createActor.d.ts")
  * [dist/declarations/src/createMachine.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/createMachine.d.ts "View file dist/declarations/src/createMachine.d.ts")
  * [dist/declarations/src/getNextSnapshot.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/getNextSnapshot.d.ts "View file dist/declarations/src/getNextSnapshot.d.ts")
  * [dist/declarations/src/guards.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/guards.d.ts "View file dist/declarations/src/guards.d.ts")
  * [dist/declarations/src/inspection.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/inspection.d.ts "View file dist/declarations/src/inspection.d.ts")
  * [dist/declarations/src/setup.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/setup.d.ts "View file dist/declarations/src/setup.d.ts")
  * [dist/declarations/src/spawn.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/spawn.d.ts "View file dist/declarations/src/spawn.d.ts")
  * [dist/declarations/src/stateUtils.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/stateUtils.d.ts "View file dist/declarations/src/stateUtils.d.ts")
  * [dist/declarations/src/system.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/system.d.ts "View file dist/declarations/src/system.d.ts")
  * [dist/declarations/src/toPromise.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/toPromise.d.ts "View file dist/declarations/src/toPromise.d.ts")
  * [dist/declarations/src/transition.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/transition.d.ts "View file dist/declarations/src/transition.d.ts")
  * [dist/declarations/src/types.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/types.d.ts "View file dist/declarations/src/types.d.ts")
  * [dist/declarations/src/utils.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/utils.d.ts "View file dist/declarations/src/utils.d.ts")
  * [dist/declarations/src/waitFor.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/declarations/src/waitFor.d.ts "View file dist/declarations/src/waitFor.d.ts")
  * [dist/xstate.cjs.d.ts](https://unpkg.com/browse/xstate@5.28.0/dist/xstate.cjs.d.ts "View file dist/xstate.cjs.d.ts")



## Dependencies (0)

No  dependencies.

## Dev Dependencies (5)

  * [@scion-scxml/test-framework](/package/@scion-scxml/test-framework/v/2.0.15 "@scion-scxml/test-framework@^2.0.15")
  * [ajv](/package/ajv/v/8.12.0 "ajv@^8.12.0")
  * [pkg-up](/package/pkg-up/v/3.1.0 "pkg-up@^3.1.0")
  * [rxjs](/package/rxjs/v/7.8.1 "rxjs@^7.8.1")
  * [xml-js](/package/xml-js/v/1.6.11 "xml-js@^1.6.11")



## Peer Dependencies (0)

No peer dependencies.

## Badge

To add a badge like this one![jsDocs.io badge](/badge.svg)to your package's README, use the codes available below.

You may also use [Shields.io](https://shields.io/) to create a custom badge linking to `https://www.jsdocs.io/package/xstate`.

  * Markdown
        
        [![jsDocs.io](https://img.shields.io/badge/jsDocs.io-reference-blue)](https://www.jsdocs.io/package/xstate)

  * HTML
        
        <a href="https://www.jsdocs.io/package/xstate"><img src="https://img.shields.io/badge/jsDocs.io-reference-blue" alt="jsDocs.io"></a>




* * *

  * Updated 1 second ago.  
Package analyzed in 11044 ms.
  * Missing or incorrect documentation? [Open an issue for this package](https://github.com/jsdocs-io/web/issues/new?title=Package+xstate%405.28.0+has+missing+or+incorrect+documentation&template=package-with-missing-or-incorrect-documentation.md).
  * Back to top



[![Logo for jsDocs.io](/logo.png)jsDocs.io](/ "jsDocs.io")

  * [Home](/)
  * [Guide](/guide)
  * [Donate](/sponsor)
  * [About](/about)
  * [Credits](/credits)
  * [Privacy](/privacy)
  * [GitHub](https://github.com/jsdocs-io)
  * [Issues](https://github.com/jsdocs-io/web/issues)
  * [Twitter](https://twitter.com/jsDocs)

[](https://vercel.com/?utm_source=jsdocs-io&utm_campaign=oss "Powered by Vercel")
