# Epic 005 — Infrastructure

## Overview
Set up Docker containerization and deployment configuration.

## Epic Goal
All services can be started with a single `docker-compose up` command.

## Tasks

### Task 001: Generator Dockerfile
- **Layer:** Infrastructure
- **Effort:** 2h
- **Files Created:**
  - `generator/Dockerfile`
  - `generator/pyproject.toml`
- **Acceptance Criteria:**
  - Multi-stage build
  - Non-root user
  - Docker image builds
  - Health check configured

### Task 002: docker-compose Configuration
- **Layer:** Infrastructure
- **Effort:** 2h
- **Files Created:**
  - `docker-compose.yml`
  - `docker-compose.override.yml`
- **Acceptance Criteria:**
  - All 6 services defined
  - Networks configured
  - Health checks configured
  - Environment variables set

### Task 003: PostgreSQL Init
- **Layer:** Data
- **Effort:** 1h
- **Files Created:**
  - `postgres/init.sql`
- **Acceptance Criteria:**
  - Schema created on first run
  - All indexes created
  - Migrations work

### Task 004: Environment Configuration
- **Layer:** Infrastructure
- **Effort:** 1h
- **Files Created:**
  - `.env.example`
- **Acceptance Criteria:**
  - All required env vars documented
  - Example values provided
  - Defaults are sensible

### Task 005: Local Dev Workflow
- **Layer:** Delivery
- **Effort:** 2h
- **Files Created:**
  - `Makefile`
  - `scripts/dev.sh`
- **Acceptance Criteria:**
  - `make up` starts all services
  - `make logs` shows logs
  - `make down` stops all services
  - `make test` runs tests

---

## BDD Acceptance Criteria

### Scenario: Start all services locally
```
Given I have Docker installed
When I run docker-compose up
Then nginx is running on port 80
And 3 generator instances are running
And PostgreSQL is running on port 5432
And dashboard is running on port 3000
```

### Scenario: Scale generators
```
Given the system is running
When I run docker-compose up --scale generator=5
Then 5 generator instances are running
And nginx distributes requests across all 5
```

### Scenario: View logs
```
Given the system is running
When I run docker-compose logs -f generator-1
Then I see the logs from generator-1
```

---

## Definition of Done

- [ ] All 5 tasks completed
- [ ] All Dockerfiles build
- [ ] docker-compose up works
- [ ] All services healthy
- [ ] Logs accessible
- [ ] Makefile works

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete

## Related
- Parent: Phase 300 Coding
- Design: `docs/200.design/05-deployment/205.deployment-specs.md`
- Depends on: All other epics
