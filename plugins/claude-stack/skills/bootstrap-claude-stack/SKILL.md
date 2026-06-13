---
name: bootstrap-claude-stack
description: Scaffold the minimal Claude Code tuning stack into a brand-new or empty project directory. Creates `.claude/` with a stub CLAUDE.md, a settings.json with a formatter post-tool hook, an .mcp.json with filesystem + context7 MCP servers, and initialises git if needed. Use this skill whenever the user is starting a NEW project from scratch and wants Claude Code configured properly — triggers include "new project", "fresh repo", "starting from scratch", "bootstrap claude", "set up claude code for this project", "scaffold claude config", "init claude code stack", or any situation where the user is in an empty directory and asks you to set things up. Deliberately does NOT create path-scoped rules, subagents, custom skills, worktrees, or git push gates — those are added later when the project surfaces a real need for them.
---

# bootstrap-claude-stack

## Purpose

On a brand-new project, the stack order flips: you build the harness *before* the code, because the harness shapes how the code grows. But a fresh repo can't justify the full stack — you don't know the directory layout, you have no remote yet, and you have no repeated workflows worth packaging. So this skill installs only what earns its keep on day one:

- `.claude/CLAUDE.md` — a *stub* memory file. Living document, expected to grow as the project takes shape.
- `.claude/settings.json` — one post-tool formatter hook. The first file the agent writes is already clean.
- `.mcp.json` — two MCP servers: filesystem (pointed at the project) and context7 (for library docs as you pick dependencies).
- `git init` — only if the directory isn't already a repo.

Everything else (path-scoped rules, subagents, custom skills, worktrees, git push gate, GitHub MCP, code-graph MCP) is deliberately omitted. Those are "add when you notice the need" — adding them prematurely means writing instructions against a codebase that doesn't exist.

## When to trigger

The user is in an empty or near-empty directory and signals they want Claude Code configured. Phrases that should fire this skill:

- "set up Claude Code for this new project"
- "I'm starting a new repo, bootstrap the config"
- "scaffold the .claude folder"
- "init the Claude stack here"
- "this is a fresh project, get it ready"

Do **not** trigger this skill on existing repos with substantive code — those need a tailored CLAUDE.md, not a stub. If you see >10 source files or an existing `.claude/CLAUDE.md`, ask the user whether they really want to overwrite, or whether they'd rather do a targeted update.

## Inputs to gather first

Before scaffolding, ask the user for the following in one batch. If you have an `AskUserQuestion` tool, use it; otherwise ask in plain text. Don't proceed until you have all four:

1. **Project name** — used as the heading in CLAUDE.md and the project key for any future MCP scoping. Default to the current directory name if the user doesn't care.
2. **Language / runtime** — Python, TypeScript/Node, Go, Rust, etc. Determines which formatter the post-tool hook invokes.
3. **Package manager command** — `uv`, `npm`, `pnpm`, `cargo`, `go`, etc. Used in the CLAUDE.md build/test section.
4. **One-line description** — what the project is for. Single sentence. Goes at the top of CLAUDE.md.

If the user supplies only some, fill the rest with sensible defaults and confirm before writing.

## Steps

### 1. Verify the directory is appropriate

Run `ls -la` (or `Get-ChildItem`) in the working directory. If you see:
- An existing `.claude/CLAUDE.md` → ask the user before overwriting.
- A populated `src/` or many source files → confirm this is genuinely "new" and they don't want a tailored CLAUDE.md instead.
- An existing `.git/` → fine, skip `git init` later.

### 2. Create the directory structure

```
mkdir -p .claude/rules .claude/agents .claude/skills .claude/hooks .claude/lessons
```

Each subdirectory gets a short `README.md` explaining what lives there (see step 2a). The dirs are empty otherwise — no placeholder rules, agents, skills, or hook scripts. (`.claude/lessons/` is the one exception that also gets an empty `LESSONS.md` index — see 2a — because lessons accrue from day one as mistakes get corrected.) The READMEs serve as discoverability cues and mini-docs so the user (or the agent on a later turn) knows where new things go.

`.claude/logs/` is *not* created up front — that one is genuinely noise until something actually writes a log. The `.gitignore` in step 6 still excludes it.

### 2a. Write a README in each subdirectory

