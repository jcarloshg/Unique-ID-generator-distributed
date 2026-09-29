"""Degradable Repository - Infrastructure Layer.

Wraps a repository with circuit breaker pattern for graceful degradation.
"""

import time
from typing import Optional

import structlog

from generator.domain.models.snowflake_id import SnowflakeId
from generator.domain.ports.persistence import IIdPersistence

logger = structlog.get_logger()


class DegradableRepository:
    """Repository wrapper that degrades gracefully when DB is unavailable.

    When the underlying repository fails:
    - Logs the error but doesn't raise
    - Tracks consecutive failures
    - When threshold reached, marks as degraded and stops trying
    - Periodically checks if DB is back
    """

    def __init__(
        self,
        repository: IIdPersistence,
        failure_threshold: int = 3,
        recovery_interval: float = 5.0,
    ) -> None:
        self._repository = repository
        self._failure_threshold = failure_threshold
        self._recovery_interval = recovery_interval
        self._consecutive_failures = 0
        self._is_degraded = False
        self._last_failure_time: Optional[float] = None

    async def persist(self, snowflake_id: SnowflakeId) -> None:
        """Persist a Snowflake ID with graceful degradation.

        If DB is degraded, this method returns immediately without error.
        """
        if self._is_degraded:
            if self._should_try_recovery():
                await self._check_recovery()
            if self._is_degraded:
                return

        try:
            await self._repository.persist(snowflake_id)
            self._consecutive_failures = 0
        except Exception as e:
            self._handle_failure(e)

    async def persist_batch(self, snowflake_ids: list[SnowflakeId]) -> None:
        """Persist multiple Snowflake IDs with graceful degradation."""
        if self._is_degraded:
            if self._should_try_recovery():
                await self._check_recovery()
            if self._is_degraded:
                return

        try:
            await self._repository.persist_batch(snowflake_ids)
            self._consecutive_failures = 0
        except Exception as e:
            self._handle_failure(e)

    async def is_connected(self) -> bool:
        """Check if the repository is connected."""
        return await self._repository.is_connected()

    def _should_try_recovery(self) -> bool:
        """Check if enough time has passed to try recovery."""
        if self._last_failure_time is None:
            return True
        return (time.monotonic() - self._last_failure_time) >= self._recovery_interval

    async def _check_recovery(self) -> None:
        """Check if the DB has recovered."""
        try:
            if await self._repository.is_connected():
                self._is_degraded = False
                self._consecutive_failures = 0
                logger.info("persistence_recovered")
        except Exception:
            self._last_failure_time = time.monotonic()

    def _handle_failure(self, error: Exception) -> None:
        """Handle a persistence failure."""
        self._consecutive_failures += 1
        self._last_failure_time = time.monotonic()

        if self._consecutive_failures >= self._failure_threshold:
            self._is_degraded = True
            logger.warning(
                "persistence_degraded",
                consecutive_failures=self._consecutive_failures,
                error=str(error),
            )
        else:
            logger.warning(
                "persistence_write_failed",
                consecutive_failures=self._consecutive_failures,
                error=str(error),
            )
