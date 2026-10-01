# Epic 004 — Monitoring

## Overview
Build the Vite health dashboard for monitoring generator status.

## Epic Goal
A web dashboard that displays the health and metrics of all generator instances in real-time.

## Tasks

### Task 001: Vite Project Setup
- **Layer:** Delivery
- **Effort:** 2h
- **Files Created:**
  - `dashboard/index.html`
  - `dashboard/package.json`
  - `dashboard/vite.config.ts`
  - `dashboard/tsconfig.json`
- **Acceptance Criteria:**
  - npm install succeeds
  - Dev server starts
  - Builds successfully

### Task 002: Health Polling
- **Layer:** Transport
- **Effort:** 4h
- **Files Created:**
  - `dashboard/src/api/generator.ts`
  - `dashboard/src/hooks/useHealthPolling.ts`
- **Acceptance Criteria:**
  - Fetches /health from each generator
  - Polls every 5 seconds
  - Handles errors gracefully

### Task 003: Instance Status Display
- **Layer:** Delivery
- **Effort:** 4h
- **Files Created:**
  - `dashboard/src/components/InstanceTable.tsx`
  - `dashboard/src/components/StatusBadge.tsx`
- **Acceptance Criteria:**
  - Shows 3 instances in table
  - Green/Yellow/Red status indicators
  - Instance ID displayed correctly

### Task 004: Metrics Display
- **Layer:** Delivery
- **Effort:** 4h
- **Files Created:**
  - `dashboard/src/components/MetricsCards.tsx`
  - `dashboard/src/components/LatencyChart.tsx`
- **Acceptance Criteria:**
  - Total IDs generated displayed
  - Requests/sec displayed
  - Error rate displayed

### Task 005: Dashboard Dockerfile
- **Layer:** Delivery
- **Effort:** 1h
- **Files Created:**
  - `dashboard/Dockerfile`
  - `dashboard/nginx.conf`
- **Acceptance Criteria:**
  - Docker image builds
  - Dashboard accessible on port 3000
  - Health data displays correctly

### Task 006: E2E Tests
- **Layer:** Testing
- **Effort:** 2h
- **Files Created:**
  - `tests/e2e/__init__.py` (or dashboard tests)
- **Acceptance Criteria:**
  - Dashboard loads without errors
  - Instances displayed correctly
  - Auto-refresh works

---

## BDD Acceptance Criteria

### Scenario: Display healthy system
```
Given all 3 generator instances are healthy
When I open the dashboard
Then I see 3 instances with "OK" status
And total IDs generated is displayed
And uptime is shown for each instance
```

### Scenario: Display degraded instance
```
Given generator-2 is degraded
When I open the dashboard
Then I see generator-2 with "DEGRADED" status
And I see the warning message
```

### Scenario: Display all down
```
Given all generators are down
When I open the dashboard
Then I see an error message
And I see a retry button
```

---

## Definition of Done

- [x] All 6 tasks completed
- [x] Dashboard shows all 3 instances
- [x] Status updates every 5 seconds
- [x] Metrics displayed correctly
- [x] Docker image builds (uses nginx:alpine)
- [ ] E2E tests pass (not created)

## Status
- [ ] Not started
- [ ] In progress
- [x] Complete ✅

## Related
- Parent: Phase 300 Coding
- Design: `docs/100.planning/103-functional/13.dashboard-spec.md`
- Depends on: Epic 001 (Generator Core)
