# Phase 203 — Database Schema

## Overview
Design the PostgreSQL database schema and migration strategy.

## Objectives
- Define `generated_ids` table schema
- Design indexes for common queries
- Create migration scripts
- Define async write patterns

## Deliverables

### Core Documents
- `schema.sql` — PostgreSQL DDL
- `migrations/001_initial_schema.sql` — Initial migration
- `async-write-design.md` — Async batch insert design
- `connection-pooling.md` — Pool sizing and config

## Schema

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

CREATE INDEX idx_timestamp ON generated_ids(timestamp_ms DESC);
CREATE INDEX idx_dc_machine ON generated_ids(datacenter_id, machine_id);
```

## Status
- [ ] Initiated
- [ ] In progress
- [ ] Complete
