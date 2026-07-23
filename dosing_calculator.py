"""OpenDoser dosing calculator."""

from __future__ import annotations

from .model.feed_program_nutrient import FeedProgramNutrient
from .model.nutrient import Nutrient
from .model.system import System


class DosingCalculator:
    """Calculates dosing volumes."""

    def calculate_ph_volume(
        self,
        nutrient: Nutrient,
        delta: float,
        water_volume_liters: float,
    ) -> float:
        """Calculate the required pH dosing volume."""

        return self._calculate_volume(
            nutrient=nutrient,
            delta=delta,
            water_volume_liters=water_volume_liters,
            ratio=1.0,
        )

    def calculate_ec_volumes(
        self,
        system: System,
        nutrients: list[FeedProgramNutrient],
        delta: float,
    ) -> dict[str, float]:
        """Calculate EC dosing volumes for all nutrients."""

        volumes: dict[str, float] = {}

        total_ratio = sum(
            entry.ratio
            for entry in nutrients
        )

        if total_ratio <= 0:
            return volumes

        for entry in nutrients:

            nutrient = system.get_nutrient(
                entry.nutrient_id,
            )

            if nutrient is None:
                continue

            volume = self._calculate_volume(
                nutrient=nutrient,
                delta=delta,
                water_volume_liters=system.water_volume_liters,
                ratio=entry.ratio / total_ratio,
            )

            if volume <= 0:
                continue

            volumes[entry.nutrient_id] = volume

        return volumes

    def _calculate_volume(
        self,
        nutrient: Nutrient,
        delta: float,
        water_volume_liters: float,
        ratio: float,
    ) -> float:
        """Calculate one dosing volume."""

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