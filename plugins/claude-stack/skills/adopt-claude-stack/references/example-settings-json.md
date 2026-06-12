# Example: `settings.json` with hooks (Layer 6)

The article's full `settings.json` for the citation-rag service. Includes the post-tool formatter, the pre-tool push gate, and the permission-denied audit log.

## Why hooks

From the article:

> Hooks make the agent safe to run with fewer babysitters. They add deterministic guardrails to a probabilistic system.

And on deferred permissions specifically:

> The most important addition is Deferred Permissions. A pre-tool hook can now return a defer decision which pauses the agent mid-run in headless mode. You inspect the session and approve the action out of band. The agent resumes exactly where it left off. Before deferred permissions, a nightly run that needed to push to main either had `--dangerously-skip-permissions` on or the job failed at 3am.

## The full example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/gate_git_push.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run ruff format $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true"
          }
        ]
      }
    ],
    "PermissionDenied": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq -c . >> .claude/logs/denied.jsonl"
          }
        ]
      }
    ]
  }
}
```

## Why the boring formatter hook is the highest-ROI move

From the article:

> The post-tool hook is boring on purpose. One-liner formatting hooks are the highest return on investment you can get. The agent writes a messy file and the hook runs the linter. This way the file is clean before the next turn. The agent never gets confused by its own bad indentation.

## How to adapt this for the user's repo

**Post-tool formatter** — substitute the command based on detection:

| Detected config | Hook command |
|---|---|
| `pyproject.toml` with `[tool.ruff]` | `uv run ruff format $CLAUDE_TOOL_FILE_PATH` |
| `pyproject.toml` with `[tool.black]` | `black $CLAUDE_TOOL_FILE_PATH` |
| `.prettierrc*` or `prettier` in `package.json` | `npx prettier --write $CLAUDE_TOOL_FILE_PATH` |
| `rustfmt.toml` or any Rust crate | `rustfmt $CLAUDE_TOOL_FILE_PATH` |
| Go module | `gofmt -w $CLAUDE_TOOL_FILE_PATH` |

Always wrap with `>/dev/null 2>&1 || true` — a formatter miss must never block the agent or pollute its context.

**Pre-tool push gate** — drop the entire `PreToolUse` block if `git remote -v` is empty. If a remote exists, install the gate. See `example-push-gate.sh` for the script.

**PermissionDenied audit** — cheap and worth keeping always. Helps debug the push gate later. The `.claude/logs/` directory is created the first time this writes; `.gitignore` should exclude it.
