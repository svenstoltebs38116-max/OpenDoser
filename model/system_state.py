"""Current system state."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SystemState:
    """Represents the current measured system state."""

    ph: float | None = None

    ec: float | None = None

    temperature: float | None = None

    tds: float | None = None

    salinity: float | None = None

    @property
    def available(self) -> bool:
        """Return True if the required sensors are available."""

        return (
            self.ph is not None
            and self.ec is not None
            and self.temperature is not None
        )