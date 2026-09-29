"""Async Write Queue - Infrastructure Layer."""

import asyncio
from dataclasses import dataclass
from typing import Optional

import structlog

from generator.domain.models.snowflake_id import SnowflakeId
from generator.domain.ports.persistence import IIdPersistence

logger = structlog.get_logger()


@dataclass
class IdRecord:
    """Record to be persisted."""
    snowflake_id: SnowflakeId


class AsyncWriteQueue:
    """Async queue for non-blocking ID persistence.

    This queue accepts ID records and asynchronously writes them
    to the persistence layer in batches for efficiency.
    """

    def __init__(
        self,
        repository: IIdPersistence,
        batch_size: int = 100,
        batch_timeout: float = 0.01,
        max_queue_size: int = 10000,
    ) -> None:
        self._repository = repository
        self._batch_size = batch_size
        self._batch_timeout = batch_timeout
        self._queue: asyncio.Queue[IdRecord] = asyncio.Queue(maxsize=max_queue_size)
        self._worker_task: Optional[asyncio.Task[None]] = None
        self._running = False
        self._dropped_count = 0

    async def start(self) -> None:
        """Start the background worker."""
        self._running = True
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("async_write_queue_started", batch_size=self._batch_size)

    async def stop(self) -> None:
        """Stop the background worker and flush remaining items."""
        self._running = False
        if self._worker_task:
            await self._worker_task
        logger.info("async_write_queue_stopped", dropped_count=self._dropped_count)

    def enqueue(self, snowflake_id: SnowflakeId) -> None:
        """Enqueue an ID for async persistence (non-blocking).

        If the queue is full, the ID is dropped and a warning is logged.
        """
        try:
            self._queue.put_nowait(IdRecord(snowflake_id=snowflake_id))
        except asyncio.QueueFull:
            self._dropped_count += 1
            logger.warning(
                "persistence_queue_full_dropping_record",
                dropped_total=self._dropped_count,
            )

    async def _worker(self) -> None:
        """Background worker that processes batches."""
        batch: list[SnowflakeId] = []

        while self._running or not self._queue.empty():
            try:
                record = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=self._batch_timeout,
                )
                batch.append(record.snowflake_id)

                if len(batch) >= self._batch_size:
                    await self._flush(batch)
                    batch = []

            except asyncio.TimeoutError:
                if batch:
                    await self._flush(batch)
                    batch = []
            except Exception as e:
                logger.error("async_write_queue_error", error=str(e))

        if batch:
            await self._flush(batch)

    async def _flush(self, batch: list[SnowflakeId]) -> None:
        """Flush a batch to the repository."""
        try:
            await self._repository.persist_batch(batch)
            logger.debug("batch_persisted", count=len(batch))
        except Exception as e:
            logger.error("batch_persist_failed", error=str(e), count=len(batch))
            self._dropped_count += len(batch)
