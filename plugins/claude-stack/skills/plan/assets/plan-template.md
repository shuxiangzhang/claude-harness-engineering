# Implementation Plan: [FEATURE]

**Feature Directory**: `specs/[NNN-short-name]` | **Date**: [DATE] | **Spec**: [spec.md](spec.md)

## Summary

[Primary requirement from the spec + the chosen technical approach, 2–4 sentences]

## Technical Context

**Language/Version**: [e.g. Python 3.12, TypeScript 5.x — or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g. FastAPI, React 19 — or NEEDS CLARIFICATION]
**Storage**: [e.g. PostgreSQL, files, N/A]
**Testing**: [e.g. pytest, vitest — or NEEDS CLARIFICATION]
**Target Platform**: [e.g. Linux server, browser, iOS 17+]
**Project Type**: [library / CLI / web service / app — drives structure below]
**Performance Goals**: [domain-specific, e.g. 1000 req/s, 60 fps — or NEEDS CLARIFICATION]
**Constraints**: [e.g. <200ms p95, offline-capable, <100MB memory]
**Scale/Scope**: [e.g. 10k users, 50 screens, 1M LOC]

## Constitution Check

*GATE: must pass before Phase 0 research; re-checked after Phase 1 design.*

[One line per constitution principle: PASS, or VIOLATION → justified in Complexity
Tracking below / requires redesign. If no constitution exists, state that.]

## Project Structure

### Documentation (this feature)

```text
specs/[NNN-short-name]/
├── spec.md         # specify output
├── plan.md         # this file
├── research.md     # Phase 0 output
├── data-model.md   # Phase 1 output (if data involved)
├── quickstart.md   # Phase 1 output
├── contracts/      # Phase 1 output (if interfaces exposed)
├── checklists/     # quality gates (implement stops to confirm if any are incomplete)
└── tasks.md        # tasks output (NOT created by plan)
```

### Source code (repository root)

```text
[Concrete layout for THIS feature with real paths — delete this placeholder.
Single project default: src/ + tests/. Web app: backend/ + frontend/. Document
the chosen structure; no option labels may remain in the delivered plan.]
```

**Structure Decision**: [selected structure and why]

## Complexity Tracking

> Fill ONLY if the Constitution Check has violations that must be justified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| [e.g. 4th project] | [current need] | [why 3 projects are insufficient] |
