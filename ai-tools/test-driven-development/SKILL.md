---
name: test-driven-development
description: "Enforce strict Test-Driven Development workflow: write one test, make it pass, verify, then proceed. Prevents over-implementation and ensures code matches requirements exactly. Use when implementing new features, adding settings, or building functionality incrementally."
---

# Test-Driven Development (TDD)

## When to Use This Skill

Use this skill when the user explicitly requests:
- "Use TDD"
- "Test-driven development"
- "Write tests first"
- "Add tests before implementing"
- Implementing features incrementally with test verification at each step

## Core TDD Principle

**NEVER write implementation code before writing a test for it.**

The TDD cycle is:
1. **Write ONE test** for the next small piece of functionality
2. **Run the test** - it should fail (red)
3. **Write minimal code** to make that specific test pass
4. **Run the test** - verify it passes (green)
5. **ONLY THEN** proceed to the next test

## Critical Rules

### 1. ONE Test at a Time

```bash
# WRONG: Adding multiple tests at once
it('should load panel1Text', () => { ... })
it('should load panel2Text', () => { ... })
it('should load panel3Text', () => { ... })
# Then implementing all at once

# RIGHT: One test, verify, next test
it('should load panel1Text', () => { ... })
# Run test → passes
# THEN add next test
it('should load panel2Text', () => { ... })
# Run test → passes
# THEN add next test
```

### 2. Test Drives Implementation, Not Vice Versa

```typescript
// WRONG: Implementation first
const settings = {
  panel1Text: "Welcome",
  panel2Text: "I'm Theia",
  panel3Text: "Your partner"
}
// Then write tests

// RIGHT: Test first
it('should have panel1Text', () => {
  expect(settings).toHaveProperty('panel1Text')
  expect(settings.panel1Text).toBe('Welcome')
})
// Test fails → add ONLY panel1Text → test passes
```

### 3. Verify After Each Step

Every test must be run and confirmed passing before writing the next test:

```bash
# After writing each test:
bun test your-test-file.test.ts

# Verify output shows:
✓ should have panel1Text
# 1 pass, 0 fail

# ONLY THEN proceed to next test
```

### 4. Minimal Implementation

Write the absolute minimum code to make the current test pass:

```json
// Test: should have panel1Text with value "Welcome"

// WRONG: Adding everything at once
{
  "panel1Text": "Welcome",
  "panel2Text": "I'm Theia",
  "panel3Text": "Your partner"
}

// RIGHT: Only what's needed for current test
{
  "panel1Text": "Welcome"
}
```

### 5. Mocked Timers and Async Testing

**CRITICAL RULE: Mocked processes with timers shall always add to a cumulative maxPotentialDelayTime so the assert timeout will always be sufficient because it will be based on that plus its own buffer.**

When testing code that uses timers (setTimeout, setInterval, debounce):

#### Track Cumulative Time

```typescript
// WRONG: Guessing how long to wait
setTimeout(async () => {
  await operation1()  // Unknown duration
  await operation2()  // Unknown duration
}, 1000)

await vi.advanceTimersByTimeAsync(2000)  // Random guess
expect(mock).toHaveBeenCalled()  // Might fail

// RIGHT: Track cumulative potential delay
let maxPotentialDelayTime = 0

// Timer adds 1000ms
maxPotentialDelayTime += 1000

// Mock operations add their durations
maxPotentialDelayTime += mockOperation1Duration  // e.g., 50ms
maxPotentialDelayTime += mockOperation2Duration  // e.g., 100ms

// Advance timers by tracked total + buffer
await vi.advanceTimersByTimeAsync(maxPotentialDelayTime + 100)
expect(mock).toHaveBeenCalled()  // Will always succeed
```

#### Implementation Pattern

```typescript
describe('async operation', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  it('completes within tracked time', async () => {
    // Define all mock process timers at start
    const mockProcessTimers = [
      1000,  // DEBOUNCE_DELAY
      10,    // MOCK_GET_DELAY
      10,    // MOCK_UPLOAD_DELAY
      10,    // MOCK_IMPORT_DELAY
      10     // MOCK_SAVE_DELAY
    ]

    // Define buffer for assertion safety
    const assertDelayBuffer = 100

    // Calculate total delay needed
    const assertDelay = mockProcessTimers.reduce((sum, delay) => sum + delay, 0) + assertDelayBuffer

    // Trigger operation
    triggerDebouncedOperation()

    // Wait for calculated delay
    await vi.advanceTimersByTimeAsync(assertDelay)

    expect(mockOperation).toHaveBeenCalled()
  })
})
```

#### Why This Matters

**Without time tracking:**
- Tests guess arbitrary wait times
- Flaky tests that sometimes pass/fail
- No relationship between mock delays and test waits
- "House of cards" timing

**With time tracking:**
- Tests know exactly how long to wait
- Deterministic, reliable tests
- Clear relationship between delays and waits
- Tests adapt when delays change

**Never use arbitrary timeouts like `2000ms` without justification. Always track cumulative delays.**

