---
name: production-readiness-assessor
description: Assess whether a codebase is production-grade by inspecting it across thirteen dimensions — testing, error handling, observability, security, maintainability, CI/CD, configuration, performance, documentation, operations, data management, compliance & governance, and dependency management. Use this skill whenever the user asks to evaluate production readiness, check if a project is ready to ship, audit a codebase, do a pre-launch review, score a repo, or any phrasing like "is this production ready", "production grade check", "prod readiness audit", "is my code ready for prod", "assess the codebase before launch", "how close to prod are we". The skill inspects the actual repository (configs, CI workflows, tests, docs, dependency manifests, migration history, licence files), adapts scoring to whatever tech stack it detects, cites concrete evidence for every score, and produces a Markdown scorecard with gap analysis and a prioritised action plan.
---

# Production Readiness Assessor

Produce a thorough, evidence-based assessment of whether a codebase is production-grade. The goal is a report the user can defend in front of their team and re-run later to track improvement.

## When this skill is right

Trigger when the user wants a holistic readiness check across multiple operational concerns. Phrases that signal this:

- "Is this codebase production ready?"
- "Audit my project before we launch"
- "How close are we to prod-grade?"
- "Score my repo on production readiness"
- "Do a pre-launch review of this service"
- "Check the readiness of this project"

If the user wants a narrower thing — code review for correctness, security audit specifically, performance tuning, style review — this skill is broader than they need. Offer it anyway if it seems like they'd benefit from the full picture, but don't force it.

## Inputs to gather upfront

Before inspecting anything, batch these questions to the user using AskUserQuestion (skip any they've already answered in conversation):

1. **Where is the codebase?** Local folder path, git URL, or uploaded files.
2. **Project context** — one paragraph: what does it do, who uses it, what stage is it at.
3. **Cost of failure** — low / medium (standard) / high / critical. This sets the scoring bar.
4. **Any dimensions to skip?** E.g., observability is less relevant for a pure CLI tool; performance/scalability may not matter for an internal one-off.

If the user gives you a repo and asks you to "just go", use sensible defaults (medium / standard production) and call that out in the report.

## The thirteen dimensions

The assessment covers these in order. Each dimension is scored 1–5 on multiple checks, then summed:

1. **Functional Correctness & Testing** (6 checks, 30 max)
2. **Error Handling & Resilience** (6 checks, 30 max)
3. **Observability** (6 checks, 30 max)
4. **Security** (6 checks, 30 max)
5. **Maintainability & Code Quality** (6 checks, 30 max)
6. **CI/CD & Release Process** (6 checks, 30 max)
7. **Configuration & Environment Management** (5 checks, 25 max)
8. **Performance & Scalability** (5 checks, 25 max)
9. **Documentation & Knowledge** (5 checks, 25 max)
10. **Operations & Oncall** (5 checks, 25 max)
11. **Data Management** (6 checks, 30 max)
12. **Compliance & Governance** (5 checks, 25 max)
13. **Dependency Management** (5 checks, 25 max)

Total: 360 points. See `references/scorecard-template.md` for the full check list and `references/scoring-rubric.md` for what each score means.

These thirteen dimensions are a scoring instrument distilled from a longer source-of-truth checklist, bundled at [`references/production-readiness-checklist.md`](references/production-readiness-checklist.md) — 16 sections, ~230 concrete line items, drawn from years of running systems that have to stay up at 3am. The scorecard collapses those line items into scoreable rows; the checklist is where the granular, specific checks live. Consult it during evidence-gathering (Step 3) whenever a scorecard row is too coarse and you need the underlying concrete checks. The 16 checklist sections map onto the 13 dimensions as follows:

| Checklist section | Scored under dimension |
|---|---|
| 1. Testing | 1. Functional Correctness & Testing |
| 2. Input Validation / 3. Output Validation | 4. Security (boundaries) + 1. Testing (output assertions) |
| 4. Error Handling and Resilience | 2. Error Handling & Resilience |
| 5. Observability | 3. Observability |
| 6. Security | 4. Security |
| 7. Data Management | 11. Data Management |
| 8. CI/CD and Deployment / 16. Release Management | 6. CI/CD & Release Process |
| 9. Configuration Management | 7. Configuration & Environment Management |
| 10. Performance | 8. Performance & Scalability |
| 11. Maintainability | 5. Maintainability & Code Quality |
| 12. Documentation | 9. Documentation & Knowledge |
| 13. Operational Readiness | 10. Operations & Oncall |
| 14. Compliance and Governance | 12. Compliance & Governance |
| 15. Dependency Management | 13. Dependency Management |

Skip or weight-down any dimension that legitimately doesn't apply (e.g. a stateless CLI tool doesn't need Data Management) and note it in the report rather than docking points.

