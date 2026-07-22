"""OpenDoser tank model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Tank:
    """Represents a dosing or water tank."""

    id: str
    name: str

    #
    # Capacity
    #

    volume_liters: float

    #
    # Current state
    #

    level_liters: float = 0.0

    #
    # Configuration
    #

    minimum_level_liters: float = 0.5

    enabled: bool = True

    def fill_percent(self) -> float:
        """Return the fill level in percent."""

        if self.volume_liters <= 0:
            return 0.0

        return (self.level_liters / self.volume_liters) * 100.0

    def free_volume(self) -> float:
        """Return the remaining free volume."""

        return max(0.0, self.volume_liters - self.level_liters)

    def is_empty(self) -> bool:
        """Return True if the tank is empty."""

        return self.level_liters <= 0.0

    def needs_refill(self) -> bool:
        """Return True if the tank should be refilled."""

        return self.level_liters <= self.minimum_level_liters

    def can_dispense(self, amount_liters: float) -> bool:
        """Return True if the requested amount can be dispensed."""

        return (
            self.enabled
            and amount_liters > 0
            and self.level_liters >= amount_liters
        )

    def dispense(self, amount_liters: float) -> bool:
        """Dispense liquid from the tank."""

        if not self.can_dispense(amount_liters):
            return False

        self.level_liters -= amount_liters

        return True

    def refill(self) -> None:
        """Fill the tank to its maximum capacity."""

        self.level_liters = self.volume_liters