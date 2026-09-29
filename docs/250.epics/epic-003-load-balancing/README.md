# Epic 003 — Load Balancing

## Overview
Configure nginx as load balancer across 3 generator instances.

## Epic Goal
nginx distributes requests across all healthy generator instances with automatic removal of unhealthy instances.

## Tasks

### Task 001: nginx Configuration
- **Layer:** Infrastructure
- **Effort:** 2h
- **Files Created:**
  - `nginx/nginx.conf`
  - `nginx/conf.d/default.conf`
- **Acceptance Criteria:**
  - Upstream block configured with 3 generators
  - least_conn algorithm configured
  - Passive health checks configured

### Task 002: nginx Dockerfile
- **Layer:** Delivery
- **Effort:** 1h
- **Files Created:**
  - `nginx/Dockerfile`
- **Acceptance Criteria:**
  - Docker image builds successfully
  - Health check configured
  - Starts without errors

### Task 003: Integration Tests
- **Layer:** Testing
- **Effort:** 2h
- **Files Created:**
  - `tests/integration/test_load_balancing.py`
- **Acceptance Criteria:**
  - Requests distributed across generators
  - Unhealthy generator removed from pool
  - All generators down returns 503

---

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
Given generator-2 is unhealthy
When I send requests to nginx
Then nginx removes generator-2 from the pool
And requests are distributed to healthy generators
And no requests are sent to generator-2
```

### Scenario: All generators unavailable
```
Given all 3 generators are unhealthy
When I send a request to nginx
Then I receive HTTP 503
And the response contains {"code": "GENERATORS_UNAVAILABLE"}
```

---

## Definition of Done

- [x] All 3 tasks completed
- [x] nginx configuration correct
- [x] Dockerfile builds (uses nginx:alpine)
- [x] Health checks work
- [x] Load balancing verified (3 generators, least_conn)

## Status
- [ ] Not started
- [ ] In progress
- [x] Complete ✅

## Related
- Parent: Phase 300 Coding
- Design: `docs/200.design/04-nginx/204.nginx-configuration.md`
- Depends on: Epic 001 (Generator Core)
