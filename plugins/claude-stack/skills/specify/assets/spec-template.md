# Feature Specification: [FEATURE NAME]

**Feature Directory**: `specs/[NNN-short-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: [one-line user description, or link to design.md from brainstorm]

## User Scenarios & Testing *(mandatory)*

<!-- User stories are PRIORITIZED user journeys. Each must be INDEPENDENTLY TESTABLE —
implementing only User Story 1 must still produce a viable MVP. -->

### User Story 1 - [Brief Title] (Priority: P1)

[The journey in plain language]

**Why this priority**: [value and why it outranks the others]

**Independent Test**: [how this story is verified on its own, delivering its own value]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[...same shape...]

---

### Edge Cases

- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific, testable capability]
- **FR-002**: System MUST [specific, testable capability]
- **FR-003**: Users MUST be able to [key interaction]

<!-- Marking genuinely blocking unknowns (max 3 total):
- **FR-004**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method — email/password, SSO, OAuth?] -->

### Key Entities *(include only if the feature involves data)*

- **[Entity]**: [what it represents, key attributes — no implementation]

## Success Criteria *(mandatory)*

<!-- Measurable, technology-agnostic, user/business-focused, verifiable without
knowing the implementation. -->

- **SC-001**: [e.g. "Users can complete account creation in under 2 minutes"]
- **SC-002**: [e.g. "System handles 1,000 concurrent users without degradation"]
- **SC-003**: [e.g. "90% of users complete the primary task on first attempt"]

## Assumptions

- [Reasonable default chosen where the description was silent, e.g. "Standard session-based auth; revisit if SSO is required"]
- [Scope boundary, e.g. "Mobile is out of scope for v1"]

## Clarifications
<!-- Added by the clarify skill; leave absent until then. -->