Write these five small files. They always get written regardless of step 2b, and double as documentation and as triggers for the agent later ("oh, there's a `rules/` dir, that's where path-scoped behaviour goes").

**`.claude/rules/README.md`:**
```markdown
# Path-scoped rules

Rules in this directory load only when Claude is editing files matching
their `globs:` (or `paths:`) frontmatter. They cost zero tokens otherwise.

Add a rule file here when a directory grows enough to want consistent
conventions (typically once you have 3+ files in the same area).

## Example

```
---
name: api-rules
description: Conventions for src/api/**.
globs:
  - "src/api/**"
  - "tests/api/**"
---
# API rules
- All handlers return Pydantic models, never raw dicts.
- Errors raise typed exceptions from `src/api/errors.py`.
```
```

**`.claude/agents/README.md`:**
```markdown
# Custom subagents

Subagents run in their own context window with a restricted tool allowlist.
Drop a markdown file here with YAML frontmatter to define one.

Add a subagent when you find yourself repeating the same review or
analysis task, or when you want a read-only role that can't mutate the
codebase (e.g. an architecture reviewer).

## Example

```
---
name: api-reviewer
description: Reviews changes under src/api/ for contract regressions.
  Read-only.
tools: Read, Grep, Glob, Bash(git diff:*)
model: sonnet
---
You are an API reviewer. Check that every handler...
```
```

**`.claude/skills/README.md`:**
```markdown
# Project-level skills

Skills are workflows packaged for reuse. Each skill lives in its own
subdirectory containing a `SKILL.md` with YAML frontmatter. Bundled
scripts and templates can live alongside the SKILL.md.

Add a skill here when a workflow is stable enough that you'd rather
invoke it by name than re-explain it each time.

## Layout

```
skills/
└── my-workflow/
    ├── SKILL.md
    └── scripts/   (optional)
```

User-level skills live in `~/.claude/skills/` and are available across
all projects. Project-level skills (here) ship with the repo.
```

**`.claude/hooks/README.md`:**
```markdown
# Hook scripts

Shell scripts referenced from `.claude/settings.json` go here. Hooks
add deterministic guardrails to a probabilistic agent — formatters,
permission gates, audit loggers.

The bootstrap already wired one hook: a post-tool formatter in
`settings.json`. Add more when you find an action you want to gate
or automate after every tool call.

## Example: a git-push-to-main gate

`.claude/hooks/gate_git_push.sh`:
```
#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"
case "$cmd" in
  *"git push"*"origin main"*)
    jq -nc '{"permissionDecision": "defer", "reason": "Push to main needs approval."}'
    ;;
  *)
    jq -nc '{"permissionDecision": "allow"}'
    ;;
esac
```

Then reference it from `settings.json` under `hooks.PreToolUse`.
```

**`.claude/lessons/README.md`:**
```markdown
# Lessons

Mistakes we've made once and don't want to repeat — shared team memory,
committed to git. Each lesson is one file; `LESSONS.md` indexes them.

Add one with the `capture-lesson` skill the moment a mistake is corrected.
Recall: skim `LESSONS.md` before non-trivial work (the claude-stack
SessionStart hook also injects it automatically once it has entries).
```

Also write an **empty index** at `.claude/lessons/LESSONS.md` so the convention is visible from day one:
```markdown
# Lessons

One row per active lesson, newest first; the full lesson is in the linked file. Skim before non-trivial work.
Hard cap: 15 rows — promote/retire/consolidate before adding a 16th (see the `capture-lesson` skill).

<!-- Added via the capture-lesson skill. The link text IS the actable rule:
- [the rule, imperative](YYYY-MM-DD-slug.md) — category; recall when <trigger>
-->
```

Leave it entry-free until a real mistake is captured. Lessons are committed (shared knowledge), so they are *not* added to `.gitignore` in step 6.

### 2b. Offer to seed each subdirectory now (or skip)

The default minimal posture is to leave `.claude/rules/`, `.claude/agents/`, `.claude/skills/`, and `.claude/hooks/` empty apart from their README. That stays the right default — *don't* invent content. But if the user already has concrete things in mind on day one, capture them now instead of forcing them to come back later.

Ask the user — one batched `AskUserQuestion` with `multiSelect: true` — which of the four slots they want to seed *now* vs leave empty. Each option corresponds to one subdirectory. Phrase each option as "skip / leave empty" by default; the user opts in by selecting.

> **Important — content comes from the chat, not a file.** When the user opts in, ask them to *type the content directly in the conversation*. Never ask for a file path, URL, or doc to pull from. The user pastes prose; you wrap it into the right file shape. If the user has nothing concrete to type, treat that as "skip" — do not fabricate placeholder content to fill the slot.

For each slot the user opted into, run a follow-up question to collect what they want to put there, then write the file as follows. If the user opts out (default), do nothing — the README from step 2a is the only thing in that directory.

#### `.claude/rules/` — path-scoped rule

Ask: "Paste the rule content here — what should Claude do (or not do) when editing files in a particular area? Also tell me a short name and which paths it applies to." Then write:

```markdown
---
name: {{slug from user}}
description: {{one-line summary, asked or inferred from the body}}
globs:
  - "{{path glob from user, e.g. 'src/api/**'}}"
---

# {{title}}

{{user-typed rule body, lightly reformatted as bullets if appropriate}}
```

Save as `.claude/rules/{{slug}}.md`. If the user pastes multiple distinct rule sets, write one file per scope.

#### `.claude/agents/` — subagent

Ask: "Describe the subagent — name, when it should be used, what tools it needs, and the prompt body." Defaults if the user is silent: tools `Read, Grep, Glob`, model `sonnet`. Then write:

```markdown
---
name: {{name}}
description: {{description}}
tools: {{tool allowlist}}
model: {{model}}
---

{{user-typed subagent prompt verbatim}}
```

Save as `.claude/agents/{{name}}.md`.

#### `.claude/skills/` — project-level skill

Ask: "Describe the workflow — name, trigger phrases (when should it fire?), and the steps the skill should walk through." Then write a stub:

```markdown
---
name: {{name}}
description: {{description including trigger phrases the user mentioned}}
---

# {{name}}

{{user-typed workflow description, treated as the body}}
```

Save as `.claude/skills/{{name}}/SKILL.md` (create the subdirectory).

#### `.claude/hooks/` — guardrail hook beyond the default formatter

Ask: "Describe the guardrail — what behaviour do you want to block, warn on, or automate? Which tool calls does it apply to (Bash for command gates, Write/Edit for file gates)?" Then:

1. Write a shell script under `.claude/hooks/{{slug}}.sh` implementing the guardrail (the user's prose becomes the logic — adapt the `gate_git_push.sh` shape from the README as a starting point).
2. Make it executable (`chmod +x`).
3. Remember to add the hook entry to `settings.json` in step 4 — alongside (not replacing) the default formatter hook.

If the user opts in but cannot articulate the logic concretely, ask one clarifying question. If still vague, fall back to "skip" rather than guessing.

### 3. Write `.claude/CLAUDE.md` (global rules + project stub)

Before writing the project stub, check whether the user already has a global Claude config at `~/.claude/CLAUDE.md`:

```bash
test -f ~/.claude/CLAUDE.md && echo "exists" || echo "missing"
```

- **If `~/.claude/CLAUDE.md` exists**, the user already has global behavioural rules loaded into every session. Don't duplicate them in the project file — write only the project stub below.
- **If `~/.claude/CLAUDE.md` is missing**, ask the user whether to (a) install [`assets/CLAUDE-global-template.md`](assets/CLAUDE-global-template.md) at user level so it applies to all their projects, *or* (b) prepend it to this project's `.claude/CLAUDE.md` so the rules apply at least here. Option (a) is preferred — global rules belong at user level. Option (b) is the fallback when the user wants the rules but doesn't want to touch their home directory yet.

The bundled `assets/CLAUDE-global-template.md` is a tested set of 12 behavioural rules and 9 application-building failure modes. Read it first if you haven't seen it — it covers think-before-coding, surgical changes, fail-loud, UI grounding, state management, etc.

**Before substituting the template variables**, ask the user — via `AskUserQuestion` — whether to enrich the stub with content they want to capture *now* rather than leave as generic placeholder. Three independent slots (multiSelect):

- **Conventions** — replaces the three placeholder bullets. Ask: "Any project-specific conventions to capture now (coding style, architectural rules, library choices)? Paste them here; otherwise I'll keep the generic placeholder."
- **Out of scope** — adds a new `## Out of scope` section under Guardrails. Ask: "Anything Claude should never do in this project? (e.g. 'never touch the migrations folder', 'no LLM calls in test code'). Skip to omit."
- **Glossary** — adds a new `## Glossary` section above Notes. Ask: "Any domain terms worth recording so the agent uses your language consistently? (term → one-line definition). Skip to omit."

For any slot the user opts into, paste their content **verbatim with light reformatting only** (bullets, capitalisation). Never paraphrase. Content comes from the chat — do not read a file or fetch from a URL. If the user skips a slot, fall back to the default template content (placeholder bullets for Conventions; no section for Out-of-scope / Glossary).

Then write the project stub. Use this template. Substitute `{{project_name}}`, `{{description}}`, `{{language}}`, `{{pkg_mgr}}`, and the slot content above. The `## Where things live` and `## Working on a task` sections are **always written verbatim** — they make the root file a hub that points at the rest of the stack (`.claude/rules/`, `.claude/lessons/`, `.claude/memory/constitution.md`, `specs/`) and tell the agent when to consult each. Leave their paths even though some targets are empty on day one; they fill in as the project grows and the relevant skills run. Keep the whole file under ~60 lines even with user content — if the user pastes a wall of text, ask whether the long-form material should live elsewhere (a path-scoped rule under `.claude/rules/`, or `docs/`).

```markdown
# {{project_name}}

{{description}}

## Stack
- Language: {{language}}
- Package manager: {{pkg_mgr}}

## Build & test
- Install:     `{{pkg_mgr_install}}`
- Run tests:   `{{pkg_mgr_test}}`
- Lint/format: `{{pkg_mgr_lint}}`

## Conventions (expand as the project takes shape)
- Prefer editing existing files over adding new top-level packages.
- Keep functions small and single-responsibility.
- No network calls in unit tests — use fakes/fixtures.

## Guardrails
- Never commit secrets. Use environment variables.
- Surface ambiguity rather than guessing.

## Where things live
This file orients; detail lives next to the work. Read the relevant one before touching an area.
- `docs/architecture/` — system architecture. `ARCHITECTURE.md` is the high-level overview (components, how they fit, external deps, key decisions) — read it first and keep it current; `README.md` indexes what else is in the folder (diagrams, per-component docs) as those are added.
- `docs/decisions/` — ADRs (architecture decision records); appears when you record your first non-obvious decision. Check an ADR's Status before applying it.
- `.claude/rules/*.md` — path-scoped conventions; auto-load when editing matching files.
- `.claude/lessons/LESSONS.md` — mistakes already made once; skim before non-trivial work.
- `.claude/memory/constitution.md` — non-negotiable principles, once the `constitution` skill has run.
- `specs/NNN-<slug>/` — per-feature `spec.md` → `plan.md` → `tasks.md`, created by the `specify`/`plan`/`tasks` skills when you build a feature.
- A subdirectory may add its own `CLAUDE.md` — the closest one wins for local detail.

## Working on a task
- **Starting:** skim `docs/architecture/ARCHITECTURE.md` for the big picture, read the active spec under `specs/` (if any), then `.claude/memory/constitution.md` and any `.claude/rules/` matching the files you'll touch. Make the smallest change that satisfies the goal.
- **Finishing:** run the build/test/lint commands above. If a mistake was corrected, capture it with the `capture-lesson` skill. Record any non-obvious decision as an ADR in `docs/decisions/` (create the folder + index from the ADR template on the first one; check an ADR's Status before relying on it).
- **Docs sync (do this before calling the task done):** if the change altered behavior, structure, interfaces, or a decision, find every doc that now describes the *old* reality — `docs/architecture/ARCHITECTURE.md`, an ADR in `docs/decisions/`, a spec, a runbook, the `README`, or `CLAUDE.md`/`.claude/rules/` themselves — and update it yourself in the same change. This is your job, not a note to hand back to the user; only *flag* a doc (with the reason) when its update is genuinely out of scope. A doc that contradicts the code is worse than no doc.

## Notes
This file is a living document. Add path-scoped rules under `.claude/rules/`
when a directory grows enough to warrant its own conventions.
```

Pick the right commands for the chosen package manager. For example:

| Language / pkg mgr | install | test | lint/format |
|---|---|---|---|
| Python + uv | `uv sync` | `uv run pytest -q` | `uv run ruff format . && uv run ruff check .` |
| Python + pip | `pip install -e .` | `pytest -q` | `ruff format . && ruff check .` |
| Node + npm | `npm install` | `npm test` | `npm run lint` |
| Node + pnpm | `pnpm install` | `pnpm test` | `pnpm lint` |
| Go | `go mod tidy` | `go test ./...` | `gofmt -w . && go vet ./...` |
| Rust + cargo | `cargo build` | `cargo test` | `cargo fmt && cargo clippy` |

If unsure, write reasonable placeholders and add a `TODO:` comment next to the command.

### 3a. Install the language rule template (if Python or TypeScript)

The skill bundles two ready-made path-scoped rule files that encode common conventions for the two most-requested language stacks:

- [`assets/python-rule-template.md`](assets/python-rule-template.md) — PEP 8, ruff/black, type hints, uv, mutable defaults, pytest, etc. Scoped to `**/*.py` and `**/*.pyi`.
- [`assets/typescript-rule-template.md`](assets/typescript-rule-template.md) — Prettier/ESLint, strict TS, `??` vs `||`, immutability, pnpm, vitest, React conventions. Scoped to `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/*.mjs`, `**/*.cjs`.

If the chosen language is Python or TypeScript/JavaScript, copy the corresponding asset into `.claude/rules/` so it loads automatically when Claude edits matching files:

```bash
# Python project
cp assets/python-rule-template.md .claude/rules/python-conventions.md

