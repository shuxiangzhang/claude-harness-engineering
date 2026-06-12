#!/usr/bin/env bash
# .claude/hooks/gate_git_push.sh
#
# Verbatim from the article: defer any `git push` that targets main. The
# session pauses. A human approves out-of-band and the agent resumes via
# `claude --resume`.
#
# Adoption note: this skill installs a slightly generalised version that
# also catches `master`. The article's original is below.

set -euo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

case "$cmd" in
  *"git push"*"origin main"*|*"git push"*" main"*)
    jq -nc '{
      "permissionDecision": "defer",
      "reason": "Push to main requires human approval."
    }'
    ;;
  *)
    jq -nc '{"permissionDecision": "allow"}'
    ;;
esac

# -----------------------------------------------------------------------
# Adoption-time variant that also catches master:
#
# case "$cmd" in
#   *"git push"*"origin main"*|*"git push"*"origin master"*|*"git push"*" main"*|*"git push"*" master"*)
#     jq -nc '{
#       "permissionDecision": "defer",
#       "reason": "Push to main/master requires human approval."
#     }'
#     ;;
#   *)
#     jq -nc '{"permissionDecision": "allow"}'
#     ;;
# esac
#
# Install: chmod +x .claude/hooks/gate_git_push.sh
# Wire it via the "PreToolUse" hook in settings.json (matcher: "Bash").
#
# Windows note: this script needs Git Bash or WSL to run. On pure
# PowerShell, write a .ps1 equivalent and reference that path instead.
