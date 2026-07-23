"""OpenDoser nutrient model."""

from __future__ import annotations

from dataclasses import dataclass

from .nutrient_role import NutrientRole


@dataclass(slots=True)
class Nutrient:
    """Represents a liquid nutrient or additive."""

    #
    # Identity
    #

    id: str
    name: str

    #
    # Compatibility
    #

    role: NutrientRole = NutrientRole.CUSTOM

    #
    # Hardware
    #

    pump_id: str = ""
    tank_id: str = ""

    #
    # Dosing
    #

    #
    # EC or pH change produced by 1 ml of this nutrient
    # in 1 liter of water.
    #
    # Example:
    #
    #   strength = 0.10
    #
    # means:
    #
    #   1 ml raises EC by 0.10 mS/cm
    #   in 1 liter of water.
    #

    strength: float = 0.0

    minimum_dose_ml: float = 0.5
    maximum_dose_ml: float = 250.0

    enabled: bool = True

    def clamp_volume(
        self,
        volume_ml: float,
    ) -> float:
        """Clamp a calculated dose to the configured limits."""

        if not self.enabled:
            return 0.0

        if volume_ml <= 0:
            return 0.0

        volume_ml = max(
            self.minimum_dose_ml,
            volume_ml,
        )

        volume_ml = min(
            self.maximum_dose_ml,
            volume_ml,
        )

        return volume_ml

    def to_dict(self) -> dict:
        """Serialize the nutrient."""

        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "pump_id": self.pump_id,
            "tank_id": self.tank_id,
            "strength": self.strength,
            "minimum_dose_ml": self.minimum_dose_ml,
            "maximum_dose_ml": self.maximum_dose_ml,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "Nutrient":
        """Deserialize a nutrient."""

        role = data.get(
            "role",
            NutrientRole.CUSTOM.value,
        )

        return cls(
            id=data["id"],
            name=data["name"],
            role=NutrientRole(role),
            pump_id=data.get("pump_id", ""),
            tank_id=data.get("tank_id", ""),
            strength=data.get("strength", 0.0),
            minimum_dose_ml=data.get(
                "minimum_dose_ml",
                0.5,
            ),
            maximum_dose_ml=data.get(
                "maximum_dose_ml",
                250.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
        )