# TypeScript / JavaScript project
cp assets/typescript-rule-template.md .claude/rules/typescript-conventions.md
```

Both files already have correct YAML frontmatter (`globs:` matching the language's file extensions) — no editing needed. The rules pair with the global behavioural rules from step 3 and load only when relevant, costing zero tokens otherwise.

For other languages (Go, Rust, etc.), don't fabricate a rule. Leave `.claude/rules/` empty (with its README) and let the user write a rule when they feel the need.

### 3b. Point the user at the production-readiness-assessor

This plugin ships a general-purpose **`production-readiness-assessor`** skill alongside this one (a sibling under `skills/`). It scores a codebase across thirteen dimensions (testing, error handling, observability, security, maintainability, CI/CD, configuration, performance, documentation, operations, data management, compliance & governance, dependency management), cites concrete evidence for every score, and produces a Markdown scorecard with a prioritised action plan.

Because it's a sibling skill in the same plugin, there is **nothing to install or copy** — once this plugin is enabled, the assessor is already available. (This replaces the older behaviour of copying it into `~/.claude/skills/`; under plugin distribution that copy is redundant and only creates drift between copies.)

A brand-new project usually has little to score yet, so **don't run it now**. Just note in the step 7 report that when the project grows and nears launch, the user can trigger it with phrases like *"is this production ready?"*, *"audit this repo before launch"*, or *"score my codebase on prod readiness"* — no setup required. The skill handles the rest, including its bundled `scan_signals.py` and the scorecard template.

### 3c. Create `docs/architecture/` with a high-level overview (compulsory)

Every project gets an architecture overview from day one — it is the first thing a new contributor (human or agent) reads to understand how the pieces fit, and on a fresh repo it doubles as a design sketch that shapes how the code grows. The folder holds two files: `ARCHITECTURE.md` (the substantive overview) and `README.md` (a short index of what's in the folder, so it renders as the folder's landing page). Diagrams and per-component docs join them later. Like `CLAUDE.md`, `ARCHITECTURE.md` is a **living skeleton**, not a finished document: write the section headings with short prompts, and let the user fill them in (offer to capture anything they describe now).

```bash
mkdir -p docs/architecture
```

First write `docs/architecture/ARCHITECTURE.md`. Substitute `{{project_name}}` / `{{description}}`; if the user described any components, flows, or dependencies during the inputs step, drop them into the matching sections verbatim — otherwise leave the prompt comments so they know what to fill in. Do **not** invent components a new project does not have yet.

```markdown
# Architecture overview — {{project_name}}

