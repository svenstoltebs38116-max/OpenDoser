"""OpenDoser recipe item model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RecipeItem:
    """Represents one nutrient entry inside a recipe."""

    #
    # Identity
    #

    nutrient_id: str

    #
    # Target dose
    #

    amount_ml_per_liter: float

    #
    # Metadata
    #

    enabled: bool = True

    def to_dict(self) -> dict:
        """Serialize the recipe item."""

        return {
            "nutrient_id": self.nutrient_id,
            "amount_ml_per_liter": self.amount_ml_per_liter,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "RecipeItem":
        """Deserialize a recipe item."""

        return cls(
            nutrient_id=data["nutrient_id"],
            amount_ml_per_liter=data.get(
                "amount_ml_per_liter",
                0.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
        )