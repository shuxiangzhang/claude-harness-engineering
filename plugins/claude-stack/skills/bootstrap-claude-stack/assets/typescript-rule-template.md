---
name: typescript-conventions
description: JavaScript / TypeScript code conventions for this project.
  Loaded only when Claude is editing or planning changes to JS/TS files.
globs:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.mjs"
  - "**/*.cjs"
---
# JavaScript / TypeScript Conventions

> Path-scoped rule. Pairs with the global behavioural rules at the
> project root `CLAUDE.md` (or `~/.claude/CLAUDE.md`).

## Style

**Prettier** (format) + **ESLint** (lint). 2 spaces, 100-char lines, semicolons unless the project opts out. `camelCase` (vars/functions), `PascalCase` (classes/types/components), `UPPER_SNAKE_CASE` (constants). File names per project (`kebab-case` modules, `PascalCase` components).

## Strict TypeScript

`strict: true`. No `any` — use `unknown` and narrow with type guards. Avoid `as` assertions; justify in a comment if you must.

```ts
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "id" in v;
}
if (!isUser(response)) throw new Error("Invalid user");
```

`type` for unions/primitives, `interface` for extensible object shapes. `readonly` and `as const` for immutable data.

## Variables, Equality, Nullish

`const` by default. `let` only when reassignment is needed. Never `var`.

Always `===`/`!==`. `??` for nullish defaults (`null`/`undefined` only); `||` only when you want any falsy to fall back. Use `?.` over manual null checks.

```ts
const name = user?.profile?.name ?? "Anonymous";  // good
```

## Imports

All at top. Groups: external → internal → relative, blank line between (`eslint-plugin-import` enforces). Dynamic `import()` only for code-splitting, optional features, or lazy routes.

Prefer named exports over default — easier to refactor. Avoid barrel files in large codebases (hurts tree-shaking).

## Functions & Async

Arrow functions for callbacks/inline; `function` for top-level when hoisting matters. Small, pure, no argument mutation. `async/await` over `.then()` chains. Always handle rejections. `Promise.all` for parallel, `for await` for sequential async.

```ts
try {
  const [user, posts] = await Promise.all([fetchUser(id), fetchPosts(id)]);
  return { user, posts };
} catch (err) {
  logger.error("Failed to load user data", { id, err });
  throw err;
}
```

## Immutability

Don't mutate arguments. `map`/`filter`/`reduce`/spread, not `.push`/`.splice` on shared data. `readonly` arrays, `Readonly<T>` for protected data.

```ts
function addItem(items: readonly string[], item: string): string[] {
  return [...items, item];
}
```

## React (if applicable)

Function components with hooks unless codebase uses classes. Components < ~150 lines. Co-locate component/styles/tests. Type props with `interface`/`type`:

```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
}

export function Button({ label, onClick, variant = "primary" }: ButtonProps) {
  return <button className={variant} onClick={onClick}>{label}</button>;
}
```

Hooks rules: no conditional calls, full `useEffect` deps, `useMemo`/`useCallback` only with measured benefit.

## Error Handling

Throw `Error` (or subclasses), never strings or plain objects. Custom classes for domain errors. Catch narrowly. Never empty `catch {}`.

```ts
class UserNotFoundError extends Error {
  constructor(public userId: string) {
    super(`User ${userId} not found`);
    this.name = "UserNotFoundError";
  }
}
```

## Package Management — `pnpm`

Use `pnpm`. Don't mix `npm`/`yarn`/`pnpm` (conflicting lockfiles).

```bash
pnpm install                          # from lockfile
pnpm add zod                          # runtime
pnpm add -D vitest @types/node        # dev
pnpm remove zod
pnpm test
```

Commit `pnpm-lock.yaml`. CI: `pnpm install --frozen-lockfile`.

## Dependency Hygiene

Pin via lockfile, `pnpm audit` + Dependabot/Renovate for vulnerabilities, cadence-based updates for non-security, read release notes before major bumps. The JS ecosystem ships breaking majors often — never auto-update framework deps.

## Project Structure

```
my-project/
├── package.json, pnpm-lock.yaml, tsconfig.json, .eslintrc.cjs, .prettierrc
├── src/{index.ts, lib/}
└── tests/
```

## Testing

**Vitest** (or Jest in legacy). Fast, isolated, clearly named. Test behaviour, not implementation. Flat suites over nested `describe`.

```ts
it("rejects login with wrong password", async () => {
  await expect(login("alice", "wrong")).rejects.toThrow();
});
```

## Performance

Don't optimise prematurely. Profile with browser DevTools or `node --inspect`. React DevTools profiler for re-renders. Stream over loading entire datasets.
