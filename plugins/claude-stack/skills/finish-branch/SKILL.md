---
name: finish-branch
description: Use when implementation on a development branch is complete, tests pass, and the work needs integrating — deciding between merge, PR, keeping the branch, or discarding it, plus worktree cleanup.
---

# finish-branch

## Overview

Close out a development branch deliberately: verify → present options → execute → clean up. No work is integrated unverified, and no work is destroyed unconfirmed.

## Steps

### 1. Verify tests — before anything else

Run the project's full suite. **Failing → stop.** Show the failures; nothing merges or ships until green. (Claims about the result follow `verify-done`: fresh run, read output.)

### 2. Determine the base branch

`git merge-base HEAD main` / `master`, or ask: "This branch split from main — correct?"

### 3. Present exactly four options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Keep it concise — no per-option essays.

### 4. Execute

- **1 — Merge locally**: checkout base → pull → merge → **run tests on the merged result** → delete the feature branch. Then cleanup (step 5).
- **2 — PR**: push with `-u`, `gh pr create` with a summary + test-plan body. Worktree stays (the PR may need fixes).
- **3 — Keep**: report branch name and worktree path. Touch nothing.
- **4 — Discard**: destructive — require the user to type `discard` after seeing exactly what dies (branch, commits, worktree). Only then force-delete.

### 5. Worktree cleanup

Options 1 & 4: if the branch lived in a worktree, `git worktree remove` it. Options 2 & 3: keep it.

| Option | Merge | Push | Keep worktree | Delete branch |
|--------|-------|------|---------------|---------------|
| 1 Merge locally | ✓ | – | – | ✓ |
| 2 Create PR | – | ✓ | ✓ | – |
| 3 Keep as-is | – | – | ✓ | – |
| 4 Discard | – | – | – | ✓ (force) |

## Never

- Proceed with failing tests, or merge without re-running tests on the merged result
- Delete work without the typed confirmation
- Force-push without an explicit request
- Replace the four options with an open-ended "what next?"

## Lineage

Distilled from [obra/superpowers](https://github.com/obra/superpowers)' `finishing-a-development-branch` skill (MIT).
