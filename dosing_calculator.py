"""OpenDoser dosing calculator."""

from __future__ import annotations

from .model.nutrient import Nutrient


class DosingCalculator:
    """Calculates dosing volumes."""

    def calculate_volume(
        self,
        nutrient: Nutrient,
        delta: float,
        water_volume_liters: float,
        ratio: float = 1.0,
    ) -> float:
        """Calculate the required dosing volume."""

        if not nutrient.enabled:
            return 0.0

        if nutrient.strength <= 0:
            return 0.0

        if delta <= 0:
            return 0.0

        if water_volume_liters <= 0:
            return 0.0

        volume = (
            delta
            * water_volume_liters
            / nutrient.strength
        )

        volume *= ratio

        return nutrient.clamp_volume(
            volume,
        )