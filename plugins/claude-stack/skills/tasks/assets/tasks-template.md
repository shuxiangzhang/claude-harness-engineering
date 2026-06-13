# Tasks: [FEATURE NAME]

**Input**: Design documents from `specs/[NNN-short-name]/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/

**Format**: `- [ ] [ID] [P?] [Story?] Description with exact file path`
- **[P]** = parallelizable (different files, no dependency on an incomplete task)
- **[Story]** = which user story the task serves (US1, US2…) — story phases only

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create project structure per plan.md
- [ ] T002 Initialize project with dependencies in pyproject.toml
- [ ] T003 [P] Configure linting and formatting in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ No user story work may begin until this phase completes.**

- [ ] T004 Set up migrations framework in migrations/env.py
- [ ] T005 [P] Base models all stories depend on in src/models/base.py

**Checkpoint**: Foundation ready — story phases can begin

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [what this story delivers]
**Independent Test**: [how to verify this story on its own]

### Tests for User Story 1 (TDD — write first, observe failure)

- [ ] T010 [P] [US1] Write failing test for [behavior] in [tests/path/test_x.py]
- [ ] T011 [US1] Run the test and confirm it fails for the expected reason

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create [Entity] model in [src/models/entity.py]
- [ ] T013 [US1] Implement minimal [Service] in [src/services/service.py] to pass T010
- [ ] T014 [US1] Run the suite, confirm green, commit

**Checkpoint**: User Story 1 independently functional — this is the MVP

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

[...same shape: Goal, Independent Test, tests-first tasks, implementation tasks...]

**Checkpoint**: Stories 1 AND 2 both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Cleanup/refactor (keep tests green)
- [ ] TXXX Run quickstart.md validation end-to-end

---

## Dependencies & Execution Order

- Setup → Foundational → story phases (priority order; parallelizable across stories after Foundational) → Polish
- Within a story: tests → models → services → endpoints → integration
- Same file = sequential; `[P]` only across different files

## Implementation Strategy

MVP first: Setup + Foundational + User Story 1, then **STOP and VALIDATE** the
checkpoint before continuing. Each later story is an independent increment —
deliverable, demoable, revertible.
