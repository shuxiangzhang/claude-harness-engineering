# Example: path-scoped rule (Layer 2)

The article's `.claude/rules/retrieval.md`, scoped to `services/retrieval/**`.

## Why path-scoped rules

From the article:

> Once you discipline your root memory you still have file-specific instructions. You put them in path-scoped rules.
>
> The pattern uses YAML frontmatter. You define an array of glob paths. The tool loads the rule file only when it touches a matching file. It costs zero tokens the rest of the time. If the agent is editing database migration scripts it does not need to read frontend styling conventions.
>
> Three or four short rule files beat one large root file. The token savings compound on every turn of the conversation.

## Schema-key caveat (from the article's note)

> While `paths:` is the documented schema key, current versions sometimes drop it due to a known bug. Using `globs:` or a CSV format works more reliably in practice if you notice your rules being silently ignored.

**Default to `globs:`** unless the user has confirmed `paths:` works for them.

## The full example

```markdown
---
name: retrieval-rules
description: Conventions for services/retrieval/**. Loaded only when
  Claude is editing or planning changes inside the retrieval service.
globs:
  - "services/retrieval/**"
  - "tests/retrieval/**"
---
# Retrieval service rules

## Chunking
- Use `shared/chunking.semantic_chunker` for all document ingest.
  Do not introduce a second chunker without updating the eval snapshot.
- Chunk size target: 512 tokens, 64 overlap. Changes require an ADR.

## Reranker
- The reranker interface is `services/retrieval/reranker.Reranker`.
  New backends must implement it, not parallel it.
- Never rerank more than the top 50 hits from vector search. Rerank latency
  is the #1 service SLO risk.

## Citations
- Every `Chunk` returned from retrieval must carry a stable `citation_id`.
- Citation ids are produced by `shared/citations.make_citation_id`. Do not
  hand-roll ids anywhere else.
- The answer node assumes `citation_id` is URL-safe. Do not change that
  without updating `services/answer/citation_packer.py` in the same diff.

## Tests
- Unit tests for retrieval must never hit the embedding API. Use the fake
  embedder in `tests/fakes/embeddings.py`.
- Integration tests live under `tests/retrieval/integration/` and are
  opt-in via `pytest -m integration`.
```

## How to adapt this for the user's repo

Pattern: one or two `## Concern` sections (Chunking / Reranker / Citations / Tests in the example), each with two to four imperative bullets. Each bullet should name a file, function, or interface that exists in the repo.

Good candidates for an adoption-time rule:

- A test directory where every file follows a consistent fixture pattern → encode the pattern.
- An API / handlers directory with a clear contract (e.g. every handler returns the same response shape) → encode the contract.
- A migrations / schema directory with a clear policy (e.g. "no destructive migrations without an ADR") → encode the policy.

Bad candidates:

- "This directory has a lot of files." Not a convention.
- "I think we might want a rule here someday." Speculative — wait for the user to feel pain.

Cap adoption at 2–3 rule files. The rest accrete as the user feels pain.
