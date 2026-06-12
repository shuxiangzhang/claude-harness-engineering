# claude-harness-engineering

A Claude Code plugin marketplace for **engineering the agent harness** — one plugin,
**`claude-stack`**, that covers the full journey: configure Claude Code for a repo,
govern it with principles, run a spec-driven feature loop with hard quality gates,
enforce engineering discipline, and audit readiness before launch.

It fuses three lineages:

- the **8-layer tuning stack** (CLAUDE.md, path-scoped rules, hooks, MCP servers) — setup skills
- **[github/spec-kit](https://github.com/github/spec-kit)**'s spec-driven workflow (spec → plan → tasks → implement, with constitution gates and cross-artifact analysis)
- **[obra/superpowers](https://github.com/obra/superpowers)**' engineering discipline (TDD iron law, systematic debugging, evidence-before-claims, subagent-driven implementation)

## Install

The skills are plain `SKILL.md` files (the format Claude Code and Codex share), so the same
kit runs on both.

### Claude Code (plugin marketplace)

```
/plugin marketplace add shuxiangzhang/claude-harness-engineering
/plugin install claude-stack@claude-harness-engineering
```

A SessionStart hook then injects a one-page routing map into each session, so the right
skill fires from natural phrasing — `/claude-stack:<skill>` also invokes any skill directly.

### Codex (native skill discovery)

Clone and symlink the skills into Codex's skill path:

```bash
git clone https://github.com/shuxiangzhang/claude-harness-engineering.git ~/.codex/claude-harness-engineering
mkdir -p ~/.agents/skills
ln -s ~/.codex/claude-harness-engineering/plugins/claude-stack/skills ~/.agents/skills/claude-stack
```

Windows (junction): see [.codex/INSTALL.md](.codex/INSTALL.md). Full guide:
[docs/README.codex.md](docs/README.codex.md). Codex has no SessionStart hook, so it discovers
the `using-claude-stack` routing map natively instead of having it injected — everything else
behaves the same.

## The skills (18)

### Setup & governance

| Skill | Use when |
|---|---|
| `bootstrap-claude-stack` | Brand-new/empty project — scaffold the minimal tuning stack |
| `adopt-claude-stack` | Existing codebase — survey, then retrofit a tailored stack |
| `constitution` | Establish/amend the project's non-negotiable principles (gates `plan` and `analyze`) |

### The feature loop (spec-driven)

| Skill | Produces |
|---|---|
| `brainstorm` | Validated design via one-question-at-a-time dialogue |
| `specify` | `specs/NNN-slug/spec.md` — prioritized user stories, testable FRs, measurable success criteria, quality checklist |
| `clarify` | Up to 5 targeted questions, answers encoded back into the spec |
| `plan` | `plan.md` (constitution-gated) + `research.md`, `data-model.md`, `contracts/` |
| `tasks` | Story-grouped `tasks.md` — `[ID] [P?] [Story]` format, 2–5-minute tasks, exact paths |
| `analyze` | Read-only cross-artifact audit, severity-ranked (constitution conflicts = CRITICAL) |
| `implement` | Checklist-gated execution — fresh subagent per task, two-stage review (spec compliance → code quality) |

### Discipline & completion

| Skill | Iron law |
|---|---|
| `tdd` | *No production code without a failing test first* |
| `debug` | *No fixes without root-cause investigation first* (4 phases; 3 failed fixes → question the architecture) |
| `verify-done` | *No completion claims without fresh verification evidence* |
| `finish-branch` | Tests verified → merge / PR / keep / discard (typed confirmation) → cleanup |
| `production-readiness-assessor` | Pre-launch audit across 13 dimensions → evidence-cited scorecard + gate check |

### Meta

| Skill | Purpose |
|---|---|
| `using-claude-stack` | The routing map (injected each session by the hook) |
| `capture-lesson` | Record a mistake-and-correction in `.claude/lessons/` so it isn't repeated; the index resurfaces each session |
| `write-skill` | Create new skills with TDD-for-documentation (baseline failure → minimal skill → close loopholes) |

## The intended flow

```
bootstrap / adopt            → harness configured
constitution                 → principles that gate everything below
brainstorm → specify → clarify → plan → tasks → analyze
implement  (tdd · debug · verify-done throughout)
finish-branch → production-readiness-assessor before launch
```

Each stage hands off to the next; each gate (spec checklist, constitution check,
analyze findings, implement's checklist halt, verify-done's evidence rule) is
designed to fail loudly rather than let plausible-but-wrong work through.

Cutting across all of it, **`capture-lesson`** writes mistakes-and-corrections to
`.claude/lessons/` (committed, shared); the index resurfaces automatically at the start of
every session, so the harness gets harder to fool the same way twice. `bootstrap`/`adopt`
create the folder; the SessionStart hook injects it once it has entries.

## Use without the marketplace

Each skill is a self-contained directory — copy any of them straight into
`~/.claude/skills/` (personal) or `.claude/skills/` (project):

```bash
cp -r plugins/claude-stack/skills/tdd ~/.claude/skills/
```

(The SessionStart hook only ships via the plugin.)

## Layout

```
.
├── .claude-plugin/marketplace.json
└── plugins/claude-stack/
    ├── .claude-plugin/plugin.json
    ├── hooks/                  # SessionStart routing-map injection
    └── skills/                 # 18 skills, each with bundled assets/references
```

## Attribution

Workflow structure, templates, and gate mechanics distilled from
[github/spec-kit](https://github.com/github/spec-kit) (MIT). Discipline skills, the
session-hook mechanism, and the subagent review chain distilled from
[obra/superpowers](https://github.com/obra/superpowers) (MIT). See [NOTICE](NOTICE).

## License

MIT — see [LICENSE](LICENSE).
