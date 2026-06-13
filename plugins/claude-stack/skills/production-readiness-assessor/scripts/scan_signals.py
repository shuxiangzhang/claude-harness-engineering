#!/usr/bin/env python3
"""Walk a repository and emit a JSON inventory of production-readiness signals.

Usage:
    python scan_signals.py <repo-path>
    python scan_signals.py <repo-path> --output signals.json

Output: JSON with detected languages, manifests, CI configs, tests, docker/IaC,
docs, observability hints, and rough file counts. Designed to seed a
production-readiness assessment — it doesn't score anything, it just inventories.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Directories to skip entirely (vendored code, build artefacts, caches)
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "target", "build",
    "dist", "out", ".next", ".nuxt", "coverage", ".coverage",
    ".tox", ".nox", ".idea", ".vscode", ".gradle", "vendor",
    ".terraform", ".cache", "bin", "obj",
}

# File extensions → language
LANG_EXTS = {
    ".py": "Python",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java", ".kt": "Kotlin", ".scala": "Scala",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#", ".fs": "F#", ".vb": "VB.NET",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++",
    ".c": "C", ".h": "C",
    ".swift": "Swift",
    ".m": "Objective-C", ".mm": "Objective-C++",
    ".sh": "Shell", ".bash": "Shell",
    ".sql": "SQL",
    ".lua": "Lua",
    ".r": "R", ".R": "R",
    ".clj": "Clojure", ".cljs": "ClojureScript",
    ".ex": "Elixir", ".exs": "Elixir",
    ".elm": "Elm",
    ".dart": "Dart",
    ".hs": "Haskell",
    ".ml": "OCaml",
    ".zig": "Zig",
}

# Manifest file → likely stack
MANIFESTS = {
    "package.json": "Node.js / JavaScript / TypeScript",
    "pyproject.toml": "Python (modern)",
    "setup.py": "Python (legacy)",
    "requirements.txt": "Python",
    "Pipfile": "Python (pipenv)",
    "poetry.lock": "Python (poetry)",
    "uv.lock": "Python (uv)",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "pom.xml": "Java / Maven",
    "build.gradle": "Java / Gradle",
    "build.gradle.kts": "Kotlin / Gradle",
    "Gemfile": "Ruby",
    "composer.json": "PHP",
    "mix.exs": "Elixir",
    "Package.swift": "Swift",
    "pubspec.yaml": "Dart / Flutter",
    "Project.toml": "Julia",
}

# Lockfiles by manifest
LOCKFILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Pipfile.lock", "uv.lock", "requirements.lock",
    "go.sum", "Cargo.lock", "Gemfile.lock", "composer.lock",
    "mix.lock", "Package.resolved",
}

# CI config files / directories
CI_FILES = {
    ".github/workflows": "GitHub Actions",
    ".gitlab-ci.yml": "GitLab CI",
    ".circleci/config.yml": "CircleCI",
    "Jenkinsfile": "Jenkins",
    "azure-pipelines.yml": "Azure Pipelines",
    ".buildkite/pipeline.yml": "Buildkite",
    ".drone.yml": "Drone",
    "bitbucket-pipelines.yml": "Bitbucket Pipelines",
    ".travis.yml": "Travis CI",
    "appveyor.yml": "AppVeyor",
}

# Test directory / file patterns
TEST_DIRS = {"tests", "test", "__tests__", "spec", "specs", "e2e"}
TEST_FILE_PATTERNS = [
    re.compile(r".*_test\.go$"),
    re.compile(r".*\.test\.[jt]sx?$"),
    re.compile(r".*\.spec\.[jt]sx?$"),
    re.compile(r"test_.*\.py$"),
    re.compile(r".*_test\.py$"),
    re.compile(r".*_spec\.rb$"),
    re.compile(r".*Test\.(java|kt|cs)$"),
    re.compile(r".*Tests\.(cs|fs)$"),
]

# Docker / containerisation
DOCKER_FILES = ["Dockerfile", "Containerfile", ".dockerignore"]
DOCKER_PATTERNS = [re.compile(r"^Dockerfile.*"), re.compile(r"^docker-compose.*\.ya?ml$")]

# IaC indicators
IAC_DIRS = {"terraform", "pulumi", "cloudformation", "helm", "k8s", "kubernetes", "kustomize", "ansible"}
IAC_EXTS = {".tf", ".tfvars"}

# Doc files (top-level)
DOC_FILES = {
    "README.md", "README.rst", "README.txt", "README",
    "CONTRIBUTING.md", "CHANGELOG.md", "SECURITY.md",
    "CODE_OF_CONDUCT.md", "LICENSE", "LICENSE.md", "LICENSE.txt",
    "RUNBOOK.md", "OPERATIONS.md", "ARCHITECTURE.md", "DESIGN.md",
}
DOC_DIRS = {"docs", "doc", "documentation"}

# Migration directories
MIGRATION_DIRS = {"migrations", "migrate", "alembic", "flyway", "liquibase"}

# Observability / monitoring hints (search inside package manifests / requirements)
OBSERVABILITY_HINTS = {
    "opentelemetry", "otel", "sentry", "datadog", "newrelic", "new-relic",
    "prometheus", "prom-client", "prom_client",
    "pino", "winston", "bunyan",
    "structlog", "loguru",
    "zap", "zerolog", "slog",
    "tracing",  # rust
    "micrometer", "logback", "slf4j",
    "lograge",
    "serilog", "nlog",
    "monolog",
}

# Security hints
SECURITY_HINTS = {
    "dependabot", "snyk", "trivy", "grype",
    "bandit", "safety", "pip-audit", "brakeman", "bundler-audit",
    "govulncheck", "cargo-audit", "cargo-deny",
    "owasp", "semgrep",
    "vault", "secrets-manager", "kms",
    "helmet",  # node
}

# Secrets / config hints
SECRETS_HINTS = {
    "vault", "secrets-manager", "key-vault", "secret-manager",
    "doppler", "infisical", "1password",
}


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".") and name not in {".github", ".gitlab", ".circleci"}


def walk_repo(root: Path):
    """Yield (path, is_file) tuples, skipping irrelevant directories."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Mutate dirnames in-place to skip
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        rel_dir = Path(dirpath).relative_to(root)
        for d in dirnames:
            yield rel_dir / d, False
        for f in filenames:
            yield rel_dir / f, True


