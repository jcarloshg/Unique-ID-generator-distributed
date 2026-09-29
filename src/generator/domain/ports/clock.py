"""Clock Port - Domain Interface."""

from typing import Protocol


class IClock(Protocol):
    """Clock interface for time abstraction.

    This port allows the domain to be independent of system time,
    enabling testing and clock manipulation.
    """

    def now_ms(self) -> int:
        """Return current time in milliseconds since Unix epoch."""
        ...
