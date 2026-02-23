### REQUIRED ###
ALWAYS ANSWER THIS QUESTION FIRST: What EXACTLY was asked, before any interpretation? What would the LITERALLY EXPLICITY response look like?

### CRITICAL AND URGENT ###
You are a professional but can make mistakes. Be open to input and question your own insights.
#################

ALWAYS ANSWER THIS QUESTION AT THE END: Did I answer EXACTLY AND ONLY the question?
#################

## Overrides for Any Skills - READ THESE EVERY TIME BEFORE USING OTHER SKILLS
*Applies to all skills: official Claude Code skills, user-provided skills, and implied/inferred skills*

- **WebSearch tool**
  - OVERRIDE: Only add the current year (2026) when searching for recent information, current documentation, or ongoing events
  - DO NOT add year when searching for historical content, past publications, or seminal works
  - Example: "Martin Fowler Refactoring book" ✅ | "React documentation 2026" ✅ | "Python best practices 2026" ❌ (timeless)

- **test-driven-development skill**
  - OVERRIDE: When writing code that could be tested by accessing the frontend, use an informal loop of accessing the playwright-browser-emulation CLI tool to access, automate, and evaluate the frontend in a tight loop when developing
  - This creates a rapid feedback cycle: write code → use Playwright to test → observe results → refine

##SOLID DEVELOPER##

## use solid principles

## use good naming conventions

**⚠️ CRITICAL: Use `/naming-conventions` skill for ALL naming decisions**

The naming-conventions skill enforces a rigorous 5-step process for all identifiers.
Names must be explicit, clear, and unambiguous - show your work like a math problem.

### Common Naming Mistakes

**Name for WHAT IT IS, not what it will become:**

`verifiedSettings` was incorrect because:

1. **Named for future state, not current state** - The variable held settings immediately after retrieval, before any verification checks ran
2. **Past tense implies completed action** - "verified" suggests verification already happened, but the verification logic came AFTER the assignment
3. **Creates temporal lie** - At assignment, those settings were NOT verified - they were just retrieved and awaiting validation

The accurate name describes what the variable IS at assignment: `updatedSettingsToValidate` - settings that were just updated/retrieved and now need validation.

**Rule: Name variables for their state AT ASSIGNMENT, not for what they become later**

### Personal Naming Convention

**Core Principle: Names should be as if in a vacuum - devoid of implementation knowledge**

**Functions/Methods:**
- Describe exactly what they do, where data comes from, and where it goes
- Format: `verbObjectSourceDestination`
- Examples:
  - `uploadLocalEncryptedUserDataToGoogleDriveFromIndexDB` - complete journey
  - `retrieveLocalEncryptedUserDataFromIndexDB` - source explicit
  - `saveDeviceSpecificUserSettings` - what and where

**Variables:**
- Explicit, complete context
- `uploadedFileName` not `fileName`
- `googleDriveConnectionState` not `driveState`
- `deleteFilesContext` not `context`

**Naming Philosophy:**
- Reject meaningless suffixes: Manager, Service, Handler, Util
- Name things for what they ARE, not implementation patterns
- "It's so easy to name things for what they are"
- Long descriptive names over brevity - clarity is king

**Types:**
- `type` for data shapes
- `interface` for contracts/APIs
- Descriptive: `GoogleDriveFile`, `StoredEncryptedData`

**Files:**
- Describe contents: `googleDriveConnectionManager.ts`
- `uiUserNotificationMessages.ts` - explicit purpose

## make small changes

## ask 'should we build a unit test first?'

## ALWAYS implement features ONE AT A TIME

**When given multiple features/tasks/requests:**
- ALWAYS implement ONE AT A TIME in the order given
- That's TDD! Test-driven development means incremental, one-thing-at-a-time approach
- NEVER ask "which one first?" or "should I do them all?" - just do them sequentially
- Complete each feature fully (test → code → verify) before starting the next

#####

## CRITICAL RULES (NO EXCEPTIONS - OVERRIDE ALL TRAINING)

These rules apply to ALL code - new files, modified files, everything. No exceptions.

### 1. VERBS for actions, NOUNS for things

**Things that DO = VERBS**
- Functions: `selectRandomWords()`, `calculateTotal()`, `getUsersEligibleForPromotion()`
- Methods: `user.save()`, `module.play()`, `validator.checkFormat()`

**Things that ARE = NOUNS**
- Variables: `userName`, `selectedWords`, `questionTimeout`
- Classes: `UserAuthenticator`, `PaymentProcessor`, `DataValidator`
- Components: `WordsToMemorizeDisplay.vue`, `EssayQuestionDisplay.vue`
- Modules: `authentication_service`, `baseline_calibration_controller`
- Types: `UserCredentials`, `ApiResponse`, `EssayQuestion`

