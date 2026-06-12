# Scoring Rubric

Concrete anchors for what 1, 3, and 5 mean in each dimension. Scores of 2 and 4 sit between the anchors. Use these to calibrate so the report is defensible.

A general rule: a **3** is "meets the bar — would not block ship on its own, but has clear room to improve". A **5** is "the team could hold this up as an exemplar for other projects". A **1** means the thing is meaningfully absent.

---

## 1. Functional Correctness & Testing

**1 — Missing**: No tests, or only a stray smoke script. No coverage of business logic. Engineers verify changes by running the app manually.

**3 — Adequate**: Unit tests exist for the main modules, CI runs them, most PRs add tests when they touch code. Coverage probably 50–70% on core. Some critical paths untested. Few or no integration tests. Test data is mostly deterministic; a couple of flaky tests are tolerated.

**5 — Excellent**: Unit + integration + E2E + contract layers, each with clear purpose. Coverage measured, tracked over time, and enforced in CI on critical modules. Tests cover edge cases, failure modes, concurrency, and chaos / fault injection. Smoke tests run post-deploy. API and event schemas are validated in CI with breaking-change detection so consumer-breaking PRs are blocked before merge. Code is structured for testability (DI, isolated side effects, no hidden global state, no monkey-patching needed). Tests are fast, deterministic, and well-organised. Flaky tests are tracked and fixed, not muted. Performance regression tests exist for critical paths; mutation testing runs periodically on the most important modules.

**Red flags**: `skip()` / `xit()` everywhere, large amounts of commented-out tests, tests that depend on production data, no CI integration, hidden global state preventing parallel test runs, coverage drops merged without CI complaining.

---

## 2. Error Handling & Resilience

**1 — Missing**: Bare `try/except` blocks that swallow exceptions, no timeouts on external calls, no retries. A downstream blip cascades into total failure. Errors logged as "Error" with no context. Process crashes take down everything in flight.

**3 — Adequate**: External calls have timeouts and basic retry. Errors are logged with stack traces. The app degrades reasonably under partial failure but isn't tested for it. Some downstream services have no fallback. Shutdown loses some in-flight work.

**5 — Excellent**: Every external call has timeout + retry (with jitter) + circuit breaker where appropriate. Bulkheads isolate workloads so one bad area doesn't starve others. Dead-letter queues capture unprocessable messages; poison messages are detected and quarantined rather than restart-looping. Errors include correlation IDs and structured context. User-facing errors are friendly; logs are detailed. Partial failures handled (one bad item in a batch doesn't discard the rest). Graceful shutdown drains in-flight work; services are stateless (or state is externalised) so they can scale and recover horizontally. Failure modes are exercised (chaos / fault injection / load shedding). Rate limiting protects against abuse.

**Red flags**: `except Exception: pass`, requests without timeout, no retry on transient failures, error messages that leak internal details to users, in-memory state on a service meant to scale, consumer crash-loops on a poison message, no graceful shutdown so SIGTERM truncates in-flight work.

---

## 3. Observability

**1 — Missing**: `print()` or unstructured logs scattered through code. No metrics. No tracing. Engineers ssh in and tail log files to debug. No external uptime checks.

**3 — Adequate**: Structured logging in place (JSON), with trace IDs for at least HTTP requests. Basic metrics (latency, error rate) emitted to some monitoring system. A few alerts set up — some noisy, most acknowledged-and-forgotten. Dashboards exist but are sparse. Log retention configured but generous.

**5 — Excellent**: Logs are structured, contextual, and correlate across services via trace IDs. Log levels are used correctly — ERROR means a human needs to look. Metrics cover RED (Rate / Errors / Duration) plus business KPIs (orders placed, jobs processed, emails sent). Distributed tracing via OpenTelemetry. Alerts are tuned to be actionable — low noise, all paged alerts have runbook links, every alert has clear ownership. Dashboards let oncall assess system health in under 30 seconds. Synthetic monitoring / external uptime checks confirm reachability from outside the infrastructure. Retention policies are deliberate — long enough for debugging, short enough to not bankrupt on storage. SLIs/SLOs defined and tracked with error budget.

**Red flags**: `print()` statements, logs without context, no metrics, alerts that fire constantly and get ignored, no way to trace a request end-to-end, ERROR-level used for routine events ("processed user 42"), no external probe so a regional outage goes unnoticed until users complain.

---

## 4. Security

**1 — Missing**: Hardcoded secrets in code or `.env` files in the repo. No dependency scanning. SQL queries built with string concatenation. Anyone with access to the app has full admin. Database is internet-reachable. Sessions never expire.

**3 — Adequate**: Secrets in a secret manager (or at least env vars not committed). Dependabot or similar scans dependencies. Input validation on most endpoints. Auth + role-based access. PII encrypted at rest. TLS at the edge. SECURITY.md exists. Basic session handling. Brute-force protection on login.

