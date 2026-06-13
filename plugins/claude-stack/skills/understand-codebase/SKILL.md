---
name: understand-codebase
description: Use when you or the user need to understand an unfamiliar codebase (or unfamiliar area of a known one) before changing it — "explain this repo", "how does X work here", "where do I make a change for Y", "onboard me to this code", "walk me through the architecture". Read-only: maps structure, entry points, data flow, and key abstractions, and pinpoints where a change would go. Does not modify anything.
---

# understand-codebase

## Overview

Build an accurate mental model *before* editing, so the change lands in the right place and respects existing patterns. This is read-only reconnaissance — the output is understanding, not edits.

**Core principle:** read what's already written before re-deriving it. A wrong model produces a change in the wrong layer.

## Start from what's documented

Don't reverse-engineer facts the repo already states. In order:

1. `CLAUDE.md` (+ nested ones) — conventions, layout, guardrails.
2. `docs/architecture/ARCHITECTURE.md` — the high-level map, if it exists.
3. `docs/decisions/` — ADRs explain *why* the non-obvious choices are the way they are (check Status).
4. `README`, `docs/`, and the dependency manifest (stack + entry points).

If `ARCHITECTURE.md` is missing or stale, offer to seed/refresh it at the end (this is exactly what `bootstrap`/`adopt` create).

## Then map the code

Scope to the user's goal — don't boil the ocean. For breadth, dispatch read-only subagents (or the Explore agent) over different areas in parallel; you synthesize.

- **Structure:** top-level layout — where source, tests, config, and entry points live.
- **Entry points:** `main`/CLI, HTTP routes, job/worker entry, scheduled tasks — where execution begins.
- **The relevant flow:** for the user's goal, trace one path end to end (request → handler → service → data, or input → transform → output). Name what calls what.
- **Key abstractions:** the 3–7 types/modules everything else leans on; the shared utilities; the data model.
- **Conventions:** how this repo does errors, validation, tests — defer to `.claude/rules/` where present.

## Output

A concise map, not a file dump:

- **What it is** — one paragraph.
- **Shape** — the major components and how they connect (prose or ASCII).
- **For your goal** — "to do X, change `path/to/file.ext` (and `…`); follow the pattern in `<existing example>`; watch out for `<gotcha>`."
- **Open questions** — anything the code couldn't answer (ask the user, don't guess).

## Do not

- Do not modify files — this skill is read-only. Hand off to `tdd`/`refactor`/the feature loop to make changes.
- Do not re-derive what `CLAUDE.md`/`ARCHITECTURE.md`/ADRs already state — read them first.
- Do not present an exhaustive file listing as "understanding" — synthesize the model and where to act.
- Do not guess at intent where the code is ambiguous — list it as an open question.
