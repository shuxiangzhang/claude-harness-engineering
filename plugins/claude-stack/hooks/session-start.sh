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

# If this project has accrued lessons (past mistakes), inject the index too, so they
# resurface automatically. Guarded: only when the file exists AND has real entries —
# a no-op in repos that never adopted the stack, or whose lessons folder is empty.
project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
lessons_index="${project_dir}/.claude/lessons/LESSONS.md"
lessons_escaped=""
if [ -f "$lessons_index" ] && grep -q '^- \[' "$lessons_index" 2>/dev/null; then
    lessons_content=$(cat "$lessons_index" 2>/dev/null || echo "")
    lessons_block=$'\n\n**Project lessons — past mistakes, do not repeat (open the linked file when a trigger matches):**\n\n'"${lessons_content}"
    lessons_escaped=$(escape_for_json "$lessons_block")
fi

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have the claude-stack harness.\n\n**Below is your 'claude-stack:using-claude-stack' skill — the routing map for the rest. For all other skills, use the Skill tool:**\n\n${routing_escaped}${lessons_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
