# C4 Component Diagram — Generator Service

## Context
This diagram shows the internal component structure of a single Generator service instance.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           nginx (External)                                   │
│                      HTTP Client (Load Balancer)                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP Request
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Generator Service (Python/FastAPI)                        │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      IDController (Flask/FastAPI)                    │    │
│  │                                                                       │    │
│  │   GET /generate  ────────►  generate_id()                           │    │
│  │   GET /health    ────────►  get_health()                             │    │
│  │   GET /metrics   ────────►  get_metrics()                            │    │
│  │                                                                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      IdGeneratorService (Domain)                     │    │
│  │                                                                       │    │
│  │   Responsibilities:                                                 │    │
│  │   - Generate Snowflake IDs                                          │    │
│  │   - Manage sequence counter                                          │    │
│  │   - Handle clock edge cases                                         │    │
│  │   - Ensure ID uniqueness                                            │    │
│  │                                                                       │    │
│  │   Methods:                                                          │    │
│  │   - generate_id() -> int                                            │    │
│  │   - get_datacenter_id() -> int                                      │    │
│  │   - get_machine_id() -> int                                         │    │
│  │                                                                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                    ┌─────────────────┴─────────────────┐                     │
│                    │                                   │                       │
│                    ▼                                   ▼                       │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐       │
│  │   ClockService (Infrastructure) │       │  IdRepository (Infrastructure) │       │
│  │                               │       │                             │       │
│  │   - get_current_time_ms()     │       │   - persist_id(id, meta)   │       │
│  │   - get_epoch_offset()        │       │   - get_count()             │       │
│  │   - validate_monotonic()     │       │                             │       │
│  │                               │       │   Implements Port:          │       │
│  │   Implements Port:            │       │   IIdPersistence            │       │
│  │   IClock                      │       │                             │       │
│  └─────────────────────────────┘       └─────────────────────────────┘       │
│                                                              │                 │
│                                                              ▼                 │
│                                               ┌─────────────────────────────┐ │
│                                               │    PostgreSQL (External)    │ │
│                                               │                             │ │
│                                               │  generated_ids table        │ │
│                                               │  - id (PK)                  │ │
│                                               │  - timestamp_ms              │ │
│                                               │  - datacenter_id            │ │
│                                               │  - machine_id                │ │
│                                               │  - sequence_num              │ │
│                                               │  - generated_at              │ │
│                                               └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### IDController
- Handles HTTP requests/responses
- Input validation
- Error handling (converts exceptions to HTTP responses)
- Routes requests to domain services

### IdGeneratorService (Domain)
- Pure business logic for ID generation
- No external dependencies
- Snowflake algorithm implementation
- Sequence number management
- Timestamp validation

### ClockService (Infrastructure)
- Abstracts system clock for testability
- Provides high-resolution timestamp
- Validates clock monotonicity
- Implements IClock port

### IdRepository (Infrastructure)
- Persists generated IDs to PostgreSQL
- Async write to avoid blocking generation
- Implements IIdPersistence port
- Handles connection pooling

## Port Interfaces

### IClock (Domain Interface)
```python
interface IClock:
    def get_current_time_ms() -> int
    def get_epoch() -> int
```

### IIdPersistence (Domain Interface)
```python
interface IIdPersistence:
    async def persist_id(id: int, metadata: dict) -> None
    async def get_count() -> int
```

## Data Flow: Generate ID

```
1. Controller receives GET /generate
2. Controller calls IdGeneratorService.generate_id()
3. IdGeneratorService asks ClockService for current time
4. IdGeneratorService checks sequence number
5. If sequence < 4096: increment and return
6. If sequence >= 4096: wait for next millisecond
7. IdGeneratorService builds 64-bit ID from components
8. Controller returns { "id": <value> }
9. (Async) Controller calls IdRepository.persist_id()
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Domain service has no external deps | Testable, pure business logic |
| Clock abstracted for testability | Enables deterministic testing |
| Async persistence | Doesn't block ID generation |
| Single domain service | Simple, focused responsibility |
