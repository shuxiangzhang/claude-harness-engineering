# Implementer Subagent Prompt Template

Dispatch via the Agent tool (general-purpose). Provide the FULL task text — the subagent
must never need to open the plan.

```
You are implementing Task N: [task name]

## Task Description

[FULL TEXT of the task from tasks.md — pasted, not referenced]

## Context

[Scene-setting: where this fits in the feature, what's already built, key decisions
from plan.md/research.md that bear on this task, exact file paths involved]

## Before You Begin

If you have questions about the requirements, the approach, dependencies, or anything
unclear — **ask them now**, before writing code. While you work: if something
unexpected appears, pause and ask. Don't guess.

## Your Job

1. Implement exactly what the task specifies — nothing more (YAGNI)
2. Follow TDD where the task includes test steps: failing test observed first
3. Verify your work (run the tests/commands; read the output)
4. Commit with a clear message
5. Self-review (below), fixing what you find
6. Report back

## Self-Review Before Reporting

- Completeness: every requirement implemented? edge cases handled?
- Quality: names accurate? code clean and consistent with the codebase?
- Discipline: nothing built beyond the task? existing patterns followed?
- Testing: tests verify real behavior (not mocks)? failure observed before passing?

## Report Format

What you implemented · test results (actual output) · files changed ·
self-review findings · open concerns
```