## Workflow

### Step 1 — Inventory and stack detection

Start by understanding what you're looking at. Run the helper script if Python is available:

```bash
python scripts/scan_signals.py <repo-path>
```

It walks the repo and emits a JSON of detected signals: languages, package manifests, CI configs, test directories, Dockerfiles, IaC, docs, and rough file counts. Save its output — you'll cite it.

If Python isn't available, do the equivalent manually with Glob/Grep:

- **Languages** — file extensions plus manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `*.csproj`)
- **CI** — `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`, `azure-pipelines.yml`, `buildkite/`
- **Tests** — `tests/`, `__tests__/`, `spec/`, files matching `*_test.*`, `*.spec.*`, `*.test.*`
- **Docker / IaC** — `Dockerfile*`, `docker-compose*.yml`, `terraform/`, `*.tf`, `helm/`, `k8s/`, `kustomization.yaml`
- **Docs** — `README*`, `docs/`, `CHANGELOG*`, `RUNBOOK*`, `ARCHITECTURE*`, `ADR*`, `SECURITY*`
- **Secret management** — search for `.env*`, `secrets.yaml`, hardcoded `password = `, `api_key = `
- **Data layer** — `migrations/`, `alembic/`, `prisma/migrations/`, `db/migrate/`, `flyway/`, `liquibase/`, backup config, ORM schema files
- **Dependency hygiene** — lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`, `Gemfile.lock`), `.github/dependabot.yml`, `renovate.json`
- **Licence / compliance** — `LICENSE*`, `LICENCE*`, `NOTICE`, `THIRD_PARTY_NOTICES*`, SBOM files (`*.spdx`, `*.cdx.json`), `PRIVACY*`, data-residency configuration

### Step 2 — Load stack-specific signals

For each language/framework detected, read the relevant section of `references/stack-signals.md`. It lists what good looks like per stack — e.g., for Python: pytest config, ruff/black/mypy, requirements pinning; for Node: ESLint/Prettier, lockfile, npm audit; for Go: `go test`, `golangci-lint`, modules.

Only load the sections that apply. If the project uses multiple stacks (monorepo, polyglot), load each.

### Step 3 — Gather evidence per dimension

Go dimension by dimension. For each check in the scorecard, look for the evidence specified in `references/stack-signals.md` and `references/scoring-rubric.md`. When a scorecard row is too coarse to act on, open [`references/production-readiness-checklist.md`](references/production-readiness-checklist.md) and work the granular line items for that dimension (use the section→dimension map above) — they spell out the concrete things to grep for and read. Read actual files. Cite paths.

Aim to inspect:

- All CI workflow files end-to-end (not just titles)
- Test directory structure plus a sample of 2–3 test files
- The main entrypoint and at least one critical module
- All top-level docs
- Dependency manifests in full plus the lockfile (top-level deps and pinning discipline)
- Security-related files (`SECURITY.md`, dependabot/renovate config, secret manager usage)
- How configuration and secrets are loaded (including startup validation)
- Error handling patterns in a sample of 3–5 files across the code
- The data layer — migration directory, any backup/restore tooling, schema-level constraints
- Licence files, NOTICE / third-party attributions, SBOM if present
- API versioning, changelog, and release notes (release-management discipline)

Time-box: roughly 3–5 minutes of inspection per dimension. You don't need to read every file — sample intelligently. If a dimension has obvious red flags early (e.g., `.env` checked into the repo), note them and move on; don't keep digging just to pad evidence.

When you genuinely can't find evidence either way, **ask the user** via AskUserQuestion (batched). Don't guess. Things you usually need to ask about: oncall process, SLOs, postmortem culture, on-prem capacity, real incident history, backup-restore drill cadence, RPO/RTO targets, access-review process, third-party DPAs, and regulatory scope (GDPR/CCPA/HIPAA/PCI).

### Step 4 — Score with evidence

For each check, assign 1–5 using `references/scoring-rubric.md`. Format every score like:

> **Score: 3** — Jest configured (`jest.config.ts`), 142 test files in `__tests__/`, but no integration tests visible and coverage isn't reported in CI (`.github/workflows/ci.yml` runs `jest` but no `--coverage` flag and no upload step).

Cite paths and line numbers wherever possible. The point is that another engineer reading the report should be able to verify your scoring without re-doing the audit.

### Step 5 — Apply the gate check

These four dimensions are critical by default — failing any of them disqualifies the project regardless of total score:

- Error Handling & Resilience
- Observability
- Security
- CI/CD & Release Process

**Promote additional dimensions to critical based on project type**:

- **Data Management** → critical for any system that owns durable user or business data, financial records, or anything where loss is unacceptable
- **Compliance & Governance** → critical for regulated industries (healthcare/HIPAA, finance/PCI-DSS/SOX, EU consumer/GDPR, public-sector)
- **Dependency Management** → critical for software shipped to customers (SDKs, on-prem products) or systems where a supply-chain compromise has wide blast radius

Calibrate the threshold to cost-of-failure:

| Cost of failure | Critical dim threshold | Other dim threshold |
|---|---|---|
| Low | ≥ 3 / 5 average | ≥ 2 / 5 average |
| Medium (default) | ≥ 4 / 5 average | ≥ 3 / 5 average |
| High | ≥ 4 / 5 average | ≥ 4 / 5 average |
| Critical | ≥ 5 / 5 average | ≥ 4 / 5 average |

If any critical dimension fails, surface it at the top of the report — not buried in the summary. This is the most important takeaway.

### Step 6 — Produce the scorecard

Copy `references/scorecard-template.md` and fill in:

- Project info (from user input + inventory)
- Each dimension table — evidence + score for every check
- Dimension subtotals and key gaps
- Summary table with totals
- Gate check result (Pass / Fail with detail)
- Action plan: top 3–5 improvements ordered by impact × ease. Each item must reference a specific gap you found, not boilerplate advice.
- Reassessment recommendation (timeline + focus areas)

Save to `<outputs>/production-readiness-<project-slug>-<YYYY-MM-DD>.md` and share a `computer://` link.

