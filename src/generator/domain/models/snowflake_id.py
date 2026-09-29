"""Snowflake ID - Domain Model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SnowflakeId:
    """64-bit Snowflake ID.

    Bit layout (from most significant to least significant):
    - Bits 63-22: Timestamp (42 bits) - milliseconds since epoch
    - Bits 21-17: Datacenter ID (5 bits) - 0-31
    - Bits 16-12: Machine ID (5 bits) - 0-31
    - Bits 11-0: Sequence (12 bits) - 0-4095

    Total: 64 bits
    """

    value: int

    TIMESTAMP_BITS = 42
    DATACENTER_BITS = 5
    MACHINE_BITS = 5
    SEQUENCE_BITS = 12

    TIMESTAMP_SHIFT = DATACENTER_BITS + MACHINE_BITS + SEQUENCE_BITS
    DATACENTER_SHIFT = MACHINE_BITS + SEQUENCE_BITS
    MACHINE_SHIFT = SEQUENCE_BITS

    MAX_DATACENTER_ID = (1 << DATACENTER_BITS) - 1
    MAX_MACHINE_ID = (1 << MACHINE_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    EPOCH = 1609459200000

    def __post_init__(self) -> None:
        if not 0 <= self.value < (1 << 64):
            raise ValueError(f"ID must be a 64-bit integer, got {self.value}")

    @property
    def timestamp_ms(self) -> int:
        """Extract timestamp in milliseconds from ID."""
        return (self.value >> self.TIMESTAMP_SHIFT) + self.EPOCH

    @property
    def datacenter_id(self) -> int:
        """Extract datacenter ID from ID."""
        return (self.value >> self.DATACENTER_SHIFT) & self.MAX_DATACENTER_ID

    @property
    def machine_id(self) -> int:
        """Extract machine ID from ID."""
        return (self.value >> self.MACHINE_SHIFT) & self.MAX_MACHINE_ID

    @property
    def sequence(self) -> int:
        """Extract sequence number from ID."""
        return self.value & self.MAX_SEQUENCE

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary representation."""
        return {
            "id": self.value,
            "timestamp_ms": self.timestamp_ms,
            "datacenter_id": self.datacenter_id,
            "machine_id": self.machine_id,
            "sequence": self.sequence,
        }
