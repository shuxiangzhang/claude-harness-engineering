---
name: analyze
description: Use after tasks.md exists and before implementation begins — phrases like "check the artifacts for consistency", "analyze the spec/plan/tasks", "anything contradictory before we build?". Read-only cross-artifact audit producing severity-ranked findings; never modifies files.
---

# analyze

## Overview

A **strictly read-only** consistency and quality audit across `spec.md`, `plan.md`, and `tasks.md` before implementation. Catches the failure modes that survive each artifact individually: requirements with zero tasks, terminology drift, constitution conflicts, vague adjectives posing as requirements.

**Constitution authority:** `.claude/memory/constitution.md` is non-negotiable here. Conflicts with a MUST principle are automatically **CRITICAL** and require fixing the spec/plan/tasks — never diluting the principle. Changing a principle happens in `constitution`, explicitly.

## Workflow

### 1. Load artifacts

Feature directory from `.claude/memory/active-feature.json` (usual fallbacks). All three of spec/plan/tasks required — abort with the missing prerequisite named. Load each selectively: requirements/stories/success criteria from the spec; stack/structure/phases from the plan; IDs/descriptions/paths from tasks; principles from the constitution.

### 2. Build the inventory

- **Requirements inventory**: every FR-### and SC-### (include only SC items needing buildable work — exclude post-launch KPIs)
- **Story inventory**: user stories + acceptance criteria
- **Coverage map**: task → requirement(s)/story, by explicit reference or keyword inference
- **Constitution rule set**: MUST/SHOULD statements

### 3. Detection passes

| Pass | Looking for |
|---|---|
| A. Duplication | near-duplicate requirements; mark the weaker phrasing |
| B. Ambiguity | vague adjectives without measurable criteria; unresolved placeholders (TODO, ???, [NEEDS CLARIFICATION]) |
| C. Underspecification | requirements missing a measurable outcome; stories without acceptance alignment; tasks referencing components no artifact defines |
| D. Constitution | anything conflicting a MUST principle; mandated gates absent |
| E. Coverage gaps | requirements with zero tasks; tasks mapped to nothing |
| F. Inconsistency | terminology drift; entities in plan but not spec (or vice versa); task ordering contradicting dependencies; conflicting requirements |

Cap at 50 findings; aggregate the overflow into one summary row.

### 4. Severity

- **CRITICAL** — constitution MUST violation; missing core artifact; zero-coverage requirement blocking baseline functionality
- **HIGH** — duplicate/conflicting requirement; ambiguous security or performance attribute; untestable acceptance criterion
- **MEDIUM** — terminology drift; missing non-functional coverage; underspecified edge case
- **LOW** — wording/style; minor redundancy

### 5. Report (chat only — no file writes)

Findings table (`ID | Category | Severity | Location | Summary | Recommendation`), coverage summary (requirement → has task? → task IDs), constitution issues, unmapped tasks, metrics (totals, coverage %, counts by severity). Then **Next Actions**: CRITICAL present → resolve before `implement`, with the concrete edit each fix needs; only LOW/MEDIUM → may proceed. Offer: "Want concrete remediation edits for the top N issues?" — and apply them **only on explicit approval**.

## Do not

- Do not modify any file — this skill is read-only by contract
- Do not hallucinate missing sections; report absence accurately
- Do not soften constitution conflicts into suggestions
- Rerunning unchanged artifacts should yield consistent IDs and counts

## Lineage

Distilled from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.analyze` command (MIT).
