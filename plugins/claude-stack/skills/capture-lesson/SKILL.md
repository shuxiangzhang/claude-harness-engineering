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

2. **Write the lesson file** at `.claude/lessons/<short-kebab-slug>.md`, following [assets/lesson-template.md](assets/lesson-template.md):

   ```markdown
   ---
   trigger: <the situation that should recall this — e.g. "editing Alembic migrations">
   date: <YYYY-MM-DD>
   ---

   **Mistake:** <what went wrong — the actual wrong assumption or action>
   **Correction:** <the right approach, concretely>
   **Why:** <root cause / why it matters, so the rule isn't followed blindly>
   ```

   Keep it to a few lines. A lesson is a postcard, not an essay.

3. **Add one line to `LESSONS.md`**:

   ```markdown
   - [<short title>](<slug>.md) — <trigger phrase>
   ```

   The trigger phrase is what a future session matches against, so make it concrete (the file type, command, or situation), not abstract.

4. **Tell the user** what you captured, in one line, and that it's now in `.claude/lessons/` (and will be picked up next session).

## Recall — how lessons come back

- **Claude Code:** the `claude-stack` SessionStart hook injects `LESSONS.md` into each session automatically (when the file has entries).
- **Both platforms:** the project `CLAUDE.md` / `AGENTS.md` points here, so the index is loaded with the always-on context. Before non-trivial work, skim `LESSONS.md` and open any lesson whose trigger matches what you're about to do.

Recall is index-first: the one-liners are always cheap to carry; full lesson files load only when their trigger is relevant.

## Do not

- Do not capture a lesson without checking for an existing one to update (dedupe beats accretion)
- Do not write essays — trigger, mistake, correction, why; done
- Do not put secrets/PII in a lesson (it's committed to git)
- Do not use lessons for standing conventions — those belong in `CLAUDE.md` or a path-scoped rule

## Lineage

The index + one-file-per-entry recall pattern mirrors the file-based memory model used by Claude Code itself; the discipline framing follows this kit's other skills.
