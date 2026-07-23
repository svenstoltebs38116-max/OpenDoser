"""Feed program nutrient configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FeedProgramNutrient:
    """Defines one nutrient used for EC correction."""

    #
    # Nutrient
    #

    nutrient_id: str

    #
    # Relative mixing ratio.
    #
    # Examples:
    #
    #   1 : 1
    #   2 : 1
    #   3 : 2 : 1
    #
    # Only the proportion between nutrients matters.
    #

    ratio: float = 1.0

    #
    # Execution order.
    #
    # Lower values are executed first.
    #

    priority: int = 100

    enabled: bool = True

    @property
    def valid(self) -> bool:
        """Return whether this entry can be used."""

        return (
            self.enabled
            and self.ratio > 0
        )

    def to_dict(self) -> dict:
        """Serialize the configuration."""

        return {
            "nutrient_id": self.nutrient_id,
            "ratio": self.ratio,
            "priority": self.priority,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "FeedProgramNutrient":
        """Deserialize the configuration."""

        return cls(
            nutrient_id=data["nutrient_id"],
            ratio=data.get(
                "ratio",
                1.0,
            ),
            priority=data.get(
                "priority",
                100,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
        )