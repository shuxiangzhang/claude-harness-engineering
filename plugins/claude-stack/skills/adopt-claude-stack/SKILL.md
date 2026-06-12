---
name: adopt-claude-stack
description: Retrofit the Claude Code tuning stack into an EXISTING codebase by surveying what's already there and then installing the floor of the 8-layer stack from Anubhav's "I Spent 6 Months Tuning Claude Code" tutorial — a tailored CLAUDE.md, one formatting hook, two or three path-scoped rules for the most-touched directories, and three MCP servers (filesystem, library docs, plus GitHub if a remote exists). Use this skill whenever the user wants to add or improve Claude Code configuration on a repo that already has source files — triggers include "set up Claude Code for this repo", "adopt the tuning stack here", "retrofit claude config", "tune Claude for this existing project", "add a tailored CLAUDE.md", "the .claude folder here is empty and I want to fix it". Do not trigger on empty directories — those need a different scaffold.
---

# adopt-claude-stack

## Source

This skill is a working implementation of the floor configuration recommended in Anubhav's article *"I Spent 6 Months Tuning Claude Code. Here's the Exact Setup That Finally Worked."* The article describes an eight-layer stack; on an existing codebase, only the first three or four layers earn their keep on day one. The rest accrete as the project surfaces real need.

The article's worked examples — the citation-rag `CLAUDE.md`, the `services/retrieval/**` rule, the `retrieval-reviewer` subagent, the `new-rag-eval` skill, the formatter + push-gate hooks, the five-server `.mcp.json`, the nightly-eval GitHub Actions workflow, and the end-to-end replay — are bundled inside this skill at [`references/`](references/README.md). They're the verbatim templates this skill adapts during adoption. Read [`references/README.md`](references/README.md) for the index, or follow the per-step pointers below.

The skill also bundles three ready-to-install templates at [`assets/`](assets/):

- [`assets/CLAUDE-global-template.md`](assets/CLAUDE-global-template.md) — global behavioural rules (12 rules + 9 failure modes). Designed for `~/.claude/CLAUDE.md`.
- [`assets/python-rule-template.md`](assets/python-rule-template.md) — a path-scoped rule for Python projects, with YAML frontmatter already set. Drop into `.claude/rules/`.
- [`assets/typescript-rule-template.md`](assets/typescript-rule-template.md) — a path-scoped rule for JS/TS projects, with YAML frontmatter already set. Drop into `.claude/rules/`.

The general-purpose **`production-readiness-assessor`** is *not* bundled here as an asset — it ships as its own sibling skill in this plugin (`skills/production-readiness-assessor/`). Nothing to copy; see step 6.

## The 8 layers and what to install on day one of adoption

The article's eight layers, with adoption guidance:

| # | Layer | Install on day one of adoption? |
|---|---|---|
| 1 | Memory hierarchy (`CLAUDE.md`) | **Yes** — tailored to the surveyed repo, under ~500 tokens |
| 2 | Path-scoped rules | **Yes, 2–3 max** — only for directories with clear, already-existing conventions |
| 3 | Plan Mode | **Recommend** in the final report; nothing to install, it's a usage habit |
| 4 | Custom subagents | **No** — wait for the first repeated review task |
| 5 | Skills | **No** — wait for the first stable workflow worth packaging |
| 6 | Hooks (formatter + push gate) | **Formatter yes. Push gate only if a remote exists.** |
| 7 | MCP servers | **Three** — filesystem, library docs (context7), GitHub (only if remote is github.com) |
| 8 | Worktrees + headless | **No** — mention in the final report as a "when to graduate" cue |

The article's own "Floor and Ceiling" section is explicit about this minimum: short imperative memory file, two path-scoped rules for most-touched directories, one formatting hook, three servers, Plan Mode for risky tasks. That is exactly what this skill produces.

## When to trigger

The user is in a directory that already contains source files (not a `git init` from this morning) and wants Claude Code configured. Phrases:

