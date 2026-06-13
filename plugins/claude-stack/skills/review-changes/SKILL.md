---
name: review-changes
description: Use to review a diff, branch, or PR that was NOT produced by the implement loop — your own ad-hoc changes before committing, or someone else's pull request. Phrases like "review my changes", "review this diff/branch/PR", "look over this before I commit", "code review this". Two passes — intent/correctness, then quality — judged against the project's own constitution, path-scoped rules, and lessons. For changes the implement skill already produced, its built-in two-stage review covers it; this is the standalone entry point for everything else.
---

# review-changes

## Overview

Review changed code the way `implement`'s internal reviewers do — but on demand, against the *project's own* standards. The value over a generic review is that this one reads `.claude/memory/constitution.md`, the matching `.claude/rules/`, and `.claude/lessons/LESSONS.md` and treats them as the rubric.

**Core stance (from `implement`'s reviewers): do not trust the description — read the code.** A PR summary or commit message states intent; only the diff states reality.

## Scope the change first

Establish exactly what you are reviewing — never "the whole repo":

- Working-tree changes: `git diff` (unstaged) / `git diff --staged`.
- A branch: `git diff <base>...<head>` (three-dot = changes on head since it diverged).
- A PR: fetch it, then diff its base..head.

Read the full diff and the surrounding code it touches. Pull in the spec/ADR/issue the change claims to satisfy, if one exists.

## Two passes — in order

**Pass 1 — Intent & correctness** (does it do the right thing?)
- Does the change actually satisfy its stated goal (spec acceptance criteria / issue / ADR)? Missing requirements, unrequested extras, misread requirements.
- Correctness bugs: edge cases (empty, zero, negative, boundary), error paths, race conditions, off-by-one, wrong table/field/ID.
- Does it violate a **constitution** principle? That is a blocker, not a nit.
- Does it repeat a recorded **lesson**? Flag with the lesson link.

**Pass 2 — Quality** (is it well built?) — only after Pass 1 is clean enough to be worth it.
- Reuse/simplification: duplicated logic, an existing helper ignored, dead code, needless abstraction.
- Conventions: conformance to the matching `.claude/rules/` and surrounding code.
- Security/observability: unvalidated input, secrets/PII in logs, swallowed errors, missing terminal states.
- Tests: do they encode *why* the behaviour matters, and would they fail if the logic regressed?

## Output

A severity-ranked list — **Blocker / Important / Nit** — each with `file:line`, what's wrong, why it matters, and a concrete fix. Cite the constitution/rule/lesson when one applies. End with a one-line verdict (ship / fix-then-ship / rework). If asked to fix, apply the Blockers and Importants, then re-review the result; don't claim done without `verify-done`.

## Do not

- Do not review without scoping the diff first — "review the repo" is not a review.
- Do not trust the PR/commit description — read the code.
- Do not let style nits bury a Blocker — rank by severity.
- Do not fix and claim success without re-running the verification (`verify-done`).

## Lineage

The two-stage stance (spec/intent before quality, "read the code not the report") is the standalone form of the reviewer chain bundled in `implement` (`references/spec-reviewer-prompt.md`, `references/quality-reviewer-prompt.md`).
