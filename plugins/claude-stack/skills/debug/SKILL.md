---
name: debug
description: Use when encountering any bug, test failure, build break, or unexpected behavior, before proposing fixes. Especially under time pressure, when a "quick fix" seems obvious, or after previous fixes didn't hold.
---

# debug

## Overview

Random fixes waste time and create new bugs; quick patches mask root causes.

**Core principle:** find the root cause before attempting any fix. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Phase 1 incomplete → you may not propose fixes. This applies *especially* when in a hurry — systematic is faster than thrashing.

## The four phases — in order, no skipping

### Phase 1 — Root cause investigation

1. **Read the error completely.** Full stack trace, line numbers, codes. Errors often contain the answer.
2. **Reproduce reliably.** Exact steps; every time? If not reproducible, gather data — don't guess.
3. **Check recent changes.** `git diff`, recent commits, new dependencies, environment drift.
4. **Multi-component systems: instrument the boundaries.** Log what enters/exits each layer; run once; the evidence shows *which* layer breaks. Then investigate that layer — not the symptom's layer.
5. **Trace data flow backward.** Where does the bad value originate? Keep walking up the call chain to the source. Fix at the source, never at the symptom site.

### Phase 2 — Pattern analysis

Find working examples of the same pattern in this codebase. Read reference implementations **completely** — skimming guarantees partial understanding. List every difference between working and broken; don't dismiss "that can't matter".

### Phase 3 — Hypothesis and test

State one specific hypothesis: "X is the root cause because Y." Test it with the **smallest possible change** — one variable. Wrong? Form a new hypothesis; don't stack more changes on top. Don't know? Say "I don't understand X" and investigate — never pretend.

### Phase 4 — Implement the fix

1. **Failing test first** that reproduces the bug (per `tdd` — this is mandatory)
2. One fix, addressing the root cause. No "while I'm here" improvements.
3. Verify: that test passes, no others broke, the original symptom is gone (per `verify-done`).

### Phase 4.5 — Three strikes → question the architecture

If **3+ fixes have failed**, this is not a failed hypothesis — it's the wrong architecture. Symptoms: every fix surfaces a new problem elsewhere; fixes demand "massive refactoring"; shared state keeps reappearing. **Stop fixing. Discuss the design with the user before attempt #4.**

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, skip the process" | Simple issues have root causes too — the process is fast on them. |
| "Emergency — no time" | Guess-and-check is the slowest option. 15–30 min systematic beats 2–3 h thrashing. |
| "Just try this first, then investigate" | The first fix sets the pattern. Start right. |
| "Multiple changes at once saves time" | You can't isolate what worked — and you'll cause new bugs. |
| "I see the problem, let me fix it" | Seeing a symptom ≠ understanding the cause. |
| "One more attempt" (after 2+) | 3+ failures = architecture problem. Question the pattern. |

## Red flags — return to Phase 1

"Quick fix for now, investigate later" · "just change X and see" · proposing fixes before tracing data flow · "it's probably X" · "I don't fully understand it, but this might work" · listing fixes without investigation.

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `systematic-debugging` skill (MIT), including the four-phase structure and the 3-failures architecture rule.
