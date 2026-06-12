---
name: using-claude-stack
description: Use when starting any conversation or coding task with the claude-stack skills available (Claude Code or Codex) — the routing map for which skill applies at each stage of the development lifecycle.
---

# Using claude-stack

If there is even a **1% chance** a skill below applies to what you are doing, invoke it before responding or acting. If an invoked skill turns out wrong for the situation, you may set it aside — but the check comes first, even before clarifying questions.

**Invoking a skill:** Claude Code — the Skill tool, or `/claude-stack:<name>`; Codex — mention the skill by name, or let its description auto-match. Either way, read the skill's body and follow it; don't just act on this one-line routing entry.

## Routing map

| Situation | Skill |
|---|---|
| New empty project, configure Claude Code | `bootstrap-claude-stack` |
| Existing repo, configure Claude Code | `adopt-claude-stack` |
| Establish/amend project principles | `constitution` |
| New feature idea, requirements fuzzy | `brainstorm` |
| Idea/design ready → formal spec | `specify` |
| Spec has ambiguities | `clarify` |
| Spec ready → technical design | `plan` |
| Plan ready → task breakdown | `tasks` |
| Before building: artifact consistency audit | `analyze` |
| Execute the task list | `implement` |
| Writing ANY production code | `tdd` |
| Bug / test failure / unexpected behavior | `debug` |
| About to claim done / commit / PR | `verify-done` |
| Feature branch complete | `finish-branch` |
| A mistake was just corrected / "don't do that again" / "remember this" | `capture-lesson` |
| Pre-launch readiness audit | `production-readiness-assessor` |
| Package a repeated workflow as a skill | `write-skill` |

## Priority

**Process skills before implementation skills.** "Build X" → `brainstorm`/`specify` before code. "Fix Y" → `debug` before any fix. Discipline skills (`tdd`, `verify-done`) are rigid — follow exactly; do not adapt away the discipline.

## Red flags — you're rationalizing

"Just a simple question" (questions are tasks) · "I need context first" (the skill check comes first) · "the skill is overkill" (simple things become complex) · "I'll just do this one thing first" (check before doing) · "I know what that skill says" (skills evolve; invoke the current version).

User instructions say WHAT, not HOW — "add X quickly" does not mean skip the workflow.

## Lineage

Mechanism and 1%-rule from [obra/superpowers](https://github.com/obra/superpowers)' `using-superpowers` (MIT).