High-level map of the system. Read this first; keep it current as the system grows.
Promote durable, non-obvious decisions to `docs/decisions/` (ADRs) when that folder appears.

## Purpose
{{description}}

## Components
<!-- The major moving parts. One bullet each: name — responsibility. -->
- _TODO: list components as they emerge._

## How they fit together
<!-- The main flow: what calls what, where data enters and leaves. Prose or an ASCII sketch. -->
_TODO._

## External dependencies
<!-- Services, APIs, datastores, queues this system relies on, and why. -->
- _TODO._

## Key decisions
<!-- Non-obvious choices and their rationale. -->
- _TODO._

## Constraints & non-goals
- _TODO: what this system deliberately does not do._
```

Then write `docs/architecture/README.md` as the folder index — short, just a map of what lives here, so the folder has a sensible landing page and there is an obvious place to register diagrams as they get added:

```markdown
# Architecture docs

What lives in this folder:

- [ARCHITECTURE.md](ARCHITECTURE.md) — high-level overview; **start here**.

<!-- Add entries as the folder grows, e.g.:
- diagrams/system-context.svg — C4 system-context diagram
- data-model.md — entity / relationship detail
-->
```

Keep both short — skeletons, not essays. They grow as the architecture takes shape; the goal on day one is that `ARCHITECTURE.md` *exists and has the right headings* and the index points at it, so there is an obvious home for architectural thinking — and for the diagrams that will land beside it in `docs/architecture/` — the moment it happens.

### 3d. Decision records (`docs/decisions/`) — the ADR pattern (not created now)

Unlike the architecture overview, **do not create `docs/decisions/` at setup** — an empty repo has no decisions yet. Just make the pattern available so the agent reaches for it when the first non-obvious choice gets made. The skill bundles two templates:

- [`assets/adr-template.md`](assets/adr-template.md) — one architecture decision record (Status / Context / Decision / Consequences).
- [`assets/decisions-README-template.md`](assets/decisions-README-template.md) — the index, encoding the discipline that makes ADRs trustworthy: a **Status** column, sequential numbering, and "**check Status before applying**, update **both** rows on supersession."

When the first durable decision arises, create `docs/decisions/` from these, write `0001-<slug>.md`, and add its row to the index. The `Working on a task` lifecycle in `CLAUDE.md` and the architecture overview both point here; until then, there is nothing to create.

### 4. Write `.claude/settings.json`

The only hook on day one is a post-tool formatter. Pick the formatter that matches the language. Examples:

**Python (uv + ruff):**
```json
{
  "hooks": {
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
    ]
  }
}
```

**Node/TypeScript (prettier):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "npx --yes prettier --write $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true"
          }
        ]
      }
    ]
  }
}
```