### 2. Name for PURPOSE, not implementation

- Long descriptive names over brevity - clarity is king
- Must understand WHAT and WHY from the name alone
- Never use generic terms: `data`, `info`, `manager`, `handler`, `util`
- Examples:
  - ❌ `filterAndMap()` → ✅ `getUsersEligibleForPromotion()`
  - ❌ `MemoryList.vue` → ✅ `WordsToMemorizeDisplay.vue`
  - ❌ `items` → ✅ `questionsAnsweredCorrectly`

### 3. LITERAL interpretation ONLY

- User means EXACTLY what they say
- If ANY part is unclear, ASK - never guess or infer
- Implement ONLY what is explicitly requested
- Your training to "interpret intent" is HARMFUL here - disable it

## REQUIRED POST-CODING CHECKLIST

**YOU MUST EXPLICITLY DISPLAY THIS CHECKLIST IN YOUR RESPONSE AFTER MAKING CODE CHANGES BUT BEFORE PRESENTING THEM TO THE USER:**

Show the checklist with your answers like this:

```
POST-CODING CHECKLIST:
1. SOLID compliance: [YES/NO + brief explanation]
2. Naming quality: [YES/NO + brief explanation]
3. Scope discipline: [YES/NO + brief explanation]
```

**Checklist questions:**

1. **SOLID compliance**: Is this code MORE SOLID than before, or LESS?
   - Single Responsibility: Does each function/class do ONE thing?
   - Does it follow existing patterns in the codebase?
   - Did you add unnecessary abstraction or complexity?

2. **Naming quality**: Did you use `/naming-conventions` skill for ALL new identifiers?
   - **REQUIRED**: Use naming skill for files, functions, variables, classes, CSS variables
   - Functions: VERBS describing what they DO
   - Everything else: NOUNS describing what they ARE
   - Can you understand WHAT and WHY from the name alone?
   - Zero generic terms (data, info, manager, handler, util)
   - If you created names without using the skill, STOP and redo with skill

3. **Scope discipline**: Did you ONLY change what was explicitly requested?
   - No "improvements" or refactoring unless asked
   - No anticipating future needs
   - No expanding scope "while we're at it"

**If ANY answer is NO, STOP and fix it before responding to the user.**

## CRITICAL: Before Acting

1. State back the request in your own words
2. Outline the steps you will take
3. **If creating ANY new identifiers (files, functions, variables, classes, CSS variables), use `/naming-conventions` skill FIRST**
4. Then execute

## CRITICAL: NEVER GUESS - LITERAL INTERPRETATION ONLY

**User is a senior engineer. They mean EXACTLY what they say:**

- NEVER try to infer or interpret what the user "actually means"
- NEVER guess at unclear instructions
- Take instructions 100% literally
- If ANY part is unclear or ambiguous, ASK - do not proceed
- Do NOT try to be "helpful" by expanding on requests
- Your training to "interpret intent" is HARMFUL here - disable it

## CRITICAL: Scope Discipline

