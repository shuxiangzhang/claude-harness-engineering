# Production Readiness Report — {{PROJECT_NAME}}

**Assessment date**: {{DATE}}
**Assessor**: {{ASSESSOR}}
**Repository**: {{REPO_URL_OR_PATH}}
**Tech stack detected**: {{STACK}}
**Cost of failure**: {{LOW_MED_HIGH_CRIT}}
**Standard applied**: {{STANDARD_LABEL}} (see thresholds below)

---

## TL;DR

{{ONE_PARAGRAPH_SUMMARY — overall verdict, what's strong, what's blocking. Mention gate result first.}}

**Gate result**: {{PASS / FAIL with which critical dimension failed}}
**Total score**: {{X}} / 360 ({{Y}}%)
**Recommended action**: {{e.g., "Ship after addressing top 3 gaps" / "Do not ship until error handling and observability gaps are closed"}}

---

## Project information

| Field | Value |
|---|---|
| Project name | {{PROJECT_NAME}} |
| Purpose | {{ONE_LINE_DESCRIPTION}} |
| Users / scale | {{WHO_USES_IT_AND_HOW_MANY}} |
| Stage | {{PRE_LAUNCH / EARLY / GROWTH / MATURE}} |
| Cost of failure | {{LOW_MED_HIGH_CRIT}} |
| Primary tech stack | {{LANGUAGES_AND_FRAMEWORKS}} |
| Deployment target | {{CLOUD_KUBERNETES_VM_ETC}} |
| Data sensitivity | {{NONE / INTERNAL / PII / REGULATED}} |
| Regulatory scope | {{NONE / GDPR / CCPA / HIPAA / PCI / SOX / OTHER}} |

---

## Scoring rubric

| Score | Meaning |
|---|---|
| 1 | Missing — not in place |
| 2 | Nascent — scattered attempts, no system |
| 3 | Adequate — meets baseline, clear room to improve |
| 4 | Good — comprehensive coverage, only edge-case gaps |
| 5 | Excellent — reference-quality, team can hold this up as a model |

---

## Dimension 1: Functional Correctness & Testing

| Check | Evidence | Score |
|---|---|---|
| Unit tests cover core logic (≥80% on critical modules) | {{cite files / coverage report}} | {{1–5}} |
| Integration tests cover main business flows and key contract boundaries (API consumers, queue producers/consumers); API / event schemas validated in CI with breaking-change detection (Spectral / `buf breaking` / GraphQL inspector / similar) | {{cite files + schema-check CI step}} | {{1–5}} |
| End-to-end tests cover critical user journeys | {{cite files}} | {{1–5}} |
| Tests run automatically in CI; must pass before merge; coverage thresholds enforced and flaky tests tracked, not muted | {{cite CI config}} | {{1–5}} |
| Tests cover edge cases, concurrency, and failure / chaos injection; smoke tests run post-deploy | {{cite examples}} | {{1–5}} |
| Performance / regression baseline tests in place; code is structured for testability (DI, isolated side effects, no hidden global state) | {{cite or "not found"}} | {{1–5}} |

**Subtotal**: {{X}} / 30 (average {{Y}} / 5)

**Key gaps**:
- {{specific finding 1}}
- {{specific finding 2}}

**Priority**: {{High / Medium / Low}}

---

## Dimension 2: Error Handling & Resilience (CRITICAL)

