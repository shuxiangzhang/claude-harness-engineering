# Stack-Specific Signals

What "good" looks like per stack. Load only the sections relevant to the project. For polyglot repos, load multiple. These signals are evidence — finding them is positive; not finding them isn't automatically negative (some are optional), but their absence raises follow-up questions.

## Table of contents

- [Node.js / TypeScript](#nodejs--typescript)
- [Python](#python)
- [Go](#go)
- [Java / Kotlin (JVM)](#java--kotlin-jvm)
- [Ruby](#ruby)
- [Rust](#rust)
- [.NET / C#](#net--c)
- [PHP](#php)
- [Generic / cross-stack](#generic--cross-stack)

---

## Node.js / TypeScript

**Manifests**: `package.json`, `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` (lockfile must exist and be committed).

**Testing**: Jest / Vitest / Mocha config; `__tests__/`, `*.test.ts`, `*.spec.ts`. Look for `jest.config.*`, coverage thresholds, snapshot tests. Integration tests often in `tests/integration/` or `e2e/`. Playwright / Cypress for E2E.

**Linting / formatting / types**: ESLint config (`.eslintrc*`, `eslint.config.js`), Prettier (`.prettierrc*`), TypeScript (`tsconfig.json` with `strict: true`). Husky / lint-staged hooks suggest enforcement before commit.

**CI**: `.github/workflows/*.yml` running `npm test`, `npm run lint`, `npm run build`, `npm audit` or `npm run audit:ci`.

**Error handling**: Look for `try/catch` around `await` calls, global error handlers (Express `app.use((err, req, res, next) => ...)`), `process.on('uncaughtException')`, async error boundaries in React.

**Observability**: `pino` / `winston` / `bunyan` for logging; `@opentelemetry/*` packages for tracing; `prom-client` for metrics; Sentry / Datadog SDKs.

**Security**: `npm audit` in CI, Snyk / Socket integration, Dependabot config (`.github/dependabot.yml`), Helmet for Express apps, CSP headers, `bcrypt` / `argon2` for password hashing.

**Config**: `dotenv` for local dev only, environment variables for production. `convict` / `zod` schemas for config validation. Avoid `process.env.X || 'default'` scattered across the codebase.

**Red flags**: `node_modules` committed, `.env` files committed, `eval()`, `child_process.exec()` with user input, missing `package-lock.json`, `console.log` for production logging.

---

## Python

**Manifests**: `pyproject.toml` (modern) or `setup.py` + `requirements.txt`. Lockfile via `poetry.lock`, `Pipfile.lock`, `uv.lock`, `requirements.lock`. Pinned dependencies, not loose ranges.

**Testing**: `pytest` config in `pyproject.toml` or `pytest.ini`. Tests in `tests/` or `test_*.py`. Look for fixtures, parametrised tests, `pytest-cov` for coverage, `tox` or `nox` for matrix testing. `hypothesis` for property-based tests is a strong positive.

**Linting / formatting / types**: `ruff` (modern, fast) or `flake8` + `black` + `isort`. `mypy` or `pyright` for type checking — look for `mypy.ini` / `[tool.mypy]` section and whether `strict = true`. `pre-commit` config.

**CI**: GitHub Actions / GitLab / etc. running `pytest`, `ruff check`, `mypy`, `safety check` or `pip-audit`.

**Error handling**: Specific exception classes (not bare `except:`), context managers for resources, `logging` module with structured config, exception chaining (`raise X from Y`). Look for `tenacity` / `backoff` for retries.

**Observability**: `structlog` for structured logging, `opentelemetry-*` packages, `prometheus_client`, Sentry SDK. `python-json-logger` for JSON logs.

**Security**: `bandit` for static analysis, `pip-audit` or `safety` in CI, Dependabot. ORM usage (SQLAlchemy / Django ORM) instead of raw SQL. `cryptography` library for crypto operations.

**Config**: `pydantic-settings` or `dynaconf` for typed config. Avoid `os.environ['X']` scattered everywhere — should be loaded once.

**Red flags**: `except Exception: pass`, `eval()` / `exec()` with input, `shell=True` in `subprocess` with input, `pickle.loads()` on untrusted data, `requirements.txt` without pins, `pdb.set_trace()` left in code.

---

## Go

**Manifests**: `go.mod`, `go.sum`. `go.sum` must be committed.

**Testing**: `*_test.go` files alongside source. `go test ./...` in CI. Look for table-driven tests, `t.Parallel()`, benchmarks (`Benchmark*` functions), fuzz tests (`Fuzz*`). `testcontainers-go` for integration tests is a strong positive.

**Linting**: `golangci-lint` config (`.golangci.yml`). `go vet` in CI. `staticcheck` either via golangci-lint or standalone.

**CI**: Runs `go build`, `go test -race -cover`, `golangci-lint run`, possibly `govulncheck`.

**Error handling**: Idiomatic Go means returning errors, not panics. Look for `errors.Wrap` / `fmt.Errorf("... : %w", err)`, `errors.Is` / `errors.As` for typing. Context propagation (`context.Context` as first arg) for cancellation/timeouts.

**Observability**: `slog` (stdlib) or `zap` / `zerolog` for structured logging. `go.opentelemetry.io/otel` for tracing. `prometheus/client_golang` for metrics.

**Security**: `govulncheck` in CI, Dependabot. SQL via parameterised queries (`sql.DB.Query` with `?` placeholders).

**Config**: `viper` is common but heavy; small services often roll their own with `flag` + env. Look for centralised config loading, not `os.Getenv` everywhere.

**Red flags**: `panic()` used as error handling, ignoring returned errors (`_ = doThing()`), no context propagation, `interface{}` everywhere.

---

## Java / Kotlin (JVM)

**Manifests**: `pom.xml` (Maven) or `build.gradle` / `build.gradle.kts` (Gradle). Wrapper scripts (`mvnw`, `gradlew`) committed.

**Testing**: JUnit 5 in `src/test/java`. Look for Mockito, AssertJ, Testcontainers, Spring Boot Test. Coverage via JaCoCo plugin.

**Linting**: Checkstyle / SpotBugs / Error Prone / detekt (Kotlin) / ktlint. Look in build files for plugins.

**CI**: Builds + tests + linting. SonarQube integration is common in enterprise.

**Error handling**: Specific exceptions, try-with-resources for AutoCloseable, no swallowed `InterruptedException`. Spring Boot apps: global `@ControllerAdvice` handlers.

**Observability**: SLF4J + Logback, Micrometer for metrics, Spring Boot Actuator endpoints, OpenTelemetry Java agent or SDK.

**Security**: OWASP Dependency Check, Snyk, Spring Security for authn/authz, JJWT for tokens. SQL via JPA / parameterised queries.

**Config**: `application.yml` per profile (dev/staging/prod), `@ConfigurationProperties` for typed config, Spring Cloud Config or HashiCorp Vault for secrets.

**Red flags**: `catch (Exception e) { e.printStackTrace(); }`, raw JDBC string concatenation, secrets in `application.properties` committed to git.

---

## Ruby

**Manifests**: `Gemfile`, `Gemfile.lock` (must be committed).

**Testing**: RSpec (`spec/`) or Minitest (`test/`). `simplecov` for coverage. Feature/system specs with Capybara for E2E.

**Linting**: RuboCop config (`.rubocop.yml`). `standard` is a common alternative.

**CI**: Runs `bundle exec rspec`, `rubocop`, `brakeman` (Rails security scanner), `bundler-audit`.

**Error handling**: Specific exception classes, retries via `retryable` or similar, ActiveJob for async with retry policies.

**Observability**: Lograge for structured Rails logs, OpenTelemetry Ruby SDK, Skylight / New Relic / Datadog APM.

**Security**: Brakeman in CI, `bundler-audit`, Rails has built-in protections (look for them not being disabled — `protect_from_forgery`, `strong_parameters`).

**Red flags**: `rescue => e` (rescues StandardError implicitly, often too broad), `eval()`, mass-assignment without strong params, `Marshal.load` on untrusted data.

---

## Rust

**Manifests**: `Cargo.toml`, `Cargo.lock` (committed for binaries, optionally for libraries).

**Testing**: `cargo test`, `#[test]` and `#[cfg(test)]` modules. Integration tests in `tests/`. Doc tests in `///` comments. `cargo-tarpaulin` or `llvm-cov` for coverage.

**Linting**: `cargo clippy -- -D warnings`. `rustfmt` enforced via `cargo fmt --check`.

**CI**: `cargo build`, `cargo test`, `cargo clippy`, `cargo audit` for vulnerabilities, `cargo-deny` for license/security policy.

**Error handling**: `Result<T, E>` everywhere (not `unwrap()` in production paths). `thiserror` for error types, `anyhow` for application-level errors. `?` operator for propagation.

**Observability**: `tracing` crate (de facto standard), `tracing-subscriber` for output, `opentelemetry-rust` for distributed tracing, `metrics` crate.

**Security**: `cargo audit` in CI, Dependabot, `#![forbid(unsafe_code)]` at crate root where appropriate.

**Red flags**: `.unwrap()` / `.expect()` scattered in production code paths, `unsafe` blocks without explanation, no `Cargo.lock` for binaries.

---

## .NET / C#

**Manifests**: `*.csproj`, `*.sln`, `Directory.Packages.props` for central package management.

**Testing**: xUnit / NUnit / MSTest. `*Tests.csproj` projects. Coverlet for coverage.

**Linting**: `.editorconfig` with code style rules, Roslyn analyzers enabled, StyleCop.

**CI**: `dotnet build`, `dotnet test`, `dotnet format --verify-no-changes`.

**Error handling**: Specific exception types, `try/catch/finally`, `using` statements (or `using` declarations in C# 8+) for IDisposable.

**Observability**: `Microsoft.Extensions.Logging` with Serilog / NLog providers, OpenTelemetry .NET SDK, Application Insights.

**Security**: `dotnet list package --vulnerable`, OWASP Dependency Check, ASP.NET Core security headers middleware.

**Config**: `appsettings.json` per environment, `IOptions<T>` pattern, Azure Key Vault / AWS Secrets Manager for secrets.

**Red flags**: `catch (Exception) { }`, SQL string concatenation, hardcoded connection strings.

---

## PHP

**Manifests**: `composer.json`, `composer.lock`.

**Testing**: PHPUnit, Pest. Tests in `tests/`. Coverage with Xdebug or PCOV.

**Linting**: PHP_CodeSniffer, PHP-CS-Fixer, PHPStan / Psalm for static analysis.

**CI**: Runs PHPUnit, static analyzers, `composer audit`.

**Error handling**: Specific exception classes, try/catch, `set_exception_handler` for top-level. PSR-3 logger.

**Observability**: Monolog for logging, OpenTelemetry PHP SDK.

**Security**: PDO with prepared statements (not `mysql_query`), input filtering, CSP headers, `password_hash` / `password_verify`.

**Red flags**: `mysql_*` functions (deprecated), `eval()`, `extract()` of user input, SQL via string interpolation.

---

## Generic / cross-stack

These apply regardless of language:

**Containerisation**: `Dockerfile` (multi-stage builds for prod, non-root user, pinned base image versions, no secrets baked in). `.dockerignore` present. `docker-compose.yml` for local dev. Image scanning in CI (Trivy, Grype).

**Infrastructure as Code**: `terraform/`, `*.tf`, `pulumi/*.py`, `cloudformation/`. Look for state backend config, modules, environments separated.

**Kubernetes**: `k8s/`, `helm/`, `kustomization.yaml`. Resource limits set, liveness/readiness probes defined, PodDisruptionBudget for production workloads.

**GitOps**: ArgoCD / Flux manifests in `argocd/` or similar.

**Database migrations**: Look for `migrations/`, `db/migrate/`, `flyway/`, `liquibase/`, `alembic/`. Migrations should be versioned, reversible, and not destructive without explicit guards.

**Secrets**: Search for committed secrets — `git log -p | grep -i 'password\|api_key\|secret'` (or equivalent). Look for use of Vault, AWS Secrets Manager, GCP Secret Manager, Doppler, 1Password CLI.

**Pre-commit hooks**: `.pre-commit-config.yaml`, `.husky/`. Reduces classes of issues from reaching CI.

**Top-level docs**: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `RUNBOOK.md` or `OPERATIONS.md`, `docs/architecture/`, `docs/adr/`.

**Repo hygiene**: `.gitignore` excludes `node_modules`, `__pycache__`, `target/`, `.env`, IDE configs. No large binary blobs. No commits with secrets in git history.