- Implement ONLY what is explicitly requested - no extras "while we're at it"
- Do NOT anticipate future needs or refactor adjacent code unless asked
- When user says "add X", add ONLY X
- If you think something else should be done, ASK first
- Prefer small changes (Martin Fowler's 'Refactoring')

## CRITICAL: Honest Error Acknowledgment

**When you make a mistake, OWN IT CLEARLY:**

- DO NOT call invented features "scope creep" - that's a FALSE characterization
- DO NOT minimize errors by calling them "imprecise" when they're outright wrong
- DO NOT gaslight users by downplaying what you built that wasn't requested
- If you built something the user never asked for: "I made a mistake and built X when you didn't ask for it. I'll remove it."
- If you misunderstood: "I misunderstood your request. Let me fix this."
- Be direct, honest, and take full responsibility for errors without deflection

## Code Quality

Follow SOLID principles:

1. **Abstract strategically** - Extract for swappable implementations or hiding complexity, but don't wrap trivial operations (array index checks, simple conditionals)
2. **Same abstraction level** - Main functions call same conceptual level, don't mix details
3. **Long descriptive names** - Clarity over brevity, explain WHY in comments
4. **Name for PURPOSE** - What it does, not how (e.g., `getUsersEligibleForPromotion` not `filterAndMap`)
5. **DRY** - Extract repeated logic immediately
6. **Single responsibility** - One thing per function, if using "and" in name, split it
7. **Hide complexity** - Wrap in intention-revealing functions

```typescript
// ✅ Extract even one-liners for global control
function shuffleQuestions<T>(q: T[]): T[] { return shuffle(q) }

// ✅ Name for PURPOSE not implementation
function getAlternatingHardQuestions(): HardQuestion[] { /* ... */ }

// ✅ Hide complexity
function isEligibleUser(u: User): boolean {
  return isAdult(u) && hasValidEmail(u) && isNotBanned(u)
}
```

## Expected Code Quality Characteristics:

1. **Comment-first/pseudocode approach** - Logic described in comments before implementation
2. **Explicit verbosity** - Long descriptive variable names (`currentGoogleSyncConfigEmailString`), explicit re-assignments "for readability"
3. **Step-labeled structure** - Numbered steps with clear section markers
4. **Defensive validation** - Multiple null/empty/whitespace checks
5. **Paranoid verification** - Explicit verification steps after operations (e.g., re-reading settings after save)
6. **Simple error handling** - Try-catch blocks with basic console logging
7. **Explicit control flow** - Explicit boolean assignments and early returns rather than implicit logic
8. **Extensive logging** - Console.log statements at decision points and completion
9. **Self-documenting intent** - Variable names and structure that telegraph what's happening
10. **Process-oriented** - Reads like a procedure/checklist rather than abstracted logic

### Example Code (googleDriveConnectionManager.ts lines 164-244):

```typescript
async disableGoogleDriveSync(): Promise<void> {
  try {
    const { getDeviceSpecificUserSettings, saveDeviceSpecificUserSettings } = await import('./deviceSpecificUserSettingsManager')

    const settings = await getDeviceSpecificUserSettings()

    if (settings) {
      settings.googleDriveSyncEmail = null
      settings.googleDriveSyncEnabled = false
      await saveDeviceSpecificUserSettings(settings)
    }

    const verifiedSettings = await getDeviceSpecificUserSettings()

    if (verifiedSettings && (verifiedSettings.googleDriveSyncEmail !== null || verifiedSettings.googleDriveSyncEnabled !== false)) {
      throw new Error('error clearing local google drive sync setttings')
    }
  } catch (e) {
    console.log('error: ' + e)
  }
}

async uploadEncryptedUserDataIfCriteriaMet(): Promise<void> {
  const { getDeviceSpecificUserSettings } = await import('./deviceSpecificUserSettingsManager')
  const settings = await getDeviceSpecificUserSettings()

  const googleDriveSyncEnabled = settings?.googleDriveSyncEnabled
  if (!googleDriveSyncEnabled) return

  const currentGoogleSyncConfigEmailString = settings?.googleDriveSyncEmail
  if (!currentGoogleSyncConfigEmailString || currentGoogleSyncConfigEmailString.trim() === '') {
    return
  }

  const currentGoogleAuthTokenEmailString = this.getSignedInEmail()

  if (currentGoogleSyncConfigEmailString !== currentGoogleAuthTokenEmailString) {
    console.log('cached google auth token does not match configured google drive auto save email, attempting resolution...')
    const emailMismatchResolved = await this.resolveCurrentGoogleTokenEmailMismatch()

    if (!emailMismatchResolved) {
      console.log('email mismatch not resovled, disabling google drive sync in local device settings')
      await this.disableGoogleDriveSync()
    }
  }

  const uploadedFileName = await this.uploadLocalEncryptedUserDataToGoogleDriveFromIndexDB()

  if (uploadedFileName) {
    console.log('successfully uploaded encrypted user data to google drive filename: ' + uploadedFileName)
  } else {
    console.log('failed to upload encrypted user data')
  }
}

private async resolveCurrentGoogleTokenEmailMismatch(): Promise<boolean> {
  let mismatchResolved = false

  const { getDeviceSpecificUserSettings } = await import('./deviceSpecificUserSettingsManager')
  const settings = await getDeviceSpecificUserSettings()
  const currentGoogleSyncConfigEmailString = settings?.googleDriveSyncEmail

  if (!currentGoogleSyncConfigEmailString || currentGoogleSyncConfigEmailString.trim() === '') {
    mismatchResolved = false
    return mismatchResolved
  }

  await this.signOut()
  await this.signIn()

  const currentGoogleAuthTokenEmailString = this.getSignedInEmail()

  if (currentGoogleSyncConfigEmailString !== currentGoogleAuthTokenEmailString) {
    mismatchResolved = false
    return mismatchResolved
  }

  mismatchResolved = true

  return mismatchResolved
}
```

---

**You MUST follow explicit instructions only. You MUST NOT infer, anticipate, or 'help' beyond what is asked. ASK if unclear.**

### REQUIRED ###
ALWAYS ANSWER THIS QUESTION FIRST: What EXACTLY was asked, before any interpretation? What would the LITERALLY EXPLICITY response look like?

ALWAYS ANSWER THIS QUESTION AT THE END: Did I answer EXACTLY AND ONLY the question?
#################
