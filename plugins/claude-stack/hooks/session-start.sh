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

# Human-facing first-turn orientation. Static and pre-escaped for JSON (literal \n / \"),
# so it is NOT passed through escape_for_json. Single-quoted to avoid shell expansion;
# kept apostrophe-free so the single-quoted string stays intact.
orientation='\n\n**First-turn orientation — show this to the human, do not just silently absorb it:** If the user has not yet given a concrete task this session (the first message is empty, a greeting, or asks how to use this / where to start / what you can do), open your reply with this menu, then route:\n- New project → say \"set up Claude Code for this new project\"\n- Existing repo → \"configure Claude Code for this repo\"\n- Build a feature → describe it: \"I want to build ...\"\n- Fix a bug → describe it: \"... is broken\"\n- Full tour → run /claude-stack:start\nIf the user already arrived with a concrete task, skip the menu and route to the matching skill silently.'

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
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have the claude-stack harness.\n\n**Below is your 'claude-stack:using-claude-stack' skill — the routing map for the rest. For all other skills, use the Skill tool:**\n\n${routing_escaped}${lessons_escaped}${orientation}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
