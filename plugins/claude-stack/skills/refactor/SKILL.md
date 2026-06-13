---
name: refactor
description: Use when restructuring code WITHOUT changing its behavior — rename, extract a function/module, deduplicate, inline, move, simplify a structure. Phrases like "refactor this", "clean this up", "extract X", "reduce the duplication", "restructure", "untangle". Distinct from tdd (which adds new behavior) and debug (which fixes wrong behavior). If the behavior must change, this is not a refactor — stop and use tdd or debug.
---

# refactor

## Overview

A refactor changes the *shape* of code while keeping its *behavior* identical. The whole risk is silent behavior drift — "while I was in there" changes that no test catches.

**Core principle:** a refactor you can't prove is behavior-preserving is just an untested rewrite.

## The Iron Law

```
NO REFACTOR WITHOUT A GREEN SAFETY NET
```

Before touching structure, the code under change must be covered by tests that pass **now**. If it isn't, your first job is a **characterization test**: write tests that capture the *current* behavior (even if that behavior is ugly), watch them pass, and only then refactor. You are pinning behavior, not judging it.

## The loop

1. **Establish green.** Run the tests covering the target. All green? Proceed. Gaps? Add characterization tests first (capture current behavior — inputs → current outputs, including edge cases), watch them pass.
2. **One structural move at a time.** Rename, *or* extract, *or* inline — not three at once. Small steps are reviewable and bisectable.
3. **Stay green after every move.** Run the tests. Red → revert the last move (don't pile a fix on top), understand why, retry smaller.
4. **Never mix behavior and structure in one step.** If a "refactor" needs a behavior change, split it: land the behavior change via `tdd` (or `debug`) as its own step, then refactor on green.
5. **Commit in small, behavior-preserving increments.** Each commit message says "refactor: …" and asserts no behavior change.

## Red flags — stop

- "I'll just fix this bug while I'm refactoring" → separate step, use `debug`.
- "I'll add the feature as part of the cleanup" → separate step, use `tdd`.
- No tests cover this, but the change "obviously can't break anything" → write the characterization test; obvious-looking changes break things.
- Tests went red and you're editing the test to make it pass → you changed behavior. Stop and decide if that was intended.
- A giant single diff that renames, moves, and rewrites at once → un-bisectable; break it up.

## Do not

- Do not refactor untested code without first pinning its behavior with characterization tests.
- Do not change behavior and structure in the same step or commit.
- Do not weaken or delete a test to make a refactor "pass" — that is a behavior change in disguise.
- Do not claim the refactor is safe without a fresh green run (`verify-done`).

## Lineage

The red-green discipline is borrowed from `tdd`'s Refactor step, promoted to a first-class workflow for the case where restructuring — not new behavior — is the whole task.
