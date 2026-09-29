# Phase 400 — Testing

## Overview
The Testing phase executes the QA pipeline to certify the release candidate. It validates functional, contract, non-functional, and production readiness.

## Phase Structure

```
docs/400.testing/
├── README.md                    ← You are here
├── 01-unit/                    ← Unit tests
├── 02-integration/             ← Integration tests
├── 03-contract/               ← Contract tests
├── 04-performance/             ← Load & performance
└── 05-chaos/                   ← Chaos engineering
```

## Prerequisites
- [ ] Phase 300 (Coding) complete
- [ ] All sprints merged to main
- [ ] Test artifacts ready

## Testing Activities

### 01 — Unit Tests
- Domain logic testing
- ID generation algorithm verification
- Sequence overflow handling
- Clock validation

### 02 — Integration Tests
- PostgreSQL persistence
- nginx load balancing
- End-to-end /generate flow
- Health endpoint verification

### 03 — Contract Tests
- OpenAPI spec validation
- Response schema verification
- Error code compliance

### 04 — Performance Tests
- 10,000+ RPS sustained load
- P99 latency validation (<50ms)
- Burst traffic handling

### 05 — Chaos Tests
- Generator instance failure
- PostgreSQL unavailability
- nginx resilience

## Deliverables

### Test Reports
- `test-reports/unit-test-results.html`
- `test-reports/integration-test-results.html`
- `test-reports/load-test-results.html`
- `test-reports/chaos-report.html`

### Certified Release Candidate
- `certified-release.json` — Artifact SHA, test results, approvers

## Test Pyramid

```
        ┌───────────┐
        │    E2E    │  ← 5 critical journeys
       ┌───────────┐┐
       │  Contract ││  ← OpenAPI validation
      ┌───────────┐┐┐
      │Integration│││  ← Testcontainers
     ┌───────────┐┐┐┐
     │   Unit    ││││  ← Domain logic
    ┌───────────┐┐┐┐┐
    └───────────┴─┴─┴─┘
```

## Non-Functional Assertions

| NFR | Target | Assertion |
|-----|--------|-----------|
| Throughput | ≥10,000 RPS | k6 threshold passes |
| Latency P99 | <50ms | k6 threshold passes |
| Availability | 99.9% | Chaos tests pass |
| Error rate | <0.1% | Integration tests pass |

## Definition of Done

All phases must be green:
- [ ] 01-unit: All tests pass
- [ ] 02-integration: All tests pass
- [ ] 03-contract: OpenAPI validated
- [ ] 04-performance: SLOs met
- [ ] 05-chaos: Resilience verified

## Status
- [ ] Phase 400 initiated
- [ ] Test pyramid defined
- [ ] Tools selected (pytest, k6, Chaos Mesh)

## Next Phase
→ Production Deployment
