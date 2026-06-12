---
name: tasks
description: Use when a feature plan exists and needs decomposing into an executable task list — phrases like "break this into tasks", "generate the task list", "what's the work breakdown". Produces a dependency-ordered, story-grouped tasks.md where every task names exact file paths.
---

# tasks

## Overview

Generate `FEATURE_DIR/tasks.md`: tasks grouped **by user story** so each story is an independently implementable, independently testable increment — and sized so an engineer with zero context (or a fresh subagent) can execute any single task without reading anything else.

**Granularity rule (the fusion):** every task is one action of roughly 2–5 minutes — "write the failing test for X in tests/foo_test.py", "implement minimal X in src/foo.py", "run the suite and confirm green". If a task description needs the word "and" twice, split it.

## Workflow

### 1. Load design documents

Feature directory from `.claude/memory/active-feature.json` (fallbacks as usual). Required: `plan.md` (stack, structure), `spec.md` (stories + priorities). Optional: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`. Constitution if present. Missing plan → send the user to `plan`.

### 2. Generate the task list

Read [assets/tasks-template.md](assets/tasks-template.md) (bundled) and instantiate at `FEATURE_DIR/tasks.md`.

**The checklist format is non-negotiable** — every task line:

```text
- [ ] [ID] [P?] [Story?] Description with exact file path
```

- **ID**: sequential in execution order (T001, T002…)
- **[P]**: only if parallelizable — different files, no dependency on an incomplete task
- **[Story]**: `[US1]`, `[US2]`… on user-story-phase tasks only (setup/foundational/polish tasks carry none)
- ✅ `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ❌ `- [ ] Create User model` (no ID, no story, no path)

**Phase structure:**
1. **Setup** — project init, tooling
2. **Foundational** — blocking prerequisites; **no story work may start before this completes**
3. **One phase per user story, in priority order** — each with goal, independent-test criterion, and a **Checkpoint** line ("Story N independently functional")
4. **Polish** — cross-cutting concerns

**Within a story**: tests before implementation (TDD — write failing test task, run-and-confirm-it-fails task, implement task, run-and-confirm-green task, commit task), models before services, services before endpoints.

**Mapping**: each contract → the story it serves; each entity → the story that needs it (shared → earliest story or Setup); every requirement traceable to ≥1 task — `analyze` will check this.

### 3. Validate and report

Confirm every line matches the format (checkbox, ID, labels, path). Report: total tasks, per-story counts, parallel opportunities, suggested MVP scope (usually User Story 1 alone), next step.

## Do not

- Do not write vague tasks ("add validation") — name the file and the behavior
- Do not create cross-story dependencies that break independent delivery
- Do not mark `[P]` on tasks touching the same file
- Do not start implementing — that's `implement`

## Next

→ `analyze` for a cross-artifact consistency check (recommended), or `implement` directly.

## Lineage

Format and story-phasing from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.tasks` (MIT); 2–5-minute granularity and zero-context executability from [obra/superpowers](https://github.com/obra/superpowers)' `writing-plans` (MIT).
