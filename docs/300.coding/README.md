# Phase 300 — Coding

## Overview
The Coding phase transforms frozen design artifacts into a working, linter-enforced, observably-instrumented codebase with CI/CD, automated tests, and versioned migrations.

## Mission
Produce a working Unique ID Generator service that implements the Snowflake algorithm, persists IDs asynchronously to PostgreSQL, and exposes health/metrics endpoints — all with automated enforcement of architectural boundaries.

## Phase Structure

```
docs/300.coding/
├── README.md                    ← You are here
├── 301.generator-scaffold.md    ← Generator project setup
├── 302.domain-layer.md          ← Snowflake domain implementation
├── 303-transport-layer.md       ← HTTP controllers
├── 304-infrastructure.md        ← Adapters, persistence
└── 305-ci-cd.md                 ← CI/CD pipeline
```

## Engineering Activities

### 2.1 Architectural Enforcement
- ESLint boundaries plugin configured
- No framework imports in `src/domain`
- No ORM entities in domain layer
- Dependency injection via constructor

### 2.2 Version Control & CI/CD
- Trunk-based development
- Fast unit/integration tests per PR
- Separate slow E2E on merge to main
- PR size capped at ~400 LOC

### 2.3 Shift-Left Quality
- Test behaviors, not implementations
- Pre-generated ID tests with uniqueness verification
- Contract tests for API responses

### 2.4 Defensive Programming
- Structured JSON logging
- Correlation ID propagation
- Circuit breakers for external calls
- Centralized error handling

## Deliverables

| Deliverable | Status |
|-------------|--------|
| Generator project scaffold | ✅ |
| Snowflake domain service | ✅ |
| Clock abstraction | ✅ |
| HTTP controller + /generate | ✅ |
| /health endpoint | ✅ |
| /metrics endpoint | ✅ |
| Unit tests | ✅ |
| CI/CD pipeline | ✅ |
| Boundary enforcement | ✅ |

## Quick-Reference Summary

### Mission
Implement a distributed Snowflake ID generator capable of 10K+ RPS with async PostgreSQL persistence, nginx load balancing across 3 instances, and a health dashboard.

### Key Decisions
- **Hexagonal Architecture** — Domain is pure Python, no framework dependencies
- **Async Persistence** — Non-blocking writes via queue, graceful degradation
- **least_conn Load Balancing** — Best performance for varying request times
- **Structured Logging** — JSON logs with correlation IDs
- **Boundary Enforcement** — Linter fails CI if domain imports infrastructure

### Critical Artifacts
- `src/generator/domain/` — Pure domain logic
- `src/generator/interfaces/` — HTTP controllers
- `src/generator/infrastructure/` — Adapters
- `pyproject.toml` — Dependencies
- `.github/workflows/` — CI/CD
- `.eslintrc` — Boundary rules

### Open Blockers
- None

### Next-Phase Handoff
→ Phase 400 (Testing) requires:
- Working generator service
- docker-compose stack running
- Unit tests written

## Status
- [x] Phase 300 initiated
- [x] Sprint 1 tasks defined
- [x] Implementation complete ✅
