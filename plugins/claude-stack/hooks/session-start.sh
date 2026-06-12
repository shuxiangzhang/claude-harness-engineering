#!/usr/bin/env bash
# SessionStart hook for the claude-stack plugin.
# Injects the using-claude-stack routing map so skills fire reliably.
# Escape technique adapted from obra/superpowers session-start.sh (MIT).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

routing_content=$(cat "${PLUGIN_ROOT}/skills/using-claude-stack/SKILL.md" 2>&1 || echo "Error reading using-claude-stack skill")

# Escape for JSON embedding via bash parameter substitution —
# each pass is a single C-level replace, far faster than per-character loops.
escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

routing_escaped=$(escape_for_json "$routing_content")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have the claude-stack harness.\n\n**Below is your 'claude-stack:using-claude-stack' skill — the routing map for the rest. For all other skills, use the Skill tool:**\n\n${routing_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