**Go:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "gofmt -w $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true"
          }
        ]
      }
    ]
  }
}
```

**Rust:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "rustfmt $CLAUDE_TOOL_FILE_PATH >/dev/null 2>&1 || true"
          }
        ]
      }
    ]
  }
}
```

The `|| true` at the end is deliberate — a formatter failure shouldn't block the agent. The `>/dev/null 2>&1` keeps the agent's context clean.

If the language isn't in this list, ask the user for their formatter command and adapt the same shape.

### 5. Write `.mcp.json`

Two servers on day one. No GitHub server (no remote yet), no code-graph server (codebase too small to benefit), no search server (add when you find yourself googling library docs repeatedly).

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

The filesystem server is scoped to `.` (the current project). If the user mentions they share prompts/configs across projects, ask whether to also include a sibling path — but default to single-directory to keep blast radius small.

### 6. Initialise git if needed

Check for `.git/`. If absent:

```bash
git init
```

Then write a minimal `.gitignore` if one doesn't exist. Include at least:

```
# Claude Code
.claude/logs/
.claude/local/

# OS / editor
.DS_Store
.idea/
.vscode/

# Language-specific (add what fits)
__pycache__/
*.pyc
node_modules/
target/
dist/
build/
```

**Before writing, ask the user** — via `AskUserQuestion` — whether there are project-specific paths to add beyond the standard list above (e.g. data directories, secret files like `secrets.toml`, generated artefacts like `*.gen.go`, fixture caches). If they paste paths, append them under a `# Project-specific` section. If they skip, write just the standard list. Paths come from the chat — do not scan the filesystem for "likely sensitive files" and silently add them; ask explicitly.

