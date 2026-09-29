"""Async PostgreSQL Repository - Infrastructure Adapter."""

import json
import os
from typing import Any

import asyncpg
import structlog

from generator.domain.models.snowflake_id import SnowflakeId

logger = structlog.get_logger()


class AsyncPgRepository:
    """Async PostgreSQL repository for persisting Snowflake IDs."""

    def __init__(
        self,
        dsn: str | None = None,
        min_size: int = 2,
        max_size: int = 10,
    ) -> None:
        self._dsn: str = dsn or os.getenv(  # type: ignore[assignment]
            "POSTGRES_DSN",
            "postgresql://app:changeme@postgres:5432/id_generator",
        )
        self._pool: asyncpg.Pool | None = None
        self._min_size = min_size
        self._max_size = max_size

    async def connect(self) -> None:
        """Create connection pool."""
        self._pool = await asyncpg.create_pool(
            self._dsn,
            min_size=self._min_size,
            max_size=self._max_size,
            command_timeout=30,
        )
        masked_dsn = self._dsn.split("@")[-1] if "@" in self._dsn else "masked"
        logger.info("postgres_connected", dsn=masked_dsn)

    async def close(self) -> None:
        """Close connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("postgres_disconnected")

    async def persist(self, snowflake_id: SnowflakeId) -> None:
        """Persist a single Snowflake ID."""
        if not self._pool:
            raise RuntimeError("Database pool not initialized")

        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO generated_ids
                    (id, timestamp_ms, datacenter_id, machine_id, sequence_num, metadata)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO NOTHING
                """,
                snowflake_id.value,
                snowflake_id.timestamp_ms,
                snowflake_id.datacenter_id,
                snowflake_id.machine_id,
                snowflake_id.sequence,
                json.dumps({}),
            )

    async def persist_batch(self, snowflake_ids: list[SnowflakeId]) -> None:
        """Persist multiple Snowflake IDs in a batch."""
        if not self._pool:
            raise RuntimeError("Database pool not initialized")

        if not snowflake_ids:
            return

        records: list[tuple[int, int, int, int, int, str]] = [
            (
                sid.value,
                sid.timestamp_ms,
                sid.datacenter_id,
                sid.machine_id,
                sid.sequence,
                json.dumps({}),
            )
            for sid in snowflake_ids
        ]

        async with self._pool.acquire() as conn:
            await conn.executemany(
                """
                INSERT INTO generated_ids
                    (id, timestamp_ms, datacenter_id, machine_id, sequence_num, metadata)
                VALUES ($1, $2, $3, $4, $5, $6::jsonb)
                ON CONFLICT (id) DO NOTHING
                """,
                records,
            )

    async def is_connected(self) -> bool:
        """Check if the repository is connected."""
        if not self._pool:
            return False
        try:
            async with self._pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False
