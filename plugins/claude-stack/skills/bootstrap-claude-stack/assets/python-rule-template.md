---
name: python-conventions
description: Python code conventions for this project. Loaded only when
  Claude is editing or planning changes to Python files.
globs:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Conventions

> Path-scoped rule. Pairs with the global behavioural rules at the
> project root `CLAUDE.md` (or `~/.claude/CLAUDE.md`).

## Style

PEP 8. 4 spaces, no tabs. 88-char lines (Black). `snake_case` (vars/functions), `PascalCase` (classes), `UPPER_CASE` (constants). Two blank lines between top-level defs, one between methods.

Tools (automated, don't hand-format): **Black** (format), **isort** (imports), **Ruff** (lint). Run `uv run ruff check . && uv run ruff format .` before commit.

## Naming

Reveal intent: `user_count` > `n`, `calculate_monthly_revenue()` > `calc()`. Single letters only for short loops or math (`i`, `x`). Booleans read as questions: `is_active`, `has_permission`.

## Imports

All at the top, grouped per PEP 8: stdlib → third-party → local, blank line between groups (`isort` handles it). Local imports only with a comment explaining why: circular imports, optional deps (`if x: import reportlab`), or deferring an expensive import (e.g. `tensorflow`) only one path needs.

## Functions

One thing well. Name contains "and" → split. Under 20-30 lines. Prefer pure functions.

## Error Handling

Specific exceptions, never bare `except:`. Context managers (`with`) for resources.

```python
try:
    data = json.loads(response)
except json.JSONDecodeError as e:
    logger.warning("Failed to parse: %s", e)
    data = {}
```

## Idioms

```python
squares = [x**2 for x in numbers if x > 0]         # comprehensions
for i, item in enumerate(items): ...               # not range(len())
for name, score in zip(names, scores): ...         # parallel iteration
message = f"Hello, {user.name}!"                   # f-strings
first, *rest = my_list                             # unpacking
```

Use `pathlib.Path`, not string paths. `dataclasses`/`pydantic` over bare dicts for fixed shapes. `is None` not `== None`. `if not seq` not `len(seq) == 0`. No `from x import *`.

## Mutable Defaults

Never. They share across calls.

```python
# Bad
def add(item, items=[]): items.append(item); return items

# Good
def add(item, items=None):
    items = items or []
    items.append(item)
    return items
```

## Type Hints

Annotate every public function. Built-in generics (`list[str]`, `dict[str, int]`) — don't import `List`/`Dict` from `typing`. `X | None` over `Optional[X]`. Accept abstract types (`Iterable`, `Sequence`, `Mapping` from `collections.abc`); return concrete.

```python
from collections.abc import Iterable

def sum_all(values: Iterable[float]) -> float: ...
def find_user(user_id: int) -> User | None: ...
```

Useful: `Literal`, `Final`, `Self` (3.11+), `Protocol`. `Any` sparingly. CI runs `uv run mypy src/` — type errors fail the build.

## Docstrings

Triple double-quotes (PEP 257), Google style, on all public modules/classes/functions. First line: imperative summary ("Return the sum"). Describe what params *mean*, not their types.

```python
def fetch_user(user_id: int, include_inactive: bool = False) -> User:
    """Fetch a user from the database.

    Args:
        user_id: Unique identifier.
        include_inactive: Include deactivated accounts.

    Returns:
        The matching User.

    Raises:
        UserNotFoundError: If no user exists with that ID.
    """
```

Don't restate the obvious. Update docstrings in the same commit as behaviour changes.

## Package Management — `uv`

Use `uv`. Not `pip`, `pipenv`, `poetry`, or `pyenv`.

```bash
uv sync                              # set up / re-sync
uv add httpx                         # runtime dep
uv add --dev pytest ruff mypy        # dev dep
uv add --group docs mkdocs           # named group
uv remove httpx
uv run python -m myapp               # run in env
uv run pytest
uv lock --upgrade-package httpx      # selective upgrade
```

CI: `uv sync --frozen --no-dev && uv run --frozen pytest`. Commit `pyproject.toml`, `uv.lock`, `.python-version`. Gitignore `.venv/`.

## Dependency Hygiene

Fresh and secure, not bleeding-edge. Pin via lockfile. Run `uv run pip-audit` (or Dependabot/Renovate) for vulnerabilities — prioritise those. Bump non-security deps on a cadence (monthly/sprint), not continuously. Read changelogs before major-version bumps.

## Project Structure

```
my_project/
├── .python-version, pyproject.toml, uv.lock, README.md
├── src/my_package/{__init__.py, module.py}
└── tests/
```

## Testing

`pytest`. Fast, isolated, clearly named (`test_user_cannot_login_with_wrong_password`). Test behaviour, not implementation. Fixtures for setup, parametrize for multiple inputs. Run: `uv run pytest`.

## Performance

Don't optimise prematurely. Profile (`cProfile`, `py-spy`) before optimising. Generators for large data. `numpy`/`pandas`/`polars` for heavy numeric/tabular work.
