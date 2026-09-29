# Phase 250 — Epics & Tasks

## Overview
The Epics & Tasks phase breaks down frozen design artifacts into vertically-sliced, engineering-ready work items with BDD acceptance criteria.

## Phase Structure

```
docs/250.epics/
├── README.md                    ← You are here
├── epic-001-generator-core/    ← Core ID generation
├── epic-002-persistence/       ← PostgreSQL persistence
├── epic-003-load-balancing/    ← Nginx setup
├── epic-004-monitoring/         ← Health dashboard
└── epic-005-infrastructure/     ← Docker & deployment
```

## Epic Inventory

| Epic | Name | Description | Priority |
|------|------|-------------|----------|
| 001 | Generator Core | Snowflake ID generation algorithm | P0 |
| 002 | Persistence | PostgreSQL async writes | P1 |
| 003 | Load Balancing | nginx configuration | P1 |
| 004 | Monitoring | Health dashboard | P2 |
| 005 | Infrastructure | Docker deployment | P1 |

## Prerequisites
- [ ] Phase 200 (Design) complete
- [ ] All ADRs signed off
- [ ] API contracts frozen

## Deliverables

### Epics
- `epic-001-generator-core/README.md` — Epic 1 breakdown ✅
- `epic-002-persistence/README.md` — Epic 2 breakdown ✅
- `epic-003-load-balancing/README.md` — Epic 3 breakdown ✅
- `epic-004-monitoring/README.md` — Epic 4 breakdown ✅
- `epic-005-infrastructure/README.md` — Epic 5 breakdown ✅

### Tasks (per epic)
- `epic-001/tasks/` — 7 tasks defined
- `epic-002/tasks/` — 5 tasks defined
- `epic-003/tasks/` — 3 tasks defined
- `epic-004/tasks/` — 6 tasks defined
- `epic-005/tasks/` — 5 tasks defined

## Definition of Ready

Each task must have:
- [ ] Clear description
- [ ] BDD Given/When/Then acceptance criteria
- [ ] Technical layer identified (Data/Domain/Transport/Defense/Delivery)
- [ ] Dependencies listed
- [ ] Estimated effort

## Definition of Done

Each task must be:
- [ ] Code implemented
- [ ] Unit tests written
- [ ] Lint clean
- [ ] Typecheck passed
- [ ] PR merged

## Status
- [x] Phase 250 initiated
- [x] Epic inventory defined
- [x] All epics broken down with tasks ✅
- [x] Ready for sprint planning

## Implementation Status

| Epic | Status | Notes |
|------|--------|-------|
| 001 Generator Core | ✅ Complete | 33 tests pass |
| 002 Persistence | ✅ Complete | IDs persist to Postgres |
| 003 Load Balancing | ✅ Complete | nginx + 3 generators |
| 004 Monitoring | ⚠️ Partial | Basic HTML only, no JS polling |
| 005 Infrastructure | ✅ Complete | docker-compose works |

## Next Phase
→ Phase 300 — Coding
