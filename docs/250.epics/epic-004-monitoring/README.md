# Epic 004 — Monitoring

## Overview
Build the Vite health dashboard for monitoring generator status.

## Tasks

| Task | Description | Layer | Effort |
|------|-------------|-------|--------|
| 001 | Set up Vite project | Delivery | 2h |
| 002 | Implement health polling | Transport | 4h |
| 003 | Display instance status | Delivery | 4h |
| 004 | Display metrics | Delivery | 4h |
| 005 | Dashboard E2E tests | Testing | 2h |

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

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete
