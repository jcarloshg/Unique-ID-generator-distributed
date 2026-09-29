"""ID Generator Service - Domain Service."""

import structlog
from typing import Protocol

from generator.domain.models.snowflake_id import SnowflakeId


class Clock(Protocol):
    """Clock port for time abstraction."""

    def now_ms(self) -> int:
        """Return current time in milliseconds."""
        ...


class ClockBackwardsError(Exception):
    """Raised when clock moves backwards."""

    def __init__(self, expected_ms: int, actual_ms: int) -> None:
        self.expected_ms = expected_ms
        self.actual_ms = actual_ms
        super().__init__(f"Clock moved backwards: expected {expected_ms}, got {actual_ms}")


class IdGeneratorService:
    """Snowflake ID Generator domain service.

    Generates unique 64-bit IDs using a Snowflake-style algorithm.
    Thread-safe for concurrent access within a single process.
    """

    def __init__(
        self,
        clock: Clock,
        datacenter_id: int,
        machine_id: int,
    ) -> None:
        if not 0 <= datacenter_id <= SnowflakeId.MAX_DATACENTER_ID:
            raise ValueError(
                f"datacenter_id must be 0-{SnowflakeId.MAX_DATACENTER_ID}, "
                f"got {datacenter_id}"
            )
        if not 0 <= machine_id <= SnowflakeId.MAX_MACHINE_ID:
            raise ValueError(
                f"machine_id must be 0-{SnowflakeId.MAX_MACHINE_ID}, got {machine_id}"
            )

        self._clock = clock
        self._datacenter_id = datacenter_id
        self._machine_id = machine_id
        self._sequence = 0
        self._last_timestamp_ms = 0
        self._lock = structlog.get_logger()

    def generate_id(self) -> SnowflakeId:
        """Generate a unique Snowflake ID.

        Returns:
            SnowflakeId: A unique 64-bit ID

        Raises:
            ClockBackwardsError: If system clock moved backwards
        """
        timestamp_ms = self._clock.now_ms()

        if timestamp_ms < self._last_timestamp_ms:
            raise ClockBackwardsError(
                expected_ms=self._last_timestamp_ms,
                actual_ms=timestamp_ms,
            )

        if timestamp_ms == self._last_timestamp_ms:
            self._sequence = (self._sequence + 1) & SnowflakeId.MAX_SEQUENCE
            if self._sequence == 0:
                self._lock.warning(
                    "sequence_overflow_waiting",
                    last_timestamp=self._last_timestamp_ms,
                )
                while self._clock.now_ms() == self._last_timestamp_ms:
                    pass
                timestamp_ms = self._clock.now_ms()
                self._sequence = 0
        else:
            self._sequence = 0

        self._last_timestamp_ms = timestamp_ms

        id_value = (
            ((timestamp_ms - SnowflakeId.EPOCH) << SnowflakeId.TIMESTAMP_SHIFT)
            | (self._datacenter_id << SnowflakeId.DATACENTER_SHIFT)
            | (self._machine_id << SnowflakeId.MACHINE_SHIFT)
            | self._sequence
        )

        return SnowflakeId(value=id_value)