### Step 7 — Offer follow-ups

After delivering the report, briefly offer:

- A scheduled re-assessment (30 / 60 / 90 days) — pair with the schedule skill
- Drilling deeper into any failing dimension
- An Excel version with auto-calculated totals and gate checks
- Filing the gaps as Jira tickets if the user has Atlassian connected
- If the repo has **no `.claude/` tuning config** (no `CLAUDE.md`, empty or absent `.claude/`), mention the sibling **`adopt-claude-stack`** skill — a tailored CLAUDE.md and path-scoped rules make the fixes this report recommends easier to land and future audits faster to run.

Don't push. One short paragraph at the end is enough.

## Principles for scoring

**Be specific.** "Tests look thin" is useless. "Only 3 of 47 modules have unit tests; the auth module has zero coverage" is actionable.

**Be calibrated.** A 5 means "team can present this as a model"; a 3 means "meets the bar but has clear room to improve". Don't grade on a curve — grade against absolute production-readiness.

**Be honest about uncertainty.** If you didn't have time to verify a check, say so. Mark it `(unverified)` rather than guessing. A short report with confident scores beats a long one with hand-waved scores.

**Adapt to context.** A CLI tool legitimately doesn't need distributed tracing. An internal admin panel doesn't need 99.99% uptime. Note when something is "N/A for this project type" rather than docking points. Calibrate to the cost-of-failure the user set.

**Don't pad the action plan.** 3–5 high-leverage items beats 15 generic ones. Order by `(reduction in production risk) / (effort to implement)`.

## What to avoid

- Scoring on vibes without citations
- Generic boilerplate advice ("add more tests") in the action plan
- Conflating "no evidence" with "missing" — sometimes it's appropriate not to have a thing
- Burying gate failures in the middle of the report
- Treating one stack's idioms as the universal standard

## Files in this skill

- `references/production-readiness-checklist.md` — the source-of-truth checklist (16 sections, ~230 line items) the 13 dimensions distill; consult for granular per-dimension checks
- `references/scorecard-template.md` — the blank template to fill in
- `references/scoring-rubric.md` — what each score means, per dimension, with examples
- `references/stack-signals.md` — per-stack evidence to look for (Node/TS, Python, Go, Java/Kotlin, Ruby, Rust, .NET)
- `scripts/scan_signals.py` — optional helper to inventory the repo as JSON
