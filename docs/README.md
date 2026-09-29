# Unique ID Generator Distributed — Documentation

## Project Overview

A distributed unique ID generation service inspired by Twitter Snowflake. Generates globally unique, time-ordered, 64-bit numerical IDs at 10,000+ per second across 3 generator instances with nginx load balancing and optional PostgreSQL persistence.

## Documentation Structure

```
docs/
├── README.md                    ← Project documentation index
├── 00.defining.md              ← Defining phase output
│
├── 100.planning/               ← Planning Phase
│   ├── README.md               ← Planning index
│   ├── 101-business-context/   ← Business context
│   ├── 102-technical/          ← Technical requirements
│   │   ├── adr/                ← Architecture Decision Records
│   │   └── diagrams/           ← C4 diagrams
│   ├── 103-functional/         ← Functional requirements
│   │   └── contracts/          ← OpenAPI spec
│   └── 104-nfr/                 ← Non-functional requirements
│
├── 200.design/                  ← Design Phase
│   ├── README.md               ← Design index
│   ├── 01-architecture/        ← System architecture
│   ├── 02-hexagonal/           ← Hexagonal architecture
│   ├── 03-database/            ← Database schema
│   ├── 04-nginx/               ← Nginx configuration
│   └── 05-deployment/          ← Deployment specs
│
├── 250.epics/                   ← Epics & Tasks Phase
│   ├── README.md               ← Epics index
│   ├── epic-001-generator-core/
│   ├── epic-002-persistence/
│   ├── epic-003-load-balancing/
│   ├── epic-004-monitoring/
│   └── epic-005-infrastructure/
│
├── 300.coding/                  ← Coding Phase
│   ├── README.md               ← Coding index
│   ├── 01-scaffolding/
│   ├── 02-generator/
│   ├── 03-nginx/
│   ├── 04-postgres/
│   ├── 05-dashboard/
│   └── 06-tests/
│
└── 400.testing/                 ← Testing Phase
    ├── README.md               ← Testing index
    ├── 01-unit/
    ├── 02-integration/
    ├── 03-contract/
    ├── 04-performance/
    └── 05-chaos/
```

## Phase Summary

| Phase | Name | Status | Description |
|-------|------|--------|-------------|
| 00 | Defining | Complete | Business context and requirements |
| 100 | Planning | Complete | ADRs, APIs, NFRs, diagrams |
| 200 | Design | Pending | Architecture and schemas |
| 250 | Epics & Tasks | Pending | Work breakdown |
| 300 | Coding | Pending | Implementation |
| 400 | Testing | Pending | QA and certification |

## Key NFRs

| Requirement | Target |
|-------------|--------|
| Throughput | ≥ 10,000 IDs/second |
| Latency | P99 < 50ms |
| Availability | 99.9% |
| CAP | CP (Consistency) |
| RPO | 0 (no data loss) |
| RTO | < 1 minute |

## Technology Stack

| Component | Technology |
|-----------|------------|
| Load Balancer | nginx |
| Generator | Python (FastAPI) |
| Database | PostgreSQL |
| Dashboard | Vite + React |
| Container | Docker |

## ID Structure (64 bits)

```
| Sign (1) | Timestamp (41) | Datacenter (5) | Machine (5) | Sequence (12) |
```

## Quick Links

- [Defining Document](00.defining.md)
- [OpenAPI Specification](100.planning/103-functional/contracts/openapi.yaml)
- [Architecture Diagrams](100.planning/102-technical/diagrams/)
- [ADRs](100.planning/102-technical/adr/)