Don't commit anything automatically. Tell the user the repo is initialised and let them make the first commit themselves.

### 7. Report what you did

Give the user a short summary:

- Files created (with clickable paths if the harness renders them) — including `docs/architecture/ARCHITECTURE.md`; point the user at it and ask them to fill the headings as the design firms up.
- What's deliberately *not* there and why (rules, subagents, GitHub MCP).
- The natural next moves: "When you've written a couple of files in the same directory and want consistency, ask me to add a path-scoped rule. When you push to GitHub for the first time, ask me to add the GitHub MCP server and the bundled git gate (`assets/gate-git.sh` — defers pushes to `main`/`master` and `--no-verify`/`--no-gpg-sign` bypasses)."
- "To build your first feature, this plugin ships the full development loop: **`brainstorm`** (refine the idea) → **`specify`** (formal spec) → **`plan`** → **`tasks`** → **`implement`** — with **`tdd`**, **`debug`**, and **`verify-done`** enforcing discipline throughout. **Before that first feature, establish the project's principles with `constitution`** — this is required, not optional: `plan` stops without it and `analyze` gates every design against it."
- "When the project grows and nears launch, run the **`production-readiness-assessor`** that ships with this plugin — just ask *'is this production ready?'* for an evidence-based scorecard and gate check. Nothing to install."

