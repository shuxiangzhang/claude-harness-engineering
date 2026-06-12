# Production Readiness Checklist

A comprehensive checklist for shipping and maintaining reliable production systems, drawn from 20 years of building systems that need to stay up at 3am.

---

## 1. Testing

- [ ] Unit tests cover core business logic with meaningful assertions (not just coverage theatre)
- [ ] Integration tests verify component boundaries — database queries, API calls, message queues
- [ ] End-to-end tests cover critical user journeys (login, checkout, data export — whatever keeps the lights on)
- [ ] Contract tests validate API agreements between services (consumer-driven where possible)
- [ ] Load/stress tests run against a production-like environment with realistic data volumes
- [ ] Chaos/failure injection tests confirm the system degrades gracefully (kill a dependency, fill a disk, drop packets)
- [ ] Tests run in CI on every PR — no "run tests locally before merging" honour system
- [ ] Test data is isolated and deterministic — no tests that pass on Tuesdays and fail on Wednesdays
- [ ] Flaky tests are tracked and fixed, not muted and forgotten
- [ ] Smoke tests run post-deploy to confirm the release actually works in production
- [ ] Code is designed for testability — dependencies injected, side effects isolated, pure functions favoured where reasonable
- [ ] Modules expose seams — collaborators can be substituted with fakes or mocks without monkey-patching internals
- [ ] No hidden global state that prevents tests running in parallel or in isolation
- [ ] Coverage thresholds defined and enforced in CI on core business logic (not arbitrary line-count targets)
- [ ] Mutation testing run periodically on critical modules to expose assertions that never actually catch anything

---

## 2. Input Validation

- [ ] All external input is validated at the boundary (type, format, length, range)
- [ ] Validation rejects early and returns clear, actionable error messages
- [ ] Schema validation enforced on API requests (OpenAPI, JSON Schema, protobuf)
- [ ] File uploads validated for type, size, and content (not just extension)
- [ ] SQL injection, XSS, and command injection prevented via parameterised queries and output encoding
- [ ] Rate limiting applied to all public-facing endpoints
- [ ] Request size limits enforced to prevent memory exhaustion
- [ ] Unicode and encoding edge cases handled (null bytes, overlong sequences, RTL characters)
- [ ] Malformed input doesn't crash the process or leak stack traces

---

## 3. Output Validation

- [ ] API responses conform to a published schema — validated in tests and optionally at runtime
- [ ] Business-rule assertions on output (totals match line items, dates are in valid ranges, counts are non-negative)
- [ ] Output sanitised to prevent injection in downstream consumers (HTML encoding, JSON escaping)
- [ ] PII/sensitive data scrubbed or masked before it reaches logs, error responses, or external systems
- [ ] AI/LLM outputs validated with guardrails (hallucination checks, toxicity filtering, format conformance)
- [ ] Idempotent endpoints return consistent output for repeated identical requests
- [ ] Error responses follow a consistent envelope (status, code, message, request ID) — no raw stack traces
- [ ] Pagination metadata is correct (total counts, next/prev cursors, boundary conditions)
- [ ] Output size is bounded — no endpoints that can return unbounded result sets
- [ ] Content-Type headers match actual response body format
- [ ] Downstream contract tests verify your output against what consumers actually expect

---

## 4. Error Handling and Resilience

- [ ] Every external call (HTTP, database, queue, file system) has a timeout
- [ ] Retries use exponential backoff with jitter — not tight loops that hammer a struggling dependency
- [ ] Circuit breakers protect against cascading failures from downstream outages
- [ ] Fallback behaviour defined for every dependency (cached response, degraded mode, honest error)
- [ ] Partial failures handled — one failed item in a batch doesn't discard the other 999
- [ ] Dead letter queues capture messages that can't be processed for later inspection
- [ ] Unhandled exceptions caught at the top level — the process logs the error and stays up
- [ ] Graceful shutdown implemented — in-flight requests complete, connections drain, resources release
- [ ] Health check endpoints distinguish between "healthy", "degraded", and "unhealthy"
- [ ] Bulkheads isolate workloads so a spike in one area doesn't starve others (thread pools, connection pools, queue consumers)
- [ ] Poison message detection — a single bad message can't crash and restart a consumer in a loop
- [ ] Race conditions and concurrency addressed — distributed locks, optimistic concurrency, or idempotency keys where needed
- [ ] Services are stateless (or state is externalised) to allow horizontal scaling
- [ ] Auto-scaling policies configured and tested — scales up under load, scales down to save cost

---

## 5. Observability

- [ ] Structured logging (JSON) with consistent fields: timestamp, level, service, request ID, user ID
- [ ] Log levels used correctly — ERROR means someone needs to look, not "this thing happened"
- [ ] Distributed tracing across service boundaries (trace ID propagated in headers)
- [ ] Key business metrics instrumented (orders placed, emails sent, jobs processed — not just CPU/memory)
- [ ] RED metrics for every service: Rate, Errors, Duration
- [ ] Dashboards exist and are actually looked at — not 47 panels nobody understands
- [ ] Alerts configured with clear ownership, runbooks linked, and escalation paths defined
- [ ] Alert fatigue addressed — every alert should be actionable, not "acknowledged and ignored"
- [ ] Logs, metrics, and traces are correlated — you can go from an alert to the specific request that caused it
- [ ] Retention policies defined — logs kept long enough for debugging, not so long they bankrupt you on storage
- [ ] Synthetic monitoring / uptime checks from outside your infrastructure
- [ ] SLIs and SLOs defined and tracked (availability, latency percentiles, error budget)

