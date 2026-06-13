#!/usr/bin/env bash
# .claude/hooks/gate-checks.sh — run this repo's DETERMINISTIC checks locally,
# as a Claude Code PreToolUse hook (matcher "Bash"). On `git commit` it runs the
# fast checks and DENIES the commit (returning the failure output) when one fails,
# so the agent fixes it before retrying. Companion to gate-git.sh (which defers
# protected-branch pushes and --no-verify bypasses).
#
# Fill in the commands below with this repo's real ones (the same the CLAUDE.md
# "Build & test" section lists). Leave one empty to skip that check.
#
# Scope is deliberate:
#   - commit: FAST checks only (lint, type-check) — keep it snappy so committing
#     stays cheap. Formatting is already handled by the PostToolUse formatter.
#   - tests / integration / real-API suites are NOT run here. Claude Code hooks are
#     time-bounded, and a multi-minute suite would time the hook out. They are
#     enforced by `verify-done` (the agent runs them and reads the output) and by
#     CI on push/PR. A judgment-call gate a hook cannot prove — "docs in sync",
#     "tests are meaningful" — stays at the skill layer too (the docs-sync step,
#     tdd, review-changes).
#
# Windows: needs Git Bash / WSL. On pure PowerShell, port to a .ps1.

set -uo pipefail

# --- this repo's commands (set at setup; empty = skip) ---
LINT_CMD='{{e.g. uv run ruff check .   — or pnpm lint, go vet ./..., cargo clippy}}'
TYPE_CMD='{{e.g. uv run mypy .         — or pnpm tsc --noEmit, go build ./...; empty to skip}}'

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

deny()  { jq -nc --arg r "$1" '{"permissionDecision":"deny","reason":$r}'; exit 0; }
allow() { jq -nc '{"permissionDecision":"allow"}'; exit 0; }

run() { # $1 = label, $2 = command; deny (with output) on failure
  case "$2" in ""|*"{{"*) return 0 ;; esac   # empty or unconfigured placeholder → skip
  local out
  out="$(bash -c "$2" 2>&1)" || deny "$1 failed — fix before committing:"$'\n'"$out"
}

case "$cmd" in
  *"git commit"*)
    run "Lint" "$LINT_CMD"
    run "Type check" "$TYPE_CMD"
    ;;
esac
allow
