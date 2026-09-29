"""System Clock - Infrastructure Adapter."""

import time

from generator.domain.ports.clock import IClock


class SystemClock(IClock):
    """System clock implementation using time.time()."""

    def now_ms(self) -> int:
        """Return current time in milliseconds."""
        return int(time.time() * 1000)