**5 — Excellent**: Secret manager with audit logs; secrets rotated automatically. Vulnerability scanning on every PR with policy gates. Comprehensive input validation at boundaries (SQLi / NoSQLi / XSS / SSRF / command-injection covered), output escaping, CSP and other security headers. Rate limiting and request-size limits everywhere external. Authn/Authz with least privilege; sessions expire and can be revoked; brute-force protection at the auth layer. PII encrypted at rest and in transit, including service-to-service (TLS internal too). Sensitive operations audit-logged with who/what/when/from-where. Network segmented so data stores aren't internet-reachable. Container images scanned on every build and based on minimal images. Regular pen tests / external audits. Threat model documented.

**Red flags**: `password = "..."` in source, `.env` in git history, `eval()` of user input, raw SQL with f-strings, no auth on internal endpoints, data store directly internet-reachable, no audit log for admin actions, sessions that never expire, plaintext internal service-to-service traffic.

---

## 5. Maintainability & Code Quality

**1 — Missing**: No linter. Inconsistent formatting. Modules tangled together with circular imports. Functions hundreds of lines long. No public interface documentation. Commit messages are "fix" / "wip".

**3 — Adequate**: Linter configured and runs in CI. Code structure is recognisable. Most functions are reasonable size. Top-level modules have docstrings. Conventional commit messages mostly. Some TODOs but not a backlog. Occasional refactor as part of feature work.

**5 — Excellent**: Linter + formatter + type checker enforced in CI, zero warnings. Clear module boundaries reflected in directory structure; dependencies flow in one direction and circular dependencies fail CI. Cognitive complexity measured by tooling (not eyeballed) with thresholds enforced on critical modules. Every public interface documented with examples and uses domain language consistently. PR descriptions explain "why", not just "what". TODOs are tracked tickets, not graveyard markers; dead code is removed promptly. Change hotspots are tracked and refactored before they become tar pits. New engineers ship value in their first week.

**Red flags**: Massive utility files, copy-paste duplication, mixed indentation, comments out of date with code, hundreds of TODOs, circular import chains, growing files nobody dares refactor.

---

## 6. CI/CD & Release Process

**1 — Missing**: No CI. Deployment is "SSH in and `git pull`". No rollback procedure. Database changes applied by hand. Releases are scary, infrequent events. No staging. No code review.

**3 — Adequate**: CI runs tests + lint on every PR; code review required before merge. Deploy is scripted or via a CD tool. Manual approval for prod. Rollback is documented if not automated. Migrations versioned. Releases happen weekly-ish. Lockfile-driven reproducible-ish builds. Basic changelog maintained.

**5 — Excellent**: CI is fast (<10 min), runs tests + lint + type-check + schema/contract validation (OpenAPI / Protobuf / GraphQL breaking-change detection, codegen drift) + migration-safety lint (squawk / atlas / migra) + security scans + build. CD is fully automated, push-button or trunk-based. Builds are reproducible from a given commit; artefacts are immutable and SHA-tagged (no `:latest` in prod). Feature flags and canary / blue-green / progressive rollouts. One-click rollback with documented rollback criteria. Migrations versioned, tested against production-size data, backward-compatible, and decoupled from app deploys. Staging mirrors production (environment parity). Infrastructure-as-Code lives alongside application code and is versioned. Release management is disciplined — semver, changelog humans can read, release notes communicated, hotfix process defined, API versioning and deprecation policy honoured. Multiple deploys per day with low failure rate; deployment history is auditable.

**Red flags**: No `.github/workflows/`, deploys involve manual steps, no staging environment, migrations applied via `psql $PROD < migration.sql`, solo commits to main allowed, `:latest` Docker tags in production, changelog last touched a year ago, breaking API change shipped without a deprecation window.

---

## 7. Configuration & Environment Management

**1 — Missing**: Config hardcoded in source. Different environments handled via `if hostname == ...`. Secrets in source. Infrastructure provisioned by hand. Bad config silently does the wrong thing for hours.

**3 — Adequate**: Config via env vars or config files, separated from code. Safe defaults. Validated at startup so the system fails fast on bad config. dev/staging/prod isolated. Some IaC for parts of the infra. Docker images used for deployment. Secrets in a manager. A few feature flags, lifecycle informally managed.

**5 — Excellent**: 12-factor compliant. All infra in IaC (Terraform / Pulumi / CloudFormation), reviewed via PR. Containerised, reproducible builds. Secrets managed centrally with rotation. Config changes auditable, reversible, and (where possible) take effect without redeploy. Config drift between environments is detectable and alerted on. Feature flags have owners, expiry dates, and a cleanup process — no permanent "temporary" flags.

