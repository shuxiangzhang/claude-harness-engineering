# Example: custom subagent (Layer 4)

The article's `retrieval-reviewer` subagent. **Adoption deliberately does not install custom subagents on day one** — this reference lives in `.claude/agents/README.md` so the user has a working template when they later decide to add one.

## When to write a subagent

From the article:

> The tool ships with built-in subagents. The explore agent handles read-only codebase searches. The general-purpose agent handles multi-step work that needs a clean context. The code-reviewer and code-architect handle specialized roles.
>
> You write a custom subagent when you have a task you repeat frequently, when you need a role with specific tool restrictions, or when a specific system prompt conflicts with your main configuration.

## The full example

```markdown
---
name: retrieval-reviewer
description: Reviews changes under services/retrieval/ for chunking,
  reranker, and citation-contract regressions. Read-only. Invoke
  proactively before opening a PR that touches retrieval code.
tools: Read, Grep, Glob, Bash(git diff:*), Bash(uv run pytest:*)
model: sonnet
---
You are a retrieval-service reviewer for the citation-rag repo.

Scope:
- Only review files under `services/retrieval/**` and their tests.
- Do not comment on unrelated files even if they appear in the diff.

Review checklist, in order:
1. Chunking: does the change respect the 512/64 target, and does it keep
   `shared.chunking.semantic_chunker` as the single entry point?
2. Reranker: if the reranker interface changed, is every implementation
   updated, and is the top-k cap still ≤ 50?
3. Citations: every returned `Chunk` must have a `citation_id` produced
   by `shared.citations.make_citation_id`. Flag any hand-rolled ids.
4. Tests: no new network calls in unit tests. Integration tests gated
   by `pytest -m integration`.
5. Eval impact: if behavior changed, confirm `evals/snapshots/*.json`
   has been regenerated in the same commit.

Output format:
- A short "Verdict" (pass / needs-changes / blocker).
- Bullet list of findings, each with the file path and a one-line fix.
- Do not suggest unrelated refactors.
```

## What to notice in the frontmatter

From the article:

> Look at the frontmatter. The tools line is a narrow allowlist granting read access and scoped bash execution. The model line downshifts the agent to Sonnet. The main loop stays on the expensive model for the hard reasoning while the subagent runs cheaply in the background.

The three knobs:

- `tools:` — narrow allowlist. Read/Grep/Glob for code inspection, plus scoped Bash patterns (`Bash(git diff:*)`) so the agent can run specific commands without unrestricted shell access.
- `model:` — downshift cheap agents (review, audit, run-the-thing) to Sonnet. Keep the main loop on the expensive model.
- The system prompt body — explicit scope ("only review X, ignore Y"), a numbered checklist, and an output format.

## Adoption guidance

Don't install this during adoption. Instead, when the user later asks "how do I add a subagent?":

1. Identify the task they want to repeat.
2. Copy this file as a template into `.claude/agents/<name>.md`.
3. Rewrite the scope, checklist, and tool allowlist for their task.

The article's `prompt-auditor` and `eval-runner` are two other subagents from the same repo — same shape, different scope.
