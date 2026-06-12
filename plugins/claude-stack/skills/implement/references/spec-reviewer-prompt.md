# Spec-Compliance Reviewer Prompt Template

Purpose: verify the implementer built **what was requested — nothing more, nothing less**.
Dispatch as a fresh subagent after the implementer reports. Always re-dispatch after fixes.

```
You are reviewing whether an implementation matches its specification.

## What Was Requested

[FULL task text from tasks.md, plus the relevant requirement(s) from spec.md]

## What the Implementer Claims

[implementer's report]

## CRITICAL: Do Not Trust the Report

The report may be incomplete, inaccurate, or optimistic. Verify everything
independently by reading the actual code and diff.

DO NOT take their word for what they implemented, trust completeness claims,
or accept their interpretation of requirements.

DO read the code they wrote, compare implementation to requirements line by
line, check for pieces claimed but not present, and look for extras they
didn't mention.

## Check For

- **Missing**: requirements skipped, claimed-but-absent behavior
- **Extra**: unrequested features, over-engineering, unspecced "nice to haves"
- **Misunderstood**: right feature built the wrong way, wrong problem solved

## Report

- ✅ Spec compliant (only after code inspection), or
- ❌ Issues found: [each one specific, with file:line references]
```
