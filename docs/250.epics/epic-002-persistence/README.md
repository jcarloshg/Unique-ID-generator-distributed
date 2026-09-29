# Epic 002 — Persistence

## Overview
Implement PostgreSQL async persistence for generated IDs.

## Tasks

| Task | Description | Layer | Effort |
|------|-------------|-------|--------|
| 001 | Design database schema | Data | 2h |
| 002 | Create migration scripts | Data | 2h |
| 003 | Implement repository adapter | Infrastructure | 4h |
| 004 | Implement async write queue | Infrastructure | 4h |
| 005 | Add graceful degradation | Domain | 2h |
| 006 | Integration tests | Testing | 4h |

## BDD Acceptance Criteria

### Scenario: Persist ID to database
```
Given PostgreSQL is available
When a generator creates an ID
Then the ID is asynchronously written to the database
And the write does not block ID generation
```

### Scenario: Graceful degradation when DB unavailable
```
Given PostgreSQL is unavailable
When a generator creates an ID
Then the ID is returned to the client immediately
And the persistence failure is logged
And no error is returned to the client
```

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete
