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
- `01-architecture/system-architecture.md` — Complete system design
- `01-architecture/component-diagrams.md` — Detailed component diagrams

### Hexagonal Architecture
- `02-hexagonal/domain-model.md` — Domain entities and services
- `02-hexagonal/ports.md` — Port interfaces
- `02-hexagonal/adapters.md` — Adapter implementations

### Database
- `03-database/schema.sql` — PostgreSQL schema
- `03-database/migrations/` — Flyway/SQLAlchemy migrations

### Nginx
- `04-nginx/nginx.conf` — Complete nginx configuration
- `04-nginx/upstream.conf` — Upstream configuration

### Deployment
- `05-deployment/docker-compose.yml` — Local development
- `05-deployment/docker/Dockerfile-generator` — Generator Dockerfile
- `05-deployment/resource-sizing.md` — CPU/memory specifications

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
- [ ] Phase 200 initiated
- [ ] All sub-phases created
- [ ] Ready for implementation

## Next Phase
→ Phase 250 — Epics & Tasks
