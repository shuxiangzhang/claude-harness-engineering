# Installing claude-stack for Codex

Codex has native skill discovery — it scans `~/.agents/skills/` at startup, parses each
`SKILL.md` frontmatter, and loads skills on demand. The same skills that ship as a Claude
Code plugin work unchanged on Codex; you just make them visible with one symlink.

## Prerequisites

- Git
- OpenAI Codex CLI

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shuxiangzhang/claude-harness-engineering.git ~/.codex/claude-harness-engineering
   ```

2. **Symlink the skills directory into Codex's skill path:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/claude-harness-engineering/plugins/claude-stack/skills ~/.agents/skills/claude-stack
   ```

   **Windows (PowerShell)** — use a junction (works without Developer Mode):
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\claude-stack" "$env:USERPROFILE\.codex\claude-harness-engineering\plugins\claude-stack\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) so it discovers the skills.

## Verify

```bash
ls -la ~/.agents/skills/claude-stack
```

You should see a symlink (or junction on Windows) into the cloned `plugins/claude-stack/skills`
directory, containing `using-claude-stack/`, `tdd/`, `specify/`, and the rest.

## Note: no SessionStart hook on Codex

On Claude Code a SessionStart hook injects the `using-claude-stack` routing map into every
session. Codex has no equivalent hook, so the routing map is instead **discovered natively** —
Codex surfaces `using-claude-stack` from its description like any other skill. If you want it
front-of-mind at the start of a task, just say "use claude-stack" or "check claude-stack
skills". Everything downstream works identically.

## Updating

```bash
cd ~/.codex/claude-harness-engineering && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/claude-stack
```

**Windows (PowerShell):** `Remove-Item "$env:USERPROFILE\.agents\skills\claude-stack"`

Optionally delete the clone: `rm -rf ~/.codex/claude-harness-engineering`.