#### Dynamic Imports and Fake Timers

**CRITICAL: Avoid dynamic imports in code paths that create timers when using fake timers for testing.**

**Generic Problem:**
When code has an async operation (dynamic import, network call, etc.) that creates a timer AFTER the async work completes, fake timer APIs like `runAllTimersAsync()` will check for timers BEFORE the async operation completes, find none, and return immediately. The timer is created later and never executes.

**Rule:** If your code uses fake timers for testing, do not use dynamic imports (`await import()`) in the code path before creating the timer.

## REQUIRED PROCEDURE FOR FIXING TEST ISSUES

**When a test fails unexpectedly, you MUST follow this procedure:**

1. **List dependencies:** Identify every tool/function the test uses
2. **Create proof file:** New test file (e.g., `featureProofTest.test.ts`) to prove each dependency works
3. **Start minimal:** Simplest possible test (tool exists and runs)
4. **Add one thing:** Each new test adds exactly one complexity
5. **Run after each:** Test fails = found the broken assumption
6. **Continue to completion:** Build proof tests all the way until they replicate ALL aspects of the problematic test (mocked modules, dynamic imports, exact async patterns, etc.)
7. **Compare patterns:** If all pass, issue is test setup not tools

**Result:** First failing proof test shows exactly what's broken. All passing = real test has environment/mocking issue.

**Do NOT:**
- Guess at solutions without proving tool behavior
- Search for fixes without understanding the problem
- Modify real tests without isolating the issue
- Repeat failed approaches expecting different results

## TDD Workflow Example

**User Request:** "Add three panel text settings to the config file"

### Step 1: First Test

```typescript
// baseline-test-settings.test.ts
it('should have panel1Text', () => {
  expect(settings.panel1Text).toBe('Welcome')
})
```

Run test:
```bash
bun test baseline-test-settings.test.ts
# ✗ Test fails - property doesn't exist
```

### Step 2: Minimal Implementation

```json
// baseline-test-settings.json
{
  "panel1Text": "Welcome"
}
```

### Step 3: Verify

```bash
bun test baseline-test-settings.test.ts
# ✓ 1 pass
```

**STOP.** Report success. Ask if user wants to proceed to next test.

### Step 4: Second Test

```typescript
it('should have panel2Text', () => {
  expect(settings.panel2Text).toBe("I'm Theia")
})
```

Run test → Fails → Add only panel2Text → Test passes → Report → Repeat

## Critical: Test Functionality, Not Configuration Data

**FUNDAMENTAL PRINCIPLE:** Tests should verify that code **works correctly**, not that configuration has specific values.

### ✅ Test Structure and Types

```typescript
// CORRECT: Test that property exists and has right type
it('should have timerVisible setting', () => {
  expect(settings).toHaveProperty('timerVisible')
  expect(typeof settings.timerVisible).toBe('boolean')
})

// CORRECT: Test that numeric property exists
it('should have questionTimeout setting', () => {
  expect(settings).toHaveProperty('questionTimeout')
  expect(typeof settings.questionTimeout).toBe('number')
})
```

### ❌ Don't Test Configuration Values

```typescript
// WRONG: Testing specific config value
it('should have timerVisible setting', () => {
  expect(settings.timerVisible).toBe(false)  // ❌ BAD
})
// Problem: If user changes config to true, test fails
// But the loading functionality still works!

// WRONG: Testing specific text content
it('should have welcome text', () => {
  expect(settings.welcomeText).toBe('Welcome')  // ❌ BAD
})
// Problem: If user changes text to "Hello", test fails
// But the loading functionality still works!
```

### Why This Matters

**Configuration data changes frequently:**
- User preferences
- Business requirements
- A/B testing
- Localization

**Functionality rarely changes:**
- Property exists
- Type is correct
- Structure is valid

**If changing a config value breaks tests, your tests are wrong.**

### Exception: Integration Tests

Only test specific values when verifying **integration** between systems:

```typescript
// ACCEPTABLE in integration test:
it('should calculate timeout correctly', () => {
  const timeout = calculateTimeout(settings.baseTime, settings.multiplier)
  expect(timeout).toBe(100)  // Testing calculation, not config
})
```

## Anti-Patterns to Avoid

### ❌ Implementing Multiple Features Without Tests

```typescript
// WRONG: Adding all settings at once
{
  "panel1Text": "Welcome",
  "panel2Text": "I'm Theia",
  "panel3Text": "Your partner",
  "fadeInTime": 0.8,
  "delayTime": 2.2
}
// Then writing tests afterward
```

### ❌ Writing Multiple Tests Before Implementation

```typescript
// WRONG: All tests written first
describe('settings', () => {
  it('should have panel1Text', () => { ... })
  it('should have panel2Text', () => { ... })
  it('should have panel3Text', () => { ... })
})
// Then implementing everything
```

### ❌ Not Verifying Tests Pass

```typescript
// Add test
it('should have panel1Text', () => { ... })

// Add implementation
{ "panel1Text": "Welcome" }

// WRONG: Immediately moving to next test without running current test
it('should have panel2Text', () => { ... })  // DON'T DO THIS YET
```

