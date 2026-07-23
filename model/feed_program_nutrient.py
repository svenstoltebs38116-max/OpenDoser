"""Feed program nutrient configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FeedProgramNutrient:
    """Defines one nutrient used for EC correction."""

    nutrient_id: str

    ratio: float = 1.0

    enabled: bool = True

    def to_dict(self) -> dict:

        return {
            "nutrient_id": self.nutrient_id,
            "ratio": self.ratio,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "FeedProgramNutrient":

        return cls(
            nutrient_id=data["nutrient_id"],
            ratio=data.get(
                "ratio",
                1.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
        )