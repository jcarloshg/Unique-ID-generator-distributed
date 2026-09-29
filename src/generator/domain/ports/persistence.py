"""Persistence Port - Domain Interface."""

from typing import Protocol

from generator.domain.models.snowflake_id import SnowflakeId


class IIdPersistence(Protocol):
    """Persistence interface for Snowflake IDs.

    This port allows the domain to persist IDs to any backend
    (PostgreSQL, Redis, etc.) without coupling to implementation.
    """

    async def persist(self, snowflake_id: SnowflakeId) -> None:
        """Persist a single Snowflake ID.

        Args:
            snowflake_id: The generated Snowflake ID to persist

        Raises:
            PersistenceError: If the write fails
        """
        ...

    async def persist_batch(self, snowflake_ids: list[SnowflakeId]) -> None:
        """Persist multiple Snowflake IDs in a batch.

        Args:
            snowflake_ids: List of generated Snowflake IDs to persist

        Raises:
            PersistenceError: If the batch write fails
        """
        ...

    async def is_connected(self) -> bool:
        """Check if the persistence layer is connected.

        Returns:
            True if connected, False otherwise
        """
        ...
