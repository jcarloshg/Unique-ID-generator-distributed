-- Migration: 001_initial_schema.sql
-- Enable UUID extension (optional, for future use)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main table for storing generated IDs
CREATE TABLE IF NOT EXISTS generated_ids (
    -- 64-bit Snowflake ID (primary key)
    id BIGINT PRIMARY KEY,

    -- Timestamp extracted from ID (for efficient time-based queries)
    timestamp_ms BIGINT NOT NULL,

    -- Datacenter identifier (0-31)
    datacenter_id SMALLINT NOT NULL
        CHECK (datacenter_id BETWEEN 0 AND 31),

    -- Machine identifier within datacenter (0-31)
    machine_id SMALLINT NOT NULL
        CHECK (machine_id BETWEEN 0 AND 31),

    -- Sequence number at time of generation (0-4095)
    sequence_num SMALLINT NOT NULL
        CHECK (sequence_num BETWEEN 0 AND 4095),

    -- Wall-clock time when record was inserted
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Optional metadata as JSONB
    metadata JSONB DEFAULT '{}'
);

-- Index for time-based queries (descending order for recent first)
CREATE INDEX IF NOT EXISTS idx_generated_ids_timestamp
    ON generated_ids(timestamp_ms DESC);

-- Index for datacenter/machine queries
CREATE INDEX IF NOT EXISTS idx_generated_ids_datacenter_machine
    ON generated_ids(datacenter_id, machine_id);

-- Index for generated_at queries
CREATE INDEX IF NOT EXISTS idx_generated_ids_generated_at
    ON generated_ids(generated_at DESC);

-- Composite index for time-range + datacenter queries
CREATE INDEX IF NOT EXISTS idx_generated_ids_timestamp_datacenter
    ON generated_ids(timestamp_ms DESC, datacenter_id);
