---
name: specify
description: Use when turning a feature idea or validated design into a formal specification — phrases like "write a spec for", "spec this feature out", "formalize these requirements". Creates `specs/<NNN>-<slug>/spec.md` with prioritized user stories, testable requirements, measurable success criteria, and a quality checklist.
---

# specify

## Overview

Produce a specification that describes **WHAT users need and WHY** — never HOW. No tech stack, no APIs, no code structure. Written so a non-technical stakeholder could read it, and so every requirement is testable.

## Workflow

### 1. Resolve the feature directory

- Derive a 2–4 word short name from the description, action-noun format (e.g. `user-auth`, `fix-payment-timeout`)
- Scan `specs/` for the next available 3-digit number → `specs/NNN-<short-name>/`
- Create the directory; record it in `.claude/memory/active-feature.json` as `{"feature_directory": "specs/NNN-<short-name>"}` so downstream skills (`clarify`, `plan`, `tasks`, `analyze`, `implement`) can find it
- If a brainstorm design doc exists for this feature, copy it in as `design.md`

### 2. Write the spec

Read [assets/spec-template.md](assets/spec-template.md) (bundled with this skill) and instantiate it at `FEATURE_DIR/spec.md`. If `.claude/memory/constitution.md` exists, load it — the spec must not contradict a principle. Rules that matter:

- **User stories are prioritized journeys** (P1, P2, P3…), each **independently testable** — implementing only P1 must still yield a viable MVP. Each story gets: why this priority, an independent test, Given/When/Then acceptance scenarios.
- **Functional requirements are numbered** (FR-001…) and each must be testable.
- **Make informed guesses** for gaps using context and industry standards; record them under Assumptions. Reserve `[NEEDS CLARIFICATION: question]` markers for decisions that genuinely block: significant scope/UX impact, multiple reasonable interpretations, no sane default. **Maximum 3 markers** — prioritize by scope > security/privacy > UX > technical.
- **Success criteria are measurable and technology-agnostic.** Good: "users complete checkout in under 3 minutes", "95% of searches return in under 1 second". Bad: "API responds in 200ms", "Redis hit rate above 80%" (implementation detail).
- Remove inapplicable sections entirely; don't leave "N/A".

### 3. Generate the quality checklist

Create `FEATURE_DIR/checklists/requirements.md` from [assets/requirements-checklist.md](assets/requirements-checklist.md). Then validate the spec against every item:

- All pass → done
- Items fail (other than clarification markers) → fix the spec, re-validate (max 3 iterations; then document what's still failing and warn)
- `[NEEDS CLARIFICATION]` markers remain → present each as a question with 2–3 suggested answers and implications (AskUserQuestion fits this). Replace each marker with the chosen answer, then re-validate.

### 4. Report

Feature directory, spec path, checklist pass count, and the recommended next step: `clarify` (recommended when any ambiguity was guessed around) or `plan`.

## Do not

- Do not include implementation details — every leaked framework name fails the checklist
- Do not exceed 3 clarification markers; guess-and-document is the default posture
- Do not create more than one feature directory per invocation
- Do not embed extra checklists inside the spec itself

## Next

→ `clarify` to systematically de-risk ambiguity, or `plan` if the spec is clean.

## Lineage

Distilled from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.specify` command, spec template, and checklist mechanism (MIT).
