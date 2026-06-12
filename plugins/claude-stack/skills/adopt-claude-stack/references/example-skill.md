# Example: project-level skill (Layer 5)

The article's `new-rag-eval` skill — a packaged workflow that adds a new eval case to the citation-rag eval harness. **Adoption deliberately does not install project-level skills on day one** — this reference lives in `.claude/skills/README.md` so the user has a working template when they later add one.

## Why progressive disclosure matters

From the article:

> Skills package a workflow so you can trigger it by name.
>
> A skill is a folder containing a markdown file with YAML frontmatter. It can bundle Python scripts, bash commands, and test fixtures.
>
> The architecture relies on progressive disclosure. The metadata loads at session start. The actual instructions load only when you trigger the skill. The bundled resources load only when the agent references them. This keeps your ambient token cost low even if you install fifty skills.

## The full example

```markdown
---
name: new-rag-eval
description: Support a new RAG eval case from a golden example, wire it
  into the eval harness, run it against the current pipeline, and write
  a result summary. Use when the user asks to "add an eval for ..."
  or "cover this regression with an eval."
allowed-tools: Read, Write, Edit, Bash(uv run:*), Bash(git add:*)
---
# new-rag-eval

## When to use
Trigger when the user wants to add a new eval case to
`evals/suites/citations/` or reproduce a regression in the eval harness.

## Inputs to gather first
1. A natural-language description of the query.
2. The expected citation ids (or the expected answer text).
3. Optional: the failing trace id from production.

## Steps
1. Read `evals/templates/case.json` — this is the case template.
2. Ask the user for the query, expected citations, and any notes.
3. Write a new case file at `evals/suites/citations/<slug>.json` using
   the template. Slug is kebab-case from the query.
4. Run the harness for just this case:
   `uv run python -m evals.run --suite citations --case <slug>`
5. Parse the JSON output at `evals/out/<slug>.json`. Summarize:
   - pass / fail
   - grounded-citation rate
   - unsupported-claim rate
   - any new latency outliers
6. If failing, add a short "why this is expected to fail today" note
   to the case file under `notes:`.
7. Stage the new case with `git add evals/suites/citations/<slug>.json`.

## Do not
- Do not edit `evals/templates/case.json`.
- Do not touch other eval suites.
- Do not open a PR from this skill. The PR flow lives in the
  `claude-pr-checklist` skill.
```

## What to notice

From the article:

> The allowed tools restrict the skill deterministically. It can run the evaluation script and stage files. It cannot push to production. It points the agent to a second skill for the pull request flow.

Key knobs in the frontmatter:

- `allowed-tools:` — narrow allowlist. Scoped Bash patterns (`Bash(uv run:*)`, `Bash(git add:*)`) restrict what the skill can shell out to.
- `description:` — *the* trigger mechanism. Include both what the skill does *and* the user phrases that should invoke it ("add an eval for...", "cover this regression").

Structural pattern in the body:

1. **When to use** — boundary conditions for the trigger.
2. **Inputs to gather first** — what the agent must collect before acting.
3. **Steps** — numbered, imperative, file-path-specific.
4. **Do not** — explicit out-of-scope behaviour. Especially valuable when adjacent skills exist.

## Adoption guidance

Don't install this during adoption. When the user later identifies a workflow stable enough to invoke by name:

1. Create `.claude/skills/<workflow-name>/SKILL.md`.
2. Use this file as a template.
3. Rewrite the steps for their workflow; tighten `allowed-tools:` to the minimum the workflow needs.

Note: project-level skills live in `.claude/skills/`. User-level skills (available across all projects) live in `~/.claude/skills/`. This `adopt-claude-stack` skill itself is a user-level skill.
