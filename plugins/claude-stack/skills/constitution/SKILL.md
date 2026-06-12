---
name: constitution
description: Use when establishing or amending a project's non-negotiable engineering principles — phrases like "set up project principles", "create a constitution", "add a governance rule", "what are this project's iron rules". Creates or updates `.claude/memory/constitution.md`, which the plan and analyze skills enforce as a hard gate.
---

# constitution

## Overview

A constitution is the project's small set of **non-negotiable principles** — the rules that gate every plan and survive every refactor. It is not a style guide and not documentation: every principle must be declarative, testable, and worth blocking a plan over.

Downstream enforcement: `plan` runs a **Constitution Check gate** before design; `analyze` treats any conflict with a MUST principle as **CRITICAL**.

## File location

`.claude/memory/constitution.md` in the target project. Create the directory if missing.

## Workflow

1. **Load or initialize.** If `.claude/memory/constitution.md` exists, read it — you are amending, not replacing. If missing, instantiate the structure from [assets/constitution-template.md](assets/constitution-template.md) (bundled with this skill).

2. **Collect principles.** From user input first; otherwise derive candidates from repo evidence (README, CLAUDE.md, CI config, existing conventions) and confirm with the user. Keep it to 3–7 principles. Each principle gets:
   - A short name (e.g. `III. Test-First (NON-NEGOTIABLE)`)
   - A paragraph or bullets of non-negotiable rules using MUST/SHOULD precisely
   - A rationale if not obvious

   Vague language fails validation: "should write good tests" → rewrite as "TDD mandatory: tests written → fail observed → then implement".

3. **Version it (semver).**
   - MAJOR: principle removed or redefined incompatibly
   - MINOR: principle added or materially expanded
   - PATCH: clarification/wording
   Footer line: `**Version**: X.Y.Z | **Ratified**: YYYY-MM-DD | **Last Amended**: YYYY-MM-DD`. If the bump type is ambiguous, state your reasoning before finalizing.

4. **Propagate.** On amendment, check artifacts that reference the constitution: open feature plans (`specs/*/plan.md` Constitution Check sections) and the project CLAUDE.md if it cites principles. List what needs updating; don't silently rewrite committed plans.

5. **Report.** New version + bump rationale, principles changed, files flagged for follow-up, suggested commit message (e.g. `docs: amend constitution to vX.Y.Z`).

## Validation before writing

- No placeholder tokens remain
- Principles are declarative and testable, no unquantified adjectives
- Dates in ISO format; version line matches the report

## Do not

- Do not fabricate principles the user/repo never expressed — a constitution nobody believes in gates nothing
- Do not exceed ~7 principles; a long constitution is a style guide wearing a costume
- Do not weaken a principle to make a plan pass — that adjustment happens here, explicitly, never inside `plan` or `analyze`

## Next

- New project, no spec yet → `brainstorm` or `specify`
- Constitution amended mid-feature → re-run `analyze` on the active feature

## Lineage

Distilled from [github/spec-kit](https://github.com/github/spec-kit)'s `/speckit.constitution` command and constitution template (MIT).
