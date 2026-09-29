# Phase 405 — Chaos Engineering

## Overview
Execute chaos engineering drills to validate resilience.

## Objectives
- Validate generator failure handling
- Test PostgreSQL unavailability
- Verify nginx resilience
- Validate graceful degradation

## Chaos Scenarios

| Scenario | Experiment | Expected Outcome |
|----------|------------|------------------|
| Generator down | Kill generator-2 | LB removes from pool |
| All generators | Kill all 3 | Return 503 |
| DB unavailable | Kill PostgreSQL | Continue without DB |
| Clock drift | Advance clock back | Return 500, alert |
| Network partition | Drop packets | Timeout, return 503 |

## Tools

- Chaos Mesh (Kubernetes chaos)
- docker-compose (local chaos)
- Pumba (container chaos)

## Validation Checklist

- [ ] Circuit breaker opens on failure
- [ ] Fallback returns correct error
- [ ] Alert fires within 60 seconds
- [ ] Recovery is automatic

## Definition of Done
- [ ] All chaos scenarios validated
- [ ] No silent failures
- [ ] Alerts fire correctly
- [ ] Recovery automated

## Status
- [ ] Planned
- [ ] In progress
- [ ] Complete
