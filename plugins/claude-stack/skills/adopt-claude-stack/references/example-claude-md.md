# Example: tailored `CLAUDE.md` (Layer 1)

The verbatim `CLAUDE.md` from the article's citation-rag service. This is the target shape for adoption — short, imperative, layout-aware, and grounded in observed code.

## Why this shape works

From the article:

> This tells the agent exactly what the directories do. It defines the strict citation contract between the retrieval node and the answer node. It establishes hard guardrails for the test suite that prevent the model from hallucinating a network mock.

Token discipline (also from the article):

> Cache hit rates drop noticeably past ~500 tokens in my own workloads. The new Opus 4.7 tokenizer maps existing prompts to roughly 1.0 to 1.35× more tokens, meaning the exact same workload is now more expensive if you do not strictly control your ambient context.
>
> Keep the file under 200 lines. Keep it imperative. Do not write descriptive suggestions like "write clean code". Write literal rules like "all functions must have TypeScript type annotations". Every line must actually change behavior.

## The full example

```markdown
# citation-rag
Retrieval + answer-generation service. LangGraph-based pipeline,
PostgreSQL+pgvector retrieval, Gemini answer generation, eval harness
in `evals/`.

## Layout
- `services/retrieval/`  — chunking, embedding, reranker, citation packer
- `services/answer/`     — prompt templates, generator node, guardrails
- `shared/`              — schemas, tracing, settings
- `evals/`               — golden sets, runners, scoring

## Build & test
- Install:           `uv sync`
- Unit tests:        `uv run pytest -q`
- Eval harness:      `uv run python -m evals.run --suite citations`
- Lint + types:      `uv run ruff format . && uv run mypy .`

## Canonical conventions
- The canonical answer prompt lives at `services/answer/prompts/v4.md`.
  Do not edit `v3.md` because it is frozen for regression evals.
- All LLM outputs are validated with the pydantic models in
  `shared/schemas/answers.py`. No raw dict returns from generator nodes.
- Retrieval always returns `Chunk` objects with a `citation_id`.
  The answer node must emit citations using those exact ids.

## Guardrails (Claude: follow these literally)
- Never bump the model version string without updating
  `evals/snapshots/<version>.json` in the same commit.
- Never introduce network calls inside `tests/unit/`. Use fixtures in
  `tests/fixtures/` and the fakes in `tests/fakes/`.
- Prefer editing existing modules over adding new top-level packages.
- If a change touches `services/retrieval/`, read `.claude/rules/retrieval.md`
  before planning.
- Keep functions under ~40 lines. Split by responsibility, not by length.

## Before opening a PR
- Run the eval harness and attach the diff output to the PR body.
- Update `CHANGELOG.md` under `## Unreleased`.
- Use the `claude-pr-checklist` skill.
```

## How to adapt this for the user's repo

Every section above is observed reality in the citation-rag repo. Adoption replaces each line with observed reality from the *user's* repo:

| Section | What to substitute |
|---|---|
| Title + one-liner | Project name and a one-sentence description, ideally lifted from `README.md` |
| Layout | The directories that actually exist (shallow tree), with a 3–8 word description each |
| Build & test | The exact command strings from `pyproject.toml` / `package.json` / CI config |
| Canonical conventions | Patterns visible in the code — schema modules, version-frozen artefacts, contracts between layers |
| Guardrails | Observed test-isolation rules, any "never edit X" invariants, any cross-cut rules ("touch directory Y → read rule Z") |
| Before opening a PR | What the user's CONTRIBUTING.md or PR template actually requires |

The discipline: **every line must name something the user can verify by reading the code right now.** If you can't point at evidence, drop the line.