**Red flags**: `if env == "production": ...` branches in code, IPs hardcoded, infrastructure changes happen in the console with no record, "temporary" feature flags older than a year, bad config that surfaces only when a code path runs hours after startup.

---

## 8. Performance & Scalability

**1 — Missing**: Never load-tested. No idea where bottlenecks are. Single instance, single DB, no caching. Will fall over under any traffic spike. No resource limits on containers. List endpoints return unbounded results.

**3 — Adequate**: Some load testing done, bottlenecks roughly known. Basic caching on hot reads. DB has indexes on common queries. Can scale horizontally for stateless parts. Connection pool tuned. Pagination on most list endpoints. Compression enabled at the edge.

**5 — Excellent**: Regular load tests against expected and 10× expected traffic; the breaking point is known. Performance budgets defined for critical paths (p50/p95/p99). Bottlenecks documented. Multi-layer caching with eviction strategy and stampede protection. DB indexes audited and query plans reviewed; no N+1 queries. CDN for static assets; compression for API responses and large files. Async processing for anything that doesn't need to block the user (email, notifications, reports). Service genuinely stateless and horizontally scalable; resource limits set per container; pagination enforced on all list endpoints. Capacity plans tied to business growth. Memory profile checked under sustained load to catch leaks.

**Red flags**: No load test ever, N+1 queries everywhere, in-memory state on a service meant to scale, no DB indexes on join columns, no resource limits on containers (noisy neighbours), unbounded endpoints that can return arbitrarily large results, no async path for slow operations like report generation.

**Note**: For low-traffic internal tools, score this dimension generously — over-engineering is its own production risk.

---

## 9. Documentation & Knowledge

**1 — Missing**: README is empty or just the auto-generated framework one. No architecture doc. No runbook. Onboarding is "ask the senior engineer". No accessibility consideration for public UI.

**3 — Adequate**: README explains what the project is, how to run it locally, basic config. Some architecture notes in `docs/`. A runbook exists for the most common issue. New engineers can get unstuck on common things via search. API docs generated from schema. Basic accessibility for user-facing surfaces.

**5 — Excellent**: README gets you running in 30 minutes. Architecture diagrams (current, not from 2 years ago). ADRs for major decisions capturing the "why". Data-flow diagram for PII (where sensitive data enters, moves, and is stored). Runbook covers top-10 incident types with diagnosis and rollback steps. Incident response playbook documents who to call, how to communicate, and the post-incident review process. API docs auto-generated and current. Accessibility (WCAG 2.1 AA) addressed for user-facing surfaces — keyboard navigation, screen readers, colour contrast. Onboarding doc walks new engineers through their first PR. Dependency map shows what this service talks to and what talks to it.

**Red flags**: README hasn't been touched in a year, architecture diagrams reference services that no longer exist, runbook says "ask <ex-employee>", no accessibility considered for a public UI, no PII data-flow diagram even though compliance audits keep asking for one.

---

## 10. Operations & Oncall

This dimension usually requires asking the user — most of it isn't in the code.

**1 — Missing**: No SLOs, no oncall rotation, no postmortems. Incidents are handled by whoever notices on Slack. No DR plan, or DR plan that's never been tested. No customer communication templates. No idea how the system behaves in degraded mode.

**3 — Adequate**: SLOs roughly defined. Oncall rotation exists, maybe informal. Severity levels loosely understood. Postmortems happen for big incidents. DR plan exists on paper. Some cost monitoring. Runbooks exist but only the author has used them.

**5 — Excellent**: SLOs measured and reported, with error budget tracking. Oncall rotation with clear escalation, handover, runbooks, and training. Incident severity levels (SEV1-4) defined with response-time expectations and customer-communication templates ready. Every incident gets a blameless postmortem; action items tracked to completion. Runbooks tested by someone other than their author. DR drills run quarterly; game days exercise real failure scenarios. Graceful degradation plan documents what to turn off first under extreme load. Capacity and cost trends reviewed monthly with quarterly capacity planning. Upstream dependency health is tracked — you know when a provider is degraded before users tell you.

**Red flags**: "We don't really have oncall, people just respond when something breaks", no postmortems for major incidents, backups never restored, runbook only the author has ever used, no idea what to shed first under load, learned about a provider's outage from your own users.

---

## 11. Data Management

For systems that own durable data, this is as important as any of the original "critical" dimensions — elevate it to the gate when the cost of data loss or corruption is high.

**1 — Missing**: No migration history, or schema changes applied by hand on prod. Backups not configured, or running but never tested. No retention or deletion policy — old data accumulates forever or is purged without record. RPO / RTO undefined. PII stored in plaintext. Dates stored in local time with no timezone.