## Do not

- Do not put *content* into `.claude/rules/`, `.claude/agents/`, `.claude/skills/`, or `.claude/hooks/` on day one **unless the user explicitly pastes it during step 2b**. Empty-with-README is the default. User-supplied content is the explicit opt-in. Never fabricate placeholder rules/agents/skills/hooks to "fill" the slot.
- Do not pull seed content from files, URLs, or doc references when the user opts in. The chat is the only input — if the user has nothing concrete to type, treat that as "skip" and move on.
- Do not install more than two MCP servers (the user-seeded hooks in step 2b don't count). Tool schemas cost tokens every turn.
- Do not write a long CLAUDE.md unprompted. The ~45-line stub is intentional — the `Where things live` map and `Working on a task` lifecycle are always written (they wire the file into the rest of the stack), but everything else stays terse because descriptive bloat trains the user to ignore the file. Pasted user content is the only reason to grow it further, and even then keep the stub under ~60 lines or move long-form content into a path-scoped rule.
- Do not auto-wire the git gate on day one — keep settings.json to just the formatter. The bundled `assets/gate-git.sh` (defers pushes to `main`/`master` and `--no-verify`/`--no-gpg-sign` bypasses) is ready to install; *offer* it, and wire it when the user adds a remote or asks for enforcement. The push clause is inert without a remote; the bypass guard works immediately. The bundled `assets/gate-checks.sh` (a PreToolUse hook that denies a commit when lint/type-check fails) is ready too — offer it once the project has a linter/type-checker configured. A hook can't prove tests/docs were done — those gates stay at the skill layer (`tdd`, `verify-done`, the docs-sync step).
- Do not commit anything automatically. The user owns the first commit.
- Do not overwrite an existing `.claude/CLAUDE.md` without explicit confirmation.
- Do not silently scan the filesystem for "likely sensitive" paths to add to `.gitignore`. Ask in step 6 instead.

## Why this minimal shape

The full eight-layer stack (CLAUDE.md + path-scoped rules + Plan Mode + subagents + skills + hooks + MCP servers + worktrees) works because each layer addresses a real problem in a mature codebase. On day one those problems don't exist yet:

- No directories to scope rules to.
- No repeated tasks worth packaging as subagents or skills.
- No remote to gate pushes against.
- No long-running parallel work that needs worktrees.

Installing the full stack into an empty repo creates instructions that drift from reality the moment the project takes shape. The stub-plus-formatter shape stays correct as the project grows, and each additional layer can be added at the moment its problem first appears — which is also the moment the user can write the instruction with real context.

The two things written *before* code — the `CLAUDE.md` stub and the `docs/architecture/ARCHITECTURE.md` skeleton — are the deliberate exceptions. They don't describe code that doesn't exist; they are living documents that *shape* how the code grows, and an empty repo is exactly when an architecture sketch is cheapest to start and most influential. They stay skeletons (headings + prompts) so they orient without pretending to knowledge the project hasn't earned yet.