---

## 6. Security

- [ ] Authentication on every endpoint that needs it — no "we'll add auth later" endpoints in production
- [ ] Authorisation checked at the resource level, not just "is the user logged in"
- [ ] Secrets stored in a vault or secrets manager — not in environment variables, config files, or (heaven forbid) source code
- [ ] Secrets rotated on a schedule and rotation is automated
- [ ] Dependencies scanned for known vulnerabilities (Dependabot, Snyk, Trivy) and findings actioned
- [ ] Container images scanned and built from minimal base images
- [ ] Network segmentation — the database isn't reachable from the internet
- [ ] TLS everywhere — internal service-to-service included, not just the edge
- [ ] CORS, CSP, and security headers configured correctly
- [ ] Audit logging for sensitive operations (who changed what, when, from where)
- [ ] Penetration testing performed at least annually
- [ ] Principle of least privilege applied to service accounts, IAM roles, and database users
- [ ] Input validation covers injection attacks (SQL, NoSQL, LDAP, OS command, SSRF)
- [ ] Session management handles expiry, revocation, and concurrent sessions
- [ ] Rate limiting and brute-force protection on authentication endpoints
- [ ] Data encrypted at rest — databases, backups, object storage, not just in transit

---

## 7. Data Management

- [ ] Database migrations are backwards-compatible (no breaking column renames in a zero-downtime deploy)
- [ ] Migrations tested against a production-size dataset — not just an empty schema
- [ ] Backups running, tested, and restoration procedure documented and rehearsed
- [ ] Point-in-time recovery available for critical data stores
- [ ] Data retention and deletion policies implemented (GDPR, CCPA, or just good hygiene)
- [ ] Soft deletes where business rules require auditability
- [ ] Database connection pooling configured with sensible limits
- [ ] Query performance monitored — slow query logs reviewed, indexes validated
- [ ] Schema changes have a rollback plan
- [ ] Data integrity constraints enforced at the database level, not just application level
- [ ] Cross-region replication configured if RPO/RTO requires it
- [ ] Database and backup encryption at rest enabled
- [ ] Timezone and clock handling is explicit — servers use UTC, user-facing times converted at the edge
- [ ] RPO and RTO formally defined and tested — you know how much data you can lose and how long recovery takes

---

## 8. CI/CD and Deployment

- [ ] Builds are reproducible — same commit always produces the same artefact
- [ ] Artefacts are immutable and versioned (Docker images tagged with commit SHA, not just "latest")
- [ ] Deployment pipeline has stages: build → test → staging → production
- [ ] Rollback is a one-click operation that takes minutes, not hours
- [ ] Blue/green or canary deployments to limit blast radius
- [ ] Database migrations decouple from application deploys (migrate-then-deploy, not simultaneously)
- [ ] Feature flags for gradual rollout and instant kill switches
- [ ] Deployment requires no manual steps — if a human has to SSH and run a script, it's not ready
- [ ] Pipeline enforces quality gates: tests pass, linting clean, static analysis clean, security scan green
- [ ] Code review required before merge — no solo commits to main
- [ ] Static analysis / linting rules enforced consistently (not just suggested)
- [ ] Deployment history is auditable — who deployed what, when, and why
- [ ] Infrastructure defined as code (Terraform, Pulumi, CloudFormation) and versioned alongside application code
- [ ] Environment parity — staging looks like production, not a single-node Docker Compose

---

## 9. Configuration Management

- [ ] Environment-specific config separated from code (no if environment == "prod" in application logic)
- [ ] Config changes don't require a redeploy where possible
- [ ] Secrets and config are separate concerns — config in config, secrets in a vault
- [ ] Default values are safe — if a config value is missing, the system doesn't silently do the wrong thing
- [ ] Config is validated at startup — fail fast on bad config, not 3 hours later when that code path runs
- [ ] Feature flags have owners, expiry dates, and a cleanup process
- [ ] Config drift between environments is detectable and alerted on

---

## 10. Performance

- [ ] Performance budgets defined for critical paths (API latency p50/p95/p99, page load time)
- [ ] Load testing establishes the breaking point — you know where the system falls over
- [ ] Caching strategy documented: what's cached, TTLs, invalidation approach, cache stampede protection
- [ ] Database queries optimised — no N+1 queries, appropriate indexes, EXPLAIN plans reviewed
- [ ] Connection pools sized correctly for expected concurrency
- [ ] Async processing for anything that doesn't need to block the user (email, notifications, report generation)
- [ ] Resource limits set on containers/processes (CPU, memory) to prevent noisy neighbours
- [ ] CDN configured for static assets
- [ ] Compression enabled (gzip/brotli) for API responses and static files
- [ ] Pagination enforced on all list endpoints — no unbounded queries
- [ ] Memory leaks tested for — run the service under sustained load and watch RSS over time

