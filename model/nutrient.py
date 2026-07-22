"""OpenDoser nutrient model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Nutrient:
    """Represents a liquid nutrient or additive."""

    id: str
    name: str

    #
    # Hardware
    #

    pump_id: str
    tank_id: str

    #
    # Dosing characteristics
    #

    strength: float

    enabled: bool = True

    minimum_dose_ml: float = 0.5

    maximum_dose_ml: float = 250.0

    def required_volume(
        self,
        delta: float,
        water_volume_liters: float,
    ) -> float:
        """Calculate the required dosing volume in ml.

        strength defines how much one ml changes the measured value
        per liter of water.
        """

        if (
            not self.enabled
            or self.strength <= 0
            or water_volume_liters <= 0
            or delta <= 0
        ):
            return 0.0

        volume = (
            delta * water_volume_liters
        ) / self.strength

        return max(
            self.minimum_dose_ml,
            min(volume, self.maximum_dose_ml),
        )