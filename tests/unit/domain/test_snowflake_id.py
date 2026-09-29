"""Tests for SnowflakeId model."""

import pytest

from generator.domain.models.snowflake_id import SnowflakeId


class TestSnowflakeId:
    """Tests for SnowflakeId dataclass."""

    def test_create_valid_id(self) -> None:
        """Test creating a valid 64-bit ID."""
        snowflake_id = SnowflakeId(value=1)
        assert snowflake_id.value == 1

    def test_create_id_with_max_value(self) -> None:
        """Test creating ID with maximum 64-bit value."""
        max_value = (1 << 64) - 1
        snowflake_id = SnowflakeId(value=max_value)
        assert snowflake_id.value == max_value

    def test_create_id_with_negative_value_raises(self) -> None:
        """Test that negative values raise ValueError."""
        with pytest.raises(ValueError):
            SnowflakeId(value=-1)

    def test_create_id_too_large_raises(self) -> None:
        """Test that values >= 2^64 raise ValueError."""
        with pytest.raises(ValueError):
            SnowflakeId(value=1 << 64)

    def test_extract_timestamp(self) -> None:
        """Test timestamp extraction from ID."""
        timestamp_ms = SnowflakeId.EPOCH + 1000
        id_value = (
            ((timestamp_ms - SnowflakeId.EPOCH) << SnowflakeId.TIMESTAMP_SHIFT)
            | (1 << SnowflakeId.DATACENTER_SHIFT)
            | (1 << SnowflakeId.MACHINE_SHIFT)
            | 0
        )
        snowflake_id = SnowflakeId(value=id_value)
        assert snowflake_id.timestamp_ms == timestamp_ms

    def test_extract_datacenter_id(self) -> None:
        """Test datacenter ID extraction from ID."""
        id_value = (
            (10 << SnowflakeId.TIMESTAMP_SHIFT)
            | (5 << SnowflakeId.DATACENTER_SHIFT)
            | (1 << SnowflakeId.MACHINE_SHIFT)
            | 0
        )
        snowflake_id = SnowflakeId(value=id_value)
        assert snowflake_id.datacenter_id == 5

    def test_extract_machine_id(self) -> None:
        """Test machine ID extraction from ID."""
        id_value = (
            (10 << SnowflakeId.TIMESTAMP_SHIFT)
            | (5 << SnowflakeId.DATACENTER_SHIFT)
            | (3 << SnowflakeId.MACHINE_SHIFT)
            | 0
        )
        snowflake_id = SnowflakeId(value=id_value)
        assert snowflake_id.machine_id == 3

    def test_extract_sequence(self) -> None:
        """Test sequence extraction from ID."""
        id_value = (
            (10 << SnowflakeId.TIMESTAMP_SHIFT)
            | (5 << SnowflakeId.DATACENTER_SHIFT)
            | (3 << SnowflakeId.MACHINE_SHIFT)
            | 42
        )
        snowflake_id = SnowflakeId(value=id_value)
        assert snowflake_id.sequence == 42

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        timestamp_ms = SnowflakeId.EPOCH + 1000
        id_value = (
            ((timestamp_ms - SnowflakeId.EPOCH) << SnowflakeId.TIMESTAMP_SHIFT)
            | (5 << SnowflakeId.DATACENTER_SHIFT)
            | (3 << SnowflakeId.MACHINE_SHIFT)
            | 42
        )
        snowflake_id = SnowflakeId(value=id_value)
        result = snowflake_id.to_dict()

        assert result["id"] == id_value
        assert result["timestamp_ms"] == timestamp_ms
        assert result["datacenter_id"] == 5
        assert result["machine_id"] == 3
        assert result["sequence"] == 42

    def test_id_is_frozen(self) -> None:
        """Test that SnowflakeId is immutable."""
        snowflake_id = SnowflakeId(value=1)
        with pytest.raises(AttributeError):
            snowflake_id.value = 2
