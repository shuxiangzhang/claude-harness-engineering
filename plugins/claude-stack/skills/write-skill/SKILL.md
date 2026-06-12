---
name: write-skill
description: Use when creating a new Claude Code skill, editing an existing one, or packaging a workflow that keeps repeating — in this plugin, in a project's .claude/skills/, or in ~/.claude/skills/.
---

# write-skill

## Overview

Writing skills is TDD applied to process documentation: pressure-test first (RED), write the minimal skill that fixes the observed failure (GREEN), close the loopholes agents find (REFACTOR).

**Core principle:** if you didn't watch an agent fail without the skill, you don't know whether the skill teaches the right thing.

## When to create a skill

Create: the technique wasn't obvious, it recurs across projects, others would benefit.
Don't create: one-off solutions, well-documented standard practice, project conventions (CLAUDE.md's job), anything enforceable by a regex/hook (automate instead — save documentation for judgment calls).

## RED — baseline first

Run a realistic pressure scenario with a subagent **without** the skill (time pressure, sunk cost, "just this once"). Record verbatim what it does wrong and which rationalizations it uses. No observed failure → you don't need the skill.

## GREEN — write the minimal skill

```
skill-name/
  SKILL.md          # required
  supporting-file   # only for heavy reference (100+ lines) or reusable tools
```

Frontmatter — `name` + `description` only:
- `name`: letters/numbers/hyphens; verb-first reads well (`writing-plans`, not `plan-authoring`)
- `description`: **triggering conditions ONLY, third person, "Use when…"** — never summarize the workflow. A description that summarizes the process becomes a shortcut: the agent follows the one-line summary and skips the skill body. (Superpowers measured exactly this failure.)
- Include searchable symptoms/keywords; keep under ~500 chars

Body: overview with the core principle → when to use → the technique → common mistakes. One excellent example beats five mediocre ones. Token discipline: assume the reader is already smart; cut everything they'd already know.

For discipline skills (rules under pressure), add the bulletproofing trio:
1. **Iron law** — one unmissable line in a code block
2. **Rationalization table** — every excuse from baseline testing, each with its reality
3. **Red flags list** — self-check phrases meaning "stop"
4. Plus the umbrella clause: *violating the letter is violating the spirit*

## REFACTOR — close loopholes

Re-run the pressure scenarios with the skill present. Agent complies → done. Agent finds a new rationalization → add the explicit counter, re-test. Repeat until bulletproof.

## Placement

- This plugin (`skills/`) — broadly useful across the kit's users
- Project `.claude/skills/` — ships with one repo
- `~/.claude/skills/` — personal, all projects

## Do not

- Deploy a skill whose baseline failure you never observed
- Summarize workflow in the description
- Batch-create several skills without testing each
- Write narrative war stories — skills are reference, not memoir

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `writing-skills` skill and its CSO (Claude Search Optimization) findings (MIT).
