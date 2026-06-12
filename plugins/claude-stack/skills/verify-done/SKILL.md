---
name: verify-done
description: Use when about to claim work is complete, fixed, or passing — before committing, creating a PR, marking a task done, or expressing any satisfaction with the state of the work. Also use when reporting results from delegated subagents.
---

# verify-done

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If the verification command didn't run **in this message**, the claim cannot be made.

## The gate function

Before claiming any status or expressing any satisfaction:

1. **IDENTIFY** — what command proves this claim?
2. **RUN** — execute it, full and fresh (not a cached, partial, or earlier run)
3. **READ** — the complete output; exit code; count the failures
4. **VERIFY** — does the output actually support the claim?
   - No → state the actual status, with the evidence
   - Yes → state the claim, with the evidence
5. **Only then** — make the claim

Skipping any step is lying, not verifying.

## What each claim requires

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| "Tests pass" | test run output: 0 failures | a previous run; "should pass" |
| "Linter clean" | linter output: 0 errors | a partial check; extrapolation |
| "Build succeeds" | build exit 0 | linter passing; "logs look fine" |
| "Bug fixed" | the original symptom re-tested: gone | code changed, fix assumed |
| "Regression test works" | red-green verified: revert fix → test FAILS → restore → passes | test passing once |
| "Subagent completed it" | the diff inspected, changes verified | the agent's "success" report |
| "Requirements met" | line-by-line checklist against the spec | "tests pass" |

## Red flags — STOP

- "should", "probably", "seems to", "looks correct"
- Satisfaction before verification: "Done!", "Great!", "Perfect!"
- About to commit/push/PR without running the verification
- Trusting a subagent's success report without reading its diff
- Tired and wanting the work to be over
- **Any wording implying success without a fresh run behind it**

## Rationalization prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification. |
| "I'm confident" | Confidence ≠ evidence. |
| "Just this once" | No exceptions. |
| "Linter passed" | The linter is not the compiler, and neither is the test suite. |
| "The agent said success" | Verify independently. |
| "Partial check is enough" | Partial proves nothing about the rest. |
| "Different words, so the rule doesn't apply" | Spirit over letter. The rule covers paraphrases and implications. |

## The bottom line

Run the command. Read the output. **Then** claim the result. Non-negotiable.

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `verification-before-completion` skill (MIT), gate function and tables preserved near-verbatim.
