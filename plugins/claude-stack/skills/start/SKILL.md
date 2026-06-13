---
name: start
description: Use when the user is new to claude-stack or unsure how to drive it — phrases like "how do I use this", "where do I start", "what can claude-stack do", "help me get started", "what skills are available", "I just installed the plugin", "how does this work". Gives a plain-language tour of the development flow and the exact first thing to say for each common goal. This is the human-facing front door; `using-claude-stack` is its model-facing routing counterpart.
---

# start

You don't drive this harness by memorising skills. **You describe what you want; the right skill fires on its own.** This page exists so a human can see the doors.

When this skill is invoked, show the user the orientation below (adapt the wording, keep the structure), then either route to the skill that matches their goal or ask the one question you need to.

## Pick your door

| Your goal | Just say… | Skill that fires |
|---|---|---|
| Set up a brand-new / empty project | *"set up Claude Code for this new project"* | `bootstrap-claude-stack` |
| Configure an existing codebase | *"configure Claude Code for this repo"* | `adopt-claude-stack` |
| Build a feature | *"I want to build &lt;X&gt;"* | `brainstorm` → `specify` → … |
| Fix a bug | *"&lt;X&gt; is broken"* / *"this test is failing"* | `debug` |
| Lock in project principles | *"set up the project's principles"* | `constitution` |
| Check launch readiness | *"is this production ready?"* | `production-readiness-assessor` |

That's all you need to start. The rest of the skills are stages the harness moves through *for* you — you don't pick them by hand.

## The feature loop (what happens after "I want to build X")

```
brainstorm → specify → clarify → plan → tasks → analyze → implement → finish-branch
              (tdd · debug · verify-done enforced throughout)
```

Each stage hands off to the next and gates the work — a spec checklist, a constitution check, a cross-artifact audit, a "show me the evidence" rule before anything is called done. You approve the handoffs; you don't have to remember the names.

## Two ways to invoke

1. **Describe the task in plain language** (preferred). The harness routes from your phrasing — *"add rate limiting to the API"* lands you in the feature loop; *"the upload silently fails"* lands you in `debug`.
2. **Name a skill explicitly** with `/claude-stack:<name>` (Claude Code) or by mentioning it (Codex) — use this when you want a specific stage and don't want the harness to choose.

## You don't need to memorise the catalogue

There are ~19 skills, but only the six doors above are entry points. Everything else is machinery the loop walks through. If you ever feel lost, say **"start"** (or run `/claude-stack:start`) to see this page again.

## See also

- `using-claude-stack` — the same map written for the model (injected each session by the SessionStart hook).
- `README.md` — the full skill catalogue and the lineages this kit fuses.
