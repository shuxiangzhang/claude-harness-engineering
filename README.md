# claude-harness-engineering

A Claude Code plugin marketplace for **engineering the agent harness** of a repo — the
CLAUDE.md, path-scoped rules, formatter hooks, and MCP servers that shape how Claude Code
works inside a project.

It ships one plugin, **`claude-stack`**, bundling three complementary skills that cover the
journey from empty repo to launch-ready:

| Skill | Use when | What it does |
|---|---|---|
| **`bootstrap-claude-stack`** | You're starting a **brand-new / empty** project | Scaffolds the minimal stack: a stub `CLAUDE.md`, a `settings.json` formatter hook, an `.mcp.json` with filesystem + context7, and `git init`. Deliberately omits everything that can't earn its keep on day one. |
| **`adopt-claude-stack`** | You have an **existing codebase** | Surveys the repo first, then retrofits a *tailored* `CLAUDE.md`, 2–3 path-scoped rules for the most-touched directories, a formatter hook, and three MCP servers (adds GitHub only if a remote exists). |
| **`production-readiness-assessor`** | You're **nearing launch** and want to know if the repo is prod-grade | Audits the codebase across 13 dimensions (testing, error handling, observability, security, CI/CD, data, compliance, dependencies, …), cites concrete evidence per score, and produces a Markdown scorecard with a gate check and prioritised action plan. Trigger with *"is this production ready?"* |

The two setup skills (`bootstrap` / `adopt`) hand off to the assessor as the project matures —
and the assessor points back at `adopt-claude-stack` when it finds a repo with no `.claude/`
config. They also ship ready-made Python / TypeScript path-scoped rule templates and a global
`CLAUDE.md` template.

The design follows Anubhav's *"I Spent 6 Months Tuning Claude Code"* eight-layer stack, installing
only the floor that earns its keep — and pointing you at the rest as the project surfaces the need.

## Install

In Claude Code:

```
/plugin marketplace add shuxiangzhang/claude-harness-engineering
/plugin install claude-stack@claude-harness-engineering
```

Then invoke a skill by name, e.g. `/bootstrap-claude-stack` in a fresh repo,
`/adopt-claude-stack` in an existing one, or `/production-readiness-assessor` before a launch.
Claude will also trigger them automatically from phrases like *"set up Claude Code for this
repo"*, *"scaffold the .claude folder"*, or *"is this production ready?"*.

To update later:

```
/plugin marketplace update claude-harness-engineering
```

## Use without the marketplace

Each skill is a self-contained `SKILL.md` directory. To install one directly, copy it into
your skills folder:

```bash
# personal (all projects)
cp -r plugins/claude-stack/skills/adopt-claude-stack ~/.claude/skills/

# project-scoped (this repo only)
cp -r plugins/claude-stack/skills/bootstrap-claude-stack .claude/skills/
```

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json        # marketplace manifest
└── plugins/
    └── claude-stack/
        ├── .claude-plugin/
        │   └── plugin.json     # plugin manifest
        └── skills/
            ├── bootstrap-claude-stack/
            ├── adopt-claude-stack/
            └── production-readiness-assessor/
```

## License

MIT — see [LICENSE](LICENSE).