def detect_signals(root: Path) -> dict:
    signals = {
        "repo_path": str(root.resolve()),
        "languages": Counter(),
        "manifests": [],
        "lockfiles_committed": [],
        "ci": [],
        "test_dirs": [],
        "test_files_count": 0,
        "test_file_examples": [],
        "docker": [],
        "iac": [],
        "migration_dirs": [],
        "top_level_docs": [],
        "docs_dirs": [],
        "pre_commit_config": False,
        "dependabot_config": False,
        "editorconfig": False,
        "gitignore_present": False,
        "license_present": False,
        "security_md": False,
        "runbook_present": False,
        "architecture_docs": [],
        "observability_hints": [],
        "security_hints": [],
        "secret_management_hints": [],
        "total_files": 0,
        "warnings": [],
    }

    test_file_count = 0
    test_file_examples = []

    for rel_path, is_file in walk_repo(root):
        path_str = str(rel_path).replace("\\", "/")
        name = rel_path.name

        if not is_file:
            # Directory
            parts = path_str.split("/")
            # Record only top-level test roots, not every nested subdirectory under one.
            if name in TEST_DIRS and not any(p in TEST_DIRS for p in parts[:-1]):
                signals["test_dirs"].append(path_str)
            if name in IAC_DIRS:
                signals["iac"].append({"type": name, "path": path_str})
            if name in DOC_DIRS:
                signals["docs_dirs"].append(path_str)
            if name in MIGRATION_DIRS:
                signals["migration_dirs"].append(path_str)
            # GitHub workflows directory
            if path_str == ".github/workflows":
                # We'll enumerate the actual files below
                pass
            continue

        signals["total_files"] += 1

        # Language detection by extension
        ext = rel_path.suffix.lower()
        if ext in LANG_EXTS:
            signals["languages"][LANG_EXTS[ext]] += 1

        # Manifests
        if name in MANIFESTS:
            signals["manifests"].append({"file": path_str, "stack": MANIFESTS[name]})

        # Lockfiles
        if name in LOCKFILES:
            signals["lockfiles_committed"].append(path_str)

        # CI
        if name == ".gitlab-ci.yml":
            signals["ci"].append({"system": "GitLab CI", "file": path_str})
        elif path_str.startswith(".github/workflows/") and ext in {".yml", ".yaml"}:
            signals["ci"].append({"system": "GitHub Actions", "file": path_str})
        elif path_str == ".circleci/config.yml":
            signals["ci"].append({"system": "CircleCI", "file": path_str})
        elif name == "Jenkinsfile":
            signals["ci"].append({"system": "Jenkins", "file": path_str})
        elif name == "azure-pipelines.yml":
            signals["ci"].append({"system": "Azure Pipelines", "file": path_str})
        elif path_str == ".buildkite/pipeline.yml":
            signals["ci"].append({"system": "Buildkite", "file": path_str})
        elif name == ".drone.yml":
            signals["ci"].append({"system": "Drone", "file": path_str})
        elif name == "bitbucket-pipelines.yml":
            signals["ci"].append({"system": "Bitbucket Pipelines", "file": path_str})
        elif name == ".travis.yml":
            signals["ci"].append({"system": "Travis CI", "file": path_str})

        # Docker
        if name in DOCKER_FILES or any(p.match(name) for p in DOCKER_PATTERNS):
            signals["docker"].append(path_str)

        # IaC files
        if ext in IAC_EXTS:
            signals["iac"].append({"type": "terraform", "path": path_str})

        # Test files
        if any(p.match(name) for p in TEST_FILE_PATTERNS):
            test_file_count += 1
            if len(test_file_examples) < 10:
                test_file_examples.append(path_str)

        # Top-level docs (only count if at repo root)
        if "/" not in path_str and name in DOC_FILES:
            signals["top_level_docs"].append(name)
            if name.startswith("LICENSE"):
                signals["license_present"] = True
            if name == "SECURITY.md":
                signals["security_md"] = True
            if name in {"RUNBOOK.md", "OPERATIONS.md"}:
                signals["runbook_present"] = True
            if name in {"ARCHITECTURE.md", "DESIGN.md"}:
                signals["architecture_docs"].append(name)

        # Special config files (at repo root)
        if "/" not in path_str:
            if name == ".pre-commit-config.yaml":
                signals["pre_commit_config"] = True
            if name == ".editorconfig":
                signals["editorconfig"] = True
            if name == ".gitignore":
                signals["gitignore_present"] = True
        if path_str == ".github/dependabot.yml" or path_str == ".github/dependabot.yaml":
            signals["dependabot_config"] = True

    signals["test_files_count"] = test_file_count
    signals["test_file_examples"] = test_file_examples
    signals["languages"] = dict(signals["languages"].most_common())

    # Scan top manifests for observability / security / secrets hints
    for m in signals["manifests"]:
        try:
            content = (root / m["file"]).read_text(encoding="utf-8", errors="ignore").lower()
        except (OSError, UnicodeDecodeError):
            continue
        for hint in OBSERVABILITY_HINTS:
            if hint in content and hint not in signals["observability_hints"]:
                signals["observability_hints"].append(hint)
        for hint in SECURITY_HINTS:
            if hint in content and hint not in signals["security_hints"]:
                signals["security_hints"].append(hint)
        for hint in SECRETS_HINTS:
            if hint in content and hint not in signals["secret_management_hints"]:
                signals["secret_management_hints"].append(hint)

    # Warnings (things that are notably absent)
    if not signals["ci"]:
        signals["warnings"].append("No CI configuration detected")
    if not signals["test_dirs"] and signals["test_files_count"] == 0:
        signals["warnings"].append("No tests detected")
    if not signals["docker"] and not signals["iac"]:
        signals["warnings"].append("No containerisation or IaC detected")
    if not signals["security_md"]:
        signals["warnings"].append("No SECURITY.md")
    if not signals["runbook_present"]:
        signals["warnings"].append("No RUNBOOK.md or OPERATIONS.md")
    if not signals["dependabot_config"] and not signals["security_hints"]:
        signals["warnings"].append("No dependency vulnerability scanning detected")
    if not signals["lockfiles_committed"]:
        signals["warnings"].append("No lockfiles committed — dependency versions may be unpinned")

    return signals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Path to the repository to scan")
    parser.add_argument("--output", "-o", help="Write JSON output to this file (default: stdout)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        print(f"Error: {repo} does not exist", file=sys.stderr)
        sys.exit(1)
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    signals = detect_signals(repo)
    output = json.dumps(signals, indent=2 if args.pretty else None, sort_keys=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
