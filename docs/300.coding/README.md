# Phase 300 — Coding

## Overview
The Coding phase implements the frozen design artifacts into working, linter-enforced, observably-instrumented code with automated tests.

## Phase Structure

```
docs/300.coding/
├── README.md                    ← You are here
├── 01-scaffolding/             ← Project setup
├── 02-generator/               ← Python generator service
├── 03-nginx/                   ← Nginx configuration
├── 04-postgres/                ← PostgreSQL setup
├── 05-dashboard/                ← Vite dashboard
└── 06-tests/                   ← Test implementation
```

## Prerequisites
- [ ] Phase 250 (Epics & Tasks) complete
- [ ] All tasks have BDD acceptance criteria
- [ ] Sprint scope defined

## Deliverables

### Source Code
```
src/
├── generator/                   ← Python generator service
│   ├── domain/                  ← Domain layer
│   │   ├── models/              ← Entity classes
│   │   ├── services/            ← Domain services
│   │   └── ports/               ← Port interfaces
│   ├── infrastructure/           ← Infrastructure layer
│   │   ├── adapters/            ← Adapter implementations
│   │   └── persistence/         ← Repository implementations
│   └── interfaces/               ← Transport layer
│       ├── http/                ← FastAPI/Flask controllers
│       └── health/              ← Health check controller
├── nginx/                       ← Nginx configuration
├── postgres/                    ← PostgreSQL migrations
└── dashboard/                   ← Vite React app
```

### Configuration
```
config/
├── generator.yaml              ← Generator configuration
├── nginx.conf                  ← Nginx main config
└── docker-compose.yml           ← Local development
```

### Tests
```
tests/
├── unit/                       ← Domain unit tests
├── integration/                ← Integration tests
└── contracts/                  ← Contract tests
```

## Coding Standards

### Python
- Python 3.11+
- FastAPI or Flask for HTTP
- asyncpg for PostgreSQL
- pytest for testing
- Ruff for linting
- mypy for type checking

### Frontend (Dashboard)
- Vite + React 18
- TypeScript
- TanStack Query for data fetching
- TailwindCSS (optional)

### Infrastructure
- Docker multi-stage builds
- docker-compose for local dev
- Environment variables for config

## Definition of Done

Each task must have:
- [ ] Code implemented
- [ ] Unit tests passing (≥80% coverage on domain)
- [ ] Integration tests passing
- [ ] Lint clean (`ruff check`)
- [ ] Typecheck clean (`mypy`)
- [ ] PR reviewed and merged

## Sprint Cadence

| Sprint | Duration | Focus |
|--------|----------|-------|
| Sprint 1 | 1 week | Project scaffolding, Generator core |
| Sprint 2 | 1 week | Persistence, nginx |
| Sprint 3 | 1 week | Dashboard, integration |
| Sprint 4 | 1 week | Polish, load testing |

## Status
- [ ] Phase 300 initiated
- [ ] Directory structure created
- [ ] Ready for Sprint 1

## Next Phase
→ Phase 400 — Testing