**3 — Adequate**: Migrations versioned with a tool (Flyway / Alembic / Prisma / Knex / equivalent). Backups configured by the cloud provider with default retention. Restoration documented but rarely tested. Basic retention. Encryption at rest enabled by default. Timezone is "mostly UTC". Some integrity constraints at the DB level.

**5 — Excellent**: Migrations are backwards-compatible, linted in CI for unsafe operations (squawk / atlas / migra catch non-concurrent indexes, NOT NULL on large tables, destructive renames), tested against production-size data, and decoupled from deploys (migrate-then-deploy). Backups run regularly with quarterly restore drills that succeed end-to-end. Point-in-time recovery or cross-region replication for critical data, sized to a measured RPO and RTO. Retention and deletion policies enforced (including GDPR right-to-delete); soft deletes where auditability requires. Data integrity constraints enforced at the database level (foreign keys, NOT NULL, CHECK), not just in the application. Databases, backups, and object storage encrypted at rest. Servers run UTC; user-facing times converted at the edge.

**Red flags**: migrations applied via `psql $PROD < migration.sql`, "we haven't restored a backup yet but it should work", PII stored in plaintext, dates stored in local time without timezone, retention "we just keep everything", no DB-level foreign keys "because the ORM handles it".

---

## 12. Compliance & Governance

This dimension is mostly process and paperwork — much of it lives outside the repo. Ask the user for what isn't visible.

**1 — Missing**: No licence audit (a copyleft library may already be in the proprietary tree). No SBOM. Personal data stored wherever convenient with no thought to region. No audit trail for admin actions. Former employees still in IAM. No privacy impact assessment for new features; no DPAs with third-party processors. Regulatory scope (GDPR / HIPAA / PCI / SOX) not mapped to controls.

**3 — Adequate**: Top-level dependency licences reviewed; SBOM available on request. Data residency at least understood for major customer regions. Some audit logging for sensitive operations. Access reviews happen annually. PIAs done for new features handling PII; DPAs in place with major processors. Regulatory requirements identified for the obvious frameworks.

**5 — Excellent**: Licence compliance enforced in CI (no copyleft creep into proprietary code). SBOM generated per build and published. Data residency mapped explicitly in IaC. Immutable audit logs with strict retention; who-accessed-what-when is queryable. Quarterly access reviews; departures trigger automated revocation across all systems. Regulatory scope explicitly mapped to technical controls (e.g. GDPR Art. 32 → encryption + access logging; HIPAA → BAA list + audit trail; PCI → tokenisation + segmentation). PIAs done up-front for any new personal-data flow; DPAs current with every processor.

**Red flags**: unknown licence on a critical dependency, EU customer data in a US-only region, ex-employees still in IAM weeks after termination, no record of who accessed PII last quarter, "we're probably covered by [framework]" with no mapping document.

**Note**: For non-regulated, internal, or single-region projects, score generously — most checks may legitimately be N/A. For regulated systems, this dimension should be promoted to critical.

---

## 13. Dependency Management

**1 — Missing**: No lockfile (or lockfile uncommitted). Versions floating (`^` / `~` without lock). No vulnerability scanning. No SLA for patching. No knowledge of the transitive tree. Includes a library that hasn't been updated since 2018. CI runs `npm install` instead of `npm ci`.

**3 — Adequate**: Lockfile committed and used in CI. Dependabot or similar runs scans; findings appear but aren't always actioned. Most critical libs are actively maintained. Rough patching cadence but no formal SLA. Top-level deps known; transitive tree mostly opaque.

**5 — Excellent**: Lockfile drives reproducible builds (`npm ci`, `pip install --require-hashes`, `cargo --locked`). Dependabot / Renovate runs with CI gating on vulnerability findings. Documented SLAs (e.g., critical 24h, high 7d) and they're hit, with evidence in PR history. Every critical third-party dependency has a fallback plan (alternate provider, in-house adapter, degraded mode) and their SLA is reviewed and accounted for in your own SLA calculations. Transitive tree audited and pinned. Abandoned libraries are tracked and replaced before they become a problem. No critical-path dependency on an archived or single-maintainer project.

**Red flags**: no lockfile, `npm install` in CI without `--frozen-lockfile` / `--ci`, critical CVE open for >30 days, depending on an archived GitHub repo for core functionality, third-party SLA worse than your own and unaccounted for, transitive tree never audited so you don't actually know what you ship.

---

## Calibration check

If you're scoring multiple dimensions in the 4–5 range with little citation evidence, you're probably being too generous. Real production-grade systems usually have a couple of 5s, several 3s and 4s, and at least one weak area. A board of all 5s on first audit is suspicious — re-check.

If you're scoring everything 1–2, double-check that you're not just missing where things are. Some shops keep CI/IaC/observability in a separate repo; legal/compliance evidence often lives in Confluence or a GRC tool rather than the codebase; backup/restore drills often live in a runbook repo or a ticketing system. Ask the user.