- "set up Claude Code for this repo"
- "the .claude folder here is missing / empty — fix it"
- "retrofit the tuning stack into this codebase"
- "adopt the stack here"
- "give this repo a proper CLAUDE.md"

If the directory is empty or has only a couple of files, route elsewhere — adoption is the wrong frame.

## When the repo already has a `.claude/`

Three cases:

1. **Empty `.claude/`** — proceed normally.
2. **Existing `CLAUDE.md`** — read it first, treat it as authoritative for intent. Extend it (fill gaps) rather than overwrite. Show the proposed additions as a diff and wait for the user to accept.
3. **Existing rules / hooks / settings** — leave them alone. Only add what's missing. If `settings.json` already has a `PostToolUse` hook, do not replace it; either skip the formatter step or add alongside with a different matcher.

Never silently overwrite. When in doubt, ask.

## Workflow

### 1. Survey first (read-only)

Build a picture before writing anything. This is the whole reason adoption needs its own workflow — the article's tailored examples only work because they reflect a real codebase. Look at:

- **Top-level manifests**: `README.md`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Makefile`, `justfile`, lockfiles. These give you the language, package manager, and likely the lint/format/test commands.
- **Directory layout**: a shallow `tree -L 2` (or `Get-ChildItem -Depth 1`). Identify which top-level directories hold source, tests, configs, docs.
- **Test patterns**: peek into `tests/`. What runner? Any fixture conventions, marks, async style?
- **Linter / formatter config**: `.ruff.toml`, `.prettierrc*`, `.eslintrc*`, `rustfmt.toml`, `.editorconfig`. The day-one formatter hook should call whatever the repo already configures.
- **CI config**: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`. The canonical test/lint commands the team has already agreed on — these belong verbatim in CLAUDE.md.
- **Git remote**: `git remote -v`. Decides whether to add GitHub MCP and the push-to-main gate.
- **Existing `.claude/`**: read everything in it before writing anything new.

Use Glob/Grep aggressively. Don't skip this.

### 2. Confirm findings with the user (one batch)

Summarise what you found in one round of questions. Cover:

- Detected language(s) and package manager.
- The exact build / test / lint / format command strings (verbatim — these will go into CLAUDE.md).
- Whether a remote exists and the host (GitHub / GitLab / other).
- Two or three directories whose conventions are clear enough to warrant a path-scoped rule (let the user choose which to write).
- Any ambiguities: multiple package managers, no obvious test command, no formatter configured.

Wait for confirmation before writing.

### 3. Layer 1 — Write `.claude/CLAUDE.md`

This is the article's headline layer. Aim for 60–150 lines — short enough to stay inside the ~500-token cache window the article warns about (cache hit rates drop noticeably past that, and the Opus 4.7 tokenizer maps existing prompts to 1.0–1.35× more tokens, so ambient context is more expensive than it used to be).

**Templates**:
- [`references/example-claude-md.md`](references/example-claude-md.md) — the verbatim citation-rag `CLAUDE.md` with notes on how to substitute survey findings into each section.
- [`assets/CLAUDE-global-template.md`](assets/CLAUDE-global-template.md) — a tested set of 12 behavioural rules and 9 application-building failure modes (think-before-coding, surgical changes, fail-loud, UI grounding, state management, etc.). Designed to live at `~/.claude/CLAUDE.md` so it applies to every project.

#### Handling the global rules

Before writing the project `CLAUDE.md`, check whether the user already has global behavioural rules at `~/.claude/CLAUDE.md`:

```bash
test -f ~/.claude/CLAUDE.md && echo "exists" || echo "missing"
```