---

## 11. Maintainability

- [ ] Code follows a consistent style enforced by a formatter and linter, not by opinion in code review
- [ ] Modules have a single, clear responsibility and a bounded public surface
- [ ] Functions are short enough to read in one screen; deep nesting avoided
- [ ] Cognitive complexity kept low and measured by tooling (SonarQube, radon, similar) — not just eyeballed
- [ ] Naming uses domain language consistently — no cryptic abbreviations, no leaking implementation detail into names
- [ ] Dependencies between modules flow in one direction — circular dependencies detected and failed in CI
- [ ] Dead code removed promptly — retired feature flags, unused modules, commented-out blocks
- [ ] Refactoring happens continuously as part of feature work, not as a separate "tech debt sprint" that never arrives
- [ ] Change hotspots tracked — modules that churn frequently get refactored before they become tar pits
- [ ] Code review focuses on design, readability, and maintainability — not just whether the change technically works
- [ ] Onboarding test: a new engineer can locate, understand, and safely change a core module within their first week

---

## 12. Documentation

- [ ] Architecture decision records (ADRs) capture the "why", not just the "what"
- [ ] System architecture diagram exists and is current (not from 2019)
- [ ] API documentation is generated from code/schema, not hand-maintained markdown that drifts
- [ ] Runbooks for every alert — what the alert means, how to diagnose, how to fix
- [ ] Onboarding guide — a new engineer can set up the dev environment and run tests in under an hour
- [ ] Dependency map — what this service talks to, what talks to it, and what happens when each one is down
- [ ] Data flow diagram for PII — where sensitive data enters, moves, and is stored
- [ ] Incident response playbook — who to call, how to communicate, post-incident review process
- [ ] Change management process documented — how changes get from idea to production
- [ ] Accessibility (WCAG 2.1 AA) addressed for user-facing interfaces — keyboard navigation, screen readers, colour contrast

---

## 13. Operational Readiness

- [ ] On-call rotation defined with clear escalation paths
- [ ] On-call engineers have access and permissions to diagnose and fix issues
- [ ] Incident severity levels defined (SEV1-4) with response time expectations
- [ ] Post-incident reviews conducted without blame, with action items tracked to completion
- [ ] Game days / disaster recovery drills conducted at least quarterly
- [ ] Capacity planning reviewed quarterly — you know when you'll need to scale
- [ ] Cost monitoring and anomaly detection on cloud spend
- [ ] Dependency health tracked — you know when an upstream provider has issues before your users tell you
- [ ] Communication templates ready for customer-facing incidents
- [ ] Runbooks tested — someone other than the author has followed them successfully
- [ ] Graceful degradation plan — what do you turn off first when the system is under extreme load

---

## 14. Compliance and Governance

- [ ] Licence compliance for all dependencies (no GPL in proprietary code without legal review)
- [ ] Data residency requirements met (data stored in correct regions)
- [ ] Audit trail for data access and modifications
- [ ] Access reviews conducted periodically — former employees and contractors removed promptly
- [ ] Data processing agreements in place with third-party processors
- [ ] Privacy impact assessment completed for new features handling personal data
- [ ] Regulatory requirements identified and mapped to technical controls

---

## 15. Dependency Management

- [ ] Dependencies pinned to exact versions (lockfiles committed)
- [ ] Automated dependency updates (Dependabot/Renovate) with CI gating
- [ ] Vulnerable dependencies patched within defined SLAs (critical: 24h, high: 7d)
- [ ] Third-party service SLAs reviewed and accounted for in your own SLA calculations
- [ ] Fallback plan for every critical third-party dependency going down
- [ ] No dependencies on abandoned or unmaintained libraries in critical paths
- [ ] Transitive dependency tree audited — you know what you're actually shipping

---

## 16. Release Management

- [ ] Versioning strategy defined and followed (semver or equivalent)
- [ ] Changelog maintained — humans can understand what changed between releases
- [ ] Release notes communicated to stakeholders
- [ ] Rollback criteria defined — what conditions trigger an automatic or manual rollback
- [ ] Release cadence established — not "whenever someone feels like it"
- [ ] Hotfix process defined — how to get an emergency fix out without the full release cycle
- [ ] Pre-release validation in a staging environment with production-like data
- [ ] Post-release validation — smoke tests, metric comparison, error rate monitoring
- [ ] API versioning strategy defined — consumers know how to handle breaking changes and deprecations
- [ ] Deprecation policy communicated with timeline — old versions don't disappear without warning

---

## How to Use This Checklist

This isn't a gate to pass once — it's a living standard. Not every item applies to every system, and the right level of rigour depends on the stakes. A weekend project and a payment processing system have very different bars.

Start by scoring where you are today. Focus on the gaps that would hurt most if they bit you tomorrow. The items that feel most uncomfortable to skip are usually the ones you need most.

Review quarterly. Systems decay. What was true six months ago may not be true now.
