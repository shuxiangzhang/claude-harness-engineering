---
name: plan
description: Use when a feature spec is ready and the technical design is the next step — phrases like "plan the implementation", "design this feature", "how do we build the spec". Produces plan.md (with a constitution gate), research.md, data-model.md, and contracts in the feature directory.
---

# plan

## Overview

Translate the spec's WHAT into a technical HOW: stack decisions, structure, data model, contracts. The plan is also where the **constitution gate** lives — violations either get justified in writing or the design changes.

## Workflow

### 1. Load context

Feature directory from `.claude/memory/active-feature.json` (fallbacks: most recent `specs/*/`, then ask). Read `spec.md` fully. Read `.claude/memory/constitution.md` — **required**: if it is missing, stop and run the `constitution` skill to establish the project's principles first, then resume. The design gate below is not optional. Unresolved `[NEEDS CLARIFICATION]` markers in the spec → stop and send the user to `clarify` first.

### 2. Instantiate the plan

Read [assets/plan-template.md](assets/plan-template.md) (bundled) and create `FEATURE_DIR/plan.md`:

- **Technical Context** — language/version, primary dependencies, storage, testing, target platform, project type, performance goals, constraints, scale. Mark genuine unknowns `NEEDS CLARIFICATION` — they become research tasks, not guesses.
- **Constitution Check (GATE)** — evaluate every constitution principle against the intended approach. A MUST violation is an ERROR: either redesign, or record it in **Complexity Tracking** with why it's needed and why the simpler alternative fails. An unjustified violation blocks the plan. The constitution is required — the entry check guarantees one exists, so this gate always runs.
- **Project Structure** — the concrete directory layout this feature will create/touch, with real paths. Delete unused layout options from the template.

### 3. Phase 0 — Research

For each `NEEDS CLARIFICATION` in Technical Context and each major dependency choice: research it (subagents fan out well here — one per unknown). Consolidate into `FEATURE_DIR/research.md` as **Decision / Rationale / Alternatives considered** entries. Phase 0 is done only when every unknown is resolved.

### 4. Phase 1 — Design artifacts

- `data-model.md` — entities from the spec: fields, relationships, validation rules, state transitions. Skip if the feature has no data.
- `contracts/` — the interfaces this feature exposes: API endpoints, CLI command schemas, public function signatures, event formats. Skip for purely internal work.
- `quickstart.md` — runnable validation scenarios proving the feature end-to-end: prerequisites, commands, expected outcomes. A validation guide, not an implementation dump.

### 5. Re-check the gate

Re-evaluate the Constitution Check against the **completed** design. New violations → justify or redesign. Then report: plan path, artifacts generated, gate result, and the next step (`tasks`).

## Do not

- Do not plan over unresolved spec clarifications — garbage in, confident garbage out
- Do not dilute or reinterpret a constitution principle to pass the gate — amend the constitution explicitly (via `constitution`) or change the design
- Do not write tasks here (that's `tasks`) or production code (that's `implement`)
- Do not leave template option labels or placeholders in the delivered plan

## Next

→ `tasks` to decompose into an executable, story-grouped task list.

## Lineage

Distilled from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.plan` command and plan template (MIT).