- **If it exists**, read it. If it already covers behavioural rules the user is happy with, don't duplicate them in the project file. The project `CLAUDE.md` should stay focused on project-specific facts (layout, build commands, conventions).
- **If it's missing**, ask the user whether to (a) install the bundled global template at `~/.claude/CLAUDE.md` so it applies across all their projects (preferred), or (b) prepend it to this project's `.claude/CLAUDE.md` so the rules apply at least here. Option (a) is the natural home for these rules; option (b) is the fallback when the user doesn't want to touch their home directory yet.

Either way, the project `CLAUDE.md` itself stays tailored to the surveyed repo — global rules complement it, they don't replace it.

Read the existing project `CLAUDE.md` (if any) first. **Never silently overwrite.** If gaps are clear, propose the additions as a diff. Then write the tailored version using the structure below.

```markdown
# {{project_name}}

{{one-sentence description, lifted from the README if possible}}

## Layout
- `{{dir_1}}/` — {{what lives here}}
- `{{dir_2}}/` — ...
- `tests/` — {{test runner + structure}}

## Build & test
- Install:           `{{detected install command}}`
- Unit tests:        `{{detected unit test command}}`
- {{Eval / integration harness if it has one}}:
- Lint + types:      `{{detected lint command}}`

## Canonical conventions
- {{Observed convention #1 — e.g. "All LLM outputs are validated with the pydantic models in `shared/schemas/`. No raw dict returns."}}
- {{Observed convention #2}}
- ...

## Guardrails (Claude: follow these literally)
- {{Observed test-isolation rule, e.g. "Never introduce network calls inside `tests/unit/`. Use fixtures in `tests/fixtures/` and the fakes in `tests/fakes/`."}}
- Prefer editing existing modules over adding new top-level packages.
- If a change touches `{{directory with a rule file}}`, read `.claude/rules/{{rule}}.md` before planning.
- Keep functions under ~40 lines. Split by responsibility, not by length.

## Before opening a PR
- {{Detected lint / test commands}}
- Update `CHANGELOG.md` under `## Unreleased`. (only if the repo has one)
- {{anything the CONTRIBUTING.md says, distilled to one line}}
```

The article's discipline applies in full: **imperative, not descriptive**. Don't write *"write clean code"* — write *"all functions must have type annotations"*. Every line must change behaviour. If you can't point at evidence for the line in the repo, drop it.

### 4. Layer 2 — Write 2–3 path-scoped rules

**Templates**:
- [`references/example-path-scoped-rule.md`](references/example-path-scoped-rule.md) — the verbatim retrieval rule from the article, plus guidance on good-vs-bad rule candidates and the `globs:` vs `paths:` caveat.
- [`assets/python-rule-template.md`](assets/python-rule-template.md) — a ready-made language rule for Python projects (PEP 8, ruff/black, type hints, uv, mutable defaults, pytest). Already has correct `globs:` for `**/*.py` and `**/*.pyi`.
- [`assets/typescript-rule-template.md`](assets/typescript-rule-template.md) — a ready-made language rule for JS/TS projects (Prettier/ESLint, strict TS, `??` vs `||`, immutability, pnpm, vitest, React). Already has correct `globs:` for `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/*.mjs`, `**/*.cjs`.

#### When to use the language template vs a hand-written rule

The language templates encode broadly-accepted conventions for their ecosystems. They're a good starting point when the surveyed repo already follows mainstream conventions (uses ruff/black, has type hints, uses pnpm, etc.). In that case:

```bash
cp assets/python-rule-template.md .claude/rules/python-conventions.md
# or
cp assets/typescript-rule-template.md .claude/rules/typescript-conventions.md
```

**Adapt before committing.** If the repo deviates from a template's defaults — uses `npm` instead of `pnpm`, uses Black at 100 chars instead of 88, doesn't use a type checker — edit the rule to match observed reality. The article's discipline still applies: every line must encode something already true in the code.

Beyond the language template, write *one or two* additional path-scoped rules for directories whose conventions are clear from the surveyed code. The shape to follow: YAML frontmatter with a `globs:` array, a short body of imperative rules grouped by concern.

```markdown
---
name: {{area-name}}-rules
description: Conventions for {{path}}/**. Loaded only when Claude is editing
  or planning changes inside {{area}}.
globs:
  - "{{path}}/**"
  - "tests/{{path}}/**"
---
# {{Area}} rules

## {{Concern 1, e.g. "Chunking" / "Handlers" / "Migrations"}}
- {{Imperative rule}}
- ...

## {{Concern 2}}
- ...

## Tests
- {{Test-isolation rule for this area}}
```

Important from the article's footnote: while `paths:` is the documented schema key, current versions sometimes drop it due to a known bug. **Use `globs:` for reliability.** If the user has confirmed `paths:` works for them, follow their preference.

Only write rules with concrete evidence in the code. Candidates:

- A `tests/` directory where every file follows the same fixture / mock pattern.
- An API / handler directory with a clear contract (e.g. every handler returns the same response shape).
- A migrations / schema directory with a clear policy.

Bad candidates: "this directory has a lot of files" (not a convention), "we might want a rule here someday" (speculative). The article is explicit that three or four short rule files beat one large root file because token savings compound on every turn — but a *speculative* rule costs tokens without earning them.

Cap adoption at two or three rules. The rest accrete as the user feels pain.

### 5. Layer 3 — Plan Mode (no install, just a recommendation)

Plan Mode separates *thinking* from *doing* and keeps exploration out of the main execution context. The article calls out three tiers — Simple, Visual, Deep — with Deep Plan using a read-only explore subagent.

There is nothing to install for this layer. In the final report (step 11), tell the user explicitly to use Plan Mode for any change with a non-trivial blast radius. This is a usage habit the configuration cannot enforce, but mentioning it doubles its uptake.

### 6. Layers 4 and 5 — Subagents and skills (defer custom; assessor ships with the plugin)

Do not write *custom, project-specific* subagents or skills during adoption. The article is clear that both layers earn their keep when a task starts *repeating* (subagents) or a workflow becomes *stable enough to package by name* (skills). Neither condition is observable on day one of adoption.

**The one general-purpose skill worth surfacing is `production-readiness-assessor`** — and it already ships as a sibling skill in this same plugin (`skills/production-readiness-assessor/`), so there is **nothing to install or copy**. Once this plugin is enabled, the assessor is available everywhere the plugin is. (This replaces the older behaviour of copying it into `~/.claude/skills/`; under plugin distribution that copy is redundant and only creates drift between copies.)

An existing codebase usually has real substance to score, so in the step 11 report tell the user they can trigger it any time with phrases like *"is this production ready?"*, *"audit this codebase before launch"*, or *"score this repo on prod readiness"*. The skill handles the rest, including its bundled `scan_signals.py` and the scorecard template.

Still create the empty `.claude/agents/` and `.claude/skills/` directories with short READMEs explaining what lives there (step 9). The READMEs should point at the bundled templates:

- [`references/example-subagent.md`](references/example-subagent.md) — the `retrieval-reviewer` subagent, with the tool-allowlist and model-downshift pattern explained.
- [`references/example-skill.md`](references/example-skill.md) — the `new-rag-eval` skill, with the `allowed-tools` and progressive-disclosure pattern explained.

When the user later asks "how do I add a subagent / skill?", point at these files. They're verbatim templates from the article, ready to adapt.

### 7. Layer 6 — Hooks (formatter always; push gate if there's a remote)

**Templates**:
- [`references/example-settings-json.md`](references/example-settings-json.md) — the full `settings.json` with formatter, push gate, and permission-denied audit log, plus the formatter detection table.
- [`references/example-push-gate.sh`](references/example-push-gate.sh) — the verbatim `gate_git_push.sh` from the article, with an adoption-time variant that also catches `master`.

The article's two practical hooks for the RAG service: post-tool formatter and pre-tool push-to-main gate.

**Post-tool formatter** — pick by detection:

| Detected config | Hook command |
|---|---|
| `pyproject.toml` with `[tool.ruff]` | `uv run ruff format $CLAUDE_TOOL_FILE_PATH` |
| `pyproject.toml` with `[tool.black]` | `black $CLAUDE_TOOL_FILE_PATH` |
| `.prettierrc*` or `prettier` in `package.json` | `npx prettier --write $CLAUDE_TOOL_FILE_PATH` |
| `rustfmt.toml` or any Rust crate | `rustfmt $CLAUDE_TOOL_FILE_PATH` |
| Go module | `gofmt -w $CLAUDE_TOOL_FILE_PATH` |

Wrap with `>/dev/null 2>&1 || true` so a formatter miss never blocks the agent and never pollutes its context. The article is explicit: *one-liner formatting hooks are the highest return on investment you can get.*

**Pre-tool push gate** — skip entirely if `git remote -v` is empty. Otherwise drop in the article's `gate_git_push.sh` verbatim, generalised to also catch `master`:

```bash
#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"
case "$cmd" in
  *"git push"*"origin main"*|*"git push"*"origin master"*|*"git push"*" main"*|*"git push"*" master"*)
    jq -nc '{
      "permissionDecision": "defer",
      "reason": "Push to main/master requires human approval."
    }'
    ;;
  *)
    jq -nc '{"permissionDecision": "allow"}'
    ;;
esac
```

Make it executable: `chmod +x .claude/hooks/gate_git_push.sh`. On Windows, this works through Git Bash / WSL; if the user is on pure PowerShell, write a `.ps1` equivalent and reference that path in `settings.json`.

**`settings.json`** that wires both (drop the `PreToolUse` block if no remote):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/gate_git_push.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "{{detected formatter command}} >/dev/null 2>&1 || true" }
        ]
      }
    ],
    "PermissionDenied": [
      {
        "hooks": [
          { "type": "command", "command": "jq -c . >> .claude/logs/denied.jsonl" }
        ]
      }
    ]
  }
}
```

The `PermissionDenied` audit log is cheap and helps debug the push gate later — keep it.

### 8. Layer 7 — MCP servers (three for adoption)

**Template**: [`references/example-mcp-json.md`](references/example-mcp-json.md) — the article's full five-server `.mcp.json` plus the three-server adoption variant and graduation cues.

The article argues for exactly five servers in a mature setup: code-graph, GitHub, filesystem, search, context server. On day one of adoption, install three:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

If `git remote get-url origin` returns a `github.com` URL, also include:

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
}
```

…and tell the user they need `GITHUB_TOKEN` in their shell. **Do not put the token in the file.** Do not add GitHub MCP if there is no remote — its tool schemas would burn ambient tokens on every turn for capabilities the agent cannot use. The article is blunt: *tool schemas are not free.*

Defer the code-graph server (vexp or similar) and the search server until the codebase is large enough or the workflow proves the need. The article cites a 65–70% token reduction from vexp on *long-running* agent setups — that benefit is real but doesn't materialise on day one. Adding it pre-emptively means an extra server's schemas in every turn without the corresponding token wins.

**About `anthropic/maxResultSizeChars`**: the article notes the April 2026 release lets servers set this annotation in tool `_meta` fields to keep large library doc pulls inline. Nothing to configure here — context7 and the GitHub server already use it appropriately. Just be aware of it when picking servers later.

### 9. Empty subdirectories with READMEs

Create `.claude/rules/`, `.claude/agents/`, `.claude/skills/`, `.claude/hooks/` and drop a short README in each. The READMEs serve discoverability and mini-docs — they tell the user (or the agent on a later turn) where new things go, and they include a copy-paste example.

Write each README with an example drawn from the article so the user has a working reference right next to where it gets installed:

- **`rules/README.md`** — point at the article's `services/retrieval/**` rule as the example.
- **`agents/README.md`** — point at the article's `retrieval-reviewer` subagent.
- **`skills/README.md`** — point at the article's `new-rag-eval` skill (and note that user-level skills live in `~/.claude/skills/`).
- **`hooks/README.md`** — explain that one hook is already wired (post-tool formatter, and push gate if remote) and point at the article's gate example as the shape for adding more.

Do not create `.claude/logs/` — that directory appears the first time the `PermissionDenied` audit hook writes to it. `.gitignore` should still exclude it (step 10).

### 10. Update `.gitignore`

Append (never replace) these lines if absent:

```
# Claude Code
.claude/logs/
.claude/local/
```

If no `.gitignore` exists at all, write a minimal one with the Claude entries plus the obvious entries for the detected language (`__pycache__/`, `node_modules/`, `target/`, etc.).

### 11. Do not auto-commit. Report what you did.

Show the user a summary in chat. They own the first commit.

The report should include:

- Files created or modified, as clickable paths.
- Anything deliberately skipped and why ("no remote, so no push gate"; "no formatter configured in the repo, so no post-tool hook — let me know if you want one wired").
- A short "what's next" list lifted directly from the article's *Floor and Ceiling* section, adapted to this repo:
  - Use **Plan Mode** for any task with non-trivial blast radius.
  - Add a **subagent** in `.claude/agents/` the first time a review task repeats.
  - Add another **path-scoped rule** when a new directory grows enough to want consistency.
  - Add a **skill** in `.claude/skills/` when a workflow is stable enough to invoke by name.
  - Run the **`production-readiness-assessor`** (ships with this plugin — just ask *"is this production ready?"*) before any launch or major release for an evidence-based scorecard and gate check.
  - Add **worktrees** when you catch yourself switching branches more than twice an hour.
  - Add **headless mode** + a GitHub Actions workflow when you want the agent shipping while you sleep — copy [`references/example-github-actions.yml`](references/example-github-actions.yml) as the starting point. The end-to-end "ninety minute shipment" narrative is in [`references/example-replay.md`](references/example-replay.md) and shows how all eight layers compose during a real task.

## Do not

- Do not write a generic stub `CLAUDE.md`. The whole reason this skill exists is to produce a tailored one. If you're filling in placeholders rather than observed facts, survey more.
- Do not silently overwrite an existing `.claude/CLAUDE.md`, `settings.json`, or hook script. Read what's there, then offer additions as a diff.
- Do not write speculative path-scoped rules. The article's discipline: each rule must encode something already true in the code.
- Do not install more than three MCP servers during adoption. Tool schemas cost tokens every turn — Anthropic's own Tool Search documentation puts 50 tools at 10,000–20,000 tokens per turn without lazy loading.
- Do not add the GitHub MCP server without checking the remote.
- Do not commit anything. Surface the changes; let the user stage and commit.
- Do not write custom subagents or project-level skills during adoption — those are layers 4 and 5, and the article is clear they're "add when a task starts repeating" / "add when a workflow is stable."

## Why this is the article's "floor"

The article spends most of its length describing the full eight-layer stack as it appears in a *mature* configuration. The closing *Floor and Ceiling* section then strips the stack back to the minimum that earns its keep, and tells you when to add each missing layer:

> If you will not do everything you should at least do the minimum. Build a short imperative memory file at the project root. Write two path-scoped rule files for the directories you touch the most. Add one formatting hook. Install three servers for your repository, your filesystem, and your library documentation. Force yourself to use Plan Mode for any task with a risk of being wrong.
>
> Add subagents when a task keeps repeating. Add skills when a workflow is stable enough to package. Add worktrees when you catch yourself switching branches more than twice an hour. Add headless mode when you want the agent shipping code while you sleep.

This skill is that floor, installed by survey rather than by template. Each subsequent layer is a *graduation* the user makes when the project surfaces the matching pain — and the READMEs in the empty subdirectories carry the article's example for each layer as the on-ramp.
