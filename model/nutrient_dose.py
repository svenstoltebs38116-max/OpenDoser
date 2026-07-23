"""Nutrient dose calculation model."""

from __future__ import annotations

from dataclasses import dataclass

from .nutrient import Nutrient


@dataclass(slots=True)
class NutrientDose:
    """Represents one nutrient participating in a dose calculation."""

    nutrient: Nutrient

    #
    # Relative contribution to the target EC increase.
    #

    ratio: float = 1.0

    @property
    def valid(self) -> bool:
        """Return whether this dose can be calculated."""

        return (
            self.nutrient.enabled
            and self.nutrient.strength > 0
            and self.ratio > 0
        )