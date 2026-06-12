---
name: tdd
description: Use when implementing any feature or bugfix, before writing implementation code. Also use when tempted to write code first "just this once", keep pre-written code as reference, or add tests after the fact.
---

# tdd

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** if you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? **Delete it. Start over.** No exceptions: don't keep it as "reference", don't "adapt" it while writing tests, don't look at it. Delete means delete. Implement fresh from the test.

Exceptions exist only with explicit user sign-off: throwaway prototypes, generated code, pure config.

## Red-Green-Refactor

**RED — write one failing test.** One behavior, clear name, real code over mocks. The test demonstrates the API you wish existed.

**Verify RED — watch it fail. MANDATORY.** Run it. Confirm it *fails* (not errors), with the expected message, because the feature is missing (not a typo). Test passes immediately? You're testing existing behavior — fix the test. Test errors? Fix until it fails correctly.

**GREEN — minimal code.** The simplest change that passes. No extra features, no opportunistic refactoring, no options the test doesn't demand (YAGNI).

**Verify GREEN — watch it pass. MANDATORY.** Run it. This test passes, all other tests still pass, output pristine. Failing? Fix the code, not the test.

**REFACTOR — only on green.** Remove duplication, improve names, extract helpers. No new behavior. Stay green.

Repeat for the next behavior.

## Common rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing — you never saw them catch anything. |
| "Tests-after achieve the same goals" | Tests-after ask "what does this do?" Tests-first ask "what *should* this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost. Keeping unverified code is the real debt. |
| "Keep it as reference while I write tests" | You'll adapt it. That's testing after. Delete means delete. |
| "TDD is dogmatic; I'm being pragmatic" | Debugging in production is the slow path. TDD *is* the pragmatic option. |
| "Need to explore first" | Fine — then throw the exploration away and start with TDD. |

## Red flags — stop and start over

Code before test · test passes on first run · can't explain why the test failed · "just this once" · "I already manually tested it" · "it's about spirit not ritual" · "this is different because…"

**All of these mean: delete the code, restart with TDD.**

## Test quality

One behavior per test ("and" in the name → split it) · name describes behavior, not "test1" · real collaborators unless unavoidable (see the quality reviewer's mock-testing-the-mock check in `implement`) · hard to test = design feedback: simplify the interface, don't contort the test.

## Bug fixes

A bug is a missing test. Write the failing test that reproduces it, then fix. Never fix a bug without one — that's how it comes back.

## Final rule

```
Production code → a test exists and failed first
Otherwise → not TDD
```

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `test-driven-development` skill (MIT), iron law and rationalization table preserved near-verbatim.
