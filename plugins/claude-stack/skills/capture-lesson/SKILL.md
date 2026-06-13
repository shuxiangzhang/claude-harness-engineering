---
name: capture-lesson
description: Use the moment a mistake is corrected — the user pushed back or said "don't do that again"/"remember this", a wrong assumption caused rework, or a bug slipped that a check would have caught. Records a durable lesson in .claude/lessons/ so the same mistake isn't repeated in a future session.
---

# capture-lesson

## Overview

A lesson is a **mistake you don't want to make twice**, written down where the next session will see it. This is project memory for failures — distinct from `CLAUDE.md` (standing conventions) and `.claude/rules/` (path-scoped style). Lessons are committed to git so the whole team (and every future agent) inherits them.

**Core principle:** capture the *correction*, not the event. A lesson nobody can act on next time is noise.

## When to capture

Capture when a genuine mistake surfaced **and** the fix carries forward:

- The user corrected you ("no, we always do X here", "that's the wrong table", "don't touch that")
- A wrong assumption caused rework (you guessed an API/path/convention and it was wrong)
- A bug slipped that a specific check would have caught
- Something was non-obvious and bit you — and would bite the next agent the same way

**Do NOT capture:**

- Routine facts the repo already states → that's `CLAUDE.md` or a path-scoped rule
- One-off context that won't recur
- Anything already covered by an existing lesson (update it instead — see Dedupe)
- Secrets, tokens, or PII — never

If you're unsure whether it's a lesson, ask: *"would stating this at the start of a future session have prevented the mistake?"* If no, it's not a lesson.

## Where lessons live

```
.claude/lessons/
├── LESSONS.md        # index — one line per lesson, loaded/skimmed at session start
└── <slug>.md         # one lesson per file
```

If `.claude/lessons/` doesn't exist (repo wasn't bootstrapped/adopted with this stack), create it with a short README, then proceed.

## How to capture

1. **Check for a duplicate first.** Skim `LESSONS.md`. If a lesson already covers this, **update that file** (sharpen it, add the new instance) rather than adding a near-duplicate.

2. **Write the lesson file** at `.claude/lessons/<YYYY-MM-DD>-<short-kebab-slug>.md`, following [assets/lesson-template.md](assets/lesson-template.md):

   ```markdown
   ---
   trigger: <the situation that should recall this — e.g. "editing Alembic migrations">
   date: <YYYY-MM-DD>
   category: <one of the categories below — or a new kebab-case mechanism if none fits>
   ---

   **Rule:** <the imperative instruction that prevents a repeat — written so a future agent can act on it without reading the rest>
   **Mistake:** <what went wrong — the actual wrong assumption or action>
   **Why:** <root cause / why it happened, so the rule isn't followed blindly>
   **Evidence:** <PR / commit / ticket, if any>
   ```

   Keep it to a few lines. A lesson is a postcard, not an essay. Record the *mechanism* ("assumed UTC day buckets"), never blame ("wrote a bad test").

3. **Add one row at the top of `LESSONS.md`** (newest first). Make it self-sufficient — a reader should be able to act on it without opening the entry file:

   ```markdown
   - [<the rule, imperative and actable>](<YYYY-MM-DD-slug>.md) — <category>; recall when <concrete trigger>
   ```

   The link text carries the rule; the trigger (file type, command, situation) is what a future session matches against, so keep it concrete. One line per row.

4. **Tell the user** what you captured, in one line, and that it's now in `.claude/lessons/` (and will be picked up next session).

## Categories

Tag each lesson with the *mechanism* that caused it. Prefer an existing category; add a new kebab-case one (with a one-line definition) only if none genuinely fits.

- **heuristic-over-deterministic** — guessed / pattern-matched / "looks right" when a deterministic mechanism existed (a parser, a real API call, a schema check, running the actual code).
- **overlooked-requirement** — a spec, `CLAUDE.md` rule, or ticket existed and was skipped or misread; record *why* it was missed.
- **wrong-assumption** — acted on an unverified belief about the code, environment, or data instead of checking.
- **insufficient-verification** — declared work done on evidence that couldn't prove it (mocked the thing under test, substring checks, lint not run).
- **scope-creep / process** — broke a workflow rule (stacked unrelated fixes, edited an applied migration, drive-by changes in a PR).

## Keeping the index small

`LESSONS.md` is skimmed (and hook-injected) every session, so each row is a standing context cost. A lesson is **active** only while it has a row there; entry files are permanent history and are never deleted. **Hard cap: 15 rows** — whoever would add row 16 first promotes, retires, or consolidates down to 14. Recency is not the criterion; keep the lessons most likely to recur and least covered by automated checks.

In order of preference:

1. **Promote path-scoped lessons out.** If a lesson only bites in one area (migrations, routes, prompts, tests), move its rule into the matching `.claude/rules/` file — those load only when editing matching paths, costing zero tokens otherwise. Remove the index row; note the promotion in the entry. This is the main pressure valve.
2. **Promote universal lessons up.** If it applies to every task, fold its rule into a Hard rule / convention in `CLAUDE.md`, remove the index row, note the promotion.
3. **Retire the obsoleted.** When a code or CI change makes the trap mechanically impossible (the formatter/linter now enforces it), remove the row and note why in the entry.
4. **Consolidate near-duplicates.** Merge entries teaching the same rule into one (multiple evidence links); keep one row.

## Recall — how lessons come back

- **Claude Code:** the `claude-stack` SessionStart hook injects `LESSONS.md` into each session automatically (when the file has entries).
- **Both platforms:** the project `CLAUDE.md` / `AGENTS.md` points here, so the index is loaded with the always-on context. Before non-trivial work, skim `LESSONS.md` and open any lesson whose trigger matches what you're about to do.

Recall is index-first: the one-liners are always cheap to carry; full lesson files load only when their trigger is relevant.

## Do not

- Do not capture a lesson without checking for an existing one to update (dedupe beats accretion); one entry per distinct mistake — if it recurs, sharpen the existing rule, don't add a twin
- Do not write essays — rule, mistake, why; done
- Do not let `LESSONS.md` grow without bound — at 15 rows, promote/retire/consolidate before adding more (see *Keeping the index small*)
- Do not put secrets/PII in a lesson (it's committed to git)
- Do not use lessons for standing conventions — those belong in `CLAUDE.md` or a path-scoped rule

## Lineage

The index + one-file-per-entry recall pattern mirrors the file-based memory model used by Claude Code itself; the discipline framing follows this kit's other skills.
