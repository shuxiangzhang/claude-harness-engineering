# Example: the 90-minute replay (end-to-end)

The article's *"Replay"* section, showing how the eight layers compose during a real task: adding citation-backed answer generation to the existing retrieval service, writing the evals, and opening a PR. Useful as a reference for what the stack *enables* once installed.

## The narrative (verbatim from the article)

> We have the stack. Let us watch the ninety minute shipment using actual artifacts.
>
> The session starts. The engineer opens the project and creates the feature worktree. The memory file and rules load automatically. The five servers connect.
>
> The engineer enters Deep Plan mode. The explore subagent maps the current retrieval paths and the planner outputs a concrete document.

```markdown
## Implementation Plan: Citation-Backed Generation
1. **Modify `services/retrieval/search.py`**: Ensure `Chunk` objects attach `citation_id` via `shared.citations.make_citation_id`.
2. **Update `services/answer/generator.py`**: Inject `[Source: {citation_id}]` into the Gemini system prompt context block.
3. **Create Eval**: Add `evals/suites/citations/defective-charger.json` to verify strict citation formatting.
```

> The engineer reviews the plan and locks it in. Implementation runs in the main worktree. When the agent finishes modifying the retrieval logic, it invokes the `retrieval-reviewer` subagent. The subagent returns a hard blocker based on the path-scoped rules.

```markdown
**Verdict: blocker**
* `services/retrieval/search.py`: You hand-rolled a UUID for the citation ID on line 42. Rule `.claude/rules/retrieval.md` requires `shared.citations.make_citation_id`.
* `tests/retrieval/test_search.py`: Missing `@pytest.mark.integration` on the new database test.
```

> The agent fixes the hand-rolled ID and the missing decorator. The post-tool hook keeps the formatting clean after every single write operation.
>
> Parallel work begins. The second worktree uses the `new-rag-eval` skill to rewrite the evaluations. The headless run executes the final evaluation harness and generates the diff.

```json
{
  "suite": "citations",
  "cases_run": 45,
  "grounded_citation_rate": {"previous": 0.82, "current": 0.98, "delta": "+0.16"},
  "unsupported_claims": {"previous": 12, "current": 0, "delta": "-12"},
  "status": "PASS"
}
```

> The deferred permission pauses the push. The engineer approves it. The pull request opens via the GitHub server with the full change set and the evaluation diff attached.
>
> This assumes the task is well scoped and the stack is already built. The first time you build this out it takes an afternoon. Every task after that compounds.

## What this shows about each installed layer

- **Layer 1 (`CLAUDE.md`)** sets the citation contract that the reviewer enforces later.
- **Layer 2 (path-scoped rule)** is the source of the blocker — `make_citation_id` is mandated by `.claude/rules/retrieval.md`.
- **Layer 3 (Plan Mode)** produces the explicit edit list before any destructive action.
- **Layer 4 (`retrieval-reviewer`)** runs read-only against the diff and catches the contract violation.
- **Layer 5 (`new-rag-eval` skill)** is invoked by name to add the eval case.
- **Layer 6 (formatter hook + push gate)** keeps the file clean between turns and defers the push for human approval.
- **Layer 7 (GitHub MCP)** opens the PR.
- **Layer 8 (worktrees + headless)** lets the eval harness run in parallel and the deferred push wait for approval out-of-band.

## The article's closing line

> The stack is the workflow. The workflow is the multiplier. The prompt is just the last five percent.
