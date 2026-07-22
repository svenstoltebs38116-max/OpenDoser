"""OpenDoser nutrient roles."""

from __future__ import annotations

from enum import StrEnum


class NutrientRole(StrEnum):
    """Logical role of a nutrient."""

    PH_UP = "ph_up"
    PH_DOWN = "ph_down"

    EC = "ec"

    CALMAG = "calmag"

    MICRO = "micro"
    GROW = "grow"
    BLOOM = "bloom"

    CUSTOM = "custom"