---
name: add-dependency
description: Use before adding a new third-party dependency or upgrading an existing one — "add a library for X", "use <package>", "pull in a dep to do Y", "upgrade <package>", "bump dependencies". Guards against needless dependencies, supply-chain risk, license problems, and breaking upgrades. Ends by running the suite to prove nothing broke.
---

# add-dependency

## Overview

Every dependency is permanent attack surface, build weight, and maintenance you don't own. Add one deliberately.

**Core principle:** the cheapest dependency is the one you didn't add. The second cheapest is the one you vetted before adding.

## Adding a new dependency

1. **Do you need it?** Check the standard library and the deps you already have first — grep the codebase for an existing helper. A few lines you own often beat a transitive tree you don't. Trivial functionality (left-pad, is-odd) is never worth a dependency.
2. **Vet the candidate.** Maintenance (recent commits, open-vs-closed issues), adoption, **license** compatibility with this project, transitive weight, and known advisories. Watch for typosquats — confirm the exact package name and owner.
3. **Add it pinned.** Use the project's package manager so the lockfile updates (`uv add`, `pnpm add`, `cargo add`, `go get`, etc.). Never hand-edit the manifest and skip the lock. Add to the right group (runtime vs dev).
4. **Prove the suite still passes** (`verify-done`). A new dep can shift transitive versions.

## Upgrading an existing dependency

1. **Read the changelog / release notes** between the current and target version — specifically the **breaking changes** and deprecations. Major-version bumps are guilty until proven innocent.
2. **Upgrade via the package manager**, refresh the lockfile, prefer one dependency (or one cohesive group) per change so a regression is bisectable.
3. **Run the full suite and the type/lint checks.** Address deprecations now, not "later."
4. **`verify-done`** with the fresh run before claiming the upgrade is safe.

## Security & guardrails

- Never install from an unverified source, a random fork, or a URL the user can't vouch for.
- Never commit a dependency that pulls secrets/telemetry without the user's explicit awareness.
- A failed audit (`npm audit`, `pip-audit`, `cargo audit`, etc.) on the new/changed dep is a blocker — surface it, don't silently proceed.

## Do not

- Do not add a dependency for something the stdlib or an existing dep already does — grep first.
- Do not edit the manifest without updating the lockfile.
- Do not upgrade across a major version without reading its breaking-changes notes.
- Do not declare the add/upgrade done without a fresh green test + audit run.

## Lineage

Operationalizes the dependency-management dimension of `production-readiness-assessor` and Failure Mode #8 (check for an existing library before implementing) from the global working rules.
