# Phase 200 — Design

## Overview
The Design phase transforms frozen planning artifacts into a detailed technical blueprint. It produces executable contracts, architecture diagrams, and implementation-ready specifications.

## Phase Structure

```
docs/200.design/
├── README.md                    ← You are here
├── 01-architecture/            ← System architecture
├── 02-hexagonal/              ← Hexagonal architecture
├── 03-database/                ← Database schema
├── 04-nginx/                   ← Nginx configuration
└── 05-deployment/              ← Deployment specs
```

## Phase Steps

| Step | Name | Description |
|------|------|-------------|
| 1 | System Architecture | C4 Level 3+ diagrams, component interactions |
| 2 | Hexagonal Architecture | Ports & adapters, domain/infrastructure split |
| 3 | Database Schema | PostgreSQL schema, migrations |
| 4 | Nginx Configuration | Load balancing, health checks |
| 5 | Deployment Specifications | Docker, docker-compose, resource sizing |

## Prerequisites
- [ ] Phase 100 (Planning) complete
- [ ] OpenAPI contracts frozen
- [ ] ADRs signed off
- [ ] NFRs validated

## Deliverables

### Architecture
- `01-architecture/201.system-architecture.md` — Complete system design ✅
- `01-architecture/component-diagrams.md` — Detailed component diagrams (TBD)

### Hexagonal Architecture
- `02-hexagonal/202.hexagonal-architecture.md` — Hexagonal architecture ✅
- `02-hexagonal/domain-model.md` — Domain entities and services (TBD)
- `02-hexagonal/ports.md` — Port interfaces (TBD)

### Database
- `03-database/203.database-schema.md` — Database schema ✅
- `03-database/migrations/` — SQLAlchemy migrations (TBD)

### Nginx
- `04-nginx/204.nginx-configuration.md` — Complete nginx configuration ✅

### Deployment
- `05-deployment/205.deployment-specs.md` — Deployment specifications ✅
- `05-deployment/docker-compose.yml` — Local development (in docker-compose)

## Key Design Decisions

### Architecture Pattern
**Hexagonal (Ports & Adapters)**
- Domain: Pure Snowflake ID generation logic
- Ports: IClock, IIdPersistence, IHealthService
- Adapters: ClockService, PostgresRepository, HttpController

### Database Design
- Single `generated_ids` table
- Async writes with batch insert
- Connection pooling with asyncpg

### Nginx Strategy
- Round-robin load balancing
- Health check on /health endpoint
- 5-second timeout for upstream

## Status
- [x] Phase 200 initiated
- [x] All sub-phases created
- [x] All deliverables complete ✅

## Next Phase
→ Phase 250 — Epics & Tasks
