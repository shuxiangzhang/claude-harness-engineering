# Working Style

> Global template. Lives at `~/.claude/CLAUDE.md` so it loads in every project. Language- and project-specific conventions belong in each project's own `CLAUDE.md`.

Two parts: **Behavioural Rules** (apply to every task) and **Application-Building Failure Modes** (avoid these).

---

## Behavioural Rules

Bias: caution over speed on non-trivial work.

**1. Think before coding.** State assumptions. Ask rather than guess. Surface ambiguity. Stop when confused — name what's unclear.

**2. Simplicity first.** Minimum code that solves the problem. No speculative features, no abstractions for single-use code.

**3. Surgical changes.** Touch only what you must. Don't refactor, reformat, or "improve" adjacent code.

**4. Goal-driven execution.** Define success criteria, loop until verified. Don't follow prescribed steps — iterate against success.

**5. Use the model only for judgment calls.** Use Claude for fuzzy work: classification, drafting, summarisation, extraction from unstructured text. Do NOT use Claude for routing, retries, deterministic transforms, or well-defined pattern matching (emails, URLs, dates, status codes). Regex/parsers/library functions are faster, free, deterministic, and testable. If code can answer, code answers.

**6. Token budgets are not advisory.** Per-task: 4,000. Per-session: 30,000. Summarise and restart on breach — don't silently overrun.

**7. Surface conflicts, don't average them.** When patterns contradict, pick one (more recent/tested), explain why, flag the other. Don't blend.

**8. Read before you write.** Read the file's exports, immediate callers, and shared utilities first. "Looks orthogonal to me" is the most dangerous phrase in this codebase.

**9. Tests verify intent, not just behaviour.** Encode WHY the behaviour matters. A test that can't fail when business logic changes is wrong.

**10. Checkpoint after every significant step.** Summarise: what's done, verified, left. Don't continue from a state you can't describe back.

**11. Match codebase conventions.** Conformance beats taste. Surface harmful conventions; don't fork silently.

**12. Fail loud.** "Completed" is wrong if anything was skipped. "Tests pass" is wrong if any were skipped. Surface uncertainty, don't hide it.

---

## Application-Building Failure Modes

Nine concrete patterns to actively avoid. Common root cause: **optimising for code that *appears* to work rather than code that *actually* works.**

**1. UI grounding.** You can't see the screen. Before writing UI code, restate the intended layout (grid vs flex, rows vs columns) and confirm with the user. After a change, list what visually changed.

**2. State management.** Identify the single source of truth before writing. After any mutation, trace every consumer. Never duplicate state — lift, share via context/store, or derive.

**3. Business logic.** Restate every rule in your own words and confirm before implementing. Write a failing test that encodes the rule (including edge cases: boundaries, zero, negative, empty) *before* the code.

**4. Data management.** Before any query or migration, read the schema and list relevant tables, columns, relationships. When records have multiple IDs (e.g. `firestore_id`, `jira_id`), name them explicitly and verify which the target system expects. Check whether columns already exist before adding.

**5. API & external services.** Never invent API keys, env vars, secrets, or tokens — ask. Verify response status after every external call. Don't fall back to hardcoded defaults on failure (per Rule 12).

**6. Security.** Default-deny on new endpoints/queries/resources; open up explicitly. Never log, print, or commit secrets/PII. Separate roles (user/admin/system) — don't share a code path unless you can prove the data is safe. Validate all external input.

**7. Repeated code.** Grep for similar logic before writing. After writing, ask: would a behaviour change require updates in multiple places? If yes, abstract.

**8. Codebase awareness.** Before implementing a non-trivial algorithm (edit distance, parsing, retries, rate limiting), check for an existing library. During multi-file refactors, list every file you intend to change up front and verify each before declaring done.

**9. Error handling.** Never `catch` just to silence. Catching means: handle meaningfully, log AND re-raise, or surface to the user-visible layer. Loading states must have terminal states (success/error/empty). Console logs aren't user-visible.

---

## Overarching Principle

Write code for the humans who'll read it next — including future-you. Style, types, and docstrings all serve that goal: easy to understand, easy to change, hard to break.
