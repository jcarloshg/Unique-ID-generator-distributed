# Phase 402 — Integration Tests

## Overview
Execute integration tests using Testcontainers.

## Objectives
- Test PostgreSQL persistence
- Test HTTP endpoints
- Test nginx load balancing
- Test end-to-end flows

## Test Inventory

| Test Suite | Description | Status |
|------------|-------------|--------|
| test_persistence | PostgreSQL writes | Pending |
| test_generate_endpoint | /generate endpoint | Pending |
| test_health_endpoint | /health endpoint | Pending |
| test_load_balancing | nginx distribution | Pending |
| test_graceful_degradation | DB failure handling | Pending |

## Infrastructure

- Testcontainers for PostgreSQL
- Real nginx instance
- 3 real generator instances

## Definition of Done
- [ ] All integration tests pass
- [ ] Testcontainers work in CI
- [ ] No test pollution
- [ ] Parallel safe

## Status
- [ ] Planned
- [ ] In progress
- [ ] Complete
