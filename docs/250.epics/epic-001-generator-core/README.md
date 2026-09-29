# Epic 001 — Generator Core

## Overview
Implement the core Snowflake ID generation algorithm with HTTP interface.

## Tasks

| Task | Description | Layer | Effort |
|------|-------------|-------|--------|
| 001 | Project scaffolding | Delivery | 2h |
| 002 | Implement Snowflake domain service | Domain | 4h |
| 003 | Implement clock abstraction | Domain | 2h |
| 004 | Implement HTTP controller | Transport | 2h |
| 005 | Add /health endpoint | Transport | 1h |
| 006 | Add /metrics endpoint | Transport | 2h |
| 007 | Unit tests for domain | Testing | 4h |

## BDD Acceptance Criteria

### Scenario: Generate unique ID
```
Given a healthy generator instance
When I call GET /generate
Then I receive a JSON response with a 64-bit id
And the id is globally unique
And the id contains valid timestamp, datacenter, machine, and sequence bits
```

### Scenario: Handle sequence overflow
```
Given a generator has generated 4096 IDs in the same millisecond
When I call GET /generate again
Then the generator waits for the next millisecond
And returns a unique ID with sequence=0
```

## Status
- [ ] Not started
- [ ] In progress
- [ ] Complete
