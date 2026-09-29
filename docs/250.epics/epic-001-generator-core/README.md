# Epic 001 — Generator Core

## Overview
Implement the core Snowflake ID generation algorithm with HTTP interface.

## Epic Goal
A working generator service that produces unique 64-bit Snowflake IDs via HTTP.

## Tasks

### Task 001: Project Scaffolding
- **Layer:** Delivery
- **Effort:** 2h
- **Files Created:**
  - `src/generator/__init__.py`
  - `src/generator/main.py`
  - `pyproject.toml`
  - `poetry.lock`

### Task 002: Snowflake Domain Service
- **Layer:** Domain
- **Effort:** 4h
- **Files Created:**
  - `src/generator/domain/__init__.py`
  - `src/generator/domain/models/__init__.py`
  - `src/generator/domain/models/snowflake_id.py`
  - `src/generator/domain/services/__init__.py`
  - `src/generator/domain/services/id_generator.py`
- **Acceptance Criteria:**
  - `IdGeneratorService.generate_id()` returns `SnowflakeId`
  - ID is 64-bit integer
  - ID contains correct timestamp, datacenter, machine, sequence bits

### Task 003: Clock Abstraction
- **Layer:** Domain
- **Effort:** 2h
- **Files Created:**
  - `src/generator/domain/ports/__init__.py`
  - `src/generator/domain/ports/clock.py`
  - `src/generator/infrastructure/adapters/__init__.py`
  - `src/generator/infrastructure/adapters/system_clock.py`
- **Acceptance Criteria:**
  - `IClock` interface defined
  - `SystemClock` implements `IClock`
  - Clock is injectable for testing

### Task 004: HTTP Controller
- **Layer:** Transport
- **Effort:** 2h
- **Files Created:**
  - `src/generator/interfaces/__init__.py`
  - `src/generator/interfaces/http/__init__.py`
  - `src/generator/interfaces/http/router.py`
- **Acceptance Criteria:**
  - GET /generate returns `{"id": <64-bit-int>}`
  - HTTP 200 on success
  - HTTP 500 on error with `{"error": "...", "code": "..."}`

### Task 005: Health Endpoint
- **Layer:** Transport
- **Effort:** 1h
- **Files Created:**
  - `src/generator/interfaces/health/__init__.py`
  - `src/generator/interfaces/health/controller.py`
- **Acceptance Criteria:**
  - GET /health returns `{"status": "ok", "instance": "dc-01-machine-01", ...}`
  - HTTP 200 when healthy
  - HTTP 503 when unhealthy

### Task 006: Metrics Endpoint
- **Layer:** Transport
- **Effort:** 2h
- **Files Created:**
  - `src/generator/interfaces/metrics/__init__.py`
  - `src/generator/interfaces/metrics/controller.py`
- **Acceptance Criteria:**
  - GET /metrics returns Prometheus format
  - `ids_generated_total` counter exposed
  - `request_duration_seconds` histogram exposed

### Task 007: Unit Tests for Domain
- **Layer:** Testing
- **Effort:** 4h
- **Files Created:**
  - `tests/__init__.py`
  - `tests/unit/__init__.py`
  - `tests/unit/domain/__init__.py`
  - `tests/unit/domain/test_snowflake_id.py`
  - `tests/unit/domain/test_id_generator.py`
- **Acceptance Criteria:**
  - ≥80% coverage on domain layer
  - All tests pass
  - ID uniqueness verified
  - Sequence overflow handling tested

---

## BDD Acceptance Criteria

### Scenario: Generate unique ID
```
Given a healthy generator instance
When I call GET /generate
Then I receive a JSON response with a 64-bit id
And the id is globally unique
And the id contains valid timestamp, datacenter, machine, and sequence bits
```

### Scenario: Handle sequence overflow
```
Given a generator has generated 4096 IDs in the same millisecond
When I call GET /generate again
Then the generator waits for the next millisecond
And returns a unique ID with sequence=0
```

### Scenario: Clock goes backwards
```
Given the system clock went backwards by more than 10ms
When I call GET /generate
Then I receive HTTP 500
And the response contains {"code": "CLOCK_BACKWARDS"}
```

---

## Definition of Done

- [x] All 7 tasks completed
- [x] GET /generate works and returns unique IDs
- [x] GET /health works and returns correct status
- [x] GET /metrics returns Prometheus format
- [x] Unit tests pass with ≥80% coverage
- [x] Lint clean
- [x] Typecheck clean

## Status
- [ ] Not started
- [ ] In progress
- [x] Complete ✅

## Related
- Parent: Phase 300 Coding
- Design: `docs/200.design/02-hexagonal/202.hexagonal-architecture.md`
