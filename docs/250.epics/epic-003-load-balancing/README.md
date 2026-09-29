# Epic 003 — Load Balancing

## Overview
Configure nginx as load balancer across 3 generator instances.

## Tasks

| Task | Description | Layer | Effort |
|------|-------------|-------|--------|
| 001 | Configure nginx upstream | Infrastructure | 2h |
| 002 | Set up health checks | Infrastructure | 2h |
| 003 | Configure timeouts | Infrastructure | 1h |
| 004 | Integration tests | Testing | 2h |

## BDD Acceptance Criteria

### Scenario: Distribute requests across generators
```
Given 3 healthy generator instances
When I send 100 requests to nginx
Then requests are distributed across all generators
And no single generator receives more than 34-35 requests
```

### Scenario: Remove unhealthy generator
```
Given generator-2 is down
When I send requests to nginx
Then nginx removes generator-2 from the pool
And requests are distributed to healthy generators
And no requests are sent to generator-2
```

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete
