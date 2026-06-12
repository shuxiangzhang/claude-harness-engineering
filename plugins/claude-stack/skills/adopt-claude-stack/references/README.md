# Reference examples

These are the verbatim worked examples from Anubhav's article *"I Spent 6 Months Tuning Claude Code"*, bundled inside this skill so it stays self-contained when packaged as a `.skill` file.

The article uses a single fictional repo throughout — `citation-rag`, a LangGraph-based retrieval + answer-generation service with a Postgres+pgvector retriever, Gemini answer generation, and an eval harness. Every example below comes from that repo.

Read whichever reference matches the step you're working on. The main `SKILL.md` points at these files by name where relevant.

## Index

| File | Article layer | What it shows |
|---|---|---|
| [`example-tree.md`](example-tree.md) | The whole stack | The directory layout a tuned repo produces |
| [`example-claude-md.md`](example-claude-md.md) | Layer 1 — Memory | The full citation-rag `CLAUDE.md` |
| [`example-path-scoped-rule.md`](example-path-scoped-rule.md) | Layer 2 — Path-scoped rules | `.claude/rules/retrieval.md` for `services/retrieval/**` |
| [`example-subagent.md`](example-subagent.md) | Layer 4 — Subagents | The `retrieval-reviewer` subagent definition |
| [`example-skill.md`](example-skill.md) | Layer 5 — Skills | The `new-rag-eval` project-level skill |
| [`example-settings-json.md`](example-settings-json.md) | Layer 6 — Hooks | `settings.json` with formatter + push gate + audit |
| [`example-push-gate.sh`](example-push-gate.sh) | Layer 6 — Hooks | The `gate_git_push.sh` deferred-permission script |
| [`example-mcp-json.md`](example-mcp-json.md) | Layer 7 — MCP | The full 5-server `.mcp.json` (mature config) |
| [`example-github-actions.yml`](example-github-actions.yml) | Layer 8 — Headless | Nightly-eval GitHub Actions workflow |
| [`example-replay.md`](example-replay.md) | End-to-end | The 90-minute "replay" walkthrough with planner output, reviewer verdict, eval JSON |

## When to use these

- During adoption (Step 3 of the main workflow), point the user at `example-claude-md.md` so they can see the target shape.
- When writing a path-scoped rule (Step 4), pattern-match against `example-path-scoped-rule.md`.
- When seeding the empty-subdirectory READMEs (Step 9), copy the relevant example into each README so the user has a working template right next to where it goes.
- When the user later asks "how do I add a subagent / skill / nightly run?", point at the matching reference.

These examples are deliberately concrete. They're easier to adapt than to invent.
