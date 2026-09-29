# Phase 400 — Testing

## Overview
The Testing phase certifies the release candidate through automated quality gates: unit tests, integration tests, and performance validation.

## Mission
Produce a Certified Release Candidate by running the full test suite against the implemented ID Generator service, verifying all endpoints work correctly and the system meets non-functional requirements.

## Phase Structure

```
docs/400.testing/
├── README.md                    ← You are here
└── 401.test-results.md          ← Test execution results
```

## Testing Activities

### 2.1 Unit Testing
- Domain layer: SnowflakeId model, IdGeneratorService
- 19 tests, 100% coverage on domain models
- All tests pass with pytest

### 2.2 Integration Testing
- HTTP endpoints via FastAPI TestClient
- Health endpoint verification
- Metrics endpoint verification
- Generate endpoint with ID uniqueness

### 2.3 Load Testing (k6)
- Verify 1000+ RPS capability
- P99 latency < 50ms
- Error rate < 0.01%

## Test Inventory

| Test Type | Location | Count | Status |
|-----------|----------|-------|--------|
| Unit - Domain Models | `tests/unit/domain/` | 10 | ✅ Pass |
| Unit - Services | `tests/unit/domain/` | 9 | ✅ Pass |
| Integration - HTTP | `tests/integration/` | 14 | ✅ Pass |
| Load - k6 | `tests/load/` | TBD | ⬜ Pending |

## NFR Validation

| Requirement | Target | Validation |
|-------------|--------|------------|
| RPS | 10,000+ | k6 load test |
| Latency P99 | < 100ms | k6 threshold |
| Availability | 99.9% | Circuit breaker |
| ID Uniqueness | 100% | Unit tests |

## Quick-Reference Summary

### Mission
Certify the ID Generator service through automated testing, validating correctness and performance before production deployment.

### Key Decisions
- **FastAPI TestClient** for integration tests — no external dependencies
- **pytest** as test runner with async support
- **IdGeneratorService singleton** in app.state for sequence management
- **100% domain coverage** — pure domain has no external dependencies

### Critical Artifacts
- `tests/unit/domain/test_snowflake_id.py` — 10 model tests, 100% coverage ✅
- `tests/unit/domain/test_id_generator.py` — 9 service tests, 82% coverage ✅
- `tests/integration/test_endpoints.py` — 14 HTTP integration tests ✅
- `docker-compose.yml` — Full stack for integration testing ✅
- `Dockerfile` — Container image for generator service ✅

### Open Blockers
- Load testing (k6) not yet implemented

### Next-Phase Handoff
→ Deployment ready with all unit and integration tests passing.

## Status
- [x] Phase 400 initiated
- [x] Unit tests pass (19 tests)
- [x] Integration tests pass (14 tests)
- [ ] Load tests pass (TBD - k6 not created)
- [ ] Release candidate certified