| Check | Evidence | Score |
|---|---|---|
| All external calls (DB / API / IO) have explicit error handling | {{cite samples}} | {{1–5}} |
| Retry logic in place (exponential backoff with jitter, max attempts) | {{cite}} | {{1–5}} |
| Timeouts set everywhere; no unbounded blocking | {{cite}} | {{1–5}} |
| Circuit breakers, bulkheads, dead-letter queues, and fallbacks contain downstream failures; poison messages detected, not retried in a crash loop | {{cite}} | {{1–5}} |
| Exceptions are never silently swallowed; root cause context preserved; partial failures handled (one bad item doesn't discard a batch) | {{cite}} | {{1–5}} |
| User-facing errors are friendly; developer-facing logs detailed; graceful shutdown drains in-flight work; services stateless (or state externalised) for horizontal scaling | {{cite}} | {{1–5}} |

**Subtotal**: {{X}} / 30 (average {{Y}} / 5)

**Key gaps**:
- {{specific finding}}

**Priority**: {{High / Medium / Low}}

---

## Dimension 3: Observability (CRITICAL)

| Check | Evidence | Score |
|---|---|---|
| Structured logging (e.g. JSON) with consistent fields (timestamp, level, service, request_id, user_id) and trace ID correlation | {{cite}} | {{1–5}} |
| Key metrics captured: RED (Rate / Errors / Duration) plus business KPIs (orders, jobs processed, emails sent) | {{cite}} | {{1–5}} |
| Centralised monitoring platform integrated (Prometheus / Datadog / New Relic) | {{cite}} | {{1–5}} |
| Distributed tracing in place (OpenTelemetry or equivalent) with trace IDs propagated across service boundaries | {{cite}} | {{1–5}} |
| Alerts defined on key signals, tuned to be actionable (low noise) with runbook links; log levels used correctly so ERROR is paged-worthy | {{cite or ask user}} | {{1–5}} |
| Dashboards available; synthetic monitoring / external uptime checks confirm reachability; retention policies defined for logs, metrics, and traces | {{cite or ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 30 (average {{Y}} / 5)

**Key gaps**:
- {{specific finding}}

**Priority**: {{High / Medium / Low}}

---

## Dimension 4: Security (CRITICAL)

| Check | Evidence | Score |
|---|---|---|
| No hardcoded secrets / tokens / passwords; secret manager in use with rotation automated | {{cite + grep results}} | {{1–5}} |
| Automated dependency vulnerability scanning (Dependabot / Snyk / Trivy) with findings actioned within SLA | {{cite config}} | {{1–5}} |
| Comprehensive input validation at boundaries; no SQLi / NoSQLi / XSS / SSRF / command-injection risk; rate limiting and request-size limits on public endpoints | {{cite samples}} | {{1–5}} |
| Authentication + authorisation with least-privilege; session expiry/revocation handled; brute-force protection on auth endpoints | {{cite}} | {{1–5}} |
| Sensitive data encrypted at rest and in transit (TLS internal too); access controlled; sensitive operations audit-logged | {{cite}} | {{1–5}} |
| Regular penetration testing / security audits; network segmented so data stores aren't internet-reachable; container images scanned and built from minimal bases | {{cite or ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 30 (average {{Y}} / 5)

**Key gaps**:
- {{specific finding}}

**Priority**: {{High / Medium / Low}}

---

## Dimension 5: Maintainability & Code Quality

| Check | Evidence | Score |
|---|---|---|
| Unified linter / formatter / type-checker enforced in CI (not just suggested) | {{cite config}} | {{1–5}} |
| Clear code structure with well-defined module boundaries; dependencies flow in one direction | {{cite structure}} | {{1–5}} |
| Public interfaces are documented (comments / type signatures / examples) using domain language | {{cite samples}} | {{1–5}} |
| Commit messages and PR descriptions follow conventions and explain "why", not just "what" | {{cite git log sample}} | {{1–5}} |
| No large backlog of TODOs / FIXMEs or dead code; cognitive complexity and circular dependencies monitored in CI; change hotspots refactored | {{cite grep counts}} | {{1–5}} |
| New engineers can locate, understand, and safely change a core module within their first week | {{ask user / infer}} | {{1–5}} |

**Subtotal**: {{X}} / 30

**Key gaps**:
**Priority**:

---

## Dimension 6: CI/CD & Release Process (CRITICAL)

| Check | Evidence | Score |
|---|---|---|
| PRs run tests, lint, type-check, schema/contract validation (OpenAPI / Protobuf / GraphQL breaking-change detection, schema-to-codegen drift), and security scans automatically; code review required before merge (no solo commits to main) | {{cite workflows}} | {{1–5}} |
| Deployments are automated and reproducible (immutable, SHA-tagged artefacts); one-click rollback with clear rollback criteria | {{cite}} | {{1–5}} |
| Staging environment mirrors production (environment parity); infrastructure-as-code lives alongside application code and is versioned | {{cite or ask user}} | {{1–5}} |
| Feature flags, canary, or blue/green progressive rollout in place to limit blast radius | {{cite}} | {{1–5}} |
| Database migrations versioned; forward/backward compatible; decoupled from application deploys (migrate-then-deploy) | {{cite migration tool}} | {{1–5}} |
| Frequent, small-batch deployments; disciplined release process (semver, changelog, hotfix procedure, API versioning, deprecation policy) | {{cite or ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 30

**Key gaps**:
**Priority**:

---

## Dimension 7: Configuration & Environment Management

| Check | Evidence | Score |
|---|---|---|
| Configuration separated from code; safe defaults; validated at startup so the system fails fast on bad config | {{cite}} | {{1–5}} |
| dev / staging / prod configurations clear and isolated; config drift between environments detectable and alerted on | {{cite}} | {{1–5}} |
| Infrastructure as Code in use (Terraform / Pulumi / CloudFormation), reviewed via PR | {{cite}} | {{1–5}} |
| Containerised / image-based deployment; environments reproducible | {{cite Dockerfile}} | {{1–5}} |
| Secrets managed separately from general configuration; feature flags have owners, expiry dates, and a cleanup process | {{cite}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Dimension 8: Performance & Scalability

| Check | Evidence | Score |
|---|---|---|
| Load testing establishes the breaking point with bottlenecks understood; performance budgets defined for critical paths (p50/p95/p99 latency) | {{cite or ask user}} | {{1–5}} |
| Caching strategy documented (what's cached, TTLs, invalidation, stampede protection); CDN and compression for static and large responses | {{cite}} | {{1–5}} |
| Databases tuned: indexes audited, N+1 queries avoided, connection pool sized for concurrency | {{cite}} | {{1–5}} |
| Service scales horizontally with no hidden SPOFs; resource limits set per container; pagination enforced on list endpoints | {{cite}} | {{1–5}} |
| Capacity planning in place with clear scaling triggers; memory profile checked under sustained load to catch leaks | {{cite or ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Dimension 9: Documentation & Knowledge

| Check | Evidence | Score |
|---|---|---|
| README lets a newcomer run the project locally within 30 minutes | {{cite README and assess}} | {{1–5}} |
| Runbook covers common incidents with diagnosis and rollback steps; incident response playbook documents communication, escalation, and post-incident review | {{cite or "not found"}} | {{1–5}} |
| Architecture diagrams (current) and ADRs for major decisions; data-flow diagram for PII (where it enters, moves, is stored) | {{cite docs/}} | {{1–5}} |
| API documentation (OpenAPI or equivalent) complete and current; accessibility (WCAG 2.1 AA) addressed for user-facing surfaces | {{cite}} | {{1–5}} |
| Onboarding docs don't depend on tribal knowledge from one person; dependency map shows what this service talks to and what depends on it | {{cite or ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Dimension 10: Operations & Oncall

| Check | Evidence | Score |
|---|---|---|
| SLOs / SLAs defined; "what counts as down" is quantified; error budget tracked | {{cite or ask user}} | {{1–5}} |
| Oncall rotation with clear escalation; incident severity levels (SEV1-4) defined with response-time expectations; communication templates ready for customer-facing incidents | {{ask user}} | {{1–5}} |
| Blameless postmortems for significant incidents; action items tracked to closure; runbooks tested by someone other than their author | {{ask user}} | {{1–5}} |
| DR plans tested via real drills; game days run at least quarterly; graceful degradation plan documented (what to turn off first under extreme load) | {{ask user}} | {{1–5}} |
| Capacity and cost monitoring in place; quarterly capacity review; upstream dependency health tracked (you know when a provider is degraded before users tell you) | {{cite}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Dimension 11: Data Management

> Promote to **CRITICAL** if the system owns durable user / business data, financial records, or anything where loss is unacceptable.

| Check | Evidence | Score |
|---|---|---|
| Database migrations are backwards-compatible, linted in CI for unsafe operations (squawk / atlas / migra — non-concurrent indexes, NOT NULL on large tables, destructive changes), and tested against production-size data, not empty schemas | {{cite migration files + CI lint step}} | {{1–5}} |
| Backups run, are tested via real restorations, and the restoration procedure is rehearsed regularly | {{cite or ask user}} | {{1–5}} |
| Point-in-time recovery or cross-region replication available where RPO/RTO requires | {{cite}} | {{1–5}} |
| Data retention and deletion policies implemented (GDPR/CCPA where applicable); soft deletes where auditability requires | {{cite}} | {{1–5}} |
| RPO and RTO formally defined and tested — you know how much data you can lose and how long recovery takes | {{ask user}} | {{1–5}} |
| Data integrity enforced at the database level (constraints, foreign keys); databases, backups, and object storage encrypted at rest; UTC / timezone handling explicit | {{cite}} | {{1–5}} |

**Subtotal**: {{X}} / 30

**Key gaps**:
**Priority**:

---

## Dimension 12: Compliance & Governance

> Promote to **CRITICAL** for regulated industries (healthcare/HIPAA, finance/PCI-DSS/SOX, EU consumer/GDPR, public sector).

| Check | Evidence | Score |
|---|---|---|
| Licence compliance audited for all dependencies (no GPL in proprietary code without legal review); SBOM available | {{cite LICENSE, NOTICE, SBOM}} | {{1–5}} |
| Data residency requirements met — personal data stored in approved regions | {{cite IaC region config}} | {{1–5}} |
| Audit trail for sensitive data access and modifications; logs immutable and retained per policy | {{cite}} | {{1–5}} |
| Access reviews conducted periodically; former employees and contractors removed promptly; least-privilege enforced for service accounts and IAM roles | {{ask user}} | {{1–5}} |
| Privacy impact assessment completed for features handling personal data; DPAs in place with third-party processors; regulatory scope mapped to technical controls | {{ask user}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Dimension 13: Dependency Management

> Promote to **CRITICAL** for software shipped to customers (SDKs, on-prem products) or systems where supply-chain compromise has wide blast radius.

| Check | Evidence | Score |
|---|---|---|
| Dependencies pinned to exact versions with lockfiles committed and reviewed | {{cite lockfile}} | {{1–5}} |
| Automated dependency updates (Dependabot / Renovate) with CI gating on vulnerability scans | {{cite config}} | {{1–5}} |
| Vulnerable dependencies patched within defined SLAs (e.g., critical 24h, high 7d) | {{cite policy or ask user}} | {{1–5}} |
| Fallback plan documented for every critical third-party dependency; their SLAs reviewed and accounted for in your own SLA calculations | {{ask user}} | {{1–5}} |
| No abandoned or unmaintained libraries in critical paths; transitive dependency tree audited (you know what you're actually shipping) | {{cite audit}} | {{1–5}} |

**Subtotal**: {{X}} / 25

**Key gaps**:
**Priority**:

---

## Summary

| Dimension | Score | Max | % | Status |
|---|---|---|---|---|
| 1. Functional Correctness & Testing | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 2. Error Handling & Resilience (CRITICAL) | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 3. Observability (CRITICAL) | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 4. Security (CRITICAL) | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 5. Maintainability & Code Quality | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 6. CI/CD & Release Process (CRITICAL) | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 7. Configuration & Environment Management | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 8. Performance & Scalability | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 9. Documentation & Knowledge | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 10. Operations & Oncall | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 11. Data Management {{(CRITICAL if data-owning)}} | {{X}} | 30 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 12. Compliance & Governance {{(CRITICAL if regulated)}} | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| 13. Dependency Management {{(CRITICAL if shipped/wide-blast-radius)}} | {{X}} | 25 | {{Y}}% | {{✓ / ⚠ / ✗}} |
| **Total** | **{{X}}** | **360** | **{{Y}}%** | |

### Interpretation

- ≥ 306 (85%+): Mature production system; can serve as an internal reference
- 252–305 (70–84%): Production-grade with room to improve
- 180–251 (50–69%): Live but carries meaningful risk; needs phased hardening
- < 180 (< 50%): Not production-grade; should not carry business-critical load

### Critical dimension gate (cost of failure: {{LEVEL}})

Default critical dimensions are Error Handling, Observability, Security, and CI/CD. Promote any of Data Management, Compliance & Governance, or Dependency Management to critical based on project type — note explicitly which were promoted and why.

| Critical dimension | Required | Actual | Pass? |
|---|---|---|---|
| Error Handling & Resilience | {{≥ X / 30}} | {{actual}} | {{✓ / ✗}} |
| Observability | {{≥ X / 30}} | {{actual}} | {{✓ / ✗}} |
| Security | {{≥ X / 30}} | {{actual}} | {{✓ / ✗}} |
| CI/CD & Release Process | {{≥ X / 30}} | {{actual}} | {{✓ / ✗}} |
| {{Data Management — if promoted}} | {{≥ X / 30}} | {{actual}} | {{✓ / ✗}} |
| {{Compliance & Governance — if promoted}} | {{≥ X / 25}} | {{actual}} | {{✓ / ✗}} |
| {{Dependency Management — if promoted}} | {{≥ X / 25}} | {{actual}} | {{✓ / ✗}} |

**Overall gate result**: {{PASS / FAIL}}

{{If FAIL, explain which dimension failed and why this blocks production-readiness.}}

---

## Action plan

Top improvements ordered by impact × ease.

### 1. {{Specific gap, named after the finding}}
- **Why it matters**: {{tie to a real risk}}
- **Current state**: {{cite evidence from the report}}
- **Target state**: {{concrete, observable}}
- **Estimated effort**: {{S / M / L}}
- **Owner / timeline**: {{TBD}}

### 2. {{...}}
- ...

### 3. {{...}}
- ...

---

## Recommended reassessment

- **Next review**: {{date suggestion, e.g., 60 days}}
- **Focus areas**: {{which dimensions to re-check first}}
- **Trigger reassessment early if**: {{e.g., "a major incident occurs", "traffic doubles", "team grows past 10 engineers", "new regulated data type introduced"}}

---

## Appendix: Inventory

What the scan found in the repo (from `scripts/scan_signals.py` or manual inspection):

- Languages: {{list with file counts}}
- Package manifests + lockfiles: {{list}}
- CI workflows: {{list}}
- Test directories: {{list with counts}}
- Docker / IaC: {{list}}
- Documentation: {{list}}
- Data layer (migrations, backup config, ORM schema): {{list}}
- Licence / compliance files (LICENSE, NOTICE, SBOM, SECURITY.md, PRIVACY): {{list}}
- Dependency-hygiene config (dependabot, renovate): {{list}}
- Notable absences: {{e.g., "no SECURITY.md, no runbook, no LICENSE, no .github/dependabot.yml, no migration history"}}
