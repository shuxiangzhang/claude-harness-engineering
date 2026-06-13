# claude-stack for Codex

Using the claude-harness-engineering skills with OpenAI Codex via native skill discovery.

## Quick install

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/shuxiangzhang/claude-harness-engineering/refs/heads/main/.codex/INSTALL.md
```

Or follow [.codex/INSTALL.md](../.codex/INSTALL.md) manually.

## How it works

Codex scans `~/.agents/skills/` at startup, parses each `SKILL.md` frontmatter, and loads a
skill's body on demand when its `description` matches the task. A single symlink makes all 23
claude-stack skills visible:

```
~/.agents/skills/claude-stack/ → ~/.codex/claude-harness-engineering/plugins/claude-stack/skills/
```

Because skills are just `SKILL.md` files with `name` + `description` frontmatter — the format
Codex and Claude Code share — nothing in the skills needs to change between platforms.

## What transfers, and the one difference

| | Claude Code | Codex |
|---|---|---|
| Skill format (`SKILL.md`) | ✅ | ✅ identical |
| Discovery | plugin install | symlink + native scan |
| Routing map (`using-claude-stack`) | injected by SessionStart hook | self-discovered by description |
| Invoke a skill | Skill tool / `/claude-stack:<name>` | mention by name / auto-match |
| Lessons (`.claude/lessons/`) | folder + index auto-injected by hook | folder + index recalled via the `AGENTS.md`/`CLAUDE.md` pointer |
| Bundled templates & reviewer prompts | ✅ | ✅ |
| The `production-readiness-assessor` script | ✅ | ✅ (needs Python, same as Claude Code) |

The only functional difference: Claude Code force-injects the routing map every session via a
hook; Codex discovers it natively instead. The discipline skills (`tdd`, `debug`,
`verify-done`) and the spec-driven loop behave the same — they're plain instructions.

A few skills reference Claude Code's subagent tooling by name (e.g. `implement` dispatches an
"Agent" subagent for its two-stage review). On Codex, use Codex's own subagent/task mechanism
for the equivalent step — the workflow and review structure are unchanged.

## Usage

Skills activate when you mention one by name ("use brainstorming", "run the readiness audit"),
when the task matches a skill's `description`, or when `using-claude-stack` routes you to one.

The intended lifecycle is identical to Claude Code:

```
constitution → brainstorm → specify → clarify → plan → tasks → analyze → implement
               (tdd · debug · verify-done throughout) → finish-branch → readiness audit
```

## Updating / uninstalling / troubleshooting

See [.codex/INSTALL.md](../.codex/INSTALL.md). If skills don't appear: verify the symlink
(`ls -la ~/.agents/skills/claude-stack`), confirm the clone has `plugins/claude-stack/skills`,
and restart Codex — discovery happens at startup.
