# C4 Container Diagram — Level 2

## Context
This diagram shows the high-level architecture of the Unique ID Generator System and how data flows between components.

## Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Client Services                                    │
│  (Any internal service requiring unique IDs)                                │
│                                                                              │
│  Examples: Order Service, User Service, Transaction Service                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP GET /generate
                                    │ { "id": 1825478541164436481 }
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Unique ID Generator System                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        nginx (Load Balancer)                         │    │
│  │                         Port: 80                                     │    │
│  │                                                                       │    │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │    │
│  │   │  Generator   │  │  Generator   │  │  Generator   │               │    │
│  │   │    :5001     │◄─┤    :5002     │◄─┤    :5003     │               │    │
│  │   │  (Python)    │  │  (Python)    │  │  (Python)    │               │    │
│  │   └─────────────┘  └─────────────┘  └─────────────┘               │    │
│  │         ▲                ▲                ▲                         │    │
│  └─────────┼────────────────┼────────────────┼─────────────────────────┘    │
│            │                │                │                                 │
│            │                │                │                                  │
│  ┌─────────▼────────────────▼────────────────▼─────────────────────────┐    │
│  │                       PostgreSQL                                     │    │
│  │                        Port: 5432                                    │    │
│  │                   (Optional Persistence)                             │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Vite Dashboard                                   │    │
│  │                       Port: 3000                                     │    │
│  │              (Health Monitoring & Metrics)                          │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Inventory

| Component | Technology | Port | Purpose | Data Flow |
|-----------|------------|------|---------|-----------|
| nginx | nginx | 80 | Load balancing | Routes /generate to generators |
| Generator 1 | Python/FastAPI | 5001 | ID generation | Receives requests, generates IDs |
| Generator 2 | Python/FastAPI | 5002 | ID generation | Receives requests, generates IDs |
| Generator 3 | Python/FastAPI | 5003 | ID generation | Receives requests, generates IDs |
| PostgreSQL | PostgreSQL | 5432 | Persistence | Stores generated IDs (async) |
| Dashboard | Vite + React | 3000 | Monitoring | Polls /health endpoints |

## External Dependencies

| Dependency | Type | Purpose |
|-----------|------|---------|
| Client Services | Internal consumer | Request IDs via HTTP |
| NTP Server | External | Clock synchronization |

## Security Boundaries

| Boundary | Access Control |
|----------|----------------|
| nginx:80 | Public to internal network |
| Generator ports (5001-5003) | Blocked from external; only nginx can access |
| PostgreSQL:5432 | Blocked from external; only generators can access |
| Dashboard:3000 | Internal access for ops team |

## Deployment

| Environment | nginx | Generators | PostgreSQL | Dashboard |
|-------------|-------|------------|------------|-----------|
| Local (docker-compose) | 1 | 3 | 1 | 1 |
| Production (planned) | 1 | 3 | 1 | 1 |

## Scalability Characteristics

| Component | Scales? | Method |
|-----------|---------|--------|
| nginx | No | Single instance (internal SPOF) |
| Generator | Yes (horizontally) | Add more instances; update nginx config |
| PostgreSQL | No (single instance) | Vertical scaling; future: read replicas |
| Dashboard | Yes | Stateless; multiple instances behind LB |
