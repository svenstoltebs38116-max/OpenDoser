"""OpenDoser nutrient model."""

from __future__ import annotations

from dataclasses import dataclass

from .nutrient_role import NutrientRole


@dataclass(slots=True)
class Nutrient:
    """Represents a liquid nutrient or additive."""

    #
    # Identity
    #

    id: str
    name: str

    #
    # Compatibility
    #
    # Will be removed once the migration to FeedProgram is complete.
    #

    role: NutrientRole = NutrientRole.CUSTOM

    #
    # Hardware
    #

    pump_id: str = ""
    tank_id: str = ""

    #
    # Dosing
    #

    strength: float = 0.0

    minimum_dose_ml: float = 0.5
    maximum_dose_ml: float = 250.0

    enabled: bool = True

    def required_volume(
        self,
        delta: float,
        water_volume_liters: float,
    ) -> float:
        """Return the required dose in ml."""

        if not self.enabled:
            return 0.0

        if delta <= 0:
            return 0.0

        if water_volume_liters <= 0:
            return 0.0

        if self.strength <= 0:
            return 0.0

        volume = (
            delta * water_volume_liters
        ) / self.strength

        volume = max(
            self.minimum_dose_ml,
            volume,
        )

        volume = min(
            volume,
            self.maximum_dose_ml,
        )

        return volume