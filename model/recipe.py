"""OpenDoser recipe model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Recipe:
    """A dosing recipe."""

    #
    # Identity
    #

    id: str
    name: str

    #
    # Feed program
    #

    feed_program_id: str | None = None

    #
    # Target values
    #

    target_ph: float = 6.00
    target_ec: float = 1.60

    #
    # Allowed tolerance
    #

    ph_tolerance: float = 0.10
    ec_tolerance: float = 0.05

    #
    # Water information
    #

    target_temperature: float | None = None

    #
    # General settings
    #

    enabled: bool = True

    #
    # Metadata
    #

    description: str = ""

    tags: list[str] = field(default_factory=list)

    def ph_in_range(
        self,
        value: float,
    ) -> bool:
        """Return True if pH is within tolerance."""

        return (
            self.target_ph - self.ph_tolerance
            <= value
            <= self.target_ph + self.ph_tolerance
        )

    def ec_in_range(
        self,
        value: float,
    ) -> bool:
        """Return True if EC is within tolerance."""

        return (
            self.target_ec - self.ec_tolerance
            <= value
            <= self.target_ec + self.ec_tolerance
        )

    def to_dict(self) -> dict:
        """Serialize the recipe."""

        return {
            "id": self.id,
            "name": self.name,
            "feed_program_id": self.feed_program_id,
            "target_ph": self.target_ph,
            "target_ec": self.target_ec,
            "ph_tolerance": self.ph_tolerance,
            "ec_tolerance": self.ec_tolerance,
            "target_temperature": self.target_temperature,
            "enabled": self.enabled,
            "description": self.description,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> Recipe:
        """Deserialize a recipe."""

        return cls(
            id=data["id"],
            name=data["name"],
            feed_program_id=data.get("feed_program_id"),
            target_ph=data.get("target_ph", 6.00),
            target_ec=data.get("target_ec", 1.60),
            ph_tolerance=data.get("ph_tolerance", 0.10),
            ec_tolerance=data.get("ec_tolerance", 0.05),
            target_temperature=data.get("target_temperature"),
            enabled=data.get("enabled", True),
            description=data.get("description", ""),
            tags=list(data.get("tags", [])),
        )