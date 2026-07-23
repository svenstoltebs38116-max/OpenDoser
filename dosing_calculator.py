"""OpenDoser dosing calculator."""

from __future__ import annotations

from .model.calculation_result import CalculationResult
from .model.nutrient import Nutrient
from .model.nutrient_dose import NutrientDose


class DosingCalculator:
    """Calculates dosing volumes."""

    def calculate_ph_volume(
        self,
        nutrient: Nutrient,
        delta: float,
        water_volume_liters: float,
    ) -> CalculationResult:
        """Calculate the required pH dosing volume."""

        return self._calculate_volume(
            nutrient=nutrient,
            delta=delta,
            water_volume_liters=water_volume_liters,
            ratio=1.0,
        )

    def calculate_ec_volumes(
        self,
        nutrient_doses: list[NutrientDose],
        delta: float,
        water_volume_liters: float,
    ) -> dict[str, CalculationResult]:
        """Calculate EC dosing volumes."""

        results: dict[str, CalculationResult] = {}

        valid_doses = [
            dose
            for dose in nutrient_doses
            if dose.valid
        ]

        if not valid_doses:
            return results

        total_ratio = sum(
            dose.ratio
            for dose in valid_doses
        )

        if total_ratio <= 0:
            return results

        for dose in valid_doses:

            result = self._calculate_volume(
                nutrient=dose.nutrient,
                delta=delta,
                water_volume_liters=water_volume_liters,
                ratio=dose.ratio / total_ratio,
            )

            if result.volume_ml <= 0:
                continue

            results[dose.nutrient.id] = result

        return results

    def _calculate_volume(
        self,
        nutrient: Nutrient,
        delta: float,
        water_volume_liters: float,
        ratio: float,
    ) -> CalculationResult:
        """Calculate one dosing volume."""

        result = CalculationResult(
            volume_ml=0.0,
        )

        if not nutrient.enabled:
            result.add_warning(
                "Nutrient is disabled."
            )
            return result

        if nutrient.strength <= 0:
            result.add_warning(
                "Invalid nutrient strength."
            )
            return result

        if delta <= 0:
            return result

        if water_volume_liters <= 0:
            result.add_warning(
                "Invalid water volume."
            )
            return result

        volume = (
            delta
            * water_volume_liters
            / nutrient.strength
        )

        volume *= ratio

        if volume < nutrient.minimum_dose_ml:

            result.volume_ml = nutrient.minimum_dose_ml

            result.add_warning(
                "Minimum dose applied."
            )

            return result

        if volume > nutrient.maximum_dose_ml:

            result.volume_ml = nutrient.maximum_dose_ml

            result.add_warning(
                "Maximum dose applied."
            )

            return result

        result.volume_ml = volume

        return result