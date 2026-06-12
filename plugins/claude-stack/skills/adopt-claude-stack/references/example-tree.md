# Example: `.claude/` directory tree (mature configuration)

From the article opening. This is what a power-user's `.claude/` looks like once the full eight-layer stack has accreted. **Adoption installs the floor, not this.** Use it as the target shape the user is graduating towards over time.

```
.claude/
├── CLAUDE.md
├── rules/
│   ├── langgraph.md
│   ├── retrieval.md
│   ├── tests.md
│   └── python-types.md
├── agents/
│   ├── retrieval-reviewer.md
│   ├── prompt-auditor.md
│   └── eval-runner.md
├── skills/
│   ├── new-rag-eval/
│   │   └── SKILL.md
│   └── claude-pr-checklist/
│       └── SKILL.md
├── settings.json
└── .mcp.json
```

## Article notes on this tree

- None of these files is long. The main memory file is under 500 tokens on purpose.
- Each rules file is a short path-scoped behaviour.
- Each subagent is maybe thirty lines.
- The hooks configuration in the settings file is one pre-tool gate and one post-tool formatter.
- The server configuration has five servers instead of fifteen.

## What adoption installs day one

Of the above, day-one adoption produces:

- `CLAUDE.md` (tailored from survey, not from template)
- `rules/` with **2–3 path-scoped rules** for directories whose conventions are clear from the existing code
- `agents/` empty with a README pointing at `references/example-subagent.md`
- `skills/` empty with a README pointing at `references/example-skill.md`
- `settings.json` with a post-tool formatter (and the push gate if a remote exists)
- `.mcp.json` with three servers (filesystem, context7, GitHub if remote is github.com)

The user graduates to the full tree as the project surfaces real need.
