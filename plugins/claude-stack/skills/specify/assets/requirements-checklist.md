# Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate specification completeness and quality before planning
**Created**: [DATE]
**Feature**: [link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Feature Readiness

- [ ] Every functional requirement maps to an acceptance criterion
- [ ] User scenarios cover the primary flows
- [ ] Constitution principles not contradicted (if `.claude/memory/constitution.md` exists)

## Notes

- Unchecked items require spec updates before `clarify` or `plan`
- The `implement` skill STOPS and asks for confirmation on any incomplete checklist in this directory
