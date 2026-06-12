---
name: clarify
description: Use after a spec exists but before planning, when requirements may be ambiguous or underspecified — phrases like "clarify the spec", "de-risk the requirements", "anything unclear in the spec?". Asks up to 5 targeted questions and encodes every answer directly back into the spec file.
---

# clarify

## Overview

Detect and reduce ambiguity in the active feature spec, recording each resolution **in the spec itself** — not in chat history that evaporates. Expected to run before `plan`; skipping it is allowed but warn that downstream rework risk increases.

## Workflow

### 1. Locate the spec

Read `.claude/memory/active-feature.json` for the feature directory; fall back to the most recently modified `specs/*/` dir; if neither, ask. Spec missing → tell the user to run `specify` first; never create a spec here. Load `.claude/memory/constitution.md` if it exists.

### 2. Ambiguity scan

Score the spec against this taxonomy, marking each category **Clear / Partial / Missing** (internal map — output only if no questions result):

| Category | Looking for |
|---|---|
| Functional scope & behavior | core goals, out-of-scope declarations, user roles |
| Domain & data model | entities, identity rules, lifecycle/state, scale assumptions |
| Interaction & UX flow | critical journeys, error/empty/loading states, accessibility |
| Non-functional qualities | latency/throughput targets, reliability, observability, security/privacy, compliance |
| Integration & dependencies | external services and failure modes, formats, versioning |
| Edge cases & failure handling | negative scenarios, rate limits, conflict resolution |
| Constraints & tradeoffs | technical constraints, rejected alternatives |
| Terminology | canonical terms, drifting synonyms |
| Completion signals | testable acceptance criteria, measurable done-ness |
| Placeholders | TODOs, unresolved decisions, vague adjectives ("robust", "intuitive") |

### 3. Question queue (max 5)

Build a prioritized queue by **Impact × Uncertainty**. Only include questions whose answers materially change architecture, data modeling, task decomposition, test design, UX behavior, or compliance. Each must be answerable as multiple-choice (2–5 options) or a ≤5-word answer.

### 4. Ask — one at a time

- Exactly one question per turn; never reveal the queue
- Always present **your recommended option first with 1–2 sentences of reasoning** (AskUserQuestion's recommended-option pattern fits exactly)
- After each answer, integrate immediately (step 5) before asking the next
- Stop early when: critical ambiguities resolved, user signals "done"/"proceed", or 5 questions asked
- No meaningful ambiguities at all → report "No critical ambiguities detected" and suggest `plan`

### 5. Integrate each answer immediately

- Ensure a `## Clarifications` section with `### Session YYYY-MM-DD` exists; append `- Q: <question> → A: <answer>`
- Then apply the answer to the right section: functional ambiguity → Functional Requirements; data shape → Key Entities; vague adjective → a measurable Success Criterion; negative flow → Edge Cases; terminology → normalize the term everywhere
- **Replace** the ambiguous statement; leave no contradictory text behind
- Save the spec after each integration

### 6. Re-validate and report

Re-check `FEATURE_DIR/checklists/requirements.md` if it exists, toggling only checkboxes whose state actually changed. Report: questions asked, sections touched, checklist before/after (e.g. "12/16 → 15/16"), coverage summary (Resolved / Deferred / Clear / Outstanding), and the next step — `plan`, or another `clarify` pass if high-impact categories were deferred by the quota.

## Do not

- Do not exceed 5 questions (disambiguation retries don't count as new)
- Do not ask speculative tech-stack questions — that's `plan`'s territory
- Do not batch questions or dump the whole queue
- Do not record answers only in chat — the spec file is the single source of truth

## Lineage

Distilled from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.clarify` command, including its ambiguity taxonomy (MIT).
