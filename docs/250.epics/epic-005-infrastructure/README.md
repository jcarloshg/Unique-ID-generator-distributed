# Epic 005 — Infrastructure

## Overview
Set up Docker containerization and deployment configuration.

## Tasks

| Task | Description | Layer | Effort |
|------|-------------|-------|--------|
| 001 | Create generator Dockerfile | Infrastructure | 2h |
| 002 | Create nginx Dockerfile | Infrastructure | 1h |
| 003 | Create dashboard Dockerfile | Infrastructure | 1h |
| 004 | Create docker-compose.yml | Infrastructure | 2h |
| 005 | Configure environment variables | Infrastructure | 1h |
| 006 | Local dev workflow documentation | Delivery | 2h |

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

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete
