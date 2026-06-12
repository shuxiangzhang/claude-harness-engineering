---
name: brainstorm
description: Use before any creative work — a new feature, component, behavior change, or "let's build X" — when intent and requirements are not yet pinned down. Turns a rough idea into a validated design through one-question-at-a-time dialogue, before any spec or code exists.
---

# brainstorm

## Overview

Turn ideas into validated designs through collaborative dialogue — **before** writing a spec, a plan, or code. The cost of a wrong assumption multiplies at every later stage; this is the cheapest place to kill it.

**Core principle:** one question at a time, incremental validation, YAGNI ruthlessly.

## The process

**Understand the context first.** Look at the current project state (files, docs, recent commits, CLAUDE.md, constitution if present) before asking anything — don't ask what the repo already answers.

**Refine the idea — one question per message.**
- Ask exactly one question at a time; if a topic needs more, split into multiple turns
- Prefer multiple-choice (use AskUserQuestion); open-ended is fine when options would mislead
- Focus on: purpose, users, constraints, success criteria, what's explicitly out of scope

**Explore approaches.** Propose 2–3 approaches with trade-offs. Lead with your recommendation and the reasoning. Let the user pick or push back.

**Present the design in sections.** Once you believe you understand it, present the design in 200–300-word sections, validating each before continuing. Cover: architecture, components, data flow, error handling, testing strategy. Go back when something doesn't land.

## After the design

1. **Write it down.** Save the validated design to `docs/designs/YYYY-MM-DD-<topic>.md`. Suggest committing it.
2. **Offer the handoff:**
   - **Formalize as a spec** → `specify` (the design doc becomes its input; the spec adds prioritized user stories, testable requirements, and measurable success criteria)
   - **Small/contained change** → skip the spec; go straight to `tasks` or just implement with `tdd`
3. If the user continues to `specify`, pass the design doc path so it lands in the feature directory as `design.md`.

## Key principles

- **One question at a time** — never a wall of questions
- **YAGNI ruthlessly** — strike speculative features from every design
- **Explore alternatives** — never present a single option as inevitable
- **Incremental validation** — present in sections, confirm each
- **Check the constitution** — if `.claude/memory/constitution.md` exists, designs must not contradict it; surface conflicts during the dialogue, not at plan time

## Do not

- Do not write code, specs, or task lists inside this skill — it produces a design document only
- Do not batch five questions into one message
- Do not skip context-gathering and ask the user things the repo states

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `brainstorming` skill (MIT).