## Correct TDD Pattern

### Example: Adding Config Settings

**User:** "Add panel1Text, panel2Text, panel3Text to the config"

**Response:**
```
TDD Step 1: Adding panel1Text

1. Write test:
   it('should have panel1Text', () => {
     expect(settings.panel1Text).toBe('Welcome')
   })

2. Run test:
   bun test → FAILS (expected)

3. Add implementation:
   { "panel1Text": "Welcome" }

4. Run test:
   bun test → PASSES ✓

✓ panel1Text complete. Ready for panel2Text.
```

Wait for user confirmation before proceeding to panel2Text.

## Benefits of Strict TDD

1. **Prevents Over-Implementation**
   - Can't add features not requested
   - Each test represents an explicit requirement
   - Implementation scope is controlled by tests

2. **Ensures Requirements Match Code**
   - Tests define "what" before "how"
   - No guessing about intended behavior
   - Documentation through tests

3. **Immediate Feedback**
   - Know exactly when something breaks
   - Confidence that each piece works
   - Easier debugging (last change broke last test)

4. **Forces Incremental Progress**
   - Can't rush ahead
   - User sees progress step-by-step
   - Opportunity to course-correct early

## Integration with Solid Developer Principles

TDD aligns perfectly with solid-developer rules:

### Literal Interpretation
Tests make requirements explicit - no room for inference:
```typescript
// Test EXPLICITLY states requirement
it('should have panel1Text with value "Welcome"', () => {
  expect(settings.panel1Text).toBe('Welcome')
})
// Can only implement exactly this
```

### Ask When Unclear
If test requirements are ambiguous, STOP and ask:
```
User: "Add panel text settings"

STOP - Ask before writing test:
"How many panel text settings? What are their names and values?"
```

### No Anticipating Needs
Tests prevent adding "helpful" extras:
```typescript
// Test only requires panel1Text
it('should have panel1Text', () => { ... })

// WRONG: Adding more than tested
{
  "panel1Text": "Welcome",
  "panel2Text": "I'm Theia"  // NOT TESTED YET
}

// RIGHT: Only what test requires
{
  "panel1Text": "Welcome"
}
```

## When TDD is Not Appropriate

Don't use strict TDD for:
- Exploratory coding or prototyping
- One-line fixes or typo corrections
- Refactoring existing tested code
- Research tasks (reading code, analyzing)

## TDD Checklist

Before proceeding to next test, verify:
- [ ] Current test is written
- [ ] Current test was run and failed initially
- [ ] Minimal implementation added
- [ ] Current test was run and passed
- [ ] User confirmed or acknowledged success
- [ ] Ready to proceed to next test

## Common TDD Questions

**Q: How small should each test be?**
A: Test ONE property, ONE behavior, ONE requirement at a time.

**Q: What if multiple tests would pass with the same implementation?**
A: Still write them one at a time. Different tests document different requirements.

**Q: Should I run all tests or just the current one?**
A: Run all tests to ensure no regressions, but focus verification on the new test.

**Q: What if the user wants me to "implement everything"?**
A: Still use TDD - implement everything, but one test at a time, verifying each.

## Example Session

```
User: "Add three timing settings to config: fadeIn, delay, and pause"
Claude: "TDD Step 1: Adding fadeIn setting

1. Writing test for fadeIn:
   it('should have fadeIn timing', () => {
     expect(settings.timing).toHaveProperty('fadeIn')
     expect(typeof settings.timing.fadeIn).toBe('number')
   })

2. Running test:
   bun test settings.test.ts
   ✗ FAIL - property doesn't exist

3. Adding implementation:
   {
     "timing": {
       "fadeIn": 0.8
     }
   }

4. Running test:
   bun test settings.test.ts
   ✓ PASS

fadeIn setting complete. Ready to proceed to 'delay' setting."

User: "yes proceed"

Claude: "TDD Step 2: Adding delay setting

1. Writing test for delay:
   it('should have delay timing', () => {
     expect(settings.timing).toHaveProperty('delay')
     expect(typeof settings.timing.delay).toBe('number')
   })

2. Running test:
   bun test settings.test.ts
   ✗ FAIL - delay property doesn't exist

3. Adding implementation:
   {
     "timing": {
       "fadeIn": 0.8,
       "delay": 2.2
     }
   }

4. Running test:
   bun test settings.test.ts
   ✓ PASS (2 tests passing)

delay setting complete. Ready to proceed to 'pause' setting."

[Continues for pause...]
```

## Summary

**TDD ensures:**
- ✅ Only requested features are implemented
- ✅ Every feature has a test
- ✅ Tests document requirements
- ✅ Progress is verifiable at each step
- ✅ No scope creep or "helpful" additions
- ✅ User maintains control over pace and direction

**Use TDD when the user wants:**
- Incremental, verifiable progress
- Confidence that code matches specs
- Ability to course-correct early
- Documentation through tests
- To prevent over-engineering

**The TDD mantra:** Red → Green → Next
