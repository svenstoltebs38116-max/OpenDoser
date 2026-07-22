"""OpenDoser recipe model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Recipe:
    """A dosing recipe."""

    id: str
    name: str

    #
    # Feed program
    #

    feed_program_id: str | None = None

    #
    # Target values
    #

    target_ph: float = 6.00
    target_ec: float = 1.60

    #
    # Allowed tolerance
    #

    ph_tolerance: float = 0.10
    ec_tolerance: float = 0.05

    #
    # Water information
    #

    target_temperature: float | None = None

    #
    # General settings
    #

    enabled: bool = True

    #
    # Metadata
    #

    description: str = ""

    tags: list[str] = field(default_factory=list)

    def ph_in_range(self, value: float) -> bool:
        """Return True if pH is within tolerance."""

        return (
            self.target_ph - self.ph_tolerance
            <= value
            <= self.target_ph + self.ph_tolerance
        )

    def ec_in_range(self, value: float) -> bool:
        """Return True if EC is within tolerance."""

        return (
            self.target_ec - self.ec_tolerance
            <= value
            <= self.target_ec + self.ec_tolerance
        )