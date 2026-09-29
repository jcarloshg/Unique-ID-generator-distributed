# ADR-003: PostgreSQL for Persistence

## Status
Accepted

## Context
We need a database to persist generated IDs for auditing and traceability. The persistence layer is optional but required for audit compliance.

## Decision
We will use **PostgreSQL** as the persistence database.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL | ACID compliance, team expertise, JSON support, reliable | Single instance (no HA), additional resource cost |
| MySQL | Widely used, good performance | Less feature-rich than PostgreSQL |
| MongoDB | Flexible schema, horizontal scaling | No ACID for transactions |
| Redis | Extremely fast, in-memory | Data loss risk on restart, not for audit trail |

## Decision Rationale
1. **ACID compliance** — Critical for audit trail integrity
2. **Team expertise** — Strong PostgreSQL knowledge
3. **Reliability** — Proven RDBMS with excellent consistency guarantees
4. **Optional persistence** — Service can run without PostgreSQL; IDs still generated

## Consequences

### Positive
- ACID guarantees for audit trail
- JSONB support for metadata storage
- Standard SQL for queries
- Well-understood backup/recovery procedures

### Negative
- Single instance is a single point of failure
- Additional resource usage (~512MB RAM)
- Network latency added to async persistence writes

## Schema Design

```sql
CREATE TABLE generated_ids (
    id BIGINT PRIMARY KEY,
    timestamp_ms BIGINT NOT NULL,
    datacenter_id SMALLINT NOT NULL,
    machine_id SMALLINT NOT NULL,
    sequence_num SMALLINT NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_generated_ids_timestamp ON generated_ids(timestamp_ms);
CREATE INDEX idx_generated_ids_datacenter_machine ON generated_ids(datacenter_id, machine_id);
```

## Implementation Notes
- Use **async** writes to avoid blocking ID generation
- Implement retry logic with exponential backoff
- If PostgreSQL is unavailable, continue generating IDs (degrade gracefully)
- Connection pooling with **asyncpg** or **SQLAlchemy async**
