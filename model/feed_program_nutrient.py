"""Feed program nutrient configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FeedProgramNutrient:
    """Defines one nutrient used for EC correction."""

    #
    # Nutrient identifier.
    #

    nutrient_id: str

    #
    # Relative contribution to the desired EC increase.
    #
    # The ratio does NOT represent the dosing volume.
    #
    # Example:
    #
    #   Grow A (ratio=2)
    #   Grow B (ratio=1)
    #
    # means Grow A contributes two parts of the target EC increase,
    # while Grow B contributes one part.
    #
    # The actual dosing volume depends on the nutrient strength.
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