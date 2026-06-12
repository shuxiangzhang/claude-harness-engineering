# Code-Quality Reviewer Prompt Template

Purpose: verify the implementation is **well built** — clean, tested, maintainable.
Only dispatch after spec compliance is ✅. Always re-dispatch after fixes.

```
You are reviewing code quality for Task N: [task name]

## Scope

- WHAT WAS IMPLEMENTED: [from implementer's report, post spec-review]
- REQUIREMENTS: [task text reference]
- DIFF: [BASE_SHA]..[HEAD_SHA] — review the actual diff, not the description

## Review For

- **Correctness risks**: edge cases, error handling, concurrency, resource leaks
- **Tests**: do they verify real behavior (would they fail if the logic broke)?
  any mock-testing-the-mock patterns? anything skipped?
- **Maintainability**: naming, duplication (could this reuse existing code?),
  magic values, single-responsibility
- **Consistency**: does it match the codebase's existing patterns and the
  project constitution (if present)?

## Report

- Strengths (brief)
- Issues, each tagged Critical / Important / Minor, with file:line and a
  concrete suggested fix
- Assessment: ✅ Approved, or ❌ fix Critical/Important issues and re-review
```
