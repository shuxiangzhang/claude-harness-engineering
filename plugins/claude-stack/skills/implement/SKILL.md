---
name: implement
description: Use when executing a feature's tasks.md — phrases like "implement the plan", "execute the tasks", "build it". Checklist-gated, phase-by-phase execution with a fresh subagent per task and two-stage review (spec compliance, then code quality).
---

# implement

## Overview

Execute `FEATURE_DIR/tasks.md` with two quality mechanisms fused:

1. **Gates** (spec-kit): incomplete checklists HALT entry; phases complete in order; checkpoints validate each story.
2. **Fresh subagent per task + two-stage review** (superpowers): an implementer subagent does the task; a spec-compliance reviewer verifies it matches the requirement; a code-quality reviewer verifies it's well built. Spec issues are fixed **before** quality review — code beauty must not hide misalignment.

## Entry gates — check before any execution

1. **Checklists**: scan `FEATURE_DIR/checklists/*.md`, count `- [ ]` vs `- [x]` per file, show the status table. **Any incomplete checklist → STOP** and ask: "Some checklists are incomplete. Proceed anyway?" Only an explicit yes continues.
2. **Branch**: never start on main/master without explicit user consent — offer a feature branch or worktree.
3. **Context**: read `tasks.md` and `plan.md` fully (required); `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, constitution as available. Extract every task's **full text** up front — subagents receive text, they never re-read the plan.

## Per-task loop

For each task, in phase order (Setup → Foundational → stories by priority → Polish), respecting `[P]`/same-file rules:

1. **Dispatch the implementer** — fresh subagent via the Agent tool, prompt per [references/implementer-prompt.md](references/implementer-prompt.md): full task text + scene-setting context + invitation to ask questions first. Answer questions before letting it proceed.
2. **Spec-compliance review** — fresh subagent per [references/spec-reviewer-prompt.md](references/spec-reviewer-prompt.md). Core stance: **do not trust the implementer's report; read the code**. Finds missing requirements, unrequested extras, misunderstandings. Issues → implementer fixes → **re-review**. Loop until ✅.
3. **Code-quality review** — only after spec ✅. Fresh subagent per [references/quality-reviewer-prompt.md](references/quality-reviewer-prompt.md) on the task's diff (base/head SHAs). Critical/Important issues → fix → re-review.
4. **Mark complete** — tick `[x]` in tasks.md, update the task tracker, report one-line progress.

**Story checkpoints**: at each story's checkpoint line, run that story's independent test from the spec. A story that doesn't independently work doesn't pass its checkpoint — stop and fix before the next story.

**Failure handling**: a failed non-parallel task halts the run (report context + next steps). A subagent that fails its task gets a fresh fix-subagent with specific instructions — don't patch its work yourself in the controller context.

## After all tasks

- Dispatch one final reviewer over the whole implementation against spec + plan
- Verify success criteria from the spec; run `quickstart.md` scenarios if present
- Hand off: **REQUIRED** → `verify-done` for evidence-based completion claims, then `finish-branch` to merge/PR/cleanup

## Red flags — never

- Skip either review stage, or run quality review before spec review passes
- Proceed with unfixed reviewer findings, or accept "close enough" on spec compliance
- Dispatch parallel implementers onto the same file
- Make a subagent read the plan file instead of receiving full task text
- Move to the next task while either review has open issues
- Trust an agent's "success" without the reviewer reading the code

## Lineage

Checklist gate and phase discipline from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.implement`; subagent-per-task with two-stage review from [obra/superpowers](https://github.com/obra/superpowers)' `subagent-driven-development` (both MIT).
