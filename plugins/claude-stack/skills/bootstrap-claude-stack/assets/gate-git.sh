#!/usr/bin/env bash
# .claude/hooks/gate-git.sh — deterministic git guardrails.
# Wire as a PreToolUse hook with matcher "Bash" in .claude/settings.json.
#
# Defers (pauses for human approval) two classes of command:
#   1. Pushes to a protected branch (main / master).
#   2. Anything that bypasses hooks or signing (--no-verify / --no-gpg-sign),
#      which would skip the formatter, the other gates, or commit signing.
# Everything else is allowed untouched.
#
# These are the gates a hook can enforce DETERMINISTICALLY. The judgment-call
# gates — tests were written, docs were updated, the spec is satisfied — cannot
# be proven by a hook and deliberately stay at the skill layer: `tdd`,
# `verify-done`, the CLAUDE.md docs-sync step, and the `constitution`, with
# `finish-branch` as the pre-merge checkpoint. Don't fake them here.
#
# Windows: needs Git Bash / WSL. On pure PowerShell, port to a .ps1 and point
# settings.json at that path instead.

set -euo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

case "$cmd" in
  *"git push"*"origin main"*|*"git push"*"origin master"*|*"git push"*" main"*|*"git push"*" master"*)
    jq -nc '{"permissionDecision":"defer","reason":"Push to a protected branch (main/master) needs human approval."}'
    ;;
  *"--no-verify"*|*"--no-gpg-sign"*)
    jq -nc '{"permissionDecision":"defer","reason":"Bypassing hooks/signing (--no-verify / --no-gpg-sign) needs human approval."}'
    ;;
  *)
    jq -nc '{"permissionDecision":"allow"}'
    ;;
esac
