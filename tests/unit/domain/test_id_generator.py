"""Tests for IdGeneratorService."""

from unittest.mock import MagicMock

import pytest

from generator.domain.models.snowflake_id import SnowflakeId
from generator.domain.services.id_generator import ClockBackwardsError, IdGeneratorService


class MockClock:
    """Mock clock for testing."""

    def __init__(self, time_ms: int = 1000) -> None:
        self._time_ms = time_ms

    def now_ms(self) -> int:
        return self._time_ms


class TestIdGeneratorService:
    """Tests for IdGeneratorService."""

    def test_create_with_valid_ids(self) -> None:
        """Test creating service with valid datacenter and machine IDs."""
        clock = MockClock()
        service = IdGeneratorService(
            clock=clock,
            datacenter_id=1,
            machine_id=1,
        )
        assert service is not None

    def test_create_with_invalid_datacenter_id(self) -> None:
        """Test creating service with invalid datacenter ID raises."""
        clock = MockClock()
        with pytest.raises(ValueError, match="datacenter_id"):
            IdGeneratorService(
                clock=clock,
                datacenter_id=32,
                machine_id=1,
            )

    def test_create_with_invalid_machine_id(self) -> None:
        """Test creating service with invalid machine ID raises."""
        clock = MockClock()
        with pytest.raises(ValueError, match="machine_id"):
            IdGeneratorService(
                clock=clock,
                datacenter_id=1,
                machine_id=32,
            )

    def test_generate_id_structure(self) -> None:
        """Test generated ID has correct bit structure."""
        clock = MockClock(time_ms=SnowflakeId.EPOCH + 1000)
        service = IdGeneratorService(
            clock=clock,
            datacenter_id=5,
            machine_id=3,
        )
        snowflake_id = service.generate_id()

        assert snowflake_id.datacenter_id == 5
        assert snowflake_id.machine_id == 3
        assert snowflake_id.sequence == 0
        assert snowflake_id.timestamp_ms == SnowflakeId.EPOCH + 1000

    def test_generate_multiple_ids_increment_sequence(self) -> None:
        """Test that multiple IDs in same millisecond increment sequence."""
        clock = MockClock(time_ms=SnowflakeId.EPOCH + 1000)
        service = IdGeneratorService(
            clock=clock,
            datacenter_id=1,
            machine_id=1,
        )

        ids = [service.generate_id() for _ in range(5)]

        for i, snowflake_id in enumerate(ids):
            assert snowflake_id.sequence == i
        assert len(set(id.value for id in ids)) == 5

    def test_clock_backwards_raises(self) -> None:
        """Test that clock moving backwards raises ClockBackwardsError."""
        clock = MockClock(time_ms=SnowflakeId.EPOCH + 1000)
        service = IdGeneratorService(
            clock=clock,
            datacenter_id=1,
            machine_id=1,
        )
        service.generate_id()

        clock._time_ms = SnowflakeId.EPOCH + 999

        with pytest.raises(ClockBackwardsError):
            service.generate_id()

    def test_unique_ids_across_timestamps(self) -> None:
        """Test that IDs at different timestamps are unique."""
        service = IdGeneratorService(
            clock=MockClock(time_ms=SnowflakeId.EPOCH + 1000),
            datacenter_id=1,
            machine_id=1,
        )
        id1 = service.generate_id()

        service2 = IdGeneratorService(
            clock=MockClock(time_ms=SnowflakeId.EPOCH + 1001),
            datacenter_id=1,
            machine_id=1,
        )
        id2 = service2.generate_id()

        assert id1.value != id2.value

    def test_ids_are_unique_across_datacenters(self) -> None:
        """Test that IDs from different datacenters are unique."""
        clock1 = MockClock(time_ms=SnowflakeId.EPOCH + 1000)
        clock2 = MockClock(time_ms=SnowflakeId.EPOCH + 1000)

        service1 = IdGeneratorService(clock=clock1, datacenter_id=1, machine_id=1)
        service2 = IdGeneratorService(clock=clock2, datacenter_id=2, machine_id=1)

        id1 = service1.generate_id()
        id2 = service2.generate_id()

        assert id1.value != id2.value
        assert id1.datacenter_id == 1
        assert id2.datacenter_id == 2

    def test_ids_are_unique_across_machines(self) -> None:
        """Test that IDs from different machines are unique."""
        clock1 = MockClock(time_ms=SnowflakeId.EPOCH + 1000)
        clock2 = MockClock(time_ms=SnowflakeId.EPOCH + 1000)

        service1 = IdGeneratorService(clock=clock1, datacenter_id=1, machine_id=1)
        service2 = IdGeneratorService(clock=clock2, datacenter_id=1, machine_id=2)

        id1 = service1.generate_id()
        id2 = service2.generate_id()

        assert id1.value != id2.value
        assert id1.machine_id == 1
        assert id2.machine_id == 2
